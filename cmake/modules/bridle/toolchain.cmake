# Copyright (c) 2022 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# The purpose of this file is to verify that required variables have been
# defined for proper toolchain use.
#
# It also offers the possibility to verify that the selected toolchain
# matches the required version range. Currently, only when using the
# Zephyr SDK the version is verified, but other other version verification
# for other toolchains can be added as needed.
#
# This file can also be executed in script mode so that it can be used in
# other places, such as python scripts.
#
# When invoked as a script with -P:
#   cmake [options] -P toolchain.cmake
#
# it takes the following arguments:
#   -D FORMAT=json
#      Print the output as a json formatted string, useful for Python.
#   -D BRIDLE_TOOLCHAIN_ZEPHYR_SDK_VERSION=x.y.z
#      Verify given Zephyr SDK version exactly.
#   -D BRIDLE_TOOLCHAIN_ZEPHYR_SDK_REQUIRED_VERSION=x.y.z
#      Verify given Zephyr SDK version as minimally required.

include_guard(GLOBAL)

include(extensions)

# Set internal variables if set in environment.
zephyr_get(ZEPHYR_TOOLCHAIN_VARIANT)

zephyr_get(ZEPHYR_SDK_INSTALL_DIR)

if((NOT "zephyr" STREQUAL ${ZEPHYR_TOOLCHAIN_VARIANT}) AND
   (NOT ${ZEPHYR_TOOLCHAIN_VARIANT} STREQUAL NONE) AND
   (DEFINED ZEPHYR_TOOLCHAIN_VARIANT))
  message(STATUS "Bridle is trying to use Zephyr toolchain variant "
                 "'${ZEPHYR_TOOLCHAIN_VARIANT}' for compiling.")
  return()
endif()

# This is the required Zephyr-SDK version for Bridle.
if(BRIDLE_TOOLCHAIN_ZEPHYR_SDK_VERSION)
  set(BRIDLE_TOOLCHAIN_ZEPHYR_SDK_REQUIRED_VERSION ${BRIDLE_TOOLCHAIN_ZEPHYR_SDK_VERSION})
  string(REGEX MATCH "(\\.\\.\\.)" OUT_VAR "${BRIDLE_TOOLCHAIN_ZEPHYR_SDK_REQUIRED_VERSION}")
  if(NOT CMAKE_MATCH_1)
    set(EXACT "EXACT")
  endif()
endif()

# Verify Zephyr SDK Toolchain.
# There are three places where Zephyr SDK should be looked up:
# 1) Zephyr SDK specified as toolchain by environment == pass through to Zephyr
# 2) Required toolchain specified by file == search for package
# Until we completely deprecate it
if(("zephyr" STREQUAL ${ZEPHYR_TOOLCHAIN_VARIANT}) OR
   (NOT DEFINED ZEPHYR_TOOLCHAIN_VARIANT) OR
   (DEFINED ZEPHYR_SDK_INSTALL_DIR) OR
   (NOT ${BRIDLE_TOOLCHAIN_ZEPHYR_SDK_REQUIRED_VERSION} STREQUAL NONE))

  # No toolchain was specified, so inform user that we will be searching.
  if ((NOT DEFINED ZEPHYR_SDK_INSTALL_DIR) AND
      (NOT DEFINED ZEPHYR_TOOLCHAIN_VARIANT) AND
      (NOT CMAKE_SCRIPT_MODE_FILE))
    message(STATUS "Bridle is trying to locate Zephyr SDK "
                   "${BRIDLE_TOOLCHAIN_ZEPHYR_SDK_REQUIRED_VERSION}.")
  endif()

  # This ensure packages are sorted in natural ascending order.
  set(CMAKE_FIND_PACKAGE_SORT_DIRECTION_CURRENT ${CMAKE_FIND_PACKAGE_SORT_DIRECTION})
  set(CMAKE_FIND_PACKAGE_SORT_ORDER_CURRENT ${CMAKE_FIND_PACKAGE_SORT_ORDER})
  set(CMAKE_FIND_PACKAGE_SORT_DIRECTION DEC)
  set(CMAKE_FIND_PACKAGE_SORT_ORDER NATURAL)

  find_package(Zephyr-sdk ${BRIDLE_TOOLCHAIN_ZEPHYR_SDK_REQUIRED_VERSION}
                          ${EXACT} REQUIRED QUIET CONFIG
                          HINTS ${ZEPHYR_SDK_INSTALL_DIR}
                          PATHS /usr
                                /usr/local
                                /opt
                                $ENV{HOME}
                                $ENV{HOME}/.local
                                $ENV{HOME}/.local/opt
                                $ENV{HOME}/bin)

  set(CMAKE_FIND_PACKAGE_SORT_DIRECTION ${CMAKE_FIND_PACKAGE_SORT_DIRECTION_CURRENT})
  set(CMAKE_FIND_PACKAGE_SORT_ORDER ${CMAKE_FIND_PACKAGE_SORT_ORDER_CURRENT})

  if((${Zephyr-sdk_FOUND}) AND
     (DEFINED ZEPHYR_SDK_INSTALL_DIR) AND
     (DEFINED ZEPHYR_TOOLCHAIN_VARIANT))
    if(NOT CMAKE_SCRIPT_MODE_FILE)
      message(STATUS "Using Zephyr SDK ${Zephyr-sdk_VERSION} "
                     "for compiling. (${Zephyr-sdk_DIR})")
    endif()
    set(Zephyr-sdk_ROOT ${Zephyr-sdk_DIR})
  else()
    set(error_msg "The required Zephyr SDK version was not found.\n")
    set(missing_version "You need SDK version "
                        "${BRIDLE_TOOLCHAIN_ZEPHYR_SDK_REQUIRED_VERSION} "
                        "or newer.")
    string(APPEND error_msg ${missing_version})
    message(FATAL_ERROR
            "${error_msg}\n"
            "The Zephyr SDK can be downloaded from: "
            "https://github.com/zephyrproject-rtos/sdk-ng/releases/download"
            "/v${BRIDLE_TOOLCHAIN_ZEPHYR_SDK_REQUIRED_VERSION}"
            "/zephyr-sdk-${BRIDLE_TOOLCHAIN_ZEPHYR_SDK_REQUIRED_VERSION}"
            "-setup.run\n")
  endif()
endif()

if(CMAKE_SCRIPT_MODE_FILE)
  if("${FORMAT}" STREQUAL "json")
    set(json "{\"ZEPHYR_TOOLCHAIN_VARIANT\" : \"${ZEPHYR_TOOLCHAIN_VARIANT}\", ")
    string(APPEND json "\"SDK_VERSION\": \"${SDK_VERSION}\", ")
    string(APPEND json "\"ZEPHYR_SDK_INSTALL_DIR\" : \"${ZEPHYR_SDK_INSTALL_DIR}\"}")
    message("${json}")
  else()
    message(STATUS "ZEPHYR_TOOLCHAIN_VARIANT: ${ZEPHYR_TOOLCHAIN_VARIANT}")
    if(DEFINED SDK_VERSION)
      message(STATUS "SDK_VERSION: ${SDK_VERSION}")
    endif()

    if(DEFINED ZEPHYR_SDK_INSTALL_DIR)
      message(STATUS "ZEPHYR_SDK_INSTALL_DIR  : ${ZEPHYR_SDK_INSTALL_DIR}")
    endif()
  endif()
endif()
