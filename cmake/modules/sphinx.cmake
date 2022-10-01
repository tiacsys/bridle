# Copyright (c) 2022 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

include_guard(GLOBAL)

# The code line below defines the real minimum supported CMake version.
#
# Unfortunately CMake requires the toplevel `CMakeLists.txt` file to define the
# required version, not even invoking it from a CMake module is sufficient. It
# is however permitted to have multiple invocations of cmake_minimum_required.
cmake_minimum_required(VERSION 3.20.0)

# Looking for required Sphinx version.
find_package(Sphinx ${ZEPHYR_SPHINX_REQUIRED_VERSION}
                    REQUIRED build)

if(NOT TARGET Sphinx::build)
  message(FATAL_ERROR "The 'sphinx-build' command was not found.\n"
                      "Make sure you have run pip install properly.")
else()
  get_target_property(SPHINX_BUILD_EXECUTABLE Sphinx::build IMPORTED_LOCATION)
  mark_as_advanced(SPHINX_BUILD_EXECUTABLE)
endif()

set(SPHINXBUILD ${SPHINX_BUILD_EXECUTABLE})
