# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(very-simple-app)


target_sources_ifdef(
			CONFIG_APPLICATION_MODE_POLLING
			app PRIVATE
            src/poll.c
)

target_sources_ifdef(
			CONFIG_APPLICATION_MODE_INTERRUPT
			app PRIVATE
            src/event.c
)

target_sources(
	app PRIVATE
	src/init.c
)
