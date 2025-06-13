# Copyright (c) 2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

zephyr_library_amend()

zephyr_library_sources_ifdef(CONFIG_PINCTRL_WCH_X035_AFIO pinctrl_wch_x035_afio.c)
