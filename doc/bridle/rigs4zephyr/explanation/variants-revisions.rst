.. _rigs4zephyr_explanation_variants-revisions:

Why variants and revisions work this way
==========================================

:ref:`rigs4zephyr_reference_rig-file` lists the keys a :term:`rig` declares, the
fragment files it may carry and the order they apply in. This page covers
why they are shaped that way. Most of the rules follow from two
commitments: a rig uses the same conventions a Zephyr board already uses,
so a reader who knows hwmv2 can guess what a rig does; and a wrong
selection or a misnamed fragment must produce an error, never a build
that silently leaves the fragment out.

.. contents::
   :local:
   :depth: 1


Two files, because metadata and content are different things
-----------------------------------------------------------------

Zephyr names its files by one rule. A **metadata** file is named after the
entity's *type*: every board folder has a ``board.yml``, every shield
folder a ``shield.yml``. A **content** file is named after the entity's
*instance* and its qualifiers: ``<board>.dts``, ``<board>_<variant>.dts``,
``<board>_defconfig``. Metadata says what the entity is called and which
qualifiers it offers. It contains no hardware description at all.

A rig follows the same rule, so it has two files. The
:term:`rig metadata file` is ``rig.yml``, the same filename in every rig
folder, and holds the name and the qualifier axes. The
:term:`rig content file` is ``<name>.yml`` and holds the
:term:`instance`\ s and wires. The content file plays the part of
``<board>.dts``: it is the input the generator reads.

Both files are YAML, but keeping them apart still matters in three ways:

- **Discovery stays cheap.** ``west rigs`` walks ``boards/rigs/`` and
  treats any folder that has a ``rig.yml`` as a rig. It reads only that
  file, never the assembly, in the same way Zephyr's board listing reads
  ``board.yml`` without touching a devicetree.
- **The deltas have a base with the same stem.** A variant fragment
  ``<name>_<variant>.yml`` sits next to ``<name>.yml``, just as
  ``<board>_<variant>.dts`` sits next to ``<board>.dts``. If the base
  content lived in ``rig.yml``, every delta would be a delta of a file
  with a different name.
- **The name is constructed, not found.** ``rigc`` builds the content
  file name from the rig's own ``name:``. It never takes the name from
  the folder the file happens to be in. A missing content file is
  refused with the path ``rigc`` expected, before anything else about the
  rig is read.

The board belongs in neither file. It is the other half of the
:term:`invocation coordinate`, so a rig's files describe a topology that
any board with matching sockets can satisfy.


Variants and revisions are deltas over one base
---------------------------------------------------

A **variant** is one of several parallel alternatives: the same
assembly with a different sensor, or with one module fewer. Variants
have no order. A **revision** is a step in an evolution: rev 2 replaced
the sensor. Revisions are ordered. The two axes mean different things
but use one mechanism. Each selected value may add a delta to the base
content, and the loader applies the deltas in a fixed order: base, then
the variant, then the revision.

The base content *is* the declared default. That is why the default
value of an axis needs no fragment, while a selected non-default value
that contributes no file at all is an error. An axis value that changes
nothing is almost always a typo or a missing file, and failing loudly
beats building the base rig under a name that claims otherwise.

The analyzer and the emitter never see any of this. All deltas are
resolved in the loader, so what reaches the later stages is an ordinary
rig, and the same physical checks apply to every variant and revision
without any special code.

**The invariant holds after every stage, not only at the end.** After the
base and after each delta, the parameter rules must hold over the whole
effective topology: every ``params:`` entry names a declared parameter,
and every required parameter has a value. Deltas never add parameters
themselves. A :term:`shield template` declares them and a rig assigns
them, so the set of parameters only changes when a shield changes. That
can come from a delta that swaps an instance's shield, or from a shield
revision that authors a new required parameter. Checking after every
stage covers both cases with one rule, and an error found in the middle
of the chain points at the stage that caused it rather than at the end
result.


Filenames are constructed, never parsed
-------------------------------------------

Every fragment name joins the rig's name and the selected axis values
with ``_``, the same way the Zephyr build derives
``<board>_<soc>_<variant>.dts``. ``rigc`` never reads a filename and
works out which axes it stands for. That matters because ``_`` is also a
legal character inside a name, so parsing ``datalogger_rev_a_2.yml`` back
into its parts would be ambiguous.

Constructing names removes that ambiguity, but it leaves one hazard: two
*different* selections can build the *same* name. A variant called
``variant_a_2`` and the pair (variant ``variant_a``, revision ``2``) both
build ``<name>_variant_a_2``. ``rigc`` therefore enumerates every stem
the declared axes could build (each axis on its own and every combined
pair) and refuses a rig in which any two collide, before any fragment is
read. The bridle test fixture ``combined-fragment-collision`` shows
exactly that case:

.. code-block:: none

   error[lang-variant]: rig 'combined-fragment-collision': variant 'variant_a_2'
   and variant 'variant_a' + revision '2' all construct the same fragment stem
   'combined-fragment-collision_variant_a_2' -- the constructed filenames would
   be ambiguous about which selection a fragment belongs to

Two further rules are copied from Zephyr's own ``zephyr_build_string()``
rather than chosen:

- **A revision is normalized, a variant is not.** A dotted revision id
  becomes underscores in the filename (``1.2`` becomes ``1_2``), exactly
  as ``nrf9160dk_nrf9160_ns_0_14_0.overlay`` spells revision ``0.14.0``.
  Variant names are used as written.
- **The revision comes last in a filename.** A combined fragment is
  ``<name>_<variant>_<rev>``. In the selection syntax the revision comes
  first (``-DRIG=<name>@<rev>/<variant>``, like ``-b <board>@<rev>/<soc>``),
  but Zephyr's own filenames do not follow that order: they run board,
  then qualifiers, then revision. A rig uses Zephyr's filename order, so
  a rig fragment and a board fragment are spelled the same way.


A delta replaces; it never merges
-------------------------------------

A delta item that names an existing instance replaces each top-level
key it gives and leaves every other key as it was. Nothing merges below
that level. This is most visible for ``params:``, where a delta that
supplies ``params:`` replaces the instance's whole parameter map.

This is required by the most common reason for a delta: swapping an
instance's shield. The old assignments are keyed to the *old* shield's
devices, so merging them into the new shield would report errors against
a delta that is correct. For the same reason, a shield change always
clears ``params:``.

Replacing the whole map has one narrow hazard. Suppose the shield stays
the same, the base assigned an *optional* parameter, and the delta
restates ``params:`` without it. A plain replace would drop that value
and revert it to the shield's default without any message. ``rigc``
closes that hole with a check rather than a special merge rule: a delta
that supplies ``params:`` without changing the shield must restate every
property already assigned (the fixture ``restate-check`` exercises this).
The merge behaviour stays the same everywhere, and only the check looks
at context. A deep merge would also need a separate "remove this
parameter" operation, which the check makes unnecessary.

The same reasoning explains the other operations. Additions are never
implicit: ``instances:`` may only patch an instance that exists, and
``add-instances:`` may only add one that does not. A wire has no
identity beyond its two endpoints, so re-routing one is a remove followed
by an add. When a revision removes an instance that a variant already
removed, the error names that variant, so this kind of drift between
fragments cannot go unnoticed.


Why a delta error is ``lang-*``, not ``phys-*``
---------------------------------------------------

A delta that names a missing instance, or leaves a required parameter
without a value, describes a *wrong document*, not wrong hardware. So it
gets a ``lang-*`` code: ``lang-variant`` or ``lang-rev`` for the stage it
came from, and ``lang-param`` for the parameter rules. The messages
still use physical language ("revision '2': remove-instances: names
'logger', which does not exist (variant 'b' already removed it)"),
because that is the question the author is asking. The code, however,
follows the line :ref:`rigs4zephyr_explanation_architecture` draws between
files and copper. Physical impossibilities still happen, but only after
resolution, against the resolved topology, under the ``phys-*`` codes
they would carry in any rig (see :ref:`rigs4zephyr_reference_diagnostics`).


Rig revisions are hwmv2 revisions; shield revisions keep the older shape
----------------------------------------------------------------------------

A rig's ``revision:`` block is ``board.yml``'s block copied key for key:
``format:``, ``default:``, ``exact:``, and a ``revisions:`` list of
``{name:}`` entries. ``rigc`` also copies the behaviour: ids are
validated per format, a short ``major.minor.patch`` request is padded
with zeros, and a request for an undeclared revision resolves down to
the nearest lower declared one unless ``exact: true`` is set. The shape
is copied exactly, not approximately, because the obvious way to review
this schema is to compare it with ``board-schema.yaml``, and each
unnecessary difference is one more thing to explain. The ids have to be
quoted strings: YAML reads an unquoted ``2`` as an integer, not as the id
``"2"``, and ``rigc`` refuses it rather than convert it back to text.

``format: custom`` is valid YAML and is accepted when the file is parsed,
but it is refused as soon as the axis is actually used. In Zephyr,
``custom`` means the board provides its own ``revision.cmake``, which
resolves the revision inside cmake. ``rigc`` resolves revisions in
Python, so supporting ``custom`` would mean running arbitrary cmake from
a rig folder to feed a Python resolver. The parity is therefore
behavioural parity for ``letter``, ``number`` and ``major.minor.patch``,
not full parity.

A shield's ``revisions:`` block in ``shield.yml`` keeps the earlier
``{default:, list: []}`` shape with bare ids, and a shield revision must
match a declared id exactly. This is a constraint from outside ``rigc``:
the pinned Zephyr tree's own ``shield-schema.yaml`` allows only those two
keys, and Zephyr validates every ``shield.yml`` in every board root on
every configure. A ``format:`` key on any shield would break every build
in the workspace. The resolver chooses its behaviour from the
declaration itself ("does this axis have a format?"), not from whether
the owner is a rig or a shield, so when that schema changes, no resolver
code has to change.

A shield revision also needs no delta vocabulary. A shield is already
devicetree, so ``<name>_<rev>.shield`` is included after
``<name>.shield`` in the same translation unit, and devicetree's own
overlay-by-label rules do the merging. An instance selects the revision
with ``shield: <name>@<rev>``, the same ``@`` syntax a board or rig
uses.


Derive from the resolved form, never the raw one
----------------------------------------------------

A selection exists in two forms: what was *requested* and what it
*resolved* to. On a ``major.minor.patch`` axis that declares ``1.0.0``
and ``2.0.0``, ``@1`` is padded to ``1.0.0``, ``@1.5`` is padded to
``1.5.0`` and then resolves down to ``1.0.0``, and a bare
``-DRIG=<name>`` resolves to the declared defaults. ``-DRIG`` itself
carries the whole ``<name>@<rev>/<variant>`` string. Every name built from
a selection uses the resolved form: fragment stems, the shield
``.shield``/``.conf`` revision files, the shield library's cache key, the
default-value exemption of the contributes-nothing check, and the values
in ``context.cmake``.

This rule gets its own section because breaking it causes a silent
failure, not an error. All fragments are optional. A name built from the
raw ``-DRIG`` string, or from the requested ``1.5`` rather than the
resolved ``1.0.0``, points at a file that does not exist, and a missing
optional fragment is simply skipped. The build succeeds without the
fragment, and nothing reports it. So ``rigc`` keeps both forms: the
resolved one builds names, and the requested one is kept for
provenance only (``RIG_REVISION_REQUESTED`` is emitted only when the two
differ).

.. note::

   Nearest-lower matching and zero-padding are implemented by ``rigc``
   itself. In a ``west build``, the configure step first resolves
   ``-DRIG=`` with a lighter resolver that accepts only a declared
   revision spelled exactly as declared. So in a ``west build``,
   requesting an undeclared revision is refused before ``rigc`` runs.


Known limitation: no per-variant revision streams
-----------------------------------------------------

A rig has one revision stream for all its variants. Its revision delta
``<name>_<rev>.yml`` applies after *whichever* variant was selected.
This works as long as instance names stay the same across variants. It
stops working when a revision has to re-parametrize an instance whose
shield a variant has replaced. The device labels and property names
belong to the shield, so under one variant the delta must name one
device and under another variant a different one, and a single fragment
cannot do both.

``rigc`` does not guess in that case; it refuses. When a revision's
``params:`` names a device that the post-variant shield lacks, the error
names the variant that changed the shield. The bridle fixture
``revision-crosses-variant`` is exactly this shape (three files, trimmed
to the relevant lines):

.. code-block:: yaml

   # revision-crosses-variant.yml -- the base
   instances:
     - name: sensor_1
       shield: restate_fixture
       params:
         rf_sensor:
           vnd,threshold: 20

   # revision-crosses-variant_hpm.yml -- variant 'hpm' swaps the shield
   instances:
     - name: sensor_1
       shield: pilot_alt_button
       params:
         pab_key:
           zephyr,code: 9

   # revision-crosses-variant_2.yml -- revision '2', for every variant
   instances:
     - name: sensor_1
       params:
         rf_sensor:
           vnd,threshold: 30

.. code-block:: none

   error[lang-param]: instance 'sensor_1': params names no device 'rf_sensor'
   of shield 'pilot_alt_button' (this instance's shield is 'pilot_alt_button'
   because of variant 'hpm')

The fix would be a revision stream per variant, meaning a combined
``<name>_<variant>_<rev>.yml`` content delta. ``rigc`` does not read one
today. The combined stem already exists for the build's own
``<name>_<variant>_<rev>.overlay`` and ``_defconfig`` fragments, and the
collision check above already reserves it. A rig that needs different
revision content per variant models each combination as a variant of its
own instead.


.. seealso::

   :ref:`rigs4zephyr_reference_rig-file`
      The declaration grammar, the fragment names and the five delta
      operations.

   :ref:`rigs4zephyr_reference_diagnostics`
      ``lang-rev``, ``lang-variant`` and ``lang-param`` in full.

   :ref:`rigs4zephyr_explanation_architecture`
      Why the pipeline is split between file errors and hardware errors.
