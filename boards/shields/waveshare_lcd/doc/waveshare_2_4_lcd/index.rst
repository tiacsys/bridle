.. _waveshare_2_4_lcd:

Waveshare 2.4 LCD Module
########################

Overview
********

The `Waveshare 2.4 LCD Module`_ with a resolution of 240 × RGB × 320 pixels,
is based on the built-in controller `ILI9341 <ILI9341V_>`_ inside the
**2.4-inch** LCD. The LCD supports 6-bit, 16-bit, and 18-bit input color
formats per pixel, namely RGB222, RGB565, and RGB666 three color formats.
This integration **uses the RGB565** color format, which is also a commonly
used RGB format. The LCD uses a four-wire SPI communication interface.

Hardware
========

.. include:: hardware.rsti

Positions
=========

.. include:: positions.rsti

Pinouts
=======

.. include:: pinouts.rsti

Requirements
************

This shields can be used with any board which provides a configuration
either for Arduino or Arduino Nano connectors or for a special connector
set and defines node aliases for SPI and GPIO interfaces (see
:external+zephyr:ref:`shields` for more details).

Pin Assignments
===============

.. include:: wiring.rsti

Samples
*******

LCD Orientation and Bit Order Test
==================================

Draw some basic rectangles onto the display. The rectangle colors and positions
are chosen so that you can check the orientation of the LCD and correct RGB bit
order. See also Zephyr sample: :external+zephyr:zephyr:code-sample:`display`.

.. include:: display_test.rsti

LVGL Basic Sample
=================

Displays “Hello World!” in the center of the screen and a counter at the bottom
which increments every second. See also Zephyr sample:
:external+zephyr:zephyr:code-sample:`lvgl`.

.. include:: lvgl_basic.rsti

References
**********

.. target-notes::
