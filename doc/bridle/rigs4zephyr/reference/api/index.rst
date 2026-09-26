.. _rigs4zephyr_reference_api_index:

rigc API
==============

:term:`rigc`'s own Python API, generated from the source. This is
the **internal** interface of ``scripts/rigc/`` — the surface one module
offers another, not a public library. Nothing here is a stability
promise: the only supported entry points are the commands in
:ref:`rigs4zephyr_reference_commands`.

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
   * - :ref:`rigs4zephyr_reference_api_cli`
     - Parses the command line, sequences the run, decides the exit code.
       Desugars a promoted shield into the rig files the rest of the
       pipeline reads.
   * - :ref:`rigs4zephyr_reference_api_loader`
     - Reads the rig files and the shield library, resolves every
       reference and axis, and produces the rig model. Rejects anything
       the *files* get wrong.
   * - :ref:`rigs4zephyr_reference_api_board`
     - Reads the board's real devicetree — sockets, buses, controllers —
       through the preprocessor and ``edtlib``.
   * - :ref:`rigs4zephyr_reference_api_analyzer`
     - Decides whether the assembly is physically possible: mating,
       positions, nets, addresses, chip-selects, wires, labels. Rejects
       anything the *hardware* gets wrong.
   * - :ref:`rigs4zephyr_reference_api_emitter`
     - Renders the overlay, the config sheet, the expectations and the
       build glue.

:ref:`rigs4zephyr_reference_api_model` is not a stage: it is the vocabulary all five share.

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

Other modules
---------------

Not part of the five-stage pipeline above, but real modules under
``scripts/rigc/`` in this repository, documented here for the same
reason as everything else on this page — see :ref:`rigs4zephyr_reference_api_junit_html` for why
this one is bridle-specific.

.. toctree::
   :maxdepth: 1

   junit_html
