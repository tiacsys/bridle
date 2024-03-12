/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT nxp_sc18is604_i2c

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/i2c.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/spi.h>

#include <bridle/drivers/mfd/sc18is604.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(sc18is604_i2c, CONFIG_I2C_LOG_LEVEL);

struct sc18is604_i2c_config {
    const struct device *bridge;
};

struct sc18is604_i2c_data {
    uint32_t i2c_config;
    struct k_sem *interrupt_raised;
};

static int sc18is604_i2c_set_clock_speed(const struct device *dev, uint32_t speed)
{
    uint8_t value = SC18IS604_I2C_CLOCK_99KHZ;
    switch (speed) {
        case I2C_SPEED_STANDARD:
            value = SC18IS604_I2C_CLOCK_99KHZ;
            break;
        case I2C_SPEED_FAST:
            value = SC18IS604_I2C_CLOCK_375KHZ;
            break;
        default:
            return -EINVAL;
    }

    return sc18is604_write_internal_register(dev, SC18IS604_REG_I2C_CLOCK, value);
}

static int sc18is604_i2c_write_message(const struct device *dev, uint8_t *data, size_t len, uint16_t addr)
{
    int ret = 0;
    const struct sc18is604_i2c_config *const config = dev->config;
    struct sc18is604_i2c_data *drv_data = dev->data;
    uint8_t cmd[] = {SC18IS604_CMD_WRITE_I2C, len, (uint8_t) addr};
    
    /* Send 'i2c write' command with data attached */
    ret = sc18is604_transfer(config->bridge, cmd, ARRAY_SIZE(cmd), data, len, NULL, 0);
    if (ret != 0) {
        return ret;
    }

    /* Wait for i2c transation to complete */
    k_sem_take(drv_data->interrupt_raised, K_FOREVER);

    /* Confirm if i2c transaction was successful */
    uint8_t status = 0;
    sc18is604_read_internal_register(config->bridge, SC18IS604_REG_I2C_STATUS, &status);
    if (status != SC18IS604_I2C_STATUS_SUCCESS) {
        return -EIO;
    }

    return 0;
}

static int sc18is604_i2c_read_message(const struct device *dev, uint8_t *data, size_t len, uint16_t addr)
{
    int ret = 0;
    const struct sc18is604_i2c_config *const config = dev->config;
    struct sc18is604_i2c_data *drv_data = dev->data;
    uint8_t cmd[] = {SC18IS604_CMD_READ_I2C, len, (uint8_t) addr};
    
    /* Send 'i2c read' command */
    ret = sc18is604_transfer(config->bridge, cmd, ARRAY_SIZE(cmd), NULL, 0, NULL, 0);
    if (ret != 0) {
        return ret;
    }

    /* Wait for i2c transaction to complete */
    k_sem_take(drv_data->interrupt_raised, K_FOREVER);

    /* Confirm if i2c transaction was successful */
    uint8_t status = 0;
    sc18is604_read_internal_register(config->bridge, SC18IS604_REG_I2C_STATUS, &status);
    if (status != SC18IS604_I2C_STATUS_SUCCESS) {
        return -EIO;
    }

    /* Read out the received data */
    return sc18is604_read_buffer(config->bridge, data, len);
}

static int sc18is604_i2c_configure(const struct device *dev, uint32_t config)
{
    struct sc18is604_i2c_data *data = dev->data;

    /* Device can only act as controller */
    if ((config & I2C_MODE_CONTROLLER) != I2C_MODE_CONTROLLER) {
        return -EINVAL;
    }

    /* Controller doesn't support 10bit addressing */
    if ((config & I2C_ADDR_10_BITS) == I2C_ADDR_10_BITS) {
        return -EINVAL;
    }

    /* Adjust bus speed if necessary */
    uint32_t speed = I2C_SPEED_GET(config);
    if (speed != I2C_SPEED_GET(data->i2c_config)) {

        /* Controller only support 'standard' (100kHz) and 'fast' (400kHz) speeds */
        if ((speed == I2C_SPEED_STANDARD) || (speed == I2C_SPEED_FAST)) {
            
            int ret = sc18is604_i2c_set_clock_speed(dev, speed);
            if (ret != 0) {
                return ret;
            }

        } else {
            return -EINVAL;
        }
    }

    /* Store new config */
    data->i2c_config = config;

    return 0;
}

static int sc18is604_i2c_get_config(const struct device *dev, uint32_t *config)
{
    const struct sc18is604_i2c_data *data = dev->data;
    *config = data->i2c_config;
    return 0;
}

static int sc18is604_i2c_transfer_msg(const struct device *dev, struct i2c_msg *msg, uint16_t addr)
{
    /* Device doesn't support 10bit addressing */
    if ((msg->flags & I2C_MSG_ADDR_10_BITS) == I2C_MSG_ADDR_10_BITS) {
        return -EINVAL;
    }

    /* Add RW bit to address */
    addr <<= 1;
    addr |= (msg->flags & I2C_MSG_RW_MASK);

    if ((msg->flags & I2C_MSG_READ) == I2C_MSG_READ) {
        return sc18is604_i2c_read_message(dev, msg->buf, msg->len, addr);
    } else {
        return sc18is604_i2c_write_message(dev, msg->buf, msg->len, addr);
    }

    /* Should be unreachable */
    return 0;
}

static int sc18is604_i2c_transfer(const struct device *dev, struct i2c_msg *msgs, uint8_t num_msgs, uint16_t addr)
{
    int ret = 0;

    if (num_msgs == 0) {
        return 0;
    }

    /* Claim device for coming transactions */
    const struct sc18is604_i2c_config *const config = dev->config;
    ret = sc18is604_claim(config->bridge);
    if (ret != 0) {
        return ret;
    }

    /* Handle messages one-by-one */
    for (int i = 0; i < num_msgs; i++) {
        ret = sc18is604_i2c_transfer_msg(dev, &msgs[i], addr);
        if (ret != 0) {
            break;
        }
    }

    /* Release device once all messages have been processed */
    sc18is604_release(config->bridge);

    return ret;
}

static int sc18is604_i2c_recover_bus(const struct device *dev)
{
    return -ENOSYS;
}

static int sc18is604_i2c_target_register(const struct device *dev, struct i2c_target_config *cfg)
{
    return -ENOSYS;
}

static int sc18is604_i2c_target_unregister(const struct device *dev, struct i2c_target_config *cfg)
{
    return -ENOSYS;
}

static const struct i2c_driver_api sc18is604_i2c_driver_api = {
    .configure = sc18is604_i2c_configure,
    .get_config = sc18is604_i2c_get_config,
    .recover_bus = sc18is604_i2c_recover_bus,
    .target_register = sc18is604_i2c_target_register,
    .target_unregister = sc18is604_i2c_target_unregister,
    .transfer = sc18is604_i2c_transfer,
};

static int sc18is604_i2c_init(const struct device *dev)
{
    const struct sc18is604_i2c_config *config = dev->config;
    struct sc18is604_i2c_data *data = dev->data;

    /* Check bridge readiness */
    if (!sc18is604_is_ready(config->bridge)) {
        LOG_ERR("SC18IS604 bridge device not ready");
        return -ENODEV;
    }

    /* Get semaphore for interrupt signaling */
    data->interrupt_raised = sc18is604_interrupt_sem_get(config->bridge);

    return 0;
}

#define SC18IS604_I2C_DEFINE(inst) \
    static struct sc18is604_i2c_data sc18is604_i2c_data_##inst = { \
    }; \
    static const struct sc18is604_i2c_config sc18is604_i2c_config_##inst = { \
        .bridge = DEVICE_DT_GET(DT_INST_BUS(inst)), \
    }; \
    DEVICE_DT_INST_DEFINE(inst, \
        sc18is604_i2c_init, \
        NULL, /* PM */ \
        &sc18is604_i2c_data_##inst, \
        &sc18is604_i2c_config_##inst, \
        POST_KERNEL, \
        CONFIG_I2C_SC18IS604_INIT_PRIORITY, \
        &sc18is604_i2c_driver_api \
    );

DT_INST_FOREACH_STATUS_OKAY(SC18IS604_I2C_DEFINE);
