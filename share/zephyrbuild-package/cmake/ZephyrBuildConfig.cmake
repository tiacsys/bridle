# Copyright (c) 2021-2023 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

if(NOT DEFINED ZEPHYR_BASE)
  message(FATAL_ERROR "ZEPHYR_BASE not set")
endif()

# The ZephyrBuildConfig is simply including Bridle package.
include(${CMAKE_CURRENT_LIST_DIR}/../../bridle-package/cmake/BridleConfig.cmake)
