# Copyright (c) 2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

math(EXPR BOARD_FLASH_SIZE_MB "${CONFIG_FLASH_SIZE} >> 10" OUTPUT_FORMAT DECIMAL)
zephyr_compile_definitions(BOARD_FLASH_SIZE_MB=${BOARD_FLASH_SIZE_MB})

zephyr_library()

# zephyr-keep-sorted-start
zephyr_library_sources(board_control.c)
# zephyr-keep-sorted-stop

if ("${BOARD_REVISION}" STREQUAL "chipled")
  if (CONFIG_DT_HAS_PWM_LEDS_ENABLED)
    # zephyr-keep-sorted-start
    zephyr_library_sources(chipled_pwm_chipled_off.c)
    # zephyr-keep-sorted-stop
  elseif (CONFIG_DT_HAS_GPIO_LEDS_ENABLED)
    # zephyr-keep-sorted-start
    zephyr_library_sources(chipled_gpio_chipled_off.c)
    # zephyr-keep-sorted-stop
  else()
    message(FATAL_ERROR "Chip-LED throttling needs either PWM (primary) "
                        "or GPIO (secondary) driver support.")
  endif()
endif()
