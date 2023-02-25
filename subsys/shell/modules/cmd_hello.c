/*
 * Copyright (c) 2021-2023 TiaC Systems
 * Copyright (c) 2019-2021 Li-Pro.Net
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/sys/printk.h>
#include <zephyr/shell/shell.h>

static int cmd_hello(const struct shell *shell, size_t argc, char** argv)
{
        ARG_UNUSED(argc);
        ARG_UNUSED(argv);

        shell_print(shell, "Hello from shell.");

	return 0;
}

SHELL_CMD_ARG_REGISTER(hello, NULL, "say hello", cmd_hello, 1, 0);
