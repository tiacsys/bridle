# Copyright (c) 2021-2023 TiaC Systems
# Copyright (c) 2019-2021 Li-Pro.Net
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

# Standard Bridle application boilerplate, includes Zephyr.
find_package(Bridle REQUIRED HINTS $ENV{BRIDLE_BASE})
project("Hello Shell" VERSION 0.1)

assert(CONFIG_SHELL "Zephyr's embedded shell must be enabled")

# Add your source file to the "app" target. This must come after
# the boilerplate code, which defines the target.
target_sources(app PRIVATE src/main.c)
