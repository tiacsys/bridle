/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <math.h>
#include <zephyr/logging/log.h>
#include <zephyr/motion.h>

#include "zephyr/drivers/stepper.h"
#include "zephyr/dt-bindings/stepper/stepper.h"
LOG_MODULE_REGISTER(motion, CONFIG_MOTION_LOG_LEVEL);

static uint32_t flag_from_microstep_power(uint8_t power)
{
	switch (power) {
	case 0:
		return STEPPER_USTEP_RES_1;
	case 1:
		return STEPPER_USTEP_RES_2;
	case 2:
		return STEPPER_USTEP_RES_4;
	case 3:
		return STEPPER_USTEP_RES_8;
	case 4:
		return STEPPER_USTEP_RES_16;
	case 5:
		return STEPPER_USTEP_RES_32;
	case 6:
		return STEPPER_USTEP_RES_64;
	case 7:
		return STEPPER_USTEP_RES_128;
	case 8:
		return STEPPER_USTEP_RES_256;
	default:
		return 0;
	}
}

static int generate_ramp(struct stepper_action *actions, double distance_degrees,
			 uint32_t ramp_up_time_us, double max_velocity_deg_s, uint32_t fs_per_turn,
			 uint8_t microstep_power)
{
	/* Convert distance and velocity into steps/s */
	double distance_steps = fabs(fs_per_turn * distance_degrees) / 360.0;
	double max_velocity_steps_s = (fs_per_turn * max_velocity_deg_s) / 360.0;
	if (distance_degrees < 0) {
		max_velocity_steps_s = -max_velocity_steps_s;
	}

	/* Compute total necessary movement time (at max velocity) */
	uint32_t total_time_max_speed_us =
		fabs(distance_degrees) / max_velocity_deg_s * USEC_PER_SEC;

	/* Convert microstep power into raw flags */
	uint32_t flags = flag_from_microstep_power(microstep_power);
	if (flags == 0) {
		LOG_ERR("Invalid microstep power: %d", microstep_power);
		return 0;
	}

	/* If getting up to full speed and slowing down again would put us over the target distance,
	 * we need to generate a reduced trapezoid, aka a triangle. Note: Each of the 2 ramps covers
	 * half the distance as the same time spent at max speed
	 * ==> 2 * 0.5 * ramp_up_time_us >?= total_time_max_speed_us. */
	if (ramp_up_time_us > total_time_max_speed_us) {
		/* Compute new maximum speed and movement time */
		double acceleration_steps_s_s =
			fabs(max_velocity_steps_s) / ((double)ramp_up_time_us / USEC_PER_SEC);

		double reduced_max_velocity_steps_s = sqrt(distance_steps * acceleration_steps_s_s);

		if (distance_degrees < 0) {
			reduced_max_velocity_steps_s = -reduced_max_velocity_steps_s;
		}
		uint32_t reduced_ramp_up_time_us =
			sqrt(distance_steps / acceleration_steps_s_s) * USEC_PER_SEC;

		/* Ramp up */
		actions[0] = (struct stepper_action){
			.type = STEPPER_ACTION_TYPE_ACCELERATION,
			.flags = flags,
			.action.acceleration =
				{
					.start_velocity = 0,
					.end_velocity = reduced_max_velocity_steps_s,
					.duration_us = reduced_ramp_up_time_us,
				},
		};

		/* Ramp down */
		actions[1] = (struct stepper_action){
			.type = STEPPER_ACTION_TYPE_ACCELERATION,
			.flags = flags,
			.action.acceleration =
				{
					.start_velocity = reduced_max_velocity_steps_s,
					.end_velocity = 0,
					.duration_us = reduced_ramp_up_time_us,
				},
		};

		return 2;

	} else {
		/* Each ramp covers half as much as it would at full speed -> Both ramps combined
		 * take off 1x the ramp time from the coasting time */
		uint32_t coasting_time_us = total_time_max_speed_us - ramp_up_time_us;

		/* Ramp up */
		actions[0] = (struct stepper_action){
			.type = STEPPER_ACTION_TYPE_ACCELERATION,
			.flags = STEPPER_USTEP_RES_8,
			.action.acceleration =
				{
					.start_velocity = 0,
					.end_velocity = max_velocity_steps_s,
					.duration_us = ramp_up_time_us,
				},
		};

		/* Coast */
		actions[1] = (struct stepper_action){
			.type = STEPPER_ACTION_TYPE_VELOCITY,
			.flags = STEPPER_USTEP_RES_8,
			.action.velocity =
				{
					.velocity = max_velocity_steps_s,
					.duration_us = coasting_time_us,
				},
		};

		/* Ramp down */
		actions[2] = (struct stepper_action){
			.type = STEPPER_ACTION_TYPE_ACCELERATION,
			.flags = STEPPER_USTEP_RES_8,
			.action.acceleration =
				{
					.start_velocity = max_velocity_steps_s,
					.end_velocity = 0,
					.duration_us = ramp_up_time_us,
				},
		};

		return 3;
	}
}

int motion_move_by(struct stepper_action_stream *stream, double degrees, double max_speed,
		   double acceleration_time, uint8_t microstep_power)
{
	if (stream == NULL) {
		return -EINVAL;
	}

	if (max_speed <= 0) {
		LOG_ERR("Invalid maximum speed %f, maximum speed must be positive", max_speed);
		return -EINVAL;
	}

	if (acceleration_time < 0) {
		LOG_ERR("Invalid acceleration time %f, acceleration time must be non-negative",
			acceleration_time);
	}

	/* Get necessary motor properties */
	const struct stepper_motor_properties *motor_props =
		stepper_motor_props(stream->driver, stream->motor);
	const uint32_t fs_per_turn = motor_props->fs_per_turn;

	/* Motion consists of up to 3 actions */
	struct stepper_action actions[3];

	/* Generate and execute actions */
	int ret = 0;
	int n_actions = generate_ramp(actions, degrees, acceleration_time * USEC_PER_SEC, max_speed,
				      fs_per_turn, microstep_power);

	if (n_actions == 0) {
		return -EINVAL;
	}

	for (int i = 0; i < n_actions; i++) {
		ret = stepper_action_stream_submit(stream, &actions[i]);
		if (ret != 0) {
			LOG_ERR("Failed to submit stepper action (error %d)", ret);
			return ret;
		}
	}

	return 0;
}

int motion_accelerate(struct stepper_action_stream *stream, double start_velocity,
		      double end_velocity, double acceleration_time, uint8_t microstep_power)
{
	/* Convert microstep power into raw flags */
	uint32_t flags = flag_from_microstep_power(microstep_power);
	if (flags == 0) {
		LOG_ERR("Invalid microstep power: %d", microstep_power);
		return 0;
	}

	/* Get necessary motor properties */
	const struct stepper_motor_properties *motor_props =
		stepper_motor_props(stream->driver, stream->motor);
	const uint32_t fs_per_turn = motor_props->fs_per_turn;

	/* Convert velocities from degrees/s to steps/s */
	double start_velocity_steps = (fs_per_turn * start_velocity) / 360.0;
	double end_velocity_steps = (fs_per_turn * end_velocity) / 360.0;

	struct stepper_action accelerate = {
		.type = STEPPER_ACTION_TYPE_ACCELERATION,
		.flags = flags,
		.action.acceleration =
			{
				.start_velocity = start_velocity_steps,
				.end_velocity = end_velocity_steps,
				.duration_us = acceleration_time * USEC_PER_SEC,
			},
	};

	int ret = 0;
	ret = stepper_action_stream_submit(stream, &accelerate);
	if (ret != 0) {
		LOG_ERR("Failed to submit stepper action (error %d)", ret);
		return ret;
	}

	return 0;
}

int motion_rotate(struct stepper_action_stream *stream, double velocity, double time,
		  uint8_t microstep_power)
{
	/* Convert microstep power into raw flags */
	uint32_t flags = flag_from_microstep_power(microstep_power);
	if (flags == 0) {
		LOG_ERR("Invalid microstep power: %d", microstep_power);
		return 0;
	}

	/* Get necessary motor properties */
	const struct stepper_motor_properties *motor_props =
		stepper_motor_props(stream->driver, stream->motor);
	const uint32_t fs_per_turn = motor_props->fs_per_turn;

	/* Convert velocities from degrees/s to steps/s */
	double velocity_steps = (fs_per_turn * velocity) / 360.0;

	struct stepper_action rotate = {
		.type = STEPPER_ACTION_TYPE_VELOCITY,
		.flags = flags,
		.action.velocity =
			{
				.velocity = velocity_steps,
				.duration_us = time * USEC_PER_SEC,
			},
	};

	int ret = 0;
	ret = stepper_action_stream_submit(stream, &rotate);
	if (ret != 0) {
		LOG_ERR("Failed to submit stepper action (error %d)", ret);
		return ret;
	}

	return 0;
}
