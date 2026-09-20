Building a rig that already exists
====================================

.. admonition:: Prerequisites

   - A west workspace with ``btr-shields`` and a Zephyr SDK, able to build
     for ``nucleo_f401re``.
   - No hardware. Everything here stops at the ``.elf``.

Before authoring anything, see the machinery run once. This tutorial builds
a :term:`rig` that ships with ``btr-shields``, then reads what the build
produced — so that when you start writing your own sockets and shields, you
already know what they turn into.

The running example across these tutorials is **Rae**, a firmware developer
at ACME Robotics. Rae has an ST NUCLEO-F401RE on the bench and, eventually,
a pile of sensor modules to attach to it. Today they are just looking.

See what is available
-----------------------

.. code-block:: console

   $ west rigs
   ard_datalogger
   frdm_cs_clash
   frdm_eth_nest
   lotus_buttons
   lotus_pwm
   ...

Each of those names a directory under ``boards/rigs/``. Take
``nucleo_datalogger``:

.. code-block:: console

   $ cat btr-shields/boards/rigs/nucleo_datalogger/rig.yml
   rig:
     name: nucleo_datalogger

.. code-block:: console

   $ cat btr-shields/boards/rigs/nucleo_datalogger/nucleo_datalogger.yml
   instances:
     - name: logger
       shield: adafruit_data_logger
       socket: arduino_r3

That is the whole rig. Two files, and the second one is the interesting
half: **one Adafruit Data Logger, named** ``logger``\ **, plugged into the
socket called** ``arduino_r3``. No pins, no overlay, no ``&gpiob`` anywhere
— those are the board's business and the module's business respectively,
and neither belongs in the sentence "this module is plugged in there".

The split is deliberate. ``rig.yml`` is the :term:`rig metadata file`: the
rig's identity, and nothing about hardware. ``nucleo_datalogger.yml`` is the
:term:`rig content file`: the assembly. :doc:`make-the-rig-permanent`
returns to why those are two files and not one.

Build it
----------

A rig is one thing added to an ordinary ``west build``: ``-DRIG=<name>``,
passed through to CMake after ``--``. Nothing else about the command
changes — which is also why the whole mechanism works with ``west``
absent entirely, as a bare ``cmake`` invocation: the ``-D`` is CMake's,
not west's.

.. code-block:: console

   $ west build -b nucleo_f401re/stm32f401xe/rig \
       btr-shields/samples/rigs/scenario-1 -p always -- -DRIG=nucleo_datalogger

The board comes from ``-b``, exactly as in any Zephyr build. A rig names a
topology — what is plugged where — and nothing else; it has no board of its
own to fall back to, so a rig build without a board is a configure error
that says so.

Watch for four lines in the configure output. They are the rig machinery
reporting what it decided, and every later tutorial is about changing one
of them:

.. code-block:: text

   -- Rig: nucleo_datalogger (.../boards/rigs/nucleo_datalogger/rig.yml), board: nucleo_f401re/stm32f401xe/rig
   -- Rig: expanding .../boards/rigs/nucleo_datalogger/rig.yml -> .../build/rig
   -- Rig: 'nucleo_datalogger' board=nucleo_f401re/stm32f401xe/rig shields=[adafruit_data_logger]
   -- Rig: shield 'adafruit_data_logger' <- .../boards/shields/adafruit_data_logger

Note the board: ``nucleo_f401re/stm32f401xe/rig``, not plain
``nucleo_f401re``. The ``/rig`` on the end is a board *variant* — a
:term:`board extension` that takes the real upstream NUCLEO-F401RE and adds
typed :term:`socket` nodes on top of it, without modifying the upstream
board at all. :doc:`give-a-board-a-socket` builds one of those from scratch.

Then the ordinary Zephyr build runs, and finishes ordinarily:

.. code-block:: text

   [189/189] Linking C executable zephyr/zephyr.elf
   Memory region         Used Size  Region Size  %age Used
              FLASH:       31628 B       512 KB      6.03%
                RAM:        5248 B        96 KB      5.34%

Nothing about the output is special. That is the point: a rig build is a
Zephyr build whose overlay was computed instead of written.

Read what it produced
-----------------------

The expansion wrote a directory into the build tree:

.. code-block:: console

   $ ls build/rig
   config-sheet.md  context.cmake  expectations.yml  rerun-expand.sh
   rig-gen.overlay  rigc-generated

``rig-gen.overlay`` is the devicetree overlay — the file you would
otherwise have written by hand, now derived. ``rigc-generated`` is the
:term:`expander`'s own scratch directory, kept rather than cleaned up: it
holds the devicetree fragments it fed its parsers, which is where to look
when a build fails for a reason the diagnostic alone does not settle
(:doc:`../reference/commands` describes it). Both can wait; the more
interesting one for a human is ``config-sheet.md``:

.. code-block:: text

   # Physical configuration sheet — rig `nucleo_datalogger`

   Board: **nucleo_f401re/stm32f401xe/rig**

   ## Socket assignment

   | instance | shield | socket |
   |---|---|---|
   | logger | adafruit_data_logger | arduino_r3 |

   ## Chip-selects

   - logger/sdhc: CS index 0, D10 → SoC gpiob pin 6

That is the :term:`config sheet`, and it is worth pausing on. It is not
build output for the compiler — it is **assembly instructions for the
person holding the hardware**. The last line is the tell: nobody wrote
"D10" or "gpiob pin 6" anywhere in the rig. The shield said its SD card's
chip-select sits at Arduino position D10; the board said position D10
reaches ``gpiob`` pin 6; the expander put those together.

That is the whole idea in one line of generated Markdown. The board knows
its pins. The module knows its positions. Neither knows the other, and the
rig only had to say which socket.

Next
------

:doc:`give-a-board-a-socket` starts building your own, from the board end:
a socket, on a board that does not have one yet.
