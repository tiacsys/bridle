/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef SC16IS75X_H
#define SC16IS75X_H

#include <zephyr/kernel.h>
#include <zephyr/drivers/spi.h>
#include <zephyr/drivers/i2c.h>
#include <zephyr/drivers/gpio.h>

/* General registers */
#define SC16IS75X_REG_RHR 0x00
#define SC16IS75X_REG_THR 0x00
#define SC16IS75X_REG_IER 0x01
#define SC16IS75X_REG_FCR 0x02
#define SC16IS75X_REG_IIR 0x02
#define SC16IS75X_REG_LCR 0x03
#define SC16IS75X_REG_MCR 0x04
#define SC16IS75X_REG_LSR 0x05
#define SC16IS75X_REG_MSR 0x06
#define SC16IS75X_REG_SPR 0x07
#define SC16IS75X_REG_TCR 0x06
#define SC16IS75X_REG_TLR 0x07
#define SC16IS75X_REG_TXLVL 0x08
#define SC16IS75X_REG_RXLVL 0x09

#define SC16IS75X_REG_IODIR 0x0a
#define SC16IS75X_REG_IOSTATE 0x0b
#define SC16IS75X_REG_IOINTENA 0x0c
#define SC16IS75X_REG_IOCONTROL 0x0e

#define SC16IS75X_REG_EFCR 0x0f

/* Special registers */
#define SC16IS75X_REG_DLL 0x00
#define SC16IS75X_REG_DLH 0x01

/* Enhanced registers */
#define SC16IS75X_REG_EFR 0x02
#define SC16IS75X_REG_XON1 0x04
#define SC16IS75X_REG_XON2 0x05
#define SC16IS75X_REG_XOFF1 0x06
#define SC16IS75X_REG_XOFF2 0x07

/* Parity settings */
#define SC16IS75X_PARITY_NONE 0b000
#define SC16IS75X_PARITY_ODD 0b001
#define SC16IS75X_PARITY_EVEN 0b011
#define SC16IS75X_PARITY_MARK 0b101
#define SC16IS75X_PARITY_SPACE 0b111

/* Word length settings */
#define SC16IS75X_WORD_LEN_5 0b00
#define SC16IS75X_WORD_LEN_6 0b01
#define SC16IS75X_WORD_LEN_7 0b10
#define SC16IS75X_WORD_LEN_8 0b11

/* Interrupt types */
#define SC16IS75X_INT_RX_TIMEOUT 0b001100
#define SC16IS75X_INT_RHR 0b000100
#define SC16IS75X_INT_THR 0b000010
#define SC16IS75X_INT_MODEM_STATUS 0b000000
#define SC16IS75X_INT_IO 0b110000
#define SC16IS75X_INT_XOFF 0b010000
#define SC16IS75X_INT_CTS_RTS 0b100000

/* IO control bits */
#define SC16IS75X_BIT_IOCONTROL_IOLATCH 0
#define SC16IS75X_BIT_IOCONTROL_MODEM_PINS 1
#define SC16IS75X_BIT_IOCONTROL_SRESET 3

/* FIFO parameters */
#define SC16IS75X_FIFO_CAPACITY 64

/** @brief Check device readiness.
 * @param dev An SC16IS75x device.
 * @retval true if the device is ready.
 * @retval false if the device is not ready.
 */
bool sc16is75x_is_ready(const struct device *dev);

/** @brief Read from an internal register.
 * @param dev An SC16IS75x device.
 * @param channel Channel to access.
 * @param reg Register address to read from.
 * @param[out] value Value of that regiser.
 * @retval 0 On succes.
 * @return Negative error code on failure.
 */
int sc16is75x_read_register(const struct device *dev, uint8_t channel, uint8_t reg, uint8_t *value);

/** @brief Write to an internal register.
 * @param dev An SC16IS75x device.
 * @param reg Register address to write to.
 * @param channel Channel to access.
 * @param value Value to be written.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int sc16is75x_write_register(const struct device *dev, uint8_t channel, uint8_t reg, uint8_t value);

/** @brief Read data from FIFO.
 * @param dev An SC16IS75x device.
 * @param channel Channel whose FIFO to read.
 * @param[out] data Data read from FIFO.
 * @param len Number of bytes to read.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int sc16is75x_read_fifo(const struct device *dev, uint8_t channel, uint8_t *data, size_t len);

/** @brief Write data to FIFO.
 * @param dev An SC16IS75x device.
 * @param channel Channel whose FIFO to read.
 * @param data Data to be written.
 * @param len Number of bytes to write.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int sc16is75x_write_fifo(const struct device *dev, uint8_t channel, uint8_t *data, size_t len);

/** @brief Read interrupt type.
 * @param dev An SC16IS75x device.
 * @param channel Channel whose interrupt type to read.
 * @param[out] type Type of the currently set interrupt.
 * @retval 0 On success.
 * @return Negative error code on failure. 
 */
int sc16is75x_read_interrupt_type(const struct device *dev, uint8_t channel, uint8_t *type);

#endif // SC16IS75X_H
