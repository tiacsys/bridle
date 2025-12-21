.. _rpi_pico_test_shield:

Raspberry Pi Pico TEST Shields
##############################

This simple shields are well suited for teaching and training to learn how to
access GPIO, PWM or ADC signals and how to use the associated Zephyr APIs. As a
demo board you can test if all pins of the Pico are in good condition. As an
expansion board, this module contains LEDs, buttons, and a basic ADC function to
get you started. It is a simple expansion board for Raspberry Pi Pico beginners.

Supported Shields
*****************

Hardware
========

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Spotpear (Pico …)

      .. tabs::

         .. group-tab:: ALL GPIO TEST

            .. _spotpear_pico_test:

            .. include:: spotpear_pico_test/hardware.rsti

   .. zephyr-keep-sorted-stop

Positions
=========

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Spotpear (Pico …)

      .. tabs::

         .. group-tab:: ALL GPIO TEST

            .. include:: spotpear_pico_test/positions.rsti

   .. zephyr-keep-sorted-stop

Pinouts
=======

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Spotpear (Pico …)

      .. tabs::

         .. group-tab:: ALL GPIO TEST

            .. include:: spotpear_pico_test/pinouts.rsti

   .. zephyr-keep-sorted-stop

Utilization
***********

This shields can only be used with a development board, shield, or snippet that
provides a configuration for the serial console over USB device, because the
default serial device node :dts:`&rpipico_serial` (a.k.a. :dts:`&pico_serial`)
will be disable completely and can't be used anymore for serial communication
such as logging or shell access. The same applies also to the other buses such
as I2C or SPI.

Programming
===========

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Spotpear (Pico …)

      .. tabs::

         .. group-tab:: ALL GPIO TEST

            .. include:: spotpear_pico_test/helloshell.rsti

   .. zephyr-keep-sorted-stop

More Samples
************

Input dump
==========

Prints all input events as defined by the shield's Devicetree. See also Zephyr
sample: :external+zephyr:zephyr:code-sample:`input-dump`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Spotpear (Pico …)

      .. tabs::

         .. group-tab:: ALL GPIO TEST

            .. include:: spotpear_pico_test/input_dump.rsti

   .. zephyr-keep-sorted-stop

Analog-to-Digital Converter (ADC)
=================================

Read analog inputs from ADC channels as defined by the shield's Devicetree.
See also Zephyr sample: :external+zephyr:zephyr:code-sample:`adc_dt`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Spotpear (Pico …)

      .. tabs::

         .. group-tab:: ALL GPIO TEST

            .. include:: spotpear_pico_test/adc_dt.rsti

   .. zephyr-keep-sorted-stop

Light-Emitting Diode (LED) by PWM
=================================

Control PWM LEDs as defined by the shield's Devicetree. See also Zephyr
sample: :external+zephyr:zephyr:code-sample:`led-pwm`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Spotpear (Pico …)

      .. tabs::

         .. group-tab:: ALL GPIO TEST

            .. include:: spotpear_pico_test/led_pwm.rsti

   .. zephyr-keep-sorted-stop

References
**********

.. target-notes::
