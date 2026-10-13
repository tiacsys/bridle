.. _waveshare_pico_clock_green:

Waveshare Pico Clock Green
##########################

Overview
********

The `Waveshare Pico Clock Green`_ is a :bbk:`special sized` LED-digit
electronic clock designed for |zephyr:board:rpi_pico|, a RP2040 based
development board. It contains a high-precision RTC chip DS3231_ with
an on-chip temperature sensor for ambient, auto-brightness adjustment
by an photoresistor (LDR), alarm signaling by a simple buzzer. a LED
matrix with 8 × 1-bit × 24 pixel for special signing lights and data
display and buttons for navigation and configuration.

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

Input dump
==========

Prints all input events as defined by the shields Devicetree. See also Zephyr
sample: :external+zephyr:zephyr:code-sample:`input-dump`.

.. include:: input_dump.rsti

Analog-to-Digital Converter (ADC)
=================================

Read analog inputs from ADC channels as defined by the shield's Devicetree.
See also Zephyr sample: :external+zephyr:zephyr:code-sample:`adc_dt`.

.. include:: adc_dt.rsti

Sounds from the speaker
=======================

Drives an buzzer or speaker that must defined by the shields Devicetree.
See also Bridle sample: :ref:`buzzer-sample`.

.. include:: buzzer.rsti

LED Panel Orientation and Bit Order Test
========================================

Draw some basic rectangles onto the LED panel. The rectangle positions
are chosen so that you can check the orientation of the LED panel and
correct bit order.
See also Zephyr sample: :external+zephyr:zephyr:code-sample:`display`.

.. include:: display_test.rsti

References
**********

API
===

   .. doxygengroup:: mdf_interface_sipomuxgp
      :project: bridle

   .. doxygengroup:: io_gpio_sipomux
      :project: bridle

   .. doxygengroup:: io_display_sipomux
      :project: bridle

Links
=====

.. target-notes::
