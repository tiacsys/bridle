/*
 * SPDX-FileCopyrightText: Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "zephyr/dt-bindings/stepper/stepper.h"
#define DT_DRV_COMPAT dummy_steppers

/**
 * @file
 * @brief Dummy driver for steppers to experiment
 */

#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/stepper.h>
#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(stepper_dummy, CONFIG_STEPPER_LOG_LEVEL);

struct stepper_dummy_config {
	const struct stepper_driver_config common;
};

struct stepper_dummy_data {};

static int stepper_dummy_move(const struct device *dev, const uint8_t motor,
			      const struct stepper_action *action) {
	LOG_INF("Dummy: Move, Motor ID: %d Flags: %d Value %d", motor,
		action->flags, action->value);

	int ret = 0;

	return ret;
}

static int stepper_dummy_on(const struct device *dev, const uint8_t motor) {
	LOG_INF("Dummy: On, Motor ID: %d", motor);

	int ret = 0;
	return ret;
}

static int stepper_dummy_off(const struct device *dev, const uint8_t motor) {
	LOG_INF("Dummy: Off, Motor ID: %d", motor);
	int ret = 0;

	return ret;
}

static int stepper_dummy_init(const struct device *dev) {
	LOG_INF("GPIO: Initialization");
	int ret = 0;
	return ret;
}

static const struct stepper_api stepper_dummy_api = {
    .on = stepper_dummy_on,
    .off = stepper_dummy_off,
    .move = stepper_dummy_move,
};

#define STEPPER_DUMMY_DEVICE(i)                                               \
                                                                              \
	STEPPER_DRIVER_CONFIG_DT_INST_DEFINE(                                 \
	    i, dummy_stepper_driver_config_,                                  \
	    (STEPPER_USTEP_RES_1 | STEPPER_USTEP_RES_2));                     \
                                                                              \
	static const struct stepper_dummy_config stepper_dummy_config_##i = { \
	    .common = dummy_stepper_driver_config_##i,                        \
	};                                                                    \
                                                                              \
	static struct stepper_dummy_data stepper_dummy_data_##i = {};         \
                                                                              \
	DEVICE_DT_INST_DEFINE(                                                \
	    i, &stepper_dummy_init, NULL, &stepper_dummy_data_##i,            \
	    &stepper_dummy_config_##i, POST_KERNEL,                           \
	    CONFIG_STEPPER_INIT_PRIORITY, &stepper_dummy_api);

DT_INST_FOREACH_STATUS_OKAY(STEPPER_DUMMY_DEVICE)
