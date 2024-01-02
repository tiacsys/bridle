/*
 * Copyright (c) 2021-2023 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <bridle/core.h>
#include "version.h" /* generated at compile time */

#include <zephyr/shell/shell.h>

#define BRIDLE_HELP_BRIDLE		"Bridle commands."

#define BRIDLE_HELP_INFO		"Bridle information."

#define BRIDLE_HELP_VERSION		"Bridle version."
#define BRIDLE_HELP_VERSION_SHORT	"Bridle version (w/o tweak)."
#define BRIDLE_HELP_VERSION_LONG	"Bridle version (with tweak)."

#define BRIDLE_MSG_INFO_ZEPHYR		"Zephyr: "
#define BRIDLE_MSG_INFO_BRIDLE		"Bridle: "

#define BRIDLE_MSG_VERSION		"Bridle version "
#define BRIDLE_MSG_UNKNOWN_PARAMETER	" unknown parameter: "

static int cmd_bridle_info(const struct shell *shell, size_t argc, char** argv)
{
        ARG_UNUSED(argc);
        ARG_UNUSED(argv);

#ifdef CONFIG_SHELL_GETOPT
	/* When getopt() is active, the shell sub-system is not
	 * parsing command handler to print help message. It must
	 * be done explicitly. But no need to use the getopt() or
	 * getopt_long() for just one option. */
	if (argv[1] && (!strcmp("-h", argv[1]) || !strcmp("--help", argv[1]))) {
		shell_help(shell);
		return SHELL_CMD_HELP_PRINTED;
	} else if (argc > 1) {
		shell_error(shell, "Invalid option or usage.");
		return -EINVAL;
	}
#endif /* CONFIG_SHELL_GETOPT */

        shell_print(shell, BRIDLE_MSG_INFO_ZEPHYR "%s", KERNEL_VERSION_STRING);
        shell_print(shell, BRIDLE_MSG_INFO_BRIDLE "%s", BRIDLE_VERSION_STRING);

	return 0;
}

static int cmd_bridle_version_short(const struct shell *shell,
				size_t argc, char** argv)
{
	uint32_t version = sys_bridle_version_get();

        ARG_UNUSED(argc);
        ARG_UNUSED(argv);

        shell_print(shell, BRIDLE_MSG_VERSION "%d.%d.%d",
			SYS_BRIDLE_VER_MAJOR(version),
			SYS_BRIDLE_VER_MINOR(version),
			SYS_BRIDLE_VER_PATCHLEVEL(version));

	return 0;
}

static int cmd_bridle_version_long(const struct shell *shell,
				size_t argc, char** argv)
{
	uint32_t version = sys_bridle_version_get();

        ARG_UNUSED(argc);
        ARG_UNUSED(argv);

        shell_print(shell, BRIDLE_MSG_VERSION "%d.%d.%d.%d",
			SYS_BRIDLE_VER_MAJOR(version),
			SYS_BRIDLE_VER_MINOR(version),
			SYS_BRIDLE_VER_PATCHLEVEL(version),
			SYS_BRIDLE_VERSION_TWEAK(version));

	return 0;
}

static int cmd_bridle_version(const struct shell *shell,
				size_t argc, char **argv)
{
#ifdef CONFIG_SHELL_GETOPT
	/* When getopt() is active, the shell sub-system is not
	 * parsing command handler to print help message. It must
	 * be done explicitly. But no need to use the getopt() or
	 * getopt_long() for just one option. */
	if (argv[1] && (!strcmp("-h", argv[1]) || !strcmp("--help", argv[1]))) {
		shell_help(shell);
		return SHELL_CMD_HELP_PRINTED;
	}
#endif /* CONFIG_SHELL_GETOPT */

	if (argc == 2) {
		shell_error(shell, "%s:%s%s", argv[0],
			    BRIDLE_MSG_UNKNOWN_PARAMETER, argv[1]);
		return -EINVAL;
	}

	return cmd_bridle_version_short(shell, argc, argv);
}

SHELL_STATIC_SUBCMD_SET_CREATE(m_sub_version,
	SHELL_CMD_ARG(short, NULL, BRIDLE_HELP_VERSION_SHORT,
		cmd_bridle_version_short, 1, 0),
	SHELL_CMD_ARG(long, NULL, BRIDLE_HELP_VERSION_LONG,
		cmd_bridle_version_long, 1, 0),
	SHELL_SUBCMD_SET_END
);

SHELL_STATIC_SUBCMD_SET_CREATE(m_sub_bridle,
	SHELL_CMD(info, NULL, BRIDLE_HELP_INFO, cmd_bridle_info),
	SHELL_CMD_ARG(version, &m_sub_version, BRIDLE_HELP_VERSION,
		cmd_bridle_version, 1, 1),
	SHELL_SUBCMD_SET_END
);

SHELL_CMD_REGISTER(bridle, &m_sub_bridle, BRIDLE_HELP_BRIDLE, NULL);
