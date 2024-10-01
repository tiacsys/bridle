# Copyright (c) 2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

zephyr_library()

zephyr_library_sources_ifdef(CONFIG_STEPPER_ACTION_STREAM stepper_action_stream.c)
