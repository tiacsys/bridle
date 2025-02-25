/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief Driver for the GPIO controller part of an SC16IS75x bridge
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
 * @brief    GPIO controller part of an SC16IS75x bridge
 * @defgroup io_gpio_sc16is75x SC16IS75x GPIO Controller
 * @ingroup  io_gpio
 * @since    3.7
 * @version  1.0.0
 *
 * The GPIO controller part based on the MFD interface to the SC16IS75x
 * SPI/I2C to UART and GPIO controller bridge.
 *
 * @{
 */

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

#ifdef CONFIG_GPIO_SC16IS75X_INTERRUPTS

/**
 * @brief SC16IS75X cache data for interrupt configuration and emulation
 *
 * The SC16IS75X can only detect signal changes, level-controlled
 * interrupts are therefore not possible. The driver emulates these
 * in order to support all possible types of interrupt configuration
 * from the GPIO API. This requires internal cached data per GPIO pin
 * for the calculation of edge and level triggered events.
 */
struct gpio_sc16is75x_interrupts {
	uint8_t enabled;      /**< pin is event source */
	uint8_t edge_rising;  /**< pin should trigger on rising edge */
	uint8_t edge_falling; /**< pin should trigger on falling edge */
	uint8_t level_high;   /**< pin should trigger on high level */
	uint8_t level_low;    /**< pin should trigger on low level */
};

#endif /* CONFIG_GPIO_SC16IS75X_INTERRUPTS */

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
	/** Device self-reference for the interruption treatment */
	const struct device *self;
	/** MFD bridge interrupt callback */
	struct gpio_callback interrupt_cb;
	/** MFD bridge interrupt worker */
	struct k_work interrupt_work;
	/** Lock for synchronizing accesses to driver data and config */
	struct k_mutex lock;
	/** GPIO pin direction */
	uint8_t pin_dir;
	/** GPIO pin level state */
	uint8_t pin_state;
#ifdef CONFIG_GPIO_SC16IS75X_INTERRUPTS
	/** GPIO pin interrupt trigger */
	struct gpio_sc16is75x_interrupts pin_irq;
	/** GPIO port interrupt callback list */
	sys_slist_t callbacks;
#endif /* CONFIG_GPIO_SC16IS75X_INTERRUPTS */
};

static inline uint8_t gpio_sc16is75x_cached_pin_dir(const struct device *dev)
{
	struct gpio_sc16is75x_data *const data = dev->data;
	uint8_t pin_dir;

	k_mutex_lock(&data->lock, K_FOREVER);
	pin_dir = data->pin_dir;
	k_mutex_unlock(&data->lock);

	return pin_dir;
}

static inline int gpio_sc16is75x_write_pin_dir(const struct device *dev, const uint8_t dir)
{
	const struct gpio_sc16is75x_config *const config = dev->config;
	struct gpio_sc16is75x_data *const data = dev->data;
	int ret = 0;

	k_mutex_lock(&data->lock, K_FOREVER);
	ret = WRITE_SC16IS75X_REG(config->bus, IODIR, dir);
	if (ret == 0) {
		data->pin_dir = dir;
	}
	k_mutex_unlock(&data->lock);

	return ret;
}

static inline int gpio_sc16is75x_read_pin_dir(const struct device *dev, uint8_t *dir)
{
	const struct gpio_sc16is75x_config *const config = dev->config;
	struct gpio_sc16is75x_data *const data = dev->data;
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
	struct gpio_sc16is75x_data *const data = dev->data;
	uint8_t pin_state;

	k_mutex_lock(&data->lock, K_FOREVER);
	pin_state = data->pin_state;
	k_mutex_unlock(&data->lock);

	return pin_state;
}

static inline int gpio_sc16is75x_write_pin_state(const struct device *dev, uint8_t state)
{
	const struct gpio_sc16is75x_config *const config = dev->config;
	struct gpio_sc16is75x_data *const data = dev->data;
	int ret = 0;

	k_mutex_lock(&data->lock, K_FOREVER);
	ret = WRITE_SC16IS75X_REG(config->bus, IOSTATE, state);
	if (ret == 0) {
		data->pin_state = state;
	}
	k_mutex_unlock(&data->lock);

	return ret;
}

static inline int gpio_sc16is75x_read_pin_state(const struct device *dev, uint8_t *state)
{
	const struct gpio_sc16is75x_config *const config = dev->config;
	struct gpio_sc16is75x_data *const data = dev->data;
	int ret = 0;

	k_mutex_lock(&data->lock, K_FOREVER);
	ret = READ_SC16IS75X_REG(config->bus, IOSTATE, state);
	if (ret == 0) {
		data->pin_state = *state;
	}
	k_mutex_unlock(&data->lock);

	return ret;
}

static int gpio_sc16is75x_pin_configure(const struct device *dev, gpio_pin_t pin,
					gpio_flags_t flags)
{
	const struct gpio_sc16is75x_config *const config = dev->config;
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

static int gpio_sc16is75x_port_get_raw(const struct device *dev, gpio_port_value_t *value)
{
	uint8_t *const state = (uint8_t *)value;

	/* Can't do bus operations from an ISR */
	if (k_is_in_isr()) {
		return -EWOULDBLOCK;
	}

	/* Read current state from device */
	return gpio_sc16is75x_read_pin_state(dev, state);
}

static int gpio_sc16is75x_port_set_masked_raw(const struct device *dev, const gpio_port_pins_t mask,
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

static int gpio_sc16is75x_port_set_bits_raw(const struct device *dev, const gpio_port_pins_t pins)
{
	return gpio_sc16is75x_port_set_masked_raw(dev, pins, pins);
}

static int gpio_sc16is75x_port_clear_bits_raw(const struct device *dev, const gpio_port_pins_t pins)
{
	return gpio_sc16is75x_port_set_masked_raw(dev, pins, 0);
}

static int gpio_sc16is75x_port_toggle_bits(const struct device *dev, const gpio_port_pins_t pins)
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

#ifdef CONFIG_GPIO_SC16IS75X_INTERRUPTS

static inline int gpio_sc16is75x_write_pin_irq(const struct device *dev, const gpio_pin_t pin,
					       const enum gpio_int_mode mode,
					       const enum gpio_int_trig trig)
{
	const struct gpio_sc16is75x_config *const config = dev->config;
	struct gpio_sc16is75x_data *const data = dev->data;
	struct gpio_sc16is75x_interrupts *const irq = &data->pin_irq;
	int ret = 0;

	/* Update interrupt masks */
	bool enabled = !(mode & GPIO_INT_MODE_DISABLED);
	bool edge = (mode == GPIO_INT_MODE_EDGE);
	bool level = (mode == GPIO_INT_MODE_LEVEL);
	bool high = ((trig & GPIO_INT_TRIG_HIGH) == GPIO_INT_TRIG_HIGH);
	bool low = ((trig & GPIO_INT_TRIG_LOW) == GPIO_INT_TRIG_LOW);

	k_mutex_lock(&data->lock, K_FOREVER);
	WRITE_BIT(irq->enabled, pin, enabled);
	WRITE_BIT(irq->edge_rising, pin, enabled && edge && high);
	WRITE_BIT(irq->edge_falling, pin, enabled && edge && low);
	WRITE_BIT(irq->level_high, pin, enabled && level && high);
	WRITE_BIT(irq->level_low, pin, enabled && level && low);
	ret = WRITE_SC16IS75X_REG(config->bus, IOINTENA, irq->enabled);
	k_mutex_unlock(&data->lock);

	return ret;
}

static inline gpio_port_pins_t gpio_sc16is75x_trig_edge(const struct device *dev,
							const gpio_port_pins_t changed_pins,
							const gpio_port_pins_t new_state)
{
	struct gpio_sc16is75x_data *const data = dev->data;
	struct gpio_sc16is75x_interrupts *const irq = &data->pin_irq;
	gpio_port_pins_t trig_edge;

	k_mutex_lock(&data->lock, K_FOREVER);
	trig_edge = (changed_pins & new_state & irq->edge_rising) |
		    (changed_pins & ~new_state & irq->edge_falling);
	k_mutex_unlock(&data->lock);

	return trig_edge;
}

static inline gpio_port_pins_t gpio_sc16is75x_trig_level(const struct device *dev,
							 const gpio_port_pins_t changed_pins,
							 const gpio_port_pins_t new_state)
{
	struct gpio_sc16is75x_data *const data = dev->data;
	struct gpio_sc16is75x_interrupts *const irq = &data->pin_irq;
	gpio_port_pins_t trig_level;

	k_mutex_lock(&data->lock, K_FOREVER);
	trig_level = (changed_pins & new_state & irq->level_high) |
		     (changed_pins & ~new_state & irq->level_low);
	k_mutex_unlock(&data->lock);

	return trig_level;
}

static void gpio_sc16is75x_interrupt_work_fn(struct k_work *work)
{
	struct gpio_sc16is75x_data *const data =
		CONTAINER_OF(work, struct gpio_sc16is75x_data, interrupt_work);
	const struct device *const dev = data->self;
	gpio_port_pins_t changed_pins, triggered_pins;
	gpio_port_pins_t triggered_edge, triggered_level;
	uint8_t cur_state, new_state;
	int ret = 0;

	/*
	 * Read out input values and compare with previously cached values.
	 * Note that reading the inputs clears the interrupt.
	 */
	cur_state = gpio_sc16is75x_cached_pin_state(dev);
	new_state = 0;

	ret = gpio_sc16is75x_read_pin_state(dev, &new_state);
	if (ret != 0) {
		return;
	}

	changed_pins = (cur_state ^ new_state);

	/* Calculate trigger sources */
	triggered_edge = gpio_sc16is75x_trig_edge(dev, changed_pins, new_state);
	triggered_level = gpio_sc16is75x_trig_level(dev, changed_pins, new_state);

	/* Propagate triggered pins */
	triggered_pins = (triggered_edge | triggered_level);
	if (triggered_pins) {
		gpio_fire_callbacks(&data->callbacks, data->self, triggered_pins);
	}

	/* Emulate level triggering */
	if (triggered_level) {
		k_work_submit(&data->interrupt_work); /* Reschedule self */
	}
}

static void gpio_sc16is75x_interrupt_callback(const struct device *dev, struct gpio_callback *cb,
					      gpio_port_pins_t event_pins)
{
	/*
	 * The emulation of level-triggered interrupts requires
	 * an automatic rescheduling in the worker queue. The work
	 * item is therefore scheduled immediately for all entries.
	 */
	struct gpio_sc16is75x_data *const data =
		CONTAINER_OF(cb, struct gpio_sc16is75x_data, interrupt_cb);

	k_work_submit(&data->interrupt_work);
}

static int gpio_sc16is75x_pin_interrupt_configure(const struct device *dev, const gpio_pin_t pin,
						  const enum gpio_int_mode mode,
						  const enum gpio_int_trig trig)
{
	const struct gpio_sc16is75x_config *const config = dev->config;

	/* Check for invalid pin number */
	if ((BIT(pin) & config->common.port_pin_mask) == 0) {
		return -EINVAL;
	}

	/* Confirm that specific pin is configured as input */
	if (BIT(pin) & gpio_sc16is75x_cached_pin_dir(dev)) {
		/* setted bit means output, thus not supported */
		return -ENOTSUP;
	}

	return gpio_sc16is75x_write_pin_irq(dev, pin, mode, trig);
}

static int gpio_sc16is75x_manage_callback(const struct device *dev, struct gpio_callback *callback,
					  const bool set)
{
	struct gpio_sc16is75x_data *const data = dev->data;

	return gpio_manage_callback(&data->callbacks, callback, set);
}

#endif /* CONFIG_GPIO_SC16IS75X_INTERRUPTS */

static const struct gpio_driver_api gpio_sc16is75x_api = {
	.pin_configure = gpio_sc16is75x_pin_configure,
	.port_get_raw = gpio_sc16is75x_port_get_raw,
	.port_set_masked_raw = gpio_sc16is75x_port_set_masked_raw,
	.port_set_bits_raw = gpio_sc16is75x_port_set_bits_raw,
	.port_clear_bits_raw = gpio_sc16is75x_port_clear_bits_raw,
	.port_toggle_bits = gpio_sc16is75x_port_toggle_bits,
#ifdef CONFIG_GPIO_SC16IS75X_INTERRUPTS
	.pin_interrupt_configure = gpio_sc16is75x_pin_interrupt_configure,
	.manage_callback = gpio_sc16is75x_manage_callback,
#endif /* CONFIG_GPIO_SC16IS75X_INTERRUPTS */
};

static int gpio_sc16is75x_init(const struct device *dev)
{
	const struct gpio_sc16is75x_config *const config = dev->config;
	struct gpio_sc16is75x_data *const data = dev->data;
	int ret = 0;

	/* Confirm (MFD) bridge readiness */
	if (!device_is_ready(config->bus)) {
		LOG_ERR("%s: bridge device %s not ready", dev->name, config->bus->name);
		return -ENODEV;
	}

	/* Initialize synchronization lock */
	k_mutex_init(&data->lock);

	/* Initialize register cache for interrupt handling */
	ret = gpio_sc16is75x_read_pin_dir(dev, &data->pin_dir);
	if (ret != 0) {
		LOG_ERR("%s: read pin directions failed: %d", dev->name, ret);
		goto end;
	}

	ret = gpio_sc16is75x_read_pin_state(dev, &data->pin_state);
	if (ret != 0) {
		LOG_ERR("%s: read pin state failed: %d", dev->name, ret);
		goto end;
	}

#ifdef CONFIG_GPIO_SC16IS75X_INTERRUPTS

	/* Set up interrupt handling */

	/* Create back-reference to acces device from handler */
	data->self = dev;

	/* Set up handler work item */
	k_work_init(&data->interrupt_work, gpio_sc16is75x_interrupt_work_fn);

	/* Set up and register our own callback on our parent device */
	gpio_init_callback(&data->interrupt_cb, gpio_sc16is75x_interrupt_callback,
			   BIT(SC16IS75X_EVENT_IO0_STATE) | BIT(SC16IS75X_EVENT_IO1_STATE));

	ret = mfd_sc16is75x_add_callback(config->bus, &data->interrupt_cb);
	if (ret != 0) {
		LOG_ERR("%s: failed to register interrupt callback on %s: %d", dev->name,
			config->bus->name, ret);
		goto end;
	}

#endif /* CONFIG_GPIO_SC16IS75X_INTERRUPTS */

	LOG_DBG("%s: ready for %u pins with bridge backend over %s!", dev->name, config->num_pins,
		config->bus->name);

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

#define GPIO_SC16IS75X_DEFINE(inst)                                                                \
                                                                                                   \
	static struct gpio_sc16is75x_config gpio_sc16is75x_config_##inst = {                       \
		.common =                                                                          \
			{                                                                          \
				.port_pin_mask = GPIO_PORT_PIN_MASK_FROM_DT_INST(inst),            \
			},                                                                         \
		.bus = DEVICE_DT_GET(DT_INST_BUS(inst)),                                           \
		.num_pins = DT_INST_PROP(inst, ngpios),                                            \
	};                                                                                         \
	BUILD_ASSERT(DT_INST_PROP(inst, ngpios) <= SC16IS75X_IO_NUM_PINS_MAX, "Too many ngpios");  \
                                                                                                   \
	static struct gpio_sc16is75x_data gpio_sc16is75x_data_##inst;                              \
                                                                                                   \
	PM_DEVICE_DT_INST_DEFINE(inst, gpio_sc16is75x_pm_device_pm_action);                        \
                                                                                                   \
	DEVICE_DT_INST_DEFINE(inst, gpio_sc16is75x_init, PM_DEVICE_DT_INST_GET(inst),              \
			      &gpio_sc16is75x_data_##inst, &gpio_sc16is75x_config_##inst,          \
			      POST_KERNEL, CONFIG_GPIO_SC16IS75X_INIT_PRIORITY,                    \
			      &gpio_sc16is75x_api);

DT_INST_FOREACH_STATUS_OKAY(GPIO_SC16IS75X_DEFINE);

/** @} */
