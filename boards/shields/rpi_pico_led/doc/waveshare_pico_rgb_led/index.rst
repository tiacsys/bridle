.. _waveshare_pico_rgb_led:

Waveshare Pico RGB LED
######################

Overview
********

The `Waveshare Pico RGB LED`_ is an LED matrix module designed for
|zephyr:board:rpi_pico|, which has 16 × RGB × 10 (160) full-color external
controlled constant current integrated LEDs, with embedded quality controller
IC and LED chip. It is a :bbl:`pico sized` clean-looking front panel.

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

LED Blinky and Button
=====================

.. include:: led_button.rsti

Hello Shell on the USB Console (CDC/ACM)
========================================

.. include:: helloshell.rsti

More Samples
************

LED strip test pattern
======================

Drives an RGB LED strip that must defined by the shields Devicetree.
See also Zephyr sample: :external+zephyr:zephyr:code-sample:`led-strip`.

.. include:: ledstrip_test.rsti

LED Display Orientation and Bit Order Test
==========================================

Draw some basic rectangles onto the display. The rectangle colors and positions
are chosen so that you can check the orientation of the LED display and correct
RGB bit order.
See also Zephyr sample: :external+zephyr:zephyr:code-sample:`display`.

.. include:: display_test.rsti

References
**********

.. target-notes::
