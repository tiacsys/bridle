# Copyright (c) 2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

message(STATUS "Including BOARD.cmake: ${board_extension_dir}/board.cmake")

set(DEFAULT_BOSSAC_PORT "/dev/serial/by-id/usb-Arduino_LLC_Arduino_Zero-if00")
message(STATUS "overriding FLASH runner bossac PORT; it's now ${DEFAULT_BOSSAC_PORT}")

board_set_flasher(bossac)
board_runner_args(bossac "--bossac-port=${DEFAULT_BOSSAC_PORT}")
include("${ZEPHYR_BASE}/boards/common/bossac.board.cmake")
