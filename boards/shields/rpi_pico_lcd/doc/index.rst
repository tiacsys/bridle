.. _rpi_pico_lcd_shield:

Raspberry Pi Pico LCD Shields
#############################

This is a collection of very versatile displays due to its different resolutions
and sizes, the RGB capabilities and additional buttons and joystick. Nearly all
displays comes with a special LCD controller wired over SPI up to the Raspberry
Pi Pico. Additional momentary push buttons or joysticks are wired up over simple
GPIO lines. Some shield provide also a TF/SD-card slot, wired over a second
dedicated SPI bus.

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
signals on this edge connector must be free for communication with the LCD
on the shields. The shields also provide the special Devicetree labels
:dts:`&rpipico_spi_lcd` and :dts:`&lcd_panel` for this purpose.

For shields with touchscreen support, additional GPIO signals and on occasion
one I2C bus on the edge connector must also be free for communication with the
touchscreen controller on the shield. Then the shields also provide the special
Devicetree labels :dts:`&rpipico_spi_tsc` and :dts:`&tsc_panel`
for this purpose.

For shields with TF/microSD card slot, even more GPIO signals on the edge
connector must be free for communication with the card on the shield over
SDHC/SPI. The shields also provide the special Devicetree labels
:dts:`&rpipico_spi_sdc` and :dts:`&sdhc_spi` for this purpose.
In case of the SDHC/SDIO mode up to seven additional GPIO signals must be
free for communication with the card over a 4-bit SDHC/SDIO interface.
But this is not yet supported and may need changes on the shield hardware.
