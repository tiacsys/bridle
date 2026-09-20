Building a rig on the fly
===========================

.. admonition:: Prerequisites

   - :doc:`write-a-shield-template` — the module this places.
   - :doc:`give-a-board-a-socket` — the board it lands on.

.. note::

   Rewritten against bridle's own ``seeeduino_lotus`` board and
   ``grove_led`` shield — see :doc:`build-a-rig-that-exists`'s own note
   for why, and how this diverges from the rest of the series.

Rae wants to see the LED blink. Not to design a bench rig, not to commit
anything — just to check the module works before building anything around
it.

**One new concept: a single module IS a rig.** A shield name is a legal
``-DRIG=`` target, and it means "one of these, plugged in the obvious
place" — *if* there is exactly one obvious place.

Build it
----------

.. code-block:: console

   $ west build -b seeeduino_lotus samples/helloshell -- -DRIG=grove_led

No rig file was written. Two things made that command necessary to think
about, and both are worth understanding because they are load-bearing
everywhere else.

The board is a separate argument
----------------------------------

``-b`` and ``-DRIG=`` are independent. That is the :term:`invocation
coordinate`: a build is *a board times a rig*, not a rig that owns a board.

It has to be that way here. A module has no board — an LED on a Grove
connector is the same module whether it is on a Lotus or anything else —
so a rig that is just a module cannot declare one, and the board must come
from the command line.

That is the same shape as Zephyr's own ``--board X --shield Y``, which is
not a coincidence: this *is* that, generalised. Upstream's ``--shield``
is the degenerate case of a rig — one anonymous module on the well-known
connector — and everything the rest of these tutorials add is what you get
by making that case non-degenerate.

The socket has to be picked — here, explicitly
--------------------------------------------------

You never said which Grove socket. On a board with exactly one socket of
the module's connector type, that is enough: the shortcut infers it, the
same way ``build-a-rig-that-exists`` describes for
:doc:`../reference/commands`'s ``--boards-for``. ``seeeduino_lotus`` is
not that board — it carries nine Grove sockets — so the plain command
above fails at configure, and the failure is worth reading once:

.. code-block:: text

   CMake Error at .../cmake/modules/dts.cmake:601 (message):
     Rig: rigc expand failed for -DRIG=grove_led (exit 1)
     ...
     --- stderr ---

     error[phys-socket]: instance 'grove_led': shield 'grove_led' plugs 'grove',
     which mates more than one socket of board 'seeeduino_lotus/samd21g18a' --
     add an explicit socket: to pick one

         candidates: grove_d2, grove_d3, grove_d4, grove_d5, grove_d6, grove_d7, grove_a0, grove_a1, grove_a2

**Exactly one** is the rule, and it is strict on purpose. Zero candidates
is an error naming the connector type the board is missing. Two or more is
also an error, listing them, and asking you to pick — never a guess,
however reasonable a tie-break might look. This is that second case, live.
:doc:`add-a-second-socket` puts a second connector of one type on a board
that starts with exactly one, and shows this same error appear where a
plain command used to resolve cleanly.

Pick one with the ``:socket=`` option, appended to the target:

.. code-block:: console

   $ west build -b seeeduino_lotus samples/helloshell -- -DRIG=grove_led:socket=grove_d2

That links clean:

.. code-block:: text

   [207/207] Linking C executable zephyr/zephyr.elf
   Memory region         Used Size  Region Size  %age Used
              FLASH:       85300 B       232 KB     35.91%
                RAM:       19712 B        32 KB     60.16%

See what it stood for
-----------------------

The shortcut is sugar, and you can always see what it desugared to:

.. code-block:: console

   $ west rigs --explain grove_led:socket=grove_d2
   # rig.yml
   rig:
     name: grove_led

   # grove_led.yml
   instances:
     - name: grove_led
       shield: grove_led
       socket: grove_d2

That is a real rig — the exact two files you would have written by hand.
Note what is *absent*: no ``board:``, because a module has none. The
``socket:`` line, by contrast, is present here — on a board where
inference alone cannot answer the question, the desugared form makes the
choice explicit rather than leaving it implicit and ambiguous.

This printout is not a convenience. It is the guarantee that the shortcut
can never outgrow the written form: the ad-hoc rig is *defined* as the
thing that desugars to those files, so anything you can build this way you
can also write down — which is what the next tutorial does with it.

Next
------

:doc:`make-the-rig-permanent` takes that output and turns it into a rig
that lives in the repository, then grows it into something the shortcut
could not express.
