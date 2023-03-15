# Copyright (c) 2023 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(grove_shields)

target_sources(app PRIVATE src/main.c)

function(test_if_port_label if_port_list if_port_label)
  dt_nodelabel(if_port_path NODELABEL "${if_port_label}")
  list(FIND if_port_list "${if_port_path}" if_port_num)
  if(DEFINED if_port_path AND NOT if_port_num EQUAL -1)
    message(STATUS "Found label \"${if_port_label}\" at \"${if_port_path}\"")
  else()
    message(FATAL_ERROR "Test failed, "
      "actual either "
      "the node path \"${if_port_path}\" is missing or "
      "the node path is not connected to the Grove I/F or "
      "the node label is missing or misspelled, expected "
      "node label \"${if_port_label}\" connected to Grove I/F."
    )
  endif()
endfunction()

function(test_if_label_matching if_label ref_label)
  dt_nodelabel(if_path NODELABEL "${if_label}")
  dt_nodelabel(ref_path NODELABEL "${ref_label}")
  if(DEFINED if_path AND DEFINED ref_path AND
     "${if_path}" STREQUAL "${ref_path}")
    message(STATUS "Found label \"${if_label}\" points to "
                               "\"${ref_label}\" at \"${ref_path}\"")
  else()
    message(FATAL_ERROR "Test failed, "
      "actual either "
      "the node path \"${if_path}\" for label \"${if_label}\" and "
      "the node path \"${ref_path}\" for label \"${ref_label}\" "
      "are not equal or the node labels are missing or misspelled."
    )
  endif()
endfunction()

function(test_if_label_on_path if_label if_path)
  dt_nodelabel(if_label_path NODELABEL "${if_label}")
  if(DEFINED if_path AND DEFINED if_label_path AND
     "${if_path}" STREQUAL "${if_label_path}")
    message(STATUS "Found label \"${if_label}\" at \"${if_path}\"")
  else()
    message(FATAL_ERROR "Test failed, "
      "actual either "
      "the node path \"${if_path}\" of the interface and "
      "the node path \"${if_label_path}\" at label \"${if_label}\" "
      "are not equal or the node labels are missing or misspelled."
    )
  endif()
endfunction()

# get grove-laced-if node path
if(CONFIG_SHIELD_SEEED_GROVE_BASE_V2)
  dt_nodelabel(if_path NODELABEL "grove_laced_if_v2")

elseif(CONFIG_SHIELD_SEEED_GROVE_BASE_V1)
  dt_nodelabel(if_path NODELABEL "grove_laced_if_v1")

elseif(CONFIG_SHIELD_SEEED_GROVE_RPIPICO_V1)
  dt_nodelabel(if_path NODELABEL "grove_laced_if_v1")

else()
  message(FATAL_ERROR "Test failed, "
    "actual neither "
    "CONFIG_SHIELD_SEEED_GROVE_BASE_V2=${CONFIG_SHIELD_SEEED_GROVE_BASE_V2} nor "
    "CONFIG_SHIELD_SEEED_GROVE_BASE_V1=${CONFIG_SHIELD_SEEED_GROVE_BASE_V1} nor "
    "CONFIG_SHIELD_SEEED_GROVE_RPIPICO_V1=${CONFIG_SHIELD_SEEED_GROVE_RPIPICO_V1} "
    "is turned on, expected at least one of them."
  )
endif()

# check grove-laced-if properties
if(DEFINED if_path)

  dt_prop(compat_if PATH ${if_path} PROPERTY compatible)
  if(compat_if MATCHES "seeed,grove-laced-if")
  else()
    message(FATAL_ERROR "Test failed, "
      "actual the node \"${if_path}\" has the compatibility "
      "\"${compat_if}\", expected \"seeed,grove-laced-if\""
    )
  endif()

  if(CONFIG_SHIELD_SEEED_GROVE_BASE_V2 AND
     NOT "${if_path}" STREQUAL "/grove-laced-if-v2")
    message(FATAL_ERROR "Test failed, "
      "actual the grove-laced-if node path is \"${if_path}\", "
      "expected \"/grove-laced-if-v2\"."
    )
  endif()

  if((CONFIG_SHIELD_SEEED_GROVE_BASE_V1 OR
      CONFIG_SHIELD_SEEED_GROVE_RPIPICO_V1) AND
     NOT "${if_path}" STREQUAL "/grove-laced-if-v1")
    message(FATAL_ERROR "Test failed, "
      "actual the grove-laced-if node path is \"${if_path}\", "
      "expected \"/grove-laced-if-v1\"."
    )
  endif()

  message(STATUS "Found Laced Grove Signal Interface at \"${if_path}\"")
  test_if_label_on_path("grove_gpios" "${if_path}")

  # check grove-laced-if-v2 interconnection order
  if(CONFIG_SHIELD_SEEED_GROVE_BASE_V2)
    dt_comp_path(if_ports COMPATIBLE "seeed,grove-connector")
    list(LENGTH if_ports if_port_nums)
    if(DEFINED if_ports AND if_port_nums EQUAL 13)

      test_if_port_label("${if_ports}" "grove_d0_header")
      test_if_port_label("${if_ports}" "grove_d2_header")
      test_if_port_label("${if_ports}" "grove_d3_header")
      test_if_port_label("${if_ports}" "grove_d4_header")
      test_if_port_label("${if_ports}" "grove_d5_header")
      test_if_port_label("${if_ports}" "grove_d6_header")
      test_if_port_label("${if_ports}" "grove_d7_header")
      test_if_port_label("${if_ports}" "grove_d8_header")
      test_if_port_label("${if_ports}" "grove_a0_header")
      test_if_port_label("${if_ports}" "grove_a1_header")
      test_if_port_label("${if_ports}" "grove_a2_header")
      test_if_port_label("${if_ports}" "grove_a3_header")
      test_if_port_label("${if_ports}" "grove_uart_header")
      test_if_port_label("${if_ports}" "grove_i2c_header")

    else()
      message(FATAL_ERROR "Test failed, "
        "actual the numbers of ports on grove-laced-if is ${if_port_nums}, "
        "expected 13."
      )
    endif()
  endif()

  # check grove-laced-if-v1 interconnection order
  if(CONFIG_SHIELD_SEEED_GROVE_BASE_V1)
    dt_comp_path(if_ports COMPATIBLE "seeed,grove-connector")
    list(LENGTH if_ports if_port_nums)
    if(DEFINED if_ports AND if_port_nums EQUAL 21)

      test_if_port_label("${if_ports}" "grove_d0_header")
      test_if_port_label("${if_ports}" "grove_d1_header")
      test_if_port_label("${if_ports}" "grove_d2_header")
      test_if_port_label("${if_ports}" "grove_d3_header")
      test_if_port_label("${if_ports}" "grove_d4_header")
      test_if_port_label("${if_ports}" "grove_d5_header")
      test_if_port_label("${if_ports}" "grove_d6_header")
      test_if_port_label("${if_ports}" "grove_d7_header")
      test_if_port_label("${if_ports}" "grove_d8_header")
      test_if_port_label("${if_ports}" "grove_d9_header")
      test_if_port_label("${if_ports}" "grove_d10_header")
      test_if_port_label("${if_ports}" "grove_d11_header")
      test_if_port_label("${if_ports}" "grove_d12_header")
      test_if_port_label("${if_ports}" "grove_d13_header")
      test_if_port_label("${if_ports}" "grove_a0_header")
      test_if_port_label("${if_ports}" "grove_a1_header")
      test_if_port_label("${if_ports}" "grove_a2_header")
      test_if_port_label("${if_ports}" "grove_a3_header")
      test_if_port_label("${if_ports}" "grove_a4_header")
      test_if_port_label("${if_ports}" "grove_uart_header")
      test_if_port_label("${if_ports}" "grove_i2c_header")
      test_if_port_label("${if_ports}" "grove_spi_header")

    else()
      message(FATAL_ERROR "Test failed, "
        "actual the numbers of ports on grove-laced-if is ${if_port_nums}, "
        "expected 21."
      )
    endif()
  endif()

  # check grove-laced-if-v1 interconnection order
  if(CONFIG_SHIELD_SEEED_GROVE_RPIPICO_V1)
    dt_comp_path(if_ports COMPATIBLE "seeed,grove-connector")
    list(LENGTH if_ports if_port_nums)
    if(DEFINED if_ports AND if_port_nums EQUAL 10)

      test_if_port_label("${if_ports}" "grove_d1_header")
      test_if_port_label("${if_ports}" "grove_d5_header")
      test_if_port_label("${if_ports}" "grove_d7_header")
      test_if_port_label("${if_ports}" "grove_d9_header")
      test_if_port_label("${if_ports}" "grove_d16_header")
      test_if_port_label("${if_ports}" "grove_d18_header")
      test_if_port_label("${if_ports}" "grove_d20_header")
      test_if_port_label("${if_ports}" "grove_a0_header")
      test_if_port_label("${if_ports}" "grove_a1_header")
      test_if_port_label("${if_ports}" "grove_a2_header")
      test_if_port_label("${if_ports}" "grove_uart0_header")
      test_if_port_label("${if_ports}" "grove_uart1_header")
      test_if_port_label("${if_ports}" "grove_i2c0_header")
      test_if_port_label("${if_ports}" "grove_i2c1_header")

    else()
      message(FATAL_ERROR "Test failed, "
        "actual the numbers of ports on grove-laced-if is ${if_port_nums}, "
        "expected 10."
      )
    endif()
    dt_comp_path(if_ports COMPATIBLE "generic-pin-header")
    list(LENGTH if_ports if_port_nums)
    if(DEFINED if_ports AND if_port_nums EQUAL 1)

      test_if_port_label("${if_ports}" "generic_spi_header")

    else()
      message(FATAL_ERROR "Test failed, "
        "actual the numbers of ports on grove-laced-if is ${if_port_nums}, "
        "expected 1."
      )
    endif()
  endif()

  # check board specific add-ons for nucleo_f303re
  if(CONFIG_BOARD_NUCLEO_F303RE)

    test_if_label_on_path("grove_pwms" "${if_path}")

    if(CONFIG_SHIELD_SEEED_GROVE_BASE_V2 OR
       CONFIG_SHIELD_SEEED_GROVE_BASE_V1)

      test_if_label_matching("grove_pwm_d2" "pwm2")
      test_if_label_matching("grove_pwm_d3" "pwm2")
      test_if_label_matching("grove_pwm_d4" "pwm8")
      test_if_label_matching("grove_pwm_d5" "pwm3")
      test_if_label_matching("grove_pwm_d6" "pwm2")
      test_if_label_matching("grove_pwm_d7" "pwm1")
      test_if_label_matching("grove_pwm_d8" "pwm1")
      test_if_label_matching("grove_pwm_d9" "pwm3")

      if(CONFIG_SHIELD_SEEED_GROVE_BASE_V1)

        test_if_label_matching("grove_pwm_d10" "pwm4")
        test_if_label_matching("grove_pwm_d11" "pwm17")
        test_if_label_matching("grove_pwm_d12" "pwm16")
        test_if_label_matching("grove_pwm_d13" "pwm2")

      endif()

      test_if_label_matching("grove_pwm_d18" "pwm8")
      test_if_label_matching("grove_pwm_d19" "pwm8")

    endif()
  endif()

  # check board specific add-ons for nucleo_f401re
  if(CONFIG_BOARD_NUCLEO_F401RE)

    test_if_label_on_path("grove_pwms" "${if_path}")

    if(CONFIG_SHIELD_SEEED_GROVE_BASE_V2 OR
       CONFIG_SHIELD_SEEED_GROVE_BASE_V1)

      test_if_label_matching("grove_pwm_d2" "pwm1")
      test_if_label_matching("grove_pwm_d3" "pwm2")
      test_if_label_matching("grove_pwm_d5" "pwm3")
      test_if_label_matching("grove_pwm_d6" "pwm2")
      test_if_label_matching("grove_pwm_d7" "pwm1")
      test_if_label_matching("grove_pwm_d8" "pwm1")
      test_if_label_matching("grove_pwm_d9" "pwm3")

      if(CONFIG_SHIELD_SEEED_GROVE_BASE_V1)

        test_if_label_matching("grove_pwm_d10" "pwm4")
        test_if_label_matching("grove_pwm_d11" "pwm1")
        test_if_label_matching("grove_pwm_d13" "pwm2")

      endif()

      test_if_label_matching("grove_pwm_d18" "pwm11")
      test_if_label_matching("grove_pwm_d19" "pwm10")

    endif()
  endif()

  # check board specific add-ons for nucleo_f413zh
  if(CONFIG_BOARD_NUCLEO_F413ZH)

    test_if_label_on_path("grove_pwms" "${if_path}")

    if(CONFIG_SHIELD_SEEED_GROVE_BASE_V2 OR
       CONFIG_SHIELD_SEEED_GROVE_BASE_V1)

      test_if_label_matching("grove_pwm_d3" "pwm1")
      test_if_label_matching("grove_pwm_d5" "pwm1")
      test_if_label_matching("grove_pwm_d6" "pwm1")
      test_if_label_matching("grove_pwm_d9" "pwm4")

      if(CONFIG_SHIELD_SEEED_GROVE_BASE_V1)

        test_if_label_matching("grove_pwm_d10" "pwm4")
        test_if_label_matching("grove_pwm_d11" "pwm14")
        test_if_label_matching("grove_pwm_d12" "pwm13")
        test_if_label_matching("grove_pwm_d13" "pwm2")

      endif()

      test_if_label_matching("grove_pwm_d18" "pwm11")
      test_if_label_matching("grove_pwm_d19" "pwm10")

    endif()
  endif()

  # check board specific add-ons for nucleo_f767zi
  if(CONFIG_BOARD_NUCLEO_F767ZI)

    test_if_label_on_path("grove_pwms" "${if_path}")

    if(CONFIG_SHIELD_SEEED_GROVE_BASE_V2 OR
       CONFIG_SHIELD_SEEED_GROVE_BASE_V1)

      test_if_label_matching("grove_pwm_d3" "pwm1")
      test_if_label_matching("grove_pwm_d5" "pwm1")
      test_if_label_matching("grove_pwm_d6" "pwm1")
      test_if_label_matching("grove_pwm_d9" "pwm4")

      if(CONFIG_SHIELD_SEEED_GROVE_BASE_V1)

        test_if_label_matching("grove_pwm_d10" "pwm4")
        test_if_label_matching("grove_pwm_d11" "pwm14")
        test_if_label_matching("grove_pwm_d12" "pwm13")
        test_if_label_matching("grove_pwm_d13" "pwm2")

      endif()

      test_if_label_matching("grove_pwm_d18" "pwm11")
      test_if_label_matching("grove_pwm_d19" "pwm10")

    endif()
  endif()

  # check board specific add-ons for mimxrt1010_evk
  if(CONFIG_BOARD_MIMXRT1010_EVK)

    test_if_label_on_path("grove_pwms" "${if_path}")

    if(CONFIG_SHIELD_SEEED_GROVE_BASE_V2 OR
       CONFIG_SHIELD_SEEED_GROVE_BASE_V1)

      test_if_label_matching("grove_pwm_d8" "flexpwm1_pwm0")
      test_if_label_matching("grove_pwm_d9" "flexpwm1_pwm1")

    endif()
  endif()

  # check board specific add-ons for mimxrt1060_evk(b)
  if(CONFIG_BOARD_MIMXRT1060_EVK OR CONFIG_BOARD_MIMXRT1060_EVKB)

    test_if_label_on_path("grove_pwms" "${if_path}")

    if(CONFIG_SHIELD_SEEED_GROVE_BASE_V2 OR
       CONFIG_SHIELD_SEEED_GROVE_BASE_V1)

      test_if_label_matching("grove_pwm_d2" "flexpwm1_pwm3")
      test_if_label_matching("grove_pwm_d3" "flexpwm4_pwm0")
      test_if_label_matching("grove_pwm_d4" "flexpwm2_pwm3")
      test_if_label_matching("grove_pwm_d5" "flexpwm1_pwm3")

      if(CONFIG_SHIELD_SEEED_GROVE_BASE_V1)

        test_if_label_matching("grove_pwm_d10" "flexpwm1_pwm0")
        test_if_label_matching("grove_pwm_d11" "flexpwm1_pwm1")
        test_if_label_matching("grove_pwm_d12" "flexpwm1_pwm1")
        test_if_label_matching("grove_pwm_d13" "flexpwm1_pwm0")

      endif()
    endif()
  endif()

  # check common board specific add-ons
  if(CONFIG_BOARD_NUCLEO_F401RE OR
     CONFIG_BOARD_MIMXRT1060_EVK OR
     CONFIG_BOARD_MIMXRT1060_EVKB)

    test_if_label_matching("grove_uart" "arduino_serial")
    test_if_label_matching("grove_i2c" "arduino_i2c")
    test_if_label_matching("grove_spi" "arduino_spi")

  endif()

  # check board specific add-ons for rpi_pico
  if(CONFIG_BOARD_RPI_PICO)

    test_if_label_on_path("grove_pwms" "${if_path}")

    if(CONFIG_SHIELD_SEEED_GROVE_RPIPICO_V1)

      test_if_label_matching("grove_pwm_d16" "pwm")
      test_if_label_matching("grove_pwm_d18" "pwm")
      test_if_label_matching("grove_pwm_d20" "pwm")

    endif()
  endif()

  # check common board specific add-ons
  if(CONFIG_BOARD_RPI_PICO)

    test_if_label_matching("grove_uart" "rpipico_serial")
    test_if_label_matching("grove_i2c" "rpipico_i2c")
    test_if_label_matching("grove_spi" "rpipico_spi")

  endif()

else()
  message(FATAL_ERROR "Test failed, "
    "actual the grove-laced-if node path was not found in DTS."
  )
endif()
