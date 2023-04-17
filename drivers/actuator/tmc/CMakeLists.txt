# Copyright (c) 2023 TiaC Systems
#
# SPDX-License-Identifier: Apache-2.0

zephyr_library()

zephyr_library_sources_ifdef(CONFIG_TMC2130 tmc2130.c)
