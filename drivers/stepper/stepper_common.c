/*
 * Copyright (c) 2024 TiaC Systems
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include "stepper_common.h"

int stepper_submit_event(const struct device *dev, const uint8_t motor,
			 const enum stepper_event_type type,
			 const int status)
{
        struct stepper_data *data = dev->data;
        struct stepper_event drv_evt = {
                .type = type,
                .status = status,
                .dev = dev,
		.motor = motor,
        };

        return data->event_cb(dev, &drv_evt);
}

