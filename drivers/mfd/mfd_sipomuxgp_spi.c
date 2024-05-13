/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mfd_sipomuxgp_spi.h"

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(mfd_sipomuxgp_spi, CONFIG_MFD_LOG_LEVEL);

int mfd_sipomuxgp_spi_transmit(const struct device *dev, const uint8_t addr,
			       const uint8_t *tx_data, const size_t tx_count,
			       const size_t padding_sz)
{
	const mfd_sipomuxgp_config_t * const config = dev->config;
	const mfd_sipomuxgp_spi_config_t * const backend_config =
		(const mfd_sipomuxgp_spi_config_t *)config->backend.config;
	uint8_t padbuf[padding_sz];
	struct spi_buf tx_buf[2] = {
		[0] = { .buf = (void *)tx_data, .len = tx_count },
		[1] = { .buf = (void *)&padbuf, .len = ARRAY_SIZE(padbuf) },
	};
	struct spi_buf_set tx_bufs = { .buffers = &tx_buf[0], .count = 2U };
	int ret = 0;

	/* initialize 'zero' padding buffer (if ARRAY_SIZE() > 0) */
	memset(padbuf, 0, ARRAY_SIZE(padbuf));

	/* disable output drivers before data will be changed */
	ret = config->backend.set_oe(dev, 0);
	if (ret < 0)
		return ret;

	/* stream out new data (if any) */
	if (tx_data != NULL) {
		ret = spi_write_dt(&backend_config->bus, &tx_bufs);
		if (ret < 0) {
			LOG_ERR("%s: can't shift data bits!", dev->name);
			return ret;
		}
	}

	/* set new address */
	ret = config->backend.set_addr(dev, addr);
	if (ret < 0)
		return ret;

	/* enable output drivers after data were changed */
	ret = config->backend.set_oe(dev, 1);
	if (ret < 0)
		return ret;

	return 0;
}

int mfd_sipomuxgp_spi_init(const struct device *dev)
{
	const mfd_sipomuxgp_config_t * const config = dev->config;
	const mfd_sipomuxgp_spi_config_t * const backend_config =
		(const mfd_sipomuxgp_spi_config_t *)config->backend.config;
	int ret;

	/* verify backup configuration */
	if (!backend_config) {
		LOG_ERR("%s: backend: missing SPI configuration", dev->name);
	}

	if (!config->backend.cfg_oe) {
		LOG_ERR("%s: backend: missing cfg_oe() callback", dev->name);
	}

	if (!config->backend.cfg_addr) {
		LOG_ERR("%s: backend: missing cfg_addr() callback", dev->name);
	}

	if (!config->backend.set_oe) {
		LOG_ERR("%s: backend: missing set_oe() callback", dev->name);
	}

	if (!config->backend.set_addr) {
		LOG_ERR("%s: backend: missing set_addr() callback", dev->name);
	}

	if (!config->backend.xfr_data) {
		LOG_ERR("%s: backend: missing xfr_data() callback", dev->name);
	}

	/* configure backup resources */
	ret = config->backend.cfg_oe(dev);
	if (ret < 0)
		return ret;

	ret = config->backend.cfg_addr(dev);
	if (ret < 0)
		return ret;

	if (!spi_is_ready_dt(&backend_config->bus)) {
		LOG_ERR("%s: SPI device %s not ready", dev->name,
			backend_config->bus.bus->name);
		return -ENODEV;
	}

	LOG_DBG("%s: ready with SPI backend over %s!", dev->name,
		backend_config->bus.bus->name);
	return 0;
}
