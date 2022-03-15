# Copyright (c) 2020 Linumiz
# SPDX-License-Identifier: Apache-2.0

if(CONFIG_QPC)

message(STATUS "QPC is configured")
message(STATUS "CONFIG_QPC_NO_QASSERT ${CONFIG_QPC_NO_QASSERT}")

set(QPC_DIR ${ZEPHYR_CURRENT_MODULE_DIR})

zephyr_include_directories(${QPC_DIR}/include)
zephyr_include_directories(${CMAKE_CURRENT_LIST_DIR})
zephyr_include_directories_ifdef(CONFIG_QPC_AO_SUPPORT ${QPC_DIR}/src)

zephyr_compile_definitions_ifdef(CONFIG_QPC_NO_QASSERT Q_NASSERT)

zephyr_library_sources(
  qep_port.c
  ${QPC_DIR}/src/qf/qep_hsm.c
)

zephyr_library_sources_ifdef(
  CONFIG_QPC_AO_SUPPORT
  ${QPC_DIR}/src/qf/qf_act.c
)

message(STATUS ${ZEPHYR_CURRENT_MODULE_DIR})
endif()
