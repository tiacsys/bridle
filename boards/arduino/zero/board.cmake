# Copyright (c) 2024-2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

message(STATUS "Found BOARD.cmake: ${dir}/board.cmake")

set(DEFAULT_BOSSAC_PORT "/dev/serial/by-id/usb-Arduino_LLC_Arduino_Zero-if00")
message(STATUS "overriding FLASH runner bossac PORT; it's now ${DEFAULT_BOSSAC_PORT}")

board_runner_args(bossac "--bossac-port=${DEFAULT_BOSSAC_PORT}")
include("${ZEPHYR_BASE}/boards/common/bossac.board.cmake")

# Set flash runner 'bossac' as default
board_set_flasher(bossac)
