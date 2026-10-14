.. _spotpear_pico_test:

Spotpear Pico ALL GPIO TEST
###########################

Overview
********

The `Spotpear Pico ALL GPIO TEST`_ shield is one of the simplest boards for
testing all I/O signal lines of a Raspberry Pi Pico by GPIO or PWM functions.
There is also one additional ADC channel for testing purposes directly
connected to a simple high-resistance potentiometer.

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

Prints all input events as defined by the shield's Devicetree. See also Zephyr
sample: :external+zephyr:zephyr:code-sample:`input-dump`.

.. include:: input_dump.rsti

Analog-to-Digital Converter (ADC)
=================================

Read analog inputs from ADC channels as defined by the shield's Devicetree.
See also Zephyr sample: :external+zephyr:zephyr:code-sample:`adc_dt`.

.. include:: adc_dt.rsti

Light-Emitting Diode (LED) by PWM
=================================

Control PWM LEDs as defined by the shield's Devicetree. See also Zephyr
sample: :external+zephyr:zephyr:code-sample:`led-pwm`.

.. include:: led_pwm.rsti

References
**********

.. target-notes::
