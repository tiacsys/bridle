# Copyright (c) 2021-2022 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

# Standard Bridle application boilerplate, includes Zephyr.
find_package(Bridle REQUIRED HINTS $ENV{BRIDLE_BASE})
project("Fancy Button" VERSION 0.1)

target_sources(app PRIVATE src/init.c)

target_sources_ifdef(CONFIG_APPLICATION_MODE_POLLING app PRIVATE
    src/poll.c
)

target_sources_ifdef(CONFIG_APPLICATION_MODE_INTERRUPT app PRIVATE
    src/event.c
)
