# Copyright (c) 2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

if (CONFIG_BOARD_MINI_USB_RP2040 AND "${BOARD_REVISION}" STREQUAL "chipled")
  zephyr_sources(chipid_board_control.c)
  zephyr_sources_ifdef(CONFIG_DT_HAS_GPIO_LEDS_ENABLED chipid_gpio_led0_off.c)
  zephyr_sources_ifdef(CONFIG_DT_HAS_PWM_LEDS_ENABLED chipid_pwm_led0_off.c)
endif()
