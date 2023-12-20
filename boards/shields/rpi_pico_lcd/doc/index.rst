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

Positions
=========

.. tabs::

   .. group-tab:: Waveshare Pico LCD 1.14

      .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_lcd_1_14/positions.rsti

   .. group-tab:: Waveshare Pico LCD 2

      .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_lcd_2/positions.rsti

Pinouts
=======

.. tabs::

   .. group-tab:: Waveshare Pico LCD 1.14

      .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_lcd_1_14/pinouts.rsti

   .. group-tab:: Waveshare Pico LCD 2

      .. include:: /boards/shields/rpi_pico_lcd/doc/waveshare_pico_lcd_2/pinouts.rsti

Utilization
***********

This shields can be used with any development board, shield, or snippet that
provides a Devicetree node with the :dtcompatible:`raspberrypi,pico-header-r3`
property for the compatibility. In particular, the SPI1 bus and some GPIO
signals on pins 11 to 19 of this edge connector must be free for communication
with the LCD on the shields. The shields also provide the special Devicetree
label :devicetree:`&rpipico_spi_lcd` for this purpose.

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
      | :hwftlbl-btn:`DOWN` : :devicetree:`zephyr,code = <INPUT_KEY_DOWN>;`
      | :hwftlbl-btn:`ENTER` : :devicetree:`zephyr,code = <INPUT_KEY_ENTER>;`
      | :hwftlbl-btn:`RIGHT` : :devicetree:`zephyr,code = <INPUT_KEY_RIGHT>;`
      | :hwftlbl-btn:`LEFT` : :devicetree:`zephyr,code = <INPUT_KEY_LEFT>;`
      | :hwftlbl-btn:`UP` : :devicetree:`zephyr,code = <INPUT_KEY_UP>;`

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
         I: input event: dev=keys             SYN type= 1 code=108 value=1
         I: input event: dev=keys             SYN type= 1 code=108 value=0
         I: input event: dev=keys             SYN type= 1 code= 28 value=1
         I: input event: dev=keys             SYN type= 1 code= 28 value=0
         I: input event: dev=keys             SYN type= 1 code=106 value=1
         I: input event: dev=keys             SYN type= 1 code=106 value=0
         I: input event: dev=keys             SYN type= 1 code=105 value=1
         I: input event: dev=keys             SYN type= 1 code=105 value=0
         I: input event: dev=keys             SYN type= 1 code=103 value=1
         I: input event: dev=keys             SYN type= 1 code=103 value=0

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
         [00:00:00.363,000] <wrn> udc_rpi: BUS RESET
         [00:00:00.443,000] <wrn> udc_rpi: BUS RESET
         *** Booting Zephyr OS … … … (delayed boot 4000ms) ***
         uart:~$ _

         uart:~$ lvgl stats memory
         Heap at 0x20001038 contains 2047 units in 11 buckets

           bucket#    min units        total      largest      largest
                      threshold       chunks      (units)      (bytes)
           -----------------------------------------------------------
                 1            2            1            2           12
                10         1024            1         1550        12396

         12408 free bytes, 3560 allocated bytes, overhead = 412 bytes (2.5%)

   .. group-tab:: Waveshare Pico LCD 2

      Using the LVGL module on top of the :ref:`Display driver API
      <zephyr:display_api>` with chosen display. That is:

      | :hwftlbl-scr:`LCD` : :devicetree:`chosen { zephyr,display = &lcd_panel; };`
      | :hwftlbl-scr:`ST7789V` : :devicetree:`lcd_panel: &st7789v_320x240 {};`

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
         [00:00:00.332,000] <wrn> udc_rpi: BUS RESET
         [00:00:00.416,000] <wrn> udc_rpi: BUS RESET
         *** Booting Zephyr OS … … … (delayed boot 4000ms) ***
         uart:~$ _

         uart:~$ lvgl stats memory
         Heap at 0x20001048 contains 2047 units in 11 buckets

           bucket#    min units        total      largest      largest
                      threshold       chunks      (units)      (bytes)
           -----------------------------------------------------------
                 1            2            1            2           12
                10         1024            1         1550        12396

         12408 free bytes, 3560 allocated bytes, overhead = 412 bytes (2.5%)

References
**********

.. target-notes::

.. _RT9193-33:
   https://www.richtek.com/Products/Linear%20Regulator/Single%20Output%20Linear%20Regulator/RT9193

.. _RT9193 Datasheet:
   https://www.richtek.com/assets/product_file/RT9193/DS9193-18.pdf

.. _ST7789V:
   https://www.sitronix.com.tw/en/products/aiot-device-ddi

.. _ST7789VW Datasheet V1.0 (2017/09):
   http://www.lcdwiki.com/res/MSP1308/ST7789VW_datasheet.pdf
.. https://www.rhydolabz.com/documents/33/ST7789.pdf
.. https://www.waveshare.com/wiki/Pico-LCD-1.14#Document
.. https://files.waveshare.com/upload/a/ad/ST7789VW.pdf
.. https://files.waveshare.com/upload/a/ae/ST7789_Datasheet.pdf

.. _ST7789V Datasheet V1.6 (2017/09):
   https://www.crystalfontz.com/controllers/Sitronix/ST7789V/470

.. _ST7789V Datasheet V1.4 (2014/10):
   https://www.crystalfontz.com/controllers/Sitronix/ST7789V/446

.. _ST7789V Datasheet V1.3 (2014/03):
   https://newhavendisplay.com/content/datasheets/ST7789V.pdf
.. https://orientdisplay.com/wp-content/uploads/2020/11/ST7789V.pdf
.. https://threefivedisplays.com/wp-content/uploads/datasheets/lcd_driver_datasheets/ST7789_V_REV_1_3_DS.pdf

.. _ST7789V Datasheet V0.1 (2013/07):
   https://github.com/Xinyuan-LilyGO/LilyGo-HAL/raw/master/DISPLAY/ST7789V.pdf
.. https://www.crystalfontz.com/controllers/Sitronix/ST7789V/382

.. _Waveshare Pico LCD 1.14:
   https://www.waveshare.com/wiki/Pico-LCD-1.14

.. _Waveshare Pico LCD 1.14 Schematic:
   https://www.waveshare.com/wiki/Pico-LCD-1.14#Document

.. _Waveshare Pico LCD 2:
   https://www.waveshare.com/wiki/Pico-LCD-2

.. _Waveshare Pico LCD 2 Schematic:
   https://www.waveshare.com/wiki/Pico-LCD-2#Document

.. |Waveshare Pico LCD 1.14| replace::
   :ref:`Waveshare Pico LCD 1.14 <waveshare_pico_lcd_1_14>`

.. |Waveshare Pico LCD 2| replace::
   :ref:`Waveshare Pico LCD 2 <waveshare_pico_lcd_2>`
