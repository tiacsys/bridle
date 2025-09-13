# Copyright (c) 2023-2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# Add to the existing display library from Zephyr instead of defining our own.
# It is actually required to add display drivers to that library, otherwise
# build errors can occur!
zephyr_library_amend()

# zephyr-keep-sorted-start
zephyr_library_sources_ifdef(CONFIG_DISPLAY_SIPOMUX display_sipomux.c)
# zephyr-keep-sorted-stop
