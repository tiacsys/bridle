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

   .. group-tab:: Waveshare Pico LCD 1.14

      .. _waveshare_pico_lcd_1_14:

      .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_lcd_1_14/hardware.rsti

   .. group-tab:: Waveshare Pico LCD 2

      .. _waveshare_pico_lcd_2:

      .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_lcd_2/hardware.rsti

   .. group-tab:: Waveshare Pico ResTouch LCD 3.5

      .. _waveshare_pico_restouch_lcd_3_5:

      .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_restouch_lcd_3_5/hardware.rsti

Positions
=========

.. tabs::

   .. group-tab:: Waveshare Pico LCD 1.14

      .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_lcd_1_14/positions.rsti

   .. group-tab:: Waveshare Pico LCD 2

      .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_lcd_2/positions.rsti

   .. group-tab:: Waveshare Pico ResTouch LCD 3.5

      .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_restouch_lcd_3_5/positions.rsti

Pinouts
=======

.. tabs::

   .. group-tab:: Waveshare Pico LCD 1.14

      .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_lcd_1_14/pinouts.rsti

   .. group-tab:: Waveshare Pico LCD 2

      .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_lcd_2/pinouts.rsti

   .. group-tab:: Waveshare Pico ResTouch LCD 3.5

      .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_restouch_lcd_3_5/pinouts.rsti

Utilization
***********

This shields can be used with any development board, shield, or snippet that
provides a Devicetree node with the :dtcompatible:`raspberrypi,pico-header-r3`
property for the compatibility. In particular, the SPI1 bus and some GPIO
signals on pins 11 to 19 (20) of this edge connector must be free for
communication with the LCD on the shields. The shields also provide the special
Devicetree labels :devicetree:`&rpipico_spi_lcd` and :devicetree:`&lcd_panel`
for this purpose.

For shields with touchscreen support, the GPIO signals on pins 21 and 22 of
the edge connector must also be free for communication with the touchscreen
controller on the shield. The shields also provide the special Devicetree
labels :devicetree:`&rpipico_spi_tsc` and :devicetree:`&tsc_panel` for this
purpose.

For shields with TF/microSD card slot, the GPIO signal on pin 29 of the edge
connector must also be free for communication with the card on the shield over
SDHC/SPI. The shields also provide the special Devicetree labels
:devicetree:`&rpipico_spi_sdc` and :devicetree:`&sdhc_spi` for this purpose.
In case of the SDHC/SDIO mode the GPIO signals on pins 7 and 24 to 29 must
be free for communication with the card over a 4-bit SDHC/SDIO interface.
But this is not yet supported and may need changes on the shield hardware.

Programming
===========

.. tabs::

   .. group-tab:: Waveshare Pico LCD 1.14

      Set ``-DSHIELD=waveshare_pico_lcd_1_14`` and use optional the
      :ref:`snippet-usb-console` when you invoke ``west build``.
      For example:

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: waveshare_pico_lcd_1_14-helloshell
               :board: rpi_pico
               :shield: "waveshare_pico_lcd_1_14"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_lcd_1_14/helloshell.rsti

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: waveshare_pico_lcd_1_14-helloshell
               :board: rpi_pico_w
               :shield: "waveshare_pico_lcd_1_14"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_lcd_1_14/helloshell.rsti

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: waveshare_pico_lcd_1_14-helloshell
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_lcd_1_14"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: waveshare_pico_lcd_1_14-helloshell
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_lcd_1_14"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_lcd_1_14/helloshell.rsti

   .. group-tab:: Waveshare Pico LCD 2

      Set ``-DSHIELD=waveshare_pico_lcd_2`` and use optional the
      :ref:`snippet-usb-console` when you invoke ``west build``.
      For example:

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: waveshare_pico_lcd_2-helloshell
               :board: rpi_pico
               :shield: "waveshare_pico_lcd_2"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_lcd_2/helloshell.rsti

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: waveshare_pico_lcd_2-helloshell
               :board: rpi_pico_w
               :shield: "waveshare_pico_lcd_2"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_lcd_2/helloshell.rsti

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: waveshare_pico_lcd_2-helloshell
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_lcd_2"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: waveshare_pico_lcd_2-helloshell
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_lcd_2"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_lcd_2/helloshell.rsti

   .. group-tab:: Waveshare Pico ResTouch LCD 3.5

      Set ``-DSHIELD=waveshare_pico_restouch_lcd_3_5`` and use optional the
      :ref:`snippet-usb-console` when you invoke ``west build``.
      For example:

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: waveshare_pico_restouch_lcd_3_5-helloshell
               :board: rpi_pico
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_restouch_lcd_3_5/helloshell.rsti

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: waveshare_pico_restouch_lcd_3_5-helloshell
               :board: rpi_pico_w
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_restouch_lcd_3_5/helloshell.rsti

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: waveshare_pico_restouch_lcd_3_5-helloshell
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: waveshare_pico_restouch_lcd_3_5-helloshell
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_restouch_lcd_3_5/helloshell.rsti

More Samples
************

Input dump
==========

Prints all input events as defined by the shields Devicetree. See also Zephyr
sample: :doc:`zephyr:samples/subsys/input/input_dump/README`.

.. tabs::

   .. group-tab:: Waveshare Pico LCD 1.14

      Print the input events related to the five on-shield joystick keys
      and two user keys using the :ref:`Input subsystem API <zephyr:input>`.
      That are:

      | :hwftlbl-btn:`A` : :devicetree:`zephyr,code = <INPUT_KEY_0>;`
      | :hwftlbl-btn:`B` : :devicetree:`zephyr,code = <INPUT_KEY_1>;`
      | :hwftlbl-joy:`UP` : :devicetree:`zephyr,code = <INPUT_KEY_UP>;`
      | :hwftlbl-joy:`DOWN` : :devicetree:`zephyr,code = <INPUT_KEY_DOWN>;`
      | :hwftlbl-joy:`LEFT` : :devicetree:`zephyr,code = <INPUT_KEY_LEFT>;`
      | :hwftlbl-joy:`RIGHT` : :devicetree:`zephyr,code = <INPUT_KEY_RIGHT>;`
      | :hwftlbl-joy:`ENTER` : :devicetree:`zephyr,code = <INPUT_KEY_ENTER>;`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: waveshare_pico_lcd_1_14-input_dump
               :board: rpi_pico
               :shield: "waveshare_pico_lcd_1_14"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: waveshare_pico_lcd_1_14-input_dump
               :board: rpi_pico_w
               :shield: "waveshare_pico_lcd_1_14"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: waveshare_pico_lcd_1_14-input_dump
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_lcd_1_14"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: waveshare_pico_lcd_1_14-input_dump
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_lcd_1_14"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

      .. rubric:: Simple logging output on target

      .. code-block:: console

         ***** delaying boot 4000ms (per build configuration) *****
         W: BUS RESET
         W: BUS RESET
         *** Booting Zephyr OS … … … (delayed boot 4000ms) ***
         Input sample started
         I: input event: dev=gpio_keys        SYN type= 1 code= 11 value=1
         I: input event: dev=gpio_keys        SYN type= 1 code= 11 value=0
         I: input event: dev=gpio_keys        SYN type= 1 code=  2 value=1
         I: input event: dev=gpio_keys        SYN type= 1 code=  2 value=0
         I: input event: dev=gpio_keys        SYN type= 1 code=103 value=1
         I: input event: dev=gpio_keys        SYN type= 1 code=103 value=0
         I: input event: dev=gpio_keys        SYN type= 1 code=108 value=1
         I: input event: dev=gpio_keys        SYN type= 1 code=108 value=0
         I: input event: dev=gpio_keys        SYN type= 1 code=105 value=1
         I: input event: dev=gpio_keys        SYN type= 1 code=105 value=0
         I: input event: dev=gpio_keys        SYN type= 1 code=106 value=1
         I: input event: dev=gpio_keys        SYN type= 1 code=106 value=0
         I: input event: dev=gpio_keys        SYN type= 1 code= 28 value=1
         I: input event: dev=gpio_keys        SYN type= 1 code= 28 value=0

   .. group-tab:: Waveshare Pico LCD 2

      Print the input events related to the four on-shield user keys using
      the :ref:`Input subsystem API <zephyr:input>`. That are:

      | :hwftlbl-btn:`0` : :devicetree:`zephyr,code = <INPUT_KEY_0>;`
      | :hwftlbl-btn:`1` : :devicetree:`zephyr,code = <INPUT_KEY_1>;`
      | :hwftlbl-btn:`2` : :devicetree:`zephyr,code = <INPUT_KEY_2>;`
      | :hwftlbl-btn:`3` : :devicetree:`zephyr,code = <INPUT_KEY_3>;`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: waveshare_pico_lcd_2-input_dump
               :board: rpi_pico
               :shield: "waveshare_pico_lcd_2"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: waveshare_pico_lcd_2-input_dump
               :board: rpi_pico_w
               :shield: "waveshare_pico_lcd_2"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: waveshare_pico_lcd_2-input_dump
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_lcd_2"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: waveshare_pico_lcd_2-input_dump
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_lcd_2"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

      .. rubric:: Simple logging output on target

      .. code-block:: console

         ***** delaying boot 4000ms (per build configuration) *****
         W: BUS RESET
         W: BUS RESET
         *** Booting Zephyr OS … … … (delayed boot 4000ms) ***
         Input sample started
         I: input event: dev=gpio_keys        SYN type= 1 code= 11 value=1
         I: input event: dev=gpio_keys        SYN type= 1 code= 11 value=0
         I: input event: dev=gpio_keys        SYN type= 1 code=  2 value=1
         I: input event: dev=gpio_keys        SYN type= 1 code=  2 value=0
         I: input event: dev=gpio_keys        SYN type= 1 code=  3 value=1
         I: input event: dev=gpio_keys        SYN type= 1 code=  3 value=0
         I: input event: dev=gpio_keys        SYN type= 1 code=  4 value=1
         I: input event: dev=gpio_keys        SYN type= 1 code=  4 value=0

   .. group-tab:: Waveshare Pico ResTouch LCD 3.5

      Print the input events related to the on-shield touchscreen panel using
      the :ref:`Input subsystem API <zephyr:input>`. That are:

      | :hwftlbl-scr:`TSC` : :devicetree:`lvgl_pointer { input = &tsc_panel; };`
      | :hwftlbl-scr:`XPT2046` : :devicetree:`tsc_panel: &xpt2046_320x480 {};`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: waveshare_pico_restouch_lcd_3_5-input_dump
               :board: rpi_pico
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: waveshare_pico_restouch_lcd_3_5-input_dump
               :board: rpi_pico_w
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: waveshare_pico_restouch_lcd_3_5-input_dump
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: waveshare_pico_restouch_lcd_3_5-input_dump
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

      .. rubric:: Simple logging output on target

      .. code-block:: console

         ***** delaying boot 4000ms (per build configuration) *****
         W: BUS RESET
         W: BUS RESET
         *** Booting Zephyr OS … … … (delayed boot 4000ms) ***
         Input sample started
         I: input event: dev=xpt2046@1            type= 3 code=  0 value=98
         I: input event: dev=xpt2046@1            type= 3 code=  1 value=174
         I: input event: dev=xpt2046@1        SYN type= 1 code=330 value=1
         I: input event: dev=xpt2046@1        SYN type= 1 code=330 value=0

LCD Orientation and Bit Order Test
==================================

Draw some basic rectangles onto the display. The rectangle colors and positions
are chosen so that you can check the orientation of the LCD and correct RGB bit
order. See also Zephyr sample: :doc:`zephyr:samples/drivers/display/README`.

.. tabs::

   .. group-tab:: Waveshare Pico LCD 1.14

      Using the :ref:`Display driver API <zephyr:display_api>` with chosen
      display. That is:

      | :hwftlbl-scr:`LCD` : :devicetree:`chosen { zephyr,display = &lcd_panel; };`
      | :hwftlbl-scr:`ST7789V` : :devicetree:`lcd_panel: &st7789v_240x135 {};`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_pico_lcd_1_14-display_test
               :board: rpi_pico
               :shield: "waveshare_pico_lcd_1_14"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_pico_lcd_1_14-display_test
               :board: rpi_pico_w
               :shield: "waveshare_pico_lcd_1_14"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_pico_lcd_1_14-display_test
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_lcd_1_14"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_pico_lcd_1_14-display_test
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_lcd_1_14"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

      .. rubric:: Simple logging output on target

      .. code-block:: console

         ***** delaying boot 4000ms (per build configuration) *****
         [00:00:00.415,000] <wrn> udc_rpi: BUS RESET
         [00:00:00.495,000] <wrn> udc_rpi: BUS RESET
         *** Booting Zephyr OS … … … (delayed boot 4000ms) ***
         [00:00:04.151,000] <inf> sample: Display sample for st7789v@0

   .. group-tab:: Waveshare Pico LCD 2

      Using the :ref:`Display driver API <zephyr:display_api>` with chosen
      display. That is:

      | :hwftlbl-scr:`LCD` : :devicetree:`chosen { zephyr,display = &lcd_panel; };`
      | :hwftlbl-scr:`ST7789V` : :devicetree:`lcd_panel: &st7789v_320x240 {};`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_pico_lcd_2-display_test
               :board: rpi_pico
               :shield: "waveshare_pico_lcd_2"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_pico_lcd_2-display_test
               :board: rpi_pico_w
               :shield: "waveshare_pico_lcd_2"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_pico_lcd_2-display_test
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_lcd_2"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_pico_lcd_2-display_test
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_lcd_2"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

      .. rubric:: Simple logging output on target

      .. code-block:: console

         ***** delaying boot 4000ms (per build configuration) *****
         [00:00:00.337,000] <wrn> udc_rpi: BUS RESET
         [00:00:00.425,000] <wrn> udc_rpi: BUS RESET
         *** Booting Zephyr OS … … … (delayed boot 4000ms) ***
         [00:00:04.151,000] <inf> sample: Display sample for st7789v@0

   .. group-tab:: Waveshare Pico ResTouch LCD 3.5

      Using the :ref:`Display driver API <zephyr:display_api>` with chosen
      display. That is:

      | :hwftlbl-scr:`LCD` : :devicetree:`chosen { zephyr,display = &lcd_panel; };`
      | :hwftlbl-scr:`ILI9488` : :devicetree:`lcd_panel: &ili9488_480x320 {};`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_pico_restouch_lcd_3_5-display_test
               :board: rpi_pico
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_pico_restouch_lcd_3_5-display_test
               :board: rpi_pico_w
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_pico_restouch_lcd_3_5-display_test
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_pico_restouch_lcd_3_5-display_test
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

      .. rubric:: Simple logging output on target

      .. code-block:: console

         ***** delaying boot 4000ms (per build configuration) *****
         [00:00:00.337,000] <wrn> udc_rpi: BUS RESET
         [00:00:00.425,000] <wrn> udc_rpi: BUS RESET
         *** Booting Zephyr OS … … … (delayed boot 4000ms) ***
         [00:00:04.151,000] <inf> sample: Display sample for ili9488@0

LVGL Basic Sample
=================

Displays “Hello World!” in the center of the screen and a counter at the bottom
which increments every second. See also Zephyr sample:
:doc:`zephyr:samples/subsys/display/lvgl/README`.

.. tabs::

   .. group-tab:: Waveshare Pico LCD 1.14

      Using the LVGL module on top of the :ref:`Display driver API
      <zephyr:display_api>` with chosen display. That is:

      | :hwftlbl-scr:`LCD` : :devicetree:`chosen { zephyr,display = &lcd_panel; };`
      | :hwftlbl-scr:`ST7789V` : :devicetree:`lcd_panel: &st7789v_240x135 {};`

      .. rubric:: Devicetree compatible

      - :dtcompatible:`zephyr,lvgl-button-input` with devicetree relation
        :devicetree:`lvgl_buttons: lvgl-buttons { input = <&gpio_keys>; };`

        | :hwftlbl-btn:`B` :
          :devicetree:`input-codes = <INPUT_KEY_1>;` :
          :devicetree:`coordinates = <120 68>;` (center of LCD)

      - :dtcompatible:`zephyr,lvgl-keypad-input` with devicetree relation
        :devicetree:`lvgl_keypad: lvgl-keypad { input = <&gpio_keys>; };`

        | :hwftlbl-joy:`UP` :
          :devicetree:`input-codes = <INPUT_KEY_UP>;` :
          :devicetree:`lvgl-codes = <LV_KEY_UP>;`
        | :hwftlbl-joy:`DOWN` :
          :devicetree:`input-codes = <INPUT_KEY_DOWN>;` :
          :devicetree:`lvgl-codes = <LV_KEY_DOWN>;`
        | :hwftlbl-joy:`LEFT` :
          :devicetree:`input-codes = <INPUT_KEY_LEFT>;` :
          :devicetree:`lvgl-codes = <LV_KEY_LEFT>;`
        | :hwftlbl-joy:`RIGHT` :
          :devicetree:`input-codes = <INPUT_KEY_RIGHT>;` :
          :devicetree:`lvgl-codes = <LV_KEY_RIGHT>;`
        | :hwftlbl-joy:`ENTER` :
          :devicetree:`input-codes = <INPUT_KEY_ENTER>;` :
          :devicetree:`lvgl-codes = <LV_KEY_ENTER>;`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/display/lvgl
               :build-dir: waveshare_pico_lcd_1_14-lvgl_basic
               :board: rpi_pico
               :shield: "waveshare_pico_lcd_1_14"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/display/lvgl
               :build-dir: waveshare_pico_lcd_1_14-lvgl_basic
               :board: rpi_pico_w
               :shield: "waveshare_pico_lcd_1_14"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/display/lvgl
               :build-dir: waveshare_pico_lcd_1_14-lvgl_basic
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_lcd_1_14"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/display/lvgl
               :build-dir: waveshare_pico_lcd_1_14-lvgl_basic
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_lcd_1_14"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

      .. rubric:: Simple test execution on target

      .. code-block:: console

         ***** delaying boot 4000ms (per build configuration) *****
         [00:00:00.321,000] <wrn> udc_rpi: BUS RESET
         [00:00:00.401,000] <wrn> udc_rpi: BUS RESET
         *** Booting Zephyr OS … … … (delayed boot 4000ms) ***
         uart:~$ _

         uart:~$ lvgl stats memory
         Heap at 0x20001400 contains 2047 units in 11 buckets

           bucket#    min units        total      largest      largest
                      threshold       chunks      (units)      (bytes)
           -----------------------------------------------------------
                 0            1            3            1            4
                 3            8            1           11           84
                 6           64            1           81          644
                10         1024            1         1345        10756

         11496 free bytes, 4376 allocated bytes, overhead = 508 bytes (3.1%)

   .. group-tab:: Waveshare Pico LCD 2

      Using the LVGL module on top of the :ref:`Display driver API
      <zephyr:display_api>` with chosen display. That is:

      | :hwftlbl-scr:`LCD` : :devicetree:`chosen { zephyr,display = &lcd_panel; };`
      | :hwftlbl-scr:`ST7789V` : :devicetree:`lcd_panel: &st7789v_320x240 {};`

      .. rubric:: Devicetree compatible

      - :dtcompatible:`zephyr,lvgl-button-input` with devicetree relation
        :devicetree:`lvgl_buttons: lvgl-buttons { input = <&gpio_keys>; };`

        | :hwftlbl-btn:`1` :
          :devicetree:`input-codes = <INPUT_KEY_1>;` :
          :devicetree:`coordinates = <160 120>;` (center of LCD)

      - :dtcompatible:`zephyr,lvgl-keypad-input` with devicetree relation
        :devicetree:`lvgl_keypad: lvgl-keypad { input = <&gpio_keys>; };`

        | :hwftlbl-btn:`3` :
          :devicetree:`input-codes = <INPUT_KEY_3>;` :
          :devicetree:`lvgl-codes = <LV_KEY_LEFT>;`
        | :hwftlbl-btn:`2` :
          :devicetree:`input-codes = <INPUT_KEY_2>;` :
          :devicetree:`lvgl-codes = <LV_KEY_RIGHT>;`
        | :hwftlbl-btn:`1` :
          :devicetree:`input-codes = <INPUT_KEY_1>;` :
          :devicetree:`lvgl-codes = <LV_KEY_ENTER>;`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/display/lvgl
               :build-dir: waveshare_pico_lcd_2-lvgl_basic
               :board: rpi_pico
               :shield: "waveshare_pico_lcd_2"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/display/lvgl
               :build-dir: waveshare_pico_lcd_2-lvgl_basic
               :board: rpi_pico_w
               :shield: "waveshare_pico_lcd_2"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/display/lvgl
               :build-dir: waveshare_pico_lcd_2-lvgl_basic
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_lcd_2"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/display/lvgl
               :build-dir: waveshare_pico_lcd_2-lvgl_basic
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_lcd_2"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

      .. rubric:: Simple test execution on target

      .. code-block:: console

         ***** delaying boot 4000ms (per build configuration) *****
         [00:00:00.401,000] <wrn> udc_rpi: BUS RESET
         [00:00:00.481,000] <wrn> udc_rpi: BUS RESET
         *** Booting Zephyr OS … … … (delayed boot 4000ms) ***
         uart:~$ _

         uart:~$ lvgl stats memory
         Heap at 0x20001328 contains 2047 units in 11 buckets

           bucket#    min units        total      largest      largest
                      threshold       chunks      (units)      (bytes)
           -----------------------------------------------------------
                 0            1            2            1            4
                 1            2            1            2           12
                 6           64            1           81          644
                10         1024            1         1356        10844

         11508 free bytes, 4368 allocated bytes, overhead = 504 bytes (3.1%)

   .. group-tab:: Waveshare Pico ResTouch LCD 3.5

      Using the LVGL module on top of the :ref:`Display driver API
      <zephyr:display_api>` and the :ref:`Input subsystem API
      <zephyr:input>` with chosen display and touchscreen panel. That is:

      | :hwftlbl-scr:`LCD` : :devicetree:`chosen { zephyr,display = &lcd_panel; };`
      | :hwftlbl-scr:`ILI9488` : :devicetree:`lcd_panel: &ili9488_480x320 {};`
      | :hwftlbl-scr:`TSC` : :devicetree:`lvgl_pointer { input = &tsc_panel; };`
      | :hwftlbl-scr:`XPT2046` : :devicetree:`tsc_panel: &xpt2046_320x480 {};`

      .. rubric:: Devicetree compatible

      - :dtcompatible:`zephyr,lvgl-pointer-input`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/display/lvgl
               :build-dir: waveshare_pico_restouch_lcd_3_5-lvgl_basic
               :board: rpi_pico
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/display/lvgl
               :build-dir: waveshare_pico_restouch_lcd_3_5-lvgl_basic
               :board: rpi_pico_w
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/display/lvgl
               :build-dir: waveshare_pico_restouch_lcd_3_5-lvgl_basic
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/display/lvgl
               :build-dir: waveshare_pico_restouch_lcd_3_5-lvgl_basic
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

      .. rubric:: Simple test execution on target

      .. code-block:: console

         ***** delaying boot 4000ms (per build configuration) *****
         [00:00:00.294,000] <wrn> udc_rpi: BUS RESET
         [00:00:00.374,000] <wrn> udc_rpi: BUS RESET
         *** Booting Zephyr OS … … … (delayed boot 4000ms) ***
         uart:~$ _

         uart:~$ lvgl stats memory
         Heap at 0x20001210 contains 2047 units in 11 buckets

           bucket#    min units        total      largest      largest
                      threshold       chunks      (units)      (bytes)
           -----------------------------------------------------------
                 1            2            1            2           12
                10         1024            1         1502        12012

         12024 free bytes, 3908 allocated bytes, overhead = 448 bytes (2.7%)

TF/microSD Demonstration
========================

This samples and test applications are only applicable on the |Waveshare Pico
ResTouch LCD 3.5| board. They will be built with activated USB-CDC/ACM console.

.. tabs::

   .. group-tab:: Waveshare Pico LCD 1.14

      .. hint::

         The |Waveshare Pico LCD 1.14| doesn't provide a TF/microSD card slot.
         This samples are not applicable.

   .. group-tab:: Waveshare Pico LCD 2

      .. hint::

         The |Waveshare Pico LCD 2| doesn't provide a TF/microSD card slot.
         This samples are not applicable.

   .. group-tab:: Waveshare Pico ResTouch LCD 3.5

      The following samples work with the chosen SDHC interface in 1-bit
      mode and connected to SPI. That is:

      | :hwftlbl-spi:`SDHC` :
        :devicetree:`&rpipico_spi_sdc { &sdhc_spi { compatible = "zephyr,sdhc-spi-slot"; }; };`
      | :hwftlbl-dsk:`TF/microSD` :
        :devicetree:`&sdhc_spi { mmc { compatible = "zephyr,sdmmc-disk"; }; };`

      .. rubric:: File system manipulation

      Using the :ref:`File Systems API <zephyr:file_system_api>` ontop of the
      :ref:`Disk Access API <zephyr:disk_access_api>` with chosen TF/microSD.
      See also Zephyr sample: :doc:`zephyr:samples/subsys/fs/fs_sample/README`.

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/fs/fs_sample
               :build-dir: waveshare_pico_restouch_lcd_3_5-display_test
               :board: rpi_pico
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/fs/fs_sample
               :build-dir: waveshare_pico_restouch_lcd_3_5-display_test
               :board: rpi_pico_w
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/fs/fs_sample
               :build-dir: waveshare_pico_restouch_lcd_3_5-display_test
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/fs/fs_sample
               :build-dir: waveshare_pico_restouch_lcd_3_5-display_test
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

      .. image:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_restouch_lcd_3_5/BEACH.bmp
         :align: right
         :height: 240
         :alt: Waveshare Pico ResTouch LCD 3.5 Demo Bitmap Image

      The TF/microSD card should be pre-formatted with FAT FS. If there are
      any files or directories present in the card, the sample lists them out
      on the console, e.g.:

      * :bbl:`(optional)` Boot Sector:
        :strong:`MBR` :emphasis:`(Master Boot Record)`
      * :bbl:`(optional)` 1st Primary Partition:
        :strong:`W95 FAT32 (LBA)` :emphasis:`(ID: 0x0C)`
      * FAT File System: :strong:`FAT (32-bit version)`
      * Content: :download:`waveshare_pico_restouch_lcd_3_5/BEACH.bmp`
        and :download:`waveshare_pico_restouch_lcd_3_5/CAT.bmp`

      .. rubric:: Simple logging output on target

      .. code-block:: console

         ***** delaying boot 4000ms (per build configuration) *****
         [00:00:00.177,000] <wrn> udc_rpi: BUS RESET
         [00:00:00.257,000] <wrn> udc_rpi: BUS RESET
         *** Booting Zephyr OS … … … (delayed boot 4000ms) ***
         [00:00:04.281,000] <inf> main: Block count 15523840
         Sector size 512
         Memory Size(MB) 7580
         Disk mounted.

         Listing dir /SD: ...
         [FILE] BEACH.BMP (size = 460854)
         [FILE] CAT.BMP (size = 460854)

      In case when no files could be listed, because there are none (empty FS),
      :file:`some.dir` directory and :file:`other.txt` file will be created and
      list will run again to show them, e.g.:

      * :bbl:`(optional)` Boot Sector:
        :strong:`MBR` :emphasis:`(Master Boot Record)`
      * :bbl:`(optional)` 1st Primary Partition:
        :strong:`W95 FAT32 (LBA)` :emphasis:`(ID: 0x0C)`
      * FAT File System: :strong:`FAT (32-bit version)`
      * Content: :brd:`NONE (empty FS)`

      .. rubric:: Simple logging output on target

      .. code-block:: console

         ***** delaying boot 4000ms (per build configuration) *****
         [00:00:00.234,000] <wrn> udc_rpi: BUS RESET
         [00:00:00.314,000] <wrn> udc_rpi: BUS RESET
         *** Booting Zephyr OS … … … (delayed boot 4000ms) ***
         [00:00:04.293,000] <inf> main: Block count 15523840
         Sector size 512
         Memory Size(MB) 7580
         Disk mounted.

         Listing dir /SD: ...
         [00:00:04.298,000] <inf> main: Creating some dir entries in /SD:

         Listing dir /SD: ...
         [FILE] SOME.DAT (size = 0)
         [DIR ] SOME

      In there is no FS (or the FS is corrupted), the disk is attempted
      to re-format to FAT FS and list will run again to show them, e.g.:

      * Boot Sector: :brd:`NONE (empty boot sector, no partition table)`
        – :bbl:`(optional)` :strong:`MBR` :emphasis:`(Master Boot Record)`
      * 1st Primary Partition: :brd:`NONE (empty partition table entry)`
        – :bbl:`(optional)` :strong:`W95 FAT32 (LBA)` :emphasis:`(ID: 0x0C)`
      * FAT File System: :brd:`NONE (empty partition)`
      * Content: :brd:`NONE (empty FS)`

      .. code-block:: console

         ***** delaying boot 4000ms (per build configuration) *****
         [00:00:00.318,000] <wrn> udc_rpi: BUS RESET
         [00:00:00.398,000] <wrn> udc_rpi: BUS RESET
         *** Booting Zephyr OS … … … (delayed boot 4000ms) ***
         [00:00:04.270,000] <inf> main: Block count 15523840
         Sector size 512
         Memory Size(MB) 7580
         Disk mounted.

         Listing dir /SD: ...
         [00:00:07.892,000] <inf> main: Creating some dir entries in /SD:

         Listing dir /SD: ...
         [FILE] SOME.DAT (size = 0)
         [DIR ] SOME

      .. tsn-include:: samples/subsys/fs/fs_sample/README.rst
         :docset: zephyr
         :start-after: sample lists them out on the debug serial output.
         :end-before: Building and Running EXT2 samples

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/fs/fs_sample
               :build-dir: waveshare_pico_restouch_lcd_3_5-display_test
               :board: rpi_pico
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :gen-args: -DCONFIG_FS_FATFS_MOUNT_MKFS=n
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/fs/fs_sample
               :build-dir: waveshare_pico_restouch_lcd_3_5-display_test
               :board: rpi_pico_w
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :gen-args: -DCONFIG_FS_FATFS_MOUNT_MKFS=n
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/fs/fs_sample
               :build-dir: waveshare_pico_restouch_lcd_3_5-display_test
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :gen-args: -DCONFIG_FS_FATFS_MOUNT_MKFS=n
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/fs/fs_sample
               :build-dir: waveshare_pico_restouch_lcd_3_5-display_test
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_restouch_lcd_3_5"
               :goals: build flash
               :west-args: -p -S usb-console
               :gen-args: -DCONFIG_FS_FATFS_MOUNT_MKFS=n
               :flash-args: -r uf2
               :compact:

References
**********

.. target-notes::
