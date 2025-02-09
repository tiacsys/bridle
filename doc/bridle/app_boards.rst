.. _app_boards:

Board support
#############

.. contents::
   :local:
   :depth: 2

The |BRIDLE| provides board definitions for all |TIAC| devices.
In addition, you can define custom boards.

.. _gs_programming_board_names:

Board names
***********

The following tables list all boards and build targets for |TIAC|
hardware platforms.

Boards included in tiac-zephyr
==============================

The following boards are defined in the :file:`zephyr/boards/` folder.
Also see the |zephyr:boards| section in the |ZEPHYR| documentation.
Bridle provides some standard board extensions. For more details, see
the :ref:`boards-extensions` section in this documentation.

+-------------------+------------------------------------+--------------------------------------------+
| Hardware platform | Board name                         | Build target                               |
+===================+====================================+============================================+
| Native            | |zephyr:board:native_posix|        | | ``native_posix``                         |
|                   |                                    | | ``native_posix/native/64``               |
|                   +------------------------------------+--------------------------------------------+
|                   | |zephyr:board:native_sim|          | | ``native_sim``                           |
|                   |                                    | | ``native_sim/native/64``                 |
+-------------------+------------------------------------+--------------------------------------------+
| Emulator          | |zephyr:board:qemu_x86|            | | ``qemu_x86``                             |
|                   |                                    | | ``qemu_x86_64``                          |
|                   +------------------------------------+--------------------------------------------+
|                   | |zephyr:board:qemu_cortex_m3|      | ``qemu_cortex_m3``                         |
+-------------------+------------------------------------+--------------------------------------------+
| ATSAMD21G18A      | |zephyr:board:arduino_zero|        | ``arduino_zero``                           |
|                   +------------------------------------+--------------------------------------------+
|                   | |zephyr:board:seeeduino_xiao|      | ``seeeduino_xiao``                         |
+-------------------+------------------------------------+--------------------------------------------+
| i.MX RT1010       | |zephyr:board:mimxrt1010_evk|      | ``mimxrt1010_evk``                         |
+-------------------+------------------------------------+--------------------------------------------+
| i.MX RT1060       | |zephyr:board:mimxrt1060_evk|      | | ``mimxrt1060_evk/mimxrt1062/hyperflash`` |
|                   |                                    | | ``mimxrt1060_evk@A/mimxrt1062/qspi``     |
|                   |                                    | | ``mimxrt1060_evk@B/mimxrt1062/qspi``     |
|                   |                                    | | ``mimxrt1060_evk@C/mimxrt1062/qspi``     |
+-------------------+------------------------------------+--------------------------------------------+
| i.MX RT1170 (CM7) | |zephyr:board:mimxrt1170_evk|      | | ``mimxrt1170_evk/mimxrt1176/cm4``        |
|                   |                                    | | ``mimxrt1170_evk/mimxrt1176/cm7``        |
|                   |                                    | | ``mimxrt1170_evk@B/mimxrt1176/cm4``      |
|                   |                                    | | ``mimxrt1170_evk@B/mimxrt1176/cm7``      |
+-------------------+------------------------------------+--------------------------------------------+
| nRF52840          | |zephyr:board:nrf52840dk_nrf52840| | ``nrf52840dk/nrf52840``                    |
|                   +------------------------------------+--------------------------------------------+
|                   | |zephyr:board:nrf9160dk_nrf52840|  | ``nrf9160dk/nrf52840``                     |
+-------------------+------------------------------------+--------------------------------------------+
| nRF9160           | |zephyr:board:nrf9160dk_nrf9160|   | | ``nrf9160dk/nrf9160``                    |
|                   |                                    | | ``nrf9160dk/nrf9160/ns``                 |
+-------------------+------------------------------------+--------------------------------------------+
| RP2040            | |zephyr:board:rpi_pico|            | | ``rpi_pico``                             |
|                   |                                    | | ``rpi_pico/rp2040/w``                    |
+-------------------+------------------------------------+--------------------------------------------+
| STM32F303RE       | |zephyr:board:nucleo_f303re|       | ``nucleo_f303re``                          |
+-------------------+------------------------------------+--------------------------------------------+
| STM32F401RE       | |zephyr:board:nucleo_f401re|       | ``nucleo_f401re``                          |
+-------------------+------------------------------------+--------------------------------------------+
| STM32F413ZH       | |zephyr:board:nucleo_f413zh|       | ``nucleo_f413zh``                          |
+-------------------+------------------------------------+--------------------------------------------+
| STM32F746ZG       | |zephyr:board:nucleo_f746zg|       | ``nucleo_f746zg``                          |
+-------------------+------------------------------------+--------------------------------------------+
| STM32F767ZI       | |zephyr:board:nucleo_f767zi|       | ``nucleo_f767zi``                          |
+-------------------+------------------------------------+--------------------------------------------+
| STM32L496ZG       | |zephyr:board:nucleo_l496zg|       | ``nucleo_l496zg``                          |
+-------------------+------------------------------------+--------------------------------------------+


Boards included in tiac-bridle
==============================

The following boards are defined in the :file:`bridle/boards/` folder.
Also see the :ref:`boards` section in this documentation.

+-------------------+------------------------------------+----------------------------------+
| Hardware platform | Board name                         | Build target                     |
+===================+====================================+==================================+
| ATSAMD21G18A      | |bridle:board:arduino_zero|        | ``arduino_zero``                 |
|                   +------------------------------------+----------------------------------+
|                   | |bridle:board:xiao_samd21|         | ``xiao_samd21``                  |
|                   +------------------------------------+----------------------------------+
|                   | |bridle:board:seeeduino_cm0|       | ``seeeduino_cm0``                |
|                   +------------------------------------+----------------------------------+
|                   | |bridle:board:seeeduino_lotus|     | ``seeeduino_lotus``              |
+-------------------+------------------------------------+----------------------------------+
| RP2040            | |bridle:board:cytron_maker_rp2040| | | ``cytron_maker_nano_rp2040``   |
|                   |                                    | | ``cytron_maker_pi_rp2040``     |
|                   +------------------------------------+----------------------------------+
|                   | |bridle:board:picoboy|             | | ``picoboy/rp2040``             |
|                   |                                    | | ``picoboy/rp2040/color``       |
|                   +------------------------------------+----------------------------------+
|                   | |bridle:board:waveshare_rp2040|    | | ``waveshare_rp2040_one``       |
|                   |                                    | | ``waveshare_rp2040_zero``      |
|                   |                                    | | ``waveshare_rp2040_matrix``    |
|                   |                                    | | ``waveshare_rp2040_tiny``      |
|                   |                                    | | ``waveshare_rp2040_eth``       |
|                   |                                    | | ``waveshare_rp2040_lcd_0_96``  |
|                   |                                    | | ``waveshare_rp2040_plus``      |
|                   |                                    | | ``waveshare_rp2040_plus@16mb`` |
|                   |                                    | | ``waveshare_rp2040_geek``      |
+-------------------+------------------------------------+----------------------------------+
| STM32F777NI       | |bridle:board:magpie_f777ni|       | ``magpie_f777ni``                |
+-------------------+------------------------------------+----------------------------------+


Shield names
************

The following tables list all shields and build targets for |TIAC|
hardware platforms.

Shields included in tiac-bridle
===============================

The following shields are defined in the :file:`bridle/boards/shields/` folder.
Also see the :ref:`boards-shields` section in this documentation.

+------------------------------------------+-------------------------------------+----------------------------------------+
| Hardware platform                        | Shield name                         | Build target                           |
+==========================================+=====================================+========================================+
| Common for testing                       | :ref:`loopback_test_shield`         | | ``loopback_test``                    |
|                                          |                                     | | ``loopback_test_tmph``               |
+------------------------------------------+-------------------------------------+----------------------------------------+
| Common for (new) chip support            | :ref:`sc16is75x_bb_shield`          | | ``cjmcu_750_i2c``                    |
|                                          |                                     | | ``cjmcu_750_i2c_noirq``              |
| - NXP_ SC16IS750_                        |                                     | | ``cjmcu_750_spi``                    |
| - NXP_ SC16IS752_                        |                                     | | ``cjmcu_750_spi_noirq``              |
| - NXP_ SC18IS604_                        |                                     | | ``cjmcu_752_i2c``                    |
|                                          |                                     | | ``cjmcu_752_i2c_noirq``              |
|                                          |                                     | | ``cjmcu_752_spi``                    |
|                                          |                                     | | ``cjmcu_752_spi_noirq``              |
|                                          +-------------------------------------+----------------------------------------+
|                                          | :ref:`x_cjmcu_75x_shield`           | ``x_cjmcu_75x``                        |
|                                          +-------------------------------------+----------------------------------------+
|                                          | :ref:`nxp_sc18is604_evb_shield`     | ``nxp_sc18is604_evb``                  |
|                                          +-------------------------------------+----------------------------------------+
|                                          | :ref:`x_nxp_sc18is604_evb_shield`   | ``x_nxp_sc18is604_evb``                |
|                                          +-------------------------------------+----------------------------------------+
|                                          | :ref:`tcs_604_ard_shield`           | | ``tcs_604_ard``                      |
|                                          |                                     | | ``tcs_604_x_grove_testbed``          |
+------------------------------------------+-------------------------------------+----------------------------------------+
| :ref:`grove_shield`                      | :ref:`grove_base_shield_v2`         | ``seeed_grove_base_v2``                |
|                                          +-------------------------------------+----------------------------------------+
|                                          | :ref:`grove_base_shield_v1`         | ``seeed_grove_base_v1``                |
|                                          +-------------------------------------+----------------------------------------+
|                                          | :ref:`grove_base_shield_xiao_v1`    | ``seeed_grove_xiao_v1``                |
|                                          +-------------------------------------+----------------------------------------+
|                                          | :ref:`grove_rpipico_shield_v1`      | ``seeed_grove_rpipico_v1``             |
|                                          +-------------------------------------+----------------------------------------+
|                                          | :ref:`grove_button_shield`          | ``grove_btn_d[0…31]``                  |
|                                          +-------------------------------------+----------------------------------------+
|                                          | :ref:`grove_led_shield`             | ``grove_led_d[0…31]``                  |
|                                          +-------------------------------------+----------------------------------------+
|                                          | :ref:`grove_sensor_shield`          | | ``grove_sens_bme280``                |
|                                          |                                     | | ``grove_sens_bmp280``                |
|                                          |                                     | | ``grove_sens_dps310``                |
|                                          +-------------------------------------+----------------------------------------+
|                                          | :ref:`x_grove_testbed_shield`       | ``x_grove_testbed``                    |
+------------------------------------------+-------------------------------------+----------------------------------------+
| :ref:`rpi_pico_bb_shield`                | |GeeekPi Pico Breadboard Kit|       | ``geeekpi_pico_bb``                    |
|                                          +-------------------------------------+----------------------------------------+
|                                          | |GeeekPi Pico Breadboard Kit Plus|  | ``geeekpi_pico_bb_plus``               |
+------------------------------------------+-------------------------------------+----------------------------------------+
| :ref:`rpi_pico_clock_shield`             | |Waveshare Pico Clock Green|        | ``waveshare_pico_clock_green``         |
+------------------------------------------+-------------------------------------+----------------------------------------+
| :ref:`rpi_pico_lcd_shield`               | |PiMoroni Pico LCD 1.44|            | ``pimoroni_pico_lcd_1_44``             |
|                                          +-------------------------------------+----------------------------------------+
|                                          | |PiMoroni Pico LCD 2|               | ``pimoroni_pico_lcd_2``                |
|                                          +-------------------------------------+----------------------------------------+
|                                          | |Spotpear Pico LCD 1.54|            | ``spotpear_pico_lcd_1_54``             |
|                                          +-------------------------------------+----------------------------------------+
|                                          | |Waveshare Pico LCD 0.96|           | ``waveshare_pico_lcd_0_96``            |
|                                          +-------------------------------------+----------------------------------------+
|                                          | |Waveshare Pico LCD 1.14|           | ``waveshare_pico_lcd_1_14``            |
|                                          +-------------------------------------+----------------------------------------+
|                                          | |Waveshare Pico LCD 1.3|            | ``waveshare_pico_lcd_1_3``             |
|                                          +-------------------------------------+----------------------------------------+
|                                          | |Waveshare Pico LCD 1.44|           | ``waveshare_pico_lcd_1_44``            |
|                                          +-------------------------------------+----------------------------------------+
|                                          | |Waveshare Pico LCD 1.8|            | ``waveshare_pico_lcd_1_8``             |
|                                          +-------------------------------------+----------------------------------------+
|                                          | |Waveshare Pico LCD 2|              | ``waveshare_pico_lcd_2``               |
|                                          +-------------------------------------+----------------------------------------+
|                                          | |Waveshare Pico ResTouch LCD 2.8|   | ``waveshare_pico_restouch_lcd_2_8``    |
|                                          +-------------------------------------+----------------------------------------+
|                                          | |Waveshare Pico ResTouch LCD 3.5|   | ``waveshare_pico_restouch_lcd_3_5``    |
+------------------------------------------+-------------------------------------+----------------------------------------+
| :ref:`rpi_pico_led_shield`               | |Waveshare Pico RGB LED|            | ``waveshare_pico_rgb_led``             |
+------------------------------------------+-------------------------------------+----------------------------------------+
| :ref:`rpi_pico_test_shield`              | |Spotpear Pico ALL GPIO TEST|       | ``spotpear_pico_test``                 |
+------------------------------------------+-------------------------------------+----------------------------------------+
| :ref:`waveshare_lcd_modules`             | |Waveshare 2.4 LCD|                 | ``waveshare_2_4_lcd``                  |
+------------------------------------------+-------------------------------------+----------------------------------------+
| :ref:`waveshare_pico_10dof_imu_sensor`   | |Waveshare Pico 10-DOF IMU Sensor|  | ``waveshare_pico_10dof_imu_sensor_r2`` |
|                                          |                                     +----------------------------------------+
|                                          |                                     | ``waveshare_pico_10dof_imu_sensor_r1`` |
+------------------------------------------+-------------------------------------+----------------------------------------+
| :ref:`waveshare_pico_environment_sensor` | |Waveshare Pico Environment Sensor| | ``waveshare_pico_environment_sensor``  |
+------------------------------------------+-------------------------------------+----------------------------------------+


Snippet names
*************

The following tables list all snippets and build targets for |TIAC|
hardware platforms.

Snippets included in tiac-bridle
================================

The following snippets are defined in the :file:`bridle/snippets/` folder.
Also see the :ref:`snippets` section in this documentation.

+---------------------+---------------------------------------------+----------------------------------+
| Hardware platform   | Snippet name                                | Build target                     |
+=====================+=============================================+==================================+
| Common for usage    | :ref:`snippet-del-default-aliases`          | ``del-default-aliases``          |
+---------------------+---------------------------------------------+----------------------------------+
| Common for usage    | :ref:`snippet-usb-console`                  | ``usb-console``                  |
+---------------------+---------------------------------------------+----------------------------------+
| Common for usage    | :ref:`snippet-pwm-servo`                    | ``pwm-servo``                    |
+---------------------+---------------------------------------------+----------------------------------+
| Common for testing  | :ref:`snippet-can-timing-adj`               | ``can-timing-adj``               |
+---------------------+---------------------------------------------+----------------------------------+
| Common for testing  | :ref:`snippet-wdt-timing-adj`               | ``wdt-timing-adj``               |
+---------------------+---------------------------------------------+----------------------------------+
| Common for testing  | :ref:`snippet-tstdrv-bldall-display-adj`    | ``tstdrv-bldall-display-adj``    |
+---------------------+---------------------------------------------+----------------------------------+
| Common for testing  | :ref:`snippet-tstdrv-bldall-gpio-adj`       | ``tstdrv-bldall-gpio-adj``       |
+---------------------+---------------------------------------------+----------------------------------+
| Common for testing  | :ref:`snippet-tstdrv-bldall-i2c-adj`        | ``tstdrv-bldall-i2c-adj``        |
+---------------------+---------------------------------------------+----------------------------------+
| Common for testing  | :ref:`snippet-tstdrv-bldall-mfd-adj`        | ``tstdrv-bldall-mfd-adj``        |
+---------------------+---------------------------------------------+----------------------------------+
| Common for testing  | :ref:`snippet-tstdrv-bldall-rtc-adj`        | ``tstdrv-bldall-rtc-adj``        |
+---------------------+---------------------------------------------+----------------------------------+
| Common for testing  | :ref:`snippet-tstdrv-bldall-sensor-adj`     | ``tstdrv-bldall-sensor-adj``     |
+---------------------+---------------------------------------------+----------------------------------+
| Common for testing  | :ref:`snippet-tstdrv-bldall-uart-adj`       | ``tstdrv-bldall-uart-adj``       |
+---------------------+---------------------------------------------+----------------------------------+
| Tweak for setups    | :ref:`snippet-samples-sensor-bme280-tweaks` | ``samples-sensor-bme280-tweaks`` |
+---------------------+---------------------------------------------+----------------------------------+


Custom boards and shields
*************************

Defining your own board or shield is a very common step in application
development, since applications are typically designed to run on boards
that are not directly supported by |ZEPHYR| or |BRIDLE|, given that they
are typically custom designs and not available publicly. To define your
own board or shield, you can use the following |ZEPHYR| guides as reference,
since boards are defined in |BRIDLE| just as they are in the |ZEPHYR|:

* :zephyr:ref:`custom_board_definition`
  is a guide to adding your own custom board to the Zephyr build system.
* :zephyr:ref:`shields`
  is a complete guide to integrate your own modules as shields.
* :zephyr:ref:`board_porting_guide`
  is a complete guide to porting Zephyr to your own board.
* :zephyr:ref:`soc_porting_guide`
  is a complete guide to porting Zephyr to your own SoC.
* :zephyr:ref:`architecture_porting_guide`
  is a complete guide to porting Zephyr to your own architecture.
