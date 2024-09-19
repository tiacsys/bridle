/*
 * Copyright (c) 2024, Fabian Blatz <fabianblatz@gmail.com>
 * Copyright (c) 2024 TiaC Systems
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <stdlib.h>
#include <zephyr/drivers/stepper.h>
#include <zephyr/logging/log.h>
#include <zephyr/shell/shell.h>

#include "zephyr/dt-bindings/stepper/stepper.h"
#include "zephyr/shell/shell_string_conv.h"
LOG_MODULE_REGISTER(stepper_shell);

enum {
	arg_idx_dev = 1,
	arg_idx_motor = 2,
};

static int parse_common_args(const struct shell *sh, char **argv, const struct device **dev,
			     uint8_t *motor)
{
	char *end_ptr;

	*dev = device_get_binding(argv[arg_idx_dev]);
	if (*dev == NULL) {
		shell_error(sh, "Device unknown (%s)", argv[arg_idx_dev]);
		return -ENODEV;
	}

	*motor = strtoul(argv[arg_idx_motor], &end_ptr, 0);
	if (*end_ptr != '\0') {
		shell_error(sh, "Invalid motor number parameter %s", argv[arg_idx_motor]);
		return -EINVAL;
	}

	return 0;
}

static int parse_microsteps(const struct shell *sh, char *msr_arg, uint32_t *flags)
{
	if (strlen(msr_arg) > 1) {
		return -EINVAL;
	}

	uint32_t parsed_flags = 0;

	switch (msr_arg[0]) {
	case '0':
		parsed_flags |= STEPPER_USTEP_RES_1;
		break;
	case '1':
		parsed_flags |= STEPPER_USTEP_RES_2;
		break;
	case '2':
		parsed_flags |= STEPPER_USTEP_RES_4;
		break;
	case '3':
		parsed_flags |= STEPPER_USTEP_RES_8;
		break;
	case '4':
		parsed_flags |= STEPPER_USTEP_RES_16;
		break;
	case '5':
		parsed_flags |= STEPPER_USTEP_RES_32;
		break;
	case '6':
		parsed_flags |= STEPPER_USTEP_RES_64;
		break;
	case '7':
		parsed_flags |= STEPPER_USTEP_RES_128;
		break;
	case '8':
		parsed_flags |= STEPPER_USTEP_RES_256;
		break;
	default:
		return -EINVAL;
	}

	*flags = parsed_flags;

	return 0;
}

static int cmd_position(const struct shell *sh, size_t argc, char **argv)
{
	int ret = 0;
	const struct device *dev;
	uint8_t motor;

	ret = parse_common_args(sh, argv, &dev, &motor);
	if (ret < 0) {
		shell_help(sh);
		return SHELL_CMD_HELP_PRINTED;
	}

	char *steps_str = argv[3];
	char *velocity_str = argv[4];

	uint32_t steps = shell_strtoul(steps_str, 10, &ret);
	if (ret != 0) {
		shell_error(sh, "Invalid number of steps: %s", steps_str);
		return -EINVAL;
	}
	int32_t velocity = shell_strtol(velocity_str, 10, &ret);
	if (ret != 0) {
		shell_error(sh, "Invalid velocity: %s", velocity_str);
		return -EINVAL;
	}

	uint32_t flags = 0;
	if (argc > 5) {
		char *msr_str = argv[5];
		ret = parse_microsteps(sh, msr_str, &flags);
		if (ret != 0) {
			shell_error(sh, "Invalid microstep resolution: %s", msr_str);
			return -EINVAL;
		}
	} else {
		flags = STEPPER_USTEP_RES_1;
	}

	const struct stepper_action action = {
		.type = STEPPER_ACTION_TYPE_POSIIONING,
		.flags = flags,
		.action.positioning =
			{
				.steps = steps,
				.velocity = velocity,
			},
	};

	ret = stepper_move(dev, motor, &action);
	if (ret != 0) {
		shell_error(sh, "Error: %d", ret);
		return ret;
	}

	return 0;
}

static int cmd_velocity(const struct shell *sh, size_t argc, char **argv)
{
	int ret = 0;
	const struct device *dev;
	uint8_t motor;

	ret = parse_common_args(sh, argv, &dev, &motor);
	if (ret < 0) {
		shell_help(sh);
		return SHELL_CMD_HELP_PRINTED;
	}

	char *velocity_str = argv[3];
	char *duration_str = argv[4];

	int32_t velocity = shell_strtol(velocity_str, 10, &ret);
	if (ret != 0) {
		shell_error(sh, "Invalid velocity: %s", velocity_str);
		return -EINVAL;
	}
	uint32_t duration_us = shell_strtoul(duration_str, 10, &ret);
	if (ret != 0) {
		shell_error(sh, "Invalid duration: %s", duration_str);
		return -EINVAL;
	}

	uint32_t flags = 0;
	if (argc > 5) {
		char *msr_str = argv[5];
		ret = parse_microsteps(sh, msr_str, &flags);
		if (ret != 0) {
			shell_error(sh, "Invalid microstep resolution: %s", msr_str);
			return -EINVAL;
		}
	} else {
		flags = STEPPER_USTEP_RES_1;
	}

	const struct stepper_action action = {
		.type = STEPPER_ACTION_TYPE_VELOCITY,
		.flags = flags,
		.action.velocity =
			{
				.velocity = velocity,
				.duration_us = duration_us,
			},
	};

	ret = stepper_move(dev, motor, &action);
	if (ret != 0) {
		shell_error(sh, "Error: %d", ret);
		return ret;
	}

	const struct stepper_action stop = STEPPER_ACTION_STOP;
	ret = stepper_move(dev, motor, &stop);
	if (ret != 0) {
		shell_error(sh, "Error: %d", ret);
	}

	return 0;
}

static int cmd_acceleration(const struct shell *sh, size_t argc, char **argv)
{
	int ret = 0;
	const struct device *dev;
	uint8_t motor;

	ret = parse_common_args(sh, argv, &dev, &motor);
	if (ret < 0) {
		shell_help(sh);
		return SHELL_CMD_HELP_PRINTED;
	}

	char *start_velocity_str = argv[3];
	char *end_velocity_str = argv[4];
	char *duration_str = argv[5];

	int32_t start_velocity = shell_strtol(start_velocity_str, 10, &ret);
	if (ret != 0) {
		shell_error(sh, "Invalid velocity: %s", start_velocity_str);
		return -EINVAL;
	}

	int32_t end_velocity = shell_strtol(end_velocity_str, 10, &ret);
	if (ret != 0) {
		shell_error(sh, "Invalid velocity: %s", end_velocity_str);
		return -EINVAL;
	}

	uint32_t duration_us = shell_strtoul(duration_str, 10, &ret);
	if (ret != 0) {
		shell_error(sh, "Invalid duration: %s", duration_str);
		return -EINVAL;
	}

	uint32_t flags = 0;
	if (argc > 6) {
		char *msr_str = argv[6];
		ret = parse_microsteps(sh, msr_str, &flags);
		if (ret != 0) {
			shell_error(sh, "Invalid microstep resolution: %s", msr_str);
			return -EINVAL;
		}
	} else {
		flags = STEPPER_USTEP_RES_1;
	}

	const struct stepper_action action = {
		.type = STEPPER_ACTION_TYPE_ACCELERATION,
		.flags = flags,
		.action.acceleration =
			{
				.start_velocity = start_velocity,
				.end_velocity = end_velocity,
				.duration_us = duration_us,
			},
	};

	ret = stepper_move(dev, motor, &action);
	if (ret != 0) {
		shell_error(sh, "Error: %d", ret);
		return ret;
	}

	return 0;
}

static int cmd_off(const struct shell *sh, size_t argc, char **argv)
{
	const struct device *dev;
	uint8_t motor;
	int ret = 0;

	ret = parse_common_args(sh, argv, &dev, &motor);
	if (ret < 0) {
		shell_help(sh);
		return SHELL_CMD_HELP_PRINTED;
	}

	shell_print(sh, "%s: turning off stepper motor %d", dev->name, motor);

	ret = stepper_off(dev, motor);
	if (ret != 0) {
		shell_error(sh, "error: %d", ret);
	}

	return ret;
}

static int cmd_on(const struct shell *sh, size_t argc, char **argv)
{
	const struct device *dev;
	uint8_t motor;
	int ret = 0;

	ret = parse_common_args(sh, argv, &dev, &motor);
	if (ret < 0) {
		shell_help(sh);
		return SHELL_CMD_HELP_PRINTED;
	}

	shell_print(sh, "%s: turning on stepper motor %d", dev->name, motor);

	ret = stepper_on(dev, motor);
	if (ret != 0) {
		shell_error(sh, "error: %d", ret);
	}

	return ret;
}

static void device_name_get(size_t idx, struct shell_static_entry *entry)
{
	const struct device *dev = shell_device_lookup(idx, NULL);

	entry->syntax = (dev != NULL) ? dev->name : NULL;
	entry->handler = NULL;
	entry->help = NULL;
	entry->subcmd = NULL;
}

SHELL_DYNAMIC_CMD_CREATE(sub_stepper_dev, device_name_get);

SHELL_STATIC_SUBCMD_SET_CREATE(
	sub_stepper,
	SHELL_CMD_ARG(position, &sub_stepper_dev,
		      "Perform a positioning action with a stepper motor\n"
		      "Usage: stepper position <device> <motor> <steps> <velocity> [MSR]\n"
		      "<steps>    - Number of steps to move by\n"
		      "<velocity> - Stepping rate [full-steps/s]\n"
		      "[MSR]      - one of n=0|1|2|3|4|5|6|7|8 - microstep resolution "
		      "(1/2^n)\n",
		      cmd_position, 5, 1),
	SHELL_CMD_ARG(velocity, &sub_stepper_dev,
		      "Perform a velocity action with a stepper motor\n"
		      "Usage: stepper velocity <device> <motor> <velocity> <duration> [MSR]\n"
		      "<velocity> - Stepping rate [full-steps/s]\n"
		      "<duration> - Movement duration [microseconds]\n"
		      "[MSR]      - one of n=0|1|2|3|4|5|6|7|8 - microstep resolution "
		      "(1/2^n)\n",
		      cmd_velocity, 5, 1),
	SHELL_CMD_ARG(
		acceleration, &sub_stepper_dev,
		"Perform an acceleration action with a stepper motor\n"
		"Usage: stepper acceleration <device> <motor> <v_start> <v_end> <duration> [MSR]\n"
		"<v_start>  - Start velocity [full-steps/s]\n"
		"<v_end>    - End velocity [full-steps/s]\n"
		"<duration> - Duration [microseconds]\n"
		"[MSR]      - one of n=0|1|2|3|4|5|6|7|8 - microstep resolution "
		"(1/2^n)\n",
		cmd_acceleration, 6, 1),
	SHELL_CMD_ARG(off, &sub_stepper_dev,
		      "Turn off stepper motor power\n"
		      "Usage: stepper off <device> <motor>",
		      cmd_off, 3, 0),
	SHELL_CMD_ARG(on, &sub_stepper_dev,
		      "Turn on stepper motor power\n"
		      "Usage: stepper on <device> <motor>",
		      cmd_on, 3, 0),
	SHELL_SUBCMD_SET_END);

SHELL_CMD_REGISTER(stepper, &sub_stepper, "Stepper motor commands", NULL);
