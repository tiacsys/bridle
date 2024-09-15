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

   .. group-tab:: Spotpear Pico ALL GPIO TEST

      .. _spotpear_pico_test:

      .. include:: spotpear_pico_test/hardware.rsti

Positions
=========

.. tabs::

   .. group-tab:: Spotpear Pico ALL GPIO TEST

      .. include:: spotpear_pico_test/positions.rsti

Pinouts
=======

.. tabs::


   .. group-tab:: Spotpear Pico ALL GPIO TEST

      .. include:: spotpear_pico_test/pinouts.rsti

Utilization
***********

This shields can only be used with a development board, shield, or snippet that
provides a configuration for the serial console over USB device, because the
default serial device node :devicetree:`&rpipico_serial` (a.k.a.
:devicetree:`&pico_serial`) will be disable completely and can't be used anymore
for serial communication such as logging or shell access. The same applies also
to the other buses such as I2C or SPI.

Programming
===========

.. tabs::

   .. group-tab:: Spotpear Pico ALL GPIO TEST

      Use the :ref:`snippet-usb-console` and set ``-DSHIELD=spotpear_pico_test``
      when you invoke ``west build``. For example:

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: spotpear_pico_test-helloshell
               :board: rpi_pico
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. include:: spotpear_pico_test/helloshell.rsti

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: spotpear_pico_test-helloshell
               :board: rpi_pico/rp2040/w
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. include:: spotpear_pico_test/helloshell.rsti

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: spotpear_pico_test-helloshell
               :board: waveshare_rp2040_plus
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: spotpear_pico_test-helloshell
               :board: waveshare_rp2040_plus@16mb
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. include:: spotpear_pico_test/helloshell.rsti

         .. group-tab:: Waveshare RP2040-LCD-0.96

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: spotpear_pico_test-helloshell
               :board: waveshare_rp2040_lcd_0_96
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. include:: spotpear_pico_test/helloshell.rsti

More Samples
************

Input dump
==========

Prints all input events as defined by the shield's Devicetree. See also Zephyr
sample: :zephyr:code-sample:`zephyr:input-dump`.

.. tabs::

   .. group-tab:: Spotpear Pico ALL GPIO TEST

      Print the input events related to the five on-shield test keys using
      the :ref:`Input subsystem API <zephyr:input>`. That are:

      | :hwftlbl-btn:`K1` : :devicetree:`zephyr,code = <INPUT_KEY_DOWN>;`
      | :hwftlbl-btn:`K2` : :devicetree:`zephyr,code = <INPUT_KEY_ENTER>;`
      | :hwftlbl-btn:`K3` : :devicetree:`zephyr,code = <INPUT_KEY_RIGHT>;`
      | :hwftlbl-btn:`K4` : :devicetree:`zephyr,code = <INPUT_KEY_LEFT>;`
      | :hwftlbl-btn:`K5` : :devicetree:`zephyr,code = <INPUT_KEY_UP>;`

      .. rubric:: Devicetree compatible

      - :dtcompatible:`zephyr,lvgl-keypad-input` with devicetree relation
        :devicetree:`lvgl_keypad: lvgl-keypad { input = <&gpio_keys>; };`

        | :hwftlbl-btn:`K1` :
          :devicetree:`input-codes = <INPUT_KEY_DOWN>;` :
          :devicetree:`lvgl-codes = <LV_KEY_DOWN>;`
        | :hwftlbl-btn:`K2` :
          :devicetree:`input-codes = <INPUT_KEY_ENTER>;` :
          :devicetree:`lvgl-codes = <LV_KEY_ENTER>;`
        | :hwftlbl-btn:`K3` :
          :devicetree:`input-codes = <INPUT_KEY_RIGHT>;` :
          :devicetree:`lvgl-codes = <LV_KEY_RIGHT>;`
        | :hwftlbl-btn:`K4` :
          :devicetree:`input-codes = <INPUT_KEY_LEFT>;` :
          :devicetree:`lvgl-codes = <LV_KEY_LEFT>;`
        | :hwftlbl-btn:`K5` :
          :devicetree:`input-codes = <INPUT_KEY_UP>;` :
          :devicetree:`lvgl-codes = <LV_KEY_UP>;`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: spotpear_pico_test-input_dump
               :board: rpi_pico
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: spotpear_pico_test-input_dump
               :board: rpi_pico/rp2040/w
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: spotpear_pico_test-input_dump
               :board: waveshare_rp2040_plus
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: spotpear_pico_test-input_dump
               :board: waveshare_rp2040_plus@16mb
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-LCD-0.96

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: spotpear_pico_test-input_dump
               :board: waveshare_rp2040_lcd_0_96
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

      .. rubric:: Simple test execution on target

      .. parsed-literal::
         :class: highlight-console notranslate

         \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
         W: BUS RESET
         W: BUS RESET
         \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* (delayed boot 4000ms) \*\*\*
         Input sample started
         I: input event: dev=gpio_keys        SYN type= 1 code=108 value=1
         I: input event: dev=gpio_keys        SYN type= 1 code=108 value=0
         I: input event: dev=gpio_keys        SYN type= 1 code= 28 value=1
         I: input event: dev=gpio_keys        SYN type= 1 code= 28 value=0
         I: input event: dev=gpio_keys        SYN type= 1 code=106 value=1
         I: input event: dev=gpio_keys        SYN type= 1 code=106 value=0
         I: input event: dev=gpio_keys        SYN type= 1 code=105 value=1
         I: input event: dev=gpio_keys        SYN type= 1 code=105 value=0
         I: input event: dev=gpio_keys        SYN type= 1 code=103 value=1
         I: input event: dev=gpio_keys        SYN type= 1 code=103 value=0

Analog-to-Digital Converter (ADC)
=================================

Read analog inputs from ADC channels as defined by the shield's Devicetree.
See also Zephyr sample: :zephyr:code-sample:`zephyr:adc_dt`.

.. tabs::

   .. group-tab:: Spotpear Pico ALL GPIO TEST

      Read and print the analog input value from the one on-shield
      high-resistance potentiometer using the :ref:`ADC driver API
      <zephyr:adc_api>`. That are:

      | :hwftlbl:`Rₚ` : :devicetree:`zephyr,user { io-channels = <&adc 0>; };`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/adc/adc_dt
               :build-dir: spotpear_pico_test-drivers_adc
               :board: rpi_pico
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/adc/adc_dt
               :build-dir: spotpear_pico_test-drivers_adc
               :board: rpi_pico/rp2040/w
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/adc/adc_dt
               :build-dir: spotpear_pico_test-drivers_adc
               :board: waveshare_rp2040_plus
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/adc/adc_dt
               :build-dir: spotpear_pico_test-drivers_adc
               :board: waveshare_rp2040_plus@16mb
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-LCD-0.96

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/adc/adc_dt
               :build-dir: spotpear_pico_test-drivers_adc
               :board: waveshare_rp2040_lcd_0_96
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

      .. rubric:: Simple test execution on target

      .. parsed-literal::
         :class: highlight-console notranslate

         \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
         [00:00:00.287,000] :byl:`<wrn> udc_rpi: BUS RESET`
         [00:00:00.368,000] :byl:`<wrn> udc_rpi: BUS RESET`
         \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* (delayed boot 4000ms) \*\*\*
         ADC reading[0]:
         - adc\ @\ 4004c000, channel 0: 25 = 20 mV
         ADC reading[1]:
         - adc\ @\ 4004c000, channel 0: 171 = 137 mV
         ADC reading[2]:
         - adc\ @\ 4004c000, channel 0: 979 = 788 mV
         ADC reading[3]:
         - adc\ @\ 4004c000, channel 0: 1818 = 1464 mV
         ADC reading[4]:
         - adc\ @\ 4004c000, channel 0: 2521 = 2031 mV
         ADC reading[5]:
         - adc\ @\ 4004c000, channel 0: 3152 = 2539 mV
         ADC reading[6]:
         - adc\ @\ 4004c000, channel 0: 4019 = 3237 mV
         ADC reading[7]:
         - adc\ @\ 4004c000, channel 0: 4095 = 3299 mV

Light-Emitting Diode (LED) by PWM
=================================

Control PWM LEDs as defined by the shield's Devicetree. See also Zephyr
sample: :zephyr:code-sample:`zephyr:led-pwm`.

.. tabs::

   .. group-tab:: Spotpear Pico ALL GPIO TEST

      For each of the twenty on-shield LEDs attached to the first
      :dtcompatible:`pwm-leds` device instance found in Devicetree the same
      standard test pattern (described in the original sample documentation)
      is executed using the :ref:`LED driver API <zephyr:led_api>`. That are:

      | :hwftlbl-led:`L0` :
        :devicetree:`&pwm_leds { pl0: pl0 { pwms = <&pwm 12 /* … */>; }; };`
      | :hwftlbl-led:`L1` :hwftlbl-led:`L16` :
        :devicetree:`&pwm_leds { pl1: pl1 { pwms = <&pwm 11 /* … */>; }; };`
      | :hwftlbl-led:`L2` :
        :devicetree:`&pwm_leds { pl2: pl2 { pwms = <&pwm 1 /* … */>; }; };`
      | :hwftlbl-led:`L3` :
        :devicetree:`&pwm_leds { pl3: pl3 { pwms = <&pwm 0 /* … */>; }; };`
      | :hwftlbl-led:`L4` :hwftlbl-led:`L15` :
        :devicetree:`&pwm_leds { pl4: pl4 { pwms = <&pwm 6 /* … */>; }; };`
      | :hwftlbl-led:`L5` :hwftlbl-led:`L10` :
        :devicetree:`&pwm_leds { pl5: pl5 { pwms = <&pwm 5 /* … */>; }; };`
      | :hwftlbl-led:`L6` :hwftlbl-led:`L9` :
        :devicetree:`&pwm_leds { pl6: pl6 { pwms = <&pwm 3 /* … */>; }; };`
      | :hwftlbl-led:`L7` :hwftlbl-led:`L13` :
        :devicetree:`&pwm_leds { pl7: pl7 { pwms = <&pwm 2 /* … */>; }; };`
      | :hwftlbl-led:`L8` :hwftlbl-led:`L11` :
        :devicetree:`&pwm_leds { pl8: pl8 { pwms = <&pwm 4 /* … */>; }; };`
      | :hwftlbl-led:`L6` :hwftlbl-led:`L9` :
        :devicetree:`&pwm_leds { pl9: pl9 { pwms = <&pwm 3 /* … */>; }; };`
      | :hwftlbl-led:`L5` :hwftlbl-led:`L10` :
        :devicetree:`&pwm_leds { pl10: pl10 { pwms = <&pwm 5 /* … */>; }; };`
      | :hwftlbl-led:`L11` :hwftlbl-led:`L8` :
        :devicetree:`&pwm_leds { pl11: pl11 { pwms = <&pwm 4 /* … */>; }; };`
      | :hwftlbl-led:`L12` :
        :devicetree:`&pwm_leds { pl12: pl12 { pwms = <&pwm 15 /* … */>; }; };`
      | :hwftlbl-led:`L13` :hwftlbl-led:`L7` :
        :devicetree:`&pwm_leds { pl13: pl13 { pwms = <&pwm 2 /* … */>; }; };`
      | :hwftlbl-led:`L14` :
        :devicetree:`&pwm_leds { pl14: pl14 { pwms = <&pwm 7 /* … */>; }; };`
      | :hwftlbl-led:`L15` :hwftlbl-led:`L4` :
        :devicetree:`&pwm_leds { pl15: pl15 { pwms = <&pwm 6 /* … */>; }; };`
      | :hwftlbl-led:`L16` :hwftlbl-led:`L1` :
        :devicetree:`&pwm_leds { pl16: pl16 { pwms = <&pwm 11 /* … */>; }; };`
      | :hwftlbl-led:`L17` :
        :devicetree:`&pwm_leds { pl17: pl17 { pwms = <&pwm 10 /* … */>; }; };`
      | :hwftlbl-led:`L18` :
        :devicetree:`&pwm_leds { pl18: pl18 { pwms = <&pwm 9 /* … */>; }; };`
      | :hwftlbl-led:`L19` :
        :devicetree:`&pwm_leds { pl19: pl19 { pwms = <&pwm 8 /* … */>; }; };`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/led_pwm
               :build-dir: spotpear_pico_test-drivers_led_pwm
               :board: rpi_pico
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/led_pwm
               :build-dir: spotpear_pico_test-drivers_led_pwm
               :board: rpi_pico/rp2040/w
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/led_pwm
               :build-dir: spotpear_pico_test-drivers_led_pwm
               :board: waveshare_rp2040_plus
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/led_pwm
               :build-dir: spotpear_pico_test-drivers_led_pwm
               :board: waveshare_rp2040_plus@16mb
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-LCD-0.96

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/led_pwm
               :build-dir: spotpear_pico_test-drivers_led_pwm
               :board: waveshare_rp2040_lcd_0_96
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

      .. rubric:: Simple test execution on target

      .. parsed-literal::
         :class: highlight-console notranslate

         \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
         [00:00:00.181,000] :byl:`<wrn> udc_rpi: BUS RESET`
         [00:00:00.266,000] :byl:`<wrn> udc_rpi: BUS RESET`
         \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* (delayed boot 4000ms) \*\*\*
         [00:00:04.003,000] <inf> main: Testing LED 0 - L0: Test LED 0
         [00:00:04.004,000] <inf> main:   Turned on
         [00:00:05.005,000] <inf> main:   Turned off
         [00:00:06.005,000] <inf> main:   Increasing brightness gradually
         [00:00:08.026,000] :brd:`<err> main: err=-22`
         [00:00:08.026,000] <inf> main: Testing LED 1 - L1: Test LED 1
         [00:00:08.027,000] <inf> main:   Turned on
         [00:00:09.027,000] <inf> main:   Turned off
         [00:00:10.028,000] <inf> main:   Increasing brightness gradually
         [00:00:12.049,000] :brd:`<err> main: err=-22`
         [00:00:12.049,000] <inf> main: Testing LED 2 - L2: Test LED 2
         [00:00:12.049,000] <inf> main:   Turned on
         [00:00:13.050,000] <inf> main:   Turned off
         [00:00:14.050,000] <inf> main:   Increasing brightness gradually
         [00:00:16.071,000] :brd:`<err> main: err=-22`
         [00:00:16.071,000] <inf> main: Testing LED 3 - L3: Test LED 3
         [00:00:16.072,000] <inf> main:   Turned on
         [00:00:17.072,000] <inf> main:   Turned off
         [00:00:18.073,000] <inf> main:   Increasing brightness gradually
         [00:00:20.094,000] :brd:`<err> main: err=-22`
         [00:00:20.094,000] <inf> main: Testing LED 4 - L4: Test LED 4
         [00:00:20.094,000] <inf> main:   Turned on
         [00:00:21.095,000] <inf> main:   Turned off
         [00:00:22.095,000] <inf> main:   Increasing brightness gradually
         [00:00:24.116,000] :brd:`<err> main: err=-22`
         [00:00:24.117,000] <inf> main: Testing LED 5 - L5: Test LED 5
         [00:00:24.117,000] <inf> main:   Turned on
         [00:00:25.118,000] <inf> main:   Turned off
         [00:00:26.118,000] <inf> main:   Increasing brightness gradually
         [00:00:28.139,000] :brd:`<err> main: err=-22`
         [00:00:28.139,000] <inf> main: Testing LED 6 - L6: Test LED 6
         [00:00:28.140,000] <inf> main:   Turned on
         [00:00:29.140,000] <inf> main:   Turned off
         [00:00:30.141,000] <inf> main:   Increasing brightness gradually
         [00:00:32.162,000] :brd:`<err> main: err=-22`
         [00:00:32.162,000] <inf> main: Testing LED 7 - L7: Test LED 7
         [00:00:32.162,000] <inf> main:   Turned on
         [00:00:33.163,000] <inf> main:   Turned off
         [00:00:34.163,000] <inf> main:   Increasing brightness gradually
         [00:00:36.184,000] :brd:`<err> main: err=-22`
         [00:00:36.184,000] <inf> main: Testing LED 8 - L8: Test LED 8
         [00:00:36.185,000] <inf> main:   Turned on
         [00:00:37.185,000] <inf> main:   Turned off
         [00:00:38.186,000] <inf> main:   Increasing brightness gradually
         [00:00:40.207,000] :brd:`<err> main: err=-22`
         [00:00:40.207,000] <inf> main: Testing LED 9 - L9: Test LED 9
         [00:00:40.207,000] <inf> main:   Turned on
         [00:00:41.208,000] <inf> main:   Turned off
         [00:00:42.208,000] <inf> main:   Increasing brightness gradually
         [00:00:44.229,000] :brd:`<err> main: err=-22`
         [00:00:44.230,000] <inf> main: Testing LED 10 - L10: Test LED 10
         [00:00:44.230,000] <inf> main:   Turned on
         [00:00:45.231,000] <inf> main:   Turned off
         [00:00:46.231,000] <inf> main:   Increasing brightness gradually
         [00:00:48.252,000] :brd:`<err> main: err=-22`
         [00:00:48.252,000] <inf> main: Testing LED 11 - L11: Test LED 11
         [00:00:48.253,000] <inf> main:   Turned on
         [00:00:49.253,000] <inf> main:   Turned off
         [00:00:50.254,000] <inf> main:   Increasing brightness gradually
         [00:00:52.275,000] :brd:`<err> main: err=-22`
         [00:00:52.275,000] <inf> main: Testing LED 12 - L12: Test LED 12
         [00:00:52.275,000] <inf> main:   Turned on
         [00:00:53.276,000] <inf> main:   Turned off
         [00:00:54.276,000] <inf> main:   Increasing brightness gradually
         [00:00:56.297,000] :brd:`<err> main: err=-22`
         [00:00:56.298,000] <inf> main: Testing LED 13 - L13: Test LED 13
         [00:00:56.298,000] <inf> main:   Turned on
         [00:00:57.298,000] <inf> main:   Turned off
         [00:00:58.299,000] <inf> main:   Increasing brightness gradually
         [00:01:00.320,000] :brd:`<err> main: err=-22`
         [00:01:00.320,000] <inf> main: Testing LED 14 - L14: Test LED 14
         [00:01:00.321,000] <inf> main:   Turned on
         [00:01:01.321,000] <inf> main:   Turned off
         [00:01:02.322,000] <inf> main:   Increasing brightness gradually
         [00:01:04.342,000] :brd:`<err> main: err=-22`
         [00:01:04.343,000] <inf> main: Testing LED 15 - L15: Test LED 15
         [00:01:04.343,000] <inf> main:   Turned on
         [00:01:05.344,000] <inf> main:   Turned off
         [00:01:06.344,000] <inf> main:   Increasing brightness gradually
         [00:01:08.365,000] :brd:`<err> main: err=-22`
         [00:01:08.365,000] <inf> main: Testing LED 16 - L16: Test LED 16
         [00:01:08.366,000] <inf> main:   Turned on
         [00:01:09.366,000] <inf> main:   Turned off
         [00:01:10.367,000] <inf> main:   Increasing brightness gradually
         [00:01:12.388,000] :brd:`<err> main: err=-22`
         [00:01:12.388,000] <inf> main: Testing LED 17 - L17: Test LED 17
         [00:01:12.388,000] <inf> main:   Turned on
         [00:01:13.389,000] <inf> main:   Turned off
         [00:01:14.389,000] <inf> main:   Increasing brightness gradually
         [00:01:16.410,000] :brd:`<err> main: err=-22`
         [00:01:16.411,000] <inf> main: Testing LED 18 - L18: Test LED 18
         [00:01:16.411,000] <inf> main:   Turned on
         [00:01:17.412,000] <inf> main:   Turned off
         [00:01:18.412,000] <inf> main:   Increasing brightness gradually
         [00:01:20.433,000] :brd:`<err> main: err=-22`
         [00:01:20.433,000] <inf> main: Testing LED 19 - L19: Test LED 19
         [00:01:20.434,000] <inf> main:   Turned on
         [00:01:21.434,000] <inf> main:   Turned off
         [00:01:22.435,000] <inf> main:   Increasing brightness gradually
         [00:01:24.456,000] :brd:`<err> main: err=-22`

References
**********

.. target-notes::
