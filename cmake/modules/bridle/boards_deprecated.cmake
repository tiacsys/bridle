# Copyright (c) 2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# If board name is deprecated, then board will be adjusted to new board name and
# a deprecation warning will be printed to the user, later by Zephyr validation.

include_guard(GLOBAL)

if(EXISTS ${BRIDLE_BASE}/boards/deprecated.cmake)
  include(${BRIDLE_BASE}/boards/deprecated.cmake)
endif()
