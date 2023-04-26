# Copyright (c) 2023 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
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
          "was not found or has no \"label\" property with \"${alias_dscr}\" or "
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

if(NOT CONFIG_HAS_RPI_PICO AND NOT CONFIG_SHIELD_SEEED_GROVE_BASE_V2)
  message(FATAL_ERROR "Test failed, "
    "actual CONFIG_SHIELD_SEEED_GROVE_BASE_V2=${CONFIG_SHIELD_SEEED_GROVE_BASE_V2}, "
    "expected CONFIG_SHIELD_SEEED_GROVE_BASE_V2=y"
  )
endif()

if(CONFIG_HAS_RPI_PICO AND NOT CONFIG_SHIELD_SEEED_GROVE_RPIPICO_V1)
  message(FATAL_ERROR "Test failed, "
    "actual CONFIG_SHIELD_SEEED_GROVE_RPIPICO_V1=${CONFIG_SHIELD_SEEED_GROVE_RPIPICO_V1}, "
    "expected CONFIG_SHIELD_SEEED_GROVE_RPIPICO_V1=y"
  )
endif()

if(CONFIG_SHIELD_SEEED_GROVE_BASE_V2)

  if(NOT CONFIG_SHIELD_GROVE_BTN)
    message(FATAL_ERROR "Test failed, "
      "actual CONFIG_SHIELD_GROVE_BTN=${CONFIG_SHIELD_GROVE_BTN}, "
      "expected CONFIG_SHIELD_GROVE_BTN=y"
    )
  else()

    test_if(CONFIG_SHIELD_GROVE_BTN "sw0" "grove_btn_d4" "Grove Button D4")

  endif()

  if(NOT CONFIG_SHIELD_GROVE_LED)
    message(FATAL_ERROR "Test failed, "
      "actual CONFIG_SHIELD_GROVE_LED=${CONFIG_SHIELD_GROVE_LED}, "
      "expected CONFIG_SHIELD_GROVE_LED=y"
    )
  else()

    test_if(CONFIG_SHIELD_GROVE_LED "led0" "grove_led_d6" "Grove LED D6")

  endif()

  if(CONFIG_BOARD_NUCLEO_F303RE OR
     CONFIG_BOARD_NUCLEO_F401RE OR
     CONFIG_BOARD_NUCLEO_F413ZH OR
     CONFIG_BOARD_NUCLEO_F767ZI)

    if(NOT CONFIG_SHIELD_GROVE_PWM_LED)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_PWM_LED=${CONFIG_SHIELD_GROVE_PWM_LED}, "
        "expected CONFIG_SHIELD_GROVE_PWM_LED=y"
      )
    else()

      test_if(CONFIG_SHIELD_GROVE_PWM_LED "pwm-led0" "grove_pwm_led_d6" "Grove LED D6")

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

    test_if(CONFIG_SHIELD_GROVE_BTN "sw0" "grove_btn_d16" "Grove Button D16")

  endif()

  if(NOT CONFIG_SHIELD_GROVE_LED)
    message(FATAL_ERROR "Test failed, "
      "actual CONFIG_SHIELD_GROVE_LED=${CONFIG_SHIELD_GROVE_LED}, "
      "expected CONFIG_SHIELD_GROVE_LED=y"
    )
  else()

    test_if(CONFIG_SHIELD_GROVE_LED "led0" "grove_led_d18" "Grove LED D18")

  endif()

  if(CONFIG_HAS_RPI_PICO)

    if(NOT CONFIG_SHIELD_GROVE_PWM_LED)
      message(FATAL_ERROR "Test failed, "
        "actual CONFIG_SHIELD_GROVE_PWM_LED=${CONFIG_SHIELD_GROVE_PWM_LED}, "
        "expected CONFIG_SHIELD_GROVE_PWM_LED=y"
      )
    else()

      test_if(CONFIG_SHIELD_GROVE_PWM_LED "pwm-led0" "grove_pwm_led_d18" "Grove LED D18")

    endif()

  endif()

endif()