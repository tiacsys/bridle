# Copyright (c) 2023-2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

find_package(Bridle REQUIRED HINTS $ENV{BRIDLE_BASE})
project(grove_x_grove_testbed_shield)

target_sources(app PRIVATE src/main.c)

function(test_if config node_alias node_label node_dscr)
  if(${config})
    dt_alias(alias_path PROPERTY "${node_alias}")
    dt_nodelabel(node_path NODELABEL "${node_label}")
    if(DEFINED alias_path AND DEFINED node_path AND
       "${alias_path}" STREQUAL "${node_path}")
      dt_prop(alias_prop PATH "${alias_path}" PROPERTY "label")
      if(DEFINED alias_prop AND "${alias_prop}" STREQUAL "${node_dscr}")
        message(STATUS "Found alias \"${node_alias}\" "
                         "for label \"${node_label}\" "
                                "at \"${alias_path}\" "
                                "as \"${alias_prop}\"")
      else()
        message(FATAL_ERROR "Test failed, "
          "actual either "
          "the node path \"${alias_path}\" at alias \"${node_alias}\" "
          "was not found or has no \"label\" property with \"${node_dscr}\" or "
          "the node labels are missing or misspelled."
        )
      endif()
    else()
      message(FATAL_ERROR "Test failed, "
        "actual "
        "the node path \"${alias_path}\" at alias \"${node_alias}\" or "
        "the node path \"${node_path}\" at label \"${node_label}\" "
        "was not found in DTS."
      )
    endif()
  endif()
endfunction()

if(NOT CONFIG_SHIELD_X_GROVE_TESTBED)
  message(FATAL_ERROR "Test failed, "
    "actual CONFIG_SHIELD_X_GROVE_TESTBED=${CONFIG_SHIELD_X_GROVE_TESTBED}, "
    "expected CONFIG_SHIELD_X_GROVE_TESTBED=y"
  )
endif()

if(NOT CONFIG_SHIELD_X_GROVE_TESTBED_SINGLE_BOARD)

  if(NOT CONFIG_BOARD_XIAO_SAMD21 AND
     NOT CONFIG_BOARD_SEEEDUINO_XIAO AND
     NOT CONFIG_BOARD_RPI_PICO AND
     NOT CONFIG_BOARD_RPI_PICO2 AND
     NOT CONFIG_BOARD_WAVESHARE_RP2040_PICO AND
     NOT CONFIG_BOARD_WAVESHARE_RP2350_PICO AND
     NOT CONFIG_SHIELD_SEEED_GROVE_BASE_V2)
    message(FATAL_ERROR "Test failed, "
      "actual CONFIG_SHIELD_SEEED_GROVE_BASE_V2=${CONFIG_SHIELD_SEEED_GROVE_BASE_V2}, "
      "expected CONFIG_SHIELD_SEEED_GROVE_BASE_V2=y"
    )
  endif()

  if( (  CONFIG_BOARD_XIAO_SAMD21 OR
         CONFIG_BOARD_SEEEDUINO_XIAO ) AND
     NOT CONFIG_SHIELD_SEEED_GROVE_XIAO_V1)
    message(FATAL_ERROR "Test failed, "
      "actual CONFIG_SHIELD_SEEED_GROVE_XIAO_V1=${CONFIG_SHIELD_SEEED_GROVE_XIAO_V1}, "
      "expected CONFIG_SHIELD_SEEED_GROVE_XIAO_V1=y"
    )
  endif()

  if( (  CONFIG_BOARD_RPI_PICO OR
         CONFIG_BOARD_RPI_PICO2 OR
         CONFIG_BOARD_WAVESHARE_RP2040_PICO OR
         CONFIG_BOARD_WAVESHARE_RP2350_PICO ) AND
     NOT CONFIG_SHIELD_SEEED_GROVE_RPIPICO_V1)
    message(FATAL_ERROR "Test failed, "
      "actual CONFIG_SHIELD_SEEED_GROVE_RPIPICO_V1=${CONFIG_SHIELD_SEEED_GROVE_RPIPICO_V1}, "
      "expected CONFIG_SHIELD_SEEED_GROVE_RPIPICO_V1=y"
    )
  endif()

endif()

if(CONFIG_SHIELD_SEEED_GROVE_BASE_V2)

  if(NOT CONFIG_SHIELD_GROVE_BTN)
    message(FATAL_ERROR "Test failed, "
      "actual CONFIG_SHIELD_GROVE_BTN=${CONFIG_SHIELD_GROVE_BTN}, "
      "expected CONFIG_SHIELD_GROVE_BTN=y"
    )
  else()

    if(CONFIG_BOARD_ARDUINO_ZERO OR
       CONFIG_BOARD_SEEEDUINO_CM0 OR
       CONFIG_BOARD_SEEEDUINO_LOTUS)

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_BTN "sw0" "grove_btn_d7" "Grove Button D7")
      # zephyr-keep-sorted-stop

    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_BTN "sw0" "grove_btn_d4" "Grove Button D4")
      # zephyr-keep-sorted-stop

    endif()

  endif()

  if(NOT CONFIG_SHIELD_GROVE_LED)
    message(FATAL_ERROR "Test failed, "
      "actual CONFIG_SHIELD_GROVE_LED=${CONFIG_SHIELD_GROVE_LED}, "
      "expected CONFIG_SHIELD_GROVE_LED=y"
    )
  else()

    # zephyr-keep-sorted-start re(^\s+\w)
    test_if(CONFIG_SHIELD_GROVE_LED "led0" "grove_led_d6" "Grove LED D6")
    # zephyr-keep-sorted-stop

  endif()

  if(CONFIG_BOARD_NUCLEO_F303RE OR
     CONFIG_BOARD_NUCLEO_F401RE OR
     CONFIG_BOARD_NUCLEO_F413ZH OR
     CONFIG_BOARD_NUCLEO_F767ZI OR
     CONFIG_BOARD_ARDUINO_ZERO OR
     CONFIG_BOARD_SEEEDUINO_CM0)

    if(NOT CONFIG_SHIELD_GROVE_PWM_LED)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_PWM_LED=${CONFIG_SHIELD_GROVE_PWM_LED}, "
        "expected CONFIG_SHIELD_GROVE_PWM_LED=y"
      )
    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_PWM_LED "pwm-led0" "grove_pwm_led_d6" "Grove LED D6")
      # zephyr-keep-sorted-stop

    endif()

  endif()

endif()

if(CONFIG_SHIELD_SEEED_GROVE_XIAO_V1)

  if(NOT CONFIG_SHIELD_GROVE_BTN)
    message(FATAL_ERROR "Test failed, "
      "actual CONFIG_SHIELD_GROVE_BTN=${CONFIG_SHIELD_GROVE_BTN}, "
      "expected CONFIG_SHIELD_GROVE_BTN=y"
    )
  else()

    # zephyr-keep-sorted-start re(^\s+\w)
    test_if(CONFIG_SHIELD_GROVE_BTN "sw0" "grove_btn_d0" "Grove Button D0")
    # zephyr-keep-sorted-stop

  endif()

  if(NOT CONFIG_SHIELD_GROVE_LED)
    message(FATAL_ERROR "Test failed, "
      "actual CONFIG_SHIELD_GROVE_LED=${CONFIG_SHIELD_GROVE_LED}, "
      "expected CONFIG_SHIELD_GROVE_LED=y"
    )
  else()

    # zephyr-keep-sorted-start re(^\s+\w)
    test_if(CONFIG_SHIELD_GROVE_LED "led0" "grove_led_d1" "Grove LED D1")
    # zephyr-keep-sorted-stop

  endif()

  if(CONFIG_BOARD_XIAO_SAMD21 OR
     CONFIG_BOARD_SEEEDUINO_XIAO)

    if(NOT CONFIG_SHIELD_GROVE_PWM_LED)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_PWM_LED=${CONFIG_SHIELD_GROVE_PWM_LED}, "
        "expected CONFIG_SHIELD_GROVE_PWM_LED=y"
      )
    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_PWM_LED "pwm-led0" "grove_pwm_led_d1" "Grove LED D1")
      # zephyr-keep-sorted-stop

    endif()

  endif()

endif()

if(CONFIG_SHIELD_SEEED_GROVE_RPIPICO_V1)

  if(NOT CONFIG_SHIELD_GROVE_BTN)
    message(FATAL_ERROR "Test failed, "
      "actual CONFIG_SHIELD_GROVE_BTN=${CONFIG_SHIELD_GROVE_BTN}, "
      "expected CONFIG_SHIELD_GROVE_BTN=y"
    )
  else()

      # zephyr-keep-sorted-start re(^\s+\w)
    test_if(CONFIG_SHIELD_GROVE_BTN "sw0" "grove_btn_d16" "Grove Button D16")
    # zephyr-keep-sorted-stop

  endif()

  if(NOT CONFIG_SHIELD_GROVE_LED)
    message(FATAL_ERROR "Test failed, "
      "actual CONFIG_SHIELD_GROVE_LED=${CONFIG_SHIELD_GROVE_LED}, "
      "expected CONFIG_SHIELD_GROVE_LED=y"
    )
  else()

    # zephyr-keep-sorted-start re(^\s+\w)
    test_if(CONFIG_SHIELD_GROVE_LED "led0" "grove_led_d18" "Grove LED D18")
    # zephyr-keep-sorted-stop

  endif()

  if(CONFIG_BOARD_RPI_PICO OR
     CONFIG_BOARD_RPI_PICO2 OR
     CONFIG_BOARD_WAVESHARE_RP2040_PICO OR
     CONFIG_BOARD_WAVESHARE_RP2350_PICO)

    if(NOT CONFIG_SHIELD_GROVE_PWM_LED)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_PWM_LED=${CONFIG_SHIELD_GROVE_PWM_LED}, "
        "expected CONFIG_SHIELD_GROVE_PWM_LED=y"
      )
    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_PWM_LED "pwm-led0" "grove_pwm_led_d18" "Grove LED D18")
      # zephyr-keep-sorted-stop

    endif()

  endif()

endif()

if(CONFIG_SHIELD_X_GROVE_TESTBED_SINGLE_BOARD)

  if(CONFIG_BOARD_COFFEECALLER_NRF52)

    if(NOT CONFIG_SHIELD_GROVE_BTN)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_BTN=${CONFIG_SHIELD_GROVE_BTN}, "
        "expected CONFIG_SHIELD_GROVE_BTN=y"
      )
    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_BTN "sw0" "grove_btn_d16" "Grove Button D16")
      # zephyr-keep-sorted-stop

    endif()

    if(NOT CONFIG_SHIELD_GROVE_LED)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_LED=${CONFIG_SHIELD_GROVE_LED}, "
        "expected CONFIG_SHIELD_GROVE_LED=y"
      )
    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_LED "led0" "grove_led_d17" "Grove LED D17")
      # zephyr-keep-sorted-stop

    endif()

    # not yet: if(NOT CONFIG_SHIELD_GROVE_PWM_LED)
    # not yet:   message(FATAL_ERROR "Test failed, "
    # not yet:     "actual CONFIG_SHIELD_GROVE_PWM_LED=${CONFIG_SHIELD_GROVE_PWM_LED}, "
    # not yet:     "expected CONFIG_SHIELD_GROVE_PWM_LED=y"
    # not yet:   )
    # not yet: else()

    # not yet:   # zephyr-keep-sorted-start re(^\s+\w)
    # not yet:   test_if(CONFIG_SHIELD_GROVE_PWM_LED "pwm-led0" "grove_pwm_led_d17" "Grove LED D17")
    # not yet:   # zephyr-keep-sorted-stop

    # not yet: endif()

  endif()

  if(CONFIG_BOARD_CYTRON_MAKER_NANO_RP2040)

    if(NOT CONFIG_SHIELD_GROVE_BTN)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_BTN=${CONFIG_SHIELD_GROVE_BTN}, "
        "expected CONFIG_SHIELD_GROVE_BTN=y"
      )
    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_BTN "sw0" "grove_btn_d0" "Grove Button D0")
      # zephyr-keep-sorted-stop

    endif()

    if(NOT CONFIG_SHIELD_GROVE_LED)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_LED=${CONFIG_SHIELD_GROVE_LED}, "
        "expected CONFIG_SHIELD_GROVE_LED=y"
      )
    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_LED "led0" "grove_led_d15" "Grove LED D15")
      # zephyr-keep-sorted-stop

    endif()

    if(NOT CONFIG_SHIELD_GROVE_PWM_LED)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_PWM_LED=${CONFIG_SHIELD_GROVE_PWM_LED}, "
        "expected CONFIG_SHIELD_GROVE_PWM_LED=y"
      )
    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_PWM_LED "pwm-led0" "grove_pwm_led_d15" "Grove LED D15")
      # zephyr-keep-sorted-stop

    endif()

  endif()

  if(CONFIG_BOARD_CYTRON_MAKER_PI_RP2040)

    if(NOT CONFIG_SHIELD_GROVE_BTN)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_BTN=${CONFIG_SHIELD_GROVE_BTN}, "
        "expected CONFIG_SHIELD_GROVE_BTN=y"
      )
    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_BTN "sw0" "grove_btn_d3" "Grove Button D3")
      # zephyr-keep-sorted-stop

    endif()

    if(NOT CONFIG_SHIELD_GROVE_LED)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_LED=${CONFIG_SHIELD_GROVE_LED}, "
        "expected CONFIG_SHIELD_GROVE_LED=y"
      )
    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_LED "led0" "grove_led_d5" "Grove LED D5")
      # zephyr-keep-sorted-stop

    endif()

    if(NOT CONFIG_SHIELD_GROVE_PWM_LED)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_PWM_LED=${CONFIG_SHIELD_GROVE_PWM_LED}, "
        "expected CONFIG_SHIELD_GROVE_PWM_LED=y"
      )
    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_PWM_LED "pwm-led0" "grove_pwm_led_d5" "Grove LED D5")
      # zephyr-keep-sorted-stop

    endif()

  endif()

  if(CONFIG_BOARD_MINI_USB_RP2040 OR CONFIG_BOARD_MINI_USB_RP2350)

    if(NOT CONFIG_SHIELD_GROVE_BTN)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_BTN=${CONFIG_SHIELD_GROVE_BTN}, "
        "expected CONFIG_SHIELD_GROVE_BTN=y"
      )
    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_BTN "sw0" "grove_btn_d16" "Grove Button D16")
      # zephyr-keep-sorted-stop

    endif()

    if(NOT CONFIG_SHIELD_GROVE_LED)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_LED=${CONFIG_SHIELD_GROVE_LED}, "
        "expected CONFIG_SHIELD_GROVE_LED=y"
      )
    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_LED "led0" "grove_led_d17" "Grove LED D17")
      # zephyr-keep-sorted-stop

    endif()

    if(NOT CONFIG_SHIELD_GROVE_PWM_LED)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_PWM_LED=${CONFIG_SHIELD_GROVE_PWM_LED}, "
        "expected CONFIG_SHIELD_GROVE_PWM_LED=y"
      )
    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_PWM_LED "pwm-led0" "grove_pwm_led_d17" "Grove LED D17")
      # zephyr-keep-sorted-stop

    endif()

  endif()

  if(CONFIG_BOARD_SEEEDUINO_LOTUS)

    if(NOT CONFIG_SHIELD_GROVE_BTN)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_BTN=${CONFIG_SHIELD_GROVE_BTN}, "
        "expected CONFIG_SHIELD_GROVE_BTN=y"
      )
    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_BTN "sw0" "grove_btn_d7" "Grove Button D7")
      # zephyr-keep-sorted-stop

    endif()

    if(NOT CONFIG_SHIELD_GROVE_LED)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_LED=${CONFIG_SHIELD_GROVE_LED}, "
        "expected CONFIG_SHIELD_GROVE_LED=y"
      )
    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_LED "led0" "grove_led_d6" "Grove LED D6")
      # zephyr-keep-sorted-stop

    endif()

    if(NOT CONFIG_SHIELD_GROVE_PWM_LED)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_PWM_LED=${CONFIG_SHIELD_GROVE_PWM_LED}, "
        "expected CONFIG_SHIELD_GROVE_PWM_LED=y"
      )
    else()

      # zephyr-keep-sorted-start re(^\s+\w)
      test_if(CONFIG_SHIELD_GROVE_PWM_LED "pwm-led0" "grove_pwm_led_d6" "Grove LED D6")
      # zephyr-keep-sorted-stop

    endif()

  endif()

endif()
