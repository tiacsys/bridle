/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT nxp_sc16is75x

#include <bridle/drivers/mfd/sc16is75x.h>

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/spi.h>
#include <zephyr/drivers/i2c.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/uart.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(sc16is75x, CONFIG_MFD_LOG_LEVEL);

typedef int (*sc16is75x_transfer_function)(const struct device *dev, uint8_t sub_address, uint8_t *data, size_t len);

struct sc16is75x_transfer {
    sc16is75x_transfer_function read;
    sc16is75x_transfer_function write;
};

struct sc16is75x_config {
    union {
        struct spi_dt_spec spi;
        struct i2c_dt_spec i2c;
    } bus;
    struct gpio_dt_spec reset;
    struct gpio_dt_spec interrupt;
    struct gpio_dt_spec bus_select;
    struct gpio_dt_spec address_select_0; // DEBUG
    struct gpio_dt_spec address_select_1; // DEBUG
    struct sc16is75x_transfer transfer;
};

struct sc16is75x_data {
    atomic_t is_ready;
    struct k_mutex lock;
};

static int sc16is75x_init_common(const struct device *dev);

static inline int sc16is75x_sub_address(uint8_t channel, uint8_t reg, bool read, uint8_t *addr)
{
    /* Subaddress scheme: [ R/W, A3, A2, A1, A0, CH1, Ch0, X] 
     * R/W: 1: Read, 0: Write
     * A[3:0]: Register address
     * CH1, CH0: Select serial channel
     * X: Unused
     */

    if (channel > 3) {
        return -EINVAL;
    }

    *addr = (reg << 3) | (channel << 1);
    if (read) {
        *addr |= (1U << 7);
    }

    return 0;
}

#if DT_ANY_INST_ON_BUS_STATUS_OKAY(spi)

static int sc16is75x_read_spi(const struct device *dev, uint8_t sub_address, uint8_t *data, size_t len)
{
    const struct sc16is75x_config *const config = dev->config;
    struct sc16is75x_data *drv_data = dev->data;
    int ret = 0;

    const struct spi_buf tx_buffers[] = {
        {
            .buf = &sub_address,
            .len = 1,
        },
        {
            .buf = NULL,
            .len = len,
        }
    };
    const struct spi_buf rx_buffers[] = {
        {
            .buf = NULL,
            .len = 1,
        },
        {
            .buf = data,
            .len = len,
        }
    };
    struct spi_buf_set tx = {
        .buffers = tx_buffers,
        .count = ARRAY_SIZE(tx_buffers),
    };
    struct spi_buf_set rx = {
        .buffers = rx_buffers,
        .count = ARRAY_SIZE(rx_buffers),
    };

    /* Make sure noone else has a lock on the bus */
    k_mutex_lock(&drv_data->lock, K_FOREVER);

    ret = spi_transceive_dt(&config->bus.spi, &tx, &rx);
    
    k_mutex_unlock(&drv_data->lock);

    return ret;
}

static int sc16is75x_write_spi(const struct device *dev, uint8_t sub_address, uint8_t *data, size_t len)
{
    const struct sc16is75x_config *const config = dev->config;
    struct sc16is75x_data *drv_data = dev->data;
    int ret = 0;

    const struct spi_buf tx_buffers[] = {
        {
            .buf = &sub_address,
            .len = 1,
        },
        {
            .buf = data,
            .len = len,
        }
    };
    const struct spi_buf_set tx = {
        .buffers = tx_buffers,
        .count = ARRAY_SIZE(tx_buffers),
    };
    
    /* Make sure noone else has a lock on the bus */
    k_mutex_lock(&drv_data->lock, K_FOREVER);

    ret = spi_write_dt(&config->bus.spi, &tx);

    k_mutex_unlock(&drv_data->lock);

    return ret;
}

static int sc16is75x_init_spi(const struct device *dev)
{
    const struct sc16is75x_config *const config = dev->config;
    struct sc16is75x_data *data = dev->data;
    int ret = 0;

    /* Confirm device readiness */
    if (!spi_is_ready_dt(&config->bus.spi)) {
        LOG_ERR("SPI device not ready");
        return -ENODEV;
    }

    /* Do non-SPI related initialization */
    ret = sc16is75x_init_common(dev);
    if (ret != 0) {
        return ret;
    }

    /* Set bus select to SPI (low) */
    ret = gpio_pin_set_dt(&config->bus_select, 0);
    if (ret != 0) {
        LOG_ERR("Failed to set bus_select pin: %d", ret);
        return ret;
    }

    /* Mark device as ready */
    atomic_set(&data->is_ready, true);

    return 0;
}

#endif // DT_ANY_INST_ON_BUS_STATUS_OKAY(spi)

#if DT_ANY_INST_ON_BUS_STATUS_OKAY(i2c)

static int sc16is75x_read_i2c(const struct device *dev, uint8_t sub_address, uint8_t *data, size_t len)
{
    const struct sc16is75x_config *const config = dev->config;
    struct sc16is75x_data *drv_data = dev->data;
    int ret = 0;

    /* Make sure noone else has a lock on the bus */
    k_mutex_lock(&drv_data->lock, K_FOREVER);
    
    ret = i2c_write_read_dt(&config->bus.i2c, &sub_address, 1, data, len);

    k_mutex_unlock(&drv_data->lock);

    return ret;
}

static int sc16is75x_write_i2c(const struct device *dev, uint8_t sub_address, uint8_t *data, size_t len)
{
    const struct sc16is75x_config *const config = dev->config;
    struct sc16is75x_data *drv_data = dev->data;
    int ret = 0;

    if (len > 64) {
        return -EINVAL;
    }

    uint8_t buffer[65] = {0};
    buffer[0] = sub_address;
    memcpy(buffer + 1, data, len);

    /* Make sure noone else has a lock on the bus */
    k_mutex_lock(&drv_data->lock, K_FOREVER);

    ret = i2c_write_dt(&config->bus.i2c, buffer, len + 1);

    k_mutex_unlock(&drv_data->lock);

    return ret;
}

static int sc16is75x_init_i2c(const struct device *dev)
{
    const struct sc16is75x_config *const config = dev->config;
    struct sc16is75x_data *data = dev->data;
    int ret = 0;

    /* Confirm device readiness */
    if (!i2c_is_ready_dt(&config->bus.i2c)) {
        LOG_ERR("I2C device not ready");
        return -ENODEV;
    }

    /* Do non-I2C related initialization */
    ret = sc16is75x_init_common(dev);
    if (ret != 0) {
        return ret;
    }

    /* Set bus select to I2C (high) */
    ret = gpio_pin_set_dt(&config->bus_select, 1);
    if (ret != 0) {
        LOG_ERR("Failed to set bus_select pin: %d", ret);
        return ret;
    }

    /* DEBUG */
    gpio_pin_configure_dt(&config->address_select_0, GPIO_OUTPUT_HIGH);
    gpio_pin_configure_dt(&config->address_select_1, GPIO_OUTPUT_HIGH);

    /* Mark device as ready */
    atomic_set(&data->is_ready, true);

    return 0;
}

#endif // DT_ANY_INST_ON_BUS_STATUS_OKAY(i2c)

bool sc16is75x_is_ready(const struct device *dev)
{
    struct sc16is75x_data *data = dev->data;
    return atomic_get(&data->is_ready);
}

static int sc16is75x_write(const struct device *dev, uint8_t channel, uint8_t reg, uint8_t *data, size_t len)
{
    const struct sc16is75x_config *const config = dev->config;
    int ret = 0;

    uint8_t sub_address = 0;
    ret = sc16is75x_sub_address(channel, reg, false, &sub_address);
    if (ret != 0) {
        return ret;
    }

    return config->transfer.write(dev, sub_address, data, len);
}

static int sc16is75x_read(const struct device *dev, uint8_t channel, uint8_t reg, uint8_t *data, size_t len)
{
    const struct sc16is75x_config *const config = dev->config;
    int ret = 0;

    uint8_t sub_address = 0;
    ret = sc16is75x_sub_address(channel, reg, true, &sub_address);
    if (ret != 0) {
        return ret;
    }

    return config->transfer.read(dev, sub_address, data, len);
}

int sc16is75x_read_register(const struct device *dev, uint8_t channel, uint8_t reg, uint8_t *value)
{
    return sc16is75x_read(dev, channel, reg, value, 1);
}

int sc16is75x_write_register(const struct device *dev, uint8_t channel, uint8_t reg, uint8_t value)
{
    return sc16is75x_write(dev, channel, reg, &value, 1);
}

int sc16is75x_read_fifo(const struct device *dev, uint8_t channel, uint8_t *data, size_t len)
{
    return sc16is75x_read(dev, channel, SC16IS75X_REG_RHR, data, len);
}

int sc16is75x_write_fifo(const struct device *dev, uint8_t channel, uint8_t *data, size_t len)
{
    return sc16is75x_write(dev, channel, SC16IS75X_REG_THR, data, len);
}

int sc16is75x_read_interrupt_type(const struct device *dev, uint8_t channel, uint8_t *type)
{
    return sc16is75x_read_register(dev, channel, SC16IS75X_REG_IIR, type);
}

static int sc16is75x_init_common(const struct device *dev)
{
    const struct sc16is75x_config *const config = dev->config;
    struct sc16is75x_data *data = dev->data;
    int ret = 0;

    /* Initialize lock */
    k_mutex_init(&data->lock);

    /* Configure pins */
    ret = gpio_pin_configure_dt(&config->reset, GPIO_OUTPUT);
    if (ret != 0) {
        LOG_ERR("Failed to configure reset pin: %d", ret);
        return ret;
    }
    ret = gpio_pin_configure_dt(&config->interrupt, GPIO_INPUT);
    if (ret != 0) {
        LOG_ERR("Failed to configure interrupt pin: %d", ret);
        return ret;
    }
    ret = gpio_pin_configure_dt(&config->bus_select, GPIO_OUTPUT);
    if (ret != 0) {
        LOG_ERR("Failed to configure bus_select pin: %d", ret);
        return ret;
    }

    /* Pull reset for a few µs, then wait another few µs for device startup */
    gpio_pin_set_dt(&config->reset, 1);
    k_busy_wait(5);
    gpio_pin_set_dt(&config->reset, 0);
    k_busy_wait(5);

    /* Enable interrupts */
    ret = gpio_pin_interrupt_configure_dt(&config->interrupt, GPIO_INT_EDGE_TO_ACTIVE);
    if (ret != 0) {
        LOG_ERR("Failed to enable interrupt on interrupt pin: %d", ret);
        return ret;
    }

    return 0;
}

#define SC16IS75X_CONFIG_SPI(inst) \
    { \
        .bus.spi = SPI_DT_SPEC_INST_GET(inst, (SPI_OP_MODE_MASTER | SPI_WORD_SET(8)), 0), \
        .transfer.read = sc16is75x_read_spi, \
        .transfer.write = sc16is75x_write_spi, \
        .reset = GPIO_DT_SPEC_GET(DT_DRV_INST(inst), reset_gpios), \
        .interrupt = GPIO_DT_SPEC_GET(DT_DRV_INST(inst), interrupt_gpios), \
        .bus_select = GPIO_DT_SPEC_GET(DT_DRV_INST(inst), bus_select_gpios), \
    };

#define SC16IS75X_CONFIG_I2C(inst) \
    { \
        .bus.i2c = I2C_DT_SPEC_INST_GET(inst), \
        .transfer.read = sc16is75x_read_i2c, \
        .transfer.write = sc16is75x_write_i2c, \
        .reset = GPIO_DT_SPEC_GET(DT_DRV_INST(inst), reset_gpios), \
        .interrupt = GPIO_DT_SPEC_GET(DT_DRV_INST(inst), interrupt_gpios), \
        .bus_select = GPIO_DT_SPEC_GET(DT_DRV_INST(inst), bus_select_gpios), \
        .address_select_0 = GPIO_DT_SPEC_GET_OR(DT_DRV_INST(inst), address_select_0_gpios, NULL), /*DEBUG*/ \
        .address_select_1 = GPIO_DT_SPEC_GET_OR(DT_DRV_INST(inst), address_select_1_gpios, NULL), /*DEBUG*/ \
    };

#define SC16IS75X_DEFINE(inst) \
    static struct sc16is75x_data sc16is75x_data_##inst = { \
        .is_ready = false, \
    }; \
    static struct sc16is75x_config sc16is75x_config_##inst = \
        COND_CODE_1(DT_INST_ON_BUS(inst, spi), \
            (SC16IS75X_CONFIG_SPI(inst)), \
            (SC16IS75X_CONFIG_I2C(inst))) \
    DEVICE_DT_INST_DEFINE(inst, \
        COND_CODE_1(DT_INST_ON_BUS(inst, spi), \
            (sc16is75x_init_spi), \
            (sc16is75x_init_i2c)), \
        NULL, /* PM */ \
        &sc16is75x_data_##inst, \
        &sc16is75x_config_##inst, \
        POST_KERNEL, \
        CONFIG_MFD_SC16IS75X_INIT_PRIORITY, \
        NULL /* driver API */ \
    );

DT_INST_FOREACH_STATUS_OKAY(SC16IS75X_DEFINE);
