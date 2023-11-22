.. _mimxrt1060_evk-extensions:

NXP MIMXRT1060-EVK
##################

Overview
********

This is a set of Bridle's extension to the original Zephyr upstream board
:ref:`zephyr:mimxrt1060_evk` with some adaptions and improvement on
Devicetree level.

List of extensions
******************

- add a :dtcompatible:`zephyr,flash-disk` node linked to the
  :devicetree:`partition = <&storage_partition>;` with the hard defined
  mass storage disk name :devicetree:`disk-name = "NAND";` – also set
  the mass storage disk name hard on Kconfig level by a new board config
  file with :kconfig:option:`CONFIG_MASS_STORAGE_DISK_NAME`
