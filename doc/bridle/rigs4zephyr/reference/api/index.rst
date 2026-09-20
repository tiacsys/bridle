Expander API
==============

The :term:`expander`'s own Python API, generated from the source. This is
the **internal** interface of ``scripts/rigc/`` — the surface one module
offers another, not a public library. Nothing here is a stability
promise: the only supported entry points are the commands in
:doc:`../commands`.

Read it to find out *where* something happens, or when a diagnostic sends
you into the code. The prose is each module's own docstring, so a page here
cannot fall behind the code without the code changing under it — and
``test_api_reference_drift.py`` fails the test suite if a module is added
with no page to document it.

The pipeline
--------------

One run is five stages, in this order. Each page below is one stage.

.. list-table::
   :widths: 22 78
   :header-rows: 1

   * - Stage
     - What it does
   * - :doc:`cli`
     - Parses the command line, sequences the run, decides the exit code.
       Desugars a promoted shield into the rig files the rest of the
       pipeline reads.
   * - :doc:`loader`
     - Reads the rig files and the shield library, resolves every
       reference and axis, and produces the rig model. Rejects anything
       the *files* get wrong.
   * - :doc:`board`
     - Reads the board's real devicetree — sockets, buses, controllers —
       through the preprocessor and ``edtlib``.
   * - :doc:`analyzer`
     - Decides whether the assembly is physically possible: mating,
       positions, nets, addresses, chip-selects, wires, labels. Rejects
       anything the *hardware* gets wrong.
   * - :doc:`emitter`
     - Renders the overlay, the config sheet, the expectations and the
       build glue.

:doc:`model` is not a stage: it is the vocabulary all five share.

.. toctree::
   :maxdepth: 1

   cli
   model
   loader
   board
   analyzer
   emitter

The package root
------------------

.. automodule:: rigc
