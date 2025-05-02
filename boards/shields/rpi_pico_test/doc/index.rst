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
default serial device node :dts:`&rpipico_serial` (a.k.a. :dts:`&pico_serial`)
will be disable completely and can't be used anymore for serial communication
such as logging or shell access. The same applies also to the other buses such
as I2C or SPI.

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
sample: :external+zephyr:zephyr:code-sample:`input-dump`.

.. tabs::

   .. group-tab:: Spotpear Pico ALL GPIO TEST

      Print the input events related to the five on-shield test keys using
      the :external+zephyr:ref:`Input subsystem API <input>`. That are:

      | :hwftlbl-btn:`K1` : :dts:`zephyr,code = <INPUT_KEY_DOWN>;`
      | :hwftlbl-btn:`K2` : :dts:`zephyr,code = <INPUT_KEY_ENTER>;`
      | :hwftlbl-btn:`K3` : :dts:`zephyr,code = <INPUT_KEY_RIGHT>;`
      | :hwftlbl-btn:`K4` : :dts:`zephyr,code = <INPUT_KEY_LEFT>;`
      | :hwftlbl-btn:`K5` : :dts:`zephyr,code = <INPUT_KEY_UP>;`

      .. rubric:: Devicetree compatible

      - :dtcompatible:`zephyr,lvgl-keypad-input` with devicetree relation
        :dts:`lvgl_keypad: lvgl-keypad { input = <&gpio_keys>; };`

        | :hwftlbl-btn:`K1` :
          :dts:`input-codes = <INPUT_KEY_DOWN>;` :
          :dts:`lvgl-codes = <LV_KEY_DOWN>;`
        | :hwftlbl-btn:`K2` :
          :dts:`input-codes = <INPUT_KEY_ENTER>;` :
          :dts:`lvgl-codes = <LV_KEY_ENTER>;`
        | :hwftlbl-btn:`K3` :
          :dts:`input-codes = <INPUT_KEY_RIGHT>;` :
          :dts:`lvgl-codes = <LV_KEY_RIGHT>;`
        | :hwftlbl-btn:`K4` :
          :dts:`input-codes = <INPUT_KEY_LEFT>;` :
          :dts:`lvgl-codes = <LV_KEY_LEFT>;`
        | :hwftlbl-btn:`K5` :
          :dts:`input-codes = <INPUT_KEY_UP>;` :
          :dts:`lvgl-codes = <LV_KEY_UP>;`

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

      .. container:: highlight highlight-console notranslate no-copybutton

         .. parsed-literal::

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
See also Zephyr sample: :external+zephyr:zephyr:code-sample:`adc_dt`.

.. tabs::

   .. group-tab:: Spotpear Pico ALL GPIO TEST

      Read and print the analog input value from the one on-shield
      high-resistance potentiometer using the
      :external+zephyr:ref:`ADC driver API <adc_api>`. That are:

      | :hwftlbl:`Rₚ` : :dts:`zephyr,user { io-channels = <&adc 0>; };`

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

      .. container:: highlight highlight-console notranslate no-copybutton

         .. parsed-literal::

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
sample: :external+zephyr:zephyr:code-sample:`led-pwm`.

.. tabs::

   .. group-tab:: Spotpear Pico ALL GPIO TEST

      For each of the twenty on-shield LEDs attached to the first
      :dtcompatible:`pwm-leds` device instance found in Devicetree the same
      standard test pattern (described in the original sample documentation)
      is executed using the :external+zephyr:ref:`LED driver API <led_api>`.
      That are:

      | :hwftlbl-led:`L0` :
        :dts:`&pwm_leds { pl0: pl0 { pwms = <&pwm 12 /* … */>; }; };`
      | :hwftlbl-led:`L1` :hwftlbl-led:`L16` :
        :dts:`&pwm_leds { pl1: pl1 { pwms = <&pwm 11 /* … */>; }; };`
      | :hwftlbl-led:`L2` :
        :dts:`&pwm_leds { pl2: pl2 { pwms = <&pwm 1 /* … */>; }; };`
      | :hwftlbl-led:`L3` :
        :dts:`&pwm_leds { pl3: pl3 { pwms = <&pwm 0 /* … */>; }; };`
      | :hwftlbl-led:`L4` :hwftlbl-led:`L15` :
        :dts:`&pwm_leds { pl4: pl4 { pwms = <&pwm 6 /* … */>; }; };`
      | :hwftlbl-led:`L5` :hwftlbl-led:`L10` :
        :dts:`&pwm_leds { pl5: pl5 { pwms = <&pwm 5 /* … */>; }; };`
      | :hwftlbl-led:`L6` :hwftlbl-led:`L9` :
        :dts:`&pwm_leds { pl6: pl6 { pwms = <&pwm 3 /* … */>; }; };`
      | :hwftlbl-led:`L7` :hwftlbl-led:`L13` :
        :dts:`&pwm_leds { pl7: pl7 { pwms = <&pwm 2 /* … */>; }; };`
      | :hwftlbl-led:`L8` :hwftlbl-led:`L11` :
        :dts:`&pwm_leds { pl8: pl8 { pwms = <&pwm 4 /* … */>; }; };`
      | :hwftlbl-led:`L6` :hwftlbl-led:`L9` :
        :dts:`&pwm_leds { pl9: pl9 { pwms = <&pwm 3 /* … */>; }; };`
      | :hwftlbl-led:`L5` :hwftlbl-led:`L10` :
        :dts:`&pwm_leds { pl10: pl10 { pwms = <&pwm 5 /* … */>; }; };`
      | :hwftlbl-led:`L11` :hwftlbl-led:`L8` :
        :dts:`&pwm_leds { pl11: pl11 { pwms = <&pwm 4 /* … */>; }; };`
      | :hwftlbl-led:`L12` :
        :dts:`&pwm_leds { pl12: pl12 { pwms = <&pwm 15 /* … */>; }; };`
      | :hwftlbl-led:`L13` :hwftlbl-led:`L7` :
        :dts:`&pwm_leds { pl13: pl13 { pwms = <&pwm 2 /* … */>; }; };`
      | :hwftlbl-led:`L14` :
        :dts:`&pwm_leds { pl14: pl14 { pwms = <&pwm 7 /* … */>; }; };`
      | :hwftlbl-led:`L15` :hwftlbl-led:`L4` :
        :dts:`&pwm_leds { pl15: pl15 { pwms = <&pwm 6 /* … */>; }; };`
      | :hwftlbl-led:`L16` :hwftlbl-led:`L1` :
        :dts:`&pwm_leds { pl16: pl16 { pwms = <&pwm 11 /* … */>; }; };`
      | :hwftlbl-led:`L17` :
        :dts:`&pwm_leds { pl17: pl17 { pwms = <&pwm 10 /* … */>; }; };`
      | :hwftlbl-led:`L18` :
        :dts:`&pwm_leds { pl18: pl18 { pwms = <&pwm 9 /* … */>; }; };`
      | :hwftlbl-led:`L19` :
        :dts:`&pwm_leds { pl19: pl19 { pwms = <&pwm 8 /* … */>; }; };`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/led/pwm
               :build-dir: spotpear_pico_test-drivers_led_pwm
               :board: rpi_pico
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/led/pwm
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
               :app: zephyr/samples/drivers/led/pwm
               :build-dir: spotpear_pico_test-drivers_led_pwm
               :board: waveshare_rp2040_plus
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/led/pwm
               :build-dir: spotpear_pico_test-drivers_led_pwm
               :board: waveshare_rp2040_plus@16mb
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-LCD-0.96

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/led/pwm
               :build-dir: spotpear_pico_test-drivers_led_pwm
               :board: waveshare_rp2040_lcd_0_96
               :shield: "spotpear_pico_test"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

      .. rubric:: Simple test execution on target

      .. container:: highlight highlight-console notranslate no-copybutton

         .. parsed-literal::

            \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
            [00:00:00.374,000] :byl:`<wrn> udc_rpi: BUS RESET`
            [00:00:00.454,000] :byl:`<wrn> udc_rpi: BUS RESET`
            \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…* (delayed boot 4000ms) \*\*\*
            [00:00:04.003,000] <inf> main: Testing LED 0 - L0: Test LED 0
            [00:00:04.004,000] <inf> main:   Turned on
            [00:00:05.004,000] <inf> main:   Turned off
            [00:00:06.005,000] <inf> main:   Increasing brightness gradually
            [00:00:08.531,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:00:13.531,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:00:18.532,000] <inf> main:   Turned off, loop end
            [00:00:18.532,000] <inf> main: Testing LED 1 - L1: Test LED 1
            [00:00:18.533,000] <inf> main:   Turned on
            [00:00:19.533,000] <inf> main:   Turned off
            [00:00:20.534,000] <inf> main:   Increasing brightness gradually
            [00:00:23.059,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:00:28.060,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:00:33.061,000] <inf> main:   Turned off, loop end
            [00:00:33.061,000] <inf> main: Testing LED 2 - L2: Test LED 2
            [00:00:33.061,000] <inf> main:   Turned on
            [00:00:34.062,000] <inf> main:   Turned off
            [00:00:35.062,000] <inf> main:   Increasing brightness gradually
            [00:00:37.588,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:00:42.588,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:00:47.589,000] <inf> main:   Turned off, loop end
            [00:00:47.589,000] <inf> main: Testing LED 3 - L3: Test LED 3
            [00:00:47.590,000] <inf> main:   Turned on
            [00:00:48.590,000] <inf> main:   Turned off
            [00:00:49.591,000] <inf> main:   Increasing brightness gradually
            [00:00:52.116,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:00:57.117,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:01:02.118,000] <inf> main:   Turned off, loop end
            [00:01:02.118,000] <inf> main: Testing LED 4 - L4: Test LED 4
            [00:01:02.118,000] <inf> main:   Turned on
            [00:01:03.119,000] <inf> main:   Turned off
            [00:01:04.119,000] <inf> main:   Increasing brightness gradually
            [00:01:06.645,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:01:11.645,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:01:16.646,000] <inf> main:   Turned off, loop end
            [00:01:16.646,000] <inf> main: Testing LED 5 - L5: Test LED 5
            [00:01:16.647,000] <inf> main:   Turned on
            [00:01:17.647,000] <inf> main:   Turned off
            [00:01:18.648,000] <inf> main:   Increasing brightness gradually
            [00:01:21.173,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:01:26.174,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:01:31.175,000] <inf> main:   Turned off, loop end
            [00:01:31.175,000] <inf> main: Testing LED 6 - L6: Test LED 6
            [00:01:31.175,000] <inf> main:   Turned on
            [00:01:32.176,000] <inf> main:   Turned off
            [00:01:33.176,000] <inf> main:   Increasing brightness gradually
            [00:01:35.702,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:01:40.702,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:01:45.703,000] <inf> main:   Turned off, loop end
            [00:01:45.703,000] <inf> main: Testing LED 7 - L7: Test LED 7
            [00:01:45.704,000] <inf> main:   Turned on
            [00:01:46.704,000] <inf> main:   Turned off
            [00:01:47.705,000] <inf> main:   Increasing brightness gradually
            [00:01:50.230,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:01:55.231,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:02:00.232,000] <inf> main:   Turned off, loop end
            [00:02:00.232,000] <inf> main: Testing LED 8 - L8: Test LED 8
            [00:02:00.232,000] <inf> main:   Turned on
            [00:02:01.233,000] <inf> main:   Turned off
            [00:02:02.233,000] <inf> main:   Increasing brightness gradually
            [00:02:04.759,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:02:09.759,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:02:14.760,000] <inf> main:   Turned off, loop end
            [00:02:14.760,000] <inf> main: Testing LED 9 - L9: Test LED 9
            [00:02:14.761,000] <inf> main:   Turned on
            [00:02:15.761,000] <inf> main:   Turned off
            [00:02:16.762,000] <inf> main:   Increasing brightness gradually
            [00:02:19.287,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:02:24.288,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:02:29.289,000] <inf> main:   Turned off, loop end
            [00:02:29.289,000] <inf> main: Testing LED 10 - L10: Test LED 10
            [00:02:29.289,000] <inf> main:   Turned on
            [00:02:30.290,000] <inf> main:   Turned off
            [00:02:31.290,000] <inf> main:   Increasing brightness gradually
            [00:02:33.816,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:02:38.816,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:02:43.817,000] <inf> main:   Turned off, loop end
            [00:02:43.817,000] <inf> main: Testing LED 11 - L11: Test LED 11
            [00:02:43.818,000] <inf> main:   Turned on
            [00:02:44.818,000] <inf> main:   Turned off
            [00:02:45.819,000] <inf> main:   Increasing brightness gradually
            [00:02:48.344,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:02:53.345,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:02:58.346,000] <inf> main:   Turned off, loop end
            [00:02:58.346,000] <inf> main: Testing LED 12 - L12: Test LED 12
            [00:02:58.346,000] <inf> main:   Turned on
            [00:02:59.347,000] <inf> main:   Turned off
            [00:03:00.347,000] <inf> main:   Increasing brightness gradually
            [00:03:02.873,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:03:07.873,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:03:12.874,000] <inf> main:   Turned off, loop end
            [00:03:12.874,000] <inf> main: Testing LED 13 - L13: Test LED 13
            [00:03:12.875,000] <inf> main:   Turned on
            [00:03:13.875,000] <inf> main:   Turned off
            [00:03:14.876,000] <inf> main:   Increasing brightness gradually
            [00:03:17.401,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:03:22.402,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:03:27.403,000] <inf> main:   Turned off, loop end
            [00:03:27.403,000] <inf> main: Testing LED 14 - L14: Test LED 14
            [00:03:27.403,000] <inf> main:   Turned on
            [00:03:28.404,000] <inf> main:   Turned off
            [00:03:29.404,000] <inf> main:   Increasing brightness gradually
            [00:03:31.930,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:03:36.930,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:03:41.931,000] <inf> main:   Turned off, loop end
            [00:03:41.931,000] <inf> main: Testing LED 15 - L15: Test LED 15
            [00:03:41.932,000] <inf> main:   Turned on
            [00:03:42.932,000] <inf> main:   Turned off
            [00:03:43.933,000] <inf> main:   Increasing brightness gradually
            [00:03:46.458,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:03:51.459,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:03:56.460,000] <inf> main:   Turned off, loop end
            [00:03:56.460,000] <inf> main: Testing LED 16 - L16: Test LED 16
            [00:03:56.460,000] <inf> main:   Turned on
            [00:03:57.461,000] <inf> main:   Turned off
            [00:03:58.461,000] <inf> main:   Increasing brightness gradually
            [00:04:00.987,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:04:05.987,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:04:10.988,000] <inf> main:   Turned off, loop end
            [00:04:10.988,000] <inf> main: Testing LED 17 - L17: Test LED 17
            [00:04:10.989,000] <inf> main:   Turned on
            [00:04:11.989,000] <inf> main:   Turned off
            [00:04:12.990,000] <inf> main:   Increasing brightness gradually
            [00:04:15.515,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:04:20.516,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:04:25.517,000] <inf> main:   Turned off, loop end
            [00:04:25.517,000] <inf> main: Testing LED 18 - L18: Test LED 18
            [00:04:25.517,000] <inf> main:   Turned on
            [00:04:26.518,000] <inf> main:   Turned off
            [00:04:27.518,000] <inf> main:   Increasing brightness gradually
            [00:04:30.044,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:04:35.044,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:04:40.045,000] <inf> main:   Turned off, loop end
            [00:04:40.045,000] <inf> main: Testing LED 19 - L19: Test LED 19
            [00:04:40.046,000] <inf> main:   Turned on
            [00:04:41.046,000] <inf> main:   Turned off
            [00:04:42.047,000] <inf> main:   Increasing brightness gradually
            [00:04:44.572,000] <inf> main:   Blinking on: 20 msec, off: 20 msec
            [00:04:49.573,000] <inf> main:   Blinking on: 65 msec, off: 65 msec
            [00:04:54.574,000] <inf> main:   Turned off, loop end

References
**********

.. target-notes::
