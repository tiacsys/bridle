# Copyright (c) 2023-2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# Add to the existing mfd library from zephyr instead of defining our own.
# It is actually required to add MFD drivers to that library, otherwise
# build errors can occur!
zephyr_library_amend()

zephyr_library_sources_ifdef(CONFIG_MFD_SC16IS75X	mfd_sc16is75x.c)
zephyr_library_sources_ifdef(CONFIG_MFD_SC16IS75X_SPI	mfd_sc16is75x_spi.c)
zephyr_library_sources_ifdef(CONFIG_MFD_SC16IS75X_I2C	mfd_sc16is75x_i2c.c)
zephyr_library_sources_ifdef(CONFIG_MFD_SC16IS75X_ASWQ	mfd_sc16is75x_async.c)
zephyr_library_sources_ifdef(CONFIG_MFD_SIPOMUXGP	mfd_sipomuxgp.c
							mfd_sipomuxgp_workq.c)
zephyr_library_sources_ifdef(CONFIG_MFD_SIPOMUXGP_SPI	mfd_sipomuxgp_spi.c)

add_subdirectory_ifdef(CONFIG_MFD_SC18IS604 sc18is604)
