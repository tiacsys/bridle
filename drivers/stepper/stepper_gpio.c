/*
 * SPDX-FileCopyrightText: Copyright (c) 2024 Carl Zeiss Meditec AG
 * SPDX-FileCopyrightText: Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT gpio_stepper

#include <zephyr/sys/__assert.h>
#include <zephyr/sys_clock.h>

#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/stepper.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(stepper_gpio, CONFIG_STEPPER_LOG_LEVEL);

#define NUMBER_OF_GPIO_PINS 4

struct stepper_gpio_config {
	const struct gpio_dt_spec *control_pins;
};

struct stepper_gpio_data {
	const struct device *dev;
	struct k_spinlock lock;
	struct k_work_delayable stepper_dwork;
	int32_t actual_position;
	int32_t target_position;
	uint32_t delay_in_us;
};

static int stepper_motor_move_with_4_gpios(const struct gpio_dt_spec *gpio_spec,
					   int32_t step_number)
{
	int ret = 0;

	/* FIXME: check result code */
	switch (step_number) {
	case 0:
		LOG_DBG("Step 1010 %d %d %d %d",
			gpio_spec[0].pin, gpio_spec[1].pin,
			gpio_spec[2].pin, gpio_spec[3].pin);
		gpio_pin_configure_dt(&gpio_spec[0], GPIO_OUTPUT_ACTIVE);
		gpio_pin_configure_dt(&gpio_spec[1], GPIO_OUTPUT_INACTIVE);
		gpio_pin_configure_dt(&gpio_spec[2], GPIO_OUTPUT_ACTIVE);
		gpio_pin_configure_dt(&gpio_spec[3], GPIO_OUTPUT_INACTIVE);
		break;

	case 1:
		LOG_DBG("Step 0110 %d %d %d %d",
			gpio_spec[0].pin, gpio_spec[1].pin,
			gpio_spec[2].pin, gpio_spec[3].pin);
		gpio_pin_configure_dt(&gpio_spec[0], GPIO_OUTPUT_INACTIVE);
		gpio_pin_configure_dt(&gpio_spec[1], GPIO_OUTPUT_ACTIVE);
		gpio_pin_configure_dt(&gpio_spec[2], GPIO_OUTPUT_ACTIVE);
		gpio_pin_configure_dt(&gpio_spec[3], GPIO_OUTPUT_INACTIVE);
		break;

	case 2:
		LOG_DBG("Step 0101 %d %d %d %d",
			gpio_spec[0].pin, gpio_spec[1].pin,
			gpio_spec[2].pin, gpio_spec[3].pin);
		gpio_pin_configure_dt(&gpio_spec[0], GPIO_OUTPUT_INACTIVE);
		gpio_pin_configure_dt(&gpio_spec[1], GPIO_OUTPUT_ACTIVE);
		gpio_pin_configure_dt(&gpio_spec[2], GPIO_OUTPUT_INACTIVE);
		gpio_pin_configure_dt(&gpio_spec[3], GPIO_OUTPUT_ACTIVE);
		break;

	case 3:
		LOG_DBG("Step 1001 %d %d %d %d",
			gpio_spec[0].pin, gpio_spec[1].pin,
			gpio_spec[2].pin, gpio_spec[3].pin);
		gpio_pin_configure_dt(&gpio_spec[0], GPIO_OUTPUT_ACTIVE);
		gpio_pin_configure_dt(&gpio_spec[1], GPIO_OUTPUT_INACTIVE);
		gpio_pin_configure_dt(&gpio_spec[2], GPIO_OUTPUT_INACTIVE);
		gpio_pin_configure_dt(&gpio_spec[3], GPIO_OUTPUT_ACTIVE);
		break;

	default:
		ret = -ENOTSUP;
		break;
	}

	return ret;
}

void stepper_work_step_handler(struct k_work *work)
{
	struct k_work_delayable *dwork = k_work_delayable_from_work(work);
	struct stepper_gpio_data *data = CONTAINER_OF(dwork,
			struct stepper_gpio_data, stepper_dwork);
	const struct stepper_gpio_config *config = data->dev->config;
	/* FIXME: Avoid static variable inside functions, that have to
	 * place on drivers private data!
	 */
	static int32_t step_count = 1;

	/*
	 * FIXME: Should we not better use the State Machine API here?
	 */
	K_SPINLOCK(&data->lock) {
		LOG_DBG("Moving Motor from %d to %d with delay %d ",
			data->actual_position, data->target_position,
			data->delay_in_us);

		if (data->actual_position != data->target_position) {

			if (data->actual_position > data->target_position) {

				/* FIXME: check result code */
				stepper_motor_move_with_4_gpios(config->control_pins,
								step_count--);
				step_count = step_count < 0
					   ? (NUMBER_OF_GPIO_PINS - 1)
					   : step_count;

				data->actual_position--;

			} else if (data->actual_position < data->target_position) {

				/* FIXME: check result code */
				stepper_motor_move_with_4_gpios(config->control_pins,
								step_count++);
				step_count = step_count > (NUMBER_OF_GPIO_PINS - 1)
					   ? 0
					   : step_count;

				data->actual_position++;

			}

			k_work_reschedule(&data->stepper_dwork, K_USEC(data->delay_in_us));
		}
	}
}

/* FIXME:
 * https://github.com/zephyrproject-rtos/zephyr/pull/68774#discussion_r1689298543
 */
static int stepper_gpio_move(const struct device *dev,
			     const int32_t micro_steps)
{
	struct stepper_gpio_data *data = dev->data;

	K_SPINLOCK(&data->lock) {
		data->target_position = data->actual_position + micro_steps;
		k_work_reschedule(&data->stepper_dwork, K_NO_WAIT);
	}

	return 0;
}

static int stepper_gpio_set_actual_position(const struct device *dev,
					    const int32_t position)
{
	struct stepper_gpio_data *data = dev->data;

	K_SPINLOCK(&data->lock) {
		data->actual_position = position;
		k_work_reschedule(&data->stepper_dwork, K_NO_WAIT);
	}

	return 0;
}

static int stepper_gpio_get_actual_position(const struct device *dev,
					    int32_t *position)
{
	struct stepper_gpio_data *data = dev->data;

	K_SPINLOCK(&data->lock) {
		*position = data->actual_position;
	}

	return 0;
}

static int stepper_gpio_set_target_position(const struct device *dev,
					    const int32_t position)
{
	struct stepper_gpio_data *data = dev->data;

	K_SPINLOCK(&data->lock) {
		data->target_position = position;
		k_work_reschedule(&data->stepper_dwork, K_NO_WAIT);
	}

	return 0;
}

static int stepper_gpio_is_moving(const struct device *dev, bool *is_moving)
{
	struct stepper_gpio_data *data = dev->data;

	*is_moving = k_work_delayable_is_pending(&data->stepper_dwork);
	LOG_DBG("Is Motor Moving %d", *is_moving);

	return 0;
}

static int stepper_gpio_set_max_velocity(const struct device *dev,
					 const uint32_t micro_steps_per_second)
{
	struct stepper_gpio_data *data = dev->data;

	if (micro_steps_per_second == 0) {
		LOG_ERR("Velocity cannot be zero");
		return -EINVAL;
	}

	K_SPINLOCK(&data->lock) {
		data->delay_in_us = USEC_PER_SEC / micro_steps_per_second;
	}

	LOG_DBG("Setting Motor Speed to %d (delay is %d usec)",
		micro_steps_per_second, data->delay_in_us);

	return 0;
}

static int stepper_gpio_get_micro_step_res(const struct device *dev,
				enum micro_step_resolution *resolution)
{
	ARG_UNUSED(dev);

	*resolution = STEPPER_MICRO_STEP_1;

	return 0;
}

static int stepper_gpio_enable(const struct device *dev, const bool enable)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(enable);

	return -ENOTSUP;
}

static int stepper_gpio_init(const struct device *dev)
{
	struct stepper_gpio_data *data = dev->data;

	const struct stepper_gpio_config *config = dev->config;

	LOG_DBG("%s: initializing GPIO driven stepper motor", dev->name);

	data->dev = dev;

	for (uint8_t n_pin = 0; n_pin < NUMBER_OF_GPIO_PINS; n_pin++) {
		/* FIXME: check result code */
		gpio_pin_configure_dt(&config->control_pins[n_pin],
				      GPIO_OUTPUT_INACTIVE);
	}

	k_work_init_delayable(&data->stepper_dwork, stepper_work_step_handler);

	return 0;
}

static const struct stepper_api stepper_gpio_api = {
	.enable = stepper_gpio_enable,
	.move = stepper_gpio_move,
	.is_moving = stepper_gpio_is_moving,
	.set_actual_position = stepper_gpio_set_actual_position,
	.get_actual_position = stepper_gpio_get_actual_position,
	.set_target_position = stepper_gpio_set_target_position,
	.set_max_velocity = stepper_gpio_set_max_velocity,
	.get_micro_step_res = stepper_gpio_get_micro_step_res,
};

#define STEPPER_GPIO_DEFINE(n)                                               \
                                                                             \
	static const struct gpio_dt_spec gpio_dt_spec_##n[] = {              \
		DT_INST_FOREACH_PROP_ELEM_SEP(n, gpios,                      \
					      GPIO_DT_SPEC_GET_BY_IDX, (,)), \
	};                                                                   \
                                                                             \
	BUILD_ASSERT(ARRAY_SIZE(gpio_dt_spec_##n) == NUMBER_OF_GPIO_PINS,    \
		     "This driver only supports 4 control pins");            \
                                                                             \
	static const struct stepper_gpio_config stepper_gpio_config_##n = {  \
			.control_pins = gpio_dt_spec_##n,                    \
	};                                                                   \
                                                                             \
	static struct stepper_gpio_data stepper_gpio_data_##n;               \
                                                                             \
	DEVICE_DT_INST_DEFINE(n, &stepper_gpio_init, NULL,                   \
			      &stepper_gpio_data_##n,                        \
			      &stepper_gpio_config_##n,                      \
			      POST_KERNEL, CONFIG_STEPPER_INIT_PRIORITY,     \
			      &stepper_gpio_api);

DT_INST_FOREACH_STATUS_OKAY(STEPPER_GPIO_DEFINE)
