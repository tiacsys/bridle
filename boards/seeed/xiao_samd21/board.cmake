# Copyright (c) 2020 Google LLC.
# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

message(STATUS "Found BOARD.cmake: ${dir}/board.cmake")

include(${ZEPHYR_BASE}/boards/common/openocd.board.cmake)
include(${ZEPHYR_BASE}/boards/common/bossac.board.cmake)

# Set flash runner 'bossac' as default
board_set_flasher(bossac)
