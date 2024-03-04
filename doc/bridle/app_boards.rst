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

The following boards are defined in the :file:`zephyr/boards/arm/` folder.
Also see the :ref:`zephyr:boards` section in the Zephyr documentation.

.. _table:

+-------------------+---------------------------------------+------------------------+
| Hardware platform | Board name                            | Build target           |
+===================+=======================================+========================+
| Native            | :ref:`zephyr:native_posix`            | ``native_posix``       |
+-------------------+---------------------------------------+------------------------+
| Emulator          | :ref:`zephyr:qemu_x86`                | ``qemu_x86``           |
|                   +---------------------------------------+------------------------+
|                   | :ref:`zephyr:qemu_cortex_m3`          | ``qemu_cortex_m3``     |
+-------------------+---------------------------------------+------------------------+
| ATSAMD21G18A      | :ref:`zephyr:arduino_zero`            | ``arduino_zero``       |
|                   +---------------------------------------+------------------------+
|                   | :ref:`zephyr:seeeduino_xiao`          | ``seeeduino_xiao``     |
+-------------------+---------------------------------------+------------------------+
| STM32F746ZG       | :ref:`zephyr:nucleo_f746zg_board`     | ``nucleo_f746zg``      |
+-------------------+---------------------------------------+------------------------+


Boards included in tiac-bridle
==============================

The following boards are defined in the :file:`bridle/boards/arm/` folder.
Also see the :ref:`boards` section in this documentation.

+-------------------+---------------------------------------+----------------------------------+
| Hardware platform | Board name                            | Build target                     |
+===================+=======================================+==================================+
| ATSAMD21G18A      | :ref:`arduino_zero`                   | ``arduino_zero``                 |
|                   +---------------------------------------+----------------------------------+
|                   | :ref:`seeed_xiao_samd21`              | ``seeed_xiao_samd21``            |
|                   +---------------------------------------+----------------------------------+
|                   | :ref:`seeeduino_cm0`                  | ``seeeduino_cm0``                |
|                   +---------------------------------------+----------------------------------+
|                   | :ref:`seeeduino_lotus`                | ``seeeduino_lotus``              |
+-------------------+---------------------------------------+----------------------------------+
| RP2040            | :ref:`waveshare_rp2040`               | | ``waveshare_rp2040_one``       |
|                   |                                       | | ``waveshare_rp2040_zero``      |
|                   |                                       | | ``waveshare_rp2040_matrix``    |
|                   |                                       | | ``waveshare_rp2040_tiny``      |
|                   |                                       | | ``waveshare_rp2040_eth``       |
|                   |                                       | | ``waveshare_rp2040_lcd_0_96``  |
|                   |                                       | | ``waveshare_rp2040_plus``      |
|                   |                                       | | ``waveshare_rp2040_plus@16mb`` |
|                   |                                       | | ``waveshare_rp2040_geek``      |
+-------------------+---------------------------------------+----------------------------------+
| STM32F777NI       | :ref:`tiac_magpie_board`              | ``tiac_magpie``                  |
+-------------------+---------------------------------------+----------------------------------+


Shields included in tiac-bridle
===============================

The following shields are defined in the :file:`bridle/boards/shields/` folder.

+---------------------+----------------------------------+-----------------------------+
| Hardware platform   | Shield name                      | Build target                |
+=====================+==================================+=============================+
| Common for testing  | :ref:`loopback_test_shield`      | | ``loopback_test``         |
|                     |                                  | | ``loopback_test_tmph``    |
+---------------------+----------------------------------+-----------------------------+
| :ref:`grove_shield` | :ref:`grove_base_shield_v2`      | ``seeed_grove_base_v2``     |
|                     +----------------------------------+-----------------------------+
|                     | :ref:`grove_base_shield_v1`      | ``seeed_grove_base_v1``     |
|                     +----------------------------------+-----------------------------+
|                     | :ref:`grove_base_shield_xiao_v1` | ``seeed_grove_xiao_v1``     |
|                     +----------------------------------+-----------------------------+
|                     | :ref:`grove_rpipico_shield_v1`   | ``seeed_grove_rpipico_v1``  |
|                     +----------------------------------+-----------------------------+
|                     | :ref:`grove_button_shield`       | ``grove_btn_d[0…31]``       |
|                     +----------------------------------+-----------------------------+
|                     | :ref:`grove_led_shield`          | ``grove_led_d[0…31]``       |
|                     +----------------------------------+-----------------------------+
|                     | :ref:`x_grove_testbed_shield`    | ``x_grove_testbed``         |
+---------------------+----------------------------------+-----------------------------+


Snippets included in tiac-bridle
================================

The following snippets are defined in the :file:`bridle/snippets/` folder.
Also see the :ref:`snippets` section in this documentation.

+---------------------+----------------------------------+-----------------------------+
| Hardware platform   | Snippet name                     | Build target                |
+=====================+==================================+=============================+
| Common for usage    | :ref:`snippet-usb-console`       | ``usb-console``             |
+---------------------+----------------------------------+-----------------------------+
| Common for testing  | :ref:`snippet-can-timing-adj`    | ``can-timing-adj``          |
+---------------------+----------------------------------+-----------------------------+


Custom boards
*************

Defining your own board is a very common step in application development,
since applications are typically designed to run on boards that are not
directly supported by |BRIDLE|, given that they are typically custom
designs and not available publicly. To define your own board, you can
use the following Zephyr guides as reference, since boards are defined
in the |BRIDLE| just as they are in Zephyr:

* :ref:`zephyr:custom_board_definition`
  is a guide to adding your own custom board to the Zephyr build system.
* :ref:`zephyr:board_porting_guide`
  is a complete guide to porting Zephyr to your own board.
