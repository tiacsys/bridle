# Copyright (c) 2022 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
#
# This CMake module will load all Zephyr CMake modules required for a
# documentation build.
#
# The following CMake modules will be loaded:
# - doxygen
# - sphinx
#
# Outcome:
# The Bridle package required for documentation build setup.

include_guard(GLOBAL)

include(doxygen)
include(sphinx)
