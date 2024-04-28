# Copyright (c) 2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

include_guard(GLOBAL)

# Process board extensions
if(BOARD_EXTENSIONS)
  foreach(board_extension_dir ${BOARD_EXTENSION_DIRS})
    include(${board_extension_dir}/board.cmake OPTIONAL)
  endforeach()
endif()

if(DEFINED BOARD_FLASH_RUNNER)
  set(BOARD_FLASH_RUNNER ${BOARD_FLASH_RUNNER} PARENT_SCOPE)
endif()

if(DEFINED BOARD_DEBUG_RUNNER)
  set(BOARD_DEBUG_RUNNER ${BOARD_DEBUG_RUNNER} PARENT_SCOPE)
endif()
