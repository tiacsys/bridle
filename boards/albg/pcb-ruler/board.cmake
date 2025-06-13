# Copyright (c) 2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# specify openocd like from https://github.com/dragonlock2/miscboards/tree/main/wch
if (DEFINED ENV{WCH_RISCV_OPENOCD_PATH})

  if(NOT "${OPENOCD}" MATCHES "^$ENV{WCH_RISCV_OPENOCD_PATH}/.*")
    set(OPENOCD OPENOCD-NOTFOUND)
  endif()

find_program(OPENOCD openocd PATHS $ENV{WCH_RISCV_OPENOCD_PATH} NO_DEFAULT_PATH)

endif()

board_runner_args(minichlink)
include(${ZEPHYR_BASE}/boards/common/minichlink.board.cmake)

# wch-riscv.cfg as support/openocd.cfg from http://www.mounriver.com/download
board_runner_args(openocd "--use-elf" "--cmd-reset-halt" "halt")
include(${ZEPHYR_BASE}/boards/common/openocd.board.cmake)
