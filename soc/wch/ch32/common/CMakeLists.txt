# TODO move to hal_wch
set(WCH_SDK_DIR ${ZEPHYR_BASE}/../modules/hal/openwch/${SOC_SERIES}/EVT/EXAM/SRC)

file(GLOB WCH_SDK_SRCS
    ${WCH_SDK_DIR}/Peripheral/src/*.c
    ${WCH_SDK_DIR}/Core/*.c
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
