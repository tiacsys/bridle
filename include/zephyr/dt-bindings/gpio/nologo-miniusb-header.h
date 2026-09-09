/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief No Name Technology Mini USB header pin constants
 * @ingroup waveshare-rp2040mini-header
 */

#ifndef ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_NOLOGO_MINIUSB_HEADER_H_
#define ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_NOLOGO_MINIUSB_HEADER_H_

/**
 * @defgroup waveshare-rp2040mini-header No Name Technology Mini USB header
 * @brief Constants for pins exposed on No Name Technology Mini USB header
 * @ingroup devicetree-gpio-pin-headers
 * @{
 */

#define NNT_MINIUSB_HEADER_D0  0  /**< Digital pin 0 (GP0) */
#define NNT_MINIUSB_HEADER_D1  1  /**< Digital pin 1 (GP1) */
#define NNT_MINIUSB_HEADER_D2  2  /**< Digital pin 2 (GP2) */
#define NNT_MINIUSB_HEADER_D3  3  /**< Digital pin 3 (GP3) */
#define NNT_MINIUSB_HEADER_D4  4  /**< Digital pin 4 (GP4) */
#define NNT_MINIUSB_HEADER_D5  5  /**< Digital pin 5 (GP5) */
#define NNT_MINIUSB_HEADER_D6  6  /**< Digital pin 6 (GP6) */
#define NNT_MINIUSB_HEADER_D7  7  /**< Digital pin 7 (GP7) */
#define NNT_MINIUSB_HEADER_D8  8  /**< Digital pin 8 (GP8) */
#define NNT_MINIUSB_HEADER_D9  9  /**< Digital pin 14 (GP14) */
#define NNT_MINIUSB_HEADER_D10 10 /**< Digital pin 15 (GP15) */
#define NNT_MINIUSB_HEADER_A0  11 /**< Analog pin 0 (ADC0/GP26) */
#define NNT_MINIUSB_HEADER_A1  12 /**< Analog pin 1 (ADC1/GP27) */
#define NNT_MINIUSB_HEADER_A2  13 /**< Analog pin 2 (ADC2/GP28) */
#define NNT_MINIUSB_HEADER_A3  14 /**< Analog pin 3 (ADC2/GP29) */

/** @} */

#endif /* ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_NOLOGO_MINIUSB_HEADER_H_ */
