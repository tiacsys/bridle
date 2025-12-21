.. _rpi_pico_led_shield:

Raspberry Pi Pico LED Shields
#############################

This is a collection of very versatile LED matrix displays due to its different
resolutions and sizes, the RGB capabilities and additional buttons and joystick.

Supported Shields
*****************

Hardware
========

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: RGB LED

            .. _waveshare_pico_rgb_led:

            .. include:: waveshare_pico_rgb_led/hardware.rsti

   .. zephyr-keep-sorted-stop

Positions
=========

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: RGB LED

            .. include:: waveshare_pico_rgb_led/positions.rsti

   .. zephyr-keep-sorted-stop

Pinouts
=======

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: RGB LED

            .. include:: waveshare_pico_rgb_led/pinouts.rsti

   .. zephyr-keep-sorted-stop

More Samples
************

LED Blinky and Button
=====================

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: RGB LED

            .. include:: waveshare_pico_rgb_led/led_button.rsti

   .. zephyr-keep-sorted-stop

LED Display Orientation and Bit Order Test
==========================================

Draw some basic rectangles onto the display. The rectangle colors and positions
are chosen so that you can check the orientation of the LED display and correct
RGB bit order.
See also Zephyr sample: :external+zephyr:zephyr:code-sample:`display`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: RGB LED

            .. include:: waveshare_pico_rgb_led/display_test.rsti

   .. zephyr-keep-sorted-stop

References
**********

.. target-notes::
