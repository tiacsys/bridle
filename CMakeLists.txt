# Copyright (c) 2019-2021 Li-Pro.Net
# SPDX-License-Identifier: Apache-2.0

# set to know where our project lies
set(BRIDLE_DIR "${CMAKE_CURRENT_LIST_DIR}"
    CACHE PATH "Bridle root directory")

# include custom headers for e.g. drivers or services sorted by sub-folders
zephyr_include_directories(include)

# add custom services (e.g. control engines)
add_subdirectory(services)

# add custom sub-system modules (e.g. logging)
add_subdirectory(subsys)

# add custom device drivers (e.g. sensor and actuator chips)
add_subdirectory(drivers)

# add custom support libraries (e.g. commands)
add_subdirectory(lib)

# add external 3rd party modules (e.g. MicroPython or LUA)
add_subdirectory(modules)
