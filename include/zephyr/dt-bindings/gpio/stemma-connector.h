/*
 * SPDX-FileCopyrightText: Copyright (c) 2023-2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief Adafruit STEMMA connector pin constants
 * @ingroup stemma-connector
 */

#ifndef ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_STEMMA_CONNECTOR_H_
#define ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_STEMMA_CONNECTOR_H_

/**
 * @defgroup stemma-connector Adafruit STEMMA connector
 * @brief Constants for pins exposed on Adafruit STEMMA connectors
 * @ingroup devicetree-gpio-pin-headers
 * @{
 */

#define STEMMA_A0 0 /**< Pin 1: ADC input 0 */

#define STEMMA_D0 0 /**< Pin 1: GPIO in-/output 0 */

#define STEMMA_SCL 0 /**< Pin 1: I2C SCL */
#define STEMMA_SDA 1 /**< Pin 2: I2C SDA */

/** @} */

#endif /* ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_STEMMA_CONNECTOR_H_ */
