/*
 * SPDX-FileCopyrightText: Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <stdint.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/pwm.h>
#include <zephyr/drivers/stepper.h>
#include <zephyr/logging/log.h>

#include "zephyr/kernel.h"
#include "zephyr/sys_clock.h"
LOG_MODULE_REGISTER(stepper_drv84xx, CONFIG_STEPPER_LOG_LEVEL);

#define DT_DRV_COMPAT drv84xx

/**
 * @brief DRV84XX stepper driver configuration data.
 *
 * This structure contains all of the devicetree specifications for the pins
 * needed by a given DRV84XX stepper driver.
 */
struct drv84xx_config {
	/** Common @ref stepper_driver_config (needs to be first). */
	struct stepper_driver_config common;
	/** Devicetree specification of the direction pin. */
	struct gpio_dt_spec dir_pin;
	/** Devicetree specification of the step signal pwm. */
	struct pwm_dt_spec step_pwm;
	/** Devicetree specification of the sleep pin. */
	struct gpio_dt_spec sleep_pin;
	/** Devicetree specification of the enable pin. */
	struct gpio_dt_spec en_pin;
	/** Devicetree specification of the microstep pin 0. */
	struct gpio_dt_spec m0_pin;
	/** Devicetree specification of the microstep pin 1. */
	struct gpio_dt_spec m1_pin;
};

/* Struct for storing the states of output pins. */
struct drv84xx_pin_states {
	uint8_t sleep: 1;
	uint8_t en: 1;
	uint8_t m0: 2;
	uint8_t m1: 2;
};

/**
 * @brief DRV84XX stepper driver data.
 *
 * This structure contains mutable data used by a DRV84XX stepper driver.
 */
struct drv84xx_data {
	/** Struct containing the states of different pins. */
	struct drv84xx_pin_states pin_states;
};

/* Pin configurations for different microstep settings. */
static const uint8_t microstep_table[9][2] = {{0, 0}, {2, 0}, {0, 1}, {1, 1}, {2, 1},
					      {0, 2}, {2, 4}, {2, 2}, {1, 2}};

/*
 * If microstep setter fails, attempt to recover into previous state.
 */
static int drv84xx_microstep_recovery(const struct device *dev)
{
	const struct drv84xx_config *config = dev->config;
	struct drv84xx_data *data = dev->data;
	int ret = 0;

	int m0_value = data->pin_states.m0;
	int m1_value = data->pin_states.m1;

	/* Reset m0 pin as it may have been disconnected */
	ret = gpio_pin_configure_dt(&config->m0_pin, GPIO_OUTPUT_INACTIVE);
	if (ret != 0) {
		LOG_ERR("%s: Failed to restore microstep configuration (error: %d)", dev->name,
			ret);
		return ret;
	}

	/* Reset m1 pin as it may have been disconnected. */
	ret = gpio_pin_configure_dt(&config->m1_pin, GPIO_OUTPUT_INACTIVE);
	if (ret != 0) {
		LOG_ERR("%s: Failed to restore microstep configuration (error: %d)", dev->name,
			ret);
		return ret;
	}

	switch (m0_value) {
	case 0:
		ret = gpio_pin_set_dt(&config->m0_pin, 0);
		break;
	case 1:
		ret = gpio_pin_set_dt(&config->m0_pin, 1);
		break;
	case 2:
		/* Hi-Z is set by configuring pin as disconnected, not
		 * all gpio controllers support this. */
		ret = gpio_pin_configure_dt(&config->m0_pin, GPIO_DISCONNECTED);
		break;
	default:
		break;
	}

	if (ret != 0) {
		LOG_ERR("%s: Failed to restore microstep configuration (error: %d)", dev->name,
			ret);
		return ret;
	}

	switch (m1_value) {
	case 0:
		ret = gpio_pin_set_dt(&config->m1_pin, 0);
		break;
	case 1:
		ret = gpio_pin_set_dt(&config->m1_pin, 1);
		break;
	case 2:
		/* Hi-Z is set by configuring pin as disconnected, not
		 * all gpio controllers support this. */
		ret = gpio_pin_configure_dt(&config->m1_pin, GPIO_DISCONNECTED);
		break;
	default:
		break;
	}

	if (ret != 0) {
		LOG_ERR("%s: Failed to restore microstep configuration (error: %d)", dev->name,
			ret);
		return ret;
	}

	return 0;
}

/*
 * Sets microstep resolution.
 */
static int drv84xx_set_microstep(const struct device *dev, uint32_t microstep_id)
{
	const struct drv84xx_config *config = dev->config;
	struct drv84xx_data *data = dev->data;
	int ret = 0;

	if (microstep_id > 8) {
		LOG_ERR("%s: Microstep index of %d is too large, maximum value is 8", dev->name,
			microstep_id);
		return -EINVAL;
	}

	int m0_value = microstep_table[microstep_id][0];
	int m1_value = microstep_table[microstep_id][1];

	/* Reset m0 pin as it may have been disconnected. */
	ret = gpio_pin_configure_dt(&config->m0_pin, GPIO_OUTPUT_INACTIVE);
	if (ret != 0) {
		LOG_ERR("%s: Failed to reset m0_pin (error: %d)", dev->name, ret);
		drv84xx_microstep_recovery(dev);
		return ret;
	}

	/* Reset m1 pin as it may have been disconnected */
	ret = gpio_pin_configure_dt(&config->m1_pin, GPIO_OUTPUT_INACTIVE);
	if (ret != 0) {
		LOG_ERR("%s: Failed to reset m1_pin (error: %d)", dev->name, ret);
		drv84xx_microstep_recovery(dev);
		return ret;
	}

	/* Set m0 pin */
	switch (m0_value) {
	case 0:
		ret = gpio_pin_set_dt(&config->m0_pin, 0);
		break;
	case 1:
		ret = gpio_pin_set_dt(&config->m0_pin, 1);
		break;
	case 2:
		/* Hi-Z is set by configuring pin as disconnected, not
		 * all gpio controllers support this. */
		ret = gpio_pin_configure_dt(&config->m0_pin, GPIO_DISCONNECTED);
		break;
	default:
		break;
	}

	if (ret != 0) {
		LOG_ERR("%s: Failed to set m0_pin (error: %d)", dev->name, ret);
		drv84xx_microstep_recovery(dev);
		return ret;
	}

	switch (m1_value) {
	case 0:
		ret = gpio_pin_set_dt(&config->m1_pin, 0);
		break;
	case 1:
		ret = gpio_pin_set_dt(&config->m1_pin, 1);
		break;
	case 2:
		/* Hi-Z is set by configuring pin as disconnected, not
		 * all gpio controllers support this. */
		ret = gpio_pin_configure_dt(&config->m1_pin, GPIO_DISCONNECTED);
		break;
	default:
		break;
	}

	if (ret != 0) {
		LOG_ERR("%s: Failed to set m1_pin (error: %d)", dev->name, ret);
		drv84xx_microstep_recovery(dev);
		return ret;
	}

	data->pin_states.m0 = m0_value;
	data->pin_states.m1 = m1_value;

	return 0;
}

/*
 * Sets the stepper motor driver chip to on.
 */
static int drv84xx_on(const struct device *dev, const uint8_t motor)
{
	int ret;
	const struct drv84xx_config *config = dev->config;
	struct drv84xx_data *data = dev->data;
	bool has_enable = config->en_pin.port != NULL;
	bool has_sleep = config->sleep_pin.port != NULL;

	/* Check availability of sleep and and enable pins, as these might be
	 * hardwired. */
	if (!has_sleep && !has_enable) {
		LOG_ERR("%s: Failure to set device to on, neither sleep pin nor enable pin are "
			"available. The device is always on.",
			dev->name);
		return -ENOTSUP;
	}

	if (has_sleep) {
		ret = gpio_pin_set_dt(&config->sleep_pin, 0);
		if (ret != 0) {
			LOG_ERR("%s: Failed to set sleep_pin (error: %d)", dev->name, ret);
			return ret;
		}
		data->pin_states.sleep = 0U;
	}

	if (has_enable) {
		ret = gpio_pin_set_dt(&config->en_pin, 1);
		if (ret != 0) {
			LOG_ERR("%s: Failed to set en_pin (error: %d)", dev->name, ret);
			return ret;
		}
		data->pin_states.en = 1U;
	}

	return 0;
}

/*
 * Sets the stepper motor driver chip to off.
 */
static int drv84xx_off(const struct device *dev, const uint8_t motor)
{
	int ret;
	const struct drv84xx_config *config = dev->config;
	struct drv84xx_data *data = dev->data;
	bool has_enable = config->en_pin.port != NULL;
	bool has_sleep = config->sleep_pin.port != NULL;

	/* Check availability of sleep and and enable pins, as these might be
	 * hardwired. */
	if (!has_sleep && !has_enable) {
		LOG_ERR("%s: Failure to set device to off, neither sleep pin nor enable pin are "
			"available. The device is always on.",
			dev->name);
		return -ENOTSUP;
	}

	if (has_sleep) {
		ret = gpio_pin_set_dt(&config->sleep_pin, 1);
		if (ret != 0) {
			LOG_ERR("%s: Failed to set sleep_pin (error: %d)", dev->name, ret);
			return ret;
		}
		data->pin_states.sleep = 1U;
	}

	if (has_enable) {
		ret = gpio_pin_set_dt(&config->en_pin, 0);
		if (ret != 0) {
			LOG_ERR("%s: Failed to set en_pin (error: %d)", dev->name, ret);
			return ret;
		}
		data->pin_states.en = 0U;
	}

	ret = pwm_set_cycles(config->step_pwm.dev, config->step_pwm.channel, 1U, 0U,
			     config->step_pwm.flags);
	if (ret != 0) {
		LOG_ERR("Error %d: failed to zero pwm", ret);
		return ret;
	}

	return 0;
}

static int drv84xx_set_pwm_off(const struct device *dev)
{
	const struct drv84xx_config *config = dev->config;

#ifdef CONFIG_DT_HAS_RASPBERRYPI_PICO_PWM_ENABLED
	return pwm_set_cycles(config->step_pwm.dev, config->step_pwm.channel, 1, 0, 0);
#elif CONFIG_DT_HAS_ST_STM32_PWM_ENABLED
	return pwm_set_cycles(config->step_pwm.dev, config->step_pwm.channel, 0, 0, 0);
#else
#error "Unsupported PWM platform"
#endif
}

static int drv84xx_set_pwm_freq(const struct device *dev, uint32_t freq_hz)
{
	const struct drv84xx_config *config = dev->config;

	if (freq_hz == 0) {
		return drv84xx_set_pwm_off(dev);
	}

	uint32_t period_width = PWM_SEC(1) / freq_hz;
	uint32_t pulse_width = period_width / 2;
	return pwm_set_dt(&config->step_pwm, period_width, pulse_width);
}

static int drv84xx_set_dir(const struct device *dev, int32_t dir)
{
	const struct drv84xx_config *config = dev->config;
	int ret = 0;

	if (dir >= 0) {
		ret = gpio_pin_set_dt(&config->dir_pin, 1);
	} else {
		ret = gpio_pin_set_dt(&config->dir_pin, 0);
	}

	return ret;
}

/*
 * Executes motor rotation, currently only supports velocity mode
 */
static int drv84xx_move(const struct device *dev, const uint8_t motor,
			const struct stepper_action *action)
{
	const struct drv84xx_config *config = dev->config;
	const struct drv84xx_data *data = dev->data;
	bool has_enable = config->en_pin.port != NULL;
	bool has_sleep = config->sleep_pin.port != NULL;
	int ret = 0;

	if (has_enable) {
		if (data->pin_states.en == 0) {
			LOG_ERR("%s: Stepper is in OFF state", dev->name);
			return -EIO;
		}
	}
	if (has_sleep) {
		if (data->pin_states.sleep == 1) {
			LOG_ERR("%s: Stepper is in OFF state", dev->name);
			return -EIO;
		}
	}

	int microstep_count = STEPPER_USTEP_RES_GET(action->flags);
	/* Log2 as the _RES_GET macro returns a 2^n value*/
	int microstep_id = LOG2(microstep_count);
	ret = drv84xx_set_microstep(dev, microstep_id);
	if (ret != 0) {
		LOG_ERR("%s: Failed to set microsteps (error: %d)", dev->name, ret);
		return ret;
	}

	if (action->type == STEPPER_ACTION_TYPE_VELOCITY) {
		int32_t velocity = action->action.velocity.velocity;
		ret = drv84xx_set_dir(dev, velocity);
		if (ret != 0) {
			LOG_ERR("%s: Failed to set direction pin (error: %d)", dev->name, ret);
			return ret;
		}

		if (labs(velocity) == 0) {
			ret = drv84xx_set_pwm_off(dev);
			if (ret != 0) {
				LOG_ERR("%s: Failed to pause pwm (error: %d)", dev->name, ret);
				return ret;
			}
		} else {
			uint32_t freq_hz = labs(velocity) * microstep_count;
			ret = drv84xx_set_pwm_freq(dev, freq_hz);
			if (ret != 0) {
				LOG_ERR("%s: Failed to set PWM frequency (error: %d)", dev->name,
					ret);
				return ret;
			}
		}

		k_sleep(K_USEC(action->action.velocity.duration_us));

	} else if (action->type == STEPPER_ACTION_TYPE_ACCELERATION) {
		int32_t start_velocity = action->action.acceleration.start_velocity;
		int32_t end_velocity = action->action.acceleration.end_velocity;
		uint32_t duration_us = action->action.acceleration.duration_us;

		/* Measure all time in microseconds */
		uint32_t dt_us = 10;
		uint64_t start_time = k_uptime_get() * USEC_PER_MSEC;
		uint64_t end_time = start_time + duration_us;

		uint64_t now = 0;
		while ((now = (k_uptime_get() * USEC_PER_MSEC)) < end_time) {
			/* Shift time at which we sample by half a timestep to
			 * correct for integral error */
			uint64_t now_plus_half_step = now + (dt_us / 2);

			/* Partition the unit time interval into 1000 pieces to
			 * let us do integer math */
			uint64_t t_milliunit =
				((1000 * (now_plus_half_step - start_time)) / duration_us);

			/* Compute target velocity as convex combination of
			 * start- and end-velocities, with the milliunits as
			 * affine parameter */
			int32_t velocity = ((int32_t)(1000 - t_milliunit) * start_velocity +
					    (int32_t)t_milliunit * end_velocity) /
					   1000;

			/* Clamp velocity to prevent overshooting on the final
			 * timestep */
			if (end_velocity > start_velocity) {
				velocity = MIN(velocity, end_velocity);
			} else {
				velocity = MAX(velocity, end_velocity);
			}

			/* Set direction pin */
			ret = drv84xx_set_dir(dev, velocity);
			if (ret != 0) {
				LOG_ERR("%s: Failed to set direction pin (error: %d)", dev->name,
					ret);
				return ret;
			}

			/* Set PWM frequency to new velocity */
			uint32_t freq_hz = labs(velocity) * microstep_count;
			ret = drv84xx_set_pwm_freq(dev, freq_hz);
			if (ret != 0) {
				LOG_ERR("%s: Failed to set PWM frequency (error: %d)", dev->name,
					ret);
				return ret;
			}

			/* Sleep until the next timestep */
			k_sleep(K_USEC(dt_us));
		}

		/* Set end state explicitely */
		ret = drv84xx_set_dir(dev, end_velocity);
		if (ret != 0) {
			LOG_ERR("%s: Failed to set direction pin (error %d)", dev->name, ret);
			return ret;
		}
		uint32_t end_freq_hz = labs(end_velocity) * microstep_count;
		ret = drv84xx_set_pwm_freq(dev, end_freq_hz);
		if (ret != 0) {
			LOG_ERR("%s: Failed to set PWM frequency (error %d)", dev->name, ret);
			return ret;
		}
	}

	return 0;
}

static const struct stepper_api drv84xx_api = {
	.on = drv84xx_on,
	.off = drv84xx_off,
	.move = drv84xx_move,
};

/*
 * Initializes driver
 */
static int drv84xx_init(const struct device *dev)
{
	const struct drv84xx_config *const config = dev->config;
	struct drv84xx_data *const data = dev->data;
	int ret = 0;

	/* Configure direction pin */
	ret = gpio_pin_configure_dt(&config->dir_pin, GPIO_OUTPUT_ACTIVE);
	if (ret != 0) {
		LOG_ERR("%s: Failed to configure dir_pin (error: %d)", dev->name, ret);
		return ret;
	}

	/* Configure pwm */
	if (!pwm_is_ready_dt(&config->step_pwm)) {
		LOG_ERR("Error: PWM device %s is not ready", config->step_pwm.dev->name);
		return ret;
	} else {
		ret = drv84xx_set_pwm_off(dev);
		if (ret != 0) {
			LOG_ERR("Error %d: failed to initialize PWM", ret);
			return ret;
		}
	}

	/* Configure sleep pin if it is available */
	if (config->sleep_pin.port != NULL) {
		ret = gpio_pin_configure_dt(&config->sleep_pin, GPIO_OUTPUT_ACTIVE);
		if (ret != 0) {
			LOG_ERR("%s: Failed to configure sleep_pin (error: %d)", dev->name, ret);
			return ret;
		}
		data->pin_states.sleep = 1U;
	}

	/* Configure enable pin if it is available */
	if (config->en_pin.port != NULL) {
		ret = gpio_pin_configure_dt(&config->en_pin, GPIO_OUTPUT_INACTIVE);
		if (ret != 0) {
			LOG_ERR("%s: Failed to configure en_pin (error: %d)", dev->name, ret);
			return ret;
		}
		data->pin_states.en = 0U;
	}

	/* Configure microstep pin 0 */
	ret = gpio_pin_configure_dt(&config->m0_pin, GPIO_OUTPUT_INACTIVE);
	if (ret != 0) {
		LOG_ERR("%s: Failed to configure m0_pin (error: %d)", dev->name, ret);
		return ret;
	}
	data->pin_states.m0 = 0U;

	/* Configure microstep pin 1 */
	ret = gpio_pin_configure_dt(&config->m1_pin, GPIO_OUTPUT_INACTIVE);
	if (ret != 0) {
		LOG_ERR("%s: Failed to configure m1_pin (error: %d)", dev->name, ret);
		return ret;
	}
	data->pin_states.m1 = 0U;

	return 0;
}

#define DRV84XX_DEVICE(inst)                                                                       \
	STEPPER_DRIVER_CONFIG_DT_INST_DEFINE(                                                      \
		inst, drv84xx_stepper_driver_config_,                                              \
		(STEPPER_OP_MODE_VELOCITY | STEPPER_OP_MODE_ACCELERATION | STEPPER_USTEP_RES_1 |   \
		 STEPPER_USTEP_RES_2 | STEPPER_USTEP_RES_4 | STEPPER_USTEP_RES_8 |                 \
		 STEPPER_USTEP_RES_16 | STEPPER_USTEP_RES_32 | STEPPER_USTEP_RES_128 |             \
		 STEPPER_USTEP_RES_256));                                                          \
                                                                                                   \
	static const struct drv84xx_config drv84xx_config_##inst = {                               \
		.common = drv84xx_stepper_driver_config_##inst,                                    \
		.dir_pin = GPIO_DT_SPEC_INST_GET(inst, dir_gpios),                                 \
		.step_pwm = PWM_DT_SPEC_INST_GET(inst),                                            \
		.sleep_pin = GPIO_DT_SPEC_INST_GET_OR(inst, sleep_gpios, {0}),                     \
		.en_pin = GPIO_DT_SPEC_INST_GET_OR(inst, en_gpios, {0}),                           \
		.m0_pin = GPIO_DT_SPEC_INST_GET_OR(inst, m0_gpios, {0}),                           \
		.m1_pin = GPIO_DT_SPEC_INST_GET_OR(inst, m1_gpios, {0}),                           \
	};                                                                                         \
                                                                                                   \
	static struct drv84xx_data drv84xx_data_##inst = {0};                                      \
                                                                                                   \
	DEVICE_DT_INST_DEFINE(inst, &drv84xx_init,          /* Init */                             \
			      NULL,                         /* PM */                               \
			      &drv84xx_data_##inst,         /* Data */                             \
			      &drv84xx_config_##inst,       /* Config */                           \
			      POST_KERNEL,                  /* Init stage */                       \
			      CONFIG_STEPPER_INIT_PRIORITY, /* Init priority */                    \
			      &drv84xx_api);                /* API */

DT_INST_FOREACH_STATUS_OKAY(DRV84XX_DEVICE)
