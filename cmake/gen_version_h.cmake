# Copyright (c) 2021-2022 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

if(NOT DEFINED BRIDLE_BUILD_VERSION)
  find_package(Git QUIET)
  if(GIT_FOUND)
    execute_process(
      COMMAND ${GIT_EXECUTABLE} describe --abbrev=12 --always
      WORKING_DIRECTORY                ${BRIDLE_BASE}
      OUTPUT_VARIABLE                  BRIDLE_BUILD_VERSION
      OUTPUT_STRIP_TRAILING_WHITESPACE
      ERROR_STRIP_TRAILING_WHITESPACE
      ERROR_VARIABLE                   stderr
      RESULT_VARIABLE                  return_code
    )
    if(return_code)
      message(STATUS "git describe failed: ${stderr}")
    elseif(NOT "${stderr}" STREQUAL "")
      message(STATUS "git describe warned: ${stderr}")
    endif()
  endif()
  if((DEFINED BRIDLE_BUILD_VERSION) AND
     (NOT BRIDLE_BUILD_VERSION MATCHES "^bridle-"))
    string(PREPEND BRIDLE_BUILD_VERSION "bridle-")
  endif()
endif()

include(${BRIDLE_BASE}/cmake/modules/bridle/version.cmake)
configure_file(${BRIDLE_BASE}/version.h.in ${OUT_DIR}/${OUT_FILE})
