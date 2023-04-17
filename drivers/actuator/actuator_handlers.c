/*
 * Copyright (c) 2023 TiaC Systems
 * Copyright (c) 2017 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <bridle/drivers/actuator.h>
#include <zephyr/syscall_handler.h>

static inline int z_vrfy_actuator_attr_set(const struct device *dev,
					   enum actuator_channel chan,
					   enum actuator_attribute attr,
					   const struct actuator_value *val)
{
	Z_OOPS(Z_SYSCALL_DRIVER_ACTUATOR(dev, attr_set));
	Z_OOPS(Z_SYSCALL_MEMORY_READ(val, sizeof(struct actuator_value)));
	return z_impl_actuator_attr_set((const struct device *)dev, chan, attr,
				        (const struct actuator_value *)val);
}
#include <syscalls/actuator_attr_set_mrsh.c>

static inline int z_vrfy_actuator_attr_get(const struct device *dev,
					   enum actuator_channel chan,
					   enum actuator_attribute attr,
					   struct actuator_value *val)
{
	Z_OOPS(Z_SYSCALL_DRIVER_ACTUATOR(dev, attr_get));
	Z_OOPS(Z_SYSCALL_MEMORY_WRITE(val, sizeof(struct actuator_value)));
	return z_impl_actuator_attr_get((const struct device *)dev, chan, attr,
				        (struct actuator_value *)val);
}
#include <syscalls/actuator_attr_get_mrsh.c>
