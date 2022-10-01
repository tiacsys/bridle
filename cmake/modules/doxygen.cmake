# Copyright (c) 2022 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

include_guard(GLOBAL)

# The code line below defines the real minimum supported CMake version.
#
# Unfortunately CMake requires the toplevel `CMakeLists.txt` file to define the
# required version, not even invoking it from a CMake module is sufficient. It
# is however permitted to have multiple invocations of cmake_minimum_required.
cmake_minimum_required(VERSION 3.20.0)

# Looking for required Doxygen version.
find_package(Doxygen ${BRIDLE_DOXYGEN_REQUIRED_VERSION}
                     REQUIRED dot mscgen)

if(NOT TARGET Doxygen::doxygen)
  message(FATAL_ERROR "The 'doxygen' command was not found.\n"
                      "Make sure you have install the required tools.")
else()
  get_target_property(DOXYGEN_EXECUTABLE Doxygen::doxygen IMPORTED_LOCATION)
  mark_as_advanced(DOXYGEN_EXECUTABLE)
endif()

if(NOT TARGET Doxygen::dot)
  message(FATAL_ERROR "The Graphviz 'dot' command was not found.\n"
                      "Make sure you have install the required tools.")
else()
  get_target_property(DOXYGEN_DOT_EXECUTABLE Doxygen::dot IMPORTED_LOCATION)
  mark_as_advanced(DOXYGEN_DOT_EXECUTABLE)
endif()

if(NOT TARGET Doxygen::mscgen)
  message(NOTICE "The optional 'mscgen' command was not found.\n")
else()
  get_target_property(DOXYGEN_MSCGEN_EXECUTABLE Doxygen::mscgen IMPORTED_LOCATION)
  mark_as_advanced(DOXYGEN_MSCGEN_EXECUTABLE)
endif()
