/*
 * Copyright (c) 2024, Fabian Blatz <fabianblatz@gmail.com>
 * Copyright (c) 2024 TiaC Systems
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/drivers/stepper.h>
#include <zephyr/shell/shell.h>

#include <stdlib.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(stepper_shell);

static bool device_is_stepper(const struct device *dev)
{
#ifdef CONFIG_STEPPER_INFO
	STRUCT_SECTION_FOREACH(stepper_info, stepper) {
		if (stepper->dev == dev) {
			return true;
		}
	}
	return false;
#else
	return true;
#endif /* CONFIG_STEPPER_INFO */
}

enum {
	arg_idx_dev = 1,
	arg_idx_motor = 2,
	arg_idx_flags = 3,
	arg_idx_value = 4,
};

/* FIXME: replace parse_device_arg() by parse_common_args() */
#if 0	/* FIXME: remove old API usage */
static int parse_device_arg(const struct shell *sh, char **argv,
			    const struct device **dev)
{
	*dev = device_get_binding(argv[arg_idx_dev]);
	if (!*dev) {
		shell_error(sh, "Stepper device %s not found", argv[arg_idx_dev]);
		return -ENODEV;
	}
	return 0;
}
#endif

static int parse_common_args(const struct shell *sh, char **argv,
			     const struct device * *dev, uint8_t *motor)
{
	char *end_ptr;

	printk("Shell: Parsing Arguments\n");

	*dev = device_get_binding(argv[arg_idx_dev]);
	if (*dev == NULL) {
		shell_error(sh, "Device unknown (%s)", argv[arg_idx_dev]);
		return -ENODEV;
	}

	if (!device_is_stepper(*dev)) {
		shell_error(sh, "Device is not a stepper motor (%s)",
				argv[arg_idx_dev]);
		return -ENODEV;
	}

	*motor = strtoul(argv[arg_idx_motor], &end_ptr, 0);
	if (*end_ptr != '\0') {
		shell_error(sh, "Invalid motor number parameter %s",
			    argv[arg_idx_motor]);
		return -EINVAL;
	}

	return 0;
}

static int cmd_move(const struct shell *sh, size_t argc, char **argv)
{
	printk("Shell: Move Command\n");
	struct stepper_action action;
	const struct device *dev;
	uint8_t motor;
	long flags = 0;
	long value = 0;
	int ret = 0;

	ret = parse_common_args(sh, argv, &dev, &motor);
	if (ret < 0) {
		shell_help(sh);
		return SHELL_CMD_HELP_PRINTED;
	}

	for (int i = 0; i < strlen(argv[arg_idx_flags]); i++) {
		switch (argv[arg_idx_flags][i]) {
		case 'a':
			flags |= STEPPER_OP_MODE_ACCELERATION;
			break;
		case 'p':
			flags |= STEPPER_OP_MODE_POSITION;
			break;
		case 'v':
			flags |= STEPPER_OP_MODE_VELOCITY;
			break;
		case '0':
			flags |= STEPPER_USTEP_RES_1;
			break;
		case '1':
			flags |= STEPPER_USTEP_RES_2;
			break;
		case '2':
			flags |= STEPPER_USTEP_RES_4;
			break;
		case '3':
			flags |= STEPPER_USTEP_RES_8;
			break;
		case '4':
			flags |= STEPPER_USTEP_RES_16;
			break;
		case '5':
			flags |= STEPPER_USTEP_RES_32;
			break;
		case '6':
			flags |= STEPPER_USTEP_RES_64;
			break;
		case '7':
			flags |= STEPPER_USTEP_RES_128;
			break;
		case '8':
			flags |= STEPPER_USTEP_RES_256;
			break;
		default:
			shell_error(sh, "Unknown: '%c'", argv[arg_idx_flags][i]);
			shell_help(sh);
			return SHELL_CMD_HELP_PRINTED;
		}
	}

	if (STEPPER_OP_MODE_GET(flags) == 0) {
		shell_error(sh, "operation mode must be specified");
		shell_help(sh);
		return SHELL_CMD_HELP_PRINTED;
	}

	/* Default to full step if not specified */
	if (STEPPER_USTEP_RES_GET(flags) == 0) {
		flags |= STEPPER_USTEP_RES_1;
	}

	if (!IS_POWER_OF_TWO(STEPPER_USTEP_RES_GET(flags))) {
		shell_error(sh, "cannot be multiple microstep resolutions");
		shell_help(sh);
		return SHELL_CMD_HELP_PRINTED;
	}

	value = shell_strtol(argv[arg_idx_value], 0, &ret);
	if ((ret == 0) && (labs(value) <= INT32_MAX)) {
		action.flags = (uint32_t)flags;
		action.value = (int32_t)value;
	} else {
		shell_error(sh, "microsteps or microsteps per seconds exceeds value range");
		shell_help(sh);
		return SHELL_CMD_HELP_PRINTED;
	}

	ret = stepper_move(dev, motor, &action);
	if (ret != 0) {
		shell_error(sh, "error: %d", ret);
	}

	return ret;
}

static int cmd_off(const struct shell *sh, size_t argc, char **argv)
{
	printk("Shell: Off Command\n");
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
	printk("Shell: On Command\n");
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

static int cmd_info(const struct shell *sh, size_t argc, char **argv)
{
	ARG_UNUSED(argc);
	ARG_UNUSED(argv);

#ifdef CONFIG_STEPPER_INFO
	const char *null_str = "(null)";

	STRUCT_SECTION_FOREACH(stepper_info, stepper) {
		shell_print(sh, "device name: %s, motor: %u, "
				"vendor: %s, model: %s, "
				"friendly name: %s",
			stepper->dev->name, stepper->motor,
			stepper->vendor ? stepper->vendor : null_str,
			stepper->model ? stepper->model : null_str,
			stepper->friendly_name ? stepper->friendly_name
					       : null_str);
	}
	return 0;
#else
	return -EINVAL;
#endif
}


#if 0	/* FIXME: remove old API usage */
static int cmd_stepper_move(const struct shell *sh, size_t argc, char **argv)
{
	const struct device *dev;
	int ret = 0;
	int32_t micro_steps = strtol(argv[arg_idx_flags], NULL, 0);

	ret = parse_device_arg(sh, argv, &dev);
	if (ret < 0) {
		return ret;
	}

	ret = stepper_move(dev, micro_steps);
	if (ret != 0) {
		shell_error(sh, "error: %d", ret);
	}

	return ret;
}

static int cmd_stepper_set_max_velocity(const struct shell *sh, size_t argc, char **argv)
{
	const struct device *dev;
	int ret = 0;
	uint32_t velocity = strtoul(argv[arg_idx_flags], NULL, 0);

	ret = parse_device_arg(sh, argv, &dev);
	if (ret < 0) {
		return ret;
	}

	ret = stepper_set_max_velocity(dev, velocity);
	if (ret != 0) {
		shell_error(sh, "error: %d", ret);
	}

	return ret;
}

static int cmd_stepper_set_micro_step_res(const struct shell *sh, size_t argc, char **argv)
{
	const struct device *dev;
	int ret = 0;
	enum micro_step_resolution resolution = atoi(argv[arg_idx_flags]);

	ret = parse_device_arg(sh, argv, &dev);
	if (ret < 0) {
		return ret;
	}

	ret = stepper_set_micro_step_res(dev, resolution);
	if (ret != 0) {
		shell_error(sh, "error: %d", ret);
	}

	return ret;
}

static int cmd_stepper_set_actual_position(const struct shell *sh, size_t argc, char **argv)
{
	const struct device *dev;
	int ret = 0;
	int32_t position = strtol(argv[arg_idx_flags], NULL, 0);

	ret = parse_device_arg(sh, argv, &dev);
	if (ret < 0) {
		return ret;
	}

	ret = stepper_set_actual_position(dev, position);
	if (ret != 0) {
		shell_error(sh, "error: %d", ret);
	}

	return ret;
}

static int cmd_stepper_set_target_position(const struct shell *sh, size_t argc, char **argv)
{
	const struct device *dev;
	int ret = 0;
	int32_t position = strtol(argv[arg_idx_flags], NULL, 0);

	ret = parse_device_arg(sh, argv, &dev);
	if (ret < 0) {
		return ret;
	}

	ret = stepper_set_target_position(dev, position);
	if (ret != 0) {
		shell_error(sh, "error: %d", ret);
	}

	return ret;
}

static int cmd_stepper_enable_constant_velocity_mode(const struct shell *sh, size_t argc,
						     char **argv)
{
	const struct device *dev;
	int ret = 0;
	enum stepper_direction direction = atoi(argv[arg_idx_flags]);
	uint32_t velocity = strtoul(argv[arg_idx_value], NULL, 0);

	ret = parse_device_arg(sh, argv, &dev);
	if (ret < 0) {
		return ret;
	}

	ret = stepper_enable_constant_velocity_mode(dev, direction, velocity);
	if (ret != 0) {
		shell_error(sh, "error: %d", ret);
	}

	return ret;
}

static int cmd_stepper_info(const struct shell *sh, size_t argc, char **argv)
{
	const struct device *dev;
	int ret = 0;
	bool is_moving = false;
	int32_t actual_position = 0;
	enum micro_step_resolution micro_step_res = 0;

	ret = parse_device_arg(sh, argv, &dev);
	if (ret < 0) {
		return ret;
	}

	shell_print(sh, "Stepper Info:");
	shell_print(sh, "Device: %s", dev->name);

	ret = stepper_get_actual_position(dev, &actual_position);
	if (ret < 0) {
		shell_warn(sh, "Failed to get actual position: %d", ret);
	} else {
		shell_print(sh, "Actual Position: %d", actual_position);
	}

	ret = stepper_get_micro_step_res(dev, &micro_step_res);
	if (ret < 0) {
		shell_warn(sh, "Failed to get micro-step resolution: %d", ret);
	} else {
		shell_print(sh, "Micro-step Resolution: %d", micro_step_res);
	}

	ret = stepper_is_moving(dev, &is_moving);
	if (ret < 0) {
		shell_warn(sh, "Failed to check if the motor is moving: %d", ret);
	} else {
		shell_print(sh, "Is Moving: %s", is_moving ? "Yes" : "No");
	}

	return 0;
}
#endif

static void device_name_get(size_t idx, struct shell_static_entry *entry)
{
	const struct device *dev = shell_device_lookup(idx, NULL);

	entry->syntax = (dev != NULL) ? dev->name : NULL;
	entry->handler = NULL;
	entry->help = NULL;
	entry->subcmd = NULL;
}

SHELL_DYNAMIC_CMD_CREATE(sub_stepper_dev, device_name_get);

SHELL_STATIC_SUBCMD_SET_CREATE(sub_stepper,
	SHELL_CMD_ARG(move, &sub_stepper_dev,
		"Move stepper motor\n"
		"Usage: stepper move <device> <motor> <flags <p|v|a>[MSR]> <value>\n"
		"<p|v|a> - operation mode: positioning|velocity|accelerating\n"
		"[MSR]   - one of n=0|1|2|3|4|5|6|7|8 - microstep resolution (1/2^n)\n"
		"<value> - microsteps in positioning mode (relative), or\n"
		"          microsteps per second in velocity mode (absolute), or\n"
		"          microsteps per square-second in accelerating mode (absolute)\n"
		"Defaults: full step (MSR=0)\n"
		"NOTE:     accelerating mode is not (yet) supported", cmd_move, 5, 0),
	SHELL_CMD_ARG(off, &sub_stepper_dev,
		"Turn off stepper motor power\n"
		"Usage: stepper off <device> <motor>", cmd_off, 3, 0),
	SHELL_CMD_ARG(on, &sub_stepper_dev,
		"Turn on stepper motor power\n"
		"Usage: stepper on <device> <motor>", cmd_on, 3, 0),
	SHELL_COND_CMD(CONFIG_STEPPER_INFO, info, NULL,
		"Get information, such as vendor and model name, for all stepper motors.\n"
		"Usage: stepper info", cmd_info),
#if 0	/* FIXME: remove old API usage */
	SHELL_CMD_ARG(move, NULL, "<device> <micro_steps>", cmd_stepper_move, 3, 0),
	SHELL_CMD_ARG(set_max_velocity, NULL, "<device> <velocity>", cmd_stepper_set_max_velocity,
		      3, 0),
	SHELL_CMD_ARG(set_micro_step_res, NULL, "<device> <resolution>",
		      cmd_stepper_set_micro_step_res, 3, 0),
	SHELL_CMD_ARG(set_actual_position, NULL, "<device> <position>",
		      cmd_stepper_set_actual_position, 3, 0),
	SHELL_CMD_ARG(set_target_position, NULL, "<device> <position>",
		      cmd_stepper_set_target_position, 3, 0),
	SHELL_CMD_ARG(enable_constant_velocity_mode, NULL, "<device> <direction> <velocity>",
		      cmd_stepper_enable_constant_velocity_mode, 4, 0),
	SHELL_CMD_ARG(info, NULL, "<device>", cmd_stepper_info, 2, 0),
#endif
	SHELL_SUBCMD_SET_END);

SHELL_CMD_REGISTER(stepper, &sub_stepper, "Stepper motor commands", NULL);
