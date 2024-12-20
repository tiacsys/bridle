# Copyright (c) 2022-2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# The purpose of this file is to verify that required variables have been
# defined for proper toolchain use.
#
# It also offers the possibility to verify that the selected toolchain
# matches the required version range. Currently, only when using the
# Zephyr SDK the version is verified, but other version verification
# for other toolchains can be added as needed.

include_guard(GLOBAL)

include(extensions)

# This is the required Zephyr-SDK version for Bridle.
if((DEFINED BRIDLE_TOOLCHAIN_ZEPHYR_SDK_REQUIRED_VERSION) AND
   (DEFINED BRIDLE_TOOLCHAIN_ZEPHYR_SDK_VERSION))
  string(JOIN "..." BRIDLE_TOOLCHAIN_ZEPHYR_SDK_CONSIDERED_VERSIONS
         "${BRIDLE_TOOLCHAIN_ZEPHYR_SDK_REQUIRED_VERSION}"
         "${BRIDLE_TOOLCHAIN_ZEPHYR_SDK_VERSION}")
else()
  set(error_msg "The considered Zephyr SDK version can not set.\n")
  set(missing_version "Either 'BRIDLE_TOOLCHAIN_ZEPHYR_SDK_REQUIRED_VERSION' "
                      "or 'BRIDLE_TOOLCHAIN_ZEPHYR_SDK_VERSION' not defined!")
  string(APPEND error_msg ${missing_version})
  message(FATAL_ERROR "${error_msg}\n")
endif()

# Save default values for later restore.
set(CMAKE_CURRENT_MESSAGE_INDENT ${CMAKE_MESSAGE_INDENT})

# Set internal variables if set in environment.
zephyr_get(ZEPHYR_TOOLCHAIN_VARIANT)
zephyr_get(ZEPHYR_SDK_INSTALL_DIR)

# Verify Zephyr SDK Toolchain.
if(("zephyr" STREQUAL ${ZEPHYR_TOOLCHAIN_VARIANT}) OR
   (NOT DEFINED ZEPHYR_TOOLCHAIN_VARIANT) OR
   (DEFINED ZEPHYR_SDK_INSTALL_DIR) OR
   (NOT ${BRIDLE_TOOLCHAIN_ZEPHYR_SDK_CONSIDERED_VERSIONS} STREQUAL NONE))

  # No toolchain was specified, so inform user that we will be searching.
  if ((NOT DEFINED ZEPHYR_SDK_INSTALL_DIR) AND
      (NOT DEFINED ZEPHYR_TOOLCHAIN_VARIANT))
    message(STATUS "Bridle is trying to locate Zephyr SDK "
                   "${BRIDLE_TOOLCHAIN_ZEPHYR_SDK_CONSIDERED_VERSIONS}.")
  endif()

  list(APPEND CMAKE_MESSAGE_INDENT " [✓] ")
  find_package(Zephyr-sdk ${BRIDLE_TOOLCHAIN_ZEPHYR_SDK_CONSIDERED_VERSIONS} QUIET REQUIRED)

  if((${Zephyr-sdk_FOUND}) AND
     (DEFINED ZEPHYR_SDK_INSTALL_DIR) AND
     (DEFINED ZEPHYR_TOOLCHAIN_VARIANT) AND
     (${Zephyr-sdk_VERSION} VERSION_LESS_EQUAL ${BRIDLE_TOOLCHAIN_ZEPHYR_SDK_VERSION}))
    message(STATUS "Found toolchain: ${Zephyr-sdk_VERSION} (${Zephyr-sdk_DIR})")
    set(Zephyr-sdk_ROOT ${Zephyr-sdk_DIR})
  else()
    set(error_msg "The required Zephyr SDK version was not found.\n")
    set(missing_version "You need SDK version "
                        "${BRIDLE_TOOLCHAIN_ZEPHYR_SDK_VERSION}")
    string(APPEND error_msg ${missing_version})
    message(FATAL_ERROR
            "${error_msg}\n"
            "The Zephyr SDK can be downloaded from: "
            "https://github.com/zephyrproject-rtos/sdk-ng/releases/tag"
            "/v${BRIDLE_TOOLCHAIN_ZEPHYR_SDK_VERSION}\n")
  endif()
endif()

# Clean up temp variables
set(CMAKE_MESSAGE_INDENT ${CMAKE_CURRENT_MESSAGE_INDENT})
set(BRIDLE_TOOLCHAIN_ZEPHYR_SDK_CONSIDERED_VERSIONS)
set(missing_version)
set(error_msg)
