.. _rigs4zephyr_explanation_testing:

Why rigc's test suite is shaped this way
==========================================

:term:`rigc` carries its own gate, ``scripts/rigc/check.sh``:
mypy over the package, the unit suite under coverage, then the
integration suite. The suite itself lives in ``scripts/rigc/tests/``,
split into ``unit/`` and ``integration/``, with the committed goldens in
``goldens/`` and every input they read in ``fixtures/``. This page
explains the rules that shape it: where the line between the two layers
sits, which outputs are compared byte for byte and which by contract, and
why a green run alone does not prove a check works. It is written for
contributors who are changing or debugging ``rigc``. It builds on
:ref:`rigs4zephyr_explanation_architecture`, which explains why the
output is deterministic, and does not repeat that argument.

Two layers, cut at the subprocess
------------------------------------

**A unit test runs no subprocess.** A test that reaches ``rigc`` through
its front door, ``python -m rigc expand``, tests the whole pipeline,
whatever its file is called. So the line between the layers is drawn
where the process boundary falls, not by speed or by how much a test
checks. ``tests/unit/test_layer_discipline.py`` enforces this by reading
the syntax tree of every module in ``tests/unit/`` and failing on any
import of ``subprocess``. There the directory is the classification, so
the same test also bans pytest markers under ``tests/unit/``.

**A reject is never a unit concern.** A reject is the tool's verdict on
a whole scenario: a :term:`rig`, the :term:`shield template` library and
a board, taken together. No single unit's specification says "this
assembly cannot be built", so no unit test can own that claim. Rejects
live in ``tests/integration/``. The unit layer covers something
different: the value-shaped rules each stage is built from, such as how a
chip-select position is picked from a pool, how addresses are allocated,
or how an anchor path is rendered.

**Hermetic describes cost, not the unit boundary.** The reject goldens
in ``tests/integration/test_emitted_rejects.py`` read nothing but
``tests/fixtures/``. They need no real board, no production bindings and
no build, yet they are integration tests, because they drive the CLI as
a subprocess and each one pins a system verdict. Hermetic means that no
Zephyr *data* leaks in. ``ZEPHYR_BASE`` can still be set, because it is
how the suite finds the devicetree Python package. That is why the check
is structural: ``assert_fixture_local()`` looks at the paths a test
actually passes to the code under test, instead of looking for a missing
environment variable. The same reasoning keeps every ``ZEPHYR_BASE``
lookup inside a function. pytest imports every module before it
deselects anything, so a lookup at module scope would break collection
for runs that never use it. ``test_layer_discipline.py`` guards that
too.

**Unit test modules are named after their unit.** ``test_<module>.py``
tests ``<module>.py``. When one unit needs several test modules, they sit
in ``tests/unit/<unit>/``, as ``tests/unit/analyzer/`` and
``tests/unit/loader/`` do. A reviewer can then find the tests for a piece
of code by its name. The design story lives inside each module, in its
docstrings, section headers and test names, so "where is ``cs-gpios``
worked out?" is answered by a section of the tests. The layer-discipline
test rejects any unit module whose name does not match a module or
sub-package of ``rigc``.

**Only stable contracts get a unit test.** The question to ask is: would
you keep this contract if the implementation were rewritten? Revision
normalization, position indices, build recipes, controller identity, and
chip-select and address allocation all pass. The shape of a rejection
branch, the way a delta key is dispatched, and the wording of a
diagnostic do not: a rewrite could reasonably change any of them. Pinning
them in a unit test would churn with every refactor and protect nothing a
user relies on.

**Diagnostic wording is pinned only by the goldens.**
``tests/unit/test_diag.py`` checks the format of a rendered diagnostic
(the ``severity[code]: head`` line, the four-space continuation lines,
the order and de-duplication of anchors) using made-up content. Unit
tests elsewhere check a diagnostic's code and the facts it carries, such
as which instance or which socket it names. The full sentence a rig
author reads belongs to the golden that freezes it.

Byte-exact where the user reads, by contract everywhere else
---------------------------------------------------------------

Each golden case is a directory ``tests/goldens/<case>/`` holding
``exit_code`` and ``stderr.txt``. Both are compared byte for byte, and
that is permanent, not a placeholder until a looser comparator is
written. The rendered diagnostics and the exit status are the tool's
product surface: rig authors read the text, and CI scripts branch on the
code. The only rewriting before comparison is done by ``normalize()`` in
``tests/integration/harness.py``. It replaces machine-specific absolute
paths (the run's ``rigc-generated`` work directory, ``ZEPHYR_BASE``, the
repository root and the west top directory) with placeholders. Anchor
paths need no replacement: ``diag.anchor_path()`` renders a path under a
``scripts/<module>/`` component relative to that component, so a fixture
anchor reads the same on every machine:

.. code-block:: none

   error[lang-variant]: rig 'no-such-axis' names a variant ('anything'), but this rig declares no variants: at all
       at tests/fixtures/boards/rigs/no-such-axis/rig.yml:7 (rig)

A byte-exact stderr golden also makes **source line numbers part of the
contract**. An edit that shifts a line in a fixture moves every anchor
that points past it. "No behavior change" therefore does not mean "no
golden change". It means every golden change can be explained as a line
shift.

The other artifacts are compared against what their consumers actually
rely on. ``tests/compare.py`` holds those comparators. They are pure
functions over text, and ``freeze_or_assert()`` in the harness picks one
by artifact filename:

- ``context.cmake`` is compared as the key-to-value mapping that
  ``cmake/modules/dts.cmake`` includes. ``RIG_DEPENDS`` is compared as a
  set, because cmake only consumes it as a dependency set. ``RIG_SHIELDS``
  stays an ordered list, because it is iterated in rig order.
- The :term:`config sheet` is compared as the facts a person relies on:
  instance, socket, address, chip-select index, strap state and so on,
  never the prose. Sections are compared as a set, and the rows inside a
  section as an ordered list, because the emitter sorts them and a
  reordering is a real regression. Every non-blank line must be consumed
  by exactly one extractor, and at most one prose paragraph may sit
  between a heading and its first row. Otherwise an extractor that
  silently stopped matching would drop facts and still report a match.
- ``rig-gen-includes.dtsi`` is compared as an ordered list of headers,
  because include order can matter to cpp.
- ``rig-gen.overlay`` is not a parseable devicetree: it holds unresolved
  ``#include`` lines, macros and label references. ``compare_overlay()``
  checks only the facts that disappear once it is resolved: parameter
  macro tokens, the opening quoted ``#include``, and the comments meant
  for people. Its full meaning is designed to be checked by comparing the
  resolved ``zephyr.dts`` structurally.

**Current state in bridle:** every committed golden is a reject. The
accepted cases in ``tests/integration/``, such as reference shields,
carriers and three-cell PWM, check what they emit with targeted
assertions in their own modules, not with frozen artifacts. The
comparators above are wired into ``freeze_or_assert()`` and fully
unit-tested, but no golden in the tree exercises them yet. The gate
also has **no build tier**. No test runs a west or cmake configure, no
resolved ``zephyr.dts`` is compared, and the ``build`` marker declared in
``pyproject.toml`` is carried by no test, so ``CHECK_FAST=1`` deselects
nothing.

Coverage is measured over the unit layer only
------------------------------------------------

``check.sh`` runs the unit suite under ``coverage run`` and the
integration suite as a separate pytest invocation, and the two must stay
separate. The integration suite drives ``rigc`` as a subprocess, and
``coverage`` cannot see inside a subprocess. Merging the runs would not
raise the figure. It would only water it down with work that is never
measured. The floor is ``fail_under = 88`` under
``[tool.coverage.report]`` in ``scripts/rigc/pyproject.toml``. It is a
floor, not a target: it only ever moves up. Its purpose is to catch new
untested code in the unit layer, not to suggest the integration suite is
covered.

A check is proven by breaking it
-----------------------------------

A passing check proves only that it accepts correct output. It says
nothing about whether it rejects wrong output. For the comparators, the
integration suite can never show that: the emitter's output matches the
goldens, so a correct comparator, a weakened one and one gutted to
``return None`` all pass it equally. Three rules follow.

**Every comparator guard has a negative control that has been
mutation-tested.** ``tests/unit/test_compare.py`` consists mostly of
deliberate mutations that a comparator must still reject: altered
values and, above all, omissions such as a dropped section, row or
bullet, because silently dropped content is what a fact extractor tends
to miss. This file, not the integration suite, is what stops a
refactored comparator from going quietly green. The config-sheet cases
that no golden covers are produced by running the real ``render_sheet()``
on synthetic input, so those fixtures cannot drift away from what the
emitter really produces.

**A control is run, not reasoned about.** A mutation is proven by making
the change, watching the named test fail for the named reason, and
restoring the code. A test can pass for the wrong reason. For example,
every reject fixture exits non-zero, often for an unrelated later
reason, so ``returncode != 0`` on its own discriminates almost nothing.
The stderr assertion and the golden are what actually tell cases apart,
and only a mutation shows which assertion is carrying the weight.

**A negative control's expectation comes from outside the code under
test.** ``test_the_build_helper_set_is_exactly_the_known_launchers`` in
``test_layer_discipline.py`` spells out its expected names rather than
iterating the production set: a control that loops over the set it
guards gets smaller along with that set and keeps passing.

Refreezing is a review, not a reset
--------------------------------------

With ``RIGC_REFREEZE=1`` set, ``freeze_or_assert()`` writes the golden
instead of comparing against it, and ``assert_absent_or_refreeze()``
deletes a golden for an artifact the run no longer produces. Outside a
refreeze, a golden with no matching output is itself a failure. A
refreeze only produces a diff, and the diff is what gets reviewed. Every
changed line in ``git diff scripts/rigc/tests/goldens`` must be put in
one of two groups: an intended, understood behavior change (including a
line shift you can explain), or an unintended regression. Unrelated drift
must not be carried along with an otherwise correct change.

The same classification applies when a Zephyr update, with no local
change, moves a golden that reflects a board's devicetree. That is how
upstream churn is expected to look, not a defect in itself. If every node
that moved belongs to the SoC or the board, refreeze. If a node the rig
owns moved (a socket, a shield device, an instance, or anything
``rigc`` generates), treat it as a regression.

Logs describe execution, diagnostics describe input
------------------------------------------------------

``rigc`` uses the standard ``logging`` module, with one logger per module
under the ``rigc`` tree. Log records describe what the *tool* did:
lifecycle milestones at INFO, and per-item decisions and the exact cpp
argv at DEBUG. Diagnostics describe what is wrong with the *user's
input*. A finding about the rig, the shield or the board is always a
diagnostic, never a log warning.

The two share stderr, so stderr stays pure unless you ask otherwise. The
package root logger has only a ``NullHandler``, which also stops Python's
``lastResort`` handler from printing warnings. A real handler is attached
only when ``RIGC_LOG=<level>`` or ``-v``/``-vv`` is given (see
:ref:`rigs4zephyr_reference_commands`). Turning logging on during a run
that compares goldens breaks every stderr golden, and that is intended.
``tests/unit/test_cli.py`` checks both sides without a subprocess: with
``RIGC_LOG`` unset, a rejecting run puts only rendered diagnostics on
stderr while ``caplog`` confirms records were emitted. Every unit test
also sees the ``rigc`` tree at DEBUG through ``caplog``, because
``tests/unit/conftest.py`` sets that up automatically.

Drift guards hold the documentation to the code
--------------------------------------------------

Three integration tests compare pages of this documentation with the
code, in both directions:

- ``test_api_reference_drift.py``: every production module under
  ``scripts/rigc/`` has exactly one page in
  :ref:`rigs4zephyr_reference_api_index`, and every page names a module
  that exists.
- ``test_cli_reference_drift.py``: every long option the real parsers
  declare has its own entry in :ref:`rigs4zephyr_reference_commands`, and
  every ``--option`` on that page is real.
- ``test_diagnostics_reference_drift.py``: every ``lang-*`` and
  ``phys-*`` code passed to ``diag.error()`` or ``diag.warning()`` in
  production source has an entry in
  :ref:`rigs4zephyr_reference_diagnostics`, and every entry is raised
  somewhere.

They exist because no other check catches these failures. A new module or
a new diagnostic code usually arrives in a change that never touches
``doc/``, and the docs build is a separate gate that someone running only
the test suite never sees. Each guard is a text scan with no build, so it
runs on every gate. Like any other guard, each one has a control showing
it can fail. The CLI guard, for example, fails if its scan finds almost
no ``west`` mentions, so it cannot pass just because the regex matched
nothing.

Practical facts for working on the suite
-------------------------------------------

- Integration modules import shared plumbing from ``harness``
  (``from harness import ...``), never from ``conftest``.
  ``tests/integration/conftest.py`` only re-exports ``harness``, because
  pytest needs a file with that name there. Importing ``conftest`` by
  name is unsafe, because ``sys.modules["conftest"]`` holds whichever
  ``conftest`` module was imported first.
- ``check.sh`` needs ``ZEPHYR_BASE`` and takes ``PYTHON=`` to choose the
  interpreter. It stops at the first stage that fails, so if the unit
  stage fails, the integration stage never runs. It does not run ruff:
  the repository's own ``.ruff.toml`` governs ``scripts/rigc/`` like any
  other tree.
- When you pipe the gate, the exit status you see is the last command's.
  ``check.sh | tail; echo $?`` reports what ``tail`` returned, and hides
  both a failure and the stages that never ran. Make the gate the last
  command in the pipeline, or capture ``$?`` straight away.
- ``pyproject.toml`` sets ``testpaths`` to ``tests/integration``, so a
  bare ``pytest -c pyproject.toml`` runs only the integration layer. Pass
  ``tests/unit`` explicitly to run the unit layer.
- Every ``run_expand()`` call writes a ``rerun.sh`` next to its output
  before the subprocess starts. The script replays that exact invocation,
  and it survives a failing test because pytest keeps a failed test's
  ``tmp_path``. Set ``RIGC_SUBPROCESS_TIMEOUT=0`` while stepping through
  that child in a debugger, or the timeout will kill it.
- When you mutate a file and restore it, copy it aside first and hash it
  before you mutate. An untracked file has no ``git checkout`` safety
  net. Then delete ``__pycache__``: a restore within the same second
  that keeps the file size leaves bytecode that Python still trusts,
  and the gate then runs the mutated code.
