.. _waveshare_lcd_modules:

Waveshare LCD Modules
#####################

The Waveshare LCD modules are available in different sizes and resolutions.
Nearly all displays comes with a special LCD controller wired over SPI up to
the board by free wiring.

.. toctree::
   :caption: Supported Shields
   :maxdepth: 1
   :glob:

   **/index

Utilization
***********

This shields can be used with any development board, shield, or snippet that
provides a Devicetree node with either the :dtcompatible:`arduino-nano-header-r3`
or the :dtcompatible:`seeed,grove-laced-if` property for the compatibility.
In particular, the :dts:`&arduino_nano_spi` or :dts:`&grove_spi` bus and some
GPIO signals of :dts:`&arduino_nano_header` or :dts:`&grove_gpio` must be free
for communication with the LCD on the modules. On Devicetree level, the shields
also providing the special node label :dts:`&board_spi_lcd` for this purpose.
