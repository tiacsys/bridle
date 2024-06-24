.. _rpi_pico_lcd_shield:

Raspberry Pi Pico LCD Shields
#############################

This is a collection of very versatile displays due to its different resolutions
and sizes, the RGB capabilities and additional buttons and joystick. Nearly all
displays comes with a special LCD controller wired over SPI up to the Raspberry
Pi Pico. Additional momentary push buttons or joysticks are wired up over simple
GPIO lines. Some shield provide also a TF/SD-card slot, wired over a second
dedicated SPI bus.

Supported Shields
*****************

Hardware
========

.. tabs::

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: LCD 0.96

            .. _waveshare_pico_lcd_0_96:

            .. include:: waveshare_pico_lcd_0_96/hardware.rsti

         .. group-tab:: LCD 1.14

            .. _waveshare_pico_lcd_1_14:

            .. include:: waveshare_pico_lcd_1_14/hardware.rsti

         .. group-tab:: LCD 1.3

            .. _waveshare_pico_lcd_1_3:

            .. include:: waveshare_pico_lcd_1_3/hardware.rsti

         .. group-tab:: LCD 1.44

            .. _waveshare_pico_lcd_1_44:

            .. include:: waveshare_pico_lcd_1_44/hardware.rsti

         .. group-tab:: LCD 1.8

            .. _waveshare_pico_lcd_1_8:

            .. include:: waveshare_pico_lcd_1_8/hardware.rsti

         .. group-tab:: LCD 2

            .. _waveshare_pico_lcd_2:

            .. include:: waveshare_pico_lcd_2/hardware.rsti

         .. group-tab:: ResTouch LCD 2.8

            .. _waveshare_pico_restouch_lcd_2_8:

            .. include:: waveshare_pico_restouch_lcd_2_8/hardware.rsti

         .. group-tab:: ResTouch LCD 3.5

            .. _waveshare_pico_restouch_lcd_3_5:

            .. include:: waveshare_pico_restouch_lcd_3_5/hardware.rsti

Positions
=========

.. tabs::

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: LCD 0.96

            .. include:: waveshare_pico_lcd_0_96/positions.rsti

         .. group-tab:: LCD 1.14

            .. include:: waveshare_pico_lcd_1_14/positions.rsti

         .. group-tab:: LCD 1.3

            .. include:: waveshare_pico_lcd_1_3/positions.rsti

         .. group-tab:: LCD 1.44

            .. include:: waveshare_pico_lcd_1_44/positions.rsti

         .. group-tab:: LCD 1.8

            .. include:: waveshare_pico_lcd_1_8/positions.rsti

         .. group-tab:: LCD 2

            .. include:: waveshare_pico_lcd_2/positions.rsti

         .. group-tab:: ResTouch LCD 2.8

            .. include:: waveshare_pico_restouch_lcd_2_8/positions.rsti

         .. group-tab:: ResTouch LCD 3.5

            .. include:: waveshare_pico_restouch_lcd_3_5/positions.rsti

Pinouts
=======

.. tabs::

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: LCD 0.96

            .. include:: waveshare_pico_lcd_0_96/pinouts.rsti

         .. group-tab:: LCD 1.14

            .. include:: waveshare_pico_lcd_1_14/pinouts.rsti

         .. group-tab:: LCD 1.3

            .. include:: waveshare_pico_lcd_1_3/pinouts.rsti

         .. group-tab:: LCD 1.44

            .. include:: waveshare_pico_lcd_1_44/pinouts.rsti

         .. group-tab:: LCD 1.8

            .. include:: waveshare_pico_lcd_1_8/pinouts.rsti

         .. group-tab:: LCD 2

            .. include:: waveshare_pico_lcd_2/pinouts.rsti

         .. group-tab:: ResTouch LCD 2.8

            .. include:: waveshare_pico_restouch_lcd_2_8/pinouts.rsti

         .. group-tab:: ResTouch LCD 3.5

            .. include:: waveshare_pico_restouch_lcd_3_5/pinouts.rsti

Utilization
***********

This shields can be used with any development board, shield, or snippet that
provides a Devicetree node with the :dtcompatible:`raspberrypi,pico-header-r3`
property for the compatibility. In particular, one SPI bus and some GPIO
signals on this edge connector must be free for communication with the LCD
on the shields. The shields also provide the special Devicetree labels
:devicetree:`&rpipico_spi_lcd` and :devicetree:`&lcd_panel` for this purpose.

For shields with touchscreen support, additional GPIO signals and on occasion
one I2C bus on the edge connector must also be free for communication with the
touchscreen controller on the shield. Then the shields also provide the special
Devicetree labels :devicetree:`&rpipico_spi_tsc` and :devicetree:`&tsc_panel`
for this purpose.

For shields with TF/microSD card slot, even more GPIO signals on the edge
connector must be free for communication with the card on the shield over
SDHC/SPI. The shields also provide the special Devicetree labels
:devicetree:`&rpipico_spi_sdc` and :devicetree:`&sdhc_spi` for this purpose.
In case of the SDHC/SDIO mode up to seven additional GPIO signals must be
free for communication with the card over a 4-bit SDHC/SDIO interface.
But this is not yet supported and may need changes on the shield hardware.

Programming
===========

.. tabs::

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: LCD 0.96

            .. include:: waveshare_pico_lcd_0_96/helloshell.rsti

         .. group-tab:: LCD 1.14

            .. include:: waveshare_pico_lcd_1_14/helloshell.rsti

         .. group-tab:: LCD 1.3

            .. include:: waveshare_pico_lcd_1_3/helloshell.rsti

         .. group-tab:: LCD 1.44

            .. include:: waveshare_pico_lcd_1_44/helloshell.rsti

         .. group-tab:: LCD 1.8

            .. include:: waveshare_pico_lcd_1_8/helloshell.rsti

         .. group-tab:: LCD 2

            .. include:: waveshare_pico_lcd_2/helloshell.rsti

         .. group-tab:: ResTouch LCD 2.8

            .. include:: waveshare_pico_restouch_lcd_2_8/helloshell.rsti

         .. group-tab:: ResTouch LCD 3.5

            .. include:: waveshare_pico_restouch_lcd_3_5/helloshell.rsti

More Samples
************

Input dump
==========

Prints all input events as defined by the shields Devicetree. See also Zephyr
sample: :zephyr:code-sample:`zephyr:input-dump`.

.. tabs::

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: LCD 0.96

            .. include:: waveshare_pico_lcd_0_96/input_dump.rsti

         .. group-tab:: LCD 1.14

            .. include:: waveshare_pico_lcd_1_14/input_dump.rsti

         .. group-tab:: LCD 1.3

            .. include:: waveshare_pico_lcd_1_3/input_dump.rsti

         .. group-tab:: LCD 1.44

            .. include:: waveshare_pico_lcd_1_44/input_dump.rsti

         .. group-tab:: LCD 1.8

            .. hint::

               The |Waveshare Pico LCD 1.8| doesn't provide any input
               components. This sample is not applicable.

         .. group-tab:: LCD 2

            .. include:: waveshare_pico_lcd_2/input_dump.rsti

         .. group-tab:: ResTouch LCD 2.8

            .. include:: waveshare_pico_restouch_lcd_2_8/input_dump.rsti

         .. group-tab:: ResTouch LCD 3.5

            .. include:: waveshare_pico_restouch_lcd_3_5/input_dump.rsti

LCD Orientation and Bit Order Test
==================================

Draw some basic rectangles onto the display. The rectangle colors and positions
are chosen so that you can check the orientation of the LCD and correct RGB bit
order. See also Zephyr sample: :zephyr:code-sample:`zephyr:display`.

.. tabs::

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: LCD 0.96

            .. include:: waveshare_pico_lcd_0_96/display_test.rsti

         .. group-tab:: LCD 1.14

            .. include:: waveshare_pico_lcd_1_14/display_test.rsti

         .. group-tab:: LCD 1.3

            .. include:: waveshare_pico_lcd_1_3/display_test.rsti

         .. group-tab:: LCD 1.44

            .. include:: waveshare_pico_lcd_1_44/display_test.rsti

         .. group-tab:: LCD 1.8

            .. include:: waveshare_pico_lcd_1_8/display_test.rsti

         .. group-tab:: LCD 2

            .. include:: waveshare_pico_lcd_2/display_test.rsti

         .. group-tab:: ResTouch LCD 2.8

            .. include:: waveshare_pico_restouch_lcd_2_8/display_test.rsti

         .. group-tab:: ResTouch LCD 3.5

            .. include:: waveshare_pico_restouch_lcd_3_5/display_test.rsti

LVGL Basic Sample
=================

Displays “Hello World!” in the center of the screen and a counter at the bottom
which increments every second. See also Zephyr sample:
:zephyr:code-sample:`zephyr:lvgl`.

.. tabs::

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: LCD 0.96

            .. include:: waveshare_pico_lcd_0_96/lvgl_basic.rsti

         .. group-tab:: LCD 1.14

            .. include:: waveshare_pico_lcd_1_14/lvgl_basic.rsti

         .. group-tab:: LCD 1.3

            .. include:: waveshare_pico_lcd_1_3/lvgl_basic.rsti

         .. group-tab:: LCD 1.44

            .. include:: waveshare_pico_lcd_1_44/lvgl_basic.rsti

         .. group-tab:: LCD 1.8

            .. include:: waveshare_pico_lcd_1_8/lvgl_basic.rsti

         .. group-tab:: LCD 2

            .. include:: waveshare_pico_lcd_2/lvgl_basic.rsti

         .. group-tab:: ResTouch LCD 2.8

            .. include:: waveshare_pico_restouch_lcd_2_8/lvgl_basic.rsti

         .. group-tab:: ResTouch LCD 3.5

            .. include:: waveshare_pico_restouch_lcd_3_5/lvgl_basic.rsti

TF/microSD Demonstration
========================

This samples and test applications aren't applicable on all boards. They will
be built with activated USB-CDC/ACM console.

.. tabs::

   .. group-tab:: Waveshare (Pico …)

      .. tabs::

         .. group-tab:: LCD 0.96

            .. hint::

               The |Waveshare Pico LCD 0.96| doesn't provide a TF/microSD card
               slot. This samples are not applicable.

         .. group-tab:: LCD 1.14

            .. hint::

               The |Waveshare Pico LCD 1.14| doesn't provide a TF/microSD card
               slot. This samples are not applicable.

         .. group-tab:: LCD 1.3

            .. hint::

               The |Waveshare Pico LCD 1.3| doesn't provide a TF/microSD card
               slot. This samples are not applicable.

         .. group-tab:: LCD 1.44

            .. hint::

               The |Waveshare Pico LCD 1.44| doesn't provide a TF/microSD card
               slot. This samples are not applicable.

         .. group-tab:: LCD 1.8

            .. hint::

               The |Waveshare Pico LCD 1.8| doesn't provide a TF/microSD card
               slot. This samples are not applicable.

         .. group-tab:: LCD 2

            .. hint::

               The |Waveshare Pico LCD 2| doesn't provide a TF/microSD card
               slot. This samples are not applicable.

         .. group-tab:: ResTouch LCD 2.8

            .. include:: waveshare_pico_restouch_lcd_2_8/sdhc_fatfs_test.rsti

         .. group-tab:: ResTouch LCD 3.5

            .. include:: waveshare_pico_restouch_lcd_3_5/sdhc_fatfs_test.rsti

References
**********

.. target-notes::
