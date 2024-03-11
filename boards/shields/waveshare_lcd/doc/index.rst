.. _waveshare_lcd_modules:

Waveshare LCD Modules
#####################

Overview
********

The Waveshare LCD modules are avaliable in different sizes and resolutions.
Nearly all displays comes with a special LCD controller wired over SPI up to
the board by free wiring.

Supported Modules
*****************

Hardware
========

.. tabs::

   .. group-tab:: Waveshare 2.4 LCD

      .. _waveshare_2_4_lcd:

      .. include:: /boards/shields/waveshare_lcd/doc/waveshare_2_4_lcd/hardware.rsti

Positions
=========

.. tabs::

   .. group-tab:: Waveshare 2.4 LCD

      .. include:: /boards/shields/waveshare_lcd/doc/waveshare_2_4_lcd/positions.rsti

Pinouts
=======

.. tabs::

   .. group-tab:: Waveshare 2.4 LCD

      .. include:: /boards/shields/waveshare_lcd/doc/waveshare_2_4_lcd/pinouts.rsti

Requirements
************

This shields can be used with any board which provides a configuration either
for Arduino or Arduino Nano connectors or for a special connector set and
defines node aliases for SPI and GPIO interfaces (see :ref:`zephyr:shields` for
more details).

Pin Assignments
===============

.. tabs::

   .. group-tab:: Waveshare 2.4 LCD

      .. include:: /boards/shields/waveshare_lcd/doc/waveshare_2_4_lcd/wiring.rsti

Utilization
***********

This shields can be used with any development board, shield, or snippet that
provides a Devicetree node with either the :dtcompatible:`arduino-nano-header-r3`
or the :dtcompatible:`seeed,grove-laced-if` property for the compatibility.
In particular, the :devicetree:`&arduino_nano_spi` or :devicetree:`&grove_spi`
bus and some GPIO signals of :devicetree:`&arduino_nano_header` or
:devicetree:`&grove_gpio` must be free for communication with the LCD on the
modules. On Devicetree level, the shields also providing the special node label
:devicetree:`&board_spi_lcd` for this purpose.

Programming
===========

.. tabs::

   .. group-tab:: LCD Orientation and Bit Order Test

      Using the :ref:`Display driver API <zephyr:display_api>` with chosen
      display. That is:

      | :hwftlbl-scr:`LCD` : :devicetree:`chosen { zephyr,display = &lcd_panel; };`
      | :hwftlbl-scr:`ILI9341` : :devicetree:`lcd_panel: &ili9341_240x320 {};`

      .. tabs::

         .. group-tab:: Arduino Nano R3

            If the shield is connected to a board which has Arduino Nano
            connector, set :console:`-DSHIELD=waveshare_2_4_lcd` when you
            invoke :program:`west build`. For example:

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_2_4_lcd-display_test
               :board: cytron_maker_nano_rp2040
               :shield: waveshare_2_4_lcd
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

         .. group-tab:: Grove System

            If the shield is connected to a board which has `Grove System`_
            compatiple connectors, set :console:`-DSHIELD=waveshare_2_4_lcd`
            when you invoke :program:`west build` and use one of supported
            boards with special Devicetree setup for free wiring. For example:

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_2_4_lcd-display_test
               :board: cytron_maker_pi_rp2040
               :shield: waveshare_2_4_lcd
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

   .. group-tab:: LVGL Basic Sample

      Using the LVGL module on top of the :ref:`Display driver API
      <zephyr:display_api>` with chosen display. That is:

      | :hwftlbl-scr:`LCD` : :devicetree:`chosen { zephyr,display = &lcd_panel; };`
      | :hwftlbl-scr:`ILI9341` : :devicetree:`lcd_panel: &ili9341_240x320 {};`

      .. tabs::

         .. group-tab:: Arduino Nano R3

            If the shield is connected to a board which has Arduino Nano
            connector, set :console:`-DSHIELD=waveshare_2_4_lcd` when you
            invoke :program:`west build`. For example:

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/display/lvgl
               :build-dir: waveshare_2_4_lcd-lvgl_basic
               :board: cytron_maker_nano_rp2040
               :shield: waveshare_2_4_lcd
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

         .. group-tab:: Grove System

            If the shield is connected to a board which has `Grove System`_
            compatiple connectors, set :console:`-DSHIELD=waveshare_2_4_lcd`
            when you invoke :program:`west build` and use one of supported
            boards with special Devicetree setup for free wiring. For example:

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/display/lvgl
               :build-dir: waveshare_2_4_lcd-lvgl_basic
               :board: cytron_maker_pi_rp2040
               :shield: waveshare_2_4_lcd
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

References
**********

.. target-notes::
