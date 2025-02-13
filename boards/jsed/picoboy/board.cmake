# Copyright (c) 2023-2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

if("${NORMALIZED_BOARD_QUALIFIERS}" STREQUAL "_rp2040")
  board_runner_args(uf2 "--board-id=RPI-RP2")
else()
  message(FATAL_ERROR "Unsupported board qualifiers: "
                      "'${NORMALIZED_BOARD_QUALIFIERS}'\n")
endif()

include(${ZEPHYR_BASE}/boards/common/uf2.board.cmake)
