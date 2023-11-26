# Copyright (c) 2023 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

# Standard Bridle application boilerplate, includes Zephyr.
find_package(Bridle REQUIRED HINTS $ENV{BRIDLE_BASE})
project("Buzzer Shell" VERSION 0.1)

assert(CONFIG_SHELL "Zephyr's embedded shell must be enabled")

# Add your source file to the "app" target. This must come after
# the boilerplate code, which defines the target.
target_sources(app PRIVATE
    src/main.c
    src/shell.c
    src/buzzer.c
    src/song_beep.c
    src/song_folksong.c
    src/song_xmastime.c
    src/song_funkytown.c
    src/song_mario.c
    src/song_golioth.c
    src/song_tiacsys.c
)

target_include_directories(app PRIVATE
    src
)
