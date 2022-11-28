# Copyright (c) 2022 TiaC Systems
# Copyright (c) 2020 Kalyan Sriram <coder.kalyan@gmail.com>
# SPDX-License-Identifier: Apache-2.0

board_set_flasher_ifnset(misc-flasher)
board_runner_args(misc-flasher "${BOARD_DIR}/support/misc-flasher")
### NEEDS PATCHES IN DFU_UTIL ### board_runner_args(dfu-util "--pid=0483:df11" "--alt=0" "--dfuse")
board_runner_args(jlink "--device=STM32F401CE" "--speed=4000")

include(${ZEPHYR_BASE}/boards/common/misc.board.cmake)
### NEEDS PATCHES IN DFU_UTIL ### include(${ZEPHYR_BASE}/boards/common/dfu-util.board.cmake)
include(${ZEPHYR_BASE}/boards/common/openocd.board.cmake)
include(${ZEPHYR_BASE}/boards/common/jlink.board.cmake)
include(${ZEPHYR_BASE}/boards/common/blackmagicprobe.board.cmake)
