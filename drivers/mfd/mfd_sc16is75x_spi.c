/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/device.h>

#include <zephyr/drivers/spi.h>
#include <zephyr/drivers/mfd/sc16is75x.h>

#include "mfd_sc16is75x.h"

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(mfd_sc16is75x_spi, CONFIG_MFD_LOG_LEVEL);

static int mfd_sc16is75x_spi_read_raw(const struct device *dev,
				      const uint8_t sub_address,
				      uint8_t *buf, const size_t len)
{
	const struct mfd_sc16is75x_config * const config = dev->config;
	int ret = 0;

	const struct spi_buf tx_buffers[] = {
		{
			.buf = (void *)&sub_address,
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
			.buf = buf,
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

	ret = spi_transceive_dt(&config->spi, &tx, &rx);
	return ret;
}

static int mfd_sc16is75x_spi_write_raw(const struct device *dev,
				       const uint8_t sub_address,
				       const uint8_t *buf, const size_t len)
{
	const struct mfd_sc16is75x_config * const config = dev->config;
	int ret = 0;

	const struct spi_buf tx_buffers[] = {
		{
			.buf = (void *)&sub_address,
			.len = 1,
		},
		{
			.buf = (void *)buf,
			.len = len,
		}
	};
	const struct spi_buf_set tx = {
		.buffers = tx_buffers,
		.count = ARRAY_SIZE(tx_buffers),
	};

	ret = spi_write_dt(&config->spi, &tx);
	return ret;
}

static const struct mfd_sc16is75x_transfer_function
mfd_sc16is75x_spi_init_transfer_function = {
	.read_raw = mfd_sc16is75x_spi_read_raw,
	.write_raw = mfd_sc16is75x_spi_write_raw,
};

int mfd_sc16is75x_spi_init(const struct device *dev)
{
	const struct mfd_sc16is75x_config * const config = dev->config;
	struct mfd_sc16is75x_data * const data = dev->data;

	data->transfer_function = &mfd_sc16is75x_spi_init_transfer_function;

	/* Confirm device readiness */
	if (!spi_is_ready_dt(&config->spi)) {
		LOG_ERR("%s: SPI device %s not ready",
			dev->name, config->spi.bus->name);
		return -ENODEV;
	}

	LOG_DBG("%s: ready over %s!", dev->name, config->spi.bus->name);

	return 0;
}
