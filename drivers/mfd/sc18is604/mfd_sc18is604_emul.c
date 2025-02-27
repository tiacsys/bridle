/*
 * Copyright (c) 2025 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT nxp_sc18is604

#include <stdint.h>
#include <zephyr/drivers/emul.h>
#include <zephyr/drivers/gpio/gpio_emul.h>
#include <zephyr/drivers/mfd/sc18is604.h>
#include <zephyr/drivers/mfd/sc18is604_emul.h>
#include "mfd_sc18is604.h"

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(mfd_sc18is604_emul, CONFIG_MFD_LOG_LEVEL);

#define SC18IS604_N_REGISTERS 6 /* 0x00 through 0x05 */

static const uint8_t sc18is604_reg_defaults[SC18IS604_N_REGISTERS] = {
	0x00, /* SC18IS604_REG_IO_CONFIG */
	0x00, /* SC18IS604_REG_IO_STATE (actually depends on pin states) */
	0x19, /* SC18IS604_REG_I2C_CLOCK (99kHz) */
	0x00, /* SC18IS604_REG_I2C_TIMEOUT */
	0x00, /* SC18IS604_REG_I2C_STATUS */
	0x00, /* SC18IS604_REG_I2C_ADDRESS */
};

struct mfd_sc18is604_emul_data {
	uint8_t reg[SC18IS604_N_REGISTERS];
	uint8_t rx_buf[SC18IS604_BUFFER_SIZE];
	struct mfd_sc18is604_emul_transmission last_transmission;
	uint8_t pending_rx[SC18IS604_BUFFER_SIZE];
};

struct mfd_sc18is604_emul_config {
};

int mfd_sc18is604_emul_i2c_set_rx(const struct emul *target, uint8_t *buf, size_t len)
{
	struct mfd_sc18is604_emul_data *data = target->data;

	/* Clear pending buffer */
	memset(data->pending_rx, 0, sizeof(data->pending_rx));

	/* Copy data into pending buffer */
	size_t copy_len = MIN(len, sizeof(data->pending_rx));

	memcpy(data->pending_rx, buf, copy_len);

	return copy_len;
}

int mfd_sc18is604_emul_i2c_get_last_tx(const struct emul *target,
				       struct mfd_sc18is604_emul_transmission *transmission)
{
	struct mfd_sc18is604_emul_data *data = target->data;
	*transmission = data->last_transmission;
	return 0;
}

int mfd_sc18is604_emul_gpio_set_input(const struct emul *target, uint8_t pin, uint8_t value)
{
	struct mfd_sc18is604_emul_data *data = target->data;

	/* Verify that pin exists */
	if (pin >= SC18IS604_IO_NUM_PINS_MAX) {
		LOG_ERR("Pin %d does not exist", pin);
		return -EINVAL;
	}

	/* Verify that pin is configured as input. Pin 4 is always configured as input. */
	if (pin <= 3) {
		/* Pin configuration is stored in 2 bits per pin. 0b00 and 0b01 both mean input. */
		uint8_t pin_config =
			(data->reg[SC18IS604_REG_IO_CONFIG] & (0b11 << (pin * 2))) >> (pin * 2);
		if (pin_config != 0b00 && pin_config != 0b01) {
			LOG_ERR("Pin %d is not configured as input", pin);
			return -EINVAL;
		}
	}

	data->reg[SC18IS604_REG_IO_STATE] &= ~(1 << pin);
	data->reg[SC18IS604_REG_IO_STATE] |= value << pin;
	return 0;
}

int mfd_sc18is604_emul_gpio_get_output(const struct emul *target, uint8_t pin, uint8_t *value)
{
	struct mfd_sc18is604_emul_data *data = target->data;

	/* Verify that pin exists */
	if (pin >= SC18IS604_IO_NUM_PINS_MAX) {
		LOG_ERR("Pin %d does not exist", pin);
		return -EINVAL;
	}

	/* Verify that pin is configured as output. Pin 4 can never be configured as output. */
	uint8_t pin_config =
		(data->reg[SC18IS604_REG_IO_CONFIG] & (0b11 << (pin * 2))) >> (pin * 2);
	if ((pin == 4) || pin_config != SC18IS604_IO_CONFIG_PUSH_PULL) {
		{
			LOG_ERR("Pin %d is not configured as output", pin);
			return -EINVAL;
		}
	}

	*value = (data->reg[SC18IS604_REG_IO_STATE] >> pin) & 1;
	return 0;
}

static void mfd_sc18is604_emul_version_string_into_rx_buffer(const struct emul *target)
{
	const struct mfd_sc18is604_config *dev_config = target->dev->config;
	struct mfd_sc18is604_emul_data *data = target->data;
	int ret = 0;

	const char version_string[] = MFD_SC18IS604_VERSION_CHIP " 1.0.0";
	size_t len = MIN(sizeof(data->rx_buf), sizeof(version_string));

	/* Move string into buffer */
	memcpy(data->rx_buf, version_string, len);

	/* Assert interrupt */
	ret = gpio_emul_input_set(dev_config->interrupt.port, dev_config->interrupt.pin, 1);
	if (ret != 0) {
		LOG_ERR("Failed to assert interrupt pin");
	}
}

static void mfd_sc18is604_get_rx_buffer(const struct emul *target, uint8_t *rx_buf, size_t len)
{
	struct mfd_sc18is604_emul_data *data = target->data;

	size_t copy_len = MIN(len, sizeof(data->rx_buf));

	memcpy(rx_buf, data->rx_buf, copy_len);
}

static uint8_t mfd_sc18is604_get_register(const struct emul *target, uint8_t reg)
{
	__ASSERT(reg < SC18IS604_N_REGISTERS, "Invalid register address");
	struct mfd_sc18is604_emul_data *data = target->data;

	/* If I2C status register is read, clear interrupt */
	if (reg == SC18IS604_REG_I2C_STATUS) {
		const struct mfd_sc18is604_config *dev_config = target->dev->config;
		int ret = gpio_emul_input_set(dev_config->interrupt.port, dev_config->interrupt.pin,
					      0);
		if (ret != 0) {
			LOG_ERR("Failed to de-assert interrupt pin");
		}
	}

	return data->reg[reg];
}

static void mfd_sc18is604_set_register(const struct emul *target, uint8_t reg, uint8_t val)
{
	__ASSERT(reg < SC18IS604_N_REGISTERS, "Invalid register address");
	struct mfd_sc18is604_emul_data *data = target->data;

	data->reg[reg] = val;

	LOG_DBG("Set register 0x%02x to 0x%02x", reg, val);
}

static void mfd_sc18is604_emul_read_i2c(const struct emul *target, size_t len)
{
	const struct mfd_sc18is604_config *dev_config = target->dev->config;
	struct mfd_sc18is604_emul_data *data = target->data;
	int ret = 0;

	/* Copy pending RX buffer into RX buffer proper */
	memcpy(data->rx_buf, data->pending_rx, len);

	/* Set I2C status register */
	data->reg[SC18IS604_REG_I2C_STATUS] = SC18IS604_I2C_STATUS_SUCCESS;

	/* Assert interrupt */
	ret = gpio_emul_input_set(dev_config->interrupt.port, dev_config->interrupt.pin, 1);
	if (ret != 0) {
		LOG_ERR("Failed to assert interrupt pin");
	}
}

static void mfd_sc18is604_emul_write_i2c(const struct emul *target, uint8_t addr,
					 const uint8_t *msg, size_t len)
{
	struct mfd_sc18is604_emul_data *data = target->data;
	const struct mfd_sc18is604_config *dev_config = target->dev->config;
	int ret = 0;

	__ASSERT(len <= SC18IS604_BUFFER_SIZE, "Message too long");

	/* Get address in 7-bit format */
	uint8_t addr_raw = addr >> 1;

	/* Register as last transmission */
	data->last_transmission.addr = addr_raw;
	data->last_transmission.len = len;
	memset(data->last_transmission.msg, 0, sizeof(data->last_transmission.msg));
	memcpy(data->last_transmission.msg, msg, len);

	/* Set I2C status register */
	data->reg[SC18IS604_REG_I2C_STATUS] = SC18IS604_I2C_STATUS_SUCCESS;

	/* Assert interrupt */
	ret = gpio_emul_input_set(dev_config->interrupt.port, dev_config->interrupt.pin, 1);
	if (ret != 0) {
		LOG_ERR("Failed to assert interrupt pin");
	}
}

static int mfd_sc18is604_emul_io_spi(const struct emul *target, const struct spi_config *config,
				     const struct spi_buf_set *tx_bufs,
				     const struct spi_buf_set *rx_bufs)
{
	/* Assert general preconditions for valid SPI IO */
	__ASSERT(tx_bufs != NULL, "SPI IO must always include a command byte");

	/* Assemble TX buffers into coherent message */
	size_t n_tx_bufs = tx_bufs->count;
	size_t tx_len = 0;

	for (size_t i = 0; i < n_tx_bufs; i++) {
		tx_len += tx_bufs->buffers[i].len;
	}

	uint8_t tx[tx_len];
	size_t tx_offset = 0;

	for (size_t i = 0; i < n_tx_bufs; i++) {
		const struct spi_buf *buf = &tx_bufs->buffers[i];
		/* Skip NULL buffers */
		if (buf->buf == NULL) {
			/* Still need to increment offset */
			tx_offset += buf->len;
			continue;
		}
		memcpy(tx + tx_offset, buf->buf, buf->len);
		tx_offset += buf->len;
	}

	/* First byte is always the command byte */
	uint8_t command = tx[0];

	/* Set up RX buffer */
	size_t rx_len = 0;

	if (rx_bufs != NULL) {
		size_t n_rx_bufs = rx_bufs->count;

		for (size_t i = 0; i < n_rx_bufs; i++) {
			rx_len += rx_bufs->buffers[i].len;
		}
		__ASSERT(rx_len == tx_len, "Total TX and RX buffer lengths must match");

	} else {
		rx_len = tx_len;
	}

	uint8_t rx[rx_len];

	memset(rx, 0, rx_len);

	/* Handle command */
	switch (command) {

	case SC18IS604_CMD_WRITE_I2C: {
		__ASSERT(tx_len >= 3, "Missing address and/or message bytes");

		size_t len = tx[1];
		uint8_t addr = tx[2];
		uint8_t *data = tx + 3;

		__ASSERT(len >= tx_len - 3, "Message length exceeds buffer length");

		mfd_sc18is604_emul_write_i2c(target, addr, data, len);
	} break;

	case SC18IS604_CMD_READ_I2C: {
		__ASSERT(tx_len >= 2, "Missing read length byte");

		size_t len = tx[1];

		mfd_sc18is604_emul_read_i2c(target, len);
	} break;

	case SC18IS604_CMD_READ_AFTER_WRITE_I2C: {
		__ASSERT(tx_len >= 4, "Missing address, write length, and/or read length bytes");
		size_t write_len = tx[1];
		size_t read_len = tx[2];
		uint8_t addr = tx[3];
		uint8_t *write_data = tx + 4;

		mfd_sc18is604_emul_write_i2c(target, addr, write_data, write_len);
		mfd_sc18is604_emul_read_i2c(target, read_len);
	} break;

	case SC18IS604_CMD_READ_BUFFER: {
		size_t len = rx_len - 1;

		mfd_sc18is604_get_rx_buffer(target, rx + 1, len);
	} break;

	case SC18IS604_CMD_WRITE_AFTER_WRITE_I2C: {
		size_t len_1 = tx[1];
		size_t len_2 = tx[2];
		uint8_t addr_1 = tx[3];
		uint8_t *data_1 = tx + 4;
		uint8_t addr_2 = tx[4 + len_1];
		uint8_t *data_2 = tx + 4 + len_1 + 1;

		mfd_sc18is604_emul_write_i2c(target, addr_1, data_1, len_1);
		mfd_sc18is604_emul_write_i2c(target, addr_2, data_2, len_2);
	} break;

	case SC18IS604_CMD_WRITE_REGISTER: {
		__ASSERT(tx_len >= 3, "Missing register and/or value bytes");

		uint8_t reg = tx[1];
		uint8_t val = tx[2];

		mfd_sc18is604_set_register(target, reg, val);
	} break;

	case SC18IS604_CMD_READ_REGISTER: {
		__ASSERT(tx_len >= 2, "Missing register byte");
		__ASSERT(rx_len >= 3, "RX buffer too short");

		uint8_t reg = tx[1];

		rx[2] = mfd_sc18is604_get_register(target, reg);
	} break;

	case SC18IS604_CMD_POWER_DOWN:
		__ASSERT(tx_len >= 3, "Missing power-down sequence bytes");
		/* Validate power-down sequence */
		if (tx[1] != 0x5a || tx[2] != 0xa5) {
			LOG_WRN("Invalid power-down sequence");
		}
		/* Do nothing here. The wake-up signal is asserting the CS pin, which will be done
		 * anyway when interacting with the device again.
		 */
		break;

	case SC18IS604_CMD_VERSION_STRING:
		mfd_sc18is604_emul_version_string_into_rx_buffer(target);
		break;
	}

	/* Copy RX buffer into SPI RX buffer(s) */
	if (rx_bufs != NULL) {
		size_t rx_offset = 0;

		for (size_t i = 0; i < rx_bufs->count; i++) {
			const struct spi_buf *buf = &rx_bufs->buffers[i];
			/* Skip NULL buffers */
			if (buf->buf == NULL) {
				/* Still need to increment offset */
				rx_offset += buf->len;
				continue;
			}
			memcpy(buf->buf, rx + rx_offset, buf->len);
			rx_offset += buf->len;
		}
	}

	return 0;
}

static struct spi_emul_api mfd_sc18is604_emul_api = {
	.io = mfd_sc18is604_emul_io_spi,
};

static int mfd_sc18is604_emul_init(const struct emul *target, const struct device *parent)
{
	ARG_UNUSED(parent);

	struct mfd_sc18is604_emul_data *data = target->data;

	/* Set registers to default values */
	memcpy(data->reg, sc18is604_reg_defaults, sizeof(data->reg));

	return 0;
}

#define MFD_SC18IS604_EMUL_DEFINE(inst)                                                            \
	static struct mfd_sc18is604_emul_data mfd_sc18is604_emul_data_##inst;                      \
	static const struct mfd_sc18is604_emul_config mfd_sc18is604_emul_config_##inst;            \
                                                                                                   \
	EMUL_DT_INST_DEFINE(inst, mfd_sc18is604_emul_init, &mfd_sc18is604_emul_data_##inst,        \
			    &mfd_sc18is604_emul_config_##inst, &mfd_sc18is604_emul_api, NULL)

DT_INST_FOREACH_STATUS_OKAY(MFD_SC18IS604_EMUL_DEFINE);
