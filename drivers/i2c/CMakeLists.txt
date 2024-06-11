# Copyright (c) 2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# Add to the existing i2c library from zephyr instead of defining our own.
# It is actually required to add I2C drivers to that library, otherwise
# build errors can occur!
zephyr_library_amend()

zephyr_library_sources_ifdef(CONFIG_I2C_SC18IS604 i2c_sc18is604.c)
zephyr_library_sources_ifdef(CONFIG_I2C_CALLBACK i2c_sc18is604_callback.c)
