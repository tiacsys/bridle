/*
 * Copyright (c) 2025 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef ZEPHYR_DRIVERS_MFD_SC18IS604_EMUL_H_
#define ZEPHYR_DRIVERS_MFD_SC18IS604_EMUL_H_

#include <stdint.h>
#include <stddef.h>
#include <zephyr/drivers/emul.h>

#define SC18IS604_BUFFER_SIZE 255

struct mfd_sc18is604_emul_transmission {
	uint8_t addr;
	uint8_t msg[SC18IS604_BUFFER_SIZE];
	size_t len;
};

/**
 * @brief Simulate the device receiving a message. The message will be moved to the RX buffer the
 * next time a read is performed.
 *
 * @param target The emulated device to receive the message.
 * @param buf The message to receive.
 * @param len The length of the message.
 *
 * @return The number of bytes received, or a negative error code on failure.
 */
int mfd_sc18is604_emul_i2c_set_rx(const struct emul *target, uint8_t *buf, size_t len);

/**
 * @brief Get the last transmission sent by the device.
 *
 * @param target The amulated device to get the last transmission from.
 * @param[out] transmission The transmission to fill with the last transmission.
 *
 * @retval 0 On success
 * @return A negative error code on failure.
 */
int mfd_sc18is604_emul_i2c_get_last_tx(const struct emul *target,
				       struct mfd_sc18is604_emul_transmission *transmission);

/**
 * @brief Simulate a GPIO input pin being set to a specific value.
 *
 * @param target The emulated device to set the pin on.
 * @param pin The pin to set.
 * @param value The value to set the pin to.
 *
 * @return 0 On success.
 * @return A negative error code on failure.
 */
int mfd_sc18is604_emul_gpio_set_input(const struct emul *target, uint8_t pin, uint8_t value);

/**
 * @brief Get the value of a GPIO output pin.
 *
 * @param target The emulated device to get the pin value from.
 * @param pin The pin to get the value of.
 * @param[out] value The value of the pin.
 *
 * @return 0 On success.
 * @return A negative error code on failure.
 */
int mfd_sc18is604_emul_gpio_get_output(const struct emul *target, uint8_t pin, uint8_t *value);

#endif /* ZEPHYR_DRIVERS_MFD_SC18IS604_EMUL_H_ */
