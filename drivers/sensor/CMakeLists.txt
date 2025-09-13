# Copyright (c) 2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# Add to the existing sensor library from Zephyr instead of defining our own.
# It is actually required to add sensor drivers to that library, otherwise
# build errors can occur!
zephyr_library_amend()

# zephyr-keep-sorted-start
add_subdirectory(sensortek)
# zephyr-keep-sorted-stop
