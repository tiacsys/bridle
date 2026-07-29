# SPDX-FileCopyrightText: Copyright (c) 2023-2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

message(STATUS "Found BOARD.cmake: ${dir}/board.cmake")

board_runner_args(uf2 "--board-id=RPI-RP2")

include(${ZEPHYR_BASE}/boards/common/uf2.board.cmake)

# Set flash runner 'uf2' as default
board_set_flasher(uf2)
