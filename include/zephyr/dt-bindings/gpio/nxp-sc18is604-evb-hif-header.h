/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief NXP SC18IS604-EVB host interface header pin constants
 * @ingroup nxp-sc18is604-hif-header
 */

#ifndef ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_NXP_SC18IS604_EVB_HIF_HEADER_H_
#define ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_NXP_SC18IS604_EVB_HIF_HEADER_H_

/**
 * @defgroup nxp-sc18is604-hif-header NXP SC18IS604-EVB host interface header
 * @brief Constants for pins exposed on NXP SC18IS604-EVB host interface header
 * @ingroup devicetree-gpio-pin-headers
 * @{
 */

#define NXP_SC18IS604_EVB_HIF_HEADER_RESET 0 /**< Reset device */
#define NXP_SC18IS604_EVB_HIF_HEADER_INT   1 /**< Interrupt request */
#define NXP_SC18IS604_EVB_HIF_HEADER_SCLK  2 /**< SPI serial clock */
#define NXP_SC18IS604_EVB_HIF_HEADER_MOSI  3 /**< SPI serial data input */
#define NXP_SC18IS604_EVB_HIF_HEADER_MISO  4 /**< SPI serial data output */
#define NXP_SC18IS604_EVB_HIF_HEADER_CS    5 /**< SPI chip select */

/** @} */

#endif /* ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_NXP_SC18IS604_EVB_HIF_HEADER_H_ */
