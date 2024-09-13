/*
 * SPDX-FileCopyrightText: Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT gpio_steppers

/**
 * @file
 * @brief GPIO driven stepper motors
 */

#include "stepper_common.h"

#include <zephyr/drivers/gpio.h>
#include <zephyr/device.h>
#include <zephyr/kernel.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(stepper_gpio, CONFIG_STEPPER_LOG_LEVEL);

struct stepper_gpio_io {
	const size_t motor;
	const char *const name;
	const size_t num_gpios;
	const struct gpio_dt_spec *const gpios;
};

struct stepper_gpio_config {
	const size_t num_motor;
	const struct stepper_gpio_io *const io;
};

struct stepper_gpio_logic {
	const size_t motor;
	const struct device *const dev;
	struct k_spinlock lock;
	struct k_work_delayable dwork;
	/* TODO: better reuse the API flags here, avoid single booleans */
	bool power_on;		/**< motor power enable status */
	bool running;		/**< running in position or velocity mode */
	bool positive;		/**< running with positive direction */
	bool positioning;	/**< positioning mode, use ustep_move if true */
	uint32_t fstep_spd;	/**< used full-step rotational speed */
	uint32_t ustep_res;	/**< used microstep resolution */
	uint32_t ustep_now;	/**< relative motor position in microsteps */
	uint32_t ustep_move;	/**< microsteps that have to move */
};

struct stepper_gpio_data {
	const size_t num_logic;
	struct stepper_gpio_logic *const logic;
};

static const int stepper_gpio_acbd[STEPPER_USTEP_RES_2]
				  [STEPPER_USTEP_RES_2 * 4]
				  [4] = {
	/*
	 * full-step 1 with: |a|c|b|d| = |+|-|-|-|
	 * full-step 2 with: |a|c|b|d| = |-|+|-|-|
	 * full-step 3 with: |a|c|b|d| = |-|-|+|-|
	 * full-step 4 with: |a|c|b|d| = |-|-|-|+|
	 */
	[STEPPER_USTEP_RES_1 - 1] = {
		[0] = { 1, 0, 0, 0 },
		[1] = { 0, 1, 0, 0 },
		[2] = { 0, 0, 1, 0 },
		[3] = { 0, 0, 0, 1 },
		/* repeat to fill up table with valid values */
		[4] = { 1, 0, 0, 0 },
		[5] = { 0, 1, 0, 0 },
		[6] = { 0, 0, 1, 0 },
		[7] = { 0, 0, 0, 1 },
	},
	/*
	 * half-step 1 with: |a|c|b|d| = |+|-|-|-|
	 * half-step 2 with: |a|c|b|d| = |+|+|-|-|
	 * half-step 3 with: |a|c|b|d| = |-|+|-|-|
	 * half-step 4 with: |a|c|b|d| = |-|+|+|-|
	 * half-step 5 with: |a|c|b|d| = |-|-|+|-|
	 * half-step 6 with: |a|c|b|d| = |-|-|+|+|
	 * half-step 7 with: |a|c|b|d| = |-|-|-|+|
	 * half-step 8 with: |a|c|b|d| = |+|-|-|+|
	 */
	[STEPPER_USTEP_RES_2 - 1] = {
		[0] = { 1, 0, 0, 0 },
		[1] = { 1, 1, 0, 0 },
		[2] = { 0, 1, 0, 0 },
		[3] = { 0, 1, 1, 0 },
		[4] = { 0, 0, 1, 0 },
		[5] = { 0, 0, 1, 1 },
		[6] = { 0, 0, 0, 1 },
		[7] = { 1, 0, 0, 1 },
	},
};

static int stepper_gpio_acbd_poweroff(const struct gpio_dt_spec *gpios)
{
	printk("GPIO: ABCD Power Off\n");
	int ret = 0;

	/* set to standby (not break), power stage FETs to Z-level */
	gpio_flags_t flags[4] = {
		GPIO_OUTPUT_INACTIVE,
		GPIO_OUTPUT_INACTIVE,
		GPIO_OUTPUT_INACTIVE,
		GPIO_OUTPUT_INACTIVE,
	};

	for (uint8_t pin = 0; pin < 4 /* acbd */; pin++) {
		if (!ret) {
			ret = gpio_pin_configure_dt(&gpios[pin], flags[pin]);
		} else {
			break;
		}
	}

	return ret;
}

static int stepper_gpio_acbd_update(const struct gpio_dt_spec *gpios,
				    const uint32_t ustep_res,
				    const uint32_t ustep_now)
{
	//printk("GPIO: ABCD Update\n");
	uint32_t ustep_table;
	uint32_t ustep_number;
	const int *values;
	int ret = 0;

	ustep_table = ustep_res - 1;
	ustep_number = ustep_now & BIT_MASK(ustep_res + 1);
	values = stepper_gpio_acbd[ustep_table][ustep_number];

	for (uint8_t pin = 0; pin < 4; pin++) {
		if (!ret) {
			ret = gpio_pin_set_dt(&gpios[pin], values[pin]);
		} else {
			break;
		}
	}

	return ret;
}

static void stepper_gpio_dworker(struct k_work *work)
{
	//printk("GPIO: DWorker\n");
	const struct k_work_delayable *const dwork = k_work_delayable_from_work(work);
	struct stepper_gpio_logic *const logic = CONTAINER_OF(dwork,
				struct stepper_gpio_logic, dwork);
	const struct device *const dev = logic->dev;
	const struct stepper_gpio_config *const config = dev->config;
	const struct stepper_gpio_io *const io = &config->io[logic->motor];
	int ret = 0;

	K_SPINLOCK(&logic->lock) {

		if (logic->power_on && logic->running && logic->fstep_spd) {

			/* adjust rotational speed by microstep resolution */
			uint32_t ustep_spd = logic->fstep_spd
					   * logic->ustep_res;

			/* either position or velocity mode, change position */
			if (logic->positive) {
				logic->ustep_now++;
			} else {
				logic->ustep_now--;
			}

			/* update GPIO pins with new position */
			ret = stepper_gpio_acbd_update(io->gpios,
						       logic->ustep_res,
						       logic->ustep_now);
			if (ret < 0) {
				/* TODO/FIXME: submit event in API for FAULT */
				LOG_ERR("%s: %s: GPIO update error",
					dev->name, io->name);
			}

			/* decrement microsteps for positioning mode */
			if (logic->positioning && logic->ustep_move) {
				logic->ustep_move--;
			}

			/* no more, stop positioning mode in next round */
			if (logic->positioning && !logic->ustep_move) {
				logic->running = false;
			}

			/* reschedule next round */
			k_work_reschedule(&logic->dwork,
					  K_USEC(USEC_PER_SEC / ustep_spd));

		} else {

			/* stop explicitely */
			logic->running = false;

			/* TODO/FIXME: submit event in API for END ACTION */

			LOG_DBG("%s: motor %u: %s: reach %u (%u)",
				dev->name, io->motor, io->name,
				logic->ustep_now, logic->ustep_now &
				(uint32_t)(BIT_MASK(logic->ustep_res + 1)));
		}
	}
}

static int stepper_gpio_move(const struct device *dev, const uint8_t motor,
			     const struct stepper_action *action)
{
	/* NOTE: motor number already verified in stepper motor API */
	printk("GPIO: Move\n");

	const struct stepper_gpio_config *config = dev->config;
	const struct stepper_gpio_io *const io = &config->io[motor];
	struct stepper_gpio_data *const data = stepper_get_private(dev);
	struct stepper_gpio_logic *const logic = &data->logic[motor];
	int ret = 0;

	__ASSERT_NO_MSG(action != NULL);

	K_SPINLOCK(&logic->lock) {

		if (!logic->power_on) {
			LOG_ERR("%s: %s: power off, do nothing",
				dev->name, io->name);
			ret = -EIO;
			K_SPINLOCK_BREAK;
		}

		if (STEPPER_OP_MODE_GET(action->flags)
				== STEPPER_OP_MODE_POSITION) {

			/* use positioning mode with given microstep moves */
			logic->positioning = true;
			logic->ustep_move = labs(action->value);

		} else if (STEPPER_OP_MODE_GET(action->flags)
				== STEPPER_OP_MODE_VELOCITY) {

			/* use velocity mode with given full-steps / seconds */
			logic->positioning = false;
			logic->fstep_spd = labs(action->value);

		} else {
			LOG_ERR("%s: %s: unsupported action",
				dev->name, io->name);
			ret = -EINVAL;
			K_SPINLOCK_BREAK;
		}

		/* TODO/FIXME: This "hot-swap" of microstep resolution
		 * leads to disturbing "cracks" or "gaps" of the relative
		 * motor position counting. When the microstep resolution
		 * change from up to down or vice versa, any kind of
		 * "count stuffing" have to insert.
		 *
		 * But how? This driver needs a concept for this!
		 */

		logic->ustep_res = STEPPER_USTEP_RES_GET(action->flags);
		logic->positive = action->value > 0 ? true : false;
		logic->running = true;

		ret = k_work_reschedule(&logic->dwork, K_NO_WAIT);
		if (ret >= 0) {
			/* ignore informative result codes */
			ret = 0;
		}
	};

	return ret;
}

static int stepper_gpio_on(const struct device *dev, const uint8_t motor)
{
	printk("GPIO: On\n");
	/* NOTE: motor number already verified in stepper motor API */

	const struct stepper_gpio_config *const config = dev->config;
	const struct stepper_gpio_io *const io = &config->io[motor];
	struct stepper_gpio_data *const data = stepper_get_private(dev);
	struct stepper_gpio_logic *const logic = &data->logic[motor];
	int ret = 0;

	/* TODO/FIXME: handle power cycle as async safety call */
	K_SPINLOCK(&logic->lock) {

		/* TODO/FIXME: support also 2 GPIO pins for |dir|stp| */

		/* check 4 GPIO pins for |a|c|b|d| */
		if (4 != io->num_gpios) {
			LOG_ERR("%s: %s: only 4 GPIO pins supported",
				dev->name, io->name);
			K_SPINLOCK_BREAK;
		}

		ret = stepper_gpio_acbd_update(io->gpios,
					       logic->ustep_res,
					       logic->ustep_now);
		if (ret < 0) {
			LOG_ERR("%s: %s: GPIO update error",
				dev->name, io->name);
			K_SPINLOCK_BREAK;
		}

		logic->power_on = true; /* set to power on */
	};

	return ret;
}

static int stepper_gpio_off(const struct device *dev, const uint8_t motor)
{
	printk("GPIO: Off\n");
	/* NOTE: motor number already verified in stepper motor API */

	const struct stepper_gpio_config *config = dev->config;
	const struct stepper_gpio_io *const io = &config->io[motor];
	struct stepper_gpio_data *const data = stepper_get_private(dev);
	struct stepper_gpio_logic *const logic = &data->logic[motor];
	int ret = 0;

	/* TODO/FIXME: handle power cycle as async safety call */
	K_SPINLOCK(&logic->lock) {

		/* TODO/FIXME: support also 2 GPIO pins for |dir|stp| */

		/* check 4 GPIO pins for |a|c|b|d| */
		if (4 != io->num_gpios) {
			LOG_ERR("%s: %s: only 4 GPIO pins supported",
				dev->name, io->name);
			K_SPINLOCK_BREAK;
		}

		ret = stepper_gpio_acbd_poweroff(io->gpios);
		if (ret < 0) {
			LOG_ERR("%s: %s: GPIO power off error",
				dev->name, io->name);
			K_SPINLOCK_BREAK;
		}

		logic->running = false;  /* stop any movement */
		logic->power_on = false; /* set to power off */
	};

	return ret;
}

static int stepper_gpio_init(const struct device *dev)
{
	printk("GPIO: Initialization\n");
	const struct stepper_gpio_config *config = dev->config;
	const struct stepper_data *const api_data = dev->data;
	struct stepper_gpio_data *const data = stepper_get_private(dev);
	int ret = 0;

	if (config->num_motor != data->num_logic) {
		LOG_ERR("%s: missmatch number of motors and logic", dev->name);
		ret = -EINVAL;
		goto err;
	}

	if (config->num_motor != api_data->num_motor) {
		LOG_ERR("%s: wrong number of motors in API data", dev->name);
		ret = -EINVAL;
		goto err;
	}

	LOG_DBG("%s: init with %u motors", dev->name, config->num_motor);
	LOG_DBG("%s: init with %u logics", dev->name, data->num_logic);

	/* defaults to power off */
	for (int m = 0; m < config->num_motor; m++) {
		const struct stepper_gpio_io *const io = &config->io[m];

		LOG_DBG("%s: %s: setup %u gpios to inactive", dev->name,
			io->name, io->num_gpios);

		ret = stepper_gpio_off(dev, m);
		if (ret < 0) {
			LOG_ERR("%s: GPIO pin setup failed", dev->name);
			goto err;
		}
	}

err:
	return ret;
}

static const struct stepper_api stepper_gpio_api = {
	.on = stepper_gpio_on,
	.off = stepper_gpio_off,
	.move = stepper_gpio_move,
};

#define STEPPER_GPIO_IO_GPIOS(node_id)					\
	static const struct gpio_dt_spec gpio_dt_spec_##node_id[] = {	\
		DT_FOREACH_PROP_ELEM_SEP(node_id, gpios,		\
					 GPIO_DT_SPEC_GET_BY_IDX, (,)),	\
	};

#define STEPPER_GPIO_IO(node_id)					\
	{								\
		.motor = DT_NODE_CHILD_IDX(node_id),			\
		.name = DT_NODE_FULL_NAME(node_id),			\
		.num_gpios = ARRAY_SIZE(gpio_dt_spec_##node_id),	\
		.gpios = gpio_dt_spec_##node_id,			\
	}

#define STEPPER_GPIO_LOGIC(node_id)					\
	{								\
		.motor = DT_NODE_CHILD_IDX(node_id),			\
		.dev = DEVICE_DT_GET(DT_PARENT(node_id)),		\
		.dwork = Z_WORK_DELAYABLE_INITIALIZER(			\
						stepper_gpio_dworker),	\
		.power_on = false,					\
		.running = false,					\
		.positive = true,					\
		.positioning = true,					\
		.fstep_spd = DT_PROP(node_id, fs_max_speed),		\
		.ustep_res = DT_PROP(node_id, microstep_res),		\
		.ustep_now = 0,						\
		.ustep_move = 0,					\
	}

#define STEPPER_GPIO_DEVICE(i)						\
									\
DT_INST_FOREACH_CHILD_STATUS_OKAY(i, STEPPER_GPIO_IO_GPIOS)		\
									\
static const struct stepper_gpio_io stepper_gpio_io_##i[] = {		\
	DT_INST_FOREACH_CHILD_STATUS_OKAY_SEP(i, STEPPER_GPIO_IO, (,))	\
};									\
									\
static const struct stepper_gpio_config stepper_gpio_config_##i = {	\
	.num_motor = ARRAY_SIZE(stepper_gpio_io_##i),			\
	.io = stepper_gpio_io_##i,					\
};									\
									\
DT_INST_FOREACH_CHILD_STATUS_OKAY_SEP_VARGS(i,				\
	STEPPER_BUILD_ASSERT_DT_PROP_GT, (;), fs_max_speed, 0,		\
	"Maximum rotational speed must be greater than zero.");		\
									\
DT_INST_FOREACH_CHILD_STATUS_OKAY_SEP_VARGS(i,				\
	STEPPER_BUILD_ASSERT_DT_PROP_LT, (;), microstep_res, 3,		\
	"Maximum microstep resulution exceeds hardware capabilities.");	\
									\
static struct stepper_gpio_logic stepper_gpio_logic##i[] = {		\
	DT_INST_FOREACH_CHILD_STATUS_OKAY_SEP(i, STEPPER_GPIO_LOGIC, (,))\
};									\
									\
static struct stepper_gpio_data stepper_gpio_data_##i = {		\
	.num_logic = ARRAY_SIZE(stepper_gpio_logic##i),			\
	.logic = stepper_gpio_logic##i,					\
};									\
									\
STEPPER_DATA_DT_INST_DEFINE(i, stepper_data_,				\
			       stepper_gpio_data_,			\
			       stepper_gpio_caps_,			\
			       STEPPER_OP_MODE_VELOCITY |		\
			       STEPPER_OP_MODE_POSITION |		\
			       STEPPER_USTEP_RES_2 |			\
			       STEPPER_USTEP_RES_1);			\
									\
STEPPER_DEVICE_DT_INST_DEFINE(i, &stepper_gpio_init, NULL,		\
			      &stepper_data_##i,			\
			      &stepper_gpio_config_##i, POST_KERNEL,	\
			      CONFIG_STEPPER_INIT_PRIORITY,		\
			      &stepper_gpio_api);

DT_INST_FOREACH_STATUS_OKAY(STEPPER_GPIO_DEVICE)
