/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief No Name Technology BluePill(+) header pin constants
 * @ingroup nologo-bluepill-header
 */

#ifndef ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_NOLOGO_BLUEPILL_HEADER_H_
#define ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_NOLOGO_BLUEPILL_HEADER_H_

/**
 * @defgroup nologo-bluepill-header No Name Technology BluePill(+) header
 * @brief Constants for pins exposed on No Name Technology BluePill(+) header
 * @ingroup devicetree-gpio-pin-headers
 * @{
 */

#define NNT_BLUEPILL_HEADER_B12 0  /**< Digital pin 0 (SPI-NSS) */
#define NNT_BLUEPILL_HEADER_B13 1  /**< Digital pin 1 (SPI-SCK) */
#define NNT_BLUEPILL_HEADER_B14 2  /**< Digital pin 2 (SPI-MISO) */
#define NNT_BLUEPILL_HEADER_B15 3  /**< Digital pin 3 (SPI-MOSI) */
#define NNT_BLUEPILL_HEADER_A8  4  /**< Digital pin 4 (MCO) */
#define NNT_BLUEPILL_HEADER_A9  5  /**< Digital pin 5 (UART-TX) */
#define NNT_BLUEPILL_HEADER_A10 6  /**< Digital pin 6 (UART-RX) */
#define NNT_BLUEPILL_HEADER_A11 7  /**< Digital pin 7 (USB-DM) */
#define NNT_BLUEPILL_HEADER_A12 8  /**< Digital pin 8 (USB-DP) */
#define NNT_BLUEPILL_HEADER_A15 9  /**< Digital pin 9 (JTDI) */
#define NNT_BLUEPILL_HEADER_B3  10 /**< Digital pin 10 (JTDO) */
#define NNT_BLUEPILL_HEADER_B4  11 /**< Digital pin 11 (JTRST) */
#define NNT_BLUEPILL_HEADER_B5  12 /**< Digital pin 12 (GPIO) */
#define NNT_BLUEPILL_HEADER_B6  13 /**< Digital pin 13 (I2C-SCL) */
#define NNT_BLUEPILL_HEADER_B7  14 /**< Digital pin 14 (I2C-SDA) */
#define NNT_BLUEPILL_HEADER_B8  15 /**< Digital pin 15 (CAN-RX) */
#define NNT_BLUEPILL_HEADER_B9  16 /**< Digital pin 16 (CAN-TX) */
#define NNT_BLUEPILL_HEADER_C13 17 /**< Digital pin 17 (LED/GPIO) */
#define NNT_BLUEPILL_HEADER_C14 18 /**< Digital pin 18 (OSC32-IN/GPIO) */
#define NNT_BLUEPILL_HEADER_C15 19 /**< Digital pin 19 (OSC32-OUT/GPIO) */
#define NNT_BLUEPILL_HEADER_A0  20 /**< Analog pin 0 (ADC0/WKUP) */
#define NNT_BLUEPILL_HEADER_A1  21 /**< Analog pin 1 (ADC1) */
#define NNT_BLUEPILL_HEADER_A2  22 /**< Analog pin 2 (ADC2) */
#define NNT_BLUEPILL_HEADER_A3  23 /**< Analog pin 3 (ADC3) */
#define NNT_BLUEPILL_HEADER_A4  24 /**< Analog pin 4 (ADC4) */
#define NNT_BLUEPILL_HEADER_A5  25 /**< Analog pin 5 (ADC5) */
#define NNT_BLUEPILL_HEADER_A6  26 /**< Analog pin 6 (ADC6) */
#define NNT_BLUEPILL_HEADER_A7  27 /**< Analog pin 7 (ADC7) */
#define NNT_BLUEPILL_HEADER_B0  28 /**< Analog pin 8 (ADC8) */
#define NNT_BLUEPILL_HEADER_B1  29 /**< Analog pin 9 (ADC9) */
#define NNT_BLUEPILL_HEADER_B10 30 /**< Digital pin 20 (UART-TX/I2C-SCL) */
#define NNT_BLUEPILL_HEADER_B11 31 /**< Digital pin 21 (UART-RX/I2C-SDA) */

/** @} */

#endif /* ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_NOLOGO_BLUEPILL_HEADER_H_ */
