# SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

# Standard Bridle application boilerplate, includes Zephyr.
find_package(Bridle REQUIRED HINTS $ENV{BRIDLE_BASE})
project("RGB Matrix Colour Wheel" VERSION 0.1)

assert(CONFIG_DISPLAY "Zephyr's display driver API must be enabled")

# Add source files to the "app" target after the boilerplate above,
# which defines the target.
target_sources(app PRIVATE
    src/main.c
    src/hsv.c
    src/polar.c
)

target_include_directories(app PRIVATE
    src
)
