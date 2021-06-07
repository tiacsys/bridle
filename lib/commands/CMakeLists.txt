# Copyright (c) 2021 TiaC Systems
# Copyright (c) 2019-2021 Li-Pro.Net
# SPDX-License-Identifier: Apache-2.0

zephyr_library()

# simple hello command
zephyr_library_sources_ifdef(CONFIG_BRIDLE_CMD_HELLO cmd_hello.c)
