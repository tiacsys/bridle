/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief MFD SPI-Bus Transfer Driver for an SC16IS75X bridge
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

	const struct spi_buf tx_buffers[] = { { .buf = (void *)&sub_address, .len = 1, },
					      { .buf = NULL, .len = len, } };
	const struct spi_buf rx_buffers[] = { { .buf = NULL, .len = 1, },
					      { .buf = buf, .len = len, } };
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

	const struct spi_buf tx_buffers[] = { { .buf = (void *)&sub_address, .len = 1, },
					      { .buf = (void *)buf, .len = len, } };
	const struct spi_buf_set tx = {
		.buffers = tx_buffers,
		.count = ARRAY_SIZE(tx_buffers),
	};

	ret = spi_write_dt(&config->spi, &tx);
	return ret;
}

#if defined(CONFIG_MFD_SC16IS75X_ASYNC) && defined(CONFIG_SPI_ASYNC)

struct mfd_sc16is75x_spi_xfer_data {
	uint8_t sub_address;
	struct k_poll_signal *signal;
};

static void mfd_sc16is75x_spi_xfer_complete(const struct device *dev,
					    int result, void *data)
{
	struct mfd_sc16is75x_spi_xfer_data *xfer_data = data;

	k_poll_signal_raise(xfer_data->signal, result);
	k_free(xfer_data);
}

static int mfd_sc16is75x_spi_read_raw_signal(const struct device *dev,
					     const uint8_t sub_address,
					     uint8_t *buf, const size_t len,
					     struct k_poll_signal *signal)
{
	const struct mfd_sc16is75x_config * const config = dev->config;
	struct mfd_sc16is75x_spi_xfer_data *xfer_data;
	int ret = 0;

	/*
	 * We need to keep a live pointer to the value of sub_address
	 * throughout the transfer.
	 */
	xfer_data = k_calloc(1, sizeof(struct mfd_sc16is75x_spi_xfer_data));
	if (xfer_data == NULL) {
		return -ENOMEM;
	}

	/* Fill in value of sub_address and signal reference */
	*xfer_data = (struct mfd_sc16is75x_spi_xfer_data){
		.sub_address = sub_address,
		.signal = signal,
	};

	/* Setup transfer data buffers */
	const struct spi_buf tx_buffers[] = { { .buf = &xfer_data->sub_address, .len = 1, },
					      { .buf = NULL, .len = len, } };
	const struct spi_buf rx_buffers[] = { { .buf = NULL, .len = 1, },
					      { .buf = buf, .len = len, } };
	const struct spi_buf_set tx = {
		.buffers = tx_buffers,
		.count = ARRAY_SIZE(tx_buffers),
	};
	const struct spi_buf_set rx = {
		.buffers = rx_buffers,
		.count = ARRAY_SIZE(rx_buffers),
	};

	ret = spi_transceive_cb(config->spi.bus, &config->spi.config, &tx, &rx,
				mfd_sc16is75x_spi_xfer_complete,
				(void *)xfer_data);
	if (ret != 0) {
		k_free(xfer_data);
	}

	return ret;
}

#endif /* defined(CONFIG_MFD_SC16IS75X_ASYNC) && defined(CONFIG_SPI_ASYNC) */

static const struct mfd_sc16is75x_transfer_function
mfd_sc16is75x_spi_init_transfer_function = {
	.read_raw = mfd_sc16is75x_spi_read_raw,
	.write_raw = mfd_sc16is75x_spi_write_raw,
#ifdef CONFIG_MFD_SC16IS75X_ASYNC
#ifdef CONFIG_SPI_ASYNC
	.read_raw_signal = mfd_sc16is75x_spi_read_raw_signal,
#else /* CONFIG_SPI_ASYNC */
	.read_raw_signal = mfd_sc16is75x_read_raw_signal,
#endif /* CONFIG_SPI_ASYNC */
#endif /* CONFIG_MFD_SC16IS75X_ASYNC */
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
