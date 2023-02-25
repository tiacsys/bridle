# Copyright (c) 2022-2023 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(i2c_target_api)

# still using Zephyr's sources
FILE(GLOB app_sources ${ZEPHYR_BASE}/tests/drivers/i2c/i2c_target_api/src/*.c)
target_sources(app PRIVATE ${app_sources})

zephyr_sources_ifdef(CONFIG_I2C_VIRTUAL
${ZEPHYR_BASE}/tests/drivers/i2c/i2c_target_api/common/i2c_virtual.c)
