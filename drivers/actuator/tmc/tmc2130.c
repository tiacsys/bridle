/*
 * Copyright (c) 2023 TiaC Systems
 * Copyright (c) 2022 Stefano Cottafavi
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT trinamic_tmc2130

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/init.h>
#include <zephyr/sys/byteorder.h>
#include <zephyr/sys/__assert.h>
#include <zephyr/logging/log.h>

#include "tmc2130.h"

LOG_MODULE_REGISTER(TMC2130, CONFIG_BRIDLE_ACTUATOR_LOG_LEVEL);

static int tmc2130_attr_set(const struct device *dev,
			     enum actuator_channel chan,
			     enum actuator_attribute attr,
			     const struct actuator_value *val)
{
	LOG_INF("channel: %u, attribute: %u, value: [%i,%i]",
		chan, attr, val->val1, val->val2);
	return -ENOTSUP;
}

static int tmc2130_attr_get(const struct device *dev,
			     enum actuator_channel chan,
			     enum actuator_attribute attr,
			     struct actuator_value *val)
{
	LOG_INF("channel: %u, attribute: %u", chan, attr);
	return -ENOTSUP;
}

static const struct actuator_driver_api tmc2130_api_funcs = {
	.attr_set = tmc2130_attr_set,
	.attr_get = tmc2130_attr_get,
};

static int tmc2130_init_chip(const struct device *dev)
{
	struct tmc2130_data * const data = dev->data;

	tmc2130_init(&data->api_type, 1, &data->api_conf,
		     &tmc2130_defaultRegisterResetState[0]);
	// TODO: use tmc2130_setCallback()
	// instead of tmc2130_fillShadowRegisters()
	tmc2130_fillShadowRegisters(&data->api_type);

	// +++ HACK +++ HACK +++ HACK +++
	for (size_t i = 0; i < TMC2130_REGISTER_COUNT; i++) {
		LOG_WRN("shadow register 0x%02x has 0x%08x", i,
			data->api_conf.shadowRegister[i]);
	}
	// +++ HACK +++ HACK +++ HACK +++

	return 0;
};

static int tmc2130_init_dev(const struct device *dev)
{
	const struct tmc_config * const config = dev->config;

	if (!spi_is_ready_dt(&config->spi)) {
		LOG_ERR("SPI bus is not ready");
		return -ENODEV;
	}

	// TODO: config->bus_init(dev);

	if (tmc2130_init_chip(dev) < 0) {
		LOG_DBG("Failed to initialize chip");
		return -EIO;
	}

	return 0;
}

// TODO: .bus_init = tmc2130_spi_init,
#define TMC2130_DEFINE(inst)						\
	static struct tmc2130_data tmc2130_data_##inst;			\
									\
	static const struct tmc_config tmc2130_config_##inst = {	\
		COND_CODE_1(DT_INST_ON_BUS(inst, spi),			\
			    (.spi = SPI_DT_SPEC_INST_GET(inst,		\
						SPI_OP_MODE_MASTER |	\
						SPI_TRANSFER_MSB |	\
						SPI_MODE_CPOL |		\
						SPI_MODE_CPHA |		\
						SPI_WORD_SET(8), 0U),),	\
			    ())						\
	};								\
									\
	BRIDLE_ACTUATOR_DEVICE_DT_INST_DEFINE(inst,			\
			tmc2130_init_dev,				\
			NULL /* w/o PM */,				\
			&tmc2130_data_##inst,				\
			&tmc2130_config_##inst,				\
			POST_KERNEL,					\
			CONFIG_BRIDLE_ACTUATOR_INIT_PRIORITY,		\
			&tmc2130_api_funcs);

DT_INST_FOREACH_STATUS_OKAY(TMC2130_DEFINE)
