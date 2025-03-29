# Copyright (c) 2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

# Standard Bridle application boilerplate, includes Zephyr.
find_package(Bridle REQUIRED HINTS $ENV{BRIDLE_BASE})
project("STK8BA58 3-Axis Accelerometer Sample" VERSION 0.1)

FILE(GLOB app_sources src/*.c)
target_sources(app PRIVATE ${app_sources})
