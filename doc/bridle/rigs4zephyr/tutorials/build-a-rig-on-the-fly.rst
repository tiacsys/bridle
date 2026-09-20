Building a rig on the fly
===========================

.. admonition:: Prerequisites

   - :doc:`write-a-shield-template` — the module this places.
   - :doc:`give-a-board-a-socket` — the board it lands on.

Rae wants to see the LED blink. Not to design a bench rig, not to commit
anything — just to check the module works before building anything around
it.

**One new concept: a single module IS a rig.** A shield name is a legal
``-DRIG=`` target, and it means "one of these, plugged in the obvious
place".

Build it
----------

.. code-block:: console

   $ west build -b nucleo_f411re/stm32f411xe/rig \
       btr-shields/samples/rigs/scenario-1 -- -DRIG=acme_grove_led

No rig file was written. Two things made that work, and both are worth
understanding because they are load-bearing everywhere else.

The board is a separate argument
----------------------------------

``-b`` and ``-DRIG=`` are independent. That is the :term:`invocation
coordinate`: a build is *a board times a rig*, not a rig that owns a board.

It has to be that way here. A module has no board — an LED on a Grove
connector is the same module whether it is on a NUCLEO or anything else —
so a rig that is just a module cannot declare one, and the board must come
from the command line.

That is the same shape as Zephyr's own ``--board X --shield Y``, which is
not a coincidence: this *is* that, generalised. Upstream's ``--shield``
is the degenerate case of a rig — one anonymous module on the well-known
connector — and everything the rest of these tutorials add is what you get
by making that case non-degenerate.

The socket was inferred
-------------------------

You never said ``grove_d2``. You did not have to: the module plugs
``grove``, and your board has exactly one Grove socket, so there is exactly
one place it can go.

**Exactly one** is the rule, and it is strict on purpose. Zero candidates
is an error naming the connector type the board is missing. Two or more is
also an error, listing them, and asking you to pick — never a guess,
however reasonable a tie-break might look. :doc:`add-a-second-socket`
puts a second Grove connector on the board, and this command starts
refusing to choose.

See what it stood for
-----------------------

The shortcut is sugar, and you can always see what it desugared to:

.. code-block:: console

   $ west rigs --explain acme_grove_led
   # rig.yml
   rig:
     name: acme_grove_led

   # acme_grove_led.yml
   instances:
     - name: acme_grove_led
       shield: acme_grove_led

That is a real rig — the exact two files you would have written by hand.
Note what is *absent*: no ``board:``, because a module has none; no
``socket:``, because inference answers it.

This printout is not a convenience. It is the guarantee that the shortcut
can never outgrow the written form: the ad-hoc rig is *defined* as the
thing that desugars to those files, so anything you can build this way you
can also write down — which is what the next tutorial does with it.

Next
------

:doc:`make-the-rig-permanent` takes that output and turns it into a rig
that lives in the repository, then grows it into something the shortcut
could not express.
