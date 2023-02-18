# Copyright (c) 2022 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# The purpose of this file is to load Bridle specific modules.

include_guard(GLOBAL)

# The code line below defines the real minimum supported CMake version.
#
# Unfortunately CMake requires the toplevel `CMakeLists.txt` file to define the
# required version, not even invoking it from a CMake module is sufficient. It
# is however permitted to have multiple invocations of cmake_minimum_required.
cmake_minimum_required(VERSION 3.20.0)

# Load Bridle defaults
list(APPEND bridle_cmake_modules bridle/requirements)
list(APPEND bridle_cmake_modules bridle/version)
list(APPEND bridle_cmake_modules bridle/toolchain)

foreach(module IN LISTS bridle_cmake_modules)
  # Ensures any module of type `${module}` are properly expanded to list before
  # passed on the `include(${module})`.
  # This is done twice to support cases where the content of `${module}` itself
  # contains a variable, like `${BOARD_DIR}`.
  string(CONFIGURE "${module}" module)
  string(CONFIGURE "${module}" module)
  include(${module})

  list(REMOVE_ITEM SUB_COMPONENTS ${module})
  if(DEFINED SUB_COMPONENTS AND NOT SUB_COMPONENTS)
    # All requested Bridle CMake modules have been loaded, so let's return.
    return()
  endif()
endforeach()
