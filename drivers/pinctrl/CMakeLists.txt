# Copyright (c) 2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

zephyr_library_amend()

zephyr_library_sources_ifdef(CONFIG_PINCTRL_CH32X035_AFIO pinctrl_ch32x035_afio.c)
