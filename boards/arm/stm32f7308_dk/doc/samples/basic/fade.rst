.. _stm32f7308_dk_led_fade-sample:

LED Fade
########

Overview
********

See :doc:`zephyr:samples/basic/fade_led/README` for the original description.

.. _stm32f7308_dk_led_fade-sample-requirements:

Requirements
************

The STM32F7308-DK discovery kit have three "User LEDs" connected via GPIO pins
and only the last one connected to a dedicated PWM channel. The third LED is
configured using the ``pwm-led0`` :ref:`devicetree <dt-guide>` alias.

Building and Running
********************

Build and flash LED Fade as follows:

.. zephyr-app-commands::
   :app: zephyr/samples/basic/fade_led
   :build-dir: led_fade-stm32f7308_dk
   :board: stm32f7308_dk
   :goals: build flash
   :west-args: -p always
   :host-os: unix

After flashing, the third "User LED (green)" starts to fade.
The output to the console will look something like this:

.. code-block:: none

   PWM-based LED fade
