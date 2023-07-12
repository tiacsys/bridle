# Copyright (c) 2021-2023 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)
find_package(Bridle REQUIRED HINTS $ENV{BRIDLE_BASE})
project(bridle_common)

target_sources(app PRIVATE
  src/main.c
  )
