# Copyright (c) 2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

math(EXPR BOARD_FLASH_SIZE_MB "${CONFIG_FLASH_SIZE} >> 10" OUTPUT_FORMAT DECIMAL)
zephyr_compile_definitions(BOARD_FLASH_SIZE_MB=${BOARD_FLASH_SIZE_MB})

zephyr_library()

# zephyr-keep-sorted-start
zephyr_library_sources(board_control.c)
# zephyr-keep-sorted-stop
