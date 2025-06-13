# Copyright (c) 2025 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

if(HWMv2)
  message(NOTICE "\n"
    "\t---------------------------------------------------------------------\n"
    "\t--- NOTICE: Use unofficially supported SoC:\t'${SOC_NAME}'\n"
    "\t--- Relying on upstream startup and initialization code in:\n"
    "\t---\t'zephyr/soc/wch/${SOC_FAMILY}'\n"
    "\t---\t'zephyr/soc/wch/${SOC_FAMILY}/${SOC_SERIES}'\n"
    "\t---------------------------------------------------------------------\n"
    )
  add_subdirectory(
    ${ZEPHYR_BASE}/soc/wch/${SOC_FAMILY} ${CMAKE_CURRENT_BINARY_DIR}/zephyr
    )
else()
  message(FATAL_ERROR "HWMv1 SoCs are not supported and must be "
                      "replaced by HWMv2.")
endif()
