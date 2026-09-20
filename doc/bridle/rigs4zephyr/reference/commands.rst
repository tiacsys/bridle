Commands
==========

Two things exist for a person: building a rig, and ``west rigs``, which
answers questions about rigs without building. The :term:`expander` itself
(``rigc``) is run *by* ``cmake`` during configure, never directly by a
person — its argument list is documented here anyway, because a failing
configure prints it and ``build/rig/rerun-expand.sh`` re-runs it.

.. contents::
   :local:
   :depth: 1


Building a rig
----------------

.. code-block:: console

   $ west build -b <board> <app-source-dir> -- -DRIG=<target>

Building a rig is not a command of its own — it is an ordinary
``west build`` (or a bare ``cmake -S ... -B ...``) invocation, one flag
added. ``-DRIG=<target>`` resolves ``<target>`` — either a persisted rig,
named by its ``rig.yml`` ``rig.name`` field, or a :term:`shield template`
promoted to a rig of one instance (see `Promotion targets`_ for the
grammar) — into a devicetree overlay during configure. Every other
``west build``/cmake option works unchanged alongside it.

Two rules this acquires:

- **The board is required, and comes from** ``-b``/``--board`` (or
  ``-DBOARD=`` for a bare ``cmake`` invocation). A rig names a topology;
  no rig file declares a board, so there is nothing to fall back to and a
  rig build without a board is a configure-time error that says so.
- ``--shield`` **must not be given.** A rig's own instances are the sole
  source of shields for a rig build; the combination is a fatal configure
  error. A ``SHIELD`` still cached in a build directory from an earlier
  non-rig configure trips it too — pristine the directory (``-p always``)
  when switching one to ``-DRIG``.

The ``$ZEPHYR_BASE`` a rig build resolves against, and everything else
about the build, is whatever an ordinary ``west build``/``cmake``
invocation would already use — nothing about ``-DRIG`` changes it.


``west rigs``
---------------

.. code-block:: console

   $ west rigs [-f FORMAT] [-n NAME_RE]
   $ west rigs --boards-for TARGET
   $ west rigs --explain TARGET

With no arguments, lists the name of every rig discovered under the board
roots of every Zephyr module that declares one — ``btr-shields`` does, so
its own rigs are found with no path given.

``-f, --format FORMAT``
   A Python format string, one line per rig. Keys: ``{name}`` (the rig's
   identity), ``{dir}`` (the directory holding its two files),
   ``{revisions}`` and ``{variants}`` (declared axis values,
   comma-separated, empty when the rig declares none). Default:
   ``{name}``.

   There is no ``{board}`` key. A rig declares no board, so a listing has
   nothing of its own to print — ``--boards-for`` is the question that
   replaces it.

``-n, --name NAME_RE``
   List only rigs whose name matches this regular expression.

``--board-root DIR``
   Add a board root to the scan. Repeatable. Rarely needed: module-declared
   roots are scanned already.

``--boards-for TARGET``
   Instead of listing, print every board whose typed sockets satisfy
   ``TARGET`` — mating, bus-subset exposure, alias-aware reference
   resolution and stackability, censused from board sources with no cmake
   configure. ``TARGET`` resolves against both namespaces (a rig, or a
   :term:`promoted shield`), so *"which boards can host this module?"* is askable
   before any rig exists for it:

   .. code-block:: console

      $ west rigs --boards-for adafruit_data_logger
      frdm_k64f/mk64f12/rig
      nucleo_f401re/stm32f401xe/rig

   **This is not a promise that the rig builds on a listed board.** GPIO
   position routing, chip-select allocation, address domains and net
   analysis all need the board's real devicetree, which this census does
   not read. It answers *cannot possibly work* with certainty, and *might
   work* otherwise.

``--explain TARGET``
   Instead of listing, print the two files ``TARGET`` stands for — verbatim
   from disk for a persisted rig, or the synthesized pair a shield name
   desugars to when the target names a shield:

   .. code-block:: console

      $ west rigs --explain adafruit_data_logger
      # rig.yml
      rig:
        name: adafruit_data_logger

      # adafruit_data_logger.yml
      instances:
        - name: adafruit_data_logger
          shield: adafruit_data_logger

   Printed *as authored*: no axis is resolved into the text, so a
   variant's fragment is not folded in and a revision is not selected.
   This is the copy-paste source for turning a promoted shield into a
   checked-in rig.

``--rig TARGET``
   Accepted and **without effect** on this command. It belongs to the
   standalone resolver ``cmake`` calls, which shares its argument
   definitions with this command; use ``--explain`` to resolve a target
   here.

``--boards-for`` and ``--explain`` each short-circuit the listing, so
``-f`` and ``-n`` do not apply to them. Both exit non-zero, with a
diagnostic on stderr, on a target that does not resolve.


Promotion targets
-------------------

A ``TARGET`` — the value of ``--rig``, ``-DRIG``, ``--boards-for`` and
``--explain`` alike — is either the name of a persisted rig, or a
**promoted shield**: a shield name (optionally a ``;``-separated list of
them), each with its own optional revision and ``:``-separated
assignments (``socket=``, ``socket.<slot>=``, ``config.<label>=``,
``<device>.<prop>=``). See :doc:`promotion` for what a promotion target
means, its full grammar, what it desugars to, and which forms are
refused.

.. code-block:: console

   $ west build -b nucleo_f401re/stm32f401xe/rig <app> \
       -- -DRIG='adafruit_winc1500:config.w_irq_jmp=D2'
   $ west build -b mikroe_quail/stm32f427xx/rig <app> \
       -- -DRIG='eth_click:socket=quail_sock1;temp_click:socket=quail_sock2'

Both elements of that list name their socket because the board carries four
mikroBUS sockets: with one candidate a socket is inferred, with four it has
to be chosen. ``west rigs --boards-for`` answers the same question ahead of
a build — it lists no board at all for a bare ``eth_click``, and
``mikroe_quail/stm32f427xx/rig`` once the socket is named.


``rigc expand``
-----------------

The :term:`expander`'s own command line. ``cmake`` builds this invocation
during configure and runs it; a person runs it to reproduce a failure,
most easily through the ``rerun-expand.sh`` the build writes next to the
artifacts:

.. code-block:: console

   $ build/rig/rerun-expand.sh

It is a plain shell script holding the exact environment and argument list
of the run that produced the build directory, so it can be edited, or
re-run under a debugger.

.. code-block:: console

   $ python3 -m rigc expand <rig.yml> --out-dir DIR [options]
   $ python3 -m rigc expand --promote TARGET --out-dir DIR [options]

Exactly one of the positional ``rig.yml`` path or ``--promote`` is
required, and ``--out-dir`` always is.

.. list-table::
   :widths: 28 72
   :header-rows: 1

   * - Option
     - Meaning
   * - ``rig`` (positional)
     - Path to the rig's :term:`rig metadata file`, ``rig.yml``. The
       content file is found beside it, by the rig's name.
   * - ``--promote TARGET``
     - Expand a promoted shield instead of a rig file: the synthesized
       pair is written into this run's work directory and loaded from
       there, so nothing downstream can tell the difference. Takes the
       full target grammar above, list form included. Mutually exclusive
       with the positional.
   * - ``--out-dir DIR``
     - Where the emitted artifacts are written. Required.
   * - ``--board NAME``
     - The board, in Zephyr's ``<board>/<soc>/<variant>`` spelling. The
       only source of one. Omitted, the rig loads with an empty board,
       which every stage except the board reader accepts.
   * - ``--board-dts PATH``
     - The board's own ``.dts``, instead of discovering it by name.
   * - ``--build-info PATH``
     - Recover the preprocessor and bindings recipe from a real build's
       ``build_info.yml``, instead of naming the directories separately.
   * - ``--include-dir DIR``
     - A preprocessor ``-I`` directory. Repeatable.
   * - ``--bindings-dir DIR``
     - A devicetree bindings directory. Repeatable.
   * - ``--shield-dir DIR``
     - A shield-library root. Repeatable.
   * - ``--connector-dir DIR``
     - A :term:`connector type` root. Repeatable.
   * - ``--revision REV``
     - The selected revision axis value.
   * - ``--variant NAME``
     - The selected variant axis value.
   * - ``--verbose``, ``-v``, ``-vv``
     - Progress logging on stderr: given once for INFO, twice for DEBUG.
       Overrides ``RIGC_LOG``.

``RIGC_LOG=<level>``
   A logging level (``INFO``, ``DEBUG``, ...) for a run that cannot easily
   have a flag added to it — a cmake-driven one. ``-v``/``-vv`` win when
   both are given.

   Logging goes to the same stream diagnostics do. Enabling it changes what
   a caller comparing stderr sees, which is why it is off unless asked for.

Exit codes
~~~~~~~~~~~~

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Code
     - Meaning
   * - ``0``
     - Accepted. The artifacts below were written. Warnings may still have
       been printed.
   * - ``1``
     - The input was rejected. Every rendered diagnostic is on stderr, and
       nothing was emitted.
   * - ``2``
     - Usage error — a malformed command line, refused by the argument
       parser before any work.
   * - ``3``
     - Not implemented: a real input the expander does not handle yet,
       reported as one line rather than a traceback.


What a run writes
-------------------

Into ``--out-dir`` (``build/rig`` for a cmake-driven build):

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - File
     - Contents
   * - ``rig-gen.overlay``
     - The devicetree overlay — the whole point.
   * - ``rig-gen-includes.dtsi``
     - The headers the rig's own parameter values need the preprocessor to
       see. Written only when some parameter needs one.
   * - ``config-sheet.md``
     - The :term:`config sheet`: which module goes in which socket, which
       jumper to set, which chip-select each device ended up on.
   * - ``expectations.yml``
     - A stub naming what the assembly should look like at runtime, for a
       runtime test harness to check against.
   * - ``context.cmake``
     - The build-glue handoff: the rig's name, board and shield list, and
       every source file the run read, so cmake re-configures when one
       changes.

And one directory:

``rigc-generated``
   The expander's own work directory, and **it is kept** — on a rejected
   run and an accepted one alike. It holds what the run actually fed its
   parsers: each shield's devicetree fragment, the preprocessed form of
   each, the preprocessed board devicetree, and, for a promoted shield,
   the synthesized rig files. That is the evidence for reading a
   diagnostic that names a preprocessed file, and for answering *why does
   the overlay say that* after a build that succeeded.

   It is not durable and does not accumulate: the name is fixed, so one
   build directory holds exactly one of these, wiped at the start of the
   next run into the same place — never merged with it. It costs tens of
   kilobytes, and ``west build -p`` or deleting the build directory reclaims
   them.
