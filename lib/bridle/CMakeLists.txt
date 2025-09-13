# Copyright (c) 2021-2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

zephyr_library()

# zephyr-keep-sorted-start
zephyr_library_sources(
  version.c
  )
# zephyr-keep-sorted-stop

# zephyr-keep-sorted-start
zephyr_include_directories(include)
# zephyr-keep-sorted-stop
