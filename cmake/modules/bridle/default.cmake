# Copyright (c) 2022 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# The purpose of this file is to extend the list of CMake modules to be loaded
# by Zephyr (zephyr_cmake_modules) with the Bridle specific modules. This is
# possible at this point, since Zephyr first runs through all known Zephyr
# build configurations via CMake find_package, before Zephyr itself includes
# its own preset modules via the zephyr_cmake_modules list.

include_guard(GLOBAL)

# The code line below defines the real minimum supported CMake version.
#
# Unfortunately CMake requires the toplevel `CMakeLists.txt` file to define the
# required version, not even invoking it from a CMake module is sufficient. It
# is however permitted to have multiple invocations of cmake_minimum_required.
cmake_minimum_required(VERSION 3.20.0)

# Load Bridle defaults
list(APPEND zephyr_cmake_modules bridle/requirements)
list(APPEND zephyr_cmake_modules bridle/version)
list(APPEND zephyr_cmake_modules bridle/toolchain)
