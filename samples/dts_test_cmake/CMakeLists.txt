# Copyright (c) 2021-2023 TiaC Systems
# Copyright (c) 2019-2021 Li-Pro.Net
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

# Standard Bridle application boilerplate, includes Zephyr.
find_package(Bridle REQUIRED HINTS $ENV{BRIDLE_BASE})
project("Test device tree with CMake" VERSION 0.1)

include(${ZEPHYR_BASE}/cmake/hex.cmake)

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

function(test_if_status_matching if_path ref_status)
    message("if_path = ${if_path}")
    dt_node_has_status(if_status PATH ${if_path} STATUS okay)
    if(if_status STREQUAL ref_status)
        message(STATUS "Found status \"${ref_status}\" at \"${if_path}\"." )
    else()
        message(FATAL_ERROR "Test failed, "
            "the status property is ${if_status} at \"${if_path}\" , "
            "expected \"${ref_status}\"."
        )
    endif()
endfunction()

function(test_if_property_matching if_path property_name ref_properties convert_to_hex)
    set(message_string "")
    message("property_name = ${property_name}")
    dt_prop(if_properties PATH ${if_path} PROPERTY ${property_name})
    message("if_properties = ${if_properties} \n ")
    if(DEFINED if_properties)
        foreach(if_property ref_property IN ZIP_LISTS if_properties ref_properties)
            if(DEFINED if_property AND DEFINED ref_property)
                message(STATUS "ref_property = ${ref_property}")
                message(STATUS "if_property = ${if_property}")
                message(STATUS "convert_to_hex = ${convert_to_hex}")
                if(convert_to_hex STREQUAL "TRUE")
                    to_hex(${if_property}  if_property_hex)
                    message(STATUS "if_property_hex = ${if_property_hex}")
                    set(if_property ${if_property_hex})
                    message(STATUS "if_property = ${if_property}")
                endif()
                string(APPEND message_string ${if_property}  " ")
                message(STATUS "message_string = ${message_string}")
                if(NOT ref_property STREQUAL if_property)
                    message(FATAL_ERROR "Test failed, "
                        "the property value \"${if_property}\" at property \"${property_name}\" "
                        "at path \"${if_path}\" is not equal with \"${ref_property}\"."
                    )
                endif()
            elseif(DEFINED ref_property)
                    message(FATAL_ERROR "Test failed, "
                    "the property value at property \"${property_name}\" at path \"${if_path}\" "
                    "is missing, "
                    "expected \"${ref_status}\"."
                    )
            endif()
        endforeach()
    else()
        message(FATAL_ERROR "Test failed, "
            "the property \"${property_name}\" is missing at path \"${if_path}\"."
        )
    endif()
    message(STATUS "Found property entries \"${message_string}\" "
        "at property \"${property_name}\" at path \"${if_path}\"."
    )
endfunction()

# get grove-laced-if node path
if(CONFIG_SHIELD_SEEED_GROVE_BASE_V2)
  dt_nodelabel(if_path NODELABEL "grove_laced_if_v2")
else()
  message(FATAL_ERROR "Test failed, "
    "actual the "
    "CONFIG_SHIELD_SEEED_GROVE_BASE_V2=${CONFIG_SHIELD_SEEED_GROVE_BASE_V2} "
    "is turned on, expected \"grove_laced_if_v2\"."
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

  # check common board specific add-ons
  if(CONFIG_BOARD_NUCLEO_F401RE OR
     CONFIG_BOARD_MIMXRT1060_EVK OR
     CONFIG_BOARD_MIMXRT1060_EVKB OR
     CONFIG_BOARD_ARDUINO_ZERO OR
     CONFIG_BOARD_SEEEDUINO_LOTUS)

    test_if_label_matching("grove_serial" "arduino_serial")
    test_if_label_matching("grove_i2c" "arduino_i2c")
    test_if_label_matching("grove_spi" "arduino_spi")
  endif()

  # check I2C interface
  if(CONFIG_BOARD_NUCLEO_F401RE)
    dt_comp_path(if_i2cs COMPATIBLE "st,stm32-i2c-v1")
    list(LENGTH if_i2cs if_i2c_nums)
    message("if_i2cs = ${if_i2cs}")
    if(DEFINED if_i2cs AND if_i2c_nums EQUAL 3)
        list(GET if_i2cs 0 if_path)

        # check i2c0 status, reg, usw
        test_if_status_matching(${if_path} "TRUE")

        list(APPEND ref_property 0x40005400 0x400)
        test_if_property_matching(${if_path} "reg" "${ref_property}" "TRUE")
        test_if_property_matching(${if_path} "clock-frequency" "0x61A80" "TRUE")
        test_if_property_matching(${if_path} "pinctrl-names" "default" "FALSE")

        list(REMOVE_AT ref_property 0 1)
        list(APPEND ref_property event error)
        message("ref_property = ${ref_property}")
        test_if_property_matching(${if_path} "interrupt-names" "${ref_property}" "FALSE")

        # CMake can't get values with leading '&'. Therefore this test will fail.
        # list(REMOVE_AT ref_property 0 1)
        # list(APPEND ref_property &i2c1_scl_pb8 &i2c1_sda_pb9)
        # message("ref_property = ${ref_property}")
        # test_if_property_matching(${if_path} "pinctrl-0" "${ref_property}" "FALSE")

        # i2c1 and i2c2 are disabled
        list(GET if_i2cs 1 if_path)
        test_if_status_matching(${if_path} "FALSE")
        list(GET if_i2cs 2 if_path)
        test_if_status_matching(${if_path} "FALSE")

    else()
      message(FATAL_ERROR "Test failed, "
        "actual the numbers of ports on grove-laced-if is ${if_i2c_nums}, "
        "expected 3."
      )
    endif()
  endif()
else()
  message(FATAL_ERROR "Test failed, "
    "actual the grove-laced-if node path was not found in DTS."
  )
endif()
