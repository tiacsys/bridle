.. _rpi_pico_clock_shield:

Raspberry Pi Pico Clock Shields
###############################

This is a collection of very versatile clocks due to its different feature sets
and sizes, the RGB capabilities and additional buttons and sensors. Nearly all
displays comes with a special LED controller wired over GPIO or other standard
serial buses up to the Raspberry Pi Pico. Additional momentary push buttons or
joysticks and a small buzzer are wired up over simple GPIO lines. Some shield
provide also a simple temperature sensor or Real-Time-Clock, mostly wired over
a dedicated I2C bus.

Supported Shields
*****************

Hardware
========

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: Clock Green

            .. _waveshare_pico_clock_green:

            .. include:: waveshare_pico_clock_green/hardware.rsti

   .. zephyr-keep-sorted-stop

Positions
=========

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: Clock Green

            .. include:: waveshare_pico_clock_green/positions.rsti

   .. zephyr-keep-sorted-stop

Pinouts
=======

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: Clock Green

            .. include:: waveshare_pico_clock_green/pinouts.rsti

   .. zephyr-keep-sorted-stop

Utilization
***********

This shields can be used with any development board, shield, or snippet that
provides a Devicetree node with the :dtcompatible:`raspberrypi,pico-header-r3`
property for the compatibility. In particular, the I2C1 bus on pins 9 to 10 and
some GPIO signals on pins 4 to 5, 14 to 22, 24 and 29 of this edge connector
must be free for communication with the buttons, buzzer, LEDs, RTC and sensors
on the shields. The ADC channel 0 on pin 31 must also be free for communication
with the on-shield LDR (photoresistor). The shields also provide the special
Devicetree labels :dts:`&rpipico_i2c_rtc`, :dts:`&clock_rtc`,
:dts:`&rpipico_pwm_buzzers` and :dts:`&clock_buzzer` for this
purpose.

Programming
===========

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: Clock Green

            .. include:: waveshare_pico_clock_green/helloshell.rsti

   .. zephyr-keep-sorted-stop

More Samples
************

LED Blinky and Button
=====================

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: Clock Green

            .. include:: waveshare_pico_clock_green/led_button.rsti

   .. zephyr-keep-sorted-stop

Input dump
==========

Prints all input events as defined by the shields Devicetree. See also Zephyr
sample: :external+zephyr:zephyr:code-sample:`input-dump`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: Clock Green

            .. include:: waveshare_pico_clock_green/input_dump.rsti

   .. zephyr-keep-sorted-stop

Analog-to-Digital Converter (ADC)
=================================

Read analog inputs from ADC channels as defined by the shield's Devicetree.
See also Zephyr sample: :external+zephyr:zephyr:code-sample:`adc_dt`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: Clock Green

            .. include:: waveshare_pico_clock_green/adc_dt.rsti

   .. zephyr-keep-sorted-stop

Sounds from the speaker
=======================

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: Clock Green

            .. include:: waveshare_pico_clock_green/buzzer.rsti

   .. zephyr-keep-sorted-stop

LED Panel Orientation and Bit Order Test
========================================

Draw some basic rectangles onto the LED panel. The rectangle positions
are chosen so that you can check the orientation of the LED panel and
correct bit order.
See also Zephyr sample: :external+zephyr:zephyr:code-sample:`display`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: Clock Green

            .. include:: waveshare_pico_clock_green/display_test.rsti

   .. zephyr-keep-sorted-stop

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
