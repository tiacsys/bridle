# Copyright (c) 2023 TiaC Systems
#
# SPDX-License-Identifier: Apache-2.0

if(CONFIG_HAS_TMCAPI)

  set(tmc_api "${ZEPHYR_CURRENT_MODULE_DIR}")
  zephyr_include_directories(${tmc_api})

  zephyr_library_sources_ifdef(CONFIG_HAS_TMCHELPERS
      ${tmc_api}/tmc/helpers/CRC.c
      ${tmc_api}/tmc/helpers/Functions.c
  )

  zephyr_library_sources_ifdef(CONFIG_HAS_TMCRAMP
      ${tmc_api}/tmc/ramp/Ramp.c
      ${tmc_api}/tmc/ramp/LinearRamp.c
      ${tmc_api}/tmc/ramp/LinearRamp1.c
  )

  set(tmc_chips
      max22216
      tmc2041
      tmc2130
      tmc2160
      tmc2208
      tmc2209
      tmc2224
      tmc2225
      tmc2226
      tmc2240
      tmc2300
      tmc2590
      tmc262
      tmc2660
      tmc389
      tmc4210
      tmc424
      tmc429
      tmc4330
      tmc4331
      tmc4361
      tmc4361a
      tmc43xx
      tmc457
      tmc4670
      tmc4671
      tmc5031
      tmc5041
      tmc5062
      tmc5072
      tmc5130
      tmc5160
      tmc5240
      tmc5271
      tmc5272
      tmc6100
      tmc6200
      tmc7300
      tmc8461
      tmc8462
      tmc846x
      )

  foreach(tmc_chip ${tmc_chips})

    string(TOUPPER ${tmc_chip} tmc_chip_to_upper)
    if(CONFIG_USE_TCMAPI_${tmc_chip_to_upper})

      set(tmc_chip_dir ${tmc_api}/tmc/ic/${tmc_chip_to_upper})
      if(EXISTS ${tmc_chip_dir})

        zephyr_include_directories(${tmc_chip_dir})

        set(tmc_chip_api ${tmc_chip_dir}/${tmc_chip_to_upper}.c)
        if(EXISTS ${tmc_chip_api})

          zephyr_library_sources(${tmc_chip_api})

        endif()

      endif()

    endif()

    unset(tmc_chip_dir)
    unset(tmc_chip_api)

  endforeach()

endif()
