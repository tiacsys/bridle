# SPDX-FileCopyrightText: 2021-2026 TiaC Systems
# SPDX-FileCopyrightText: 2019-2021 Li-Pro.Net
# SPDX-License-Identifier: Apache-2.0

# zephyr-keep-sorted-start
add_subdirectory_ifdef(CONFIG_DISPLAY display)
add_subdirectory_ifdef(CONFIG_GPIO gpio)
add_subdirectory_ifdef(CONFIG_I2C i2c)
add_subdirectory_ifdef(CONFIG_MFD mfd)
add_subdirectory_ifdef(CONFIG_SENSOR sensor)
add_subdirectory_ifdef(CONFIG_SERIAL serial)
# zephyr-keep-sorted-stop
