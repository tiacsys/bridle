# Copyright (c) 2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

set(SUPPORT_STM32CUBEPROGRAMMER FALSE)
set(SUPPORT_OPENOCD_STM32 FALSE)
set(SUPPORT_JLINK FALSE)
set(SUPPORT_PYOCD FALSE)

if(CONFIG_BOARD_VCCGND_BLUEPILL_STM32F103C8)

  set(SUPPORT_STM32CUBEPROGRAMMER TRUE)
  set(STM32CUBEPROGRAMMER_PORT "uart")	# possible "uart", "jlink", "swd", "jtag"

  set(SUPPORT_OPENOCD_STM32 TRUE)
  set(OPENOCD_INTERFACE "cmsis-dap")	# possible "cmsis-dap", "jlink"
  set(OPENOCD_TRANSPORT "swd")		# possible "swd", "jtag"
  set(OPENOCD_TARGET "stm32f1x")

  set(SUPPORT_JLINK TRUE)
  set(JLINK_DEVICE "STM32F103C8")

  set(SUPPORT_PYOCD TRUE)
  set(PYOCD_TARGET "stm32f103c8")

elseif(CONFIG_BOARD_VCCGND_BLUEPILL_STM32F103CB)

  set(SUPPORT_STM32CUBEPROGRAMMER TRUE)
  set(STM32CUBEPROGRAMMER_PORT "uart")	# possible "uart", "jlink", "swd", "jtag"

  set(SUPPORT_OPENOCD_STM32 TRUE)
  set(OPENOCD_INTERFACE "cmsis-dap")	# possible "cmsis-dap", "jlink"
  set(OPENOCD_TRANSPORT "swd")		# possible "swd", "jtag"
  set(OPENOCD_TARGET "stm32f1x")

  set(SUPPORT_JLINK TRUE)
  set(JLINK_DEVICE "STM32F103CB")

  set(SUPPORT_PYOCD TRUE)
  set(PYOCD_TARGET "stm32f103cb")

elseif(CONFIG_BOARD_VCCGND_BLUEPILL_STM32F072C8)

  set(SUPPORT_STM32CUBEPROGRAMMER TRUE)
  set(STM32CUBEPROGRAMMER_PORT "uart")	# possible "uart", "jlink", "swd", "jtag"

  set(SUPPORT_OPENOCD_STM32 TRUE)
  set(OPENOCD_INTERFACE "cmsis-dap")	# possible "cmsis-dap", "jlink"
  set(OPENOCD_TRANSPORT "swd")		# possible "swd", "jtag"
  set(OPENOCD_TARGET "stm32f0x")

  set(SUPPORT_JLINK TRUE)
  set(JLINK_DEVICE "STM32F072C8")

  set(SUPPORT_PYOCD TRUE)
  set(PYOCD_TARGET "stm32f072c8")

elseif(CONFIG_BOARD_VCCGND_BLUEPILL_STM32F072CB)

  set(SUPPORT_STM32CUBEPROGRAMMER TRUE)
  set(STM32CUBEPROGRAMMER_PORT "uart")	# possible "uart", "jlink", "swd", "jtag"

  set(SUPPORT_OPENOCD_STM32 TRUE)
  set(OPENOCD_INTERFACE "cmsis-dap")	# possible "cmsis-dap", "jlink"
  set(OPENOCD_TRANSPORT "swd")		# possible "swd", "jtag"
  set(OPENOCD_TARGET "stm32f0x")

  set(SUPPORT_JLINK TRUE)
  set(JLINK_DEVICE "STM32F072CB")

  set(SUPPORT_PYOCD TRUE)
  set(PYOCD_TARGET "stm32f072cb")

elseif(CONFIG_BOARD_VCCGND_BLUEPILL_STM32F051C8)

  set(SUPPORT_STM32CUBEPROGRAMMER TRUE)
  set(STM32CUBEPROGRAMMER_PORT "uart")	# possible "uart", "jlink", "swd", "jtag"

  set(SUPPORT_OPENOCD_STM32 TRUE)
  set(OPENOCD_INTERFACE "cmsis-dap")	# possible "cmsis-dap", "jlink"
  set(OPENOCD_TRANSPORT "swd")		# possible "swd", "jtag"
  set(OPENOCD_TARGET "stm32f0x")

  set(SUPPORT_JLINK TRUE)
  set(JLINK_DEVICE "STM32F051C8")

  set(SUPPORT_PYOCD TRUE)
  set(PYOCD_TARGET "stm32f051c8")

elseif(CONFIG_BOARD_VCCGND_BLUEPILL_STM32F030C8)

  set(SUPPORT_STM32CUBEPROGRAMMER TRUE)
  set(STM32CUBEPROGRAMMER_PORT "uart")	# possible "uart", "jlink", "swd", "jtag"

  set(SUPPORT_OPENOCD_STM32 TRUE)
  set(OPENOCD_INTERFACE "cmsis-dap")	# possible "cmsis-dap", "jlink"
  set(OPENOCD_TRANSPORT "swd")		# possible "swd", "jtag"
  set(OPENOCD_TARGET "stm32f0x")

  set(SUPPORT_JLINK TRUE)
  set(JLINK_DEVICE "STM32F030C8")

  set(SUPPORT_PYOCD TRUE)
  set(PYOCD_TARGET "stm32f030c8")

else()
  message(FATAL_ERROR "Unsupported SoC selection in VccGND BluePill board list.")
endif()

# keep order

if(SUPPORT_STM32CUBEPROGRAMMER)
  if("${STM32CUBEPROGRAMMER_PORT}" STREQUAL "uart")
    board_runner_args(stm32cubeprogrammer "--port=ttyACM0")
  else()
    board_runner_args(stm32cubeprogrammer "--port=${STM32CUBEPROGRAMMER_PORT}" "--reset-mode=sw")
  endif()
  include(${ZEPHYR_BASE}/boards/common/stm32cubeprogrammer.board.cmake)
endif()

if(SUPPORT_OPENOCD_STM32)
  board_runner_args(openocd --config "openocd.${OPENOCD_INTERFACE}.${OPENOCD_TRANSPORT}.${OPENOCD_TARGET}.cfg")
  include(${ZEPHYR_BASE}/boards/common/openocd-stm32.board.cmake)
endif()

if(SUPPORT_JLINK)
  board_runner_args(jlink "--device=${JLINK_DEVICE}" "--speed=4000")
  include(${ZEPHYR_BASE}/boards/common/jlink.board.cmake)
endif()

if(SUPPORT_PYOCD)
  board_runner_args(pyocd "--target=${PYOCD_TARGET}")
  include(${ZEPHYR_BASE}/boards/common/pyocd.board.cmake)
endif()
