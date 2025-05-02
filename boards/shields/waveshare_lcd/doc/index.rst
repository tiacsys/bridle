.. _waveshare_lcd_modules:

Waveshare LCD Modules
#####################

Overview
********

The Waveshare LCD modules are available in different sizes and resolutions.
Nearly all displays comes with a special LCD controller wired over SPI up to
the board by free wiring.

Supported Modules
*****************

Hardware
========

.. tabs::

   .. group-tab:: Waveshare 2.4 LCD

      .. _waveshare_2_4_lcd:

      .. include:: waveshare_2_4_lcd/hardware.rsti

Positions
=========

.. tabs::

   .. group-tab:: Waveshare 2.4 LCD

      .. include:: waveshare_2_4_lcd/positions.rsti

Pinouts
=======

.. tabs::

   .. group-tab:: Waveshare 2.4 LCD

      .. include:: waveshare_2_4_lcd/pinouts.rsti

Requirements
************

This shields can be used with any board which provides a configuration
either for Arduino or Arduino Nano connectors or for a special connector
set and defines node aliases for SPI and GPIO interfaces (see
:external+zephyr:ref:`shields` for more details).

Pin Assignments
===============

.. tabs::

   .. group-tab:: Waveshare 2.4 LCD

      .. include:: waveshare_2_4_lcd/wiring.rsti

Utilization
***********

This shields can be used with any development board, shield, or snippet that
provides a Devicetree node with either the :dtcompatible:`arduino-nano-header-r3`
or the :dtcompatible:`seeed,grove-laced-if` property for the compatibility.
In particular, the :dts:`&arduino_nano_spi` or :dts:`&grove_spi` bus and some
GPIO signals of :dts:`&arduino_nano_header` or :dts:`&grove_gpio` must be free
for communication with the LCD on the modules. On Devicetree level, the shields
also providing the special node label :dts:`&board_spi_lcd` for this purpose.

Programming
===========

.. tabs::

   .. group-tab:: Waveshare 2.4 LCD

      .. include:: waveshare_2_4_lcd/programming.rsti

References
**********

.. target-notes::
