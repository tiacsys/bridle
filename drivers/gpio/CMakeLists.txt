# Copyright (c) 2021-2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# Add to the existing gpio library from zephyr instead of defining our own.
# It is actually required to add GPIO drivers to that library, otherwise
# build errors can occur!
zephyr_library_amend()

zephyr_library_sources_ifdef(CONFIG_GPIO_PCA9554_REGRST	gpio_pca9554_regrst.c)
zephyr_library_sources_ifdef(CONFIG_GPIO_PCA9555_REGRST	gpio_pca9555_regrst.c)
zephyr_library_sources_ifdef(CONFIG_GPIO_SC16IS75X	gpio_sc16is75x.c)
zephyr_library_sources_ifdef(CONFIG_GPIO_SC18IS604	gpio_sc18is604.c)
zephyr_library_sources_ifdef(CONFIG_GPIO_SIPOMUX	gpio_sipomux.c)
