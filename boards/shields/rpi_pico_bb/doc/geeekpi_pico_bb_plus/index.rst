.. _geeekpi_pico_bb_plus:

GeeekPi Pico Breadboard Kit Plus (EP-0172)
##########################################

Overview
********

The `GeeekPi Pico Breadboard Kit Plus (EP-0172)`_ shield comes with the built-in
controller `ST7796S <ST7796U_>`_ inside the LCD, which is an LCD controller
with 320 × RGB × 480 pixels, while the pixels of this **3.5-inch** LCD itself
is 320 (H) RGB × 480 (V). There are two types of horizontal and vertical
screens, so the internal RAM of the LCD is not fully used. The LCD supports
16-bit, 18-bit, and 24-bit input color formats per pixel, namely RGB565,
RGB666, and RGB888 three color formats. This integration **uses the RGB565**
color format, which is also a commonly used RGB format. The LCD uses a
four-wire SPI communication interface.

Additional there is a capasitive Touch Screen (TS) with the 5-point TS
controller GT911_ and a standard RGB LED WS2812B_.

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

.. include:: input_dump.rsti

Sounds from the speaker
=======================

Drives an buzzer or speaker that must defined by the shields Devicetree.
See also Bridle sample: :ref:`buzzer-sample`.

.. include:: buzzer.rsti

LED color change
================

Drives an RGB LED that must defined by the shields Devicetree. See also Zephyr
sample: :external+zephyr:zephyr:code-sample:`rgb-led`.

.. hint::

   The |GeeekPi Pico Breadboard Kit Plus| doesn't provide a TriColor ChipLED.
   This sample is not applicable.

LED strip test pattern
======================

Drives an RGB LED strip that must defined by the shields Devicetree.
See also Zephyr sample: :external+zephyr:zephyr:code-sample:`led-strip`.

.. include:: ledstrip_test.rsti

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

.. include:: touch_test.rsti

LVGL Basic Sample
=================

Displays “Hello World!” in the center of the screen and a counter at the bottom
which increments every second. See also Zephyr sample:
:external+zephyr:zephyr:code-sample:`lvgl`.

.. include:: lvgl_basic.rsti

LVGL Widgets Demo
=================

Shows how the widgets look like out of the box using the built-in material
theme. See also Zephyr sample: :external+zephyr:zephyr:code-sample:`lvgl-demos`.

.. include:: lvgl_demo.rsti

TF/microSD Demonstration
========================

This samples and test applications aren't applicable on all boards. They will
be built with activated USB-CDC/ACM console.

.. hint::

   The |GeeekPi Pico Breadboard Kit Plus| doesn't provide a TF/microSD card slot.
   This sample is not applicable.

References
**********

.. target-notes::
