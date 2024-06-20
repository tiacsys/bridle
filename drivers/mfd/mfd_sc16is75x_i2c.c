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

#if defined(CONFIG_MFD_SC16IS75X_ASYNC) && defined(CONFIG_I2C_CALLBACK)

struct mfd_sc16is75x_i2c_xfer_data {
	uint8_t sub_address;
	struct k_poll_signal *signal;
};

static void mfd_sc16is75x_i2c_xfer_complete(const struct device *dev,
					    int result, void *data)
{
	struct mfd_sc16is75x_i2c_xfer_data *xfer_data = data;

	k_poll_signal_raise(xfer_data->signal, result);
	k_free(xfer_data);
}

static int mfd_sc16is75x_i2c_read_raw_signal(const struct device *dev,
				 const uint8_t sub_address,
				 uint8_t *buf, const size_t len,
				 struct k_poll_signal *signal)
{
	const struct mfd_sc16is75x_config * const config = dev->config;
	struct mfd_sc16is75x_i2c_xfer_data *xfer_data;
	int ret = 0;

	/*
	 * We need to keep a live pointer to the value of sub_address
	 * throughout the transfer.
	 */
	xfer_data = k_calloc(1, sizeof(struct mfd_sc16is75x_i2c_xfer_data));
	if (xfer_data == NULL) {
		return -ENOMEM;
	}

	/* Fill in value of sub_address and signal reference */
	*xfer_data = (struct mfd_sc16is75x_i2c_xfer_data){
		.sub_address = sub_address,
		.signal = signal,
	};

	/* Setup transfer data buffers */
	struct i2c_msg msgs[] = {
		{
			.buf = &xfer_data->sub_address,
			.len = 1,
			.flags = I2C_MSG_WRITE,
		},
		{
			.buf = buf,
			.len = len,
			.flags = I2C_MSG_RESTART | I2C_MSG_READ | I2C_MSG_STOP,
		},
	};

	ret = i2c_transfer_cb_dt(&config->i2c, msgs, ARRAY_SIZE(msgs),
				 mfd_sc16is75x_i2c_xfer_complete,
				 (void *)xfer_data);
	if (ret != 0) {
		k_free(xfer_data);
	}

	return ret;
}

#endif /* defined(CONFIG_MFD_SC16IS75X_ASYNC) && defined(CONFIG_I2C_CALLBACK) */

static const struct mfd_sc16is75x_transfer_function
mfd_sc16is75x_i2c_init_transfer_function = {
	.read_raw = mfd_sc16is75x_i2c_read_raw,
	.write_raw = mfd_sc16is75x_i2c_write_raw,
#ifdef CONFIG_MFD_SC16IS75X_ASYNC
#ifdef CONFIG_I2C_CALLBACK
	.read_raw_signal = mfd_sc16is75x_i2c_read_raw_signal,
#else /* CONFIG_I2C_CALLBACK */
	.read_raw_signal = mfd_sc16is75x_read_raw_signal,
#endif /* CONFIG_I2C_CALLBACK */
#endif /* CONFIG_MFD_SC16IS75X_ASYNC */
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
