/*
 * Copyright (c) 2024 TiaC Systems
 *
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief Private API for stepper motor drivers
 */

#ifndef ZEPHYR_DRIVERS_STEPPER_STEPPER_COMMON_H_
#define ZEPHYR_DRIVERS_STEPPER_STEPPER_COMMON_H_

#include <zephyr/drivers/stepper.h>

/**
 * @brief Get driver's private data.
 *
 * @param[in] dev       Stepper motor device driver instance.
 *
 * @return Pointer to driver's private data.
 */
static inline void *stepper_get_private(const struct device *dev)
{
	struct stepper_data *data = dev->data;

	return data->priv;
}

/**
 * @brief Helper function to send stepper motor event to a higher level.
 *
 * @details The callback would typically sends stepper motor even to
 * (TODO/TBD: a message queue (k_msgq)).
 *
 * @param[in] dev       Stepper motor device driver instance.
 * @param[in] motor     Stepper motor number.
 * @param[in] type      Stepper motor event type.
 * @param[in] status    Stepper motor event status.
 *
 * @return 0 on success, all other values should be treated as error.
 * @retval -EPERM controller is not initialized
 */
int stepper_submit_event(const struct device *dev, const uint8_t motor,
			 const enum stepper_event_type type,
			 const int status);

#endif /* ZEPHYR_DRIVERS_STEPPER_STEPPER_COMMON_H_ */
