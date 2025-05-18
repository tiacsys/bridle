/*
 * Copyright (c) 2023 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief MFD SPI-Bus Transfer Driver Interface for an SIPO/MUX GP matrix controller
 */

#ifndef DRIVERS_MFD_MFD_SIPOMUXGP_SPI_H_
#define DRIVERS_MFD_MFD_SIPOMUXGP_SPI_H_

#include "mfd_sipomuxgp.h"

#include <zephyr/drivers/spi.h>

typedef struct mfd_sipomuxgp_spi_config {
	const struct spi_dt_spec bus;
} mfd_sipomuxgp_spi_config_t;

#define MFD_SIPOMUXGP_spi_CFG_INIT(n, b)                        \
	static const mfd_sipomuxgp_spi_config_t                 \
			    mfd_sipomuxgp_spi_config_##n =      \
	{                                                       \
		.bus = SPI_DT_SPEC_GET(INST_DT_SIPOMUXGP(n, b), \
				       SPI_OP_MODE_MASTER |     \
				       SPI_TRANSFER_MSB |       \
				       SPI_WORD_SET(8), 0),     \
	};

int mfd_sipomuxgp_spi_init(const struct device *dev);
int mfd_sipomuxgp_spi_transmit(const struct device *dev, const uint8_t addr,
			       const uint8_t *tx_data, const size_t tx_count,
			       const size_t padding_sz);

#endif /* DRIVERS_MFD_MFD_SIPOMUXGP_SPI_H_ */
