.. _n6-boot-selector-sample:

N6 Boot Selector
################

Overview
********

A small helper application that exposes the ``assert`` and ``deassert``
:external+zephyr:ref:`shell <shell_api>` commands to drive a single GPIO line.

The STM32N6's external flash is multiplexed between the STM32CubeProgrammer
(via STLink) and the N6 SoC itself; a hardware boot pin selects which side gets
access. This application is meant to run on a *second* board that is wired to
that boot pin. The :bridle_file:`stm32n6_boot west flash runner
<scripts/west_commands/runners/stm32n6_boot.py>` opens this board's shell UART
and sends ``assert`` before programming and ``deassert`` afterwards, so the pin
is toggled automatically around every flash operation.


Requirements
************

The board acting as the boot-pin controller must have a free GPIO pin wired to
the STM32N6 boot pin, exposed through the :dts:`boot-ctrl-gpios` property of the
:dts:`/zephyr,user` node, and a shell UART. You will see this error if you try
to build this sample for a board without that property:

   .. parsed-literal::
      :class: highlight-none notranslate

      **Unsupported board**: ``boot-ctrl-gpios`` is **not defined**
      in ``/zephyr,user``

The sample supports the following platforms (located
in :bridle_file:`samples/n6_boot_selector/sample.yaml`):

.. table-from-sample-yaml::

A ready-to-use overlay is provided for the |zephyr:board:frdm_rw612| board
(located in :bridle_file:`samples/n6_boot_selector/boards/frdm_rw612.overlay`),
which maps the control pin to the Arduino ``D2`` header pin (``hsgpio0`` pin
11).

Devicetree details
==================

Here is a minimal devicetree fragment which supports this sample. The
:dts:`/zephyr,user` node is a binding-free place to put application-specific
devicetree configuration, so no custom binding is needed:

   .. code-block:: devicetree

      / {
          zephyr,user {
              boot-ctrl-gpios = <&gpio0 11 GPIO_ACTIVE_HIGH>;
          };
      };


Building and Running
********************

This sample can be built for any board that provides the
:dts:`boot-ctrl-gpios` property in :dts:`/zephyr,user`. In this example we build
it for the |zephyr:board:frdm_rw612| board:

.. zephyr-app-commands::
   :app: bridle/samples/n6_boot_selector
   :build-dir: frdm_rw612-n6-boot-selector
   :board: frdm_rw612
   :west-args: -p
   :goals: flash
   :compact:

During startup the application configures the :dts:`boot-ctrl` pin as an output
in the de-asserted (inactive) state and registers the ``assert`` and
``deassert`` shell commands:

   .. code-block:: console

      uart:~$ assert
      boot-ctrl asserted (gpio@0 pin 11)
      uart:~$ deassert
      boot-ctrl de-asserted (gpio@0 pin 11)

Using it with the STM32N6 flash runner
======================================

Once this application is flashed onto the controller board, point the
:bridle_file:`stm32n6_boot runner
<scripts/west_commands/runners/stm32n6_boot.py>` at its shell UART when
flashing the STM32N6 target:

   .. code-block:: console

      west flash -- --boot-device=/dev/ttyACM1

The runner asserts the boot pin, runs STM32CubeProgrammer, and de-asserts the
pin again when programming finishes.
