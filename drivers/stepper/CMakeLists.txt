# SPDX-FileCopyrightText: Copyright (c) 2023 Carl Zeiss Meditec AG
# SPDX-FileCopyrightText: Copyright (c) 2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

zephyr_syscall_header(${BRIDLE_BASE}/include/zephyr/drivers/stepper.h)

zephyr_library()

zephyr_library_sources_ifdef(CONFIG_STEPPER_SHELL stepper_shell.c)
