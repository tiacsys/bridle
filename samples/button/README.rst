.. _button-sample:

Button
######

.. admonition:: Downstream Copy!
   :class: note

   This sample is a copy from Zephyr with identical name and will be used
   for further development, improvement and preparation of changes for
   Zephyr within Bridle. However, the original sample still lives within
   the Zephyr namespace under the exactly same name:
   :external+zephyr:zephyr:code-sample:`button`.

Overview
********

A simple button demo showcasing the use of GPIO input using a dedicated polling
thread, spawned by an init function. Alternatively, it can be configured to use
interrupts instead. In either mode, pressing the button will light up an led.

Requirements
************

The board hardware must have a push button connected via a GPIO pin. These are
called "User buttons" on many of Zephyr's :external+zephyr:ref:`boards` and
Bridle's :ref:`boards`.

The button must be configured using the :dts:`sw0`
:external+zephyr:ref:`devicetree <dt-guide>` alias, usually in the
:external+zephyr:ref:`BOARD.dts file <devicetree-in-out-files>`. You will see
this error if you try to build this sample for an unsupported board:

   .. parsed-literal::
      :class: highlight-none notranslate

      **Unsupported board**: ``sw0`` devicetree alias is **not defined**

You may see additional build errors if the :dts:`sw0` alias exists, but is not
properly defined.

Additionally, the sample requires the :dts:`led0` devicetree alias.

The sample supports the following platforms (located
in :bridle_file:`samples/button/sample.yaml`):

.. table-from-sample-yaml::

Configuration options
=====================

The following sample-specific Kconfig options are used in this sample (located
in :bridle_file:`samples/button/Kconfig`):

.. options-from-kconfig::

Devicetree details
==================

This section provides more details on devicetree configuration.

Here is a minimal devicetree fragment which supports this sample, containing
both an :dts:`sw0` and an :dts:`led0` alias:

   .. code-block:: devicetree

      / {
          aliases {
              sw0 = &user_button;
              led0 = &user_lamp;
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
              user_button: gpio0_button {
                  gpios = <__GPIO_CTRL_NODE__ __PIN__ __FLAGS__>;
                  label = "User button";
              };
              /* ... other buttons ... */
          };

          leds {
              compatible = "gpio-leds";
              user_lamp: gpio0_led {
                  gpios = <&gpio0 10 GPIO_ACTIVE_HIGH>;
                  label = "User LD1";
              };
              /* ... other leds ... */

      };

.. rubric:: As shown:

- the :dts:`sw0 = &user_button;`
  :external+zephyr:ref:`devicetree alias <dt-alias-chosen>` must point
  to a child node of a node with a :dtcompatible:`gpio-keys`
  :external+zephyr:ref:`compatible <dt-important-props>`, and
- the :dts:`led0 = &user_lamp;`
  :external+zephyr:ref:`devicetree alias <dt-alias-chosen>` must point
  to a child node of one with a :dtcompatible:`gpio-leds`
  :external+zephyr:ref:`compatible <dt-important-props>`.

.. rubric:: The above situation is for the common case where:

- :dts:`__GPIO_CTRL_NODE__` should be a reference to a node label of class
  GPIO controller, e.g. in node :dts:`user_lamp: gpio0_led {/* … */};` the
  reference :dts:`gpios = <&gpio0 /* … */>` uses the example node label
  :dts:`gpio0:` and points to the given GPIO controller
- :dts:`__PIN__` should be a pin number, like :dts:`8` or :dts:`0`, see
  :dts:`user_lamp:` for an example
- :dts:`__FLAGS__` should be a logical OR of
  :external+zephyr:ref:`GPIO configuration flags <gpio_api>` meant to apply
  to the button, such as :dts:`(GPIO_PULL_UP | GPIO_ACTIVE_LOW)`, see
  :dts:`user_lamp:` for an example

.. rubric:: Required devicetree bindings:

This assumes the common case, where is :dts:`#gpio-cells = <2>` in the
:dts:`gpio0:` node, and that the :external+zephyr:ref:`GPIO controller's
devicetree binding <dt-bindings>` declares those two cells :yaml:`pin` and
:yaml:`flags` in :yaml:`gpio-cells` like so:

   .. code-block:: yaml

      properties:
        "#gpio-cells":
          type: int
          required: true
          const: 2

      gpio-cells:
        - pin
        - flags

This sample requires a :yaml:`pin` cell in the :dts:`gpios` property. The
:yaml:`flags` cell is optional, however, and the sample still works if the
GPIO cells do not contain :yaml:`flags`. This assumes the common case, where
the :dts:`gpios = <&gpio0 /* … */>` property in the :dts:`user_button:` and
:dts:`user_lamp:` child nodes reflects an :external+zephyr:ref:`GPIO keys and
leds devicetree binding <dt-bindings>` similar like so:

   .. code-block:: yaml

      child-binding:
        properties:
          gpios:
            type: phandle-array
            required: true

Building and Running
********************

This sample can be built for multiple boards, in this example we will build it
for the |zephyr:board:nucleo_f413zh| board:

#. polling thread

   .. zephyr-app-commands::
      :app: bridle/samples/button
      :board: nucleo_f413zh
      :build-dir: nucleo_f413zh-button-poll
      :gen-args: -DEXTRA_CONF_FILE="prj-poll.conf"
      :west-args: -p
      :goals: flash
      :compact:

#. interrupt callback

   .. zephyr-app-commands::
      :app: bridle/samples/button
      :board: nucleo_f413zh
      :build-dir: nucleo_f413zh-button-event
      :gen-args: -DEXTRA_CONF_FILE="prj-event.conf"
      :west-args: -p
      :goals: flash
      :compact:

During startup, an init function look up predefined GPIO devices, and
configures their pins in input and output mode, respectively. Depending on
the build configuration, an additional init function either spawns a
dedicated polling thread which continuously monitors the button state and
adjusts the led state to match, or sets up an interrupt that does the same
whenever the button is pressed or released.
