/*
 * SPDX-FileCopyrightText: Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT dummy_steppers

/**
 * @file
 * @brief Dummy driver for steppers to experiment
 */

#include "stepper_common.h"

#include <zephyr/drivers/gpio.h>
#include <zephyr/device.h>
#include <zephyr/kernel.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(stepper_dummy, CONFIG_STEPPER_LOG_LEVEL);

struct stepper_dummy_config {
};

struct stepper_dummy_data {
};

static int stepper_dummy_move(const struct device *dev, const uint8_t motor,
			     const struct stepper_action *action)
{
	LOG_INF("Dummy: Move, Motor ID: %d Flags: %d Value %d", motor, action->flags, action->value);

	int ret = 0;

	return ret;
}

static int stepper_dummy_on(const struct device *dev, const uint8_t motor)
{
	LOG_INF("Dummy: On, Motor ID: %d", motor);

	int ret = 0;
	return ret;
}

static int stepper_dummy_off(const struct device *dev, const uint8_t motor)
{
	LOG_INF("Dummy: Off, Motor ID: %d", motor);
	int ret = 0;

	return ret;
}

static int stepper_dummy_init(const struct device *dev)
{
	LOG_INF("GPIO: Initialization");
	int ret = 0;
	return ret;
}

static const struct stepper_api stepper_dummy_api = {
	.on = stepper_dummy_on,
	.off = stepper_dummy_off,
	.move = stepper_dummy_move,
};

#define STEPPER_DUMMY_DEVICE(i)						\
									\
static const struct stepper_dummy_config stepper_dummy_config_##i = {	\
};									\
									\
DT_INST_FOREACH_CHILD_STATUS_OKAY_SEP_VARGS(i,				\
	STEPPER_BUILD_ASSERT_DT_PROP_GT, (;), fs_max_speed, 0,		\
	"Maximum rotational speed must be greater than zero.");		\
									\
DT_INST_FOREACH_CHILD_STATUS_OKAY_SEP_VARGS(i,				\
	STEPPER_BUILD_ASSERT_DT_PROP_LT, (;), microstep_res, 5,		\
	"Maximum microstep resulution exceeds hardware capabilities.");	\
									\
static struct stepper_dummy_data stepper_dummy_data_##i = {		\
};									\
									\
STEPPER_DATA_DT_INST_DEFINE(i, stepper_data_,				\
			       stepper_dummy_data_,			\
			       stepper_dummy_caps_,			\
			       STEPPER_OP_MODE_VELOCITY |		\
			       STEPPER_OP_MODE_POSITION |		\
			       STEPPER_USTEP_RES_2 |			\
			       STEPPER_USTEP_RES_1);			\
									\
STEPPER_DEVICE_DT_INST_DEFINE(i, &stepper_dummy_init, NULL,		\
			      &stepper_data_##i,			\
			      &stepper_dummy_config_##i, POST_KERNEL,	\
			      CONFIG_STEPPER_INIT_PRIORITY,		\
			      &stepper_dummy_api);

DT_INST_FOREACH_STATUS_OKAY(STEPPER_DUMMY_DEVICE)
