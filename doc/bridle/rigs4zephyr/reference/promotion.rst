Promotion
==========

A shield can become a rig of one instance — or a small list of shields a
rig of several — **with neither a** :term:`rig metadata file` **nor a**
:term:`rig content file` **ever written to disk.** This page is the
semantics of that grammar: what a promotion target means, what it
desugars to, and which forms are refused and why. The authority is
``scripts/rigc/promote.py`` (the desugaring itself) and
``scripts/list_rigs.py`` (the namespace rule cmake's own ``-DRIG=``
resolution runs before promotion is ever reached).

:doc:`commands` keeps the command-line surface — which flags accept a
promotion target, and how they spell it. This page is what that target
*means*.

.. contents::
   :local:
   :depth: 1


What promoting a shield means
--------------------------------

A :term:`shield template` is *promotable* when its own ``shield.yml``
declares ``template: true``. Naming a promotable shield's own name
wherever a rig target is accepted (``-DRIG=``, ``west rigs --explain``,
``west rigs --boards-for``) is the **natural mapping** ``a -> [a]``: one
instance, named after the shield itself, with no ``socket:`` unless one
is given — the same *unique-by-type* inference an authored rig's own
un-socketed instance gets.

A bare name is resolved against **both namespaces** — a persisted rig
(``boards/rigs/<name>/``) and a discoverable, promotable shield — before
anything else about the target is read:

- a name that is **only** a rig resolves as that rig, unaffected by
  anything on this page;
- a name that is **only** a promotable shield resolves as a promotion;
- a name that is **neither** does not resolve at all;
- a name that is **both** is refused outright — ``'<name>' names both a
  rig (<rig-dir>) and a shield (<shield-dir>) -- rename one; a name that
  is both is ambiguous by construction, never guessed between.``

A shield that is *discoverable* (``shield.yml`` exists) but not
*promotable* (no ``template: true``, or no ``shield.yml`` at all) is
named in the refusal along with which of the two it is missing.


The target grammar
----------------------

.. code-block:: text

   <target>     := <element>[;<element>...]
   <element>    := <name>[@<revision>][/<variant>][:<assignment>...]
   <assignment> := socket=<label>
                 | socket.<slot>=<label>
                 | config.<label>=<value>
                 | <device>.<prop>=<value>

A single (no ``;``) target shares its grammar with an **authored rig's
own** target string — ``name[@rev][/variant]`` resolves a persisted
rig's own qualifier axes when ``<name>`` is a rig. ``/<variant>`` is
**refused** the moment ``<name>`` resolves as a shield instead: *"a
promoted shield has no variant axis to select from -- '@rev' is the only
axis it promotes with, and it selects the SHIELD's own revision, never a
rig variant"*. ``@<revision>`` on a promoted shield selects that
shield's own revision axis (:doc:`shield-template`) — it desugars to
``shield: <name>@<revision>`` on the one synthesized instance, and is
never checked against the shield's declared revisions here; that stays
the loader's own job once the synthesized document is actually loaded.

A ``;``-separated **list** target promotes several shields into one rig
of several instances, each element carrying its own optional ``@rev``
and assignments — but **never** ``/<variant>``: every list element must
be a shield, which has no variant axis at all, so the grammar simply
omits the slot rather than accepting and then refusing it.


Assignments
--------------

Assignments are ``:``-separated ``<key>=<value>`` pairs — never
positional, and never comma-separated (a devicetree property name may
itself contain a comma, e.g. ``zephyr,code``). A key is either the bare
word ``socket``, or dotted (``<label>.<name>``, split on the *first*
dot only).

``socket=<label>``
   The single-plug spelling: which board socket (or :term:`carrier`
   socket, ``<carrier instance>.<socket>``) the shield's one plug mates.
   Refused on a shield with more than one plug — *"shield plugs N
   sockets -- use socket.<slot>=<label> ..., not bare socket=<label>"*.

``socket.<slot>=<label>``
   The plural spelling, one assignment per plug slot — ``<slot>`` must
   be one of the shield's own plug node names, or the assignment is
   refused, listing the real ones. Refused the other way on a
   single-plug shield too: *"shield has a single plug -- use
   socket=<label>, not socket.<slot>=<label>"*.

``config.<label>=<value>``
   Which position or address a :term:`routing jumper` or strap is set
   to, named by the config element's own devicetree label — the exact
   analogue of a rig content file's own ``config:`` block (see
   :doc:`rig-file`). Not checked against the shield's real config
   elements here; a label naming none is refused once the synthesized
   document loads.

``<device>.<prop>=<value>``
   A shield parameter, named by the device's own devicetree label — the
   analogue of ``params:``. Likewise not validated here; an undeclared
   device or property, or a token that fails to resolve, is refused
   once the synthesized document loads (see :doc:`rig-file`).

Every assignment key may be given **at most once** per target element —
a duplicate ``socket.<slot>=``, ``config.<label>=`` or
``<device>.<prop>=`` is refused, naming which. An empty value
(``key=``) is refused. A malformed assignment (no ``=`` at all, or a
dotted key missing either half) is refused naming the whole malformed
fragment.


What a promoted shield becomes
----------------------------------

A single-element promotion desugars to exactly the text an author would
have to check in to mean the same thing — ``west rigs --explain
<target>`` prints it verbatim, and is the copy-paste source for turning
one into a real rig (:doc:`../tutorials/make-the-rig-permanent`):

.. code-block:: yaml

   # rig.yml -- name only; no board, ever (see rig-file's own rule)
   rig:
     name: <shield-name>

   # <shield-name>.yml -- one instance, named after the shield itself
   instances:
     - name: <shield-name>
       shield: <shield-name>[@<revision>]
       socket: <label>            # only if socket= was given
       sockets:                   # only if socket.<slot>= was given
         <slot>: <label>
       config:                    # only if any config.<label>= was given
         <label>: <value>
       params:                    # only if any <device>.<prop>= was given
         <device-label>:
           <prop>: <value>

A **list** target (``a;b``) desugars the same way, generalized to N
instances: one rig, its own name every element's shield name joined
with ``+`` (``a+b``), one instance per element in the given order —
each rendered by the identical printer a single-element promotion uses,
so a one-element list is byte-identical to a bare promotion by
construction. Socket exclusivity is enforced across the **whole** list,
the same as it would be across an authored rig's own instances.

Neither the single nor the list form checks a promoted assignment
against the shield's real slots, config elements or parameters *here* —
what actually loads the synthesized documents is the identical loader
path an authored rig goes through (:doc:`rig-file`), so a promoted
shield fails for the same reasons, with the same diagnostics, that an
authored rig with equivalent content would. In particular, promoting a
shield whose devices declare a required parameter with no default
succeeds as *syntax* but the desugared rig is refused
(``lang-param``, "declares ... as required") unless a
``<device>.<prop>=`` assignment supplies it.


Refusals specific to promotion
----------------------------------

Beyond the assignment-grammar refusals above, and beyond whatever the
synthesized document itself fails to load as (:doc:`rig-file`'s own
refusals), promotion adds these, checked in this order:

.. list-table::
   :widths: 45 55
   :header-rows: 1

   * - Target
     - Refused because
   * - a name matching both a rig and a shield
     - ambiguous by construction — rename one
   * - a shield with no ``shield.yml``, or one that omits
       ``template: true``
     - not promotable — the message names which of the two is missing
   * - a shield target qualified with ``/<variant>``
     - a promoted shield has no variant axis
   * - a bare ``socket=`` on a shield with more than one plug
     - use ``socket.<slot>=`` instead
   * - ``socket.<slot>=`` on a shield with exactly one plug
     - use bare ``socket=`` instead
   * - ``socket.<slot>=`` naming a slot the shield does not have
     - lists the shield's real slot names
   * - a list element naming a **persisted rig**
     - every list element must be a shield; a rig is already a
       container, and a list mixing containers with elements has no
       coherent desugaring
   * - a list element naming neither a rig nor a discoverable shield
     - names the specific element that failed to resolve
   * - the same shield name given more than once in one list
     - one instance per element; a repeated name has no naming rule yet


.. seealso::

   :doc:`rig-file`
      What the synthesized documents mean, and what refuses them once
      they load.

   :doc:`commands`
      ``--rig``/``-DRIG=``/``--boards-for``/``--explain`` — the surfaces
      that accept a promotion target.
