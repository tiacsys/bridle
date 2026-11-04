# SPDX-FileCopyrightText: 2021-2026 TiaC Systems
# SPDX-FileCopyrightText: 2019-2021 Li-Pro.Net
# SPDX-License-Identifier: Apache-2.0

zephyr_library()

# Bridle commands
# zephyr-keep-sorted-start
zephyr_library_sources_ifdef(CONFIG_BRIDLE_CMD_HELLO cmd_hello.c)
zephyr_library_sources_ifdef(CONFIG_BRIDLE_SHELL bridle_service.c)
# zephyr-keep-sorted-stop
