# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# This configuration allows selecting what debug adapter debugging
# waveshare_rp2350 by a command-line argument. It is mainly intended
# to support both the 'picoprobe' and 'raspberrypi-swd' adapter described
# in "Getting started with Raspberry Pi Pico". Any other SWD debug adapter
# might also be usable with this configuration.

# Set CYTRON_RP2350_DEBUG_ADAPTER to select debug adapter by command-line
# arguments, e.g.:
#
#   west build -b <cytron_motion_rp2350_BOARD_VARIANT> \
#              -- -DCYTRON_RP2350_DEBUG_ADAPTER=raspberrypi-swd
#
# The value is treated as a part of an interface file name contained in the
# debugger configuration file. The value must be the 'stem' part of the name
# of one of the files in the OpenOCD interface configuration file. The setting
# is store to CMakeCache.txt.

if ("${CYTRON_RP2350_DEBUG_ADAPTER}" STREQUAL "")
	set(CYTRON_RP2350_DEBUG_ADAPTER "cmsis-dap")
endif()

board_runner_args(openocd --cmd-pre-init "source [find interface/${CYTRON_RP2350_DEBUG_ADAPTER}.cfg]")
board_runner_args(openocd --cmd-pre-init "transport select swd")
board_runner_args(openocd --cmd-pre-init "source [find target/rp2350.cfg]")

# The adapter speed is expected to be set by interface configuration.
# But if not so, set 2000 to adapter speed.
board_runner_args(openocd --cmd-pre-init "set_adapter_speed_if_not_set 2000")

board_runner_args(jlink "--device=RP2350_M33_0")
board_runner_args(uf2 "--board-id=RP2350")

include(${ZEPHYR_BASE}/boards/common/openocd.board.cmake)
include(${ZEPHYR_BASE}/boards/common/jlink.board.cmake)
include(${ZEPHYR_BASE}/boards/common/uf2.board.cmake)
