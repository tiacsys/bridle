# Copyright (c) 2021-2022 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# Relative directory of Bridle directoryy as seen from the
# ZephyrExtension package file.
set(BRIDLE_RELATIVE_DIR "../../..")

# Set the current BRIDLE_BASE
# The use of get_filename_component ensures that the final path variable will not contain `../..`.
get_filename_component(BRIDLE_BASE ${CMAKE_CURRENT_LIST_DIR}/${BRIDLE_RELATIVE_DIR} ABSOLUTE)

if(NOT NO_BOILERPLATE)
  include(${BRIDLE_BASE}/cmake/boilerplate.cmake NO_POLICY_SCOPE)
endif()
