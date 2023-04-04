.. _memc-sram-sample:

MEMC Driver SRAM Sample
#######################

Overview
********

This sample can be used with any memory controller driver that memory maps
external RAM. It is intended to demonstrate the ability to read and write
from the memory mapped region.

Note that the chosen region (set by ``sram-ext`` dt alias node) should not
overlap with memory used for XIP or SRAM by the application, as the sample
would overwrite this data


Building and Running
********************

This application can be built and executed on an
:ref:`STM32F7308-DK <stm32f7308_dk_board>` as follows:

.. zephyr-app-commands::
   :zephyr-app: bridle/samples/memc-sram-ext
   :host-os: unix
   :board: stm32f7308_dk
   :goals: build flash
   :compact:

To build for another board, change ``stm32f7308_dk`` above to
that other board's name.

Sample Output
=============

.. code-block:: console

   *** Booting Zephyr OS build zephyr-vX.Y.Y ***
   Writing to memory region with base 0x60000000, size 0x80000

   First 1024B of data in memory:

   00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f
   10 11 12 13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f
   20 21 22 23 24 25 26 27 28 29 2a 2b 2c 2d 2e 2f
   ....
   f0 f1 f2 f3 f4 f5 f6 f7 f8 f9 fa fb fc fd fe ff


   Read data matches written data.
