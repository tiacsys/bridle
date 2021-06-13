# Copyright (c) 2021 TiaC Systems
# Copyright (c) 2019-2021 Li-Pro.Net
# SPDX-License-Identifier: Apache-2.0

zephyr_library()

# Bridle commands
zephyr_library_sources_ifdef(CONFIG_BRIDLE_SHELL bridle_service.c)

# simple hello command
zephyr_library_sources_ifdef(CONFIG_BRIDLE_CMD_HELLO cmd_hello.c)
