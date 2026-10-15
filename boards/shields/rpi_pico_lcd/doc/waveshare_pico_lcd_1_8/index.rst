.. _waveshare_pico_lcd_1_8:

Waveshare Pico LCD 1.8
######################

Overview
********

The `Waveshare Pico LCD 1.8`_ shield comes with the built-in controller
ST7735S_ inside the LCD, which is an LCD controller with 162 × RGB × 132
pixels, while the pixels of this **1.8-inch** LCD itself is 128 (H) RGB ×
160 (V). There are two types of horizontal and vertical screens, so the
internal RAM of the LCD is not fully used. The LCD supports 12-bit, 16-bit,
and 18-bit input color formats per pixel, namely RGB444, RGB565, and RGB666
three color formats. This integration **uses the RGB565** color format,
which is also a commonly used RGB format. The LCD uses a four-wire SPI
communication interface.

Hardware
========

.. include:: hardware.rsti

Positions
=========

.. include:: positions.rsti

Pinouts
=======

.. include:: pinouts.rsti

Basic Samples
*************

Hello Shell on the USB Console (CDC/ACM)
========================================

.. include:: helloshell.rsti

More Samples
************

Input dump
==========

Prints all input events as defined by the shields Devicetree. See also Zephyr
sample: :external+zephyr:zephyr:code-sample:`input-dump`.

.. hint::

   The |Waveshare Pico LCD 1.8| doesn't provide any input
   components. This sample is not applicable.

Sounds from the speaker
=======================

Drives an buzzer or speaker that must defined by the shields Devicetree.
See also Bridle sample: :ref:`buzzer-sample`.

.. hint::

   The |Waveshare Pico LCD 1.8| doesn't provide an buzzer or speaker.
   This sample is not applicable.

LED color change
================

Drives an RGB LED that must defined by the shields Devicetree. See also Zephyr
sample: :external+zephyr:zephyr:code-sample:`rgb-led`.

.. hint::

   The |Waveshare Pico LCD 1.8| doesn't provide a RGB LED.
   This samples are not applicable.

LED strip test pattern
======================

Drives an RGB LED strip that must defined by the shields Devicetree.
See also Zephyr sample: :external+zephyr:zephyr:code-sample:`led-strip`.

.. hint::

   The |Waveshare Pico LCD 1.8| doesn't provide a RGB LED strip.
   This sample is not applicable.

LCD Orientation and Bit Order Test
==================================

Draw some basic rectangles onto the display. The rectangle colors and positions
are chosen so that you can check the orientation of the LCD and correct RGB bit
order. See also Zephyr sample: :external+zephyr:zephyr:code-sample:`display`.

.. include:: display_test.rsti

Draw touch events on LCD
========================

Draw a small plus in the last touched coordinates. In this way, parameters such
as inverted/swapped axes can be examined. See also Zephyr sample:
:external+zephyr:zephyr:code-sample:`draw_touch_events`.

.. hint::

   The |Waveshare Pico LCD 1.8| doesn't provide a touchscreen panel.
   This sample is not applicable.

LVGL Basic Sample
=================

Displays “Hello World!” in the center of the screen and a counter at the bottom
which increments every second. See also Zephyr sample:
:external+zephyr:zephyr:code-sample:`lvgl`.

.. include:: lvgl_basic.rsti

TF/microSD Demonstration
========================

This samples and test applications aren't applicable on all boards. They will
be built with activated USB-CDC/ACM console.

.. hint::

   The |Waveshare Pico LCD 1.8| doesn't provide a TF/microSD card slot.
   This samples are not applicable.

References
**********

.. target-notes::
