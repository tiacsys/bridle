Giving a board a socket
=========================

.. admonition:: Prerequisites

   - :doc:`build-a-rig-that-exists`, so the vocabulary is familiar.
   - A west workspace with ``btr-shields``, able to build for
     ``nucleo_f411re``.
   - No hardware needed to follow along; two Grove connectors soldered to
     the Arduino header if you want to run the result.

Rae has a NUCLEO-F411RE and two Grove connectors wired to its Arduino
header — a completely ordinary prototype. Zephyr knows the board; it does
not know about those two connectors. This tutorial tells it.

**One new concept: a socket is a devicetree node the board declares.**
Declaring one is how a board opts in to rigs. Everything else in this
series depends on it, and nothing in this tutorial mentions a module.

Make a place to work
----------------------

Board extensions live in a Zephyr module, and the one you are about to
write is yours, not ``btr-shields``'s. Create a small module beside it in
the workspace:

.. code-block:: console

   $ mkdir -p acme-rigs/zephyr acme-rigs/boards/extend/st/nucleo_f411re

.. code-block:: yaml

   # acme-rigs/zephyr/module.yml
   name: acme-rigs
   build:
     settings:
       board_root: .

``board_root: .`` is what makes ``boards/extend/`` under this module
discoverable. Point Zephyr at the module with
``-DEXTRA_ZEPHYR_MODULES=<workspace>/acme-rigs`` on the build command line,
or add it to your manifest.

Extend the board
------------------

You are not editing ``nucleo_f411re``. You are adding a **variant** of it —
a :term:`board extension`. Upstream's board stays untouched, and both the
plain board and your rig-enabled one remain buildable.

.. code-block:: yaml

   # acme-rigs/boards/extend/st/nucleo_f411re/board.yml
   board:
     extend: nucleo_f411re
     variants:
       - name: rig
         qualifier: stm32f411xe

``extend:`` names the base board; the variant adds the target
``nucleo_f411re/stm32f411xe/rig``. That third segment is the one you will
type from now on, and it is the same shape you saw in the previous
tutorial's configure output.

The variant needs its own devicetree, which pulls in the real board and
layers your sockets on top:

.. code-block:: devicetree

   /* acme-rigs/boards/extend/st/nucleo_f411re/nucleo_f411re_stm32f411xe_rig.dts */
   #include "nucleo_f411re.dts"
   #include "grove_sockets.dtsi"

Two lines. The first is the upstream board, verbatim — every peripheral,
pinctrl and alias it already had. The second is the only thing you are
adding.

Declare the socket
--------------------

Here is the whole new concept:

.. code-block:: devicetree

   /* acme-rigs/boards/extend/st/nucleo_f411re/grove_sockets.dtsi */
   #include <dt-bindings/connector/grove.h>

   / {
           grove_d2: connector_grove_d2 {
                   compatible = "socket,grove";
                   #gpio-cells = <2>;
                   gpio-map-mask = <0xffffffff 0xffffffc0>;
                   gpio-map-pass-thru = <0 0x3f>;
                   gpio-map = <GROVE_SIG0 0 &gpioa 10 0>,
                              <GROVE_SIG1 0 &gpiob 3  0>;
           };
   };

Read it line by line, because every line is a decision you will make again
for every board you rig-enable:

``compatible = "socket,grove"``
   This is the opt-in. It says the node is a socket of the :term:`connector
   type` ``grove``, whose contract is already authored in ``btr-shields``
   (``dts/bindings/connectors/grove.yaml``). You are *using* a connector
   type here, not defining one — a Grove connector means the same thing on
   every board, which is exactly what makes modules portable.

``grove_d2:``
   The label. This is the name a rig will use to say "plug it in here", so
   pick one a human recognises from the silkscreen. The convention is
   ``<type>`` for a board's only socket of that type and
   ``<type>_<silkscreen>`` for a family — so ``grove_d2``, because the
   connector sits on the D2/D3 pins.

``gpio-map``
   The physical truth, written down once. ``GROVE_SIG0`` and
   ``GROVE_SIG1`` are :term:`position`\ s — ``#define``\ s from the
   connector type's header, not pin numbers. The map says *this board*
   routes SIG0 to ``gpioa`` pin 10 and SIG1 to ``gpiob`` pin 3.

That last one is the load-bearing one. A module will later say "I drive
SIG0"; it will never say ``gpioa 10``. The board is the only thing that
knows the pin, this file is the only place it is written, and every rig on
this board reuses it. The tedium is paid once per board, not once per
placement — which is precisely the difference between this and the 64
overlays.

Add the variant's defconfig, mirroring the base board's:

.. code-block:: cfg

   # acme-rigs/boards/extend/st/nucleo_f411re/nucleo_f411re_stm32f411xe_rig_defconfig
   CONFIG_ARM_MPU=y
   CONFIG_HW_STACK_PROTECTION=y
   CONFIG_SERIAL=y
   CONFIG_CONSOLE=y
   CONFIG_UART_CONSOLE=y

Check that it took
--------------------

There is no module to plug in yet, so there is no rig to build. What you
*can* confirm is that the board now advertises a socket. Ask which boards
satisfy a Grove rig that already exists:

.. code-block:: console

   $ west rigs --boards-for lotus_buttons
   seeeduino_lotus/samd21g18a/rig

Your board is not listed — correctly. ``lotus_buttons`` names sockets
``grove_d2``, ``grove_d6`` and ``grove_a0`` explicitly, and yours has only
the first. That answer is a real check, not a formality: it means the
census can see your board and evaluated it. Add the other two sockets and
the same command starts listing you.

.. note::

   ``--boards-for`` answers whether a board's *sockets* satisfy a rig. It
   is not a promise the rig builds there — pin routing, chip-select
   allocation and address conflicts are decided per build, by the
   :term:`expander`.

What you have
---------------

A board that is rig-enabled. It declares, in its own devicetree, that a
Grove connector exists and where its two signals go. Nothing about modules,
nothing about applications, and nothing that any particular rig depends on.

Next
------

:doc:`write-a-shield-template` builds the other half: a module that says
what it needs in positions, so it can land on this socket or any other
Grove socket anywhere.
