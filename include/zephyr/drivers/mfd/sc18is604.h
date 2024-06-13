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
#include <zephyr/drivers/gpio.h>

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
 * @brief Perform a data transfer to and from an SC18IS604 device.
 *
 * @param dev An SC18IS604 MFD device.
 * @param cmd A command sequence sent before the TX data. Can be NULL, in which
 *            case no command sequence is sent).
 * @param cmd_len Length of the command sequence.
 * @param tx_data Data to be sent to the device. Can be NULL, in which case no
 *                data is send).
 * @param tx_len Length of the TX data buffer.
 * @param[out] rx_data Buffer to hold data received from the device. Can be
 *                     NULL, in which case no data is received.
 * @param rx_len Length of the RX data buffer.
 *
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
 *
 * @return A value from mfd_sc18is604_transfer().
 */
int mfd_sc18is604_read_register(const struct device *dev,
				uint8_t reg, uint8_t *val);

#define READ_SC18IS604_REG(dev, reg, val)                                    \
	mfd_sc18is604_read_register((dev), SC18IS604_REG_##reg, (val));

/**
 * @brief Read from an internal register.
 *
 * @param dev An SC18IS604 MFD device.
 * @param reg Register address to read from.
 * @param[out] value Value read from the register.
 *
 * @return A value from mfd_sc18is604_transfer().
 */
int mfd_sc18is604_write_register(const struct device *dev,
				 uint8_t reg, uint8_t val);

#define WRITE_SC18IS604_REG(dev, reg, val)                                   \
	mfd_sc18is604_write_register((dev), SC18IS604_REG_##reg, (val));

/**
 * @brief Read data from the internal buffer of an SC18IS604.
 *
 * @param dev An SC18IS604 MFD device.
 * @param[out] data Data read from the buffer.
 * @param len Number of bytes to read from the buffer.
 *
 * @return A value from mfd_sc18is604_transfer().
 */
int mfd_sc18is604_read_buffer(const struct device *dev,
			      uint8_t *data, size_t len);

/**
 * @brief Register an interrupt callback.
 *
 * @param dev An SC18IS604 device
 * @param callback The callback to add.
 *
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int mfd_sc18is604_add_callback(const struct device *dev,
			       struct gpio_callback *callback);

/**
 * @brief Remove a previously registered interrupt callback.
 *
 * @param dev An SC18IS604 device
 * @param callback The callback to remove.
 *
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int mfd_sc18is604_remove_callback(const struct device *dev,
				  struct gpio_callback *callback);

/**
 * @brief Claim a lock on an SC18IS604 device, preventing other users from
 *        accessing the device until the lock is released.
 *
 * @param dev The SC18IS604 MFD device to be locked.
 * @param timeout Timeout after which trying to claim the device is aborted.
 *
 * @return A value from k_sem_take.
 */
int mfd_sc18is604_claim(const struct device *dev, k_timeout_t timeout);

/**
 * @brief Release a previously acquired lock on an SC18IS604 device.
 *
 * @param dev The SC18IS604 MFD device to be unlocked.
 */
void mfd_sc18is604_release(const struct device *dev);

#ifdef CONFIG_MFD_SC18IS604_ASYNC

/**
 * @brief Asynchronously transfer data to and from an SC18IS604 device. This is
 *        the most general transfer routine, all other transfer variants are
 *        implemented in terms of this one.
 *
 * @param dev An SC18IS604 MFD device.
 * @param cmd A command sequence sent before the TX data. Can be NULL, in which
 *            case no command sequence is sent).
 * @param cmd_len Length of the command sequence.
 * @param tx_data Data to be sent to the device. Can be NULL, in which case no
 *                data is send).
 * @param tx_len Length of the TX data buffer.
 * @param[out] rx_data Buffer to hold data received from the device. Can be
 *                     NULL, in which case no data is received.
 * @param rx_len Length of the RX data buffer.
 * @param signal Signal to be raised once the transfer is complete.
 *
 * @retval 0 If the transfer was successfully started.
 * @return Negative error code on failure.
 */
int mfd_sc18is604_transfer_signal(const struct device *dev,
				  uint8_t *cmd, size_t cmd_len,
				  uint8_t *tx_data, size_t tx_len,
				  uint8_t *rx_data, size_t rx_len,
				  struct k_poll_signal *signal);

/**
 * @brief Read from an internal register asychronously.
 *
 * @param dev An SC18IS604 MFD device.
 * @param reg Register address to read from.
 * @param[out] value Value read from the register. Pointer must remain valid
 *                   until the transfer is complete.
 * @param signal Signal that will be raised on transfer completion. Pointer
 *               must remain valid until the transfer is complete.
 *
 * @return A value from mfd_sc18is604_transfer_signal().
 */
int mfd_sc18is604_read_register_signal(const struct device *dev,
				       uint8_t reg, uint8_t *val,
				       struct k_poll_signal *signal);

#define READ_SC18IS604_REG_SIGNAL(dev, reg, val, signal)                     \
	mfd_sc18is604_read_register_signal((dev), SC18IS604_REG_##reg,       \
						  (val), (signal));

/**
 * @brief Read data from the internal buffer of an SC18IS604 asynchronously.
 *
 * @param dev An SC18IS604 MFD device.
 * @param[out] data Data read from the buffer. Pointer must remain valid until
 *                  the transfer is complete.
 * @param len Number of bytes to read from the buffer.
 * @param signal Signal that will be raised on transfer completion. Pointer
 *               must remain valid until the transfer is complete.
 *
 * @return A value from mfd_sc18is604_transfer().
 */
int mfd_sc18is604_read_buffer_signal(const struct device *dev,
				     uint8_t *data, size_t len,
				     struct k_poll_signal *signal);

#endif /* CONFIG_MFD_SC18IS604_ASYNC */

/** @} */

#ifdef __cplusplus
}
#endif

#endif /* ZEPHYR_INCLUDE_DRIVERS_MFD_SC18IS604_H_ */
