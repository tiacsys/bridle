.. _mimxrt1010_evk-extensions:

NXP MIMXRT1010-EVK
##################

Overview
********

This is a set of Bridle's extension to the original Zephyr upstream board
:ref:`zephyr:mimxrt1010_evk` with some adaptions and improvement on
Devicetree level.

List of extensions
******************

- overwrite the Arduino UNO R3 specific edge connecor binding:

  - :devicetree:`&arduino_header {...};`

- extend with a :dtcompatible:`fixed-partitions` table for the on-board
  16㎆ QuadSPI NOR Flash declared as :devicetree:`&at25sf128a`
- add a :dtcompatible:`zephyr,flash-disk` node linked to the
  :devicetree:`partition = <&storage_partition>;` with the hard defined
  mass storage disk name :devicetree:`disk-name = "NAND";` – also set
  the mass storage disk name hard on Kconfig level by a new board config
  file with :kconfig:option:`CONFIG_MASS_STORAGE_DISK_NAME`

.. note::

   On :ref:`zephyr:mimxrt1010_evk` pin D4 (GPIO), D5 (GPIO/PWM), and
   D9 (GPIO/PWM) are disconnected in default and can be closed optionally.
   With this GPIO map overwrites the resistors R793, R795 and R800 must be
   fitted for proper use. But keep in mind that the signals are already
   connected to other on-board header for the NXP special motor driver
   add-on bard.
