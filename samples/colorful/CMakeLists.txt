# SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

# Standard Bridle application boilerplate, includes Zephyr.
find_package(Bridle REQUIRED HINTS $ENV{BRIDLE_BASE})
project("Colorful LCD or LED strip (matrix) as display" VERSION 0.1)

target_sources(app PRIVATE src/main.c src/colorful.c)
