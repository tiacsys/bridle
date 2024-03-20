/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT nxp_sc16is75x_gpio

#include <bridle/drivers/mfd/sc16is75x.h>

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/gpio.h>

#include <zephyr/drivers/gpio/gpio_utils.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(sc16is75x_gpio, CONFIG_GPIO_LOG_LEVEL);

struct sc16is75x_gpio_data {
    /* gpio_driver_data must be first */
    struct gpio_driver_data common;
    uint8_t pin_dir;
    uint8_t pin_state;
    struct {
        uint8_t enabled;
        uint8_t edge_rising;
        uint8_t edge_falling;
        uint8_t level_high;
        uint8_t level_low;
    } interrupts;
    struct gpio_callback interrupt_cb;
    struct k_work interrupt_work;
    sys_slist_t callbacks;
    const struct device *self;
};

struct sc16is75x_gpio_config {
    /* gpio_driver_config must be first */
    struct gpio_driver_config common;
    const struct device *bus;
    struct gpio_dt_spec interrupt;
};

static int sc16is75x_gpio_write_pin_dir(const struct device *dev, uint8_t dir)
{
    const struct sc16is75x_gpio_config *const config = dev->config;
    struct sc16is75x_gpio_data *data = dev->data;
    
    int ret = sc16is75x_write_register(config->bus, 0, SC16IS75X_REG_IODIR, dir);
    if (ret != 0) {
        return ret;
    }
    
    data->pin_dir = dir;

    return 0;
}

static int sc16is75x_gpio_read_pin_dir(const struct device *dev, uint8_t *dir)
{
    const struct sc16is75x_gpio_config *const config = dev->config;
    struct sc16is75x_gpio_data *data = dev->data;
    
    int ret = sc16is75x_read_register(config->bus, 0, SC16IS75X_REG_IODIR, dir);
    if (ret != 0) {
        return ret;
    }

    data->pin_dir = *dir;

    return 0;
}

static int sc16is75x_gpio_write_pin_state(const struct device *dev, uint8_t state)
{
    const struct sc16is75x_gpio_config *const config = dev->config;
    struct sc16is75x_gpio_data *data = dev->data;

    int ret = sc16is75x_write_register(config->bus, 0, SC16IS75X_REG_IOSTATE, state);
    if (ret != 0) {
        return ret;
    }

    data->pin_state = state;

    return 0;
}

static int sc16is75x_gpio_read_pin_state(const struct device *dev, uint8_t *state)
{
    const struct sc16is75x_gpio_config *const config = dev->config;
    struct sc16is75x_gpio_data *data = dev->data;

    int ret = sc16is75x_read_register(config->bus, 0, SC16IS75X_REG_IOSTATE, state);
    if (ret != 0) {
        return ret;
    }

    data->pin_state = *state;

    return 0;
}

static int sc16is75x_gpio_write_interrupt_mask(const struct device *dev, uint8_t mask)
{
    const struct sc16is75x_gpio_config *const config = dev->config;
    struct sc16is75x_gpio_data *data = dev->data;

    int ret = sc16is75x_write_register(config->bus, 0, SC16IS75X_REG_IOINTENA, mask);
    if (ret != 0) {
        return ret;
    }

    data->interrupts.enabled = mask;

    return 0;
}

static void sc16is75x_gpio_handle_interrupt_work_fn(struct k_work *work)
{
    struct sc16is75x_gpio_data *data = CONTAINER_OF(work, struct sc16is75x_gpio_data, interrupt_work);
    const struct device *dev = data->self;
    const struct sc16is75x_gpio_config *const config = dev->config;
    int ret = 0;

    /* Check if this is actually a GPIO interrupt */
    uint8_t type = 0;
    ret = sc16is75x_read_interrupt_type(config->bus, 0, &type);
    if (ret != 0 || type != SC16IS75X_INT_IO) {
        return;
    }

    /* Read out input values and compare with previously cached values. Note
       that reading the inputs clears the interrupt. */
    uint8_t old_state = data->pin_state;
    uint8_t new_state = 0;
    ret = sc16is75x_gpio_read_pin_state(dev, &new_state);
    if (ret != 0) {
        return;
    }

    uint32_t changed_pins = (old_state ^ new_state);
    uint32_t triggered_edge = (changed_pins & new_state & data->interrupts.edge_rising)
        | (changed_pins & ~new_state & data->interrupts.edge_falling);
    uint32_t triggered_level = (changed_pins & new_state & data->interrupts.level_high)
        | (changed_pins & ~new_state & data->interrupts.level_low);

    uint32_t triggered_pins = (triggered_edge | triggered_level);

    if (triggered_pins) {
        gpio_fire_callbacks(&data->callbacks, data->self, triggered_pins);
    }

    /* Emulate level triggering */
    if (triggered_level) {
        k_work_submit(&data->interrupt_work); // Reschedule self
    }
}

static void sc16is75x_gpio_interrupt_callback(const struct device *dev, struct gpio_callback *cb, gpio_port_pins_t pins)
{
    /* Handling interrupts requires bus operations, which we can't do from an
       ISR. Schedule a work item to do it instead. */
    struct sc16is75x_gpio_data *data = CONTAINER_OF(cb, struct sc16is75x_gpio_data, interrupt_cb);
    k_work_submit(&data->interrupt_work);
}

static int sc16is75x_gpio_pin_configure(const struct device *dev, gpio_pin_t pin, gpio_flags_t flags)
{
    struct sc16is75x_gpio_data *data = dev->data;
    int ret = 0;

    /* Does not support disconnected pin */
	if ((flags & (GPIO_INPUT | GPIO_OUTPUT)) == GPIO_DISCONNECTED) {
		return -ENOTSUP;
	}

    /* Can't do bus operations from an ISR */
	if (k_is_in_isr()) {
		return -EWOULDBLOCK;
	}

    /* Set new pin config */
    uint8_t dir = data->pin_dir;
    dir &= ~(BIT(pin)); // clear config for this pin
    if ((flags & GPIO_INPUT) == GPIO_INPUT) {
        ; // leave bit as 0
    } else if ((flags & GPIO_OUTPUT) == GPIO_OUTPUT) {
        dir |= BIT(pin); // set bit to 1
    }
    ret = sc16is75x_gpio_write_pin_dir(dev, dir);
    if (ret != 0) {
        return ret;
    }

    /* Possibly set initial state for output pins */
    if ((flags & GPIO_OUTPUT) == GPIO_OUTPUT) {
        
        uint8_t state = data->pin_state;
        if ((flags & GPIO_OUTPUT_INIT_HIGH) == GPIO_OUTPUT_INIT_HIGH) {
            state |= BIT(pin);
        } else if ((flags & GPIO_OUTPUT_INIT_LOW) == GPIO_OUTPUT_INIT_LOW) {
            state &= ~BIT(pin);
        }

        ret = sc16is75x_gpio_write_pin_state(dev, state);
        if (ret != 0) {
            return ret;
        }
    }

    return 0;
}

static int sc16is75x_gpio_port_get_raw(const struct device *dev, uint32_t *value)
{
    /* Can't do bus operations from an ISR */
    if (k_is_in_isr()) {
        return -EWOULDBLOCK;
    }

    /* Read current state from device */
    uint8_t state = 0;
    int ret = sc16is75x_gpio_read_pin_state(dev, &state);
    if (ret != 0) {
        return ret;
    }

    /* Return state through pointer */
    *value = state;
    return 0;
}

static int sc16is75x_gpio_port_set_masked_raw(const struct device *dev, uint32_t mask, uint32_t value)
{
    /* Can't do bus operations from an ISR */
    if (k_is_in_isr()) {
        return -EWOULDBLOCK;
    }

    /* Get (cached) state, and set bits according to mask */
    struct sc16is75x_gpio_data *data = dev->data;
    uint8_t state = data->pin_state;
    state = (state & ~mask) | (mask & value);

    /* Apply the new pin state */
    int ret = sc16is75x_gpio_write_pin_state(dev, state);

    return ret;
}

static int sc16is75x_gpio_port_set_bits_raw(const struct device *dev, uint32_t pins)
{
    return sc16is75x_gpio_port_set_masked_raw(dev, pins, pins);
}

static int sc16is75x_gpio_port_clear_bits_raw(const struct device *dev, uint32_t pins)
{
    return sc16is75x_gpio_port_set_masked_raw(dev, pins, 0);
}

static int sc16is75x_gpio_port_toggle_bits(const struct device *dev, uint32_t pins)
{
    /* Can't do bus operations from an ISR */
    if (k_is_in_isr()) {
        return -EWOULDBLOCK;
    }

    /* Get (cached) state, and toggle bits according to mask */
    struct sc16is75x_gpio_data *data = dev->data;
    uint8_t state = data->pin_state;
    state ^= pins;

    /* Apply new pin state */
    int ret = sc16is75x_gpio_write_pin_state(dev, state);

    return ret;
}

static int sc16is75x_gpio_pin_interrupt_configure(const struct device *dev, gpio_pin_t pin, enum gpio_int_mode mode, enum gpio_int_trig trig)
{
    const struct sc16is75x_gpio_config *const config = dev->config;
    struct sc16is75x_gpio_data *data = dev->data;
    int ret = 0;

    /* Check for invalid pin number */
    if (BIT(pin) > config->common.port_pin_mask) {
        return -EINVAL;
    }

    /* Confirm that specific pin is configured as input */
    if (data->pin_dir & BIT(pin)) { // 1-bit means output
        return -ENOTSUP;
    }

    /* Update interrupt masks */
    bool enabled = !(mode & GPIO_INT_MODE_DISABLED);
    bool edge = (mode == GPIO_INT_MODE_EDGE);
    bool level = (mode == GPIO_INT_MODE_LEVEL);
    bool high = ((trig & GPIO_INT_TRIG_HIGH) == GPIO_INT_TRIG_HIGH);
    bool low = ((trig & GPIO_INT_TRIG_LOW) == GPIO_INT_TRIG_LOW);

    WRITE_BIT(data->interrupts.enabled, pin, enabled);
    WRITE_BIT(data->interrupts.edge_rising, pin,
        enabled && edge && high
    );
    WRITE_BIT(data->interrupts.edge_falling, pin,
        enabled && edge && low
    );
    WRITE_BIT(data->interrupts.level_high, pin,
        enabled && level && high
    );
    WRITE_BIT(data->interrupts.level_low, pin,
        enabled && level && low
    );

    ret = sc16is75x_gpio_write_interrupt_mask(dev, data->interrupts.enabled);
    if (ret != 0) {
        return ret;
    }

    return 0;
}

static int sc16is75x_gpio_manage_callback(const struct device *dev, struct gpio_callback *callback, bool set)
{
    struct sc16is75x_gpio_data *data = dev->data;
    return gpio_manage_callback(&data->callbacks, callback, set);
}

static const struct gpio_driver_api sc16is75x_gpio_driver_api = {
    .pin_configure = sc16is75x_gpio_pin_configure,
    .port_get_raw = sc16is75x_gpio_port_get_raw,
    .port_set_masked_raw = sc16is75x_gpio_port_set_masked_raw,
    .port_set_bits_raw = sc16is75x_gpio_port_set_bits_raw,
    .port_clear_bits_raw = sc16is75x_gpio_port_clear_bits_raw,
    .port_toggle_bits = sc16is75x_gpio_port_toggle_bits,
    .pin_interrupt_configure = sc16is75x_gpio_pin_interrupt_configure,
    .manage_callback = sc16is75x_gpio_manage_callback,
};


static int sc16is75x_gpio_init(const struct device *dev)
{
    const struct sc16is75x_gpio_config *const config = dev->config;
    struct sc16is75x_gpio_data *data = dev->data;
    int ret = 0;

    /* Confirm bridge readiness */
    if (!sc16is75x_is_ready(config->bus)) {
        LOG_ERR("SC16IS75X bridge device not ready");
        return -ENODEV;
    }

    /* Initialize register caches */
    uint8_t buf;
    ret = sc16is75x_gpio_read_pin_dir(dev, &buf);
    if (ret != 0) {
        LOG_ERR("Failed to read pin directions: %d", ret);
        return ret;
    }
    ret = sc16is75x_gpio_read_pin_state(dev, &buf);
    if (ret != 0) {
        LOG_ERR("Failed to read pin state: %d", ret);
        return ret;
    }

    /* Set up interrupt handling */
    gpio_init_callback(&data->interrupt_cb, sc16is75x_gpio_interrupt_callback, BIT(config->interrupt.pin));
    k_work_init(&data->interrupt_work, sc16is75x_gpio_handle_interrupt_work_fn);
    ret = gpio_add_callback_dt(&config->interrupt, &data->interrupt_cb);
    if (ret != 0) {
        LOG_ERR("Failed to register interrupt callback: %d", ret);
        return ret;
    }

    /* Create back-reference for interrupt handling */
    data->self = dev;

    return 0;
}

#define SC16IS75X_GPIO_DEFINE(inst) \
    static struct sc16is75x_gpio_data sc16is75x_gpio_data_##inst; \
    static struct sc16is75x_gpio_config sc16is75x_gpio_config_##inst = { \
        .common.port_pin_mask = GPIO_PORT_PIN_MASK_FROM_DT_INST(inst), \
        .bus = DEVICE_DT_GET(DT_INST_BUS(inst)), \
        .interrupt = GPIO_DT_SPEC_GET(DT_INST_BUS(inst), interrupt_gpios), \
    }; \
    DEVICE_DT_INST_DEFINE(inst, \
        sc16is75x_gpio_init, \
        NULL, /* PM */ \
        &sc16is75x_gpio_data_##inst, \
        &sc16is75x_gpio_config_##inst, \
        POST_KERNEL, \
        CONFIG_GPIO_SC16IS75X_INIT_PRIORITY, \
        &sc16is75x_gpio_driver_api \
    );

DT_INST_FOREACH_STATUS_OKAY(SC16IS75X_GPIO_DEFINE);
