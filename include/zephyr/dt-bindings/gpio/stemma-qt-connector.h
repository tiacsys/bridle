/*
 * SPDX-FileCopyrightText: Copyright (c) 2023-2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief Adafruit STEMMA QT connector pin constants
 * @ingroup grove-connector
 */

#ifndef ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_STEMMA_QT_CONNECTOR_H_
#define ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_STEMMA_QT_CONNECTOR_H_

/**
 * @defgroup grove-connector Adafruit STEMMA QT connector
 * @brief Constants for pins exposed on Adafruit STEMMA QT connectors
 * @ingroup devicetree-gpio-pin-headers
 * @{
 */

#define STEMMA_QT_SCL 0 /**< Pin 1: I2C SCL */
#define STEMMA_QT_SDA 1 /**< Pin 2: I2C SDA */

/** @} */

#endif /* ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_STEMMA_QT_CONNECTOR_H_ */
