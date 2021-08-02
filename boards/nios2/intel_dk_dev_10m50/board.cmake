# SPDX-License-Identifier: Apache-2.0

board_runner_args(nios2 "--cpu-sof=${ZEPHYR_GHRD_SOCFPGA_MODULE_DIR}/nios2f-zephyr/dk-dev-10m50-a/ghrd_10m50daf484c6ges.sof")
include(${ZEPHYR_BASE}/boards/common/nios2.board.cmake)
