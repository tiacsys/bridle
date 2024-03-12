# Copyright (c) 2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

zephyr_library_amend()

zephyr_library_sources_ifdef(CONFIG_I2C_SC18IS604 i2c_sc18is604.c)
