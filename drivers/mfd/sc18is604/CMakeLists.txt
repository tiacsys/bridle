# Copyright (c) 2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# zephyr-keep-sorted-start
zephyr_library_sources(mfd_sc18is604.c)
zephyr_library_sources(mfd_sc18is604_transfer.c)
zephyr_library_sources_ifdef(CONFIG_EMUL_MFD_SC18IS604 mfd_sc18is604_emul.c)
zephyr_library_sources_ifdef(CONFIG_MFD_SC18IS604_ASYNC mfd_sc18is604_transfer_async.c)
# zephyr-keep-sorted-stop
