# Copyright (c) 2020 Linumiz
# SPDX-License-Identifier: Apache-2.0

if(CONFIG_QPC)

message(STATUS "QPC is configured")

set(QPC_DIR ${ZEPHYR_CURRENT_MODULE_DIR})

zephyr_library_named(qpc)
zephyr_include_directories(${QPC_DIR}/include)

target_include_directories(qpc PRIVATE ${CMAKE_CURRENT_LIST_DIR})

target_compile_definitions(qpc PRIVATE Q_NASSERT)

zephyr_library_sources(
  qpc_port.c
  ${QPC_DIR}/src/qf/qep_hsm.c
)

message(STATUS ${ZEPHYR_CURRENT_MODULE_DIR})
endif()
