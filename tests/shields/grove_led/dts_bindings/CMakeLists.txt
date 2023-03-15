# Copyright (c) 2023 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(grove_led_shields)

target_sources(app PRIVATE src/main.c)

function(test_if config node_parent node_label node_dscr)
  if(${config})
    dt_nodelabel(node_path NODELABEL "${node_label}")
    if(DEFINED node_path AND "${node_path}" MATCHES "${node_parent}")
      dt_prop(node_prop PATH "${node_path}" PROPERTY "label")
      if(DEFINED node_prop AND "${node_prop}" STREQUAL "${node_dscr}")
        message(STATUS "Found label \"${node_label}\" at \"${node_path}\" "
                                "as \"${node_prop}\"")
      else()
        message(FATAL_ERROR "Test failed, "
          "actual either "
          "the node path \"${node_path}\" at label \"${node_label}\" "
          "was not found or has no \"label\" property with \"${node_dscr}\" or "
          "the node labels are missing or misspelled."
        )
      endif()
    else()
      message(FATAL_ERROR "Test failed, "
        "actual the node path \"${node_path}\" "
        "was not found in DTS at \"${node_parent}\"."
      )
    endif()
  endif()
endfunction()

if(CONFIG_SHIELD_GROVE_LED AND NOT CONFIG_GPIO)
  message(FATAL_ERROR "Test failed, "
    "actual CONFIG_SHIELD_GROVE_LED=${CONFIG_SHIELD_GROVE_LED} "
    "and CONFIG_GPIO=${CONFIG_GPIO}, expected CONFIG_GPIO=y"
  )
endif()

# disabled, because it is too common, GPIO is enabled by nearly all boards
#if(NOT CONFIG_SHIELD_GROVE_LED AND CONFIG_GPIO)
#  message(FATAL_ERROR "Test failed, "
#    "actual CONFIG_SHIELD_GROVE_LED=${CONFIG_SHIELD_GROVE_LED} "
#    "and CONFIG_GPIO=${CONFIG_GPIO}, expected CONFIG_GPIO=n"
#  )
#endif()

if(CONFIG_SHIELD_GROVE_PWM_LED AND NOT CONFIG_PWM)
  message(FATAL_ERROR "Test failed, "
    "actual CONFIG_SHIELD_GROVE_PWM_LED=${CONFIG_SHIELD_GROVE_PWM_LED} "
    "and CONFIG_PWM=${CONFIG_PWM}, expected CONFIG_PWM=y"
  )
endif()

if(NOT CONFIG_SHIELD_GROVE_PWM_LED AND CONFIG_PWM)
  message(FATAL_ERROR "Test failed, "
    "actual CONFIG_SHIELD_GROVE_PWM_LED=${CONFIG_SHIELD_GROVE_PWM_LED} "
    "and CONFIG_PWM=${CONFIG_PWM}, expected CONFIG_PWM=n"
  )
endif()

test_if(CONFIG_SHIELD_GROVE_LED_D0 "/grove_leds" "grove_led_d0" "Grove LED D0")
test_if(CONFIG_SHIELD_GROVE_LED_D1 "/grove_leds" "grove_led_d1" "Grove LED D1")
test_if(CONFIG_SHIELD_GROVE_LED_D2 "/grove_leds" "grove_led_d2" "Grove LED D2")
test_if(CONFIG_SHIELD_GROVE_LED_D3 "/grove_leds" "grove_led_d3" "Grove LED D3")
test_if(CONFIG_SHIELD_GROVE_LED_D4 "/grove_leds" "grove_led_d4" "Grove LED D4")
test_if(CONFIG_SHIELD_GROVE_LED_D5 "/grove_leds" "grove_led_d5" "Grove LED D5")
test_if(CONFIG_SHIELD_GROVE_LED_D6 "/grove_leds" "grove_led_d6" "Grove LED D6")
test_if(CONFIG_SHIELD_GROVE_LED_D7 "/grove_leds" "grove_led_d7" "Grove LED D7")
test_if(CONFIG_SHIELD_GROVE_LED_D8 "/grove_leds" "grove_led_d8" "Grove LED D8")
test_if(CONFIG_SHIELD_GROVE_LED_D9 "/grove_leds" "grove_led_d9" "Grove LED D9")
test_if(CONFIG_SHIELD_GROVE_LED_D10 "/grove_leds" "grove_led_d10" "Grove LED D10")
test_if(CONFIG_SHIELD_GROVE_LED_D11 "/grove_leds" "grove_led_d11" "Grove LED D11")
test_if(CONFIG_SHIELD_GROVE_LED_D12 "/grove_leds" "grove_led_d12" "Grove LED D12")
test_if(CONFIG_SHIELD_GROVE_LED_D13 "/grove_leds" "grove_led_d13" "Grove LED D13")
test_if(CONFIG_SHIELD_GROVE_LED_D14 "/grove_leds" "grove_led_d14" "Grove LED D14")
test_if(CONFIG_SHIELD_GROVE_LED_D15 "/grove_leds" "grove_led_d15" "Grove LED D15")
test_if(CONFIG_SHIELD_GROVE_LED_D16 "/grove_leds" "grove_led_d16" "Grove LED D16")
test_if(CONFIG_SHIELD_GROVE_LED_D17 "/grove_leds" "grove_led_d17" "Grove LED D17")
test_if(CONFIG_SHIELD_GROVE_LED_D18 "/grove_leds" "grove_led_d18" "Grove LED D18")
test_if(CONFIG_SHIELD_GROVE_LED_D19 "/grove_leds" "grove_led_d19" "Grove LED D19")
test_if(CONFIG_SHIELD_GROVE_LED_D20 "/grove_leds" "grove_led_d20" "Grove LED D20")
test_if(CONFIG_SHIELD_GROVE_LED_D21 "/grove_leds" "grove_led_d21" "Grove LED D21")
test_if(CONFIG_SHIELD_GROVE_LED_D22 "/grove_leds" "grove_led_d22" "Grove LED D22")
test_if(CONFIG_SHIELD_GROVE_LED_D23 "/grove_leds" "grove_led_d23" "Grove LED D23")
test_if(CONFIG_SHIELD_GROVE_LED_D24 "/grove_leds" "grove_led_d24" "Grove LED D24")
test_if(CONFIG_SHIELD_GROVE_LED_D25 "/grove_leds" "grove_led_d25" "Grove LED D25")
test_if(CONFIG_SHIELD_GROVE_LED_D26 "/grove_leds" "grove_led_d26" "Grove LED D26")
test_if(CONFIG_SHIELD_GROVE_LED_D27 "/grove_leds" "grove_led_d27" "Grove LED D27")
test_if(CONFIG_SHIELD_GROVE_LED_D28 "/grove_leds" "grove_led_d28" "Grove LED D28")
test_if(CONFIG_SHIELD_GROVE_LED_D29 "/grove_leds" "grove_led_d29" "Grove LED D29")
test_if(CONFIG_SHIELD_GROVE_LED_D30 "/grove_leds" "grove_led_d30" "Grove LED D30")
test_if(CONFIG_SHIELD_GROVE_LED_D31 "/grove_leds" "grove_led_d31" "Grove LED D31")

test_if(CONFIG_SHIELD_GROVE_PWM_LED_D0 "/grove_pwm_leds" "grove_pwm_led_d0" "Grove LED D0")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D1 "/grove_pwm_leds" "grove_pwm_led_d1" "Grove LED D1")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D2 "/grove_pwm_leds" "grove_pwm_led_d2" "Grove LED D2")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D3 "/grove_pwm_leds" "grove_pwm_led_d3" "Grove LED D3")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D4 "/grove_pwm_leds" "grove_pwm_led_d4" "Grove LED D4")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D5 "/grove_pwm_leds" "grove_pwm_led_d5" "Grove LED D5")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D6 "/grove_pwm_leds" "grove_pwm_led_d6" "Grove LED D6")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D7 "/grove_pwm_leds" "grove_pwm_led_d7" "Grove LED D7")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D8 "/grove_pwm_leds" "grove_pwm_led_d8" "Grove LED D8")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D9 "/grove_pwm_leds" "grove_pwm_led_d9" "Grove LED D9")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D10 "/grove_pwm_leds" "grove_pwm_led_d10" "Grove LED D10")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D11 "/grove_pwm_leds" "grove_pwm_led_d11" "Grove LED D11")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D12 "/grove_pwm_leds" "grove_pwm_led_d12" "Grove LED D12")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D13 "/grove_pwm_leds" "grove_pwm_led_d13" "Grove LED D13")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D14 "/grove_pwm_leds" "grove_pwm_led_d14" "Grove LED D14")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D15 "/grove_pwm_leds" "grove_pwm_led_d15" "Grove LED D15")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D16 "/grove_pwm_leds" "grove_pwm_led_d16" "Grove LED D16")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D17 "/grove_pwm_leds" "grove_pwm_led_d17" "Grove LED D17")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D18 "/grove_pwm_leds" "grove_pwm_led_d18" "Grove LED D18")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D19 "/grove_pwm_leds" "grove_pwm_led_d19" "Grove LED D19")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D20 "/grove_pwm_leds" "grove_pwm_led_d20" "Grove LED D20")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D21 "/grove_pwm_leds" "grove_pwm_led_d21" "Grove LED D21")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D22 "/grove_pwm_leds" "grove_pwm_led_d22" "Grove LED D22")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D23 "/grove_pwm_leds" "grove_pwm_led_d23" "Grove LED D23")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D24 "/grove_pwm_leds" "grove_pwm_led_d24" "Grove LED D24")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D25 "/grove_pwm_leds" "grove_pwm_led_d25" "Grove LED D25")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D26 "/grove_pwm_leds" "grove_pwm_led_d26" "Grove LED D26")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D27 "/grove_pwm_leds" "grove_pwm_led_d27" "Grove LED D27")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D28 "/grove_pwm_leds" "grove_pwm_led_d28" "Grove LED D28")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D29 "/grove_pwm_leds" "grove_pwm_led_d29" "Grove LED D29")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D30 "/grove_pwm_leds" "grove_pwm_led_d30" "Grove LED D30")
test_if(CONFIG_SHIELD_GROVE_PWM_LED_D31 "/grove_pwm_leds" "grove_pwm_led_d31" "Grove LED D31")
