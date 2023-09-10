# Copyright (c) 2023 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# Suppress "simple_bus_reg" on RP2xxx boards as long as the phandles
# "peripheral-clk" and "system-clk" are located below "soc" but have
# compatibility to "fixed-clock" that can't have the "reg" property.
list(APPEND EXTRA_DTC_FLAGS "-Wno-simple_bus_reg")
