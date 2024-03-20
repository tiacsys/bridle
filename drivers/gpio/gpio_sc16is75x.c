/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT nxp_sc16is75x_gpio

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/pm/device.h>

#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/gpio/gpio_utils.h>

#include <zephyr/drivers/mfd/sc16is75x.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(gpio_sc16is75x, CONFIG_GPIO_LOG_LEVEL);

/**
 * @brief SC16IS75X GPIO controller configuration data
 *
 * @a num_pins must be in the range [1, @ref SC16IS75X_IO_NUM_PINS_MAX].
 *
 * This structure contains all of the state for a given SC16IS75X GPIO
 * controller as well as the binding to related MFD device.
 */
struct gpio_sc16is75x_config {
	/** Common @ref gpio_driver_config (needs to be first) */
	struct gpio_driver_config common;
	/** Backend MFD (bridge) device for real operations on hardware */
	const struct device *bus;
	/** Number of pins available in the given GPIO controller instance */
	const gpio_pin_t num_pins;
};

/**
 * @brief SC16IS75X GPIO controller data
 *
 * This structure contains data structures used by a SC16IS75X GPIO controller.
 *
 * Changes to @ref gpio_sc16is75x_data and @ref gpio_sc16is75x_config and also
 * multi-transfer bus transactions are synchronized using @a k_mutex.
 */
struct gpio_sc16is75x_data {
	/** Common @ref gpio_driver_data (needs to be first) */
	struct gpio_driver_data common;
	/** Lock for synchronizing accesses to driver data and config */
	struct k_mutex lock;
	/** GPIO pin direction */
	uint8_t pin_dir;
	/** GPIO pin level state */
	uint8_t pin_state;
};

static inline uint8_t gpio_sc16is75x_cached_pin_dir(const struct device *dev)
{
	struct gpio_sc16is75x_data * const data = dev->data;
	uint8_t pin_dir;

	k_mutex_lock(&data->lock, K_FOREVER);
	pin_dir = data->pin_dir;
	k_mutex_unlock(&data->lock);

	return pin_dir;
}

static inline int gpio_sc16is75x_write_pin_dir(const struct device *dev,
					       const uint8_t dir)
{
	const struct gpio_sc16is75x_config * const config = dev->config;
	struct gpio_sc16is75x_data * const data = dev->data;
	int ret = 0;

	k_mutex_lock(&data->lock, K_FOREVER);
	ret = WRITE_SC16IS75X_REG(config->bus, IODIR, dir);
	if (ret == 0) {
		data->pin_dir = dir;
	}
	k_mutex_unlock(&data->lock);

	return ret;
}

static inline int gpio_sc16is75x_read_pin_dir(const struct device *dev,
					      uint8_t *dir)
{
	const struct gpio_sc16is75x_config * const config = dev->config;
	struct gpio_sc16is75x_data * const data = dev->data;
	int ret = 0;

	k_mutex_lock(&data->lock, K_FOREVER);
	ret = READ_SC16IS75X_REG(config->bus, IODIR, dir);
	if (ret == 0) {
		data->pin_dir = *dir;
	}
	k_mutex_unlock(&data->lock);

	return ret;
}

static inline uint8_t gpio_sc16is75x_cached_pin_state(const struct device *dev)
{
	struct gpio_sc16is75x_data * const data = dev->data;
	uint8_t pin_state;

	k_mutex_lock(&data->lock, K_FOREVER);
	pin_state = data->pin_state;
	k_mutex_unlock(&data->lock);

	return pin_state;
}

static inline int gpio_sc16is75x_write_pin_state(const struct device *dev,
						 uint8_t state)
{
	const struct gpio_sc16is75x_config * const config = dev->config;
	struct gpio_sc16is75x_data * const data = dev->data;
	int ret = 0;

	k_mutex_lock(&data->lock, K_FOREVER);
	ret = WRITE_SC16IS75X_REG(config->bus, IOSTATE, state);
	if (ret == 0) {
		data->pin_state = state;
	}
	k_mutex_unlock(&data->lock);

	return ret;
}

static inline int gpio_sc16is75x_read_pin_state(const struct device *dev,
						uint8_t *state)
{
	const struct gpio_sc16is75x_config * const config = dev->config;
	struct gpio_sc16is75x_data * const data = dev->data;
	int ret = 0;

	k_mutex_lock(&data->lock, K_FOREVER);
	ret = READ_SC16IS75X_REG(config->bus, IOSTATE, state);
	if (ret == 0) {
		data->pin_state = *state;
	}
	k_mutex_unlock(&data->lock);

	return ret;
}

static int gpio_sc16is75x_pin_configure(const struct device *dev,
					gpio_pin_t pin, gpio_flags_t flags)
{
	const struct gpio_sc16is75x_config * const config = dev->config;
	uint8_t dir, state;
	int ret = 0;

	/* Can't do bus operations from an ISR */
	if (k_is_in_isr()) {
		return -EWOULDBLOCK;
	}

	/* Check for invalid pin number */
	if ((BIT(pin) & config->common.port_pin_mask) == 0) {
		return -EINVAL;
	}

	/* Does not support open source/drain pin */
	if (flags & (GPIO_OPEN_SOURCE | GPIO_OPEN_DRAIN)) {
		return -ENOTSUP;
	}
	/* Does not support pull-up/pull-down pin resistor */
	if (flags & (GPIO_PULL_UP | GPIO_PULL_DOWN)) {
		return -ENOTSUP;
	}

	/* Does not support disconnected pin */
	if ((flags & (GPIO_INPUT | GPIO_OUTPUT)) == GPIO_DISCONNECTED) {
		return -ENOTSUP;
	}

	/* Get (cached) port direction and state */
	dir = gpio_sc16is75x_cached_pin_dir(dev);
	state = gpio_sc16is75x_cached_pin_state(dev);

	/* Calculate new pin direction and state */
	if (flags & GPIO_OUTPUT) {
		dir |= BIT(pin); /* set direction bit */
		if (flags & GPIO_OUTPUT_INIT_HIGH) {
			state |= BIT(pin); /* set state bit */
		} else if (flags & GPIO_OUTPUT_INIT_LOW) {
			state &= ~BIT(pin); /* clear state bit */
		}
	} else if (flags & GPIO_INPUT) {
		dir &= ~BIT(pin); /* clear direction bit */
	} else {
		return -EINVAL;
	}

	/* Set (cached) port direction to new value */
	if (gpio_sc16is75x_cached_pin_dir(dev) != dir) {
		ret = gpio_sc16is75x_write_pin_dir(dev, dir);
		if (ret != 0) {
			goto end;
		}
	}

	/* Set (cached) port state to new value */
	if (gpio_sc16is75x_cached_pin_state(dev) != state) {
		ret = gpio_sc16is75x_write_pin_state(dev, state);
		if (ret != 0) {
			goto end;
		}
	}

end:
	return ret;
}

static int gpio_sc16is75x_port_get_raw(const struct device *dev,
				       gpio_port_value_t *value)
{
	uint8_t * const state = (uint8_t *)value;

	/* Can't do bus operations from an ISR */
	if (k_is_in_isr()) {
		return -EWOULDBLOCK;
	}

	/* Read current state from device */
	return gpio_sc16is75x_read_pin_state(dev, state);
}

static int gpio_sc16is75x_port_set_masked_raw(const struct device *dev,
					      const gpio_port_pins_t mask,
					      const gpio_port_value_t value)
{
	uint8_t state = gpio_sc16is75x_cached_pin_state(dev);

	/* Can't do bus operations from an ISR */
	if (k_is_in_isr()) {
		return -EWOULDBLOCK;
	}

	/* Get (cached) port state, and set bits according to pin mask */
	state = (state & ~mask) | (mask & value);

	/* Apply the new pin state */
	return gpio_sc16is75x_write_pin_state(dev, state);
}

static int gpio_sc16is75x_port_set_bits_raw(const struct device *dev,
					    const gpio_port_pins_t pins)
{
	return gpio_sc16is75x_port_set_masked_raw(dev, pins, pins);
}

static int gpio_sc16is75x_port_clear_bits_raw(const struct device *dev,
					      const gpio_port_pins_t pins)
{
	return gpio_sc16is75x_port_set_masked_raw(dev, pins, 0);
}

static int gpio_sc16is75x_port_toggle_bits(const struct device *dev,
					   const gpio_port_pins_t pins)
{
	uint8_t state = gpio_sc16is75x_cached_pin_state(dev);

	/* Can't do bus operations from an ISR */
	if (k_is_in_isr()) {
		return -EWOULDBLOCK;
	}

	/* Get (cached) state, and toggle bits according to mask */
	state ^= pins;

	/* Apply new pin state */
	return gpio_sc16is75x_write_pin_state(dev, state);
}

static const struct gpio_driver_api gpio_sc16is75x_api = {
	.pin_configure = gpio_sc16is75x_pin_configure,
	.port_get_raw = gpio_sc16is75x_port_get_raw,
	.port_set_masked_raw = gpio_sc16is75x_port_set_masked_raw,
	.port_set_bits_raw = gpio_sc16is75x_port_set_bits_raw,
	.port_clear_bits_raw = gpio_sc16is75x_port_clear_bits_raw,
	.port_toggle_bits = gpio_sc16is75x_port_toggle_bits,
};

static int gpio_sc16is75x_init(const struct device *dev)
{
	const struct gpio_sc16is75x_config * const config = dev->config;
	struct gpio_sc16is75x_data * const data = dev->data;
	int ret = 0;

	/* Confirm (MFD) bridge readiness */
	if (!device_is_ready(config->bus)) {
		LOG_ERR("%s: bridge device %s not ready",
			dev->name, config->bus->name);
		return -ENODEV;
	}

	/* Initialize synchronization lock */
	k_mutex_init(&data->lock);

	ret = gpio_sc16is75x_read_pin_state(dev, &data->pin_state);
	if (ret != 0) {
		LOG_ERR("%s: read pin state failed: %d",
			dev->name, ret);
		goto end;
	}

	LOG_DBG("%s: ready for %u pins with bridge backend over %s!",
		dev->name, config->num_pins, config->bus->name);

end:
	return ret;
}

#ifdef CONFIG_PM_DEVICE
static int gpio_sc16is75x_pm_device_pm_action(const struct device *dev,
					      enum pm_device_action action)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(action);

	return 0;
}
#endif

#define GPIO_SC16IS75X_DEFINE(inst)                                          \
                                                                             \
	static struct gpio_sc16is75x_config gpio_sc16is75x_config_##inst =   \
	{                                                                    \
		.common = {                                                  \
			.port_pin_mask =                                     \
				GPIO_PORT_PIN_MASK_FROM_DT_INST(inst),       \
		},                                                           \
		.bus = DEVICE_DT_GET(DT_INST_BUS(inst)),                     \
		.num_pins = DT_INST_PROP(inst, ngpios),                      \
	};                                                                   \
	BUILD_ASSERT(                                                        \
		DT_INST_PROP(inst, ngpios) <= SC16IS75X_IO_NUM_PINS_MAX,     \
		"Too many ngpios");                                          \
                                                                             \
	static struct gpio_sc16is75x_data gpio_sc16is75x_data_##inst;        \
                                                                             \
	PM_DEVICE_DT_INST_DEFINE(inst, gpio_sc16is75x_pm_device_pm_action);  \
                                                                             \
	DEVICE_DT_INST_DEFINE(inst, gpio_sc16is75x_init,                     \
			      PM_DEVICE_DT_INST_GET(inst),                   \
			      &gpio_sc16is75x_data_##inst,                   \
			      &gpio_sc16is75x_config_##inst, POST_KERNEL,    \
			      CONFIG_GPIO_SC16IS75X_INIT_PRIORITY,           \
			      &gpio_sc16is75x_api);

DT_INST_FOREACH_STATUS_OKAY(GPIO_SC16IS75X_DEFINE);
