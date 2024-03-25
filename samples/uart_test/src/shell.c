/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/shell/shell.h>

#include "main.h"

static int cmd_uart_send(const struct shell *sh, size_t argc, char **argv, void *data) {

    if (argc < 2) {
        shell_print(sh, "Usage: uart send <msg>");
        return -1;
    }

    char *msg = argv[1];

    return uart_send(msg, strlen(msg) + 1);
}

SHELL_STATIC_SUBCMD_SET_CREATE(sub_uart,
    SHELL_CMD(send, NULL, "Send bytes via UART", cmd_uart_send),
    SHELL_SUBCMD_SET_END
);

SHELL_CMD_REGISTER(uart, &sub_uart, "Interact with the selected UART", NULL);
