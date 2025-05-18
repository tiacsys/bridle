/*
 * Copyright (c) 2023 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief MFD Interface for an SIPO/MUX GP matrix controller
 */

#ifndef ZEPHYR_INCLUDE_DRIVERS_MFD_SIPOMUXGP_H_
#define ZEPHYR_INCLUDE_DRIVERS_MFD_SIPOMUXGP_H_

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief    MFD interface for an generic latched SIPO/MUX GP matrix controller
 * @defgroup mdf_interface_sipomuxgp SIPO/MUX GP MFD Interface
 * @ingroup  mfd_interfaces
 * @since    3.6
 * @version  1.0.0
 *
 * The MFD interface for an generic latched SIPO/MUX General Purpose (GP)
 * matrix controller.
 *
 * @par SIPO/MUX:
 * Serial Input Parallel Output / Multiplexing hardware
 *
 * @{
 */

#include <stddef.h>
#include <stdint.h>

#include <zephyr/device.h>

/**
 * @brief Get number of available bits from SIPO/MUX GP
 *
 * @param dev sipomuxgp mfd device
 * @retval num_bits Number of bits
 */
int mfd_sipomuxgp_num_bits(const struct device *dev);

/**
 * @brief Read 32 bits from SIPO/MUX GP
 *
 * @param dev sipomuxgp mfd device
 * @param offs Offset number where starting to read bits
 * @param val Pointer to buffer for exactly 32-bit data
 * @retval 0 If successful
 * @retval -errno In case of any error
 */
int mfd_sipomuxgp_bits(const struct device *dev, size_t offs, uint32_t *val);

/**
 * @brief Write logical one to a single bit on SIPO/MUX GP
 *
 * @param dev sipomuxgp mfd device
 * @param bit Number of the bit where to write logical one
 * @retval 0 If successful
 * @retval -errno In case of any error
 */
int mfd_sipomuxgp_bit_on(const struct device *dev, size_t bit);

/**
 * @brief Write logical zero to a single bit on SIPO/MUX GP
 *
 * @param dev sipomuxgp mfd device
 * @param bit Number of the bit where to write logical zero
 * @retval 0 If successful
 * @retval -errno In case of any error
 */
int mfd_sipomuxgp_bit_off(const struct device *dev, size_t bit);

/**
 * @brief Write logical one to a single XY position on SIPO/MUX GP
 *
 * @param dev sipomuxgp mfd device
 * @param x Number of the X coordinate where to write logical one
 * @param y Number of the Y coordinate where to write logical one
 * @retval 0 If successful
 * @retval -errno In case of any error
 */
int mfd_sipomuxgp_xy_on(const struct device *dev, size_t x, size_t y);

/**
 * @brief Write logical zero to a single XY position on SIPO/MUX GP
 *
 * @param dev sipomuxgp mfd device
 * @param x Number of the X coordinate where to write logical zero
 * @param y Number of the Y coordinate where to write logical zero
 * @retval 0 If successful
 * @retval -errno In case of any error
 */
int mfd_sipomuxgp_xy_off(const struct device *dev, size_t x, size_t y);

/**
 * @brief Change ratio of SIPO/MUX GP output enable signal
 *
 * The percentage value affects the duty cycle of the outgoing data.
 * If the matrix is used to drive LEDs, for example, this affects the
 * brightness.
 *
 * Only three ratios are supported due to the time critical design:
 *
 *     - full force (100%), or
 *     - half force (50%), or
 *     - none (0%)
 *
 * @param dev sipomuxgp mfd device
 * @param percent Percentage ratio of the ON phase
 * @retval 0 If successful
 * @retval -errno In case of any error
 */
int mfd_sipomuxgp_output_ratio(const struct device *dev, uint8_t percent);

/** @} */

#ifdef __cplusplus
}
#endif

#endif /* ZEPHYR_INCLUDE_DRIVERS_MFD_SIPOMUXGP_H_ */
