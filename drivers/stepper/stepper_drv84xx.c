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
	struct gpio_dt_spec step_pin;
	struct gpio_dt_spec sleep_pin;
	struct gpio_dt_spec en_pin;
	struct gpio_dt_spec m0_pin;
	struct gpio_dt_spec m1_pin;
};

struct drv84xx_data {};

static int drv84xx_on(const struct device *dev, const uint8_t motor) {
	int ret;
	const struct drv84xx_config *config = dev->config;
	bool has_enable = config->en_pin.port != NULL;
	bool has_sleep = config->sleep_pin.port != NULL;

	if (!has_sleep && !has_enable) {
		LOG_ERR(
		    "%s: Failure to set device to on, neither of sleep pin and "
		    "enable pin are available. The device is always on",
		    dev->name);
		return -ENOTSUP;
	}

	if (has_sleep) {
		ret = gpio_pin_set_dt(&config->sleep_pin, 0);
		if (ret != 0) {
			LOG_ERR("%s: Failed to set sleep_pin (error: %d)",
				dev->name, ret);
			return ret;
		}
	}

	if (has_enable) {
		ret = gpio_pin_set_dt(&config->en_pin, 1);
		if (ret != 0) {
			LOG_ERR("%s: Failed to set en_pin (error: %d)",
				dev->name, ret);
			return ret;
		}
	}

	return 0;
}

static int drv84xx_off(const struct device *dev, const uint8_t motor) {
	int ret;
	const struct drv84xx_config *config = dev->config;
	bool has_enable = config->en_pin.port != NULL;
	bool has_sleep = config->sleep_pin.port != NULL;

	if (!has_sleep && !has_enable) {
		LOG_ERR(
		    "%s: Failure to set device to off, neither of sleep pin "
		    "and enable pin are available. The device is always on",
		    dev->name);
		return -ENOTSUP;
	}

	if (has_sleep) {
		ret = gpio_pin_set_dt(&config->sleep_pin, 1);
		if (ret != 0) {
			LOG_ERR("%s: Failed to set sleep_pin (error: %d)",
				dev->name, ret);
			return ret;
		}
	}

	if (has_enable) {
		ret = gpio_pin_set_dt(&config->en_pin, 0);
		if (ret != 0) {
			LOG_ERR("%s: Failed to set en_pin (error: %d)",
				dev->name, ret);
			return ret;
		}
	}

	return 0;
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
	int ret = 0;

	/* Configure direction pin */
	ret = gpio_pin_configure_dt(&config->dir_pin, GPIO_OUTPUT_ACTIVE);
	if (ret != 0) {
		LOG_ERR("%s: Failed to configure dir_pin (error: %d)",
			dev->name, ret);
		return ret;
	}

	/* Configure step pin */
	ret = gpio_pin_configure_dt(&config->step_pin, GPIO_OUTPUT_INACTIVE);
	if (ret != 0) {
		LOG_ERR("%s: Failed to configure step_pin (error: %d)",
			dev->name, ret);
		return ret;
	}

	/* Configure sleep pin if it is available */
	if (config->sleep_pin.port != NULL) {
		ret = gpio_pin_configure_dt(&config->sleep_pin,
					    GPIO_OUTPUT_ACTIVE | GPIO_INPUT);
		if (ret != 0) {
			LOG_ERR("%s: Failed to configure sleep_pin (error: %d)",
				dev->name, ret);
			return ret;
		}
	}

	/* Configure enable pin if it is available */
	if (config->en_pin.port != NULL) {
		ret = gpio_pin_configure_dt(&config->en_pin,
					    GPIO_OUTPUT_INACTIVE | GPIO_INPUT);
		if (ret != 0) {
			LOG_ERR("%s: Failed to configure en_pin (error: %d)",
				dev->name, ret);
			return ret;
		}
	}

	/* Configure microstep pin 0 */
	ret = gpio_pin_configure_dt(&config->m0_pin, GPIO_OUTPUT_INACTIVE);
	if (ret != 0) {
		LOG_ERR("%s: Failed to configure m0_pin (error: %d)", dev->name,
			ret);
		return ret;
	}

	/* Configure microstep pin 1 */
	ret = gpio_pin_configure_dt(&config->m1_pin, GPIO_OUTPUT_INACTIVE);
	if (ret != 0) {
		LOG_ERR("%s: Failed to configure m1_pin (error: %d)", dev->name,
			ret);
		return ret;
	}

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
	    .step_pin = GPIO_DT_SPEC_INST_GET(inst, step_gpios),           \
	    .sleep_pin = GPIO_DT_SPEC_INST_GET_OR(inst, sleep_gpios, {0}), \
	    .en_pin = GPIO_DT_SPEC_INST_GET_OR(inst, en_gpios, {0}),       \
	    .m0_pin = GPIO_DT_SPEC_INST_GET_OR(inst, m0_gpios, {0}),       \
	    .m1_pin = GPIO_DT_SPEC_INST_GET_OR(inst, m1_gpios, {0}),       \
	};                                                                 \
                                                                           \
	static struct drv84xx_data drv84xx_data_##inst = {};               \
                                                                           \
	DEVICE_DT_INST_DEFINE(                                             \
	    inst, &drv84xx_init,	  /* Init */                       \
	    NULL,			  /* PM */                         \
	    &drv84xx_data_##inst,	  /* Data */                       \
	    &drv84xx_config_##inst,	  /* Config */                     \
	    POST_KERNEL,		  /* Init stage */                 \
	    CONFIG_STEPPER_INIT_PRIORITY, /* Init priority */              \
	    &drv84xx_api);		  /* API */

DT_INST_FOREACH_STATUS_OKAY(DRV84XX_DEVICE)
