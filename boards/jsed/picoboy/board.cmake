# Copyright (c) 2023-2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

if("${NORMALIZED_BOARD_TARGET}" STREQUAL "picoboy_rp2040")
  set(BOARD_FULL_NAME "The PicoBoy Mini-Handheld")
elseif("${NORMALIZED_BOARD_TARGET}" STREQUAL "picoboy_rp2040_color")
  set(BOARD_FULL_NAME "The PicoBoy Color (PBC) Mini-Handheld")
else()
  message(FATAL_ERROR "Unsupported board variant: "
                      "'${BOARD}${BOARD_QUALIFIERS}'\n")
endif()

message(NOTICE "\n"
  "\t---------------------------------------------------------------------\n"
  "\t--- Build for: '${BOARD_FULL_NAME}'\n"
  "\t---------------------------------------------------------------------\n"
  )

board_runner_args(uf2 "--board-id=RPI-RP2")
include(${ZEPHYR_BASE}/boards/common/uf2.board.cmake)
