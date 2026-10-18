/*
 * SPDX-FileCopyrightText: Copyright (c) 2023-2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief SparkFun Qwiic connector pin constants
 * @ingroup qwiic-connector
 */

#ifndef ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_QWIIC_CONNECTOR_H_
#define ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_QWIIC_CONNECTOR_H_

/**
 * @defgroup qwiic-connector SparkFun Qwiic connector
 * @brief Constants for pins exposed on SparkFun Qwiic connectors
 * @ingroup devicetree-gpio-pin-headers
 * @{
 */

#define QWIIC_SCL 0 /**< Pin 1: I2C SCL */
#define QWIIC_SDA 1 /**< Pin 2: I2C SDA */

/** @} */

#endif /* ZEPHYR_INCLUDE_DT_BINDINGS_GPIO_QWIIC_CONNECTOR_H_ */
