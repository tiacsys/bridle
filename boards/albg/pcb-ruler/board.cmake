if (DEFINED ENV{WCH_RISCV_OPENOCD_BIN}) # specify openocd like from https://github.com/dragonlock2/miscboards/tree/main/wch
    set(OPENOCD $ENV{WCH_RISCV_OPENOCD_BIN})
endif()

board_runner_args(openocd "--config=${CMAKE_CURRENT_LIST_DIR}/support/wch-riscv.cfg") # from http://www.mounriver.com/download

include(${ZEPHYR_BASE}/boards/common/openocd.board.cmake)
