# Copyright (c) 2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

zephyr_library()

# zephyr-keep-sorted-start
zephyr_library_sources_ifdef(CONFIG_BOARD_COFFEECALLER_NRF52 coffeecaller_nrf52_nrf52840.c)
# zephyr-keep-sorted-stop
