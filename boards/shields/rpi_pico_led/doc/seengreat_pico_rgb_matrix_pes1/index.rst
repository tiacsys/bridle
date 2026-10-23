.. _seengreat_pico_rgb_matrix_pes1:

SeenGreat Pico RGB Matrix Panel Expansion S1
############################################

Overview
********

The `SeenGreat Pico RGB Matrix Panel Expansion S1`_ is an LED matrix module
designed for |zephyr:board:rpi_pico|, which has 20 × RGB × 10 (200) full-color
external controlled constant current integrated LEDs, with embedded quality
controller IC and LED chip. It is a :bbl:`pico sized` clean-looking front
panel. Furthermore it provides an DS1302 real-time clock chip, an analog
silicon microphone audio sampling circuit, a light-dependent resistor, and a
reset button.

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

Analog-to-Digital Converter (ADC)
=================================

Read analog inputs from ADC channels as defined by the shield's Devicetree.
See also Zephyr sample: :external+zephyr:zephyr:code-sample:`adc_dt`.

.. include:: adc_dt.rsti

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
