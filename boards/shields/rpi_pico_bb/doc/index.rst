.. _rpi_pico_bb_shield:

Raspberry Pi Pico Breadboard Shields
####################################

This is a collection of different shields with a breadboard area specifically
designed for use with a Raspberry Pi Pico (W) for rapid prototyping. Ranging
from very simple setups, just to reach the individual signals, to providing
already more complex components such as digital inputs and outputs (buttons,
LEDs or buzzer), joysticks (digital or analog), displays with or without
touchscreen, multi-color (RGB) LEDs, or TF/SD card slots.

Supported Shields
*****************

Hardware
========

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: GeeekPi (Pico …)

      .. tabs::

         .. group-tab:: Breadboard Kit

            .. _geeekpi_pico_bb:

            .. include:: geeekpi_pico_bb/hardware.rsti

         .. group-tab:: Breadboard Kit Plus

            .. _geeekpi_pico_bb_plus:

            .. include:: geeekpi_pico_bb_plus/hardware.rsti

   .. zephyr-keep-sorted-stop

Positions
=========

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: GeeekPi (Pico …)

      .. tabs::

         .. group-tab:: Breadboard Kit

            .. include:: geeekpi_pico_bb/positions.rsti

         .. group-tab:: Breadboard Kit Plus

            .. include:: geeekpi_pico_bb_plus/positions.rsti

   .. zephyr-keep-sorted-stop

Pinouts
=======

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: GeeekPi (Pico …)

      .. tabs::

         .. group-tab:: Breadboard Kit

            .. include:: geeekpi_pico_bb/pinouts.rsti

         .. group-tab:: Breadboard Kit Plus

            .. include:: geeekpi_pico_bb_plus/pinouts.rsti

   .. zephyr-keep-sorted-stop

Utilization
***********

This shields can be used with any development board, shield, or snippet that
provides a Devicetree node with the :dtcompatible:`raspberrypi,pico-header-r3`
property for the compatibility. In particular, one SPI bus and some GPIO
signals on this edge connector must be free for communication with the
components on the breadboard shields. The shields also provide the special
Devicetree labels :dts:`&rpipico_spi_lcd` and :dts:`&lcd_panel` for the special
purpose of a on-shield LCD.

For shields with touchscreen support, additional GPIO signals and one I2C bus
on the edge connector must also be free for communication with the touchscreen
controller on the shield. Then the shields also provide the special Devicetree
labels :dts:`&rpipico_spi_tsc` and :dts:`&tsc_panel` for this purpose.

For shields with TF/microSD card slot, even more GPIO signals on the edge
connector must be free for communication with the card on the shield over
SDHC/SPI. Then the shields also provide the special Devicetree labels
:dts:`&rpipico_spi_sdc` and :dts:`&sdhc_spi` for this purpose. In case of
the SDHC/SDIO mode up to seven additional GPIO signals must be free for
communication with the card over a 4-bit SDHC/SDIO interface. But this is
not yet supported and may need changes on the shield hardware.

Programming
===========

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: GeeekPi (Pico …)

      .. tabs::

         .. group-tab:: Breadboard Kit

            .. include:: geeekpi_pico_bb/helloshell.rsti

         .. group-tab:: Breadboard Kit Plus

            .. include:: geeekpi_pico_bb_plus/helloshell.rsti

   .. zephyr-keep-sorted-stop

More Samples
************

Input dump
==========

Prints all input events as defined by the shields Devicetree. See also Zephyr
sample: :zephyr:code-sample:`input-dump`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: GeeekPi (Pico …)

      .. tabs::

         .. group-tab:: Breadboard Kit

            .. include:: geeekpi_pico_bb/input_dump.rsti

         .. group-tab:: Breadboard Kit Plus

            .. include:: geeekpi_pico_bb_plus/input_dump.rsti

   .. zephyr-keep-sorted-stop

Sounds from the speaker
=======================

Drives an buzzer or speaker that must defined by the shields Devicetree.
See also Bridle sample: :ref:`buzzer-sample`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: GeeekPi (Pico …)

      .. tabs::

         .. group-tab:: Breadboard Kit

            .. include:: geeekpi_pico_bb/buzzer.rsti

         .. group-tab:: Breadboard Kit Plus

            .. include:: geeekpi_pico_bb_plus/buzzer.rsti

   .. zephyr-keep-sorted-stop

LED color change
================

Drives an RGB LED that must defined by the shields Devicetree. See also Zephyr
sample: :zephyr:code-sample:`rgb-led`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: GeeekPi (Pico …)

      .. tabs::

         .. group-tab:: Breadboard Kit

            .. hint::

               The |GeeekPi Pico Breadboard Kit| doesn't provide
               a TriColor ChipLED. This sample is not applicable.

         .. group-tab:: Breadboard Kit Plus

            .. hint::

               The |GeeekPi Pico Breadboard Kit Plus| doesn't provide
               a TriColor ChipLED. This sample is not applicable.

   .. zephyr-keep-sorted-stop

LED strip test pattern
======================

Drives an RGB LED strip that must defined by the shields Devicetree.
See also Zephyr sample: :zephyr:code-sample:`led-strip`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: GeeekPi (Pico …)

      .. tabs::

         .. group-tab:: Breadboard Kit

            .. hint::

               The |GeeekPi Pico Breadboard Kit| doesn't provide
               a RGB LED strip. This sample is not applicable.

         .. group-tab:: Breadboard Kit Plus

            .. include:: geeekpi_pico_bb_plus/ledstrip_test.rsti

   .. zephyr-keep-sorted-stop

LCD Orientation and Bit Order Test
==================================

Draw some basic rectangles onto the display. The rectangle colors and positions
are chosen so that you can check the orientation of the LCD and correct RGB bit
order. See also Zephyr sample: :zephyr:code-sample:`display`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: GeeekPi (Pico …)

      .. tabs::

         .. group-tab:: Breadboard Kit

            .. include:: geeekpi_pico_bb/display_test.rsti

         .. group-tab:: Breadboard Kit Plus

            .. include:: geeekpi_pico_bb_plus/display_test.rsti

   .. zephyr-keep-sorted-stop

Draw touch events on LCD
========================

Draw a small plus in the last touched coordinates. In this way, parameters such
as inverted/swapped axes can be examined. See also Zephyr sample:
:zephyr:code-sample:`draw_touch_events`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: GeeekPi (Pico …)

      .. tabs::

         .. group-tab:: Breadboard Kit

            .. include:: geeekpi_pico_bb/touch_test.rsti

         .. group-tab:: Breadboard Kit Plus

            .. include:: geeekpi_pico_bb_plus/touch_test.rsti

   .. zephyr-keep-sorted-stop

LVGL Basic Sample
=================

Displays “Hello World!” in the center of the screen and a counter at the bottom
which increments every second. See also Zephyr sample:
:zephyr:code-sample:`lvgl`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: GeeekPi (Pico …)

      .. tabs::

         .. group-tab:: Breadboard Kit

            .. include:: geeekpi_pico_bb/lvgl_basic.rsti

         .. group-tab:: Breadboard Kit Plus

            .. include:: geeekpi_pico_bb_plus/lvgl_basic.rsti

   .. zephyr-keep-sorted-stop

LVGL Widgets Demo
=================

Shows how the widgets look like out of the box using the built-in material
theme. See also Zephyr sample: :zephyr:code-sample:`lvgl-demos`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: GeeekPi (Pico …)

      .. tabs::

         .. group-tab:: Breadboard Kit

            .. include:: geeekpi_pico_bb/lvgl_demo.rsti

         .. group-tab:: Breadboard Kit Plus

            .. include:: geeekpi_pico_bb_plus/lvgl_demo.rsti

   .. zephyr-keep-sorted-stop

TF/microSD Demonstration
========================

This samples and test applications aren't applicable on all boards. They will
be built with activated USB-CDC/ACM console.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: GeeekPi (Pico …)

      .. tabs::

         .. group-tab:: Breadboard Kit

            .. hint::

               The |GeeekPi Pico Breadboard Kit| doesn't provide
               a TF/microSD card slot. This sample is not applicable.

         .. group-tab:: Breadboard Kit Plus

            .. hint::

               The |GeeekPi Pico Breadboard Kit Plus| doesn't provide
               a TF/microSD card slot. This sample is not applicable.

   .. zephyr-keep-sorted-stop

References
**********

.. target-notes::
