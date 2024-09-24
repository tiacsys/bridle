/*
 * SPDX-FileCopyrightText: Copyright (c) 2024 TiaC Systems
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef ZEPHYR_INCLUDE_DEVICETREE_MOTORS_H_
#define	ZEPHYR_INCLUDE_DEVICETREE_MOTORS_H_

#ifdef __cplusplus
extern "C" {
#endif

#define DT_STEPPER_MOTOR_DRIVER_BY_IDX(node_id, idx) \
	DT_PHANDLE_BY_IDX(node_id, stepper_motors, idx)

#define DT_STEPPER_MOTOR_OUTPUT_BY_IDX(node_id, idx) \
	DT_PHA_BY_IDX(node_id, stepper_motors, idx, motor)

#ifdef __cplusplus
}
#endif

#endif // ZEPHYR_INCLUDE_DEVICETREE_MOTORS_H_
