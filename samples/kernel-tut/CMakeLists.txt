# Copyright (c) 2023 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

# Standard Zephyr application boilerplate.
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project("Kernel Tutorial" VERSION 0.1)

zephyr_sources_ifdef(CONFIG_TUTORIAL_1 src/tut_1.c)
zephyr_sources_ifdef(CONFIG_TUTORIAL_2 src/tut_2.c)


target_sources(app PRIVATE src/dummy.c)
