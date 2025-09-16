.. _magpie_f777ni_led_blinky-sample:

LED Blinky
##########

Overview
********

See :external+zephyr:zephyr:code-sample:`blinky` for the original description.

.. _magpie_f777ni_led_blinky-sample-requirements:

Requirements
************

The TiaC Magpie board have two "User LEDs" connected via GPIO pins.
The first LED is configured using the ``led0``
:external+zephyr:ref:`devicetree <dt-guide>` alias.

Building and Running
********************

Build and flash LED Blinky as follows:

   .. zephyr-app-commands::
      :app: zephyr/samples/basic/blinky
      :build-dir: led_blinky-magpie_f777ni
      :board: magpie_f777ni
      :west-args: -p
      :goals: flash
      :host-os: unix

Sample Output
=============

After flashing, the first "User LED" starts to blink.
LED Blinky does not print to the console.

   .. container:: highlight highlight-console notranslate

      .. parsed-literal::

         \*\*\* Booting Zephyr OS build |zephyr_version_em|\ *…*\*\*\*
         LED state: OFF
         LED state: ON
         LED state: OFF
         LED state: ON
         LED state: OFF
         … … …
