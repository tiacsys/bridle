# Copyright (c) 2025 TiaC Systems
# Copyright (c) 2024 Matthew Tran
# SPDX-License-Identifier: Apache-2.0

# TODO move to hal_wch
set(WCH_SDK_DIR ${ZEPHYR_BASE}/../modules/hal/openwch/${SOC_SERIES}/EVT/EXAM/SRC)

file(GLOB WCH_SDK_SRCS
    ${WCH_SDK_DIR}/Core/core_riscv.c
    ${WCH_SDK_DIR}/Peripheral/src/ch32x035_usart.c
)

zephyr_sources(
    idle.c
    irq.c
    startup.c
    timer.c
    ${WCH_SDK_SRCS}
)

zephyr_include_directories(
    .
    ${WCH_SDK_DIR}/Peripheral/inc
    ${WCH_SDK_DIR}/Core
)
