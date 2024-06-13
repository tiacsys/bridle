# Copyright (c) 2023-2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# Add to the existing mfd library from zephyr instead of defining our own.
# It is actually required to add MFD drivers to that library, otherwise
# build errors can occur!
zephyr_library_amend()

zephyr_library_sources_ifdef(CONFIG_MFD_DS3231		mfd_ds3231.c)
zephyr_library_sources_ifdef(CONFIG_MFD_SIPOMUXGP	mfd_sipomuxgp.c
							mfd_sipomuxgp_workq.c)
zephyr_library_sources_ifdef(CONFIG_MFD_SIPOMUXGP_SPI	mfd_sipomuxgp_spi.c)

zephyr_library_sources_ifdef(CONFIG_MFD_SC18IS604 mfd_sc18is604.c)
zephyr_library_sources_ifdef(CONFIG_MFD_SC18IS604 mfd_sc18is604_transfer.c)
zephyr_library_sources_ifdef(CONFIG_MFD_SC18IS604_ASYNC mfd_sc18is604_transfer_async.c)
