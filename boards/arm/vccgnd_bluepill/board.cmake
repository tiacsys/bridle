# Copyright (c) 2022 TiaC Systems
# Copyright (c) 2017, embedjournal.com
# SPDX-License-Identifier: Apache-2.0

# STM32duino bootloader v1.0
# DFU: [1eaf:0003] ver=0201, serial="LLM 003"
# alt=2, name="Upload to Flash 0x8002000"
# alt=1, name="Upload to Flash 0x8005000"
# alt=0, name="ERROR. Upload to RAM not supported."
board_runner_args(dfu-util "--pid=1eaf:0003" "--alt=2")
board_runner_args(jlink "--device=STM32F103C8" "--speed=4000")

include(${ZEPHYR_BASE}/boards/common/dfu-util.board.cmake)
include(${ZEPHYR_BASE}/boards/common/openocd.board.cmake)
include(${ZEPHYR_BASE}/boards/common/jlink.board.cmake)
