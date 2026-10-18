/*
 * SPDX-FileCopyrightText: Copyright (c) 2023-2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief DFRobot Gravity connector pin constants
 * @ingroup gravity-connector
 */

#ifndef ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_GRAVITY_CONNECTOR_H_
#define ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_GRAVITY_CONNECTOR_H_

/**
 * @defgroup gravity-connector DFRobot Gravity connector
 * @brief Constants for pins exposed on DFRobot Gravity connectors
 * @ingroup devicetree-gpio-pin-headers
 * @{
 */

#define GRAVITY_A0 0 /**< Pin 1: ADC input 0 */

#define GRAVITY_D0 0 /**< Pin 1: GPIO in-/output 0 */

#define GRAVITY_SDA 1 /**< Pin 1: I2C SDA */
#define GRAVITY_SCL 0 /**< Pin 2: I2C SCL */

/** @} */

#endif /* ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_GRAVITY_CONNECTOR_H_ */
