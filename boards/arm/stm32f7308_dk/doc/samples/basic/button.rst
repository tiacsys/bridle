.. _stm32f7308_dk_led_button-sample:

LED Button
##########

Overview
********

See :doc:`zephyr:samples/basic/button/README` for the original description.

.. _stm32f7308_dk_led_button-sample-requirements:

Requirements
************

The STM32F7308-DK discovery kit have three "User LEDs" and one "User Button"
connected via GPIO pins. The first LED is configured using the ``led0``
:ref:`devicetree <dt-guide>` alias. The first Button is configured using the
``sw0`` :ref:`devicetree <dt-guide>` alias.

Building and Running
********************

Build and flash LED Button as follows:

.. zephyr-app-commands::
   :app: zephyr/samples/basic/button
   :build-dir: led_button-stm32f7308_dk
   :board: stm32f7308_dk
   :goals: build flash
   :west-args: -p always
   :host-os: unix

After flashing, the first "User LED (blue)" can switch on
by pressing the "User Button".
The output to the console will look something like this:

.. code-block:: none

   Set up button at gpio@40020000 pin 0
   Set up LED at gpio@40020000 pin 5
   Press the button
   Button pressed at 519253876
   Button pressed at 724173372
   Button pressed at 833138640
   ... ... ...
