# Copyright (c) 2023 TiaC Systems
#
# SPDX-License-Identifier: Apache-2.0

add_subdirectory_ifdef(CONFIG_TMC tmc)

if(CONFIG_USERSPACE OR CONFIG_BRIDLE_ACTUATOR_SHELL)
# The above if() is needed or else CMake would complain about empty library.

zephyr_library()
zephyr_library_sources_ifdef(CONFIG_USERSPACE actuator_handlers.c)
zephyr_library_sources_ifdef(CONFIG_BRIDLE_ACTUATOR_SHELL actuator_shell.c)

endif()

if(CONFIG_BRIDLE_ACTUATOR_INFO)
# Prepare the actuator info list symbol in ROM for the linker
# similar to Zephyr's common iterable sections as declared in
# zephyr/cmake/linker_script/common/common-rom.cmake          and
# zephyr/include/zephyr/linker/common-rom/common-rom-misc.ld  see:
# https://docs.zephyrproject.org/latest/kernel/iterable_sections/index.html

zephyr_iterable_section(NAME actuator_info KVMA RAM_REGION GROUP RODATA_REGION SUBALIGN 4)
zephyr_linker_sources(SECTIONS actuator_info.ld)
endif()
