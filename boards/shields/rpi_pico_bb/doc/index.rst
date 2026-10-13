.. _rpi_pico_bb_shield:

Raspberry Pi Pico Breadboard Shields
####################################

This is a collection of different shields with a breadboard area specifically
designed for use with a Raspberry Pi Pico (W) for rapid prototyping. Ranging
from very simple setups, just to reach the individual signals, to providing
already more complex components such as digital inputs and outputs (buttons,
LEDs or buzzer), joysticks (digital or analog), displays with or without
touchscreen, multi-color (RGB) LEDs, or TF/SD card slots.

.. toctree::
   :caption: Supported Shields
   :maxdepth: 1
   :glob:

   **/index

Utilization
***********

This shields can be used with any development board, shield, or snippet that
provides a Devicetree node with the :dtcompatible:`raspberrypi,pico-header-r3`
property for the compatibility. In particular, one SPI bus and some GPIO
signals on this edge connector must be free for communication with the
components on the breadboard shields. The shields also provide the special
Devicetree labels :dts:`&rpipico_spi_lcd` and :dts:`&lcd_panel` for the special
purpose of a on-shield LCD.

For shields with touchscreen support, additional GPIO signals and one I2C bus
on the edge connector must also be free for communication with the touchscreen
controller on the shield. Then the shields also provide the special Devicetree
labels :dts:`&rpipico_spi_tsc` and :dts:`&tsc_panel` for this purpose.

For shields with TF/microSD card slot, even more GPIO signals on the edge
connector must be free for communication with the card on the shield over
SDHC/SPI. Then the shields also provide the special Devicetree labels
:dts:`&rpipico_spi_sdc` and :dts:`&sdhc_spi` for this purpose. In case of
the SDHC/SDIO mode up to seven additional GPIO signals must be free for
communication with the card over a 4-bit SDHC/SDIO interface. But this is
not yet supported and may need changes on the shield hardware.
