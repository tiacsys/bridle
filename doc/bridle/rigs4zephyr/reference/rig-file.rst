Rig files
==========

What a rig *is*, on disk: two files, ``boards/rigs/<name>/rig.yml`` (the
:term:`rig metadata file`) and ``boards/rigs/<name>/<name>.yml`` (the
:term:`rig content file`), plus the optional qualifier-delta fragments
that layer onto the content file. The authority is the loader itself —
``scripts/rigc/loader/documents.py``, ``axes.py``, ``delta.py`` and
``params.py`` — and every key below is read (or deliberately never read)
exactly as that code does today.

This page is reference, not narrative — :doc:`../tutorials/build-a-rig-that-exists`
and :doc:`../tutorials/make-the-rig-permanent` teach the concept; this page
looks up the facts. A shield can also become a rig of one instance without
either file existing at all — see :doc:`promotion`.

.. contents::
   :local:
   :depth: 1


The two files
---------------

Metadata files are named after the entity *type* — ``rig.yml``, the same
filename in every rig's folder, the same way ``board.yml`` and
``shield.yml`` are. Content files are named after the entity *instance*:
``<name>.yml``, constructed from the rig's own ``name:``, never read back
from the folder it happens to live in.

``rig.yml``
   The rig's identity and its qualifier axes. Carries **no hardware
   description whatsoever** — not an instance, not a wire, not a board.

``<name>.yml``
   The assembly: instances, and any wires between them. Required — a rig
   with no content file is refused (``lang-content``, naming the expected
   path) before anything else about it is read.

Both are parsed by the same mark-aware YAML reader
(``loader/documents.py``), with no ``rig:`` wrapper on the content side —
only ``rig.yml`` nests its keys under a top-level ``rig:`` mapping.


``rig.yml`` — metadata
-------------------------

.. code-block:: yaml

   rig:
     name: <string>                        # required

     revision:                             # optional
       format: letter | number | major.minor.patch | custom
       default: "<id>"                     # optional
       exact: true | false                 # optional, default false
       revisions:
         - name: "<id>"

     variants:                             # optional
       default: <name>                     # optional
       list:
         - <name>                          # or {name: <name>}

``rig: name:``
   The rig's identity — its ``rig.yml`` ``name:`` field, not its folder
   name (the two conventionally match; nothing enforces it). Required; a
   missing ``rig:`` block or a missing ``name:`` inside it stops the load
   before anything else is read.

``rig: revision:``
   The rig's own revision axis, in **upstream's hwmv2 shape**
   (``board.yml``'s own block, copied key for key) — the singular key
   ``revision:``, not the plural ``revisions:`` a shield's own axis uses
   (see :doc:`shield-template`). ``format:`` is required whenever this
   block is present, one of ``letter`` (a single uppercase letter),
   ``number`` (digits only), ``major.minor.patch`` (three dot-separated
   non-negative integers) or ``custom`` — declaring ``custom`` is legal
   YAML but rejected the moment the axis is actually resolved (rigc
   implements the first three formats only). Every declared id in
   ``revisions:`` must be a **quoted string** matching the declared
   format — an unquoted numeric-looking id is rejected rather than
   silently read as a YAML number. ``default:``, if given, must be one
   of the declared ids.

   ``exact: true`` disables hwmv2's own **nearest-lower match**: normally
   a requested revision that is not itself declared resolves down to the
   highest declared revision that is ``<=`` the request (comparing
   per-format — ``major.minor.patch`` also zero-pads a short request,
   ``"1"`` becoming ``"1.0.0"``, before either comparison runs); with
   ``exact: true``, any requested value that is not an exact declared
   member is refused instead.

``rig: variants:``
   The rig's own variant axis — topology *alternates*, not a hardware
   axis: a variant selects which qualifier-delta fragments apply (below),
   never a board or a socket mapping. ``list:`` entries are either a bare
   name or ``{name: <name>}`` (any other key on a mapping entry is
   silently ignored — see `What rig.yml never declares`_). ``default:``,
   if given, must be one of the listed names. Resolution takes an exact
   declared member only; there is no hwmv2 machinery on this axis.

A rig with variants *and* revisions must not let any two distinct
selections — a variant alone, a revision alone, or a combined
``(variant, revision)`` pair — construct the same delta-fragment stem
(see `Qualifier delta fragments`_): a variant literally named the same as
a revision id is the single-axis case of the same collision, and both are
refused (``lang-variant``) at load time, before any fragment is read.

Combined selection resolves variant, then revision — both independently
against the declarations above, an unselected axis taking its declared
default (or being refused if it has none and nothing was requested).
There is no interaction between the two beyond the shared-stem collision
check: a rig may declare either axis, both, or neither.


What ``rig.yml`` never declares
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**No ``board:`` key exists anywhere in this grammar — not at the top
level, not per variant.** A rig describes a topology; the
:term:`invocation coordinate` (``-b``/``-DBOARD=``, see
:doc:`commands`) is the *only* source of the board, for every rig, with
no exception — including a rig built against more than one real board
(the same content file resolves on either, provided both boards expose
the sockets it names; see :doc:`../tutorials/make-the-rig-permanent`
and the ``arduino_r3`` alias convention it describes). A rig build with
no board given is a configure-time error, not a fallback.

A stray ``board:`` (or ``sockets:``) key on a ``variants:`` list entry is
not rejected — it is **silently ignored**, the same as any other
unrecognized key in this grammar. Nothing in ``rig.yml`` today populates
a per-variant board or socket table.


``<name>.yml`` — content
---------------------------

.. code-block:: yaml

   instances:
     - name: <string>                      # required
       shield: <string>[@<revision>]       # required
       socket: <label>                     # single-plug shields only
       sockets:                            # OR, plural shields only
         <slot>: <label>
       invert: true | false                # optional
       config:
         <config-element-label>: <value>
       params:
         <device-label>:
           <property-name>: <value>

   wires:
     - from: <instance>.<node>
       to: <instance>.<node>
       route: adhoc                        # or: {via: <position-name>}

``instances:``
   Required, a list — an empty list is legal (a rig with no modules
   attached still configures, structurally identical to a plain board
   build). Each entry is one :term:`instance`:

   ``name:`` / ``shield:``
      Both required. ``shield:`` is the template's own name, optionally
      qualified with ``@<revision>`` (the *shield's* revision axis — see
      :doc:`shield-template` — never the rig's own).

   ``socket:`` / ``sockets:``
      Mutually exclusive, and each legal only for the matching shield
      shape: a single-plug shield takes bare ``socket: <label>``; a
      *plural* shield (more than one plug) takes ``sockets:``, a slot
      name → label map, one entry per plug the shield's own plurality
      requires. Naming the wrong form for the shield's own plurality is
      refused (``lang-instance-socket``). Either is optional — an
      omitted socket (a whole omitted slot, in the plural case) is left
      to the analyzer's own *unique-by-type* inference, which succeeds
      only when exactly one board socket of the needed type exists.
      ``<label>`` may name a :term:`carrier`'s own exposed socket as
      ``<carrier instance>.<socket>`` instead of a board socket directly
      (see :term:`carrier`).

   ``invert:``
      A boolean, default false.

   ``config:``
      One entry per :term:`routing jumper` or strap this instance sets,
      keyed by the config element's own **devicetree label** — never its
      node name, and with no hyphen/underscore normalization. The value
      is spelled as the config sheet spells it: a position name
      (``D2``) for a jumper, an integer for a strap. Naming a label the
      shield has no config element for is refused
      (``lang-config``, listing the real labels).

   ``params:``
      One entry per device whose ``shield,params`` this instance
      assigns, keyed by the device's own **devicetree label**, each a
      property-name → value map. A bare integer literal is accepted
      directly; any other value must resolve (via the C preprocessor) as
      a token declared in *that device's own* ``shield,param-includes``
      — the vocabulary is always the owning device's, never something
      ``rig.yml`` supplies. Naming an undeclared device, or a property
      the device's own ``shield,params`` does not declare, is refused
      (``lang-param``) before any preprocessing runs; a value that fails
      to resolve is ``lang-dt-include``, naming the header to add it to.
      Every parameter a device declares with **no authored default**
      must end up assigned once every qualifier delta has applied, or
      the rig is refused (``lang-param``, "declares ... as required").

``wires:``
   Optional, a list of point-to-point jumper wires between two instances
   — a physical connection the shields' own connectors don't carry. No
   shield in the corpus ships one yet, so every rig on disk today omits
   this key; the grammar below is exercised only by fixtures.

   ``from:`` / ``to:``
      Both required, each a ``<instance>.<node>`` dotted reference — the
      instance must exist in the *effective* topology at this point, and
      ``<node>`` must name exactly one referencable node of that
      instance's own resolved shield (an unknown or ambiguous node is
      ``lang-wire-ref``).

   ``route:``
      Required. Either a bare value (``adhoc`` — a hand-run wire, no
      further claim) or a mapping naming ``via:`` — a connector position
      the wire is routed through. A mapping with no ``via:`` key is
      refused (``lang-schema``).


Qualifier delta fragments
----------------------------

A selected, **non-default** variant and/or revision may layer a delta
onto the base content — never required; a value that contributes nothing
at all is refused (see below). Stems are constructed from the rig's own
``name:`` and the *selected* value (a revision id normalized by
replacing ``.`` with ``_``, e.g. ``1.5`` → ``1_5`` — never applied to a
variant name), in this fixed naming scheme:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Fragment
     - Applies to
   * - ``<name>_<variant>.yml``
     - the selected variant's own content delta
   * - ``<name>_<variant>.overlay`` / ``<name>_<variant>_defconfig``
     - the selected variant's own devicetree/Kconfig fragments (Zephyr's
       own ``EXTRA_DTC_OVERLAY_FILE``/``EXTRA_CONF_FILE`` mechanism —
       collected by cmake, never parsed by rigc)
   * - ``<name>_<norm-revision>.yml``
     - the selected revision's own content delta
   * - ``<name>_<norm-revision>_defconfig``
     - the selected revision's own Kconfig fragment
   * - ``<name>_<variant>_<norm-revision>.yml``
     - the combined (variant, revision) content delta — collected LAST

**A content delta (``.yml``) applies five operations, in this fixed
order, every time:**

``instances:``
   Patches an *existing* instance's top-level keys — a given key
   **replaces** wholesale (never merges into what was there); an
   unspecified key **inherits** unchanged. Naming an instance the
   effective topology does not have is refused, naming the delta that
   already removed it if that is why. Two asymmetric resets apply on a
   shield change: ``params:`` is always cleared (the old assignments are
   keyed to devices the new shield may not have); the ``socket:``/
   ``sockets:`` map carries forward *unless* the new shield's slot names
   differ from the old map's, in which case it resets the same way. A
   patch that supplies ``params:`` for an instance whose shield did
   **not** change must restate every property the effective topology
   already assigned — omitting one is refused (the *restate rule*: a
   wholesale replace that dropped a property would otherwise silently
   revert it to the shield's own default).

``add-instances:``
   Full instance declarations, same shape as the base ``instances:``
   entries. The named instance must **not** already exist.

``remove-instances:``
   A list of instance names. Each must currently exist.

``remove-wires:``
   A list of ``{from:, to:}`` pairs, matched against the effective wire
   list by their **raw endpoint strings** (a wire carries no other
   identity). Re-routing a wire is remove, then add — there is no
   in-place "replace".

``add-wires:``
   New wires, same shape as the base ``wires:`` entries.

Every parameter invariant (``params:``'s own required-parameter rule, above) is re-checked over the
*whole* effective topology after each stage — a later stage may still
supply what an earlier one left unassigned, and a shield substituted
mid-chain is re-checked against its own requirements immediately.

**A selected non-default variant or revision that contributes nothing
at all — no delta file, and (for a variant) no ``.overlay``/
``_defconfig`` either — is refused** (``lang-variant`` / ``lang-rev``,
naming every filename that was looked for). The *declared default* of
an axis is exempt: the base content file already **is** what the
default means, so it needs no fragment of its own.


.. seealso::

   :doc:`promotion`
      A single shield, or a small ``;``-separated list of them, built as
      a rig with neither of these two files ever written to disk.

   :doc:`commands`
      How a board and a rig combine into one build.
