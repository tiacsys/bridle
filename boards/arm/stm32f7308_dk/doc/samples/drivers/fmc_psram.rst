.. _stm32f7308_dk_fmc_psram-sample:

External FMC PSRAM
##################

Overview
********

See :ref:`memc-sram-sample` for the original description.

.. _stm32f7308_dk_fmc_psram-sample-requirements:

Requirements
************

The STM32F7308-DK discovery kit have one 8-Mbit PSRAM/CRAM chip connected
to the STM32 Flexible Memory Controller (FMC) whereby only 4-Mbit of memory
will be accessible.

Building and Running
********************

Build and flash testing sample as follows:

.. zephyr-app-commands::
   :app: bridle/samples/memc-sram-ext
   :build-dir: fmc_psram-stm32f7308_dk
   :board: stm32f7308_dk
   :goals: build flash
   :west-args: -p always
   :host-os: unix

After flashing, the output to the console will look something like this:

.. code-block:: none

   Writing to memory region with base 0x60000000, size 0x80000

   ::::::::::::::::::::::::::::::::
   ::::::::::::::::::::::::::::::::
   ::::::::::::::::::::::::::::::::
   ::::::::::::::::::::::::::::::::
   ::::::::::::::::::::::::::::::::
   ::::::::::::::::::::::::::::::::
   ::::::::::::::::::::::::::::::::
   ::::::::::::::::::::::::::::::::
   ::::::::::::::::::::::::::::::::
   ::::::::::::::::::::::::::::::::
   ::::::::::::::::::::::::::::::::
   ::::::::::::::::::::::::::::::::
   ::::::::::::::::::::::::::::::::
   ::::::::::::::::::::::::::::::::
   ::::::::::::::::::::::::::::::::
   ::::::::::::::::::::::::::::::::


   First 1024B of data in memory:

   00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f
   10 11 12 13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f
   20 21 22 23 24 25 26 27 28 29 2a 2b 2c 2d 2e 2f
   ....
   f0 f1 f2 f3 f4 f5 f6 f7 f8 f9 fa fb fc fd fe ff


   Read data matches written data.
