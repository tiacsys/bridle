/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief Driver for the UART part of an SC16IS75x bridge
 */

#define DT_DRV_COMPAT nxp_sc16is75x_uart

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/pm/device.h>

#include <zephyr/drivers/uart.h>
#include <zephyr/drivers/gpio.h>

#include <zephyr/drivers/mfd/sc16is75x.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(uart_sc16is75x, CONFIG_UART_LOG_LEVEL);

/**
 * @brief    UART part of an SC16IS75x bridge
 * @defgroup io_serial_sc16is75x SC16IS75x UART Driver
 * @ingroup  io_serial
 * @since    3.7
 * @version  1.0.0
 *
 * The UART driver part based on the MFD interface to the SC16IS75x
 * SPI/I2C to UART and GPIO controller bridge.
 *
 * @{
 */

struct uart_sc16is75x_config {
	const struct device *bus;
	uint8_t channel;
	uint32_t clock_frequency;
};

struct uart_sc16is75x_data {
	/* Mutex to allow locking across multiple transactions */
	struct k_mutex transaction_lock;
	struct uart_config uart_config;
#ifdef CONFIG_UART_SC16IS75X_INTERRUPT_DRIVEN
	const struct device *self;
	struct gpio_callback interrupt_cb;
	uart_irq_callback_user_data_t callback;
	void *cb_data;
#endif /* CONFIG_UART_SC16IS75X_INTERRUPT_DRIVEN */
};

static bool uart_sc16is75x_rx_available(const struct device *dev)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	uint8_t lsr = 0;
	int ret = 0;

	/* Line Status Register */
	ret = READ_SC16IS75X_CHREG(config->bus, config->channel, LSR, &lsr);
	if (ret != 0) {
		return false;
	}

	/*
	 * NOTE: if needed, this would be a good place to detect and
	 * handle lost characters due to SC16IS75X_BIT_LSR_RX_OVERRUN
	 * or other communication conditions (break, framing or parity
	 * error, or anything else) in polling mode.
	 */

	if (IS_BIT_SET(lsr, SC16IS75X_BIT_LSR_RX_OVERRUN)) {
		LOG_WRN_ONCE("%s: overrun error has occurred", dev->name);
	}

	return IS_BIT_SET(lsr, SC16IS75X_BIT_LSR_RX_DATA);
}

static bool uart_sc16is75x_tx_possible(const struct device *dev)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	uint8_t txlvl = 0;
	int ret = 0;

	/* Line Status Register */
	ret = READ_SC16IS75X_CHREG(config->bus, config->channel, TXLVL, &txlvl);
	if (ret != 0) {
		return false;
	}

	/*
	 * NOTE: if needed, this would be a good place to detect more
	 * then just the number of spaces available in the transmit
	 * FIFO in polling mode, e.g. the transmit empty indicators:
	 * SC16IS75X_BIT_LSR_THREMPTY or SC16IS75X_BIT_LSR_THRTSREMPTY.
	 */

	return (GET_FIELD(txlvl, SC16IS75X_BIT_TXLVL_SP) >= 1);
}

#ifdef CONFIG_UART_SC16IS75X_LOOPBACK

static int uart_sc16is75x_enable_loopback(const struct device *dev, bool enable)
{
	const struct uart_sc16is75x_config *const config = dev->config;

	/* Internal loopback is enabled by setting MCR[4] to 1 */
	return SETBIT_SC16IS75X_CHREG(config->bus, config->channel, MCR, SC16IS75X_BIT_MCR_LOOPBACK,
				      enable);
}

#endif /* CONFIG_UART_SC16IS75X_LOOPBACK */

static int uart_sc16is75x_enable_fifo(const struct device *dev, bool enable)
{
	const struct uart_sc16is75x_config *const config = dev->config;

	/* FIFO is enabled by setting FCR[0] to 1 */
	return SETBIT_SC16IS75X_CHREG(config->bus, config->channel, FCR, SC16IS75X_BIT_FCR_FIFOENA,
				      enable);
}

static int uart_sc16is75x_reset_fifos(const struct device *dev)
{
	const struct uart_sc16is75x_config *const config = dev->config;

	/* FIFO reset is controlled by FCR[1] (RX) and FCR[2] (TX) */
	uint8_t fcr = (BIT(SC16IS75X_BIT_FCR_RXFIFORST) | BIT(SC16IS75X_BIT_FCR_TXFIFORST));

	return WRITE_SC16IS75X_CHREG(config->bus, config->channel, FCR, fcr);
}

static int uart_sc16is75x_poll_in(const struct device *dev, unsigned char *p_char)
{
	const struct uart_sc16is75x_config *const config = dev->config;

	if (!uart_sc16is75x_rx_available(dev)) {
		return -1;
	}

	return READ_SC16IS75X_CHREG(config->bus, config->channel, RHR, p_char);
}

static void uart_sc16is75x_poll_out(const struct device *dev, unsigned char out_char)
{
	const struct uart_sc16is75x_config *const config = dev->config;

	if (uart_sc16is75x_tx_possible(dev)) {
		WRITE_SC16IS75X_CHREG(config->bus, config->channel, THR, out_char);
	}
}

#ifdef CONFIG_UART_WIDE_DATA

static int uart_sc16is75x_poll_in_u16(const struct device *dev, uint16_t *p_u16)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	uint8_t rxlvl = 0;
	uint8_t buf = 0;
	int ret = 0;

	/* Check whether at least 2 bytes are available */
	ret = READ_SC16IS75X_CHREG(config->bus, config->channel, RXLVL, &rxlvl);
	if (ret != 0) {
		return ret;
	}

	if (GET_FIELD(rxlvl, SC16IS75X_BIT_RXLVL_CH) < 2) {
		return -1;
	}

	/* Read out data byte-wise */
	ret = READ_SC16IS75X_CHREG(config->bus, config->channel, RHR, &buf);
	if (ret != 0) {
		return ret;
	}

	*p_u16 = buf << 8;

	ret = READ_SC16IS75X_CHREG(config->bus, config->channel, RHR, &buf);
	if (ret != 0) {
		return ret;
	}

	*p_u16 |= buf;

	return 0;
}

static void uart_sc16is75x_poll_out_u16(const struct device *dev, uint16_t out_u16)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	uint8_t txlvl = 0;
	uint8_t buf = 0;
	int ret = 0;

	/* Check whether at least 2 bytes are free */
	ret = READ_SC16IS75X_CHREG(config->bus, config->channel, TXLVL, &txlvl);
	if (ret != 0) {
		return;
	}

	if (GET_FIELD(txlvl, SC16IS75X_BIT_TXLVL_SP) >= 2) {

		/* Upper byte first */
		buf = (uint8_t)((out_u16 >> 8) & BIT_MASK(8));
		WRITE_SC16IS75X_CHREG(config->bus, config->channel, THR, buf);

		/* Lower byte second */
		buf = (uint8_t)(out_u16 & BIT_MASK(8));
		WRITE_SC16IS75X_CHREG(config->bus, config->channel, THR, buf);
	}
}

#endif /* CONFIG_UART_WIDE_DATA */

static int uart_sc16is75x_err_check(const struct device *dev)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	uint8_t lsr = 0;
	int errors = 0;
	int ret = 0;

	/* Check Line Status Register for errors in the FIFO. */
	ret = READ_SC16IS75X_CHREG(config->bus, config->channel, LSR, &lsr);
	if (ret != 0) {
		return ret;
	}

	/* LSR[7] is 1 if there is at least one error present. */
	if (!IS_BIT_SET(lsr, SC16IS75X_BIT_LSR_RX_FIFO)) {
		return 0;
	}

	/* Assemble error flags */
	/* LSR[1] ^= Overrun error */
	if (IS_BIT_SET(lsr, SC16IS75X_BIT_LSR_RX_OVERRUN)) {
		errors |= UART_ERROR_OVERRUN;
	}

	/* LSR[2] ^= Parity error */
	if (IS_BIT_SET(lsr, SC16IS75X_BIT_LSR_RX_PARITY)) {
		errors |= UART_ERROR_PARITY;
	}

	/* LSR[3] ^= Framing error */
	if (IS_BIT_SET(lsr, SC16IS75X_BIT_LSR_RX_FRAMING)) {
		errors |= UART_ERROR_FRAMING;
	}

	/* LSR[4] ^= Break interrupt */
	if (IS_BIT_SET(lsr, SC16IS75X_BIT_LSR_RX_LINE_BREAK)) {
		errors |= UART_BREAK;
	}

	return errors;
}

static int uart_sc16is75x_set_baudrate(const struct device *dev, uint32_t baudrate)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	struct uart_sc16is75x_data *const data = dev->data;
	bool dlena = false;
	int ret = 0;

	/* Compute divisor value  */
	uint16_t divisor = config->clock_frequency / (baudrate * 16);
	uint8_t divisor_lsb = divisor;
	uint8_t divisor_msb = divisor >> 8;

	/* Lock device before multi-transfer transaction */
	k_mutex_lock(&data->transaction_lock, K_FOREVER);

	/* Set LCR[7] to 1 to enable access to DLL and DLH registers */
	ret = SETBIT_SC16IS75X_CHREG(config->bus, config->channel, LCR, SC16IS75X_BIT_LCR_DLENA,
				     true);
	if (ret != 0) {
		goto end;
	}

	dlena = true;

	/* Write values to device. */
	ret = WRITE_SC16IS75X_CHREG(config->bus, config->channel, DLL, divisor_lsb);
	if (ret != 0) {
		goto end;
	}
	ret = WRITE_SC16IS75X_CHREG(config->bus, config->channel, DLH, divisor_msb);
	if (ret != 0) {
		goto end;
	}

	/* Unset LCR[7] to access normal registers again */
	ret = SETBIT_SC16IS75X_CHREG(config->bus, config->channel, LCR, SC16IS75X_BIT_LCR_DLENA,
				     false);
	if (ret != 0) {
		goto end;
	}

	dlena = false;

	/* Update cached setting */
	data->uart_config.baudrate = baudrate;

end:
	/* Unlock device after transaction, and possibly do cleanup */
	if (dlena) {
		ret = SETBIT_SC16IS75X_CHREG(config->bus, config->channel, LCR,
					     SC16IS75X_BIT_LCR_DLENA, false);
	}

	k_mutex_unlock(&data->transaction_lock);
	return ret;
}

static int uart_sc16is75x_set_hw_flow_ctrl(const struct device *dev, bool enable)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	struct uart_sc16is75x_data *const data = dev->data;
	bool enhanced_reg_enabled = false;
	uint8_t lcr = 0;
	uint8_t efr = 0;
	int ret = 0;

	/*
	 * To access enhanced register set, LCR must be set to 0xbf.
	 * Save current value to restore later.
	 */

	/* Lock device for multi-transfer transaction */
	k_mutex_lock(&data->transaction_lock, K_FOREVER);

	ret = READ_SC16IS75X_CHREG(config->bus, config->channel, LCR, &lcr);
	if (ret != 0) {
		goto end;
	}

	ret = WRITE_SC16IS75X_CHREG(config->bus, config->channel, LCR,
				    SC16IS75X_BIT_LCR_ACCESS_EFR);
	if (ret != 0) {
		goto end;
	}

	enhanced_reg_enabled = true;

	/* Get value of EFR register */
	ret = READ_SC16IS75X_CHREG(config->bus, config->channel, EFR, &efr);
	if (ret != 0) {
		goto end;
	}

	/* Set Auto-RTS and Auto-CTS */
	WRITE_BIT(efr, SC16IS75X_BIT_EFR_RTSENA, enable); /* Auto-RTS */
	WRITE_BIT(efr, SC16IS75X_BIT_EFR_CTSENA, enable); /* Auto-CTS */

	/* Write back modified value */
	ret = WRITE_SC16IS75X_CHREG(config->bus, config->channel, EFR, efr);
	if (ret != 0) {
		goto end;
	}

end:
	/* Unlock device after transaction, and possibly do restore */
	if (enhanced_reg_enabled) {
		ret = WRITE_SC16IS75X_CHREG(config->bus, config->channel, LCR, lcr);
	}

	k_mutex_unlock(&data->transaction_lock);
	return ret;
}

static int uart_sc16is75x_use_modem_pins(const struct device *dev, bool enable)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	uint8_t bit;

	/*
	 * IOControl[1] enables extra modem pins for channel 0 (A),
	 * IOControl[2] enables extra modem pins for channel 1 (B).
	 */

	if (config->channel == 0) {
		bit = SC16IS75X_BIT_IOCONTROL_MODEM_PINS_A;
	} else if (config->channel == 1) {
		bit = SC16IS75X_BIT_IOCONTROL_MODEM_PINS_B;
	} else {
		return -EINVAL;
	}

	return SETBIT_SC16IS75X_REG(config->bus, IOCONTROL, bit, enable);
}

static int uart_sc16is75x_set_rs485_flow_ctrl(const struct device *dev, bool enable)
{
	const struct uart_sc16is75x_config *const config = dev->config;

	/* EFCR[4] enables RTS control by the transmitter */
	return SETBIT_SC16IS75X_CHREG(config->bus, config->channel, EFCR, SC16IS75X_BIT_EFCR_RTSCON,
				      enable);
}

static int uart_sc16is75x_configure(const struct device *dev, const struct uart_config *cfg)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	struct uart_sc16is75x_data *const data = dev->data;
	uint8_t lcr = 0;
	uint8_t parity = 0;
	uint8_t stop_bits = 0;
	uint8_t data_bits = 0;
	int ret = 0;

	/*
	 * Set parity, stop bits and data bits
	 */

	/* Parity */
	switch (cfg->parity) {
	case UART_CFG_PARITY_NONE:
		parity = SC16IS75X_PARITY_NONE;
		break;
	case UART_CFG_PARITY_ODD:
		parity = SC16IS75X_PARITY_ODD;
		break;
	case UART_CFG_PARITY_EVEN:
		parity = SC16IS75X_PARITY_EVEN;
		break;
	case UART_CFG_PARITY_MARK:
		parity = SC16IS75X_PARITY_MARK;
		break;
	case UART_CFG_PARITY_SPACE:
		parity = SC16IS75X_PARITY_SPACE;
		break;
	default:
		return -EINVAL;
	}

	/* Stop bits */
	if (cfg->stop_bits == UART_CFG_STOP_BITS_1) {
		stop_bits = SC16IS75X_STOP_LEN_1;
	} else if ((cfg->stop_bits == UART_CFG_STOP_BITS_1_5) &&
		   (cfg->data_bits == UART_CFG_DATA_BITS_5)) {
		stop_bits = SC16IS75X_STOP_LEN_1_5;
	} else if ((cfg->stop_bits == UART_CFG_STOP_BITS_2) &&
		   ((cfg->data_bits == UART_CFG_DATA_BITS_6) ||
		    (cfg->data_bits == UART_CFG_DATA_BITS_7) ||
		    (cfg->data_bits == UART_CFG_DATA_BITS_8))) {
		stop_bits = SC16IS75X_STOP_LEN_2;
	} else {
		return -ENOTSUP;
	}

	/* Data bits */
	switch (cfg->data_bits) {
	case UART_CFG_DATA_BITS_5:
		data_bits = SC16IS75X_WORD_LEN_5;
		break;
	case UART_CFG_DATA_BITS_6:
		data_bits = SC16IS75X_WORD_LEN_6;
		break;
	case UART_CFG_DATA_BITS_7:
		data_bits = SC16IS75X_WORD_LEN_7;
		break;
	case UART_CFG_DATA_BITS_8:
		data_bits = SC16IS75X_WORD_LEN_8;
		break;
	default:
		return -EINVAL;
	}

	/* Lock device before multi-transfer transaction */
	k_mutex_lock(&data->transaction_lock, K_FOREVER);

	/* Read line control register value */
	ret = READ_SC16IS75X_CHREG(config->bus, config->channel, LCR, &lcr);
	if (ret != 0) {
		goto end;
	}

	/* Insert new values */
	SET_FIELD(lcr, SC16IS75X_BIT_LCR_PARITY, parity);
	SET_FIELD(lcr, SC16IS75X_BIT_LCR_STOP_LEN, stop_bits);
	SET_FIELD(lcr, SC16IS75X_BIT_LCR_WORD_LEN, data_bits);

	/* Write back updated register value */
	ret = WRITE_SC16IS75X_CHREG(config->bus, config->channel, LCR, lcr);
	if (ret != 0) {
		goto end;
	}

	data->uart_config.parity = cfg->parity;
	data->uart_config.stop_bits = cfg->stop_bits;
	data->uart_config.data_bits = cfg->data_bits;

	/* Set baud rate */
	ret = uart_sc16is75x_set_baudrate(dev, cfg->baudrate);
	if (ret != 0) {
		goto end;
	}

	/* Set flow control */
	switch (cfg->flow_ctrl) {
	case UART_CFG_FLOW_CTRL_NONE:
		ret = uart_sc16is75x_set_hw_flow_ctrl(dev, false);
		if (ret != 0) {
			goto end;
		}
		ret = uart_sc16is75x_use_modem_pins(dev, false);
		if (ret != 0) {
			goto end;
		}
		ret = uart_sc16is75x_set_rs485_flow_ctrl(dev, false);
		if (ret != 0) {
			goto end;
		}
		break;

	case UART_CFG_FLOW_CTRL_RTS_CTS:
		ret = uart_sc16is75x_set_hw_flow_ctrl(dev, true);
		if (ret != 0) {
			goto end;
		}
		ret = uart_sc16is75x_use_modem_pins(dev, false);
		if (ret != 0) {
			goto end;
		}
		ret = uart_sc16is75x_set_rs485_flow_ctrl(dev, false);
		if (ret != 0) {
			goto end;
		}
		break;

	case UART_CFG_FLOW_CTRL_DTR_DSR:
		ret = -ENOTSUP;
		goto end;

	case UART_CFG_FLOW_CTRL_RS485:
		ret = uart_sc16is75x_set_hw_flow_ctrl(dev, false);
		if (ret != 0) {
			goto end;
		}
		ret = uart_sc16is75x_use_modem_pins(dev, false);
		if (ret != 0) {
			goto end;
		}
		ret = uart_sc16is75x_set_rs485_flow_ctrl(dev, true);
		if (ret != 0) {
			goto end;
		}
		break;

	default:
		ret = -EINVAL;
		goto end;
	}

	data->uart_config.flow_ctrl = cfg->flow_ctrl;

end:
	k_mutex_unlock(&data->transaction_lock);
	return ret;
}

#ifdef CONFIG_UART_USE_RUNTIME_CONFIGURE

static int uart_sc16is75x_config_get(const struct device *dev, struct uart_config *cfg)
{
	struct uart_sc16is75x_data *const data = dev->data;

	*cfg = data->uart_config;

	return 0;
}

#endif /* CONFIG_UART_USE_RUNTIME_CONFIGURE */

#ifdef CONFIG_UART_LINE_CTRL

static int uart_sc16is75x_line_ctrl_set(const struct device *dev, uint32_t ctrl, uint32_t val)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	struct uart_sc16is75x_data *const data = dev->data;
	uint8_t reg_val = 0;
	uint8_t reg = 0;
	uint8_t bit = 0;
	int ret = 0;

	if (ctrl == UART_LINE_CTRL_BAUD_RATE) {
		return uart_sc16is75x_set_baudrate(dev, val);
	}

	switch (ctrl) {
	case UART_LINE_CTRL_RTS:
		/* RTS is in MCR[1] */
		reg = SC16IS75X_REG_MCR;
		bit = SC16IS75X_BIT_MCR_RTS;
		break;

	case UART_LINE_CTRL_DTR:
		/* DTR is in MCR[0] */
		reg = SC16IS75X_REG_MCR;
		bit = SC16IS75X_BIT_MCR_DTR;
		break;

	case UART_LINE_CTRL_DCD:
		/* CD is read-only */
		return -EINVAL;

	case UART_LINE_CTRL_DSR:
		/* DSR is read-only */
		return -EINVAL;

	default:
		return -EINVAL;
	}

	/* Lock device before multi-transfer transaction */
	k_mutex_lock(&data->transaction_lock, K_FOREVER);

	ret = mfd_sc16is75x_read_register(config->bus, config->channel, reg, &reg_val);
	if (ret != 0) {
		goto end;
	}

	WRITE_BIT(reg_val, bit, val);

	ret = mfd_sc16is75x_write_register(config->bus, config->channel, reg, reg_val);
	if (ret != 0) {
		goto end;
	}

end:
	k_mutex_unlock(&data->transaction_lock);
	return ret;
}

static int uart_sc16is75x_line_ctrl_get(const struct device *dev, uint32_t ctrl, uint32_t *val)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	struct uart_sc16is75x_data *const data = dev->data;
	uint8_t reg_val = 0;
	uint8_t reg = 0;
	uint8_t bit = 0;
	int ret = 0;

	if (ctrl == UART_LINE_CTRL_BAUD_RATE) {
		*val = data->uart_config.baudrate;
		goto end;
	}

	switch (ctrl) {
	case UART_LINE_CTRL_RTS:
		/* RTS is in MCR[1] */
		reg = SC16IS75X_REG_MCR;
		bit = SC16IS75X_BIT_MCR_RTS;
		break;

	case UART_LINE_CTRL_DTR:
		/* DTR is in MCR[0] */
		reg = SC16IS75X_REG_MCR;
		bit = SC16IS75X_BIT_MCR_DTR;
		break;

	case UART_LINE_CTRL_DCD:
		/* CD is in MSR[7] */
		reg = SC16IS75X_REG_MSR;
		bit = SC16IS75X_BIT_MSR_CD;
		break;

	case UART_LINE_CTRL_DSR:
		/* DSR is in MSR[5] */
		reg = SC16IS75X_REG_MSR;
		bit = SC16IS75X_BIT_MSR_DSR;
		break;

	default:
		return -EINVAL;
	}

	ret = mfd_sc16is75x_read_register(config->bus, config->channel, reg, &reg_val);
	if (ret != 0) {
		goto end;
	}

	*val = IS_BIT_SET(reg_val, bit);

end:
	return ret;
}

#endif /* CONFIG_UART_LINE_CTRL */

#ifdef CONFIG_UART_SC16IS75X_INTERRUPT_DRIVEN

static int uart_sc16is75x_fifo_fill(const struct device *dev, const uint8_t *tx_data, int len)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	uint8_t data_mut[SC16IS75X_FIFO_CAPACITY] = {0};
	uint8_t txlvl = 0;
	int ret = 0;

	/* Check current FIFO fill level (number of bytes available) */
	ret = READ_SC16IS75X_CHREG(config->bus, config->channel, TXLVL, &txlvl);
	if (ret != 0) {
		return ret;
	}

	/* Calculate how many bytes to write */
	if (len > txlvl) {
		len = txlvl;
	}

	/* Copy data to respect pointer const-ness */
	memcpy(data_mut, tx_data, len);

	/* Write that many bytes to FIFO */
	ret = mfd_sc16is75x_write_fifo(config->bus, config->channel, data_mut, len);
	if (ret != 0) {
		return ret;
	}

	return len;
}

static int uart_sc16is75x_fifo_read(const struct device *dev, uint8_t *rx_data, const int size)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	uint8_t rxlvl = 0;
	int bytes_to_read;
	int ret = 0;

	/* Check FIFO fill level */
	ret = READ_SC16IS75X_CHREG(config->bus, config->channel, RXLVL, &rxlvl);
	if (ret != 0) {
		return ret;
	}

	/* Calculate how many bytes we can read */
	bytes_to_read = rxlvl;
	if (bytes_to_read > size) {
		bytes_to_read = size;
	}

	if (bytes_to_read == 0) {
		return 0;
	}

	/* Read that many bytes from FIFO */
	ret = mfd_sc16is75x_read_fifo(config->bus, config->channel, rx_data, bytes_to_read);
	if (ret != 0) {
		return ret;
	}

	return bytes_to_read;
}

#ifdef CONFIG_UART_WIDE_DATA

static int uart_sc16is75x_fifo_fill_u16(const struct device *dev, const uint16_t *tx_data, int len)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	uint8_t data_mut[SC16IS75X_FIFO_CAPACITY] = {0};
	uint8_t txlvl = 0;
	int txlvl_words;
	int len_bytes;
	int ret = 0;

	/* Check curretn FIFO fill level (number of bytes available) */
	ret = READ_SC16IS75X_CHREG(config->bus, config->channel, TXLVL, &txlvl);
	if (ret != 0) {
		return ret;
	}

	/* Calculate how many words to write */
	txlvl_words = txlvl / 2;

	if (len > txlvl_words) {
		len = txlvl_words;
	}

	len_bytes = len / 2;

	/*
	 * Copy data to respect const-ness.
	 * Also cast pointer at this opportunity.
	 */
	memcpy(data_mut, (uint8_t *)tx_data, len_bytes);

	/* Write that many words to FIFO */
	ret = mfd_sc16is75x_write_fifo(config->bus, config->channel, data_mut, len_bytes);
	if (ret != 0) {
		return ret;
	}

	return len;
}

static int uart_sc16is75x_fifo_read_u16(const struct device *dev, uint16_t *rx_data, const int size)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	uint8_t rxlvl = 0;
	int rxlvl_words;
	int words_to_read;
	int bytes_to_read;
	int ret = 0;

	/* Check FIFO fill level */
	ret = READ_SC16IS75X_CHREG(config->bus, config->channel, RXLVL, &rxlvl);
	if (ret != 0) {
		return ret;
	}

	/* Calculate how many words we can read */
	rxlvl_words = rxlvl / 2;
	words_to_read = rxlvl_words;

	if (words_to_read > size) {
		words_to_read = size;
	}

	bytes_to_read = 2 * words_to_read;

	/* Read that many words from FIFO */
	ret = mfd_sc16is75x_read_fifo(config->bus, config->channel, (uint8_t *)rx_data,
				      bytes_to_read);
	if (ret != 0) {
		return ret;
	}

	return words_to_read;
}

#endif /* CONFIG_UART_WIDE_DATA */

static inline void uart_sc16is75x_irq_tx_set(const struct device *dev, bool enable)
{
	const struct uart_sc16is75x_config *const config = dev->config;

	/* IER[1] enables THR interrupt */
	SETBIT_SC16IS75X_CHREG(config->bus, config->channel, IER, SC16IS75X_BIT_IER_TXHSENA,
			       enable);
}

static void uart_sc16is75x_irq_tx_enable(const struct device *dev)
{
	uart_sc16is75x_irq_tx_set(dev, true);
}

static void uart_sc16is75x_irq_tx_disable(const struct device *dev)
{
	uart_sc16is75x_irq_tx_set(dev, false);
}

static int uart_sc16is75x_irq_tx_ready(const struct device *dev)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	uint8_t txlvl = 0;
	int ret = 0;

	/* TXLVL register holds number of bytes free in TX FIFO */
	ret = READ_SC16IS75X_CHREG(config->bus, config->channel, TXLVL, &txlvl);
	if (ret != 0) {
		return 0;
	}

	return (txlvl > 0);
}

static int uart_sc16is75x_irq_tx_complete(const struct device *dev)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	uint8_t lsr = 0;
	int ret = 0;

	/* LSR[5] holds THR status (0: not empty, 1: empty) */
	ret = READ_SC16IS75X_CHREG(config->bus, config->channel, LSR, &lsr);
	if (ret != 0) {
		return 0;
	}

	return IS_BIT_SET(lsr, SC16IS75X_BIT_LSR_THREMPTY);
}

static inline void uart_sc16is75x_irq_rx_set(const struct device *dev, bool enable)
{
	const struct uart_sc16is75x_config *const config = dev->config;

	/* IER[0] enables RHR interrupt */
	SETBIT_SC16IS75X_CHREG(config->bus, config->channel, IER, SC16IS75X_BIT_IER_RXHSENA,
			       enable);
}

static void uart_sc16is75x_irq_rx_enable(const struct device *dev)
{
	uart_sc16is75x_irq_rx_set(dev, true);
}

static void uart_sc16is75x_irq_rx_disable(const struct device *dev)
{
	uart_sc16is75x_irq_rx_set(dev, false);
}

static int uart_sc16is75x_irq_rx_ready(const struct device *dev)
{
	return uart_sc16is75x_rx_available(dev);
}

static inline void uart_sc16is75x_irq_err_set(const struct device *dev, bool enable)
{
	const struct uart_sc16is75x_config *const config = dev->config;

	/* IER[2] enables LSR interrupt */
	SETBIT_SC16IS75X_CHREG(config->bus, config->channel, IER, SC16IS75X_BIT_IER_RXLSENA,
			       enable);
}

static void uart_sc16is75x_irq_err_enable(const struct device *dev)
{
	uart_sc16is75x_irq_err_set(dev, true);
}

static void uart_sc16is75x_irq_err_disable(const struct device *dev)
{
	uart_sc16is75x_irq_err_set(dev, false);
}

static int uart_sc16is75x_irq_is_pending(const struct device *dev)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	uint8_t iir = 0;
	int ret = 0;

	/*
	 * It is only partially possible to read the IRQ pending bit from
	 * the read-only Interrupt Identification Register (IIR) without
	 * performing an immediate interrupt handling. If this were not
	 * done, interrupts would inevitably be lost.
	 */

	/* Read out IIR */
	ret = READ_SC16IS75X_CHREG(config->bus, config->channel, IIR, &iir);
	if (ret != 0) {
		return 0;
	}

	/* IIR[0] holds interrupt status (0: pending, 1: not pending) */
	return !IS_BIT_SET(iir, SC16IS75X_BIT_IIR_PENDING);
}

static int uart_sc16is75x_irq_update(const struct device *dev)
{
	return 1;
}

static void uart_sc16is75x_irq_callback_set(const struct device *dev,
					    uart_irq_callback_user_data_t cb, void *user_data)
{
	struct uart_sc16is75x_data *const data = dev->data;

	data->callback = cb;
	data->cb_data = user_data;
}

static void uart_sc16is75x_interrupt_callback(const struct device *bus, struct gpio_callback *cb,
					      gpio_port_pins_t event_pins)
{
	struct uart_sc16is75x_data *const data =
		CONTAINER_OF(cb, struct uart_sc16is75x_data, interrupt_cb);
	const struct device *dev = data->self;

	/* Call registered UART IRQ callback, if there is one */
	if (data->callback) {
		data->callback(dev, data->cb_data);
	}
}

#endif /* CONFIG_UART_SC16IS75X_INTERRUPT_DRIVEN */

#ifdef CONFIG_UART_ASYNC_API

static int uart_sc16is75x_callback_set(const struct device *dev, uart_callback_t callback,
				       void *user_data)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(callback);
	ARG_UNUSED(user_data);

	return -ENOTSUP;
}

#endif /* CONFIG_UART_ASYNC_API */

#ifdef CONFIG_UART_DRV_CMD

static int uart_sc16is75x_drv_cmd(const struct device *dev, uint32_t cmd, uint32_t p)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(cmd);
	ARG_UNUSED(p);

	return -ENOTSUP;
}

#endif /* CONFIG_UART_DRV_CMD */

static const struct uart_driver_api uart_sc16is75x_api = {
	.poll_in = uart_sc16is75x_poll_in,
	.poll_out = uart_sc16is75x_poll_out,
#ifdef CONFIG_UART_WIDE_DATA
	.poll_in_u16 = uart_sc16is75x_poll_in_u16,
	.poll_out_u16 = uart_sc16is75x_poll_out_u16,
#endif /* CONFIG_UART_WIDE_DATA */
	.err_check = uart_sc16is75x_err_check,
#ifdef CONFIG_UART_USE_RUNTIME_CONFIGURE
	.configure = uart_sc16is75x_configure,
	.config_get = uart_sc16is75x_config_get,
#endif /* CONFIG_UART_USE_RUNTIME_CONFIGURE */
#ifdef CONFIG_UART_LINE_CTRL
	.line_ctrl_set = uart_sc16is75x_line_ctrl_set,
	.line_ctrl_get = uart_sc16is75x_line_ctrl_get,
#endif /* CONFIG_UART_LINE_CTRL */

#ifdef CONFIG_UART_SC16IS75X_INTERRUPT_DRIVEN
	.fifo_fill = uart_sc16is75x_fifo_fill,
	.fifo_read = uart_sc16is75x_fifo_read,
#ifdef CONFIG_UART_WIDE_DATA
	.fifo_fill_u16 = uart_sc16is75x_fifo_fill_u16,
	.fifo_read_u16 = uart_sc16is75x_fifo_read_u16,
#endif /* CONFIG_UART_WIDE_DATA */
	.irq_tx_enable = uart_sc16is75x_irq_tx_enable,
	.irq_tx_disable = uart_sc16is75x_irq_tx_disable,
	.irq_tx_ready = uart_sc16is75x_irq_tx_ready,
	.irq_tx_complete = uart_sc16is75x_irq_tx_complete,
	.irq_rx_enable = uart_sc16is75x_irq_rx_enable,
	.irq_rx_disable = uart_sc16is75x_irq_rx_disable,
	.irq_rx_ready = uart_sc16is75x_irq_rx_ready,
	.irq_err_enable = uart_sc16is75x_irq_err_enable,
	.irq_err_disable = uart_sc16is75x_irq_err_disable,
	.irq_is_pending = uart_sc16is75x_irq_is_pending,
	.irq_update = uart_sc16is75x_irq_update,
	.irq_callback_set = uart_sc16is75x_irq_callback_set,
#endif /* CONFIG_UART_SC16IS75X_INTERRUPT_DRIVEN */

#ifdef CONFIG_UART_ASYNC_API
	.callback_set = uart_sc16is75x_callback_set, /* Not supported */
	.tx = NULL,
	.tx_abort = NULL,
	.rx_enable = NULL,
	.rx_buf_rsp = NULL,
	.rx_disable = NULL,
#ifdef CONFIG_UART_WIDE_DATA
	.tx_u16 = NULL,
	.rx_enable_u16 = NULL,
	.rx_buf_rsp_u16 = NULL,
#endif /* CONFIG_UART_WIDE_DATA */
#endif /* CONFIG_UART_ASYNC_API */

#ifdef CONFIG_UART_DRV_CMD
	.uart_sc16is75x_drv_cmd = uart_sc16is75x_drv_cmd,
#endif /* CONFIG_UART_DRV_CMD */

};

static int uart_sc16is75x_pm_device_pm_action(const struct device *const dev,
					      enum pm_device_action action)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(action);

	return 0;
}

static int uart_sc16is75x_init(const struct device *dev)
{
	const struct uart_sc16is75x_config *const config = dev->config;
	struct uart_sc16is75x_data *const data = dev->data;
#ifdef CONFIG_UART_SC16IS75X_INTERRUPT_DRIVEN
	gpio_port_pins_t event_pins;
#endif /* CONFIG_UART_SC16IS75X_INTERRUPT_DRIVEN */
	int ret = 0;

	/* Confirm (MFD) bridge readiness */
	if (!device_is_ready(config->bus)) {
		LOG_ERR("%s: bridge device %s not ready", dev->name, config->bus->name);
		return -ENODEV;
	}

	/* Initialize transaction lock */
	k_mutex_init(&data->transaction_lock);

	/* Apply initial config */
	ret = uart_sc16is75x_configure(dev, &data->uart_config);
	if (ret != 0) {
		LOG_ERR("%s: configure device failed: %d", dev->name, ret);
		return ret;
	}

	/* Enable internal FIFO */
	ret = uart_sc16is75x_reset_fifos(dev);
	if (ret != 0) {
		LOG_ERR("%s: reset FIFO failed: %d", dev->name, ret);
		return ret;
	}
	ret = uart_sc16is75x_enable_fifo(dev, true);
	if (ret != 0) {
		LOG_ERR("%s: enable FIFO failed: %d", dev->name, ret);
		return ret;
	}

#ifdef CONFIG_UART_SC16IS75X_INTERRUPT_DRIVEN

	/* Create back-reference for interrupt handling */
	data->self = dev;

	/* Set up interrupt handling */
	switch (config->channel) {
	case 0:
		event_pins = BIT(SC16IS75X_EVENT_UART0_RXLSE) | BIT(SC16IS75X_EVENT_UART0_RXTO) |
			     BIT(SC16IS75X_EVENT_UART0_RHRI) | BIT(SC16IS75X_EVENT_UART0_THRI);
		/* no modem signals: BIT(SC16IS75X_EVENT_UART0_MSI) */
		/* no Xoff/Xon trigger: BIT(SC16IS75X_EVENT_UART0_XOFF) */
		/* no RTS/CTS trigger: BIT(SC16IS75X_EVENT_UART0_HWFL) */
		break;
	case 1:
		event_pins = BIT(SC16IS75X_EVENT_UART1_RXLSE) | BIT(SC16IS75X_EVENT_UART1_RXTO) |
			     BIT(SC16IS75X_EVENT_UART1_RHRI) | BIT(SC16IS75X_EVENT_UART1_THRI);
		/* no modem signals: BIT(SC16IS75X_EVENT_UART1_MSI) */
		/* no Xoff/Xon trigger: BIT(SC16IS75X_EVENT_UART1_XOFF) */
		/* no RTS/CTS trigger: BIT(SC16IS75X_EVENT_UART1_HWFL) */
		break;
	default:
		return -ENODEV;
	}

	gpio_init_callback(&data->interrupt_cb, uart_sc16is75x_interrupt_callback, event_pins);

	ret = mfd_sc16is75x_add_callback(config->bus, &data->interrupt_cb);
	if (ret != 0) {
		LOG_ERR("%s: failed to register interrupt callback on %s: %d", dev->name,
			config->bus->name, ret);
		return ret;
	}

#endif /* CONFIG_UART_SC16IS75X_INTERRUPT_DRIVEN */

#ifdef CONFIG_UART_SC16IS75X_LOOPBACK
	/* Enable internal loopback */
	ret = uart_sc16is75x_enable_loopback(dev, true);
	if (ret != 0) {
		LOG_ERR("%s: enable internal loopback failed: %d", dev->name, ret);
		return ret;
	}
#endif /* CONFIG_UART_SC16IS75X_LOOPBACK */

	LOG_DBG("%s: ready for %u bps with bridge backend over %s!", dev->name,
		data->uart_config.baudrate, config->bus->name);

	return pm_device_driver_init(dev, uart_sc16is75x_pm_device_pm_action);
	;
}

#define UART_SC16IS75X_DEFINE(inst)                                                                \
                                                                                                   \
	static struct uart_sc16is75x_config uart_sc16is75x_config_##inst = {                       \
		.bus = DEVICE_DT_GET(DT_INST_BUS(inst)),                                           \
		.channel = DT_INST_REG_ADDR(inst),                                                 \
		.clock_frequency =                                                                 \
			DT_PROP_BY_PHANDLE(DT_INST_PARENT(inst), clock, clock_frequency),          \
	};                                                                                         \
	BUILD_ASSERT(DT_INST_REG_ADDR(inst) < SC16IS75X_UART_CHANNELS_MAX, "Too many channels");   \
                                                                                                   \
	static struct uart_sc16is75x_data uart_sc16is75x_data_##inst = {                           \
		.uart_config = {                                                                   \
			.baudrate = DT_INST_PROP_OR(inst, current_speed, 9600),                    \
			.parity = DT_INST_ENUM_IDX_OR(inst, parity, UART_CFG_PARITY_EVEN),         \
			.stop_bits = DT_INST_ENUM_IDX_OR(inst, stop_bits, UART_CFG_STOP_BITS_2),   \
			.data_bits = DT_INST_ENUM_IDX_OR(inst, data_bits, UART_CFG_DATA_BITS_6),   \
			.flow_ctrl = COND_CODE_1(DT_INST_PROP_OR(inst,       \
						hw_flow_control, false),     \
					(UART_CFG_FLOW_CTRL_RTS_CTS),        \
					(UART_CFG_FLOW_CTRL_NONE)),      \
			},                                                                         \
	};                                                                                         \
                                                                                                   \
	PM_DEVICE_DT_INST_DEFINE(inst, uart_sc16is75x_pm_device_pm_action);                        \
                                                                                                   \
	DEVICE_DT_INST_DEFINE(inst, uart_sc16is75x_init, PM_DEVICE_DT_INST_GET(inst),              \
			      &uart_sc16is75x_data_##inst, &uart_sc16is75x_config_##inst,          \
			      POST_KERNEL, CONFIG_UART_SC16IS75X_INIT_PRIORITY,                    \
			      &uart_sc16is75x_api);

DT_INST_FOREACH_STATUS_OKAY(UART_SC16IS75X_DEFINE);

/** @} */
