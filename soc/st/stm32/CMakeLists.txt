# Copyright (c) 2024 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

if(HWMv2)
  message(NOTICE "
          ---------------------------------------------------------------------
          --- NOTICE: Unofficially supported SoC ${SOC_NAME} will be used,  ---
          --- relying on upstream startup and initialization code in:       ---
          --- zephyr/soc/st/${SOC_FAMILY} and"
            " zephyr/soc/st/${SOC_FAMILY}/${SOC_SERIES}          ---
          ---------------------------------------------------------------------"
         )
  add_subdirectory(
    ${ZEPHYR_BASE}/soc/st/${SOC_FAMILY} ${CMAKE_CURRENT_BINARY_DIR}/zephyr
    )
else()
  message(FATAL_ERROR "HWMv1 SoCs are not supported and must be "
                      "replaced by HWMv2.")
endif()
