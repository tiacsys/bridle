Making the rig permanent
==========================

.. admonition:: Prerequisites

   - :doc:`write-a-shield-template` — the module.
   - :doc:`give-a-board-a-socket` — the board.
   - :doc:`build-a-rig-on-the-fly` is worth reading first for context, but
     is not required: this tutorial writes by hand what that one generates.

The shortcut got the LED blinking. It cannot do anything else: it places
exactly one module, in the one obvious socket, with no settings. The moment
Rae wants a second module — or a name they can put in CI, or a review
comment on a wiring change — the rig has to exist as a file.

**One new concept: a rig is two files, and the split between them is the
point.**

Write the two files
---------------------

.. code-block:: console

   $ mkdir -p acme-rigs/boards/rigs/acme_bench

.. code-block:: yaml

   # acme-rigs/boards/rigs/acme_bench/rig.yml
   rig:
     name: acme_bench

.. code-block:: yaml

   # acme-rigs/boards/rigs/acme_bench/acme_bench.yml
   instances:
     - name: status
       shield: acme_grove_led
       socket: grove_d2

Build it by name:

.. code-block:: console

   $ west build -b nucleo_f411re/stm32f411xe/rig \
       btr-shields/samples/rigs/scenario-1 -- -DRIG=acme_bench

.. note::

   If you followed :doc:`build-a-rig-on-the-fly`, you can generate exactly
   this pair instead of typing it, and then edit it:

   .. code-block:: console

      $ west rigs --explain acme_grove_led

   Promotion is a copy-paste away from a checked-in rig on purpose — the
   quick path feeds the durable one rather than competing with it.

Why two files
---------------

``rig.yml`` is the :term:`rig metadata file`. It answers *which rig is
this*: the name, and the revision/variant axes it declares. It contains
no hardware description whatsoever — not even a board.

``acme_bench.yml`` is the :term:`rig content file`. It answers *what is
assembled*: instances, and later wires and parameters.

The reason they are separate is that they answer questions at different
times. The build system must know which rig you named, and where its
files are, **before** it can read any hardware description — that is how
``-DRIG=acme_bench`` turns into a directory. Content that cannot be read
that early has no business being in the file that is.

Neither file names a board, and that is the second half of the split.
Look at what the content file says: one LED module, in a Grove socket.
Nothing in that sentence is about a NUCLEO. The same two files describe
the same assembly on any board with a Grove socket, and which board it is
today is the invocation's answer — the same ``-b`` you already passed
above, and the only place a board is ever named:

.. code-block:: console

   $ west build -b nucleo_f411re/stm32f411xe/rig \
       btr-shields/samples/rigs/scenario-1 -- -DRIG=acme_bench

Point ``-b`` at another board carrying a Grove socket and the same two
files build there, with no edit in between — because the board was never
in the rig to begin with.

Three things you could not have before
----------------------------------------

**A name.** ``acme_bench`` is now a thing CI can build, a colleague can
review, and ``west rigs`` can list. Check:

.. code-block:: console

   $ west rigs
   acme_bench
   ard_datalogger
   ...

**A named instance.** The shortcut had to call the instance after the
shield; you called it ``status``. That name is not decoration — it appears
in the :term:`config sheet`, and it is how a second instance of the same
module stays distinguishable from the first.

**Room to grow.** ``instances:`` is a list. Add a second entry and you have
two modules; that is the whole change, and it is what the next tutorial
does.

Read the sheet again
----------------------

.. code-block:: console

   $ cat build/rig/config-sheet.md

.. code-block:: text

   # Physical configuration sheet — rig `acme_bench`

   Board: **nucleo_f411re/stm32f411xe/rig**

   ## Socket assignment

   | instance | shield | socket |
   |---|---|---|
   | status | acme_grove_led | grove_d2 |

One row now. It is the same document that told Rae which Arduino pin the
data logger's chip-select landed on in :doc:`build-a-rig-that-exists`, and
it grows a row per module — which is exactly what you want in your hand
when you are the one plugging the connectors in.

Next
------

:doc:`add-a-second-socket` puts a second Grove connector on the board and a
second module in the rig — and makes the socket inference you relied on
earlier start refusing to guess.
