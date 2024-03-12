/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/* FIXME: add chips timeout control as an option */

#define DT_DRV_COMPAT nxp_sc18is604_i2c

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/pm/device.h>

#include <zephyr/drivers/i2c.h>

#include <zephyr/drivers/mfd/sc18is604.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(sc18is604_i2c, CONFIG_I2C_LOG_LEVEL);

/**
 * @brief SC18IM604 I2C controller configuration data
 *
 * This structure contains all of the state for a given SC18IM604 I2C
 * controller as well as the binding to related MFD device.
 */
typedef struct i2c_sc18is604_config {
	/** Backend MFD (bridge) device for real operations on hardware */
	const struct device *bridge;
} i2c_sc18is604_config_t;

/**
 * @brief SC18IM604 I2C controller data
 *
 * This structure contains data structures used by a SC18IM604 I2C
 * controller.
 *
 * FIXME: use MFD (bridge) call back registration for interrupt handling,
 * do not synchronized using @a k_sem.
 */
typedef struct i2c_sc18is604_data {
	/** I2C bus configuration flags */
	uint32_t i2c_config;
	/** FIXME: interrupt handling by semaphore, use CB interface! */
	struct k_sem *interrupt_raised;
} i2c_sc18is604_data_t;

static inline int i2c_sc18is604_set_clock_speed(const struct device *dev,
						uint32_t speed)
{
	uint8_t value;

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

	/* FIXME: provide macro */
	return mfd_sc18is604_write_register(dev, SC18IS604_REG_I2C_CLOCK, value);
}

static int i2c_sc18is604_write_message(const struct device *dev,
				       uint8_t *data, size_t len,
				       uint16_t addr)
{
	const i2c_sc18is604_config_t * const config = dev->config;
	const i2c_sc18is604_data_t * const drv_data = dev->data;
	uint8_t status;
	int ret;

	uint8_t cmd[] = {
		SC18IS604_CMD_WRITE_I2C,
		len, (uint8_t) addr
	};

	/* Send 'I2C WRITE' command with data attached */
	ret = mfd_sc18is604_transfer(config->bridge,
				     cmd, ARRAY_SIZE(cmd),
				     data, len, NULL, 0);
	if (ret != 0) {
		return ret;
	}

	/* Wait for I2C transation to complete, FIXME: loost interrupts? */
	/* k_sem_take(drv_data->interrupt_raised, K_FOREVER); */
	k_sem_take(drv_data->interrupt_raised, K_MSEC(100));
	/* FIXME: make this better to avoid dead lock, when no device connected */

	/* Confirm if I2C transaction was successful */
	/* FIXME: provide macro */
	ret = mfd_sc18is604_read_register(config->bridge, SC18IS604_REG_I2C_STATUS, &status);
	if (ret != 0) {
		return ret;
	}

	if (status != SC18IS604_I2C_STATUS_SUCCESS) {
		return -EIO;
	}

	return 0;
}

static int i2c_sc18is604_read_message(const struct device *dev,
				      uint8_t *data, size_t len,
				      uint16_t addr)
{
	const i2c_sc18is604_config_t * const config = dev->config;
	const i2c_sc18is604_data_t * const drv_data = dev->data;
	uint8_t status;
	int ret;

	uint8_t cmd[] = {
		SC18IS604_CMD_READ_I2C,
		len, (uint8_t) addr
	};

	/* Send 'I2C READ' command */
	ret = mfd_sc18is604_transfer(config->bridge,
				     cmd, ARRAY_SIZE(cmd),
				     NULL, 0, NULL, 0);
	if (ret != 0) {
		return ret;
	}

	/* Wait for I2C transaction to complete, FIXME: loost interrupts? */
	/* k_sem_take(drv_data->interrupt_raised, K_FOREVER); */
	k_sem_take(drv_data->interrupt_raised, K_MSEC(100));
	/* FIXME: make this better to avoid dead lock, when no device connected */

	/* Confirm if I2C transaction was successful */
	/* FIXME: provide macro */
	ret = mfd_sc18is604_read_register(config->bridge, SC18IS604_REG_I2C_STATUS, &status);
	if (ret != 0) {
		return ret;
	}

	if (status != SC18IS604_I2C_STATUS_SUCCESS) {
		return -EIO;
	}

	/* Read out the received data */
	return mfd_sc18is604_read_buffer(config->bridge, data, len);
}

static int i2c_sc18is604_configure(const struct device *dev, uint32_t config)
{
	i2c_sc18is604_data_t * const data = dev->data;

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

		/*
		 * Controller only support 'standard' (100kHz)
		 * and 'fast' (400kHz) speeds.
		 */
		if ((speed == I2C_SPEED_STANDARD) ||
		    (speed == I2C_SPEED_FAST)) {

			int ret = i2c_sc18is604_set_clock_speed(dev, speed);

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

static int i2c_sc18is604_get_config(const struct device *dev, uint32_t *config)
{
	const i2c_sc18is604_data_t * const data = dev->data;
	*config = data->i2c_config;
	return 0;
}

static int i2c_sc18is604_transfer_msg(const struct device *dev,
				      struct i2c_msg *msg, uint16_t addr)
{
	/* Device doesn't support 10bit addressing */
	if ((msg->flags & I2C_MSG_ADDR_10_BITS) == I2C_MSG_ADDR_10_BITS) {
		return -EINVAL;
	}

	/* Add RW bit to address */
	addr <<= 1;
	addr |= (msg->flags & I2C_MSG_RW_MASK);

	if ((msg->flags & I2C_MSG_READ) == I2C_MSG_READ) {
		return i2c_sc18is604_read_message(dev, msg->buf,
						  msg->len, addr);
	} else {
		return i2c_sc18is604_write_message(dev, msg->buf,
						   msg->len, addr);
	}

	/* Should be unreachable */
	return -EINVAL;
}

static int i2c_sc18is604_transfer(const struct device *dev,
				  struct i2c_msg *msgs,
				  uint8_t num_msgs,
				  uint16_t addr)
{
	const i2c_sc18is604_config_t * const config = dev->config;
	int ret;

	if (num_msgs == 0) {
		return 0;
	}

	/* Claim device for coming transactions */
	ret = mfd_sc18is604_claim(config->bridge);
	if (ret != 0) {
		return ret;
	}

	/* Handle messages one-by-one */
	for (int i = 0; i < num_msgs; i++) {
		ret = i2c_sc18is604_transfer_msg(dev, &msgs[i], addr);
		if (ret != 0) {
			break;
		}
	}

	/* Release device once all messages have been processed */
	mfd_sc18is604_release(config->bridge);

	return ret;
}

static int i2c_sc18is604_recover_bus(const struct device *dev)
{
	return -ENOSYS;
}

static int i2c_sc18is604_target_register(const struct device *dev,
					 struct i2c_target_config *cfg)
{
	return -ENOSYS;
}

static int i2c_sc18is604_target_unregister(const struct device *dev,
					   struct i2c_target_config *cfg)
{
	return -ENOSYS;
}

static const struct i2c_driver_api i2c_sc18is604_api = {
	.configure = i2c_sc18is604_configure,
	.get_config = i2c_sc18is604_get_config,
	.recover_bus = i2c_sc18is604_recover_bus,
	.target_register = i2c_sc18is604_target_register,
	.target_unregister = i2c_sc18is604_target_unregister,
	.transfer = i2c_sc18is604_transfer,
};

static int i2c_sc18is604_init(const struct device *dev)
{
	const i2c_sc18is604_config_t * const config = dev->config;
	i2c_sc18is604_data_t * const data = dev->data;

	/* Check bridge readiness */
	if (!device_is_ready(config->bridge)) {
		LOG_ERR("%s: bridge device %s not ready",
			dev->name, config->bridge->name);
		return -ENODEV;
	}

	/* Get semaphore for interrupt signaling */
	data->interrupt_raised = mfd_sc18is604_interrupt_sem_get(
						config->bridge);

	LOG_DBG("%s: ready with bridge over %s!", dev->name,
		config->bridge->name);
	return 0;
}

#ifdef CONFIG_PM_DEVICE
static int i2c_sc18is604_pm_device_pm_action(const struct device *dev,
					     enum pm_device_action action)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(action);

	return 0;
}
#endif

#define I2C_SC18IS604_DEFINE(inst) \
                                                                             \
	static const i2c_sc18is604_config_t i2c_sc18is604_config_##inst =    \
	{                                                                    \
		.bridge = DEVICE_DT_GET(DT_INST_BUS(inst)),                  \
	};                                                                   \
                                                                             \
	static i2c_sc18is604_data_t i2c_sc18is604_data_##inst = { };         \
                                                                             \
	PM_DEVICE_DT_INST_DEFINE(inst, i2c_sc18is604_pm_device_pm_action);   \
                                                                             \
	DEVICE_DT_INST_DEFINE(inst, i2c_sc18is604_init,                      \
			      PM_DEVICE_DT_INST_GET(inst),                   \
			      &i2c_sc18is604_data_##inst,                    \
			      &i2c_sc18is604_config_##inst, POST_KERNEL,     \
			      CONFIG_I2C_SC18IS604_INIT_PRIORITY,            \
			      &i2c_sc18is604_api);

DT_INST_FOREACH_STATUS_OKAY(I2C_SC18IS604_DEFINE);
