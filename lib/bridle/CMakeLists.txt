# Copyright (c) 2021 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

zephyr_library()

zephyr_library_sources(
  version.c
  )

zephyr_include_directories(include)
