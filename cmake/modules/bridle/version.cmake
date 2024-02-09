# Copyright (c) 2021-2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

#.rst:
# version.cmake
# -------------
#
# Inputs:
#
#   ``*VERSION*`` and other constants set by
#   maintainers in ``${BRIDLE_BASE}/VERSION``
#
# Outputs with examples::
#
#   PROJECT_VERSION           3.5.99.04
#   BRIDLE_VERSION_STRING    "3.5.99-extraver"
#
#   BRIDLE_VERSION_MAJOR      3
#   BRIDLE_VERSION_MINOR      5
#   BRIDLE_PATCHLEVEL         99
#   BRIDLE_VERSION_TWEAK      04
#   BRIDLEVERSION            0x3056304
#   BRIDLE_VERSION_NUMBER    0x30563
#   BRIDLE_VERSION_CODE        197987
#
# Most outputs are converted to C macros, see ``version.h.in``
#
# See also: independent and more dynamic ``BRIDLE_BUILD_VERSION`` in
# ``gen_version_h.cmake``.
#
# Note:
#
# `bridle/version.cmake` is loaded multiple times by `BridleConfigVersion.cmake`
# to determine this Bridle package version and thus the correct Bridle CMake
# package to load.
#
# Therefore `bridle/version.cmake` should not use include_guard(GLOBAL). The
# final load of `bridle/version.cmake` will setup correct version values.

file(READ ${BRIDLE_BASE}/VERSION ver)

string(REGEX MATCH "VERSION_MAJOR = ([0-9]*)" _ ${ver})
set(PROJECT_VERSION_MAJOR ${CMAKE_MATCH_1})

string(REGEX MATCH "VERSION_MINOR = ([0-9]*)" _ ${ver})
set(PROJECT_VERSION_MINOR ${CMAKE_MATCH_1})

string(REGEX MATCH "PATCHLEVEL = ([0-9]*)" _ ${ver})
set(PROJECT_VERSION_PATCH ${CMAKE_MATCH_1})

string(REGEX MATCH "VERSION_TWEAK = ([0-9]*)" _ ${ver})
set(PROJECT_VERSION_TWEAK ${CMAKE_MATCH_1})

string(REGEX MATCH "EXTRAVERSION = ([a-z0-9]*)" _ ${ver})
set(PROJECT_VERSION_EXTRA ${CMAKE_MATCH_1})

# Temporary convenience variable
set(PROJECT_VERSION_WITHOUT_TWEAK ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH})


if(PROJECT_VERSION_EXTRA)
  set(PROJECT_VERSION_EXTRA_STR "-${PROJECT_VERSION_EXTRA}")
endif()

if(PROJECT_VERSION_TWEAK)
  set(PROJECT_VERSION ${PROJECT_VERSION_WITHOUT_TWEAK}.${PROJECT_VERSION_TWEAK})
else()
  set(PROJECT_VERSION ${PROJECT_VERSION_WITHOUT_TWEAK})
endif()

set(PROJECT_VERSION_STR ${PROJECT_VERSION}${PROJECT_VERSION_EXTRA_STR})

if(DEFINED BRIDLE_BUILD_VERSION)
  set(BRIDLE_BUILD_VERSION_STR ", build: ${BRIDLE_BUILD_VERSION}")
endif()

if (NOT NO_PRINT_VERSION)
  message(STATUS "Bridle version: ${PROJECT_VERSION_STR} (${BRIDLE_BASE})${BRIDLE_BUILD_VERSION_STR}")
endif()

set(MAJOR ${PROJECT_VERSION_MAJOR}) # Temporary convenience variable
set(MINOR ${PROJECT_VERSION_MINOR}) # Temporary convenience variable
set(PATCH ${PROJECT_VERSION_PATCH}) # Temporary convenience variable

math(EXPR BRIDLE_VERSION_NUMBER_INT "(${MAJOR} << 16) + (${MINOR} << 8)  + (${PATCH})")
math(EXPR BRIDLEVERSION_INT         "(${MAJOR} << 24) + (${MINOR} << 16) + (${PATCH} << 8) + (${PROJECT_VERSION_TWEAK})")

math(EXPR BRIDLE_VERSION_NUMBER "${BRIDLE_VERSION_NUMBER_INT}" OUTPUT_FORMAT HEXADECIMAL)
math(EXPR BRIDLEVERSION         "${BRIDLEVERSION_INT}"         OUTPUT_FORMAT HEXADECIMAL)

set(BRIDLE_VERSION_MAJOR      ${PROJECT_VERSION_MAJOR})
set(BRIDLE_VERSION_MINOR      ${PROJECT_VERSION_MINOR})
set(BRIDLE_PATCHLEVEL         ${PROJECT_VERSION_PATCH})

if(PROJECT_VERSION_EXTRA)
  set(BRIDLE_VERSION_STRING     "\"${PROJECT_VERSION_WITHOUT_TWEAK}-${PROJECT_VERSION_EXTRA}\"")
else()
  set(BRIDLE_VERSION_STRING     "\"${PROJECT_VERSION_WITHOUT_TWEAK}\"")
endif()

set(BRIDLE_VERSION_CODE ${BRIDLE_VERSION_NUMBER_INT})

# Cleanup convenience variables
unset(MAJOR)
unset(MINOR)
unset(PATCH)
unset(PROJECT_VERSION_WITHOUT_TWEAK)
