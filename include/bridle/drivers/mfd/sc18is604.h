/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef SC18IS604_H
#define SC18IS604_H

#include <zephyr/device.h>
#include <zephyr/kernel.h>

#define SC18IS604_CMD_WRITE_I2C 0x00
#define SC18IS604_CMD_READ_I2C 0x01
#define SC18IS604_CMD_READ_AFTER_WRITE_I2C 0x02
#define SC18IS604_CMD_WRITE_AFTER_WRITE_I2C 0x03
#define SC18IS604_CMD_READ_BUFFER 0x06
#define SC18IS604_CMD_SPI_CONFIG 0x18
#define SC18IS604_CMD_WRITE_INTERNAL 0x20
#define SC18IS604_CMD_READ_INTERNAL 0x21
#define SC18IS604_CMD_POWER_DOWN 0x30
#define SC18IS604_CMD_VERSION_STRING 0xfe

#define SC18IS604_REG_IO_CONFIG 0x00
#define SC18IS604_REG_IO_STATE 0x01
#define SC18IS604_REG_I2C_CLOCK 0x02
#define SC18IS604_REG_I2C_TIMEOUT 0x03
#define SC18IS604_REG_I2C_STATUS 0x04
#define SC18IS604_REG_I2C_ADDRESS 0x05

#define SC18IS604_IO_CONFIG_INPUT 0b00
#define SC18IS604_IO_CONFIG_PUSH_PULL 0b10
#define SC18IS604_IO_CONFIG_OPEN_DRAIN 0b11

#define SC18IS604_I2C_STATUS_SUCCESS 0xf0
#define SC18IS604_I2C_STATUS_DEVICE_ADDR_NACK 0xf1
#define SC18IS604_I2C_STATUS_BYTE_NACK 0xf2
#define SC18IS604_I2C_STATUS_BUSY 0xf3

#define SC18IS604_I2C_CLOCK_99KHZ 19
#define SC18IS604_I2C_CLOCK_375KHZ 5

/** @brief Check device readiness.
 * @param dev An SC18IS604 device.
 * @retval true if the device is ready.
 * @retval false if the device is not ready.
 */
bool sc18is604_is_ready(const struct device *dev);

/** @brief Claim a lock on an SC18IS604 device, preventing other threads
 *         from interfacing with the device until the lock is released.
 * @param dev The SC18IS604 device to be locked.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int sc18is604_claim(const struct device *dev);

/** @brief Release a previously acquired lock on an SC18IS604 device.
 * @param dev The SC18IS604 device to be unlocked.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int sc18is604_release(const struct device *dev);

/** @brief Get the semaphore signaling that an interrupt has been raised.
 * @param dev An SC18IS604 device.
 * @return A pointer to the interrupt semaphore.
 */
struct k_sem *sc18is604_interrupt_sem_get(const struct device *dev);

/** @brief Transfer data to and from an SC18IS604 device.
 * @param cmd A command sequence sent before the TX data. Can be NULL, in which case no command sequence is sent).
 * @param cmd_len Length of the command sequence.
 * @param tx_data Data to be sent to the device. Can be NULL, in which case no data is send).
 * @param tx_len Length of the TX data buffer.
 * @param[out] rx_data Buffer to hold data received from the device. Can be NULL, in which case no data is received.
 * @param rx_len Length of the RX data buffer.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int sc18is604_transfer(const struct device *dev, uint8_t *cmd, size_t cmd_len, uint8_t *tx_data, size_t tx_len, uint8_t *rx_data, size_t rx_len);

/** @brief Write to an internal register.
 * @param dev An SC18IS604 device.
 * @param reg Register address to write to.
 * @param value Value to write into the register.
 * @return A value from sc18is604_transfer().
 */
int sc18is604_write_internal_register(const struct device *dev, uint8_t reg, uint8_t value);

/** @brief Read from an internal register.
 * @param dev An SC18IS604 device.
 * @param reg Register address to read from.
 * @param[out] value Value read from the register.
 * @return A value from sc18is604_transfer().
 */
int sc18is604_read_internal_register(const struct device *dev, uint8_t reg, uint8_t *value);

/** @brief Read data from the internal buffer of an SC18IS604.
 * @param dev An SC18IS604 device.
 * @param[out] data Data read from the buffer.
 * @param len Number of bytes to read from the buffer.
 * @return A value from sc18is604_transfer().
 */
int sc18is604_read_buffer(const struct device *dev, uint8_t *data, size_t len);

/** @brief Request device version string. The string will be placed in the
 *         internal buffer. The device interrupt is set once the string is ready
 *         to be read from the buffer.
 * @param dev An SC18IS604 device.
 * @return A value from sc18is604_transfer().
 */
int sc18is604_request_version_string(const struct device *dev);

#endif // SC18IS604_H
