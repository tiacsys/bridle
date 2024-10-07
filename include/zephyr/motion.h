/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef ZEPHYR_INCLUDE_MOTION_H_
#define ZEPHYR_INCLUDE_MOTION_H_

#include <zephyr/subsys/stepper_action_stream.h>

/**
 * @brief Move a stepper motor by a specified amount with gradual acceleration and deceleration.
 *
 * @param stream            An action stream associated with the target stepper motor output.
 * @param degrees           Number of degrees to move by.
 * @param max_speed         Maximum rotational speed in degrees/second.
 * @param acceleration_time Time in which to accelerate up to maximum rotational speed in seconds.
 * @param microstep_power   Microstep resolution, as power of 2.
 *
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int motion_move_by(struct stepper_action_stream *stream, double degrees, double max_speed,
		   double acceleration_time, uint8_t microstep_power);

/**
 * @brief Gradually accelerate a stepper motor from one speed to another.
 *
 * @param stream            An action stream associated with the target stepper motor output.
 * @param start_velocity    The start velocity in degrees/second.
 * @param end_velocity      The desired end velocity in degrees/second.
 * @param acceleration_time Time in which to accelerate up to maximum rotational speed in seconds.
 * @param microstep_power   Microstep resolution, as power of 2.
 *
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int motion_accelerate(struct stepper_action_stream *stream, double start_velocity,
		      double end_velocity, double acceleration_time, uint8_t microstep_power);

/**
 * @brief Rotate a stepper motor at a constant speed for at least a specified time.
 *
 * @param stream          An action stream associated with the target stepper motor output.
 * @param velocity        Rotation speed in degrees/second.
 * @param time            Time to keep rotating for before other queued actions are performed.
 * @param microstep_power Microstep resolution, as power of 2.
 *
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int motion_rotate(struct stepper_action_stream *stream, double velocity, double time,
		  uint8_t microstep_power);

#endif /* ZEPHYR_INCLUDE_MOTION_H_ */
