/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef ZEPHYR_INCLUDE_DRIVERS_MFD_SC16IS75X_H_
#define ZEPHYR_INCLUDE_DRIVERS_MFD_SC16IS75X_H_

#ifdef __cplusplus
extern "C" {
#endif

#include <stddef.h>
#include <stdint.h>

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>

#include <zephyr/sys/util_macro.h>

/*
 * SC16IS75X register bit/field access operations
 */

#define IS_BIT_SET(reg, bit)		(((reg >> bit) & (0x1)) != 0)

#define FIELD_POS(field)		field##_POS
#define FIELD_SIZE(field)		field##_SIZE

#define GET_FIELD(reg, field) \
	_GET_FIELD_(reg, FIELD_POS(field), FIELD_SIZE(field))
#define _GET_FIELD_(reg, f_pos, f_size)	(((reg) >> (f_pos)) & ((1 << (f_size)) - 1))

#define SET_FIELD(reg, field, value) \
	_SET_FIELD_(reg, FIELD_POS(field), FIELD_SIZE(field), value)
#define _SET_FIELD_(reg, f_pos, f_size, value) \
	((reg) = ((reg) & (~(((1 << (f_size)) - 1) << (f_pos)))) \
			| ((value) << (f_pos)))

#define GET_FIELD_POS(field) \
	_GET_FIELD_POS_(FIELD_POS(field))
#define _GET_FIELD_POS_(f_ops) f_ops

#define GET_FIELD_SZ(field) \
	_GET_FIELD_SZ_(FIELD_SIZE(field))
#define _GET_FIELD_SZ_(f_ops) f_ops

/*
 * General registers
 */

/* Receive Holding Register (RHR), read only */
#define SC16IS75X_REG_RHR			0x00

/* Transmit Holding Register (THR), write only */
#define SC16IS75X_REG_THR			0x00

/* Interrupt Enable Register (IER) */
#define SC16IS75X_REG_IER			0x01
#define SC16IS75X_BIT_IER_RXHSENA		0
#define SC16IS75X_BIT_IER_TXHSENA		1
#define SC16IS75X_BIT_IER_RXLSENA		2
#define SC16IS75X_BIT_IER_MSENA			3
#define SC16IS75X_BIT_IER_SLEEPENA		4
#define SC16IS75X_BIT_IER_XOFFENA		5
#define SC16IS75X_BIT_IER_RTSENA		6
#define SC16IS75X_BIT_IER_CTSENA		7

/* FIFO Control Register (FCR), write only */
#define SC16IS75X_REG_FCR			0x02
#define SC16IS75X_BIT_FCR_FIFOENA		0
#define SC16IS75X_BIT_FCR_RXFIFORST		1
#define SC16IS75X_BIT_FCR_TXFIFORST		2
				/* reserved	3 */
#define SC16IS75X_BIT_FCR_TXFIFOTRIG		4
#define SC16IS75X_TXFIFOTRIG_8SP		0b00
#define SC16IS75X_TXFIFOTRIG_16SP		0b01
#define SC16IS75X_TXFIFOTRIG_32SP		0b10
#define SC16IS75X_TXFIFOTRIG_56SP		0b11
#define SC16IS75X_BIT_FCR_RXFIFOTRIG		6
#define SC16IS75X_RXFIFOTRIG_8CH		0b00
#define SC16IS75X_RXFIFOTRIG_16CH		0b01
#define SC16IS75X_RXFIFOTRIG_56CH		0b10
#define SC16IS75X_RXFIFOTRIG_60CH		0b11

/* Interrupt Identification Register (IIR), read only */
#define SC16IS75X_REG_IIR			0x02
#define SC16IS75X_BIT_IIR_PENDING		0
#define SC16IS75X_BIT_IIR_TYPE_POS		1
#define SC16IS75X_BIT_IIR_TYPE_SIZE		5
#define SC16IS75X_INT_RXLSE			0b00011
#define SC16IS75X_INT_RXTO			0b00110
#define SC16IS75X_INT_RHRI			0b00010
#define SC16IS75X_INT_THRI			0b00001
#define SC16IS75X_INT_MSI			0b00000
#define SC16IS75X_INT_IO			0b11000
#define SC16IS75X_INT_XOFF			0b01000
#define SC16IS75X_INT_HWFL			0b10000
#define SC16IS75X_BIT_IIR_MIRROR_FIFOENA_POS	6
#define SC16IS75X_BIT_IIR_MIRROR_FIFOENA_SIZE	2
#define SC16IS75X_INT_FIFOENA			0b11

/* Line Control Register (LCR) */
#define SC16IS75X_REG_LCR			0x03

#define SC16IS75X_BIT_LCR_WORD_LEN_POS		0
#define SC16IS75X_BIT_LCR_WORD_LEN_SIZE		2
#define SC16IS75X_WORD_LEN_5			0b00
#define SC16IS75X_WORD_LEN_6			0b01
#define SC16IS75X_WORD_LEN_7			0b10
#define SC16IS75X_WORD_LEN_8			0b11
#define SC16IS75X_BIT_LCR_STOP_LEN_POS		2
#define SC16IS75X_BIT_LCR_STOP_LEN_SIZE		1
#define SC16IS75X_STOP_LEN_1			0b0
#define SC16IS75X_STOP_LEN_1_5			0b1
#define SC16IS75X_STOP_LEN_2			0b1
#define SC16IS75X_BIT_LCR_PARITY_POS		3
#define SC16IS75X_BIT_LCR_PARITY_SIZE		3
#define SC16IS75X_PARITY_NONE			0b000
#define SC16IS75X_PARITY_ODD			0b001
#define SC16IS75X_PARITY_EVEN			0b011
#define SC16IS75X_PARITY_MARK			0b101
#define SC16IS75X_PARITY_SPACE			0b111
#define SC16IS75X_BIT_LCR_TX_LINE_BREAK		6
#define SC16IS75X_BIT_LCR_DLENA			7
#define SC16IS75X_BIT_LCR_ACCESS_EFR		0b10111111 /* 0xBF */

/* Modem Control Register (MCR) */
#define SC16IS75X_REG_MCR			0x04
#define SC16IS75X_BIT_MCR_DTR			0
#define SC16IS75X_BIT_MCR_RTS			1
#define SC16IS75X_BIT_MCR_TCRTLRENA		2
				/* reserved	3 */
#define SC16IS75X_BIT_MCR_LOOPBACK		4
#define SC16IS75X_BIT_MCR_XONANY		5
#define SC16IS75X_BIT_MCR_IRDAENA		6
#define SC16IS75X_BIT_MCR_CLKDIV		7

/* Line Status Register (LSR), read only */
#define SC16IS75X_REG_LSR			0x05
#define SC16IS75X_BIT_LSR_RX_DATA		0
#define SC16IS75X_BIT_LSR_RX_OVERRUN		1
#define SC16IS75X_BIT_LSR_RX_PARITY		2
#define SC16IS75X_BIT_LSR_RX_FRAMING		3
#define SC16IS75X_BIT_LSR_RX_LINE_BREAK		4
#define SC16IS75X_BIT_LSR_THREMPTY		5
#define SC16IS75X_BIT_LSR_THRTSREMPTY		6
#define SC16IS75X_BIT_LSR_RX_FIFO		7

/* Modem Status Register (MSR), read only */
#define SC16IS75X_REG_MSR			0x06
#define SC16IS75X_BIT_MSR_CTS_CHANGED		0
#define SC16IS75X_BIT_MSR_DSR_CHANGED		1
#define SC16IS75X_BIT_MSR_RI_CHANGED		2
#define SC16IS75X_BIT_MSR_CD_CHANGED		3
#define SC16IS75X_BIT_MSR_CTS			4
#define SC16IS75X_BIT_MSR_DSR			5
#define SC16IS75X_BIT_MSR_RI			6
#define SC16IS75X_BIT_MSR_CD			7

/* Scratchpad Register (SPR) */
#define SC16IS75X_REG_SPR			0x07

/* Transmission Control Register (TCR) */
#define SC16IS75X_REG_TCR			0x06

/* Trigger Level Register (TLR) */
#define SC16IS75X_REG_TLR			0x07

/* Transmitter FIFO Level register (TXLVL), read only */
#define SC16IS75X_REG_TXLVL			0x08
#define SC16IS75X_BIT_TXLVL_SP_POS		0
#define SC16IS75X_BIT_TXLVL_SP_SIZE		7

/* Receiver FIFO Level register (RXLVL), read only */
#define SC16IS75X_REG_RXLVL			0x09
#define SC16IS75X_BIT_RXLVL_CH_POS		0
#define SC16IS75X_BIT_RXLVL_CH_SIZE		7

/* Programmable I/O pins Direction register (IODir), all channels */
#define SC16IS75X_REG_IODIR			0x0A

/* Programmable I/O pins State register (IOState), all channels */
#define SC16IS75X_REG_IOSTATE			0x0B

/* Programmable I/O Interrupt Enable register (IOIntEna), all channels */
#define SC16IS75X_REG_IOINTENA			0x0C

/* Programmable I/O Control register (IOControl), all channels */
#define SC16IS75X_REG_IOCONTROL			0x0E
#define SC16IS75X_BIT_IOCONTROL_IOLATCH		0
#define SC16IS75X_BIT_IOCONTROL_MODEM_PINS_A	1
#define SC16IS75X_BIT_IOCONTROL_MODEM_PINS_B	2
#define SC16IS75X_BIT_IOCONTROL_SRESET		3
				/* reserved	4:7 */

/* Extra Features Control Register (EFCR) */
#define SC16IS75X_REG_EFCR			0x0F
#define SC16IS75X_BIT_EFCR_RS485		0
#define SC16IS75X_BIT_EFCR_RXDISABLE		1
#define SC16IS75X_BIT_EFCR_TXDISABLE		2
				/* reserved	3 */
#define SC16IS75X_BIT_EFCR_RTSCON		4
#define SC16IS75X_BIT_EFCR_RTSINVER		5
				/* reserved	6 */
#define SC16IS75X_BIT_EFCR_IRDA			7

/*
 * Special registers
 */

/* Division registers (DLL, DLH) */
#define SC16IS75X_REG_DLL			0x00
#define SC16IS75X_REG_DLH			0x01

/*
 * Enhanced registers
 */

/* Enhanced Features Register (EFR) */
#define SC16IS75X_REG_EFR			0x02
#define SC16IS75X_BIT_EFR_RX_SWFLOWCTRL_POS	0
#define SC16IS75X_BIT_EFR_RX_SWFLOWCTRL_SIZE	2
#define SC16IS75X_BIT_EFR_TX_SWFLOWCTRL_POS	2
#define SC16IS75X_BIT_EFR_TX_SWFLOWCTRL_SIZE	2
#define SC16IS75X_SWFLOWCTRL_NONE		0b00
#define SC16IS75X_SWFLOWCTRL_XONOFF1		0b10
#define SC16IS75X_SWFLOWCTRL_XONOFF2		0b01
#define SC16IS75X_SWFLOWCTRL_XONOFF12		0b11
#define SC16IS75X_BIT_EFR_EFENA			4
#define SC16IS75X_BIT_EFR_XOFF2ENA		5
#define SC16IS75X_BIT_EFR_RTSENA		6
#define SC16IS75X_BIT_EFR_CTSENA		7

/* Xon1 Special Character Register (XON1) */
#define SC16IS75X_REG_XON1			0x04

/* Xoff2 Special Character Register (XOFF2) */
#define SC16IS75X_REG_XON2			0x05

/* Xon1 Special Character Register (XON1) */
#define SC16IS75X_REG_XOFF1			0x06

/* Xoff2 Special Character Register (XOFF2) */
#define SC16IS75X_REG_XOFF2			0x07

/**
 * @defgroup mfd_interface_sc16is75x MFD SC16IS75X Interface
 * @ingroup mfd_interfaces
 * @{
 */

/** FIFO capacity in byte */
#define SC16IS75X_FIFO_CAPACITY			64

/** Maximum programmable I/O pins */
#define SC16IS75X_IO_NUM_PINS_MAX		8

/** Maximum UART channels */
#define SC16IS75X_UART_CHANNELS_MAX		2

/**
 * @brief Read from an internal register.
 *
 * @param dev An SC16IS75x device.
 * @param channel Channel to access.
 * @param reg Register address to read from.
 * @param[out] value Value of that register.
 * @retval 0 On succes.
 * @return Negative error code on failure.
 */
int mfd_sc16is75x_read_register(const struct device *dev,
				const uint8_t channel,
				const uint8_t reg, uint8_t *value);

#define READ_SC16IS75X_REG(dev, reg, val)                                    \
	mfd_sc16is75x_read_register((dev), 0, SC16IS75X_REG_##reg, (val));

#define READ_SC16IS75X_CHREG(dev, ch, reg, val)                              \
	mfd_sc16is75x_read_register((dev), (ch), SC16IS75X_REG_##reg, (val));

/**
 * @brief Write to an internal register.
 *
 * @param dev An SC16IS75x device.
 * @param channel Channel to access.
 * @param reg Register address to write to.
 * @param value Value to be written.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int mfd_sc16is75x_write_register(const struct device *dev,
				 const uint8_t channel,
				 const uint8_t reg, const uint8_t value);

#define WRITE_SC16IS75X_REG(dev, reg, val)                                   \
	mfd_sc16is75x_write_register((dev), 0, SC16IS75X_REG_##reg, (val));

#define WRITE_SC16IS75X_CHREG(dev, ch, reg, val)                             \
	mfd_sc16is75x_write_register((dev), (ch), SC16IS75X_REG_##reg, (val));

/**
 * @brief Enable or disable a bit in an internal register.
 *
 * @param dev An SC16IS75x device.
 * @param channel Channel to access.
 * @param reg Register address to change the bit.
 * @param bit Bit number to change.
 * @param value Value to be written (true = set to one, false = set to zero).
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int mfd_sc16is75x_set_register_bit(const struct device *dev,
				   const uint8_t channel, const uint8_t reg,
				   const uint8_t bit, const bool value);

#define SETBIT_SC16IS75X_REG(dev, reg, bit, val)                             \
	mfd_sc16is75x_set_register_bit((dev), 0, SC16IS75X_REG_##reg,        \
						 (bit), (val));

#define SETBIT_SC16IS75X_CHREG(dev, ch, reg, bit, val)                       \
	mfd_sc16is75x_set_register_bit((dev), (ch), SC16IS75X_REG_##reg,     \
						    (bit), (val));

/**
 * @brief Read data from FIFO.
 *
 * @param dev An SC16IS75x device.
 * @param channel Channel whose FIFO to read.
 * @param[out] buf Data read from FIFO.
 * @param len Number of bytes to read.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int mfd_sc16is75x_read_fifo(const struct device *dev, const uint8_t channel,
			    uint8_t *buf, const size_t len);

/**
 * @brief Write data to FIFO.
 *
 * @param dev An SC16IS75x device.
 * @param channel Channel whose FIFO to read.
 * @param buf Data to be written.
 * @param len Number of bytes to write.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int mfd_sc16is75x_write_fifo(const struct device *dev, const uint8_t channel,
			     const uint8_t *buf, const size_t len);

#ifdef CONFIG_MFD_SC16IS75X_ASYNC

/**
 * @brief Read from an internal register asynchronously.
 *
 * @param dev An SC16IS75x device.
 * @param channel Channel to access.
 * @param reg Register address to read from.
 * @param[out] value Value of that register.
 * @retval 0 On succes.
 * @return Negative error code on failure.
 */
int mfd_sc16is75x_read_register_signal(const struct device *dev,
				       const uint8_t channel,
				       const uint8_t reg, uint8_t *value,
				       struct k_poll_signal *signal);

#define READ_SC16IS75X_CHREG_SIGNAL(dev, ch, reg, val, signal)               \
	mfd_sc16is75x_read_register_signal((dev), (ch), SC16IS75X_REG_##reg, \
							(val), (signal));

#endif /* CONFIG_MFD_SC16IS75X_ASYNC */

#ifdef CONFIG_MFD_SC16IS75X_INTERRUPTS

/**
 * @brief Emitted event bits.
 *
 * These values should be used with the @ref event callback functions.
 *
 * - @c UART0 and @c UART1 means UART channel 0/1 (A/B).
 * - @c IO0 and @c IO1 means GPIO, the underlying GPIO driver should
 *   decide for itself whether it needs this channel separation or not.
 */
enum mfd_sc16is75x_event {
	/* channel 0 (A) */
	SC16IS75X_EVENT_UART0_RXLSE, /**< RX0 Line Status Error in LSR0 */
	SC16IS75X_EVENT_UART0_RXTO,  /**< RX0 Break/Time-Out, TLR0 underrun */
	SC16IS75X_EVENT_UART0_RHRI,  /**< RX0 FIFO (RHR0), RXLVL0 > TLR0 */
	SC16IS75X_EVENT_UART0_THRI,  /**< TX0 FIFO (THR0), TXLVL0 < TLR0 */
	SC16IS75X_EVENT_UART0_MSI,   /**< Modem Status in MSR0 */
	SC16IS75X_EVENT_IO0_STATE,   /**< I/O Pin in IOSTATE0 */
	SC16IS75X_EVENT_UART0_XOFF,  /**< Xoff char from XOFF0 seen */
	SC16IS75X_EVENT_UART0_HWFL,  /**< RTS0 or CTS0 change seen */
	/* channel 1 (B) */
	SC16IS75X_EVENT_UART1_RXLSE, /**< RX1 Line Status Error in LSR1 */
	SC16IS75X_EVENT_UART1_RXTO,  /**< RX1 Break/Time-Out, TLR1 underrun */
	SC16IS75X_EVENT_UART1_RHRI,  /**< RX1 FIFO (RHR1), RXLVL1 > TLR1 */
	SC16IS75X_EVENT_UART1_THRI,  /**< TX1 FIFO (THR1), TXLVL1 < TLR1 */
	SC16IS75X_EVENT_UART1_MSI,   /**< Modem Status in MSR1 */
	SC16IS75X_EVENT_IO1_STATE,   /**< I/O Pin in IOSTATE1 */
	SC16IS75X_EVENT_UART1_XOFF,  /**< Xoff char from XOFF1 seen */
	SC16IS75X_EVENT_UART1_HWFL,  /**< RTS1 or CTS1 change seen */
	/* must be last entry */
	SC16IS75X_EVENT_MAX
};

/**
 * @brief Add an event callback
 *
 * @param dev An SC16IS75x device.
 * @param callback The child callback to add.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int mfd_sc16is75x_add_callback(const struct device *dev,
			       struct gpio_callback *callback);

/**
 * @brief Remove an event callback
 *
 * @param dev An SC16IS75x device.
 * @param callback The child callback to remove.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int mfd_sc16is75x_remove_callback(const struct device *dev,
				  struct gpio_callback *callback);


#endif /* CONFIG_MFD_SC16IS75X_INTERRUPTS */

/** @} */

#ifdef __cplusplus
}
#endif

#endif /* ZEPHYR_INCLUDE_DRIVERS_MFD_SC16IS75X_H_ */
