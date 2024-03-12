/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT nxp_sc18is604_gpio

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/spi.h>

#include <zephyr/drivers/gpio/gpio_utils.h>

#include <bridle/drivers/mfd/sc18is604.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(sc18is604_gpio, CONFIG_GPIO_LOG_LEVEL);

struct sc18is604_gpio_config {
    /* gpio_driver_config must be first */
    struct gpio_driver_config common;
    const struct device *bridge;
};

struct sc18is604_gpio_data {
    /* gpio_driver_data must be first */
    struct gpio_driver_data common;
    uint8_t pin_config;
    uint8_t pin_state;
};

static int sc18is604_gpio_write_config(const struct device *dev, uint8_t config)
{
    const struct sc18is604_gpio_config *const dev_config = dev->config;
    struct sc18is604_gpio_data *data = dev->data;
    int ret = sc18is604_write_internal_register(dev_config->bridge, SC18IS604_REG_IO_CONFIG, config);
    if (ret != 0) {
        return ret;
    }
    data->pin_config = config;
    return 0;
}

static int sc18is604_gpio_read_config(const struct device *dev, uint8_t *config)
{
    const struct sc18is604_gpio_config *const dev_config = dev->config;
    struct sc18is604_gpio_data *data = dev->data;
    int ret = sc18is604_read_internal_register(dev_config->bridge, SC18IS604_REG_IO_CONFIG, config);
    if (ret != 0) {
        return ret;
    }
    data->pin_config = *config;
    return 0;
}

static int sc18is604_gpio_write_state(const struct device *dev, uint8_t state)
{
    const struct sc18is604_gpio_config *const config = dev->config;
    struct sc18is604_gpio_data *data = dev->data;
    int ret = sc18is604_write_internal_register(config->bridge, SC18IS604_REG_IO_STATE, state);
    if (ret != 0) {
        return ret;
    }
    data->pin_state = state;
    return 0;
}

static int sc18is604_gpio_read_state(const struct device *dev, uint8_t *state)
{
    const struct sc18is604_gpio_config *const config = dev->config;
    struct sc18is604_gpio_data *data = dev->data;
    int ret = sc18is604_read_internal_register(config->bridge, SC18IS604_REG_IO_STATE, state);
    if (ret != 0) {
        return ret;
    }
    data->pin_state = *state;
    return 0;
}

static int sc18is604_gpio_pin_configure(const struct device *dev, gpio_pin_t pin, gpio_flags_t flags)
{
    struct sc18is604_gpio_data *data = dev->data;
    int ret = 0;

    /* Can only configure pins 0 through 3 */
    if (pin > 3) {
        return -ENOTSUP;
    }

    /* Does not support disconnected pin */
	if ((flags & (GPIO_INPUT | GPIO_OUTPUT)) == GPIO_DISCONNECTED) {
		return -ENOTSUP;
	}

    /* Can't do SPI bus operations from an ISR */
	if (k_is_in_isr()) {
		return -EWOULDBLOCK;
	}

    /* Prepare new configuration for target pin */
    uint8_t shift = 2 * pin; // Each pin has two configuration bits
    uint8_t config_bits = 0b00;
    if ((flags & GPIO_INPUT) == GPIO_INPUT) {
        config_bits = SC18IS604_IO_CONFIG_INPUT;
    } else if ((flags & GPIO_OUTPUT) == GPIO_OUTPUT) {
        if ((flags & GPIO_OPEN_DRAIN) == GPIO_OPEN_DRAIN) {
            config_bits = SC18IS604_IO_CONFIG_OPEN_DRAIN;
        } else {
            config_bits = SC18IS604_IO_CONFIG_PUSH_PULL;
        }
    }
    uint8_t config = data->pin_config;
    config &= ~(0b11 << shift); // Clear config bits
    config |= (config_bits << shift); // Set new config

    /* Apply configuration */
    ret = sc18is604_gpio_write_config(dev, config);
    if (ret != 0) {
        return ret;
    }

    /* For output pins, state might also be configured */
    uint8_t state = data->pin_state;
    if ((flags & GPIO_OUTPUT) == GPIO_OUTPUT) {
        if ((flags & GPIO_OUTPUT_INIT_HIGH) == GPIO_OUTPUT_INIT_HIGH) {
            state |= BIT(pin);
        } else if ((flags & GPIO_OUTPUT_INIT_LOW) == GPIO_OUTPUT_INIT_LOW) {
            state &= ~BIT(pin);
        }
        /* Apply pin state */
        ret = sc18is604_gpio_write_state(dev, state);
        if (ret != 0) {
            return ret;
        }
    }

    return 0;
}

static int sc18is604_gpio_port_get_raw(const struct device *dev, uint32_t *value)
{
    /* Can't do SPI operations from an ISR */
    if (k_is_in_isr()) {
        return -EWOULDBLOCK;
    }

    /* Read curent state from device */
    uint8_t buf = 0x00;
    int ret = sc18is604_gpio_read_state(dev, &buf);
    if (ret != 0) {
        return ret;
    }

    /* Return through pointer */
    *value = buf;
    return 0;
}

static int sc18is604_gpio_port_set_masked_raw(const struct device *dev, uint32_t mask, uint32_t value)
{
    /* Can't do SPI operations from an ISR */
    if (k_is_in_isr()) {
        return -EWOULDBLOCK;
    }

    /* Get (cached) state, and set bits to value according to mask */
    struct sc18is604_gpio_data *data = dev->data;
    uint8_t state = data->pin_state;
    state = (state & ~mask) | (mask & value);

    /* Apply the new pin state */
    int ret = sc18is604_gpio_write_state(dev, state);
    
    return ret;
}

static int sc18is604_gpio_port_set_bits_raw(const struct device *dev, uint32_t pins)
{
    return sc18is604_gpio_port_set_masked_raw(dev, pins, pins);
}

static int sc18is604_gpio_port_clear_bits_raw(const struct device *dev, uint32_t pins)
{
    return sc18is604_gpio_port_set_masked_raw(dev, pins, 0);
}

static int sc18is604_gpio_port_toggle_bits(const struct device *dev, uint32_t pins)
{
    /* Can't do SPI operations from an ISR */
    if (k_is_in_isr()) {
        return -EWOULDBLOCK;
    }

    /* Get (cached) state, and toggle bits according to mask */
    struct sc18is604_gpio_data *data = dev->data;
    uint8_t state = data->pin_state;
    state ^= pins;

    /* Apply new pin state */
    int ret = sc18is604_gpio_write_state(dev, state);

    return ret;
}

static int sc18is604_gpio_pin_interrupt_configure(const struct device *dev, gpio_pin_t pin, enum gpio_int_mode mode, enum gpio_int_trig trig)
{
    LOG_WRN("GPIO interrupts are not supported");
    return -ENOTSUP;
}

static int sc18is604_gpio_init(const struct device *dev)
{
    const struct sc18is604_gpio_config *config = dev->config;

    /* Check bridge readiness */
    if (!sc18is604_is_ready(config->bridge)) {
        LOG_ERR("SC18IS604 bridge device not ready");
        return -ENODEV;
    }

    /* Initialize register cache */
    uint8_t buf;
    sc18is604_gpio_read_state(dev, &buf);
    sc18is604_gpio_read_config(dev, &buf);

    return 0;
}

static const struct gpio_driver_api sc18is604_gpio_driver_api = {
    .pin_configure = sc18is604_gpio_pin_configure,
    .port_get_raw = sc18is604_gpio_port_get_raw,
    .port_set_masked_raw = sc18is604_gpio_port_set_masked_raw,
    .port_set_bits_raw = sc18is604_gpio_port_set_bits_raw,
    .port_clear_bits_raw = sc18is604_gpio_port_clear_bits_raw,
    .port_toggle_bits = sc18is604_gpio_port_toggle_bits,
    .pin_interrupt_configure = sc18is604_gpio_pin_interrupt_configure,
};

#define SC18IS604_GPIO_DEFINE(inst) \
    static struct sc18is604_gpio_data sc18is604_gpio_data_##inst = { \
    }; \
    static const struct sc18is604_gpio_config sc18is604_gpio_config_##inst = { \
        .common.port_pin_mask = GPIO_PORT_PIN_MASK_FROM_DT_INST(inst), \
        .bridge = DEVICE_DT_GET(DT_INST_BUS(inst)), \
    }; \
    DEVICE_DT_INST_DEFINE(inst, \
        sc18is604_gpio_init, \
        NULL, /* PM */ \
        &sc18is604_gpio_data_##inst, \
        &sc18is604_gpio_config_##inst, \
        POST_KERNEL, \
        CONFIG_GPIO_SC18IS604_INIT_PRIORITY, \
        &sc18is604_gpio_driver_api \
    );

DT_INST_FOREACH_STATUS_OKAY(SC18IS604_GPIO_DEFINE);
