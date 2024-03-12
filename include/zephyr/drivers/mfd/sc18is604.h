/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef ZEPHYR_INCLUDE_DRIVERS_MFD_SC18IS604_H_
#define ZEPHYR_INCLUDE_DRIVERS_MFD_SC18IS604_H_

#ifdef __cplusplus
extern "C" {
#endif

#include <stddef.h>
#include <stdint.h>

#include <zephyr/device.h>
#include <zephyr/kernel.h>

#define SC18IS604_CMD_WRITE_I2C			0x00
#define SC18IS604_CMD_READ_I2C			0x01
#define SC18IS604_CMD_READ_AFTER_WRITE_I2C	0x02
#define SC18IS604_CMD_WRITE_AFTER_WRITE_I2C	0x03
#define SC18IS604_CMD_READ_BUFFER		0x06
#define SC18IS604_CMD_SPI_CONFIG		0x18
#define SC18IS604_CMD_WRITE_REGISTER		0x20
#define SC18IS604_CMD_READ_REGISTER		0x21
#define SC18IS604_CMD_POWER_DOWN		0x30
#define SC18IS604_CMD_POWER_DOWN_KEY1		0x5A
#define SC18IS604_CMD_POWER_DOWN_KEY2		0xA5
#define SC18IS604_CMD_VERSION_STRING		0xFE

#define SC18IS604_VERSION_STRING_SIZE		16

#define SC18IS604_REG_IO_CONFIG			0x00
#define SC18IS604_REG_IO_STATE			0x01
#define SC18IS604_REG_I2C_CLOCK			0x02
#define SC18IS604_REG_I2C_TIMEOUT		0x03
#define SC18IS604_REG_I2C_STATUS		0x04
#define SC18IS604_REG_I2C_ADDRESS		0x05

#define SC18IS604_IO_NUM_PINS_INOUT		4
#define SC18IS604_IO_NUM_PINS_IONLY		1
#define SC18IS604_IO_NUM_PINS_MAX		(SC18IS604_IO_NUM_PINS_INOUT \
						+ SC18IS604_IO_NUM_PINS_IONLY)

#define SC18IS604_IO_CONFIG_INPUT		0b00
#define SC18IS604_IO_CONFIG_PUSH_PULL		0b10
#define SC18IS604_IO_CONFIG_OPEN_DRAIN		0b11

#define SC18IS604_I2C_STATUS_SUCCESS		0xF0
#define SC18IS604_I2C_STATUS_DEVICE_ADDR_NACK	0xF1
#define SC18IS604_I2C_STATUS_BYTE_NACK		0xF2
#define SC18IS604_I2C_STATUS_BUSY		0xF3

#define SC18IS604_I2C_CLOCK_99KHZ		19
#define SC18IS604_I2C_CLOCK_375KHZ		5

/**
 * @defgroup mfd_interface_sc18is604 MFD SC18IM604 Interface
 * @ingroup mfd_interfaces
 * @{
 */

/**
 * @brief Claim a lock on an SC18IS604 device, preventing other threads
 *        from interfacing with the device until the lock is released.
 *
 * @param dev The SC18IS604 MFD device to be locked.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int mfd_sc18is604_claim(const struct device *dev);

/**
 * @brief Release a previously acquired lock on an SC18IS604 device.
 *
 * @param dev The SC18IS604 MFD device to be unlocked.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int mfd_sc18is604_release(const struct device *dev);

/**
 * @brief Get the semaphore signaling that an interrupt has been raised.
 *
 * @param dev An SC18IS604 MFD device.
 * @return A pointer to the interrupt semaphore.
 */
struct k_sem *mfd_sc18is604_interrupt_sem_get(const struct device *dev);

/**
 * @brief Transfer data to and from an SC18IS604 device.
 *
 * @param dev An SC18IS604 MFD device.
 * @param cmd A command sequence sent before the TX data.
 *            Can be NULL, in which case no command sequence is sent).
 * @param cmd_len Length of the command sequence.
 * @param tx_data Data to be sent to the device.
 *                Can be NULL, in which case no data is send).
 * @param tx_len Length of the TX data buffer.
 * @param[out] rx_data Buffer to hold data received from the device.
 *                     Can be NULL, in which case no data is received.
 * @param rx_len Length of the RX data buffer.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int mfd_sc18is604_transfer(const struct device *dev,
			   uint8_t *cmd, size_t cmd_len,
			   uint8_t *tx_data, size_t tx_len,
			   uint8_t *rx_data, size_t rx_len);

/**
 * @brief Write to an internal register.
 *
 * @param dev An SC18IS604 MFD device.
 * @param reg Register address to write to.
 * @param value Value to write into the register.
 * @return A value from mfd_sc18is604_transfer().
 */
int mfd_sc18is604_write_register(const struct device *dev,
				 uint8_t reg, uint8_t value);

/**
 * @brief Read from an internal register.
 *
 * @param dev An SC18IS604 MFD device.
 * @param reg Register address to read from.
 * @param[out] value Value read from the register.
 * @return A value from mfd_sc18is604_transfer().
 */
int mfd_sc18is604_read_register(const struct device *dev,
				uint8_t reg, uint8_t *value);

/**
 * @brief Read data from the internal buffer of an SC18IS604.
 *
 * @param dev An SC18IS604 MFD device.
 * @param[out] data Data read from the buffer.
 * @param len Number of bytes to read from the buffer.
 * @return A value from mfd_sc18is604_transfer().
 */
int mfd_sc18is604_read_buffer(const struct device *dev,
			      uint8_t *data, size_t len);

/** @} */

#ifdef __cplusplus
}
#endif

#endif /* ZEPHYR_INCLUDE_DRIVERS_MFD_SC18IS604_H_ */
