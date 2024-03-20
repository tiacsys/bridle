/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio/gpio_utils.h>

#include <zephyr/drivers/mfd/sc16is75x.h>

#include "mfd_sc16is75x.h"

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(mfd_sc16is75x, CONFIG_MFD_LOG_LEVEL);

#define SC16IS75X_SA_RD	true
#define SC16IS75X_SA_WR	false

static inline int mfd_sc16is75x_sub_address(const bool read,
					    const uint8_t reg,
					    const uint8_t channel,
					    uint8_t *sub_address)
{
	/*
	 * Subaddress scheme: [ R/W, A3, A2, A1, A0, CH1, Ch0, X]
	 * R/W: 1: Read, 0: Write (SPI only)
	 * A[3:0]: Register address
	 * CH1, CH0: Select serial channel
	 * X: Unused
	 */

	if ((reg & BIT_MASK(4)) > BIT_MASK(4)) {
		return -EINVAL;
	}

	if ((channel & BIT_MASK(2)) > BIT_MASK(2)) {
		return -EINVAL;
	}

	*sub_address = 0;
	*sub_address |= (channel & BIT_MASK(2)) << 1;
	*sub_address |= (reg & BIT_MASK(4)) << 3;
	WRITE_BIT(*sub_address, 7, read ? 1 : 0);

	return 0;
}

static int mfd_sc16is75x_read(const struct device *dev,
			      const uint8_t channel, const uint8_t reg,
			      uint8_t *buf, const size_t len)
{
	struct mfd_sc16is75x_data * const data = dev->data;
	uint8_t sub_address = 0;
	int ret = 0;

	ret = mfd_sc16is75x_sub_address(SC16IS75X_SA_RD, reg, channel,
					&sub_address);
	if (ret != 0) {
		return ret;
	}

	return data->transfer_function->read_raw(dev, sub_address, buf, len);
}

#define READ_SC16IS75X_CHANNEL(dev, ch, reg, buf, len)                       \
	mfd_sc16is75x_read((dev), (ch), SC16IS75X_REG_##reg, (buf), (len));

static int mfd_sc16is75x_write(const struct device *dev,
			       const uint8_t channel, const uint8_t reg,
			       const uint8_t *buf, const size_t len)
{
	struct mfd_sc16is75x_data * const data = dev->data;
	uint8_t sub_address = 0;
	int ret = 0;

	ret = mfd_sc16is75x_sub_address(SC16IS75X_SA_WR, reg, channel,
					&sub_address);
	if (ret != 0) {
		return ret;
	}

	return data->transfer_function->write_raw(dev, sub_address, buf, len);
}

#define WRITE_SC16IS75X_CHANNEL(dev, ch, reg, buf, len)                      \
	mfd_sc16is75x_write((dev), (ch), SC16IS75X_REG_##reg, (buf), (len));

int mfd_sc16is75x_read_register(const struct device *dev,
				const uint8_t channel,
				const uint8_t reg, uint8_t *value)
{
	return mfd_sc16is75x_read(dev, channel, reg, value, 1);
}

int mfd_sc16is75x_write_register(const struct device *dev,
				 const uint8_t channel,
				 const uint8_t reg, const uint8_t value)
{
	return mfd_sc16is75x_write(dev, channel, reg, &value, 1);
}

int mfd_sc16is75x_set_register_bit(const struct device *dev,
				   const uint8_t channel, const uint8_t reg,
				   const uint8_t bit, const bool value)
{
	struct mfd_sc16is75x_data * const data = dev->data;
	uint8_t reg_val = 0;
	int ret = 0;

	/* Lock device before multi-transfer transaction */
	k_mutex_lock(&data->transaction_lock, K_FOREVER);

	/* Read out current value */
	ret = mfd_sc16is75x_read(dev, channel, reg, &reg_val, 1);
	if (ret != 0) {
		goto end;
	}

	/* Set selected bit */
	WRITE_BIT(reg_val, bit, value);

	/* Write back modified value */
	ret = mfd_sc16is75x_write(dev, channel, reg, &reg_val, 1);
	if (ret != 0) {
		goto end;
	}

end:
	k_mutex_unlock(&data->transaction_lock);
	return ret;
}

int mfd_sc16is75x_read_fifo(const struct device *dev, const uint8_t channel,
			    uint8_t *buf, const size_t len)
{
	return READ_SC16IS75X_CHANNEL(dev, channel, RHR, buf, len);
}

int mfd_sc16is75x_write_fifo(const struct device *dev, const uint8_t channel,
			     const uint8_t *buf, const size_t len)
{
	return WRITE_SC16IS75X_CHANNEL(dev, channel, THR, buf, len);
}

static int mfd_sc16is75x_init(const struct device *dev)
{
	const struct mfd_sc16is75x_config * const config = dev->config;
	struct mfd_sc16is75x_data * const data = dev->data;
	int ret = 0;

	/* Create back-reference for interrupt handling */
	data->self = dev;

	/* Initialize transaction lock */
	k_mutex_init(&data->transaction_lock);

	/* Configure bus specific transfer functions (SPI or I2C) */
	ret = config->bus_init(dev);
	if (ret != 0) {
		LOG_ERR("%s: bus initialization failed: %d", dev->name, ret);
		goto end;
	}

	/* Configure reset GPIO pin, confirm device readiness first */
	if (gpio_is_ready_dt(&config->reset)) {
		ret = gpio_pin_configure_dt(&config->reset, GPIO_OUTPUT);
		if (ret != 0) {
			LOG_ERR("%s: configure reset pin failed: %d",
				dev->name, ret);
			goto end;
		}
	} else {
		LOG_ERR("%s: GPIO device %s with reset pin not ready",
			dev->name, config->reset.port->name);
		return -ENODEV;
	}

	/*
	 * Pull reset for a few µs, then wait another
	 * few µs for device startup.
	 */
	gpio_pin_set_dt(&config->reset, 1); /* assert */
	k_usleep(5);
	gpio_pin_set_dt(&config->reset, 0); /* deassert */
	k_usleep(5);

end:
	return ret;
}

#ifdef CONFIG_PM_DEVICE
static int mfd_sc16is75x_pm_device_pm_action(const struct device *dev,
					     enum pm_device_action action)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(action);

	return 0;
}
#endif

#define MFD_SC16IS75X_DEFINE_SPI_BUS(inst)                                   \
	.spi = SPI_DT_SPEC_INST_GET(inst, SPI_OP_MODE_MASTER |               \
					  SPI_WORD_SET(8), 0),               \
	.bus_init = mfd_sc16is75x_spi_init

#define MFD_SC16IS75X_DEFINE_I2C_BUS(inst)                                   \
	.i2c = I2C_DT_SPEC_INST_GET(inst),                                   \
	.bus_init = mfd_sc16is75x_i2c_init

#define MFD_SC16IS75X_DEFINE_BUS(inst)                                       \
	COND_CODE_1(DT_INST_ON_BUS(inst, spi),                               \
			(MFD_SC16IS75X_DEFINE_SPI_BUS(inst)),                \
			(MFD_SC16IS75X_DEFINE_I2C_BUS(inst)))

#define MFD_SC16IS75X_DEFINE(inst)                                           \
                                                                             \
	static struct mfd_sc16is75x_config mfd_sc16is75x_config_##inst =     \
	{                                                                    \
		MFD_SC16IS75X_DEFINE_BUS(inst),                              \
		.reset = GPIO_DT_SPEC_INST_GET(inst, reset_gpios),           \
	};                                                                   \
                                                                             \
	static struct mfd_sc16is75x_data mfd_sc16is75x_data_##inst;          \
                                                                             \
	PM_DEVICE_DT_INST_DEFINE(inst, mfd_sc16is75x_pm_device_pm_action);   \
                                                                             \
	DEVICE_DT_INST_DEFINE(inst, mfd_sc16is75x_init,                      \
			      PM_DEVICE_DT_INST_GET(inst),                   \
			      &mfd_sc16is75x_data_##inst,                    \
			      &mfd_sc16is75x_config_##inst, POST_KERNEL,     \
			      CONFIG_MFD_SC16IS75X_INIT_PRIORITY, NULL);

DT_INST_FOREACH_STATUS_OKAY(MFD_SC16IS75X_DEFINE);
