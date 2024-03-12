/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT nxp_sc18is604

#include <bridle/drivers/mfd/sc18is604.h>

#include <zephyr/kernel.h>
#include <string.h>
#include <zephyr/device.h>
#include <zephyr/drivers/spi.h>
#include <zephyr/drivers/gpio.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(sc18is604, CONFIG_MFD_LOG_LEVEL);

#define SC18IS604_SPI_BYTE_DELAY_MICROS 8

struct sc18is604_config {
    const struct spi_dt_spec spi;
    const struct gpio_dt_spec reset;
    const struct gpio_dt_spec interrupt;
};

struct sc18is604_data {
    const struct device *dev;
    atomic_t is_ready;
    struct k_mutex lock;
    struct k_sem interrupt_raised;
    struct gpio_callback interrupt_callback;
    struct k_work interrupt_work; 
};

bool sc18is604_is_ready(const struct device *dev) {
    const struct sc18is604_data *const data = dev->data;
    return atomic_get(&data->is_ready);
}

struct k_sem *sc18is604_interrupt_sem_get(const struct device *dev)
{
    struct sc18is604_data *data = dev->data;
    return &data->interrupt_raised;
}

int sc18is604_claim(const struct device *dev)
{
    struct sc18is604_data *data = dev->data;
    return k_mutex_lock(&data->lock, K_FOREVER);
}

int sc18is604_release(const struct device *dev)
{
    struct sc18is604_data *data = dev->data;
    return k_mutex_unlock(&data->lock);
}

int sc18is604_transfer(const struct device *dev, uint8_t *cmd, size_t cmd_len, uint8_t *tx_data, size_t tx_len, uint8_t *rx_data, size_t rx_len)
{
    /* The SC18IS604 requires significant delay between each byte sent via SPI.
       We achieve this by sending bytes in individual transactions, but keeping
       the CS line set, and the device locked, until we explicitly release it
       (see the flags SPI_HOLD_ON_CS and SPI_LOCK_ON set in device init). */

    const struct sc18is604_config *const config = dev->config;
    struct sc18is604_data *data = dev->data;
    int ret = 0;
    
    /* Lock device. Putting this gate here ensures a calling thread can't
       "forget" to check for existing locks, but still allows a thread to pass
       through if it holds an "outer" lock. This way a caller can guarantee that
       a complex transaction is not interrupted. */
    k_mutex_lock(&data->lock, K_FOREVER);

    struct spi_buf buffer = {
        .buf = NULL,
        .len = 1,
    };

    /* Write command sequence */
    if (cmd != NULL) {
        for (int i = 0; i < cmd_len; i++) {
            buffer.buf = &cmd[i];
            const struct spi_buf_set buf_set = { .buffers = &buffer, .count = 1 };
            ret = spi_write_dt(&config->spi, &buf_set);
            if (ret != 0) {
                goto end;
            }
            k_busy_wait(SC18IS604_SPI_BYTE_DELAY_MICROS);
        }
    }

    /* Write data */
    if (tx_data != NULL) {
        for (int i = 0; i < tx_len; i++) {
            buffer.buf = &tx_data[i];
            const struct spi_buf_set buf_set = { .buffers = &buffer, .count = 1 };
            ret = spi_write_dt(&config->spi, &buf_set);
            if (ret != 0) {
                goto end;
            }
            k_busy_wait(SC18IS604_SPI_BYTE_DELAY_MICROS);
        }
    }

    /* Read data */
    if (rx_data != NULL) {
        for (int i = 0; i < rx_len; i++) {
            buffer.buf = &rx_data[i];
            const struct spi_buf_set buf_set = { .buffers = &buffer, .count = 1 };
            ret = spi_read_dt(&config->spi, &buf_set);
            if (ret != 0) {
                goto end;
            }
            k_busy_wait(SC18IS604_SPI_BYTE_DELAY_MICROS);
        }
    }

    end:
    spi_release_dt(&config->spi); // Releases the SPI bus itself, which we locked with our first spi_write_dt call.
    k_mutex_unlock(&data->lock); // Release the lock on the bridge device. Potential "outer" locks will persist.
    return ret;
}

int sc18is604_write_internal_register(const struct device *dev, uint8_t reg, uint8_t value)
{
    uint8_t cmd[] = {SC18IS604_CMD_WRITE_INTERNAL, reg};
    return sc18is604_transfer(dev, cmd, ARRAY_SIZE(cmd), &value, 1, NULL, 0);
}

int sc18is604_read_internal_register(const struct device *dev, uint8_t reg, uint8_t *value)
{
    uint8_t cmd[] = {SC18IS604_CMD_READ_INTERNAL, reg};
    return sc18is604_transfer(dev, cmd, ARRAY_SIZE(cmd), NULL, 0, value, 1);
}

int sc18is604_read_buffer(const struct device *dev, uint8_t *data, size_t len)
{
    uint8_t cmd[] = {SC18IS604_CMD_READ_BUFFER};
    return sc18is604_transfer(dev, cmd, ARRAY_SIZE(cmd), NULL, 0, data, len);
}

int sc18is604_request_version_string(const struct device *dev)
{
    uint8_t cmd[] = {SC18IS604_CMD_VERSION_STRING};
    return sc18is604_transfer(dev, cmd, ARRAY_SIZE(cmd), NULL, 0, NULL, 0);
}

static int sc18is604_reset_interrupt(const struct device *dev)
{
    uint8_t buf = 0;
    /* Reset interrupt by reading from I2CStat register */
    return sc18is604_read_internal_register(dev, SC18IS604_REG_I2C_STATUS, &buf);
}

static void sc18is604_interrupt_work_fn(struct k_work *work)
{
    struct sc18is604_data *data = CONTAINER_OF(work, struct sc18is604_data, interrupt_work);
    const struct device *dev = data->dev;
    sc18is604_reset_interrupt(dev); // Reset hardware signal
    k_sem_give(&data->interrupt_raised); // Propagate software signal
}

static void sc18is604_interrupt_callback(const struct device *dev, struct gpio_callback *cb, gpio_port_pins_t pins)
{
    struct sc18is604_data *data = CONTAINER_OF(cb, struct sc18is604_data, interrupt_callback);
    /* Resetting the interrupt involves SPI communication, so we can't do it
       from the ISR */
    k_work_submit(&data->interrupt_work);
}

static int sc18is604_init(const struct device *dev)
{
    struct sc18is604_data *data = dev->data;
    const struct sc18is604_config *const config = dev->config;
    int ret = 0;

    /* Check bridge readiness */
    if (!spi_is_ready_dt(&config->spi)) {
        LOG_ERR("SPI device not ready");
        return -ENODEV;
    }

    /* Initialize lock */
    k_mutex_init(&data->lock);

    /* Set back-pointer to device */
    data->dev = dev;

    /* Reset device */
    ret = gpio_pin_configure_dt(&config->reset, GPIO_OUTPUT_ACTIVE);
    if (ret != 0) {
        LOG_ERR("Failed to configure reset pin: %d", ret);
        return ret;
    }
    k_busy_wait(1); // Should suffice to pull for 125ns
    ret = gpio_pin_set_dt(&config->reset, 0);
    if (ret != 0) {
        LOG_ERR("Failed to release reset pin: %d", ret);
        return ret;
    }

    /* Device needs some delay before becoming responsive again after reset */ 
    k_busy_wait(500);
    
    /* Set up interrupt handling */
    k_sem_init(&data->interrupt_raised, 0, 1);
    ret = gpio_pin_configure_dt(&config->interrupt, GPIO_INPUT);
    if (ret != 0) {
        LOG_ERR("Failed to configure interrupt pin: %d", ret);
        return ret;
    }
    ret = gpio_pin_interrupt_configure_dt(&config->interrupt, GPIO_INT_EDGE_TO_ACTIVE);
    if (ret != 0) {
        LOG_ERR("Failed to enable interrupt on interrupt pin: %d", ret);
        return ret;
    }
    gpio_init_callback(&data->interrupt_callback, sc18is604_interrupt_callback, BIT(config->interrupt.pin));
    ret = gpio_add_callback_dt(&config->interrupt, &data->interrupt_callback);
    if (ret != 0) {
        LOG_INF("Failed to register interrupt callback: %d", ret);
        return 0;
    }
    k_work_init(&data->interrupt_work, sc18is604_interrupt_work_fn);

    /* Confirm version string */
    uint8_t buffer[16] = {0};
    uint8_t version[16] = "SC18IS604 1.0.3";
    sc18is604_request_version_string(dev);
    k_sem_take(&data->interrupt_raised, K_FOREVER);
    sc18is604_read_buffer(dev, buffer, ARRAY_SIZE(buffer));
    if (strncmp(version, buffer, 16) != 0) {
        LOG_ERR("Version mismatch, got %s", buffer);
        return -ENODEV;
    }
    LOG_DBG("Version: %s", buffer);

    /* Mark bridge as ready */
    atomic_set(&data->is_ready, true);

    return 0;
}

#define SC18IS604_DEFINE(inst) \
    static struct sc18is604_data sc18is604_data_##inst = { \
        .is_ready = false, \
    }; \
    static struct sc18is604_config sc18is604_config_##inst = { \
        .spi = SPI_DT_SPEC_GET(DT_DRV_INST(inst), (SPI_OP_MODE_MASTER | SPI_WORD_SET(8) | SPI_MODE_CPOL | SPI_MODE_CPHA | SPI_HOLD_ON_CS | SPI_LOCK_ON), 0), \
        .reset = GPIO_DT_SPEC_GET(DT_DRV_INST(inst), reset_gpios), \
        .interrupt = GPIO_DT_SPEC_GET(DT_DRV_INST(inst), interrupt_gpios), \
    }; \
    DEVICE_DT_INST_DEFINE(inst, \
        sc18is604_init, \
        NULL, /* PM */ \
        &sc18is604_data_##inst, \
        &sc18is604_config_##inst, \
        POST_KERNEL, \
        CONFIG_MFD_SC18IS604_INIT_PRIORITY, \
        NULL, /* Driver API */ \
    );

DT_INST_FOREACH_STATUS_OKAY(SC18IS604_DEFINE);
