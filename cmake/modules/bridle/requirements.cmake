# Copyright (c) 2022-2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

include_guard(GLOBAL)

if(${CMAKE_HOST_SYSTEM_NAME} STREQUAL "Linux")
  set(tools_versions_os ${BRIDLE_BASE}/doc/tools-versions-linux.txt)
elseif(CMAKE_HOST_APPLE)
  set(tools_versions_os ${BRIDLE_BASE}/doc/tools-versions-macos.txt)
elseif(CMAKE_HOST_WIN32)
  set(tools_versions_os ${BRIDLE_BASE}/doc/tools-versions-win10.txt)
endif()

set(tools_versions_min ${BRIDLE_BASE}/doc/tools-versions-minimum.txt)

# This will determine and set the required Zephyr SDK version.
file(STRINGS ${tools_versions_min}
     zephyr_sdk_string LIMIT_COUNT 1 REGEX "^zephyr-sdk="
)
string(REGEX MATCH "=([^ \t]*)" OUT_VAR "${zephyr_sdk_string}")
if(CMAKE_MATCH_1)
  set(BRIDLE_TOOLCHAIN_ZEPHYR_SDK_REQUIRED_VERSION ${CMAKE_MATCH_1})
else()
  message(FATAL_ERROR "Zephyr SDK: malformatted version string as input?\n"
      "Got: '${zephyr_sdk_string}'\n"
      "Check: ${tools_versions_min}"
  )
endif()

# This will determine and set the maximum allowed Zephyr SDK version.
file(STRINGS ${tools_versions_os}
     zephyr_sdk_string LIMIT_COUNT 1 REGEX "^zephyr-sdk="
)
string(REGEX MATCH "=([^ \t]*)" OUT_VAR "${zephyr_sdk_string}")
if(CMAKE_MATCH_1)
  set(BRIDLE_TOOLCHAIN_ZEPHYR_SDK_VERSION ${CMAKE_MATCH_1})
else()
  message(FATAL_ERROR "Zephyr SDK: malformatted version string as input?\n"
      "Got: '${zephyr_sdk_string}'\n"
      "Check: ${tools_versions_os}"
  )
endif()

# This will determine and set the required Doxygen version.
file(STRINGS ${tools_versions_min}
     doxygen_string LIMIT_COUNT 1 REGEX "^doxygen="
)
string(REGEX MATCH "=([^ \t]*)" OUT_VAR "${doxygen_string}")
if(CMAKE_MATCH_1)
  set(BRIDLE_DOXYGEN_REQUIRED_VERSION ${CMAKE_MATCH_1})
else()
  message(FATAL_ERROR "Doxygen: malformatted version string as input?\n"
      "Got: '${doxygen_string}'\n"
      "Check: ${tools_versions_min}"
  )
endif()

# This will determine and set the required Sphinx version.
file(STRINGS ${BRIDLE_BASE}/zephyr/requirements-doc.txt
     sphinx_string LIMIT_COUNT 1 REGEX "^sphinx[~,<,>]?="
)
string(REGEX MATCH "=([^ \t]*)[^ \t]*,[<,>]([^ \t]*)"
             OUT_VAR "${sphinx_string}"
)
if(NOT CMAKE_MATCH_1)
  string(REGEX MATCH "=([^ \t]*)[^ \t]*,[!]([^ \t]*)" OUT_VAR "${sphinx_string}")
  if(CMAKE_MATCH_1)
    set(ZEPHYR_SPHINX_REQUIRED_VERSION ${CMAKE_MATCH_1})
  elseif(NOT CMAKE_MATCH_1)
    string(REGEX MATCH "=([^ \t]*)" OUT_VAR "${sphinx_string}")
    if(CMAKE_MATCH_1)
      set(ZEPHYR_SPHINX_REQUIRED_VERSION ${CMAKE_MATCH_1})
    else()
      message(FATAL_ERROR "Sphinx: malformatted PIP version string as input?\n"
          "Got: '${sphinx_string}'\n"
          "Check: ${BRIDLE_BASE}/zephyr/requirements-doc.txt"
      )
    endif()
  endif()
else()
  if(CMAKE_MATCH_2)
    if(CMAKE_MATCH_1 VERSION_LESS CMAKE_MATCH_2)
      set(ZEPHYR_SPHINX_REQUIRED_VERSION ${CMAKE_MATCH_1})
    else()
      set(ZEPHYR_SPHINX_REQUIRED_VERSION ${CMAKE_MATCH_2})
    endif()
  else()
    message(FATAL_ERROR "Sphinx: malformatted PIP version string as input?\n"
        "Got: '${sphinx_string}'\n"
        "Check: ${BRIDLE_BASE}/zephyr/requirements-doc.txt"
    )
  endif()
endif()

unset(tools_versions_os)
