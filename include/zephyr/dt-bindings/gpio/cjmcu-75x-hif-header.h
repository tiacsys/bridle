/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief CJMCU SC16IS75x breakout board host interface header pin constants
 * @ingroup cjmcu-75x-hif-header
 */

#ifndef ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_CJMCU_75X_HIF_HEADER_H_
#define ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_CJMCU_75X_HIF_HEADER_H_

/**
 * @defgroup cjmcu-75x-hif-header CJMCU SC16IS75x breakout board host interface header
 * @brief Constants for pins exposed on CJMCU SC16IS75x breakout board host interface header
 * @ingroup devicetree-gpio-pin-headers
 * @{
 */

#define CJMCU_75X_HIF_HEADER_SDA 0 /**< I2C serial data */
#define CJMCU_75X_HIF_HEADER_SCL 1 /**< I2C serial clock */
#define CJMCU_75X_HIF_HEADER_A1  5 /**< I2C address bit 1 */
#define CJMCU_75X_HIF_HEADER_A0  6 /**< I2C address bit 0 */

#define CJMCU_75X_HIF_HEADER_SCLK 1 /**< SPI serial clock */
#define CJMCU_75X_HIF_HEADER_MISO 4 /**< SPI serial data output */
#define CJMCU_75X_HIF_HEADER_MOSI 5 /**< SPI serial data input */
#define CJMCU_75X_HIF_HEADER_CS   6 /**< SPI chip select */

#define CJMCU_75X_HIF_HEADER_HISEL 2 /**< Host interface selection (I2C/nSPI) */
#define CJMCU_75X_HIF_HEADER_IRQ   3 /**< Interrupt request (nIRQ) */
#define CJMCU_75X_HIF_HEADER_RESET 7 /**< Reset device (nRESET) */

/** @} */

#endif /* ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_CJMCU_75X_HIF_HEADER_H_ */
