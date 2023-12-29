/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT sipo_mux_gpio

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/pm/device.h>

#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/gpio/gpio_utils.h>

#include <zephyr/drivers/mfd/sipomuxgp.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(gpio_sipomux, CONFIG_GPIO_LOG_LEVEL);

/**
 * @brief SIPO/MUX GPIO controller configuration data
 *
 * This structure contains all of the state for a given SIPO/MUX GPIO
 * controller as well as all of the pins associated with it.
 *
 * @a num_pins must be in the range [1, @ref GPIO_MAX_PINS_PER_PORT].
 *
 * @a num_offs must be in the range [1, SIPO/MUX GP maximum minus @a num_pins].
 *
 * Pin direction as well as other pin properties are set using
 * specific bits in @a flags. For more details, see @ref gpio_interface.
 */
typedef struct gpio_sipomux_config {
	/** Common @ref gpio_driver_config (needs to be first) */
	struct gpio_driver_config common;
	/** Number of pins available in the given GPIO controller instance */
	const gpio_pin_t num_pins;
	/** Number of pins postponed in the given GPIO controller instance */
	const gpio_port_pins_t num_offs;
	/** Backend MFD device for real operations on hardware */
	const struct device *mfd;
} gpio_sipomux_config_t;

/**
 * @brief SIPO/MUX GPIO controller data
 *
 * This structure contains data structures used by a SIPO/MUX GPIO
 * controller.
 *
 * Changes are to @ref gpio_sipomux_data and @ref gpio_sipomux_config are
 * synchronized using @a k_sem.
 */
typedef struct gpio_sipomux_data {
	/** Common @ref gpio_driver_data (needs to be first) */
	struct gpio_driver_data common;
	/** Semaphore to synchronize accesses to driver data and config */
	struct k_sem lock;
	/** Variable for internal operations to avoid optimization effects */
	gpio_port_value_t value;
} gpio_sipomux_data_t;

/*
 * GPIO Driver API
 *
 * API is documented at drivers/gpio.h
 */

static int gpio_sipomux_port_get_raw(const struct device *dev,
				     gpio_port_value_t *value)
{
	const gpio_sipomux_config_t * const config = dev->config;

	return mfd_sipomuxgp_bits(config->mfd, config->num_offs, value);
}

static int gpio_sipomux_port_set_masked_raw(const struct device *dev,
					    gpio_port_pins_t mask,
					    gpio_port_value_t value)
{
	const gpio_sipomux_config_t * const config = dev->config;
	gpio_sipomux_data_t * const data = dev->data;
	int ret = 0;

	k_sem_take(&data->lock, K_FOREVER);

	for (size_t idx = 0; idx < config->num_pins; idx++) {
		if ((mask & BIT(idx)) != 0U) {
			if ((value & BIT(idx)) != 0U) {
				ret = mfd_sipomuxgp_bit_on(config->mfd,
						config->num_offs + idx);
			} else {
				ret = mfd_sipomuxgp_bit_off(config->mfd,
						config->num_offs + idx);
			}
			if (ret != 0U) {
				goto done;
			}
		}
	}

done:
	k_sem_give(&data->lock);
	return ret;
}

static int gpio_sipomux_port_set_bits_raw(const struct device *dev,
					  gpio_port_pins_t pins)
{
	return gpio_sipomux_port_set_masked_raw(dev, pins, pins);
}

static int gpio_sipomux_port_clear_bits_raw(const struct device *dev,
					    gpio_port_pins_t pins)
{
	return gpio_sipomux_port_set_masked_raw(dev, pins, 0U);
}

static inline int gpio_sipomux_configure(const struct device *dev,
					 gpio_pin_t pin, gpio_flags_t flags)
{
	const gpio_sipomux_config_t * const config = dev->config;
	gpio_sipomux_data_t * const data = dev->data;
	int ret = 0;

	/* Can't do bus operations from an ISR */
	if (k_is_in_isr()) {
		return -EWOULDBLOCK;
	}

	if (pin >= config->num_pins) {
		return -EINVAL;
	}

	/* Does not support disconnected pin */
	if ((flags & (GPIO_INPUT | GPIO_OUTPUT)) == GPIO_DISCONNECTED) {
		return -ENOTSUP;
	}

	/* Does not support open-drain pin */
	if ((flags & GPIO_SINGLE_ENDED) != 0U) {
		return -ENOTSUP;
	}

	/* Does not support pulls-up/-down pin */
	if (((flags & GPIO_PULL_UP) != 0U) ||
	    ((flags & GPIO_PULL_DOWN) != 0U)) {
		return -ENOTSUP;
	}

	k_sem_take(&data->lock, K_FOREVER);

	/* Configure mode */
	if ((flags & GPIO_INPUT) != 0U) {
		ret = -ENOTSUP;
		goto done;
	} else if ((flags & GPIO_OUTPUT_INIT_HIGH) != 0U) {
		ret = mfd_sipomuxgp_bit_on(config->mfd,
					   config->num_offs + pin);
	} else if ((flags & GPIO_OUTPUT) != 0U) {
		ret = mfd_sipomuxgp_bit_off(config->mfd,
					    config->num_offs + pin);
	}

done:
	k_sem_give(&data->lock);
	return ret;
}

static int gpio_sipomux_port_toggle_bits(const struct device *dev,
					 gpio_port_pins_t pins)
{
	gpio_sipomux_data_t * const data = dev->data;
	int ret;

	k_sem_take(&data->lock, K_FOREVER);

	ret = gpio_sipomux_port_get_raw(dev, &data->value);
	if (ret < 0) {
		return ret;
	}

	data->value ^= pins;

	k_sem_give(&data->lock);

	return gpio_sipomux_port_set_masked_raw(dev, pins, data->value);
}

static const struct gpio_driver_api gpio_sipomux_api = {
	.pin_configure = gpio_sipomux_configure,
	.port_get_raw = gpio_sipomux_port_get_raw,
	.port_set_masked_raw = gpio_sipomux_port_set_masked_raw,
	.port_set_bits_raw = gpio_sipomux_port_set_bits_raw,
	.port_clear_bits_raw = gpio_sipomux_port_clear_bits_raw,
	.port_toggle_bits = gpio_sipomux_port_toggle_bits,
};

static int gpio_sipomux_init(const struct device *dev)
{
	const gpio_sipomux_config_t * const config = dev->config;
	gpio_sipomux_data_t * const data = dev->data;
	size_t av_pins, rq_pins;

	if (!device_is_ready(config->mfd)) {
		return -ENODEV;
	}

	rq_pins = config->num_pins;
	av_pins = mfd_sipomuxgp_num_bits(config->mfd) - config->num_offs;

	if (rq_pins > av_pins) {
		LOG_ERR("%s: invalid number of requested pins: %u > %u",
			dev->name, rq_pins, av_pins);
		return -EINVAL;
	}

	k_sem_init(&data->lock, 1, 1);

	LOG_DBG("%s: ready for %u pins with MFD backend over %s!", dev->name,
		config->num_pins, config->mfd->name);
	return 0;
}

#ifdef CONFIG_PM_DEVICE
static int gpio_sipomux_pm_device_pm_action(const struct device *dev,
					    enum pm_device_action action)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(action);

	return 0;
}
#endif

#if CONFIG_GPIO_SIPOMUX_INIT_PRIORITY <= CONFIG_MFD_SIPOMUXGP_INIT_PRIORITY
#error GPIO_SIPOMUX_INIT_PRIORITY must be greater than MFD_SIPOMUXGP_INIT_PRIORITY
#endif

#define GPIO_SIPOMUX_DEFINE(n)                                          \
                                                                        \
	static const gpio_sipomux_config_t gpio_sipomux_config_##n =    \
	{                                                               \
		.common = {                                             \
			.port_pin_mask =                                \
				GPIO_PORT_PIN_MASK_FROM_DT_INST(n),     \
		},                                                      \
		.num_pins = DT_INST_PROP(n, ngpios),                    \
		.num_offs = DT_INST_PROP(n, offset),                    \
		.mfd = DEVICE_DT_GET(DT_INST_PARENT(n)),                \
	};                                                              \
	BUILD_ASSERT(                                                   \
		DT_INST_PROP(n, ngpios) <= GPIO_MAX_PINS_PER_PORT,      \
		"Too many ngpios");                                     \
                                                                        \
	static gpio_sipomux_data_t gpio_sipomux_data_##n;               \
                                                                        \
	PM_DEVICE_DT_INST_DEFINE(n, gpio_sipomux_pm_device_pm_action);  \
                                                                        \
	DEVICE_DT_INST_DEFINE(n, gpio_sipomux_init,                     \
			      PM_DEVICE_DT_INST_GET(n),                 \
			      &gpio_sipomux_data_##n,                   \
			      &gpio_sipomux_config_##n, POST_KERNEL,    \
			      CONFIG_GPIO_SIPOMUX_INIT_PRIORITY,        \
			      &gpio_sipomux_api);

DT_INST_FOREACH_STATUS_OKAY(GPIO_SIPOMUX_DEFINE)
