/*
 * Copyright (c) 2025 TiaC Systems
 * Copyright (c) 2024 Matthew Tran
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT wch_ch32_gpio

#include <errno.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/gpio/gpio_utils.h>
#include <zephyr/drivers/clock_control.h>
#include <zephyr/irq.h>
#include <soc.h>

struct gpio_ch32_config {
    GPIO_TypeDef *base;
    const struct device *clock_dev;
    uint8_t clock_id;
};

struct gpio_ch32_data {
    sys_slist_t callbacks;
};

static int gpio_ch32_pin_configure(const struct device *dev, gpio_pin_t pin, gpio_flags_t flags) {
    const struct gpio_ch32_config *config = dev->config;
    GPIOMode_TypeDef mode = GPIO_Mode_AIN;

    if ((flags & GPIO_INPUT) && (flags & GPIO_OUTPUT)) {
        return -ENOTSUP;
    }

    if ((flags & GPIO_PULL_UP) && (flags & GPIO_PULL_DOWN)) {
        return -ENOTSUP;
    }

    if (flags & GPIO_SINGLE_ENDED) {
        return -ENOTSUP;
    }

    if (flags & GPIO_INPUT) {
        if      (flags & GPIO_PULL_UP)   { mode = GPIO_Mode_IPU;         }
        else if (flags & GPIO_PULL_DOWN) { mode = GPIO_Mode_IPD;         }
        else                             { mode = GPIO_Mode_IN_FLOATING; }
    } else if (flags & GPIO_OUTPUT) {
        mode = GPIO_Mode_Out_PP;
    }

    if (flags & GPIO_OUTPUT_INIT_LOW)  { GPIO_WriteBit(config->base, BIT(pin), RESET); }
    if (flags & GPIO_OUTPUT_INIT_HIGH) { GPIO_WriteBit(config->base, BIT(pin), SET);   }

    GPIO_InitTypeDef cfg = {
        .GPIO_Pin   = BIT(pin),
        .GPIO_Speed = GPIO_Speed_50MHz,
        .GPIO_Mode  = mode,
    };
    GPIO_Init(config->base, &cfg);

    return 0;
}

static int gpio_ch32_port_get_raw(const struct device *dev, uint32_t *value) {
    const struct gpio_ch32_config *config = dev->config;
    *value = GPIO_ReadInputData(config->base);
    return 0;
}

static int gpio_ch32_port_set_masked_raw(const struct device *dev, uint32_t mask, uint32_t value) {
    const struct gpio_ch32_config *config = dev->config;
    GPIO_SetBits(config->base,   mask & value);
    GPIO_ResetBits(config->base, mask & ~value);
    return 0;
}

static int gpio_ch32_port_set_bits_raw(const struct device *dev, uint32_t mask) {
    const struct gpio_ch32_config *config = dev->config;
    GPIO_SetBits(config->base, mask);
    return 0;
}

static int gpio_ch32_port_clear_bits_raw(const struct device *dev, uint32_t mask) {
    const struct gpio_ch32_config *config = dev->config;
    GPIO_ResetBits(config->base, mask);
    return 0;
}

static int gpio_ch32_port_toggle_bits(const struct device *dev, uint32_t mask) {
    const struct gpio_ch32_config *config = dev->config;
    uint32_t value = ~GPIO_ReadOutputData(config->base);
    GPIO_SetBits(config->base,   mask & value);
    GPIO_ResetBits(config->base, mask & ~value);
    return 0;
}

static int gpio_ch32_pin_interrupt_configure(const struct device *dev, gpio_pin_t pin,
        enum gpio_int_mode mode, enum gpio_int_trig trig) {
    ARG_UNUSED(dev);
    ARG_UNUSED(pin);
    ARG_UNUSED(mode);
    ARG_UNUSED(trig);
    return -ENOTSUP; // TODO add support
}

static int gpio_ch32_manage_callback(const struct device *dev, struct gpio_callback *cb, bool set) {
    struct gpio_ch32_data *data = dev->data;
    return gpio_manage_callback(&data->callbacks, cb, set);
}

static uint32_t gpio_ch32_get_pending_int(const struct device *dev) {
    ARG_UNUSED(dev);
    return -ENOTSUP;
}

static int gpio_ch32_init(const struct device *dev) {
    const struct gpio_ch32_config *config = dev->config;
    clock_control_on(config->clock_dev, (clock_control_subsys_t *)(uintptr_t)config->clock_id);
    return 0;
}

static const struct gpio_driver_api gpio_ch32_driver_api = {
    .pin_configure           = gpio_ch32_pin_configure,
    .port_get_raw            = gpio_ch32_port_get_raw,
    .port_set_masked_raw     = gpio_ch32_port_set_masked_raw,
    .port_set_bits_raw       = gpio_ch32_port_set_bits_raw,
    .port_clear_bits_raw     = gpio_ch32_port_clear_bits_raw,
    .port_toggle_bits        = gpio_ch32_port_toggle_bits,
    .pin_interrupt_configure = gpio_ch32_pin_interrupt_configure,
    .manage_callback         = gpio_ch32_manage_callback,
    .get_pending_int         = gpio_ch32_get_pending_int,
};

#define GPIO_CH32_INIT(n)                                           \
    static const struct gpio_ch32_config gpio_ch32_##n##_config = { \
        .base      = (GPIO_TypeDef*) DT_INST_REG_ADDR(n),           \
        .clock_dev = DEVICE_DT_GET(DT_INST_CLOCKS_CTLR(n)),         \
        .clock_id = DT_INST_CLOCKS_CELL(n, id),                     \
    };                                                              \
                                                                    \
    static struct gpio_ch32_data gpio_ch32_##n##_data;              \
                                                                    \
    DEVICE_DT_INST_DEFINE(n,                                        \
        &gpio_ch32_init,                                            \
        NULL,                                                       \
        &gpio_ch32_##n##_data,                                      \
        &gpio_ch32_##n##_config,                                    \
        PRE_KERNEL_1,                                               \
        CONFIG_GPIO_CH32_INIT_PRIORITY,                             \
        &gpio_ch32_driver_api                                       \
    );

DT_INST_FOREACH_STATUS_OKAY(GPIO_CH32_INIT)
