# Copyright (c) 2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# Add to the existing display library from zephyr instead of defining our own.
# It is actually required to add display drivers to that library, otherwise
# build errors can occur!
zephyr_library_amend()

zephyr_library_sources_ifdef(CONFIG_CLOCK_CONTROL_CH32_RCC clock_control_ch32_rcc.c)
