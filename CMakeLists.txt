# Copyright (c) 2021-2022 TiaC Systems
# Copyright (c) 2019-2021 Li-Pro.Net
# SPDX-License-Identifier: Apache-2.0

# Set to know where our project lies.
set(BRIDLE_BASE "${CMAKE_CURRENT_LIST_DIR}"
    CACHE PATH "Bridle root directory")

# Generate our version header and inject into all builds.
add_custom_command(
  OUTPUT ${PROJECT_BINARY_DIR}/include/generated/version_bridle.h
  COMMAND ${CMAKE_COMMAND}
    -DZEPHYR_BASE=${ZEPHYR_BASE}
    -DBRIDLE_BASE=${BRIDLE_BASE}
    -DOUT_DIR=${PROJECT_BINARY_DIR}/include/generated
    -DOUT_FILE=version_bridle.h
    -DEXT_FILE=version.h
    -P ${BRIDLE_BASE}/cmake/gen_version_h.cmake
  DEPENDS ${BRIDLE_BASE}/VERSION ${git_dependency}
)
add_custom_target(version_bridle_h
  DEPENDS ${PROJECT_BINARY_DIR}/include/generated/version_bridle.h)
add_dependencies(zephyr_interface version_bridle_h)

add_custom_target(version_h
  DEPENDS ${PROJECT_BINARY_DIR}/include/generated/version.h)
add_dependencies(version_bridle_h version_h)

# include custom headers for e.g. drivers or services sorted by sub-folders
zephyr_include_directories(include)

# Unfortunately, the order in which CMakeLists.txt code is processed
# matters so we need to be careful about how we order the processing
# of subdirectories.
#
# Lib is placed early because it defines important common supports
# that must be exported to other source partitions, e.g. subsys/.

# add custom support libraries (e.g. algorithms)
add_subdirectory(lib)

# add custom services (e.g. control engines)
add_subdirectory(services)

# add custom sub-system modules (e.g. shell commands or logging)
add_subdirectory(subsys)

# add custom device drivers (e.g. sensor and actuator chips)
add_subdirectory(drivers)

# add external 3rd party modules (e.g. MicroPython or LUA)
add_subdirectory(modules)
