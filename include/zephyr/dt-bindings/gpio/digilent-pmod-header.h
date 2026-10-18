/*
 * SPDX-FileCopyrightText: Copyright (c) 2023-2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief Digilent Pmod header pin constants
 * @ingroup digilent-pmod-header
 */

#ifndef ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_DIGILENT_PMOD_HEADER_H_
#define ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_DIGILENT_PMOD_HEADER_H_

/**
 * @defgroup digilent-pmod-header Digilent Pmod header
 * @brief Constants for pins exposed on Digilent Pmod header
 * @ingroup devicetree-gpio-pin-headers
 * @{
 */

#define PMOD_1_IO1  0 /**< Pin 1: GPIO in-/output 0 */
#define PMOD_1_IO2  1 /**< Pin 2: GPIO in-/output 1 (PWM) */
#define PMOD_1_IO3  2 /**< Pin 3: GPIO in-/output 2 */
#define PMOD_1_IO4  3 /**< Pin 4: GPIO in-/output 3 */
#define PMOD_1A_IO5 4 /**< Pin 7: GPIO in-/output 4 */
#define PMOD_1A_IO6 5 /**< Pin 8: GPIO in-/output 5 (PWM) */
#define PMOD_1A_IO7 6 /**< Pin 9: GPIO in-/output 6 */
#define PMOD_1A_IO8 7 /**< Pin 10: GPIO in-/output 7 */

#define PMOD_2_CS     0 /**< Pin 1: SPI CS */
#define PMOD_2_MOSI   1 /**< Pin 2: SPI MOSI */
#define PMOD_2_MISO   2 /**< Pin 3: SPI MISO */
#define PMOD_2_SCK    3 /**< Pin 4: SPI SCK */
#define PMOD_2A_INT   4 /**< Pin 7: SPI device interrupt */
#define PMOD_2A_RESET 5 /**< Pin 8: SPI device reset */
#define PMOD_2A_CS2   6 /**< Pin 9: SPI device chip select 2 */
#define PMOD_2A_CS3   7 /**< Pin 10: SPI device chip select 3 */
#define PMOD_2A_IO5   4 /**< Pin 7: GPIO in-/output 4 (INT) */
#define PMOD_2A_IO6   5 /**< Pin 8: GPIO in-/output 5 (RESET) */
#define PMOD_2A_IO7   6 /**< Pin 9: GPIO in-/output 6 (CS2) */
#define PMOD_2A_IO8   7 /**< Pin 10: GPIO in-/output 7 (CS3) */

#define PMOD_3_IO1    0 /**< Pin 1: GPIO in-/output 0 (CTS) */
#define PMOD_3_CTS    0 /**< Pin 1: UART host is clear to send */
#define PMOD_3_TXD    1 /**< Pin 2: UART host transmit data */
#define PMOD_3_RXD    2 /**< Pin 3: UART host receive data */
#define PMOD_3_RTS    3 /**< Pin 4: UART host request to send */
#define PMOD_3_IO4    3 /**< Pin 4: GPIO in-/output 3 (RTS) */
#define PMOD_3A_INT   4 /**< Pin 7: UART device interrupt */
#define PMOD_3A_RESET 5 /**< Pin 8: UART device reset */
#define PMOD_3A_IO5   4 /**< Pin 7: GPIO in-/output 4 (INT) */
#define PMOD_3A_IO6   5 /**< Pin 8: GPIO in-/output 5 (RESET) */
#define PMOD_3A_IO7   6 /**< Pin 9: GPIO in-/output 6 */
#define PMOD_3A_IO8   7 /**< Pin 10: GPIO in-/output 7 */

#define PMOD_4_DIR 0 /**< Pin 1: H-Bridge motor direction */
#define PMOD_4_EN  1 /**< Pin 2: H-Bridge motor enable (PWM) */
#define PMOD_4_SA  2 /**< Pin 3: H-Bridge motor feedback sense A */
#define PMOD_4_SB  3 /**< Pin 4: H-Bridge motor feedback sense B */

#define PMOD_5_DIR1 0 /**< Pin 1: Dual H-Bridge motor/phase 1 direction */
#define PMOD_5_EN1  1 /**< Pin 2: Dual H-Bridge motor/phase 1 enable */
#define PMOD_5_DIR2 2 /**< Pin 3: Dual H-Bridge motor/phase 1 direction */
#define PMOD_5_EN2  3 /**< Pin 4: Dual H-Bridge motor/phase 1 enable */

#define PMOD_5A_DIR1 0 /**< Pin 1: Dual H-Bridge motor 1 direction */
#define PMOD_5A_EN1  1 /**< Pin 2: Dual H-Bridge motor 1 enable (PWM) */
#define PMOD_5A_SA1  2 /**< Pin 3: Dual H-Bridge motor 1 feedback sense A */
#define PMOD_5A_SB1  3 /**< Pin 4: Dual H-Bridge motor 1 feedback sense B */
#define PMOD_5A_DIR2 4 /**< Pin 7: Dual H-Bridge motor 2 direction */
#define PMOD_5A_EN2  5 /**< Pin 8: Dual H-Bridge motor 2 enable (PWM) */
#define PMOD_5A_SA2  6 /**< Pin 9: Dual H-Bridge motor 2 feedback sense A */
#define PMOD_5A_SB2  7 /**< Pin 10: Dual H-Bridge motor 2 feedback sense B */

#define PMOD_6_IO1   0 /**< Pin 7: GPIO in-/output 0 (INT) */
#define PMOD_6_IO2   1 /**< Pin 8: GPIO in-/output 1 (RESET) */
#define PMOD_6_INT   0 /**< Pin 7: I2C device interrupt */
#define PMOD_6_RESET 1 /**< Pin 8: I2C device reset */
#define PMOD_6_SCL   2 /**< Pin 3: I2C serial clock */
#define PMOD_6_SDA   3 /**< Pin 4: I2C serial data */

#define PMOD_6A_IO1   0 /**< Pin 7: GPIO in-/output 0 (INT) */
#define PMOD_6A_IO2   1 /**< Pin 8: GPIO in-/output 1 (RESET) */
#define PMOD_6A_INT   0 /**< Pin 7: I2C device interrupt */
#define PMOD_6A_RESET 1 /**< Pin 8: I2C device reset */
#define PMOD_6A_SCL   2 /**< Pin 3: I2C serial clock */
#define PMOD_6A_SDA   3 /**< Pin 4: I2C serial data */
#define PMOD_6A_IO5   4 /**< Pin 7: GPIO in-/output 4 */
#define PMOD_6A_IO6   5 /**< Pin 8: GPIO in-/output 5 */
#define PMOD_6A_IO7   6 /**< Pin 9: GPIO in-/output 6 */
#define PMOD_6A_IO8   7 /**< Pin 10: GPIO in-/output 7 */

#define PMOD_7_LRCLK 0 /**< Pin 1: I2S left/right channel select */
#define PMOD_7_DAC   1 /**< Pin 2: I2S output data to DAC */
#define PMOD_7_ADC   2 /**< Pin 3: I2S input data from ADC */
#define PMOD_7_BCLK  3 /**< Pin 4: I2S serial bit clock */
#define PMOD_7_MCLK  6 /**< Pin 9: I2S optional master clock */
#define PMOD_7_SHDN  6 /**< Pin 9: I2S optional shutdown */
#define PMOD_7_IO5   4 /**< Pin 7: GPIO in-/output 4 */
#define PMOD_7_IO6   5 /**< Pin 8: GPIO in-/output 5 */
#define PMOD_7_IO7   6 /**< Pin 9: GPIO in-/output 6 (MCLK) */
#define PMOD_7_IO8   7 /**< Pin 10: GPIO in-/output 7 (SHDN) */

/** @} */

#endif /* ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_DIGILENT_PMOD_HEADER_H_ */
