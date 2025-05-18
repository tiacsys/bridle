/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief MFD Bus Transfer Driver for an SC18IM604 bridge
 */

#include <zephyr/kernel.h>

#include <zephyr/drivers/mfd/sc18is604.h>

#include "mfd_sc18is604.h"

int mfd_sc18is604_transfer(const struct device *dev,
			   uint8_t *cmd, size_t cmd_len,
			   uint8_t *tx_data, size_t tx_len,
			   uint8_t *rx_data, size_t rx_len)
{
	const struct mfd_sc18is604_config * const config = dev->config;
	int ret = 0;

	/*
	 * The SC18IS604 requires significant delay between each byte
	 * sent via SPI. We achieve this by sending bytes in individual
	 * transactions, but keeping the CS line set, and the device
	 * locked, until we explicitly release it (see the flags
	 * SPI_HOLD_ON_CS and SPI_LOCK_ON set in device init).
	 */

	struct spi_buf buffer = {
		.buf = NULL,
		.len = 1,
	};

	const struct spi_buf_set buf_set = {
		.buffers = &buffer,
		.count = 1
	};

	/* Write command sequence */
	if (cmd != NULL) {
		for (int i = 0; i < cmd_len; i++) {
			buffer.buf = &cmd[i];

			ret = spi_write_dt(&config->spi, &buf_set);
			if (ret != 0) {
				goto end;
			}

			k_usleep(MFD_SC18IS604_SPI_DELAY_USEC);
		}
	}

	/* Write data */
	if (tx_data != NULL) {
		for (int i = 0; i < tx_len; i++) {
			buffer.buf = &tx_data[i];

			ret = spi_write_dt(&config->spi, &buf_set);
			if (ret != 0) {
				goto end;
			}

			k_usleep(MFD_SC18IS604_SPI_DELAY_USEC);
		}
	}

	/* Read data */
	if (rx_data != NULL) {
		for (int i = 0; i < rx_len; i++) {
			buffer.buf = &rx_data[i];

			ret = spi_read_dt(&config->spi, &buf_set);
			if (ret != 0) {
				goto end;
			}

			k_usleep(MFD_SC18IS604_SPI_DELAY_USEC);
		}
	}

end:
	/*
	 * Releases the SPI bus itself, which we locked with
	 * our first spi_write_dt call.
	 */
	spi_release_dt(&config->spi);

	return ret;
}

int mfd_sc18is604_read_register(const struct device *dev,
				uint8_t reg, uint8_t *val)
{
	uint8_t cmd[] = {SC18IS604_CMD_READ_REGISTER, reg};

	return mfd_sc18is604_transfer(dev, cmd, ARRAY_SIZE(cmd),
					   NULL, 0, val, 1);
}

int mfd_sc18is604_write_register(const struct device *dev,
				 uint8_t reg, uint8_t val)
{
	uint8_t cmd[] = {SC18IS604_CMD_WRITE_REGISTER, reg};

	return mfd_sc18is604_transfer(dev, cmd, ARRAY_SIZE(cmd),
					   &val, 1, NULL, 0);
}

int mfd_sc18is604_read_buffer(const struct device *dev,
			      uint8_t *data, size_t len)
{
	uint8_t cmd[] = {SC18IS604_CMD_READ_BUFFER};

	return mfd_sc18is604_transfer(dev, cmd, ARRAY_SIZE(cmd),
					   NULL, 0, data, len);
}
