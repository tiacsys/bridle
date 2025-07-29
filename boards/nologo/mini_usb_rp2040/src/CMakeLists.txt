# Copyright (c) 2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

math(EXPR BOARD_FLASH_SIZE_MB "${CONFIG_FLASH_SIZE} >> 10" OUTPUT_FORMAT DECIMAL)
zephyr_compile_definitions(BOARD_FLASH_SIZE_MB=${BOARD_FLASH_SIZE_MB})

zephyr_library()
zephyr_library_sources(board_control.c)

if ("${BOARD_REVISION}" STREQUAL "chipled")
  if (CONFIG_DT_HAS_PWM_LEDS_ENABLED)
    zephyr_library_sources(chipled_pwm_chipled_off.c)
  elseif (CONFIG_DT_HAS_GPIO_LEDS_ENABLED)
    zephyr_library_sources(chipled_gpio_chipled_off.c)
  else()
    message(FATAL_ERROR "Chip-LED throttling needs either PWM (primary) "
                        "or GPIO (secondary) driver support.")
  endif()
endif()
