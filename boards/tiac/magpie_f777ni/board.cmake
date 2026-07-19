# Copyright (c) 2021-2026 TiaC Systems
# Copyright (c) 2021 Li-Pro.Net
# SPDX-License-Identifier: Apache-2.0

message(STATUS "Found BOARD.cmake: ${dir}/board.cmake")

board_runner_args(jlink "--device=STM32F777NI" "--speed=4000")

include(${ZEPHYR_BASE}/boards/common/jlink.board.cmake)
include(${ZEPHYR_BASE}/boards/common/openocd.board.cmake)

# Set flash runner 'openocd' as default
board_set_flasher(openocd)
