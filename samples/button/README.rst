.. _button-sample:

Button
######

Overview
********

A simple button demo showcasing the use of GPIO input using a dedicated polling
thread, spawned by an init function. Alternatively, it can be configured to use
interrupts instead.
In either mode, pressing the button will light up an led.

Requirements
************

The board hardware must have a push button connected via a GPIO pin. These are
called "User buttons" on many of Zephyr's :ref:`boards`.

The button must be configured using the ``sw0`` :ref:`devicetree <dt-guide>`
alias, usually in the :ref:`BOARD.dts file <devicetree-in-out-files>`. You will
see this error if you try to build this sample for an unsupported board:

.. code-block:: none

   Unsupported board: sw0 devicetree alias is not defined

You may see additional build errors if the ``sw0`` alias exists, but is not
properly defined.

Additionally, the sample requires the ``led0`` devicetree alias.

Devicetree details
==================

This section provides more details on devicetree configuration.

Here is a minimal devicetree fragment which supports this sample, containing
both an ``sw0`` and an ``led0`` alias.

.. code-block:: devicetree

   / {
   	aliases {
   		sw0 = &button0;
   		led0 = &green_led_1;
   	};

   	soc {
   		gpio0: gpio@0 {
   			status = "okay";
   			gpio-controller;
   			#gpio-cells = <2>;
   			/* ... */
   		};
   	};

   	buttons {
   		compatible = "gpio-keys";
   		button0: button_0 {
   			gpios = < &gpio0 PIN FLAGS >;
   			label = "User button";
   		};
   		/* ... other buttons ... */
   	};

   	leds {
		compatible = "gpio-leds";
	 	green_led_1: led_1 {
	 		gpios = <&gpiob 0 GPIO_ACTIVE_HIGH>;
	 		label = "User LD1";
	 	};
   		/* ... other leds ... */
	 	
   };

As shown, the ``sw0`` devicetree alias must point to a child node of a node
with a "gpio-keys" :ref:`compatible <dt-important-props>`, and the ``led0``
alias must point to a child node of one with a "gpio-leds" :ref:`compatible <dt-important-props>`.

The above situation is for the common case where:

- ``gpio0`` is an example node label referring to a GPIO controller
-  ``PIN`` should be a pin number, like ``8`` or ``0``
- ``FLAGS`` should be a logical OR of :ref:`GPIO configuration flags <gpio_api>`
  meant to apply to the button, such as ``(GPIO_PULL_UP | GPIO_ACTIVE_LOW)``

This assumes the common case, where ``#gpio-cells = <2>`` in the ``gpio0``
node, and that the GPIO controller's devicetree binding names those two cells
"pin" and "flags" like so:

.. code-block:: yaml

   gpio-cells:
     - pin
     - flags

This sample requires a ``pin`` cell in the ``gpios`` property. The ``flags``
cell is optional, however, and the sample still works if the GPIO cells
do not contain ``flags``.

Building and Running
********************

This sample can be built for multiple boards, in this example we will build it
for the nucleo_f413zh board:

.. zephyr-app-commands::
   :zephyr-app: bridle/samples/button
   :board: nucleo_f413zh
   :goals: build
   :compact:

During startup, an init function look up predefined GPIO devices, and
configures their pins in input and output mode, respectively. Depending on
the build configuration, an additional init function either spawns a
dedicated polling thread which continuously monitors the button state and
adjusts the led state to match, or sets up an interrupt that does the same
whenever the button is pressed or released.
