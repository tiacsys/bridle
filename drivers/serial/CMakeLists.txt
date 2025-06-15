# Copyright (c) 2024-2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

zephyr_library_amend()

zephyr_library_sources_ifdef(CONFIG_UART_CH32		uart_ch32.c)
zephyr_library_sources_ifdef(CONFIG_UART_SC16IS75X	uart_sc16is75x.c)
