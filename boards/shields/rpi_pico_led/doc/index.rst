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

   .. group-tab:: Waveshare Pico RGB LED

      .. _waveshare_pico_rgb_led:

      .. include:: waveshare_pico_rgb_led/hardware.rsti

Positions
=========

.. tabs::

   .. group-tab:: Waveshare Pico RGB LED

      .. include:: waveshare_pico_rgb_led/positions.rsti

Pinouts
=======

.. tabs::

   .. group-tab:: Waveshare Pico RGB LED

      .. include:: waveshare_pico_rgb_led/pinouts.rsti

More Samples
************

LED Blinky and Fade
===================

.. tabs::

   .. group-tab:: Waveshare Pico RGB LED

      .. image:: waveshare_pico_rgb_led/ws2812b-16x10.gif
         :align: right
         :alt: Waveshare Pico RGB LED WS2812 LED Test Pattern

      .. rubric:: WS2812 LED Test Pattern by PIO

      See also Zephyr sample: :zephyr:code-sample:`zephyr:led-strip`

      .. tabs::

         .. group-tab:: Raspberry Pi Pico

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/led_strip
               :build-dir: waveshare_pico_rgb_led-strip_test
               :board: rpi_pico
               :shield: waveshare_pico_rgb_led
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :goals: flash
               :compact:

         .. group-tab:: Raspberry Pi Pico W

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/led_strip
               :build-dir: waveshare_pico_rgb_led-strip_test
               :board: rpi_pico/rp2040/w
               :shield: waveshare_pico_rgb_led
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :goals: flash
               :compact:

         .. group-tab:: Waveshare RP2040-LCD-0.96

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/led_strip
               :build-dir: waveshare_pico_rgb_led-strip_test
               :board: waveshare_rp2040_lcd_0_96
               :shield: waveshare_pico_rgb_led
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :goals: flash
               :compact:

         .. group-tab:: Waveshare RP2040-Plus

            .. rubric:: on standard ``4㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/led_strip
               :build-dir: waveshare_pico_rgb_led-strip_test
               :board: waveshare_rp2040_plus
               :shield: waveshare_pico_rgb_led
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :goals: flash
               :compact:

            .. rubric:: on extended ``16㎆`` revision

            .. zephyr-app-commands::
               :app: zephyr/samples/drivers/led_strip
               :build-dir: waveshare_pico_rgb_led-strip_test
               :board: waveshare_rp2040_plus@16mb
               :shield: waveshare_pico_rgb_led
               :west-args: -p -S usb-console
               :flash-args: -r uf2
               :goals: flash
               :compact:

      .. rubric:: Simple logging output on target

      .. parsed-literal::
         :class: highlight-console notranslate

         \*\*\*\*\* delaying boot 4000ms (per build configuration) \*\*\*\*\*
         [00:00:00.337,000] :byl:`<wrn> udc_rpi: BUS RESET`
         [00:00:00.417,000] :byl:`<wrn> udc_rpi: BUS RESET`
         \*\*\* Booting Zephyr OS … … … (delayed boot 4000ms) \*\*\*
         [00:00:04.002,000] <inf> main: Found LED strip device rgb-led-strip
         [00:00:04.002,000] <inf> main: Displaying pattern on strip

      .. hint::

         Neither LED Blinky nor LED Fade can be built and executed on
         |Waveshare Pico RGB LED|, because this shield has only digital
         RGB LEDs. A simple GPIO or PWM control is not possible!

References
**********

.. target-notes::
