/*
 * SPDX-FileCopyrightText: Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <stdint.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/stepper.h>
#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(stepper_drv84xx, CONFIG_STEPPER_LOG_LEVEL);

#define DT_DRV_COMPAT drv84xx

struct drv84xx_config {
	struct stepper_driver_config common;
	struct gpio_dt_spec dir_pin;
	struct gpio_dt_spec stp_pin;
	struct gpio_dt_spec sleep_pin;
	struct gpio_dt_spec en_pin;
	struct gpio_dt_spec m0_pin;
	struct gpio_dt_spec m1_pin;
};

struct drv84xx_data {};

static int drv84xx_on(const struct device *dev, const uint8_t motor) {
	return -ENOTSUP;
}

static int drv84xx_off(const struct device *dev, const uint8_t motor) {
	return -ENOTSUP;
}

static int drv84xx_move(const struct device *dev, const uint8_t motor,
			const struct stepper_action *action) {
	return -ENOTSUP;
}

static const struct stepper_api drv84xx_api = {
    .on = drv84xx_on,
    .off = drv84xx_off,
    .move = drv84xx_move,
};

static int drv84xx_init(const struct device *dev) {
	const struct drv84xx_config *const config = dev->config;
	struct drv84xx_data *data = dev->data;
	int ret = 0;

	// TODO: Init pins

	return 0;
}

#define DRV84XX_DEVICE(inst)                                               \
	STEPPER_DRIVER_CONFIG_DT_INST_DEFINE(                              \
	    inst, drv84xx_stepper_driver_config_,                          \
	    (STEPPER_USTEP_RES_1 | STEPPER_USTEP_RES_2));                  \
                                                                           \
	static const struct drv84xx_config drv84xx_config_##inst = {       \
	    .common = drv84xx_stepper_driver_config_##inst,                \
	    .dir_pin = GPIO_DT_SPEC_INST_GET(inst, dir_gpios),             \
	    .stp_pin = GPIO_DT_SPEC_INST_GET(inst, step_gpios),            \
	    .sleep_pin = GPIO_DT_SPEC_INST_GET_OR(inst, sleep_gpios, {0}), \
	    .en_pin = GPIO_DT_SPEC_INST_GET_OR(inst, en_gpios, {0}),       \
	    .m0_pin = GPIO_DT_SPEC_INST_GET_OR(inst, m0_gpios, {0}),       \
	    .m1_pin = GPIO_DT_SPEC_INST_GET_OR(inst, m1_gpios, {0}),       \
	};                                                                 \
	static struct drv84xx_data drv84xx_data_##inst = {};               \
	DEVICE_DT_INST_DEFINE(                                             \
	    inst, &drv84xx_init,	  /* Init */                       \
	    NULL,			  /* PM */                         \
	    &drv84xx_data_##inst,	  /* Data */                       \
	    &drv84xx_config_##inst,	  /* Config */                     \
	    POST_KERNEL,		  /* Init stage */                 \
	    CONFIG_STEPPER_INIT_PRIORITY, /* Init priority */              \
	    &drv84xx_api);		  /* API */

DT_INST_FOREACH_STATUS_OKAY(DRV84XX_DEVICE)
