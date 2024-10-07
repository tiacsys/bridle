# Copyright (c) 2021-2024 TiaC Systems
# Copyright (c) 2019-2021 Li-Pro.Net
# SPDX-License-Identifier: Apache-2.0

# add_subdirectory_ifdef(CONFIG_name name)

add_subdirectory(bridle)
add_subdirectory_ifdef(CONFIG_MOTION motion)
