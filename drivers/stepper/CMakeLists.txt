# SPDX-FileCopyrightText: Copyright (c) 2023 Carl Zeiss Meditec AG
# SPDX-FileCopyrightText: Copyright (c) 2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

zephyr_syscall_header(${BRIDLE_BASE}/include/zephyr/drivers/stepper.h)

zephyr_library()

zephyr_library_sources(stepper_common.c)

zephyr_library_sources_ifdef(CONFIG_STEPPER_GPIO stepper_gpio.c)

if(CONFIG_STEPPER_INFO)
# Prepare the stepper motor info list symbol in ROM for the linker
# similar to Zephyr's common iterable sections as declared in
# zephyr/cmake/linker_script/common/common-rom.cmake          and
# zephyr/include/zephyr/linker/common-rom/common-rom-misc.ld  see:
# https://docs.zephyrproject.org/latest/kernel/iterable_sections/index.html

zephyr_iterable_section(NAME stepper_info KVMA RAM_REGION GROUP RODATA_REGION SUBALIGN CONFIG_LINKER_ITERABLE_SUBALIGN)
zephyr_linker_sources(SECTIONS stepper_info.ld)
endif()
