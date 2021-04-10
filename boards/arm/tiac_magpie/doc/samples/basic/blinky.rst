.. _tiac_magpie_led_blinky-sample:

LED Blinky
##########

Overview
********

See :ref:`blinky-sample` for the original description.

.. _tiac_magpie_led_blinky-sample-requirements:

Requirements
************

The TiaC Magpie board have two "User LEDs" connected via GPIO pins. The first
LED is configured using the ``led0`` :ref:`devicetree <dt-guide>` alias.

Building and Running
********************

Build and flash LED Blinky as follows:

.. zephyr-app-commands::
   :zephyr-app: zephyr/samples/basic/blinky
   :build-dir: led_blinky-tiac_magpie
   :board: tiac_magpie
   :goals: build flash
   :host-os: unix
   :compact:

After flashing, the first "User LED" starts to blink.
LED Blinky does not print to the console.
