# SPDX-License-Identifier: Apache-2.0

set(SUPPORTED_EMU_PLATFORMS renode qemu)
set(RENODE_SCRIPT ${CMAKE_CURRENT_LIST_DIR}/../../../renode/nucleo_f401re.resc)
set(RENODE_UART sysbus.uart2)