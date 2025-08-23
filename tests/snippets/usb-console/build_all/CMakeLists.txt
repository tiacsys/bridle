# Copyright (c) 2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

find_package(Bridle REQUIRED HINTS $ENV{BRIDLE_BASE})
project(grove_shields)

target_sources(app PRIVATE src/main.c)

function(test_if_exact if_value test_prompt)
  if(DEFINED CONFIG_${if_value} AND
    "${CONFIG_${if_value}}" STREQUAL "${CONFIG_TEST_EXPECTED_${if_value}}")
    message(STATUS "[✓] ${test_prompt}: ${CONFIG_TEST_EXPECTED_${if_value}}")
  else()
    message(FATAL_ERROR "${test_prompt}: Test failed, "
      "actual \"CONFIG_${if_value}\" has the value "
      "\"${CONFIG_${if_value}}\", expected "
      "\"${CONFIG_TEST_EXPECTED_${if_value}}\"."
    )
  endif()
endfunction()

function(test_if_chosen_comp if_chosen if_comp test_prompt)
  dt_has_chosen(has_if_chosen PROPERTY "${if_chosen}")
  if(NOT has_if_chosen)
    message(FATAL_ERROR "Expect to use a ${test_prompt}. "
      "Add `${if_chosen}` to the device tree.")
  else()
    dt_chosen(if_chosen_path PROPERTY "${if_chosen}")
    dt_node_exists(if_chosen_node_exists PATH "${if_chosen_path}")
    dt_prop(if_chosen_node_comp PATH "${if_chosen_path}" PROPERTY "compatible")
    if(DEFINED if_chosen_node_comp AND if_chosen_node_comp MATCHES "${if_comp}")
      message(STATUS "[✓] ${if_chosen}: compatible = \"${if_comp}\"")
    else()
      message(FATAL_ERROR "Test failed, "
        "actual either "
        "the node path \"${if_chosen_path}\" is missing or "
        "the node path is not compatible to ${test_prompt} @ USB, "
        "expected node compatible to \"${if_comp}\" "
        "but got \"${if_chosen_node_comp}\"."
      )
    endif()
  endif()
endfunction()

function(test_if_chosen_comp_ifdef if_feature_toggle)
  if(${${if_feature_toggle}})
    test_if_chosen_comp(${ARGN})
  endif()
endfunction()

# Save default values for later restore.
set(CMAKE_CURRENT_MESSAGE_INDENT ${CMAKE_MESSAGE_INDENT})
list(APPEND CMAKE_MESSAGE_INDENT " [TEST] ")

message(STATUS "")
message(STATUS "${CONFIG_TEST_NAME}")

message(STATUS "")
message(STATUS "*** USB Device Stack")
test_if_exact("USB_DEVICE_STACK" "USB Device Support")
test_if_exact("USB_DEVICE_VID" "USB Vendor ID")
test_if_exact("USB_DEVICE_PID" "USB Product ID")
test_if_exact("USB_DEVICE_MANUFACTURER" "USB Manufacturer Name")
test_if_exact("USB_DEVICE_PRODUCT" "USB Product Name")
test_if_exact("USB_DEVICE_SN" "USB Device Serial Number String")
test_if_exact("USB_DEVICE_LOG_LEVEL_ERR" "Log Level for USB Device Support is ERROR")
test_if_exact("USB_DEVICE_INITIALIZE_AT_BOOT" "Initialize USB Device Support at boot")

message(STATUS "")
message(STATUS "*** USB CDC ACM Class")
test_if_exact("USB_CDC_ACM" "USB CDC ACM Class Support")
test_if_exact("USB_CDC_ACM_LOG_LEVEL_OFF" "Log Level for USB CDC ACM Class is OFF")

message(STATUS "")
message(STATUS "*** DTS chosen properties")
test_if_chosen_comp_ifdef(CONFIG_TEST_EXPECTED_USB_CDC_ACM
  "zephyr,console" "zephyr,cdc-acm-uart" "Zephyr Console")
test_if_chosen_comp_ifdef(CONFIG_TEST_CHOSEN_ZEPHYR_SHELL_UART
  "zephyr,shell-uart" "zephyr,cdc-acm-uart" "Zephyr Shell UART")

message(STATUS "")

# Clean up temp variables
set(CMAKE_MESSAGE_INDENT ${CMAKE_CURRENT_MESSAGE_INDENT})
