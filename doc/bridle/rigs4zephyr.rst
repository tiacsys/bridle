.. _rigs4zephyr:

Rigs for Zephyr
###############

A **rig** is a board plus the modules plugged into it, described as data
instead of as a hand-written overlay per combination.

Zephyr models an add-on board as a *shield*: a devicetree overlay naming
the board's pins directly. That works for one module on one board. It
stops working the moment you want the same module twice, on a different
connector, or on a different host board — the overlay names pins, so a
second copy needs a second overlay. Bridle carries **64 overlays for a
single Grove button** for exactly this reason.

Rigs replace that with three separated facts:

- a :term:`connector type` says what a kind of socket offers — which
  positions exist, which buses can cross it;
- a board declares its :term:`socket`\ s as real devicetree nodes, once;
- a :term:`shield template` says what a module needs, in *positions*
  rather than pins.

A rig then just says *what is plugged where*, and the :term:`expander`
computes the overlay. One shield definition plus one line per placement
replaces the 64 overlays — and an assembly that cannot physically work is
rejected at configure time, with a diagnostic that names the pin.

.. warning::

   **Under active development.** The rig model is real and builds real
   firmware today, but parts of it are still moving. Tutorials covering
   functionality that has not shipped yet say so in a warning as their
   first content — believe those warnings.

This documentation follows the `Diátaxis <https://diataxis.fr/>`_
framework, organized into four kinds of page:

- **Tutorials** — guided, hands-on lessons that build up the rig model one
  concept at a time.
- **How-to guides** — step-by-step recipes for a specific task.
- **Reference** — precise, factual descriptions of files, commands, and
  terms.
- **Explanation** — the reasoning behind why rigs are built this way.

.. toctree::
   :maxdepth: 2
   :caption: Tutorials

   rigs4zephyr/tutorials/index

.. toctree::
   :maxdepth: 2
   :caption: How-to guides

   rigs4zephyr/howto/index

.. toctree::
   :maxdepth: 2
   :caption: Reference

   rigs4zephyr/reference/index

.. toctree::
   :maxdepth: 2
   :caption: Explanation

   rigs4zephyr/explanation/index
