.. _rigs4zephyr_explanation_shield-templates:

Why shield templates look the way they do
============================================

:ref:`rigs4zephyr_reference_shield-template` lists every property a
``.shield`` file may declare, and
:ref:`rigs4zephyr_tutorials_write-a-shield-template` shows how to write
one. This page explains the design behind them: why a
:term:`shield template` is not an overlay, why it names things the way it
does, and why a fact about a module sits in the shield, in the rig, or
with :term:`rigc`. One principle recurs throughout: **each
fact has one owner**, and that owner is whoever actually knows it.

The examples use bridle's own ``grove_btn`` and ``grove_led`` templates
(``boards/shields/grove_btn/grove_btn.shield``,
``boards/shields/grove_led/grove_led.shield``).

A template is not an overlay
------------------------------

A Zephyr shield overlay goes to ``dtc`` unchanged: it is a patch against
the board's devicetree, written for one placement. A ``.shield`` file
never reaches ``dtc``. ``rigc`` preprocesses and parses it, checks it
against its :term:`connector type`, and instantiates it once per
:term:`instance`. Only the overlay ``rigc`` *generates*
(``rig-gen.overlay``) joins the build. The two files look alike (the same
syntax, the same ``#include`` lines) but follow different rules:

- a ``.shield`` file is **loaded and checked**. It is written against a
  :term:`plug` rather than a board, so a reference such as
  ``<&gb_plug GROVE_SIG0 ...>`` means "signal 0 of whichever socket I end
  up in". It could not be applied to any board as written;
- an ``.overlay`` file is **applied raw**. Nothing in ``rigc`` reads a
  rig's variant overlay or the overlay in a rig's own folder. Both follow
  ``rig-gen.overlay`` in the ordinary ``EXTRA_DTC_OVERLAY_FILE`` chain,
  and ``dtc`` and the Zephyr bindings check them the way they check any
  overlay.

That is why the suffix is different. The extension tells the reader, and
the shield library's discovery, which set of rules a file follows.
Discovery treats a folder as a template when it has a ``<name>.shield``
(or a ``shield.yml`` entry declaring ``template: true``). An overlay on
its own never makes a folder a template, so a legacy Zephyr shield is
never mistaken for one. The ``shield-templates`` wrapper node inside the
file marks the same boundary: ``rigc`` reads only what sits under it.

One translation unit per shield
---------------------------------

Every template is preprocessed and parsed **on its own**, as its own
translation unit. It is never ``#include``-d into a shared tree, and two
shields never share one parse. The work directory of a real run shows
this: ``rigc-generated/`` holds one ``shield-<name>.dts`` per shield the
rig uses, and none for shields it does not.

The main consequence is a **private label namespace**. A label only has to
be unique inside its own shield. ``grove_led`` can call its plug
``gl_plug`` and ``grove_btn`` can call its plug ``gb_plug``, but either
could equally call it ``plug``, and a third shield using the same names
would conflict with neither. No prefix convention is needed to keep labels
apart across shields. Where the corpus uses short prefixes, they are for
readability only.

Label clashes in the *output* are handled differently: ``rigc`` composes
every output label from the instance name, and it checks that composition
for collisions before anything is emitted (see `Labels are the
interface`_ below).

Who decides what
------------------

A module's facts come from three places, and each part of the template
format is shaped so that each fact is written down by the one party that
can know it:

- **The shield declares the domain.** Which I²C addresses an address strap
  can select, which positions a :term:`routing jumper` can route a signal
  to, whether a chip-select is wired to a fixed pin: these are facts about
  the copper on the module. They belong in the template, written once, and
  are never copied into a rig file, where copies would drift apart.
- **The rig makes the selection.** Which state a particular module's
  strap or jumper is actually set to is a fact about *this* placement, so
  it lives on the instance, in the rig's ``config:`` block.
- **The tool authors the rendering.** ``rigc`` alone writes ``reg`` and
  the unit-address into the output, always together as a matching pair. A
  template authors ``reg`` only when copper fixes the address (a domain
  with one element), and ``rigc`` checks it. A device whose address comes
  from a strap authors ``shield,addr-from`` instead. The rule that ``reg``
  must equal the unit-address therefore holds because of how ``rigc``
  renders the output, and a template author never has to maintain it by
  hand.

The chip-select sits on the tool's side of this split on purpose. A
device either has its chip-select fixed by copper
(``shield,cs-position``), or ``rigc`` draws one from the socket's
chip-select pool, skipping positions another device already holds. No
rig-facing key selects a pool chip-select. A pool chip-select is not a
config element (a strap or jumper): the shield declares no domain for
it and gives it no sheet label, so there is nothing to select against.
Any free pool position works, and picking one is exactly the clash
avoidance that a hand-written overlay gets wrong without noticing. The
:term:`config sheet` records the result.

Every other position is **never** allocated automatically. Any free
chip-select in a pool, or any free address in a strap's domain, does the
same job as any other. A jumper position does not: moving an interrupt
from D7 to D2 changes which SoC pin and interrupt line the driver uses,
and which header pin is left free for everything else. Making that choice
automatically would be a surprise, so it is left to the rig author. If
the rig does not choose, ``rigc`` refuses the rig with ``phys-position``
and lists the jumper's domain. It never picks a pin on the author's
behalf.

When the rig says nothing
---------------------------

Each kind of choice has its own answer when the rig leaves it unset:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Choice
     - Resolved by, when the rig is silent
   * - device parameter (``shield,params``)
     - the value the template authors for that property. With no authored
       value the parameter is **required**, and the rig is refused until
       it is assigned.
   * - address strap
     - ``rigc`` **allocates** a free address from the strap's domain and
       the config sheet tells the human which state to set.
   * - routing jumper
     - **nobody**: refused (``phys-position``).
   * - chip-select
     - the socket's pool. No config element is involved.

``grove_btn`` shows the "required" case. Its ``gb_key`` device declares
``shield,params = "zephyr,code"`` and authors no ``zephyr,code`` itself.
A keycode describes one instance, not the module type: two buttons in one
rig need two different keys. Any default would therefore be wrong for all
but one of them, so the template gives none, and every rig using the
shield must supply one.

This table also separates two concepts that look alike, plus one piece of
syntax:

- A **config element** (a strap or jumper under the template's
  ``config { }``) is a choice **a person makes by hand**, with a soldering
  iron or a jumper cap. The generated devicetree records the *result* (the
  ``reg``, the routed pin), and the config sheet records the *action*
  ("set ADDR jumper to state 1"). Both outputs are needed.
- A **parameter** (``shield,params``) is a choice **made by rebuilding**.
  The value goes into the overlay as written. Its row in the config
  sheet's *Parameters* table is a record of that value, not an
  instruction to anyone.
- The rig's ``config:`` **block** is neither. It is only the syntax for
  assigning config elements (both kinds, keyed by label). It adds no
  concept of its own, just as ``params:`` is only the syntax for assigning
  parameters and ``socket:`` is only the syntax for assigning plugs.

Labels are the interface
--------------------------

Every rig-facing reference into a shield resolves by **DTS label**: a
``config:`` key, a ``params:`` device key, a ``wires:`` endpoint, and a
:term:`carrier`'s exposed socket in ``socket: <carrier>.<socket>``. A node
that such a reference could name must have a label, and a node without
one is refused (``lang-shield-label``). ``rigc`` does not fall back to the
node name.

The reason is that a shield's own internal references are already labels.
``shield,addr-from = <&tc_addr_strap>`` and ``<&gb_plug ...>`` are
phandles. By resolving the rig's strings against the same labels, a
string in a rig file and a phandle in a shield are the **same
identifier**, and one ``grep`` for ``gb_key`` finds the declaration, every
internal use, and every rig that assigns it. Node names repeat across
shields far more often than labels do (many shields have a node called
``sensor``) and could not give that. Node names remain in use, but only
*internally*: as keys ``rigc`` stores its own bookkeeping under, and as
the node names it emits. No rig author ever types one.

In the output, every device label is **composed**:
``<instance>_<shield label>``. ``rigc`` checks the composed set for
collisions before emitting (``phys-label``), and it is stable: adding or
removing *another* instance never renames yours. That makes the composed
labels the rig's **public reference API**. They reach the final
``zephyr.dts`` unchanged, so application code and hand-written overlays
can rely on them.

For the same reason, a shield never writes ``/aliases`` or ``/chosen``:
``rigc`` reads nothing outside ``shield-templates``, so a template has no
way to write either. An alias is a tree-wide singleton, and a unit that
can be instantiated several times cannot own one: two instances would
both claim ``led0``. ``rigc`` also never numbers aliases itself. Any
numbering based on a counter would renumber a deployed rig's aliases
whenever an instance is added or removed. The selection belongs to the
rig, written as an ordinary overlay against the composed labels (for
example in the rig folder's own ``<rig>.overlay``, which the build applies
after ``rig-gen.overlay``).

Device collections
--------------------

Some bindings are collections: one parent node carries the
``compatible``, and each device is a child entry (``gpio-keys``,
``gpio-leds``, ``pwm-leds``). If each instance emitted its own parent,
three buttons would produce three ``gpio-keys`` nodes where Zephyr expects
one. If they shared one fixed node, each instance would overwrite the
last. ``shield,collect`` names the collection a device is an *entry* of,
and ``rigc`` aggregates every entry from every instance into **one node
per collection compatible**. Each entry keeps its own composed label. This
is ``lotus_buttons`` (two ``grove_btn``, one ``grove_led``) as ``rigc``
emits it for ``seeeduino_lotus``:

.. code-block:: devicetree

   / {
           gpio_keys: gpio_keys {
                   compatible = "gpio-keys";
                   btn_start_gb_key: btn_start_gb_key {
                           label = "btn_start_gb_key";
                           zephyr,code = <INPUT_KEY_0>;
                           gpios = <&grove_d2 0 0x20>;     /* SIG0 */
                   };
                   btn_stop_gb_key: btn_stop_gb_key {
                           label = "btn_stop_gb_key";
                           zephyr,code = <INPUT_KEY_1>;
                           gpios = <&grove_d6 0 0x21>;     /* SIG0 inverted */
                   };
           };
           gpio_leds: gpio_leds {
                   compatible = "gpio-leds";
                   led_status_gl_led: led_status_gl_led {
                           label = "led_status_gl_led";
                           gpios = <&grove_a0 0 0x0>;      /* SIG0 */
                   };
           };
   };

The merging happens only at emission. Each entry is still its own device
in the model, so net and conflict analysis are unaffected. The same
design sets two limits. There is one collection node per compatible, and
a template cannot name a second one to split its entries off. And
``rigc`` does not merge entries into a collection the *board* already
declares: it always emits its own node.

Shields with more than one plug
---------------------------------

A shield may declare several plug nodes, for example two mikroBUS plugs
on one board spanning two sockets. There is still one authored form: the
number of plugs is simply a count, and every consumer handles one plug
and many the same way. Each plug's **node name is its slot name**, owned
by the shield. A list would not work here, because two plugs of the *same*
connector type cannot be told apart by position, only by the names the
shield gives them. The rig assigns them by name in ``sockets:``.

Two rules keep the plural case from disturbing the single case:

- **A slot qualifier appears only when there is more than one slot.** A
  diagnostic about a one-plug shield says ``instance 'btn_start'``, and one
  about a plural shield says ``instance 'canspan': slot 'left'``. A
  single-plug shield has nothing to tell apart, so its messages and
  artifacts are exactly what they would be if plurality did not exist.
  This follows the same rule as bus names, which are shown bare when there
  is one bus and role-qualified only when there are several.
- **Two slots of one instance never resolve to the same socket.** One
  physical connector cannot take two plugs. ``rigc`` resolves each slot
  independently (its own inference, mating and bus-exposure checks), and
  if two slots land on the same physical socket it refuses the rig
  (``phys-socket``) instead of trying to match slots to sockets itself.
  When the answer is ambiguous, the rig author chooses, in ``sockets:``.

A routing jumper is refused on a shield with more than one plug
(``lang-shield-plurality``). Its position domain lists connector
positions with no plug axis, so "D2" would not say *which* plug's D2.

A shield as a rig
-------------------

A :term:`promoted shield` builds a template as a rig of one instance, with
no rig files written. Its assignments reuse the rig's own keys, spelled
as dotted ``<first>.<second>=<value>`` pairs, and two first halves are
**reserved**: ``socket.<slot>=`` routes to the instance's ``sockets:``,
and ``config.<label>=`` routes to its ``config:``. Every other first half
is a device label, routed to ``params:``. The rule behind this is that
*the reserved first half names the instance key the assignment lands
in*, so any future assignment kind will take the same form. The cost is
stated openly: a device labeled literally ``socket`` or ``config`` cannot
receive a parameter through promotion. A template already reserves
``config`` as the name of its config-elements group.

Promotion **desugars to text**: the rig metadata file and rig content file
an author would have written by hand. ``west rigs --explain`` prints them
exactly:

.. code-block:: console

   $ west rigs --explain 'grove_btn:socket=grove_d2:gb_key.zephyr,code=INPUT_KEY_0'
   # rig.yml
   rig:
     name: grove_btn

   # grove_btn.yml
   instances:
     - name: grove_btn
       shield: grove_btn
       socket: grove_d2
       params:
         gb_key:
           zephyr,code: INPUT_KEY_0

``rigc expand --promote`` writes that pair into its work directory and
loads it through the same loader an authored rig goes through. Promotion
therefore adds no second set of semantics. A promoted shield is accepted
or refused for exactly the reasons, and with exactly the diagnostics, that
the equivalent authored rig would be. Promoting ``grove_btn`` without the
``gb_key.zephyr,code=`` assignment is refused as a missing required
parameter, the same as a rig file that omits it. It also makes the
printed text a working starting point for a permanent rig
(:ref:`rigs4zephyr_tutorials_make-the-rig-permanent`).

Parameter headers are build inputs
------------------------------------

``grove_btn`` declares
``shield,param-includes = "zephyr/dt-bindings/input/input-event-codes.h"``
next to its ``shield,params``. The header is the **vocabulary** of the
parameter: ``INPUT_KEY_0`` is a valid value because that header defines
it. It is declared explicitly on the device and not inferred from the
template's own ``#include`` lines, because a header that only defines
macros adds no node or property to the parsed tree, so ``rigc`` cannot
recover it from the parse. Declaring it also keeps the permitted
vocabulary narrow: a token from some other header the template happens to
include is not accepted as a keycode.

Because the value is part of the build, the header is too. ``rigc`` adds
it to the rig's ``RIG_DEPENDS`` in ``context.cmake`` (next to the
``.shield`` files, the ``shield.yml`` files and the board devicetree), so
editing the header makes the build reconfigure. Without it, a changed
keycode would leave a stale overlay that nothing would detect. The
generated ``rig-gen-includes.dtsi`` includes the same header, which lets
``rig-gen.overlay`` keep the value symbolic (``<INPUT_KEY_0>``). The
config sheet's *Parameters* table shows the resolved number next to the
symbol, for anyone who does not know the header.

.. seealso::

   :ref:`rigs4zephyr_reference_shield-template`
      Every property named on this page, with its exact refusals.

   :ref:`rigs4zephyr_reference_rig-file`
      The ``socket:``/``sockets:``, ``config:`` and ``params:`` keys that
      make the selections.

   :ref:`rigs4zephyr_reference_promotion`
      The promotion grammar in full.
