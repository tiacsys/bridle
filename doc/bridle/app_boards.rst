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
| NUCLEO-F746ZG     | :ref:`zephyr:nucleo_f746zg_board`     | ``native_posix``       |
+-------------------+---------------------------------------+------------------------+


Boards included in tiac-bridle
==============================

The following boards are defined in the :file:`bridle/boards/arm/` folder.
Also see the :ref:`boards` section in this documentation.

+-------------------+---------------------------------------+------------------------+
| Hardware platform | Board name                            | Build target           |
+===================+=======================================+========================+
| STM32F777         | :ref:`tiac_magpie_board`              | ``tiac_magpie``        |
+-------------------+---------------------------------------+------------------------+


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
