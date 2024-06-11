/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef ZEPHYR_DRIVERS_I2C_SC18IS604_H_
#define ZEPHYR_DRIVERS_I2C_SC18IS604_H_

#ifdef __cplusplus
extern "C" {
#endif

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/i2c.h>


/**
 * @brief SC18IM604 I2C controller configuration data
 *
 * This structure contains all of the state for a given SC18IM604
 * I2C controller as well as the binding to related MFD device.
 */
typedef struct i2c_sc18is604_config {
	/** Parent MFD device for real operations on hardware. */
	const struct device *parent_dev;
} i2c_sc18is604_config_t;

/**
 * @brief SC18IS604 I2C controller data
 *
 * This structure contains data structures used by a SC18IM604 I2C controller.
 *
 */
typedef struct i2c_sc18is604_data {
	/** Back-reference to driver instance. */
	const struct device *dev;
	/** I2C bus configuration flags. */
	uint32_t i2c_config;
	/** Lock for transactions. */
	struct k_sem lock;
	/** Interrupt handling callback */
	struct gpio_callback interrupt_callback;
	/** Lock for ongoing interrupt handling. */
	struct k_sem interrupt_lock;
	/** Signal for waiting on interrupts. */
	struct k_poll_signal interrupt_signal;
	/** Work items for interrupt handling */
	struct k_work interrupt_work_initial;
	struct k_work_delayable interrupt_work_final;
	/** Struct for passing data between interrupt handling work items. */
	struct sc18is604_interrupt_handling_data {
		uint8_t i2cstat;
		struct k_poll_signal signal;
	} interrupt_handling_data;
} i2c_sc18is604_data_t;

/**
 *
 * @brief Await a signal being raised.
 *
 * @param signal The signal to await.
 * @param[out] result The result attached to the raised signal.
 * @param timeout Timeout before awaiting the signal is aborted.
 *
 * @retval 1 If the signal was raised.
 * @retval 0 If the signal was not raised within the timeout.
 * @return Negative error code if some failure occurs during k_poll().
 */
int await_signal(struct k_poll_signal *signal,
		 int *result, k_timeout_t timeout);

/**
 * @brief Transfer I2C messages asynchronously.
 *
 * @param dev An SC18IS604 I2C controller.
 * @param msgs I2C messages to be transmitted. Pointer must remain valid
 *             for the duration of the transfer.
 * @param num_msgs Number of messages to be transmitted.
 * @param addr I2C address of the target device.
 * @param cb Callback to be invoked on transfer completion (or failure).
 * @param userdata User data passed to callback.
 */
int i2c_sc18is604_transfer_cb(const struct device *dev,
			      struct i2c_msg *msgs, uint8_t num_msgs,
			      uint16_t addr,
			      i2c_callback_t cb, void *userdata);

#ifdef __cplusplus
}
#endif

#endif /* ZEPHYR_DRIVERS_I2C_SC18IS604_H_ */
