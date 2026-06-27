# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 inovex GmbH
#
# Board extension for nucleo_n657x0_q.
#
# Registers the stm32n6_boot runner as the default flash runner.  That runner
# is a thin wrapper around stm32cubeprogrammer that asserts/de-asserts the
# external flash program pin via a UART-controlled helper board and power-cycles
# the target before and after programming.
#
# The boot pin controller serial device must be supplied at flash time:
#
#   west flash -- --boot-device=/dev/ttyACM1
#
# or through the N6_BOOT_CTRL_DEVICE environment variable, or by setting it
# persistently in the cmake cache:
#
#   cmake -DN6_BOOT_CTRL_DEVICE=/dev/ttyACM1 ...
#
# The stm32cubeprogrammer arguments below mirror the upstream board.cmake so
# that the wrapper runner receives the same flash configuration.

if(CONFIG_STM32N6_BOOT_SERIAL)
  board_runner_args(stm32n6_boot "--port=usb1")
  board_runner_args(stm32n6_boot "--download-modifiers=0x1")
  board_runner_args(stm32n6_boot "--start-modifiers=noack")
else()
  board_runner_args(stm32n6_boot "--port=swd")
  board_runner_args(stm32n6_boot "--no-reset")
  board_runner_args(stm32n6_boot "--tool-opt= mode=HOTPLUG ap=1")
  board_runner_args(stm32n6_boot "--extload=MX25UM51245G_STM32N6570-NUCLEO.stldr")
  board_runner_args(stm32n6_boot "--download-address=0x70000000")
endif()

# Boot pin controller device — can be set via cmake cache variable or env var.
if(DEFINED N6_BOOT_CTRL_DEVICE)
  board_runner_args(stm32n6_boot "--boot-device=${N6_BOOT_CTRL_DEVICE}")
elseif(DEFINED ENV{N6_BOOT_CTRL_DEVICE})
  board_runner_args(stm32n6_boot "--boot-device=$ENV{N6_BOOT_CTRL_DEVICE}")
endif()

board_set_flasher(stm32n6_boot)
board_finalize_runner_args(stm32n6_boot)
