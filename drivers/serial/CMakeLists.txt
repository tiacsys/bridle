# Copyright (c) 2024-2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# Add to the existing serial library from Zephyr instead of defining our own.
# It is actually required to add serial drivers to that library, otherwise
# build errors can occur!
zephyr_library_amend()

# zephyr-keep-sorted-start
zephyr_library_sources_ifdef(CONFIG_UART_SC16IS75X	uart_sc16is75x.c)
# zephyr-keep-sorted-stop
