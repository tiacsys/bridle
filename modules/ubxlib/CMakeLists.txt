# Copyright (c) 2023 Sarah Renkhoff
# SPDX-License-Identifier: Apache-2.0

if(CONFIG_UBXLIB)

# Paths we'll need
set(UBXLIB_BASE ${ZEPHYR_CURRENT_MODULE_DIR})
set(GEODESIC_DIR ${UBXLIB_BASE}/common/geofence/geographiclib)

# Helper function to add an entire source dir
function(add_src_dir dir)
file(GLOB SRCS ${dir}/*.c)
list(APPEND UBXLIB_SRC ${SRCS})
set(UBXLIB_SRC ${UBXLIB_SRC} PARENT_SCOPE)
endfunction()

if(CONFIG_ARCH_POSIX)
    # When compiling for Zephyr on Linux, need to force
    # compilation of 32-bit objects when we call ubxlib.cmake
    list(APPEND UBXLIB_COMPILE_OPTIONS "-m32")
endif() # CONFIG_ARCH_POSIX

if (NOT CONFIG_UBXLIB_LOGGING)
    list(APPEND UBXLIB_COMPILE_OPTIONS "-DU_CFG_ENABLE_LOGGING=0")
endif() # CONFIG_UBXLIB_LOGGING

# Additional library that may or may not be used
if (CONFIG_UBXLIB_GEODESIC)

    zephyr_library_named(ubxlib_geodesic)

    # Sources
    file(GLOB GEODESIC_SRC ${GEODESIC_DIR}/src/*.cpp)

    # Specific configure and build instructions
    set(GEOGRAPHICLIB_PRECISION 2)
    configure_file(
        ${GEODESIC_DIR}/include/GeographicLib/Config.h.in
        ${GEODESIC_DIR}/include/GeographicLib/Config.h
        @ONLY
    )
    set_target_properties(ubxlib_geodesic PROPERTIES CXX_STANDARD 11)

    # Library specific include dirs
    target_include_directories(ubxlib_geodesic PRIVATE
        ${GEODESIC_DIR}/include
        ${GEODESIC_DIR}/include/GeographicLib
    )

    # Extra compile options
    list(APPEND UBXLIB_COMPILE_OPTIONS
        -DGEOGRAPHICLIB_SHARED_LIB=0
        -DU_CFG_GEOFENCE_USE_GEODESIC
    )
    target_compile_options(ubxlib_geodesic PRIVATE ${UBXLIB_COMPILE_OPTIONS})

endif() # CONFIG_UBXLIB_GEODESIC

# The actual library we're building
zephyr_library_named(ubxlib)

# Include paths that should be exposed to applications ("UBXLIB_INC")
zephyr_include_directories(
    ${UBXLIB_BASE}
    ${UBXLIB_BASE}/ble/api
    ${UBXLIB_BASE}/cfg
    ${UBXLIB_BASE}/cell/api
    ${UBXLIB_BASE}/common/assert/api
    ${UBXLIB_BASE}/common/at_client/api
    ${UBXLIB_BASE}/common/error/api
    ${UBXLIB_BASE}/common/device/api
    ${UBXLIB_BASE}/common/dns/api
    ${UBXLIB_BASE}/common/geofence/api
    ${UBXLIB_BASE}/common/http_client/api
    ${UBXLIB_BASE}/common/lib_common/api
    ${UBXLIB_BASE}/common/location/api
    ${UBXLIB_BASE}/common/mqtt_client/api
    ${UBXLIB_BASE}/common/network/api
    ${UBXLIB_BASE}/common/security/api
    ${UBXLIB_BASE}/common/short_range/api
    ${UBXLIB_BASE}/common/sock/api
    ${UBXLIB_BASE}/common/spartn/api
    ${UBXLIB_BASE}/common/type/api
    ${UBXLIB_BASE}/common/ubx_protocol/api
    ${UBXLIB_BASE}/common/utils/api
    ${UBXLIB_BASE}/gnss/api
    ${UBXLIB_BASE}/port/api
    ${UBXLIB_BASE}/port/clib
    ${UBXLIB_BASE}/port/platform/common/debug_utils/api
    ${UBXLIB_BASE}/port/platform/zephyr/cfg
    ${UBXLIB_BASE}/port/platform/zephyr/src
    ${UBXLIB_BASE}/wifi/api
    ${ZEPHYR_BASE}/include
)

# Private include paths ("UBXLIB_PRIVATE_INC")
target_include_directories(ubxlib PRIVATE
    ${UBXLIB_BASE}/ble/src
    ${UBXLIB_BASE}/cell/src
    ${UBXLIB_BASE}/common/assert/src
    ${UBXLIB_BASE}/common/at_client/src
    ${UBXLIB_BASE}/common/device/src
    ${UBXLIB_BASE}/common/dns/src
    ${UBXLIB_BASE}/common/geofence/src
    ${UBXLIB_BASE}/common/http_client/src
    ${UBXLIB_BASE}/common/location/src
    ${UBXLIB_BASE}/common/mqtt_client/src
    ${UBXLIB_BASE}/common/network/src
    ${UBXLIB_BASE}/common/security/src
    ${UBXLIB_BASE}/common/short_range/src
    ${UBXLIB_BASE}/common/sock/src
    ${UBXLIB_BASE}/common/spartn/src
    ${UBXLIB_BASE}/common/ubx_protocol/src
    ${UBXLIB_BASE}/common/utils/src
    ${UBXLIB_BASE}/gnss/src
    ${UBXLIB_BASE}/gnss/src/lib_mga
    ${UBXLIB_BASE}/port/platform/common/debug_utils/src
    ${UBXLIB_BASE}/port/platform/common/event_queue
    ${UBXLIB_BASE}/port/platform/common/mutex_debug
    ${UBXLIB_BASE}/port/platform/common/log_ram
    ${UBXLIB_BASE}/wifi/src
    ${ZEPHYR_BASE}/include
)

# Hacking this in directly for now, ultimately
# we don't want the mbedtls dependency anyway!
target_include_directories(ubxlib PRIVATE
    ${ZEPHYR_BASE}/../modules/crypto/mbedtls/include
)

# Unconditional sources
add_src_dir(${UBXLIB_BASE}/common/assert/src)
add_src_dir(${UBXLIB_BASE}/common/at_client/src)
add_src_dir(${UBXLIB_BASE}/common/dns/src)
add_src_dir(${UBXLIB_BASE}/common/geofence/src)
add_src_dir(${UBXLIB_BASE}/common/http_client/src)
add_src_dir(${UBXLIB_BASE}/common/location/src)
add_src_dir(${UBXLIB_BASE}/common/lib_common/src)
add_src_dir(${UBXLIB_BASE}/common/mqtt_client/src)
add_src_dir(${UBXLIB_BASE}/common/security/src)
add_src_dir(${UBXLIB_BASE}/common/sock/src)
add_src_dir(${UBXLIB_BASE}/common/spartn/src)
add_src_dir(${UBXLIB_BASE}/common/ubx_protocol/src)
add_src_dir(${UBXLIB_BASE}/common/utils/src)
add_src_dir(${UBXLIB_BASE}/port/platform/common/debug_utils/src)
add_src_dir(${UBXLIB_BASE}/port/platform/common/event_queue)
add_src_dir(${UBXLIB_BASE}/port/platform/common/mutex_debug)
add_src_dir(${UBXLIB_BASE}/port/platform/common/log_ram)

list(APPEND UBXLIB_SRC
    ${UBXLIB_BASE}/common/device/src/u_device.c
    ${UBXLIB_BASE}/common/device/src/u_device_serial.c
    ${UBXLIB_BASE}/common/device/src/u_device_shared.c
    ${UBXLIB_BASE}/common/device/src/u_device_private.c
    ${UBXLIB_BASE}/common/device/src/u_device_private_cell_stub.c
    ${UBXLIB_BASE}/common/device/src/u_device_private_gnss_stub.c
    ${UBXLIB_BASE}/common/device/src/u_device_private_short_range_stub.c
    ${UBXLIB_BASE}/common/network/src/u_network.c
    ${UBXLIB_BASE}/common/network/src/u_network_shared.c
    ${UBXLIB_BASE}/common/network/src/u_network_private_ble_extmod_stub.c
    ${UBXLIB_BASE}/common/network/src/u_network_private_cell_stub.c
    ${UBXLIB_BASE}/common/network/src/u_network_private_gnss_stub.c
    ${UBXLIB_BASE}/common/network/src/u_network_private_wifi_stub.c
    ${UBXLIB_BASE}/port/clib/u_port_clib_mktime64.c
    ${UBXLIB_BASE}/port/platform/common/mbedtls/u_port_crypto.c
    ${UBXLIB_BASE}/port/u_port_heap.c
    ${UBXLIB_BASE}/port/u_port_timezone.c
    ${UBXLIB_BASE}/port/u_port_resource.c
    ${UBXLIB_BASE}/port/platform/zephyr/src/u_port.c
    ${UBXLIB_BASE}/port/platform/zephyr/src/u_port_debug.c
    ${UBXLIB_BASE}/port/platform/zephyr/src/u_port_os.c
    ${UBXLIB_BASE}/port/platform/zephyr/src/u_port_gpio.c
    ${UBXLIB_BASE}/port/platform/zephyr/src/u_port_uart.c
    ${UBXLIB_BASE}/port/platform/zephyr/src/u_port_i2c.c
    ${UBXLIB_BASE}/port/platform/zephyr/src/u_port_spi.c
    ${UBXLIB_BASE}/port/platform/zephyr/src/u_port_private.c
)

# Conditional sources
if (CONFIG_UBXLIB_CELL)

    add_src_dir(${UBXLIB_BASE}/cell/src)

    list (APPEND UBXLIB_SRC
        ${UBXLIB_BASE}/common/network/src/u_network_private_cell.c
        ${UBXLIB_BASE}/common/device/src/u_device_private_cell.c
    )

else()

    list(APPEND UBXLIB_SRC
        ${UBXLIB_BASE}/common/device/src/u_device_private_cell_link.c
        ${UBXLIB_BASE}/common/network/src/u_network_private_cell_link.c
    )

endif() # CONFIG_UBXLIB_CELL

if (CONFIG_UBXLIB_GEODESIC)

    target_include_directories(ubxlib PRIVATE
        ${GEODESIC_DIR}/include
        ${GEODESIC_DIR}/include/GeographicLib
    )

    zephyr_library_link_libraries(
        ubxlib_geodesic
    )

endif() # CONFIG_UBXLIB_GEODESIC

if (CONFIG_UBXLIB_GNSS)

    add_src_dir(${UBXLIB_BASE}/gnss/src)

    list(APPEND UBXLIB_SRC
        ${UBXLIB_BASE}/gnss/src/lib_mga/u_lib_mga.c
        ${UBXLIB_BASE}/common/network/src/u_network_private_gnss.c
        ${UBXLIB_BASE}/common/device/src/u_device_private_gnss.c
    )

else()

    list(APPEND UBXLIB_SRC
        ${UBXLIB_BASE}/common/device/src/u_device_private_gnss_link.c
        ${UBXLIB_BASE}/common/network/src/u_network_private_gnss_link.c
    )

endif() # CONFIG_UBXLIB_GNSS

if (CONFIG_UBXLIB_SHORTRANGE)

    add_src_dir(${UBXLIB_BASE}/common/short_range/src)
    add_src_dir(${UBXLIB_BASE}/ble/src)
    add_src_dir(${UBXLIB_BASE}/wifi/src)

    list(APPEND UBXLIB_SRC
        ${UBXLIB_BASE}/common/network/src/u_network_private_ble_extmod.c
        ${UBXLIB_BASE}/common/network/src/u_network_private_ble_intmod.c
        ${UBXLIB_BASE}/common/network/src/u_network_private_wifi.c
        ${UBXLIB_BASE}/common/device/src/u_device_private_short_range.c
    )

else()

    list(APPEND UBXLIB_SRC
        ${UBXLIB_BASE}/common/device/src/u_device_private_short_range_link.c
        ${UBXLIB_BASE}/common/network/src/u_network_private_ble_extmod_link.c
        ${UBXLIB_BASE}/common/network/src/u_network_private_wifi_link.c
    )

endif() # CONFIG_UBXLIB_SHORTRANGE

if (CONFIG_UBXLIB_OPEN_CPU_BLE)
    list(APPEND UBXLIB_SRC ${UBXLIB_BASE}/port/platform/zephyr/src/u_port_gatt.c)
endif()

if (CONFIG_MINIMAL_LIBC)
    list(APPEND UBXLIB_SRC
        ${UBXLIB_BASE}/port/clib/u_port_clib_isblank.c
        ${UBXLIB_BASE}/port/clib/u_port_clib_mktime.c
        ${UBXLIB_BASE}/port/clib/u_port_setjmp.S
        ${UBXLIB_BASE}/port/platform/zephyr/src/u_port_clib.c
    )
endif() # CONFIG_MINIMAL_LIBC

# Finally add all the accumulated sources
zephyr_library_sources(${UBXLIB_SRC})

# Any extra compile options and definitions
target_compile_options(ubxlib PRIVATE ${UBXLIB_COMPILE_OPTIONS})

if (CONFIG_UBXLIB_EDM_STREAM_DEBUG)
    target_compile_definitions(ubxlib PRIVATE U_CFG_SHORT_RANGE_EDM_STREAM_DEBUG)
endif() # CONFIG_UBXLIB_EDM_STREAM_DEBUG

if (CONFIG_UBXLIB_EDM_STREAM_DEBUG_COLOR)
    target_compile_definitions(ubxlib PRIVATE U_CFG_SHORT_RANGE_EDM_STREAM_DEBUG_COLOR)
endif() # CONFIG_UBXLIB_EDM_STREAM_DEBUG_COLOR

if (CONFIG_UBXLIB_EDM_STREAM_DEBUG_DUMP_DATA)
    target_compile_definitions(ubxlib PRIVATE U_CFG_SHORT_RANGE_EDM_STREAM_DEBUG_DUMP_DATA)
endif() # CONFIG_UBXLIB_EDM_STREAM_DEBUG_DUMP_DATA

endif() #CONFIG_UBXLIB
