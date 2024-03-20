/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/device.h>

#include <zephyr/drivers/i2c.h>
#include <zephyr/drivers/mfd/sc16is75x.h>

#include "mfd_sc16is75x.h"

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(mfd_sc16is75x_i2c, CONFIG_MFD_LOG_LEVEL);

static int mfd_sc16is75x_i2c_read_raw(const struct device *dev,
				      const uint8_t sub_address,
				      uint8_t *buf, const size_t len)
{
	const struct mfd_sc16is75x_config * const config = dev->config;
	int ret = 0;

	ret = i2c_write_read_dt(&config->i2c, &sub_address, 1, buf, len);
	return ret;
}

static int mfd_sc16is75x_i2c_write_raw(const struct device *dev,
				       const uint8_t sub_address,
				       const uint8_t *buf, const size_t len)
{
	const struct mfd_sc16is75x_config * const config = dev->config;
	uint8_t buffer[SC16IS75X_FIFO_CAPACITY + 1] = {0};
	int ret = 0;

	/* More than SC16IS75X_FIFO_CAPACITY is useless */
	if (len > SC16IS75X_FIFO_CAPACITY) {
		return -EINVAL;
	}

	buffer[0] = sub_address;
	memcpy(buffer + 1, buf, len);

	ret = i2c_write_dt(&config->i2c, buffer, len + 1);
	return ret;
}

static const struct mfd_sc16is75x_transfer_function
mfd_sc16is75x_i2c_init_transfer_function = {
	.read_raw = mfd_sc16is75x_i2c_read_raw,
	.write_raw = mfd_sc16is75x_i2c_write_raw,
};

int mfd_sc16is75x_i2c_init(const struct device *dev)
{
	const struct mfd_sc16is75x_config * const config = dev->config;
	struct mfd_sc16is75x_data * const data = dev->data;

	data->transfer_function = &mfd_sc16is75x_i2c_init_transfer_function;

	/* Confirm device readiness */
	if (!i2c_is_ready_dt(&config->i2c)) {
		LOG_ERR("%s: I2C device %s not ready",
			dev->name, config->i2c.bus->name);
		return -ENODEV;
	}

	LOG_DBG("%s: ready over %s!", dev->name, config->i2c.bus->name);

	return 0;
}
