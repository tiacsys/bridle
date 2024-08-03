/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT nxp_sc18is604_gpio

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/pm/device.h>

#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/gpio/gpio_utils.h>

#include <zephyr/drivers/mfd/sc18is604.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(gpio_sc18is604, CONFIG_GPIO_LOG_LEVEL);

/**
 * @brief SC18IM604 GPIO controller configuration data
 *
 * @a num_pins must be in the range [1, @ref SC18IS604_IO_NUM_PINS_MAX].
 *
 * This structure contains all of the state for a given SC18IM604 GPIO
 * controller as well as the binding to related MFD device.
 */
struct gpio_sc18is604_config {
	/** Common @ref gpio_driver_config (needs to be first) */
	struct gpio_driver_config common;
	/** Number of pins available in the given GPIO controller instance */
	const gpio_pin_t num_pins;
	/** Backend MFD (bridge) device for real operations on hardware */
	const struct device *bridge;
};

/**
 * @brief SC18IM604 GPIO controller data
 *
 * This structure contains data structures used by a SC18IM604 GPIO
 * controller.
 *
 * Changes to @ref gpio_sc18is604_data and @ref gpio_sc18is604_config are
 * synchronized using @a k_sem.
 */
struct gpio_sc18is604_data {
	/** Common @ref gpio_driver_data (needs to be first) */
	struct gpio_driver_data common;
	/** Semaphore to synchronize accesses to driver data and config */
	struct k_sem lock;
	/** GPIO pin direction and driver configuration */
	uint8_t pin_config;
	/** GPIO pin level state */
	uint8_t pin_state;
};

static int gpio_sc18is604_pin_write_config(const struct device *dev,
					   uint8_t val)
{
	const struct gpio_sc18is604_config * const config = dev->config;
	struct gpio_sc18is604_data * const data = dev->data;
	int ret = 0;

	ret = WRITE_SC18IS604_REG(config->bridge, IO_CONFIG, val);
	if (ret != 0) {
		goto end;
	}

	k_sem_take(&data->lock, K_FOREVER);

	data->pin_config = val;

	k_sem_give(&data->lock);

end:
	return ret;
}

static int gpio_sc18is604_pin_read_config(const struct device *dev,
					  uint8_t *val)
{
	const struct gpio_sc18is604_config * const config = dev->config;
	struct gpio_sc18is604_data * const data = dev->data;
	int ret = 0;

	ret = READ_SC18IS604_REG(config->bridge, IO_CONFIG, val);
	if (ret != 0) {
		goto end;
	}

	k_sem_take(&data->lock, K_FOREVER);

	data->pin_config = *val;

	k_sem_give(&data->lock);

end:
	return ret;
}

static int gpio_sc18is604_pin_write_state(const struct device *dev,
					  uint8_t val)
{
	const struct gpio_sc18is604_config * const config = dev->config;
	struct gpio_sc18is604_data * const data = dev->data;
	int ret = 0;

	ret = WRITE_SC18IS604_REG(config->bridge, IO_STATE, val);
	if (ret != 0) {
		goto end;
	}

	k_sem_take(&data->lock, K_FOREVER);

	data->pin_state = val;

	k_sem_give(&data->lock);

end:
	return ret;
}

static int gpio_sc18is604_pin_read_state(const struct device *dev,
					 uint8_t *val)
{
	const struct gpio_sc18is604_config * const config = dev->config;
	struct gpio_sc18is604_data * const data = dev->data;
	int ret = 0;

	ret = READ_SC18IS604_REG(config->bridge, IO_STATE, val);
	if (ret != 0) {
		goto end;
	}

	k_sem_take(&data->lock, K_FOREVER);

	data->pin_state = *val;

	k_sem_give(&data->lock);

end:
	return ret;
}

static int gpio_sc18is604_pin_configure(const struct device *dev,
					gpio_pin_t pin, gpio_flags_t flags)
{
	struct gpio_sc18is604_data * const data = dev->data;
	uint8_t shift, bits, pin_config, pin_state;
	int ret = 0;

	/* Can't do bus operations from an ISR */
	if (k_is_in_isr()) {
		return -EWOULDBLOCK;
	}

	/* Can only configure SC18IS604_IO_NUM_PINS_INOUT pins */
	if (pin >= SC18IS604_IO_NUM_PINS_INOUT) {

		/* Can only handle SC18IS604_IO_NUM_PINS_MAX pins */
		if (pin >= SC18IS604_IO_NUM_PINS_MAX) {
			return -ENOTSUP;

		/* SC18IS604_IO_NUM_PINS_MAX - SC18IS604_IO_NUM_PINS_INOUT */
		} else if ((flags & GPIO_INPUT) == GPIO_INPUT) {

			/*
			 * Do nothing for the highest pin numbers,
			 * input is the default and can not change.
			 */
			goto end;

		} else {
			return -ENOTSUP;
		}
	}

	/* Does not support disconnected pin */
	if ((flags & (GPIO_INPUT | GPIO_OUTPUT)) == GPIO_DISCONNECTED) {
		return -ENOTSUP;
	}

	k_sem_take(&data->lock, K_FOREVER);

	pin_config = data->pin_config;
	pin_state = data->pin_state;

	k_sem_give(&data->lock);

	/* Prepare new configuration for target pin */
	shift = 2 * pin; /* Each pin has two configuration bits */
	bits = 0b00;

	if ((flags & GPIO_INPUT) == GPIO_INPUT) {
		bits = SC18IS604_IO_CONFIG_INPUT;
	} else if ((flags & GPIO_OUTPUT) == GPIO_OUTPUT) {
		if ((flags & GPIO_OPEN_DRAIN) == GPIO_OPEN_DRAIN) {
			bits = SC18IS604_IO_CONFIG_OPEN_DRAIN;
		} else {
			bits = SC18IS604_IO_CONFIG_PUSH_PULL;
		}
	}

	pin_config &= ~(0b11 << shift); /* Clear config bits */
	pin_config |= (bits << shift);  /* Set new config */

	/* Apply configuration */
	ret = gpio_sc18is604_pin_write_config(dev, pin_config);
	if (ret != 0) {
		goto end;
	}

	/* For output pins, state might also be configured */
	if ((flags & GPIO_OUTPUT) == GPIO_OUTPUT) {
		if ((flags & GPIO_OUTPUT_INIT_HIGH) == GPIO_OUTPUT_INIT_HIGH) {
			pin_state |= BIT(pin);
		} else if ((flags & GPIO_OUTPUT_INIT_LOW) == GPIO_OUTPUT_INIT_LOW) {
			pin_state &= ~BIT(pin);
		}

		/* Apply pin state */
		ret = gpio_sc18is604_pin_write_state(dev, pin_state);
		if (ret != 0) {
			goto end;
		}
	}

end:
	return ret;
}

static int gpio_sc18is604_get_raw(const struct device *dev, uint32_t *value)
{
	uint8_t buf = 0x00;
	int ret = 0;

	/* Can't do bus operations from an ISR */
	if (k_is_in_isr()) {
		return -EWOULDBLOCK;
	}

	/* Read current state from device */
	ret = gpio_sc18is604_pin_read_state(dev, &buf);
	if (ret != 0) {
		goto end;
	}

	/* Return through pointer */
	*value = buf;

end:
	return ret;
}

static int gpio_sc18is604_set_masked_raw(const struct device *dev,
					 uint32_t mask, uint32_t value)
{
	struct gpio_sc18is604_data * const data = dev->data;
	uint8_t pin_state;

	/* Can't do operations from an ISR */
	if (k_is_in_isr()) {
		return -EWOULDBLOCK;
	}

	k_sem_take(&data->lock, K_FOREVER);

	/* Get (cached) state, and set bits to value according to mask */
	pin_state = data->pin_state;
	pin_state = (pin_state & ~mask) | (mask & value); /* BYTE macro ? */

	k_sem_give(&data->lock);

	/* Apply new pin state */
	return gpio_sc18is604_pin_write_state(dev, pin_state);
}

static int gpio_sc18is604_set_bits_raw(const struct device *dev, uint32_t pins)
{
	return gpio_sc18is604_set_masked_raw(dev, pins, pins);
}

static int gpio_sc18is604_clear_bits_raw(const struct device *dev, uint32_t pins)
{
	return gpio_sc18is604_set_masked_raw(dev, pins, 0U);
}

static int gpio_sc18is604_toggle_bits(const struct device *dev, uint32_t pins)
{
	struct gpio_sc18is604_data * const data = dev->data;
	uint8_t pin_state;

	/* Can't do operations from an ISR */
	if (k_is_in_isr()) {
		return -EWOULDBLOCK;
	}

	k_sem_take(&data->lock, K_FOREVER);

	/* Get (cached) state, and toggle bits according to mask */
	pin_state = data->pin_state;
	pin_state ^= pins; /* BYTE macro ? */

	k_sem_give(&data->lock);

	/* Apply new pin state */
	return gpio_sc18is604_pin_write_state(dev, pin_state);
}

static const struct gpio_driver_api gpio_sc18is604_api = {
	.pin_configure = gpio_sc18is604_pin_configure,
	.port_get_raw = gpio_sc18is604_get_raw,
	.port_set_masked_raw = gpio_sc18is604_set_masked_raw,
	.port_set_bits_raw = gpio_sc18is604_set_bits_raw,
	.port_clear_bits_raw = gpio_sc18is604_clear_bits_raw,
	.port_toggle_bits = gpio_sc18is604_toggle_bits,
};

static int gpio_sc18is604_init(const struct device *dev)
{
	const struct gpio_sc18is604_config * const config = dev->config;
	struct gpio_sc18is604_data * const data = dev->data;
	uint8_t buf;

	/* Check MFD (bridge) readiness */
	if (!device_is_ready(config->bridge)) {
		LOG_ERR("%s: bridge device %s not ready",
			dev->name, config->bridge->name);
		return -ENODEV;
	}

	k_sem_init(&data->lock, 1, 1);

	/* Initialize register cache */
	gpio_sc18is604_pin_read_state(dev, &buf);
	gpio_sc18is604_pin_read_config(dev, &buf);

	LOG_DBG("%s: ready for %u pins with bridge backend over %s!",
		dev->name, config->num_pins, config->bridge->name);
	return 0;
}

#ifdef CONFIG_PM_DEVICE
static int gpio_sc18is604_pm_device_pm_action(const struct device *dev,
					      enum pm_device_action action)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(action);

	return 0;
}
#endif

#define GPIO_SC18IS604_DEFINE(inst)                                          \
                                                                             \
	static const                                                         \
	struct gpio_sc18is604_config gpio_sc18is604_config_##inst =          \
	{                                                                    \
		.common = {                                                  \
			.port_pin_mask =                                     \
				GPIO_PORT_PIN_MASK_FROM_DT_INST(inst),       \
		},                                                           \
		.num_pins = DT_INST_PROP(inst, ngpios),                      \
		.bridge = DEVICE_DT_GET(DT_INST_BUS(inst)),                  \
	};                                                                   \
	BUILD_ASSERT(                                                        \
		DT_INST_PROP(inst, ngpios) <= SC18IS604_IO_NUM_PINS_MAX,     \
		"Too many ngpios");                                          \
                                                                             \
	static struct gpio_sc18is604_data gpio_sc18is604_data_##inst;        \
                                                                             \
	PM_DEVICE_DT_INST_DEFINE(inst, gpio_sc18is604_pm_device_pm_action);  \
                                                                             \
	DEVICE_DT_INST_DEFINE(inst, gpio_sc18is604_init,                     \
			      PM_DEVICE_DT_INST_GET(inst),                   \
			      &gpio_sc18is604_data_##inst,                   \
			      &gpio_sc18is604_config_##inst, POST_KERNEL,    \
			      CONFIG_GPIO_SC18IS604_INIT_PRIORITY,           \
			      &gpio_sc18is604_api);

DT_INST_FOREACH_STATUS_OKAY(GPIO_SC18IS604_DEFINE);
