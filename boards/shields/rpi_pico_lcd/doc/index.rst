.. _rpi_pico_lcd_shield:

Raspberry Pi Pico LCD Shields
#############################

This is a collection of very versatile displays due to its different resolutions
and sizes, the RGB capabilities and additional buttons and joystick. Nearly all
displays comes with a special LCD controller wired over SPI up to the Raspberry
Pi Pico. Additional momentary push buttons or joysticks are wired up over simple
GPIO lines. Some shield provide also a TF/SD-card slot, wired over a second
dedicated SPI bus.

.. toctree::
   :caption: Supported Shields
   :maxdepth: 1
   :glob:

   **/index

Supported Shields
*****************

Hardware
========

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: ResTouch LCD 3.5

            .. _waveshare_pico_restouch_lcd_3_5:

            .. include:: waveshare_pico_restouch_lcd_3_5/hardware.rsti

   .. zephyr-keep-sorted-stop

Positions
=========

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: ResTouch LCD 3.5

            .. include:: waveshare_pico_restouch_lcd_3_5/positions.rsti

   .. zephyr-keep-sorted-stop

Pinouts
=======

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: ResTouch LCD 3.5

            .. include:: waveshare_pico_restouch_lcd_3_5/pinouts.rsti

   .. zephyr-keep-sorted-stop

Utilization
***********

This shields can be used with any development board, shield, or snippet that
provides a Devicetree node with the :dtcompatible:`raspberrypi,pico-header-r3`
property for the compatibility. In particular, one SPI bus and some GPIO
signals on this edge connector must be free for communication with the LCD
on the shields. The shields also provide the special Devicetree labels
:dts:`&rpipico_spi_lcd` and :dts:`&lcd_panel` for this purpose.

For shields with touchscreen support, additional GPIO signals and on occasion
one I2C bus on the edge connector must also be free for communication with the
touchscreen controller on the shield. Then the shields also provide the special
Devicetree labels :dts:`&rpipico_spi_tsc` and :dts:`&tsc_panel`
for this purpose.

For shields with TF/microSD card slot, even more GPIO signals on the edge
connector must be free for communication with the card on the shield over
SDHC/SPI. The shields also provide the special Devicetree labels
:dts:`&rpipico_spi_sdc` and :dts:`&sdhc_spi` for this purpose.
In case of the SDHC/SDIO mode up to seven additional GPIO signals must be
free for communication with the card over a 4-bit SDHC/SDIO interface.
But this is not yet supported and may need changes on the shield hardware.

Programming
===========

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: ResTouch LCD 3.5

            .. include:: waveshare_pico_restouch_lcd_3_5/helloshell.rsti

   .. zephyr-keep-sorted-stop

More Samples
************

Input dump
==========

Prints all input events as defined by the shields Devicetree. See also Zephyr
sample: :external+zephyr:zephyr:code-sample:`input-dump`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: ResTouch LCD 3.5

            .. include:: waveshare_pico_restouch_lcd_3_5/input_dump.rsti

   .. zephyr-keep-sorted-stop

LED color change
================

Drives an RGB LED that must defined by the shields Devicetree. See also Zephyr
sample: :external+zephyr:zephyr:code-sample:`rgb-led`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: ResTouch LCD 3.5

            .. hint::

               The |Waveshare Pico ResTouch LCD 3.5| doesn't provide a RGB LED.
               This samples are not applicable.

   .. zephyr-keep-sorted-stop

LCD Orientation and Bit Order Test
==================================

Draw some basic rectangles onto the display. The rectangle colors and positions
are chosen so that you can check the orientation of the LCD and correct RGB bit
order. See also Zephyr sample: :external+zephyr:zephyr:code-sample:`display`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: ResTouch LCD 3.5

            .. include:: waveshare_pico_restouch_lcd_3_5/display_test.rsti

   .. zephyr-keep-sorted-stop

Draw touch events on LCD
========================

Draw a small plus in the last touched coordinates. In this way, parameters such
as inverted/swapped axes can be examined. See also Zephyr sample:
:external+zephyr:zephyr:code-sample:`draw_touch_events`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: ResTouch LCD 3.5

            .. include:: waveshare_pico_restouch_lcd_3_5/touch_test.rsti

   .. zephyr-keep-sorted-stop

LVGL Basic Sample
=================

Displays “Hello World!” in the center of the screen and a counter at the bottom
which increments every second. See also Zephyr sample:
:external+zephyr:zephyr:code-sample:`lvgl`.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: ResTouch LCD 3.5

            .. include:: waveshare_pico_restouch_lcd_3_5/lvgl_basic.rsti

   .. zephyr-keep-sorted-stop

TF/microSD Demonstration
========================

This samples and test applications aren't applicable on all boards. They will
be built with activated USB-CDC/ACM console.

.. tabs::

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: ResTouch LCD 3.5

            .. include:: waveshare_pico_restouch_lcd_3_5/sdhc_fatfs_test.rsti

   .. zephyr-keep-sorted-stop

References
**********

.. target-notes::
