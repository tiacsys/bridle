.. _stm32f7308_dk_qspi_flash-sample:

External QSPI NOR Flash
#######################

Overview
********

See :doc:`zephyr:samples/drivers/spi_flash/README` for the original description.

.. _stm32f7308_dk_qspi_flash-sample-requirements:

Requirements
************

The STM32F7308-DK discovery kit have one 512-Mbit serial NOR Flash chip
connected to the STM32 Quad-SPI (QSPI).

Building and Running
********************

Build and flash testing sample as follows:

.. zephyr-app-commands::
   :app: zephyr/samples/drivers/spi_flash
   :build-dir: qspi_flash-stm32f7308_dk
   :board: stm32f7308_dk
   :goals: build flash
   :west-args: -p always
   :host-os: unix

After flashing, the output to the console will look something like this:

.. code-block:: none

   qspi-nor-flash@0 SPI flash testing
   ==================================

   Perform test on single sector
   Test 1: Flash erase
   Flash erase succeeded!

   Test 2: Flash write
   Attempting to write 4 bytes
   Data read matches data written. Good!!
