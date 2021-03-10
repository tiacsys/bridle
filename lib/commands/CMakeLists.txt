# Copyright (c) 2019-2021 Li-Pro.Net
# SPDX-License-Identifier: Apache-2.0

zephyr_library()

#example hello command
zephyr_library_sources_ifdef(CONFIG_LPNB_CMD_HELLO cmd_hello.c)
