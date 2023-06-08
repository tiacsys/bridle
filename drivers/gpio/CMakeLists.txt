# Copyright (c) 2021-2023 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# Add to the existing gpio library from zephyr instead of defining our own.
# It is actually required to add GPIO drivers to that library, otherwise
# build errors can occur!
zephyr_library_amend()
