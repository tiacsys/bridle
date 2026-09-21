.. _rigs4zephyr_tutorials_build-a-rig-that-exists:

Building a rig that already exists
====================================

.. admonition:: Prerequisites

   - A west workspace with ``bridle`` and a Zephyr SDK, able to build for
     ``seeeduino_lotus``.
   - No hardware. Everything here stops at the ``.elf``.

.. note::

   This tutorial's examples are bridle's own two rigs, built for its own
   ``seeeduino_lotus`` board. The rest of this tutorial series follows the
   running example of **Rae**, a firmware developer at ACME Robotics
   working from `btr-shields <https://github.com/tiacsys/btr-shields>`__,
   the harness repository the rig model itself comes from — its board and
   module corpus is larger, and several later tutorials build on names
   from it (``nucleo_f411re``, ``acme_grove_led``, and so on) that this
   workspace does not carry. Read those tutorials as a description of the
   *mechanism*; substitute bridle's own boards, sockets and shields where
   you want to try something yourself.

Before authoring anything, see the machinery run once. This tutorial builds
a :term:`rig` that ships with bridle, then reads what the build produced —
so that when you start writing your own sockets and shields, you already
know what they turn into.

See what is available
-----------------------

.. code-block:: console

   $ west rigs
   lotus_buttons
   lotus_pwm_led

Each of those names a directory under ``boards/rigs/``. Take
``lotus_buttons``:

.. code-block:: console

   $ cat boards/rigs/lotus_buttons/rig.yml
   rig:
     name: lotus_buttons

.. code-block:: console

   $ cat boards/rigs/lotus_buttons/lotus_buttons.yml
   instances:
     - name: btn_start
       shield: grove_btn
       socket: grove_d2
       params:
         gb_key:
           zephyr,code: INPUT_KEY_0
     - name: btn_stop
       shield: grove_btn
       socket: grove_d6
       invert: true
       params:
         gb_key:
           zephyr,code: INPUT_KEY_1
     - name: led_status
       shield: grove_led
       socket: grove_a0

That is the whole rig. Two files, and the second one is the interesting
half: **two Grove Button modules and a Grove LED, each named and each
plugged into its own socket** — ``grove_d2``, ``grove_d6`` (inverted: this
one wires active-low) and ``grove_a0``. No pins, no overlay, no ``&porta``
anywhere — those are the board's business and the module's business
respectively, and neither belongs in the sentence "this module is plugged
in there". ``params:`` is the one thing a socket assignment cannot carry
on its own: ``grove_btn`` declares its keycode as a per-instance fact, so
each button assigns its own rather than sharing one.

The split is deliberate. ``rig.yml`` is the :term:`rig metadata file`: the
rig's identity, and nothing about hardware. ``lotus_buttons.yml`` is the
:term:`rig content file`: the assembly. :ref:`rigs4zephyr_tutorials_make-the-rig-permanent`
returns to why those are two files and not one.

Build it
----------

A rig is one thing added to an ordinary ``west build``: ``-DRIG=<name>``,
passed through to CMake after ``--``. Nothing else about the command
changes — which is also why the whole mechanism works with ``west``
absent entirely, as a bare ``cmake`` invocation: the ``-D`` is CMake's,
not west's.

.. code-block:: console

   $ west build -b seeeduino_lotus samples/helloshell -p always -- -DRIG=lotus_buttons

The board comes from ``-b``, exactly as in any Zephyr build. A rig names a
topology — what is plugged where — and nothing else; it has no board of its
own to fall back to, so a rig build without a board is a configure error
that says so.

Watch for these lines. They are the rig machinery reporting what it
decided, and every later tutorial is about changing one of them:

.. code-block:: text

   -- Rig: lotus_buttons (.../boards/rigs/lotus_buttons/rig.yml), board: seeeduino_lotus
   -- Rig: expanding .../boards/rigs/lotus_buttons/rig.yml -> .../rig
   -- Rig: 'lotus_buttons' board=seeeduino_lotus/samd21g18a shields=[grove_btn;grove_led]
   -- Rig: shield 'grove_btn' <- .../boards/shields/grove_btn
   -- Rig: shield 'grove_led' <- .../boards/shields/grove_led

Note the board qualifier: ``seeeduino_lotus/samd21g18a``, filled in from
``-b seeeduino_lotus`` — the same qualifier resolution any Zephyr build
does, rig or not.

Then the ordinary Zephyr build runs, and finishes ordinarily:

.. code-block:: text

   [213/213] Linking C executable zephyr/zephyr.elf
   Memory region         Used Size  Region Size  %age Used
              FLASH:       88168 B       232 KB     37.11%
                RAM:       22592 B        32 KB     68.95%

Nothing about the output is special. That is the point: a rig build is a
Zephyr build whose overlay was computed instead of written.

Read what it produced
-----------------------

The expansion wrote a directory into the build tree:

.. code-block:: console

   $ ls build/rig
   config-sheet.md  context.cmake  expectations.yml  rerun-expand.sh
   rig-gen-includes.dtsi  rig-gen.overlay  rigc-generated

``rig-gen.overlay`` is the devicetree overlay — the file you would
otherwise have written by hand, now derived. ``rigc-generated`` is the
:term:`expander`'s own scratch directory, kept rather than cleaned up: it
holds the devicetree fragments it fed its parsers, which is where to look
when a build fails for a reason the diagnostic alone does not settle
(:ref:`rigs4zephyr_reference_commands` describes it). Both can wait; the more
interesting one for a human is ``config-sheet.md``:

.. code-block:: text

   # Physical configuration sheet — rig `lotus_buttons`

   Board: **seeeduino_lotus/samd21g18a**

   ## Socket assignment

   | instance | shield | socket |
   |---|---|---|
   | btn_start | grove_btn | grove_d2 |
   | btn_stop | grove_btn | grove_d6 |
   | led_status | grove_led | grove_a0 |

   ## Parameters

   | instance | device | property | value |
   |---|---|---|---|
   | btn_start | gb_key | zephyr,code | INPUT_KEY_0 (11) |
   | btn_stop | gb_key | zephyr,code | INPUT_KEY_1 (2) |

That is the :term:`config sheet`, and it is worth pausing on. It is not
build output for the compiler — it is **assembly instructions for the
person holding the hardware**. The two tables are the tell: nobody wrote
"``grove_d2``, ``porta14``" or "``INPUT_KEY_0`` is ``11``" anywhere by
hand in the rig — the shield declared its keycode parameter and the board
declared its socket wiring; the expander put those together and resolved
the enum value while it was at it.

That is the whole idea in one file of generated Markdown. The board knows
its pins. The module knows its positions and its own parameters. Neither
knows the other, and the rig only had to say which socket, and which
keycode.

Next
------

:ref:`rigs4zephyr_tutorials_give-a-board-a-socket` starts building your own, from the board end:
a socket, on a board that does not have one yet.
