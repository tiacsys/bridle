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

struct drv84xx_data {
	/** Microstep configuration. */
	uint8_t m0_value;
	uint8_t m1_value;
};

static const uint8_t microstep_table[9][2] = {
    {0, 0}, {2, 0}, {0, 1}, {1, 1}, {2, 1}, {0, 2}, {2, 4}, {2, 2}, {1, 2}};

static int drv84xx_microstep_recovery(const struct device *dev) {
	const struct drv84xx_config *config = dev->config;
	struct drv84xx_data *data = dev->data;
	int ret = 0;

	int m0_value = data->m0_value;
	int m1_value = data->m1_value;

	ret = gpio_pin_configure_dt(&config->m0_pin,
				    GPIO_OUTPUT_INACTIVE); /** Reset m0 pin */
	if (ret != 0) {
		LOG_ERR(
		    "%s: Failed to restore microstep configuration (error: %d)",
		    dev->name, ret);
		return ret;
	}
	ret = gpio_pin_configure_dt(&config->m1_pin,
				    GPIO_OUTPUT_INACTIVE); /** Reset m1 pin */
	if (ret != 0) {
		LOG_ERR(
		    "%s: Failed to restore microstep configuration (error: %d)",
		    dev->name, ret);
		return ret;
	}

	/** Set m0 pin */
	switch (m0_value) {
		case 0:
			ret = gpio_pin_set_dt(&config->m0_pin, 0);
			break;
		case 1:
			ret = gpio_pin_set_dt(&config->m0_pin, 1);
			break;
		case 2:
			ret = gpio_pin_configure_dt(
			    &config->m0_pin, GPIO_DISCONNECTED); /** Hi-Z */
			break;

		default:
			break;
	}
	if (ret != 0) {
		LOG_ERR(
		    "%s: Failed to restore microstep configuration (error: %d)",
		    dev->name, ret);
		return ret;
	}

	/** Set m1 pin */
	switch (m1_value) {
		case 0:
			ret = gpio_pin_set_dt(&config->m1_pin, 0);
			break;
		case 1:
			ret = gpio_pin_set_dt(&config->m1_pin, 1);
			break;
		case 2:
			ret = gpio_pin_configure_dt(
			    &config->m1_pin, GPIO_DISCONNECTED); /** Hi-Z */
			break;

		default:
			break;
	}
	if (ret != 0) {
		LOG_ERR(
		    "%s: Failed to restore microstep configuration (error: %d)",
		    dev->name, ret);
		return ret;
	}

	return 0;
}

static int drv84xx_set_microstep(const struct device *dev,
				 uint32_t microstep_id) {
	const struct drv84xx_config *config = dev->config;
	struct drv84xx_data *data = dev->data;
	int ret = 0;

	if (microstep_id > 8) {
		LOG_ERR(
		    "%s: Microstep index of %d is too large, maximum value "
		    "is 8",
		    dev->name, microstep_id);
		return -EDOM;
	}

	int m0_value = microstep_table[microstep_id][0];
	int m1_value = microstep_table[microstep_id][1];

	ret = gpio_pin_configure_dt(&config->m0_pin,
				    GPIO_OUTPUT_INACTIVE); /** Reset m0 pin */
	if (ret != 0) {
		LOG_ERR("%s: Failed to reset m0_pin (error: %d)", dev->name,
			ret);
		drv84xx_microstep_recovery(dev);
		return ret;
	}
	ret = gpio_pin_configure_dt(&config->m1_pin,
				    GPIO_OUTPUT_INACTIVE); /** Reset m1 pin */
	if (ret != 0) {
		LOG_ERR("%s: Failed to reset m1_pin (error: %d)", dev->name,
			ret);
		drv84xx_microstep_recovery(dev);
		return ret;
	}

	/** Set m0 pin */
	switch (m0_value) {
		case 0:
			ret = gpio_pin_set_dt(&config->m0_pin, 0);
			break;
		case 1:
			ret = gpio_pin_set_dt(&config->m0_pin, 1);
			break;
		case 2:
			ret = gpio_pin_configure_dt(
			    &config->m0_pin, GPIO_DISCONNECTED); /** Hi-Z */
			break;

		default:
			break;
	}
	if (ret != 0) {
		LOG_ERR("%s: Failed to set m0_pin (error: %d)", dev->name, ret);
		drv84xx_microstep_recovery(dev);
		return ret;
	}

	/** Set m1 pin */
	switch (m1_value) {
		case 0:
			ret = gpio_pin_set_dt(&config->m1_pin, 0);
			break;
		case 1:
			ret = gpio_pin_set_dt(&config->m1_pin, 1);
			break;
		case 2:
			ret = gpio_pin_configure_dt(
			    &config->m1_pin, GPIO_DISCONNECTED); /** Hi-Z */
			break;

		default:
			break;
	}
	if (ret != 0) {
		LOG_ERR("%s: Failed to set m1_pin (error: %d)", dev->name, ret);
		drv84xx_microstep_recovery(dev);
		return ret;
	}

	data->m0_value = m0_value;
	data->m1_value = m1_value;

	return 0;
}

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
	struct drv84xx_data *data = dev->data;
	const struct drv84xx_config *config = dev->config;
	bool has_enable = config->en_pin.port != NULL;
	bool has_sleep = config->sleep_pin.port != NULL;
	int ret = 0;

	if (has_enable) {
		ret = gpio_pin_get_dt(&config->en_pin);
		if (ret < 0) {
			LOG_ERR("%s: Failed to get en_pin value (error: %d)",
				dev->name, ret);
			return ret;
		}
		if (ret == 0) {
			LOG_ERR("%s: Stepper is in OFF state", dev->name);
			return -EIO;
		}
	}

	if (has_sleep) {
		ret = gpio_pin_get_dt(&config->sleep_pin);
		if (ret < 0) {
			LOG_ERR("%s: Failed to get sleep_pin value (error: %d)",
				dev->name, ret);
			return ret;
		}
		if (ret == 1) {
			LOG_ERR("%s: Stepper is in OFF state", dev->name);
			return -EIO;
		}
	}

	if (action->value >= 0) {
		ret = gpio_pin_set_dt(&config->dir_pin, 1);

	} else {
		ret = gpio_pin_set_dt(&config->dir_pin, 0);
	}

	if (ret != 0) {
		LOG_ERR("%s: Failed to set direction pin (error: %d)",
			dev->name, ret);
		return ret;
	}

	int microstep_id = STEPPER_USTEP_RES_GET(action->flags);
	microstep_id = log(microstep_id) / log(2);
	ret = drv84xx_set_microstep(dev, microstep_id);
	if (ret != 0) {
		return ret;
	}

	/* Stepper movement goes here */

	return 0;
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

#define DRV84XX_DEVICE(inst)                                                   \
	STEPPER_DRIVER_CONFIG_DT_INST_DEFINE(                                  \
	    inst, drv84xx_stepper_driver_config_,                              \
	    (STEPPER_USTEP_RES_1 | STEPPER_USTEP_RES_2 | STEPPER_USTEP_RES_4 | \
	     STEPPER_USTEP_RES_8 | STEPPER_USTEP_RES_16 |                      \
	     STEPPER_USTEP_RES_32 | STEPPER_USTEP_RES_128 |                    \
	     STEPPER_USTEP_RES_256));                                          \
                                                                               \
	static const struct drv84xx_config drv84xx_config_##inst = {           \
	    .common = drv84xx_stepper_driver_config_##inst,                    \
	    .dir_pin = GPIO_DT_SPEC_INST_GET(inst, dir_gpios),                 \
	    .step_pin = GPIO_DT_SPEC_INST_GET(inst, step_gpios),               \
	    .sleep_pin = GPIO_DT_SPEC_INST_GET_OR(inst, sleep_gpios, {0}),     \
	    .en_pin = GPIO_DT_SPEC_INST_GET_OR(inst, en_gpios, {0}),           \
	    .m0_pin = GPIO_DT_SPEC_INST_GET_OR(inst, m0_gpios, {0}),           \
	    .m1_pin = GPIO_DT_SPEC_INST_GET_OR(inst, m1_gpios, {0}),           \
	};                                                                     \
                                                                               \
	static struct drv84xx_data drv84xx_data_##inst = {                     \
	    .m0_value = 0,                                                     \
	    .m1_value = 0,                                                     \
	};                                                                     \
                                                                               \
	DEVICE_DT_INST_DEFINE(                                                 \
	    inst, &drv84xx_init,	  /* Init */                           \
	    NULL,			  /* PM */                             \
	    &drv84xx_data_##inst,	  /* Data */                           \
	    &drv84xx_config_##inst,	  /* Config */                         \
	    POST_KERNEL,		  /* Init stage */                     \
	    CONFIG_STEPPER_INIT_PRIORITY, /* Init priority */                  \
	    &drv84xx_api);		  /* API */

DT_INST_FOREACH_STATUS_OKAY(DRV84XX_DEVICE)
