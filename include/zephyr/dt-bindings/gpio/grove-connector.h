/*
 * SPDX-FileCopyrightText: Copyright (c) 2023-2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief Seeed Studio Grove connector pin constants
 * @ingroup grove-connector
 */

#ifndef ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_GROVE_CONNECTOR_H_
#define ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_GROVE_CONNECTOR_H_

/**
 * @defgroup grove-connector Seeed Studio Grove connector
 * @brief Constants for pins exposed on Seeed Studio Grove connectors
 * @ingroup devicetree-gpio-pin-headers
 * @{
 */

#define GROVE_A0 0 /**< Pin 1: ADC input 0 */
#define GROVE_A1 1 /**< Pin 2: ADC input 1 */

#define GROVE_D0 0 /**< Pin 1: GPIO in-/output 0 */
#define GROVE_D1 1 /**< Pin 2: GPIO in-/output 1 */

#define GROVE_RX 0 /**< Pin 1: UART RX */
#define GROVE_TX 1 /**< Pin 2: UART TX */

#define GROVE_SCL 0 /**< Pin 1: I2C SCL */
#define GROVE_SDA 1 /**< Pin 2: I2C SDA */

#define GROVE_SCK  0 /**< Pin 1: SPI SCK */
#define GROVE_MISO 1 /**< Pin 2: SPI MISO */
#define GROVE_MOSI 2 /**< Pin 3: SPI MOSI */
#define GROVE_SS   3 /**< Pin 4: SPI SS */

/** @} */

#endif /* ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_GROVE_CONNECTOR_H_ */
