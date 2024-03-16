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

   .. group-tab:: Waveshare Pico Clock Green

      .. _waveshare_pico_clock_green:

      .. include:: /boards/shields/rpi_pico_clock/doc/waveshare_pico_clock_green/hardware.rsti

Positions
=========

.. tabs::

   .. group-tab:: Waveshare Pico Clock Green

      .. include:: /boards/shields/rpi_pico_clock/doc/waveshare_pico_clock_green/positions.rsti

Pinouts
=======

.. tabs::

   .. group-tab:: Waveshare Pico Clock Green

      .. include:: /boards/shields/rpi_pico_clock/doc/waveshare_pico_clock_green/pinouts.rsti

Utilization
***********

This shields can be used with any development board, shield, or snippet that
provides a Devicetree node with the :dtcompatible:`raspberrypi,pico-header-r3`
property for the compatibility. In particular, the I2C1 bus on pins 9 to 10 and
some GPIO signals on pins 4 to 5, 14 to 22, 24 and 29 of this edge connector
must be free for communication with the buttons, buzzer, LEDs, RTC and sensors
on the shields. The ADC channel 0 on pin 31 must also be free for communication
with the on-shield LDR (photoresistor). The shields also provide the special
Devicetree labels :devicetree:`&rpipico_i2c_rtc`, :devicetree:`&clock_rtc`,
:devicetree:`&rpipico_pwm_buzzers` and :devicetree:`&clock_buzzer` for this
purpose.

Programming
===========

.. tabs::

   .. group-tab:: Waveshare Pico Clock Green

      Set ``-DSHIELD=waveshare_pico_clock_green`` and use optional the
      :ref:`snippet-usb-console` when you invoke ``west build``.
      For example:

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: waveshare_pico_clock_green-helloshell
               :board: rpi_pico
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. include:: /boards/shields/rpi_pico_clock/doc/waveshare_pico_clock_green/helloshell.rsti

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: waveshare_pico_clock_green-helloshell
               :board: rpi_pico_w
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. include:: /boards/shields/rpi_pico_clock/doc/waveshare_pico_clock_green/helloshell.rsti

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: waveshare_pico_clock_green-helloshell
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: bridle/samples/helloshell
               :build-dir: waveshare_pico_clock_green-helloshell
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :host-os: unix
               :tool: all

            .. include:: /boards/shields/rpi_pico_clock/doc/waveshare_pico_clock_green/helloshell.rsti

More Samples
************

LED Blinky and Button
=====================

.. tabs::

   .. group-tab:: Waveshare Pico Clock Green

      .. rubric:: LED Blinky

      See also Zephyr sample: :doc:`zephyr:samples/basic/blinky/README`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/basic/blinky
               :build-dir: waveshare_pico_clock_green-blinky
               :board: rpi_pico
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/basic/blinky
               :build-dir: waveshare_pico_clock_green-blinky
               :board: rpi_pico_w
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/basic/blinky
               :build-dir: waveshare_pico_clock_green-blinky
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/basic/blinky
               :build-dir: waveshare_pico_clock_green-blinky
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

      .. rubric:: LED ON/OFF by Button

      See also Zephyr sample: :doc:`zephyr:samples/basic/button/README`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/basic/button
               :build-dir: waveshare_pico_clock_green-button
               :board: rpi_pico
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/basic/button
               :build-dir: waveshare_pico_clock_green-button
               :board: rpi_pico_w
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/basic/button
               :build-dir: waveshare_pico_clock_green-button
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/basic/button
               :build-dir: waveshare_pico_clock_green-button
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

Input dump
==========

Prints all input events as defined by the shields Devicetree. See also Zephyr
sample: :doc:`zephyr:samples/subsys/input/input_dump/README`.

.. tabs::

   .. group-tab:: Waveshare Pico Clock Green

      Print the input events related to the five on-shield user input keys
      and two user keys using the :ref:`Input subsystem API <zephyr:input>`.
      That are:

      | :hwftlbl-btn:`SET/FUNCTION` : :devicetree:`zephyr,code = <INPUT_KEY_ENTER>;`
      | :hwftlbl-btn:`UP` : :devicetree:`zephyr,code = <INPUT_KEY_UP>;`
      | :hwftlbl-btn:`DOWN` : :devicetree:`zephyr,code = <INPUT_KEY_DOWN>;`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: waveshare_pico_clock_green-input_dump
               :board: rpi_pico
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: waveshare_pico_clock_green-input_dump
               :board: rpi_pico_w
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: waveshare_pico_clock_green-input_dump
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/subsys/input/input_dump
               :build-dir: waveshare_pico_clock_green-input_dump
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

      .. rubric:: Simple logging output on target

      .. parsed-literal::
         :class: highlight-console notranslate

         \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
         W: BUS RESET
         W: BUS RESET
         \*\*\* Booting Zephyr OS … … … (delayed boot 4000ms) \*\*\*
         Input sample started
         I: input event: dev=wpcg-gpio-keys   SYN type= 1 code= 28 value=1
         I: input event: dev=wpcg-gpio-keys   SYN type= 1 code= 28 value=0
         I: input event: dev=wpcg-gpio-keys   SYN type= 1 code=103 value=1
         I: input event: dev=wpcg-gpio-keys   SYN type= 1 code=103 value=0
         I: input event: dev=wpcg-gpio-keys   SYN type= 1 code=108 value=1
         I: input event: dev=wpcg-gpio-keys   SYN type= 1 code=108 value=0

Analog-to-Digital Converter (ADC)
=================================

Read analog inputs from ADC channels as defined by the shield's Devicetree.
See also Zephyr sample: :doc:`zephyr:samples/drivers/adc/README`.

.. tabs::

   .. group-tab:: Waveshare Pico Clock Green

      Read and print the analog input value from the one on-shield
      high-resistance LDR using the :ref:`ADC driver API
      <zephyr:adc_api>`. That are:

      | :hwftlbl:`Rₗ` : :devicetree:`zephyr,user { io-channels = <&adc 0>; };`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/adc
               :build-dir: waveshare_pico_clock_green-drivers_adc
               :board: rpi_pico
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/adc
               :build-dir: waveshare_pico_clock_green-drivers_adc
               :board: rpi_pico_w
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/adc
               :build-dir: waveshare_pico_clock_green-drivers_adc
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/adc
               :build-dir: waveshare_pico_clock_green-drivers_adc
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_clock_green"
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
         \*\*\* Booting Zephyr OS … … … (delayed boot 4000ms) \*\*\*
         ADC reading[0]:
         - adc\ @\ 4004c000, channel 0: 907 = 730 mV
         ADC reading[1]:
         - adc\ @\ 4004c000, channel 0: 910 = 733 mV
         ADC reading[2]:
         - adc\ @\ 4004c000, channel 0: 1233 = 993 mV
         ADC reading[3]:
         - adc\ @\ 4004c000, channel 0: 1196 = 963 mV
         ADC reading[4]:
         - adc\ @\ 4004c000, channel 0: 569 = 458 mV
         ADC reading[5]:
         - adc\ @\ 4004c000, channel 0: 336 = 270 mV
         ADC reading[6]:
         - adc\ @\ 4004c000, channel 0: 285 = 229 mV
         ADC reading[7]:
         - adc\ @\ 4004c000, channel 0: 181 = 145 mV
         ADC reading[8]:
         - adc\ @\ 4004c000, channel 0: 56 = 45 mV
         ADC reading[9]:
         - adc\ @\ 4004c000, channel 0: 59 = 47 mV
         ADC reading[10]:
         - adc\ @\ 4004c000, channel 0: 56 = 45 mV
         ADC reading[11]:
         - adc\ @\ 4004c000, channel 0: 480 = 386 mV
         ADC reading[12]:
         - adc\ @\ 4004c000, channel 0: 868 = 699 mV
         ADC reading[13]:
         - adc\ @\ 4004c000, channel 0: 1878 = 1513 mV
         ADC reading[14]:
         - adc\ @\ 4004c000, channel 0: 3256 = 2623 mV
         ADC reading[15]:
         - adc\ @\ 4004c000, channel 0: 3413 = 2749 mV
         ADC reading[16]:
         - adc\ @\ 4004c000, channel 0: 3446 = 2776 mV
         ADC reading[17]:
         - adc\ @\ 4004c000, channel 0: 3470 = 2795 mV
         ADC reading[18]:
         - adc\ @\ 4004c000, channel 0: 3451 = 2780 mV
         ADC reading[19]:
         - adc\ @\ 4004c000, channel 0: 1029 = 829 mV
         ADC reading[20]:
         - adc\ @\ 4004c000, channel 0: 1004 = 808 mV
         ADC reading[21]:
         - adc\ @\ 4004c000, channel 0: 1005 = 809 mV
         ADC reading[22]:
         - adc\ @\ 4004c000, channel 0: 1000 = 805 mV
         … … …

Sounds from the speaker
=======================

.. tabs::

   .. group-tab:: Waveshare Pico Clock Green

      The sample is prepared for the on-board :hwftlbl-spk:`PIEZO` connected to
      the PWM channel at :rpi-pico-pio:`GP14` / :rpi-pico-pwm:`PWM14` (PWM7CHA).

      The PWM period is 880 ㎐, twice the concert pitch frequency of 440 ㎐.

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: bridle/samples/buzzer
               :build-dir: waveshare_pico_clock_green-buzzer
               :board: rpi_pico
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: bridle/samples/buzzer
               :build-dir: waveshare_pico_clock_green-buzzer
               :board: rpi_pico_w
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: bridle/samples/buzzer
               :build-dir: waveshare_pico_clock_green-buzzer
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: bridle/samples/buzzer
               :build-dir: waveshare_pico_clock_green-buzzer
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

      .. rubric:: Simple test execution on target

      #. play a beep
      #. play a folk song
      #. play a chrismas song

      .. parsed-literal::
         :class: highlight-console notranslate

         :bgn:`uart:~$` **buzzer beep**
         :bgn:`uart:~$` **buzzer play folksong**
         :bgn:`uart:~$` **buzzer play xmastime**

LED Panel Orientation and Bit Order Test
========================================

Draw some basic rectangles onto the LED panel. The rectangle positions are
chosen so that you can check the orientation of the LED panel and correct bit
order. See also Zephyr sample: :doc:`zephyr:samples/drivers/display/README`.

.. tabs::

   .. group-tab:: Waveshare Pico Clock Green

      .. image:: /boards/shields/rpi_pico_clock/doc/waveshare_pico_clock_green/display.gif
         :scale: 75%
         :align: right
         :alt: Waveshare Pico Clock Green Display Test

      The following samples work with the chosen display. That is:

      | :hwftlbl-scr:`LED` : :devicetree:`chosen { zephyr,display = &clock_display; };`
      | :hwftlbl-scr:`SIPOMUX-DISPLAY` : :devicetree:`clock_display: &sipo_mux_display_8 {};`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_pico_clock_green-display_test
               :board: rpi_pico
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_pico_clock_green-display_test
               :board: rpi_pico_w
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_pico_clock_green-display_test
               :board: waveshare_rp2040_plus
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/display
               :build-dir: waveshare_pico_clock_green-display_test
               :board: waveshare_rp2040_plus@16mb
               :shield: "waveshare_pico_clock_green"
               :goals: flash
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :compact:

References
**********

.. target-notes::
