/*
 * Copyright (c) 2023 TiaC Systems
 * Copyright (c) 2018 Diego Sueiro
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/shell/shell.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <zephyr/device.h>
#include <bridle/drivers/actuator.h>

#define ACTUATOR_ATTR_SET_HELP						\
	"Set the actuator's channel attribute.\n"			\
	"<device_name> <channel_name> <attribute_name> <value>"

#define ACTUATOR_ATTR_GET_HELP						\
	"Get the actuator's channel attribute. Syntax:\n"		\
	"<device_name> [<channel_name 0> <attribute_name 0> .. "	\
	"<channel_name N> <attribute_name N>]"

#define ACTUATOR_INFO_HELP						\
	"Get actuator info, such as vendor and model name, for all actuators."

static const char *actuator_channel_name[ACTUATOR_CHAN_ALL] = {
	[ACTUATOR_CHAN_ACCEL_E0] = "accel_e0",
	[ACTUATOR_CHAN_ACCEL_E1] = "accel_e1",
	[ACTUATOR_CHAN_ACCEL_E2] = "accel_e2",
	[ACTUATOR_CHAN_ACCEL_E3] = "accel_e3",
	[ACTUATOR_CHAN_ACCEL_EALL] = "accel_eall",
};

static const char *actuator_attribute_name[ACTUATOR_ATTR_COMMON_COUNT] = {
	[ACTUATOR_ATTR_OFFSET] = "offset",
	[ACTUATOR_ATTR_CALIB_TARGET] = "calib_target",
	[ACTUATOR_ATTR_CONFIGURATION] = "configuration",
	[ACTUATOR_ATTR_FEATURE_MASK] = "feature_mask",
	[ACTUATOR_ATTR_ALERT] = "alert",
};

enum dynamic_command_context {
	NONE,
	CTX_GET,
	CTX_ATTR_GET_SET,
};

static enum dynamic_command_context current_cmd_ctx = NONE;

static int parse_named_int(const char *name, const char *heystack[], size_t count)
{
	char *endptr;
	int i;

	/* Attempt to parse channel name as a number first */
	i = strtoul(name, &endptr, 0);

	if (*endptr == '\0') {
		return i;
	}

	/* Channel name is not a number, look it up */
	for (i = 0; i < count; i++) {
		if (strcmp(name, heystack[i]) == 0) {
			return i;
		}
	}

	return -ENOTSUP;
}

static int parse_actuator_value(const char *val_str, struct actuator_value *out)
{
	const bool is_negative = val_str[0] == '-';
	const char *decimal_pos = strchr(val_str, '.');
	long value;
	char *endptr;

	/* Parse int portion */
	value = strtol(val_str, &endptr, 0);

	if (*endptr != '\0' && *endptr != '.') {
		return -EINVAL;
	}
	if (value > INT32_MAX || value < INT32_MIN) {
		return -EINVAL;
	}
	out->val1 = (int32_t)value;

	if (decimal_pos == NULL) {
		return 0;
	}

	/* Parse the decimal portion */
	value = strtoul(decimal_pos + 1, &endptr, 0);
	if (*endptr != '\0') {
		return -EINVAL;
	}
	while (value < 100000) {
		value *= 10;
	}
	if (value > INT32_C(999999)) {
		return -EINVAL;
	}
	out->val2 = (int32_t)value;
	if (is_negative) {
		out->val2 *= -1;
	}

	return 0;
}

static int cmd_actuator_attr_set(const struct shell *shell_ptr,
				 size_t argc, char *argv[])
{
	const struct device *dev;
	int rc;

	dev = device_get_binding(argv[1]);
	if (dev == NULL) {
		shell_error(shell_ptr, "Device unknown (%s)", argv[1]);
		return -ENODEV;
	}

	for (size_t i = 2; i < argc; i += 3) {
		int channel = parse_named_int(argv[i], actuator_channel_name,
					      ARRAY_SIZE(actuator_channel_name));
		int attr = parse_named_int(argv[i + 1], actuator_attribute_name,
					   ARRAY_SIZE(actuator_attribute_name));
		struct actuator_value value = {0};

		if (channel < 0) {
			shell_error(shell_ptr,
				    "Channel '%s' unknown", argv[i]);
			return -EINVAL;
		}

		if (attr < 0) {
			shell_error(shell_ptr,
				    "Attribute '%s' unknown", argv[i + 1]);
			return -EINVAL;
		}

		if (parse_actuator_value(argv[i + 2], &value)) {
			shell_error(shell_ptr,
				    "Actuator value '%s' invalid", argv[i + 2]);
			return -EINVAL;
		}

		rc = actuator_attr_set(dev, channel, attr, &value);
		if (rc) {
			shell_error(shell_ptr,
				    "Failed to set channel(%s) attribute(%s): %d",
				    actuator_channel_name[channel],
				    actuator_attribute_name[attr], rc);
			continue;
		}

		shell_info(shell_ptr,
			   "%s channel=%s, attr=%s set to value=%s", dev->name,
			   actuator_channel_name[channel],
			   actuator_attribute_name[attr], argv[i + 2]);
	}

	return 0;
}

static void actuator_attr_get_handler(const struct shell *shell_ptr,
				      const struct device *dev,
				      const char *channel_name,
				      const char *attr_name,
				      bool print_missing_attribute)
{
	int channel = parse_named_int(channel_name, actuator_channel_name,
				      ARRAY_SIZE(actuator_channel_name));
	int attr = parse_named_int(attr_name, actuator_attribute_name,
				   ARRAY_SIZE(actuator_attribute_name));
	struct actuator_value value = {0};
	int rc;

	if (channel < 0) {
		shell_error(shell_ptr, "Channel '%s' unknown", channel_name);
		return;
	}

	if (attr < 0) {
		shell_error(shell_ptr, "Attribute '%s' unknown", attr_name);
		return;
	}

	rc = actuator_attr_get(dev, channel, attr, &value);

	if (rc != 0) {
		if (rc == -EINVAL && !print_missing_attribute) {
			return;
		}
		shell_error(shell_ptr,
			    "Failed to get channel(%s) attribute(%s): %d",
			    actuator_channel_name[channel],
			    actuator_attribute_name[attr], rc);
		return;
	}

	shell_info(shell_ptr, "%s(channel=%s, attr=%s) value=%.6f", dev->name,
		   actuator_channel_name[channel],
		   actuator_attribute_name[attr],
		   actuator_value_to_double(&value));
}

static int cmd_actuator_attr_get(const struct shell *shell_ptr,
				 size_t argc, char *argv[])
{
	const struct device *dev;

	dev = device_get_binding(argv[1]);
	if (dev == NULL) {
		shell_error(shell_ptr, "Device unknown (%s)", argv[1]);
		return -ENODEV;
	}

	if (argc > 2) {
		for (size_t i = 2; i < argc; i += 2) {
			actuator_attr_get_handler(shell_ptr, dev,
					argv[i], argv[i + 1],
					/*print_missing_attribute=*/true);
		}
	} else {
		for (size_t channel_idx = 0;
				channel_idx < ARRAY_SIZE(actuator_channel_name);
				++channel_idx) {
			for (size_t attr_idx = 0;
					attr_idx < ARRAY_SIZE(actuator_attribute_name);
					++attr_idx) {
				actuator_attr_get_handler(shell_ptr, dev,
						actuator_channel_name[channel_idx],
						actuator_attribute_name[attr_idx],
						/*print_missing_attribute=*/false);
			}
		}
	}

	return 0;
}

static void channel_name_get(size_t idx, struct shell_static_entry *entry);
SHELL_DYNAMIC_CMD_CREATE(dsub_channel_name, channel_name_get);

static void attribute_name_get(size_t idx, struct shell_static_entry *entry)
{
	int cnt = 0;

	entry->syntax = NULL;
	entry->handler = NULL;
	entry->help = NULL;
	entry->subcmd = &dsub_channel_name;

	for (int i = 0; i < ACTUATOR_ATTR_COMMON_COUNT; i++) {
		if (actuator_attribute_name[i] != NULL) {
			if (cnt == idx) {
				entry->syntax = actuator_attribute_name[i];
				break;
			}
			cnt++;
		}
	}
}
SHELL_DYNAMIC_CMD_CREATE(dsub_attribute_name, attribute_name_get);

static void channel_name_get(size_t idx, struct shell_static_entry *entry)
{
	int cnt = 0;

	entry->syntax = NULL;
	entry->handler = NULL;
	entry->help = NULL;
	if (current_cmd_ctx == CTX_GET) {
		entry->subcmd = &dsub_channel_name;
	} else if (current_cmd_ctx == CTX_ATTR_GET_SET) {
		entry->subcmd = &dsub_attribute_name;
	} else {
		entry->subcmd = NULL;
	}

	for (int i = 0; i < ACTUATOR_CHAN_ALL; i++) {
		if (actuator_channel_name[i] != NULL) {
			if (cnt == idx) {
				entry->syntax = actuator_channel_name[i];
				break;
			}
			cnt++;
		}
	}
}

static void device_name_get_for_attr(size_t idx, struct shell_static_entry *entry)
{
	const struct device *dev = shell_device_lookup(idx, NULL);

	current_cmd_ctx = CTX_ATTR_GET_SET;
	entry->syntax = (dev != NULL) ? dev->name : NULL;
	entry->handler = NULL;
	entry->help = NULL;
	entry->subcmd = &dsub_channel_name;
}
SHELL_DYNAMIC_CMD_CREATE(dsub_device_name_for_attr, device_name_get_for_attr);

static int cmd_get_actuator_info(const struct shell *shell_ptr,
				 size_t argc, char **argv)
{
	ARG_UNUSED(argc);
	ARG_UNUSED(argv);

#ifdef CONFIG_BRIDLE_ACTUATOR_INFO
	const char *null_str = "(null)";

	STRUCT_SECTION_FOREACH(actuator_info, actuator)
	{
		shell_print(shell_ptr,
			    "device name: %s, vendor: %s, model: %s, "
			    "friendly name: %s",
			    actuator->dev->name, actuator->vendor ? actuator->vendor : null_str,
			    actuator->model ? actuator->model : null_str,
			    actuator->friendly_name ? actuator->friendly_name : null_str);
	}
	return 0;
#else
	return -EINVAL;
#endif
}

/* clang-format off */
SHELL_STATIC_SUBCMD_SET_CREATE(sub_actuator,
	SHELL_CMD_ARG(attr_set, &dsub_device_name_for_attr, ACTUATOR_ATTR_SET_HELP,
			cmd_actuator_attr_set, 2, 255),
	SHELL_CMD_ARG(attr_get, &dsub_device_name_for_attr, ACTUATOR_ATTR_GET_HELP,
			cmd_actuator_attr_get, 2, 255),
	SHELL_COND_CMD(CONFIG_BRIDLE_ACTUATOR_INFO, info, NULL, ACTUATOR_INFO_HELP,
			cmd_get_actuator_info),
	SHELL_SUBCMD_SET_END
	);
/* clang-format on */

SHELL_CMD_REGISTER(actuator, &sub_actuator, "Actuator commands", NULL);
