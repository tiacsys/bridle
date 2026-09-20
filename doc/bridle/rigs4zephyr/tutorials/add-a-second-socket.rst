Adding a second socket
========================

.. admonition:: Prerequisites

   - :doc:`make-the-rig-permanent` — the rig this grows.

Rae solders the second Grove connector to the D4/D5 pins and wants a second
LED on it.

**One new concept: placement is a rig fact, so the same module
instantiates as many times as you have sockets.** This is the thing a
Zephyr shield overlay structurally cannot do, and it costs one line here.

Add the socket
----------------

Same file, same shape as the first — the board gains a second physical
truth:

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

           grove_d4: connector_grove_d4 {
                   compatible = "socket,grove";
                   #gpio-cells = <2>;
                   gpio-map-mask = <0xffffffff 0xffffffc0>;
                   gpio-map-pass-thru = <0 0x3f>;
                   gpio-map = <GROVE_SIG0 0 &gpiob 5 0>,
                              <GROVE_SIG1 0 &gpiob 4 0>;
           };
   };

Note the labels: ``grove_d2`` and ``grove_d4``, named for the silkscreen.
That is the family form of the naming convention — ``<type>_<silkscreen>``
once a board has more than one socket of a type. The single-socket form,
bare ``grove``, would now be a lie.

Add the instance
------------------

.. code-block:: yaml

   # acme-rigs/boards/rigs/acme_bench/acme_bench.yml
   instances:
     - name: status
       shield: acme_grove_led
       socket: grove_d2
     - name: fault
       shield: acme_grove_led
       socket: grove_d4

That is the entire change. Two lines of rig, and there are now two LEDs.

Stop and compare. To get here with Zephyr shield overlays you would need a
second overlay file — same module, same driver, different pin, duplicated
in full — and a third for the next connector, and a fourth. That is the
arithmetic that produces sixty-four overlays for one Grove button: two
axes (which pin, which polarity) multiplied out into files, because an
overlay has nowhere else to put them. Here the pin axis is ``socket:``,
one word per placement.

Both instances resolve through the **same** template. ``acme_grove_led``
was not copied, edited, or parameterised — the expander instantiated it
twice and resolved ``GROVE_SIG0`` through each socket's own ``gpio-map``,
so ``status`` lands on ``gpioa 10`` and ``fault`` on ``gpiob 5``.

.. code-block:: console

   $ west build -b nucleo_f411re/stm32f411xe/rig \
       btr-shields/samples/rigs/scenario-1 -- -DRIG=acme_bench
   $ cat build/rig/config-sheet.md

.. code-block:: text

   ## Socket assignment

   | instance | shield | socket |
   |---|---|---|
   | status | acme_grove_led | grove_d2 |
   | fault  | acme_grove_led | grove_d4 |

Two rows, and the instance names are doing their job: ``status`` and
``fault`` are the two LEDs as the *application* thinks of them, not as the
wiring does.

Inference stops guessing
--------------------------

There is a consequence for the shortcut from
:doc:`build-a-rig-on-the-fly`. It worked because the board had exactly one
Grove socket. It does not any more:

.. code-block:: console

   $ west build -b nucleo_f411re/stm32f411xe/rig \
       btr-shields/samples/rigs/scenario-1 -- -DRIG=acme_grove_led
   error: instance 'acme_grove_led': shield 'acme_grove_led' plugs 'grove',
   which mates more than one socket of board
   'nucleo_f411re/stm32f411xe/rig' -- add an explicit socket: to pick one
   candidates: grove_d2, grove_d4

This is correct behaviour, not a regression. Inference resolves a socket
only when there is exactly one candidate; two is an error that lists them
and asks you to choose. A tool that picked ``grove_d2`` because it sorted
first would be picking which LED lights up, and it would be right half the
time.

The strictness is the same instinct as the rest of the model: the board
states facts, the module states requirements, and anything genuinely
ambiguous is the *author's* decision — surfaced at configure time, in a
message that names the candidates, rather than guessed at.

.. note::

   The error above is what a rejected rig looks like in general. The
   expander runs before devicetree processing, so an assembly that cannot
   physically work fails the configure with a diagnostic that names the
   instance, the shield and the reason — never a link error, and never a
   device that silently is not there.

What you have
---------------

A board with two sockets, a rig with two instances, and one template
serving both. From here the axes separate cleanly: more sockets on the
board, more instances in the rig, and the module described exactly once.
