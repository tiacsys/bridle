# Copyright (c) 2022 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

include_guard(GLOBAL)

# This will determine and set the required Zephyr SDK version.
file(STRINGS ${BRIDLE_BASE}/scripts/tools-versions-minimum.txt
     zephyr_sdk_string LIMIT_COUNT 1 REGEX "^zephyr-sdk="
)
string(REGEX MATCH "=([^ \t]*)" OUT_VAR "${zephyr_sdk_string}")
if(CMAKE_MATCH_1)
  set(BRIDLE_TOOLCHAIN_ZEPHYR_SDK_REQUIRED_VERSION ${CMAKE_MATCH_1})
else()
  message(FATAL_ERROR "Zephyr SDK: malformatted version string as input?\n"
      "Got: '${zephyr_sdk_string}'\n"
      "Check: ${BRIDLE_BASE}/scripts/tools-versions-minimum.txt"
  )
endif()
