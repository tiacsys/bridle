/*
 * Copyright (c) 2025 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(board_control, CONFIG_BOARD_MINI_USB_RP2350_LOG_LEVEL);

int show_board_target_string(void)
{
	LOG_INF(CONFIG_BOARD_TARGET);
	LOG_INF("QSPI-Flash: %uMB", BOARD_FLASH_SIZE_MB);
	return 0;
}

SYS_INIT_NAMED(board_control, show_board_target_string, POST_KERNEL,
	       CONFIG_BOARD_MINI_USB_RP2350_INIT_PRIORITY);
