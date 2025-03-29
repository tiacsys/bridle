# Copyright (c) 2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

zephyr_library()

zephyr_library_sources(stk8ba58.c stk8ba58_reg.c)
zephyr_library_sources_ifdef(CONFIG_STK8BA58_TRIGGER stk8ba58_trigger.c)
