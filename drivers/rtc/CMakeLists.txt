# Copyright (c) 2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# Add to the existing rtc library from zephyr instead of defining our own.
# It is actually required to add RTC drivers to that library, otherwise
# build errors can occur!
zephyr_library_amend()

zephyr_library_sources_ifdef(CONFIG_RTC_DS3231 rtc_ds3231.c)
