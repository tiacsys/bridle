.. _stm32f7308_dk_led_blinky-sample:

LED Blinky
##########

Overview
********

See :doc:`zephyr:samples/basic/blinky/README` for the original description.

.. _stm32f7308_dk_led_blinky-sample-requirements:

Requirements
************

The STM32F7308-DK discovery kit have three "User LEDs" connected via GPIO pins.
The first LED is configured using the ``led0`` :ref:`devicetree <dt-guide>`
alias.

Building and Running
********************

Build and flash LED Blinky as follows:

.. zephyr-app-commands::
   :app: zephyr/samples/basic/blinky
   :build-dir: led_blinky-stm32f7308_dk
   :board: stm32f7308_dk
   :goals: build flash
   :west-args: -p always
   :host-os: unix

After flashing, the first "User LED (blue)" starts to blink.
LED Blinky does not print to the console.
