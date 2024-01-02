/*
 * Copyright (c) 2021-2023 TiaC Systems
 * Copyright (c) 2019-2021 Li-Pro.Net
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/shell/shell.h>

static int cmd_hello(const struct shell *shell, size_t argc, char** argv)
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

        shell_print(shell, "Hello from shell.");

	return 0;
}

SHELL_CMD_REGISTER(hello, NULL, "say hello", cmd_hello);
