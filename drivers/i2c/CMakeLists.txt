# Copyright (c) 2024-2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# Add to the existing i2c library from Zephyr instead of defining our own.
# It is actually required to add i2c drivers to that library, otherwise
# build errors can occur!
zephyr_library_amend()

# zephyr-keep-sorted-start
zephyr_library_sources_ifdef(CONFIG_I2C_SC18IS604	i2c_sc18is604.c)
zephyr_library_sources_ifdef(CONFIG_I2C_SC18IS604_CB	i2c_sc18is604_callback.c)
# zephyr-keep-sorted-stop
