.. _rigs4zephyr_explanation_socket-model:

Why sockets and connector types look like this
================================================

:ref:`rigs4zephyr_reference_board-socket` lists every property a
:term:`socket` node and a :term:`connector type` binding can carry. This
page covers why the model is shaped that way: why a connector exists as
three separate things, why a GPIO line can cross a socket in a plain
devicetree overlay while an I²C device can't, and why ``rigc`` resolves
names, labels and cell counts the way it does. The examples come from the
Grove sockets on ``seeeduino_lotus``
(``boards/seeed/seeeduino_lotus/grove_sockets.dtsi``) and the Grove shield
templates under ``boards/shields/``.

One connector, three artifacts
--------------------------------

When a board developer says "a Grove connector", the word covers three
separate things, and the model keeps them apart:

- The **connector type** is the contract that every Grove connector
  shares. It lives in one binding, ``dts/bindings/connectors/grove.yaml``,
  plus a header of :term:`position` indices,
  ``include/dt-bindings/connector/grove.h`` (``GROVE_SIG0``,
  ``GROVE_SIG1``).
- A **socket** is one physical Grove connector on one board. It is a real
  devicetree node such as ``grove_d2: connector_grove_d2``, with
  ``compatible = "socket,grove"``.
- A :term:`plug` is the module side. It is a node inside a
  :term:`shield template` (``gb_plug: plug`` in ``grove_btn.shield``) that
  declares ``shield,plugs = "grove"``.

.. graphviz::

   digraph socket_model {
      rankdir=LR;
      node [shape=box, fontsize=10];
      type   [label="connector type\ngrove.yaml + grove.h"];
      socket [label="board socket\ngrove_d2 (socket,grove)"];
      plug   [label="shield plug\ngb_plug (shield,plugs = \"grove\")"];
      type -> socket [label="validates", fontsize=9];
      type -> plug   [label="constrains", fontsize=9];
      plug -> socket [label="mates by type name\nand GROVE_SIG0", fontsize=9, style=dashed];
   }

The contract has a board half and a module half, and both are kept in one
file. That way the two halves can't drift apart. The type's binding keys
are namespaced by the *side* they describe. ``socket,*`` properties
(``socket,i2c``, ``socket,stackable``, ``socket,cs-pool``) describe what a
board socket node declares, and edtlib validates them as an ordinary
binding. ``plug,*`` keys (``plug,positions``, ``plug,bus-proxies``)
describe what a shield of that type may use. edtlib treats a top-level key
that contains a comma as an opaque vendor extension, so ``rigc``'s
connector-type registry (``scripts/rigc/registry.py``) reads these keys
from the raw YAML. No key is named after the project. A key says which
side of the connector it constrains, not which tool reads it.

The type itself is identified by name, the same way a compatible is. On
the board side it is the part of the compatible after ``socket,``. On the
shield side it is the string value of ``shield,plugs``. Mating is a string
comparison: a plug of type ``grove`` mates a socket whose type is
``grove`` and nothing else. The position header is the single source of
truth that both sides share. The board's ``gpio-map`` says which SoC pin
``GROVE_SIG0`` reaches, the shield says it uses ``GROVE_SIG0``, and
neither side has to know about the other.

Signals cross a socket; buses do not
--------------------------------------

A typed socket node *is* a standard Zephyr nexus. ``grove_d2`` has a
``gpio-map`` whose child specifiers are Grove positions. Sockets that can
drive PWM or read analog values also have ``pwm-map`` and
``io-channel-map`` entries, with cell shapes that match the upstream
bindings. So GPIO, PWM and ADC routing already work without ``rigc``: a
hand-written overlay can write
``gpios = <&grove_d2 GROVE_SIG0 GPIO_ACTIVE_HIGH>`` and dtc chases the map
to ``&porta 14``, just as it does for the upstream ``arduino_header``.
``rigc`` emits exactly this form. For the ``lotus_pwm_led`` rig it writes
the following:

.. code-block:: devicetree

   pwms = <&grove_d2 0 20000000>;  /* SIG0 */

The map also gives ``rigc`` *net identity*. Each position resolves to a
real SoC pin, so two sockets that share copper are recognized as one net.
On the Lotus, the Grove connectors are laced together: SIG1 of
``grove_d2`` and SIG0 of ``grove_d3`` are both ``&porta 9``. Two modules
that claim those two positions collide on that pin, even though they are
plugged into different sockets.

Buses can't cross a socket this way, and that's a limit of devicetree,
not a gap in ``rigc``. Devicetree expresses bus membership through
**parentage**: an I²C device must be a child node of its controller and
carry ``reg``. A nexus can only redirect the cell values inside a
phandle-array property. There is no nexus mechanism for parentage.
``socket,i2c`` is a plain phandle, a machine-readable statement of which
controller the socket reaches, and not something an overlay can nest
nodes under. To place a device on that bus, a hand-written overlay has to
write ``&i2c1 { sensor@68 { ... }; };``, which names the controller
directly and ties the overlay to one board again.

That is why a shield template groups its bus devices under **bus proxy**
nodes (``i2c { ... }``) instead of under a controller. The connector
type's ``plug,bus-proxies`` lists the proxies a shield of that type may
use. ``grove.yaml`` allows only ``i2c``, and a proxy the type doesn't list
is refused with ``lang-shield-proxy``. Once the socket is resolved,
``rigc`` places the devices under the real controller node that the
socket's ``socket,<kind>`` names, and writes each device's ``reg`` and
unit address as a matching pair. A socket exposes only the buses it
declares, and a missing property is the declaration: none of the Lotus
Grove sockets carry ``socket,i2c``, so a shield that needs I²C is refused
on them with ``phys-subset``.

Chip-select: the case that looks like a signal
------------------------------------------------

Chip-select is where this reasoning is least obvious. ``cs-gpios`` *is* a
phandle-array, so a shield could in principle add a chip-select entry
through a socket's GPIO nexus. But an SPI child's ``reg`` must equal the
index of its entry in ``cs-gpios``. That array belongs to the controller
and is shared by every device on the bus, so assigning indices is a
global, order-dependent allocation. No text-level mechanism, whether a
nexus, an include or an overlay, can do that allocation.

A property assignment in an overlay also *replaces* the whole array. If
``rigc`` emitted only the rig's own chip-selects, it would destroy every
entry the board authored for itself. Each existing SPI child would then
index into a shorter array, and Zephyr resolves an out-of-range index to
an empty GPIO spec with no build error. To avoid that, ``rigc`` reads the
board's existing ``cs-gpios`` and child ``reg`` values from the resolved
devicetree. It emits the board's entries verbatim and first, and reuses
an entry when a rig device's chip-select resolves to the same SoC pin.
New entries are appended only after the board's own entries. A new index
that collides with a ``reg`` an existing child already holds is refused
with ``phys-cs``.

Candidate chip-select positions come from a **pool**, and the pool is a
fact of a *bus*, not of a whole socket. Each SPI bus a socket exposes has
its own ordered candidates (``socket,cs-pool`` for the plain ``spi`` bus).
The Grove connector type exposes no SPI and declares no pool, so the
Lotus Grove rigs never reach this code path. The design is there for
connector types that do expose SPI.

Bus names belong to the connector type
----------------------------------------

A socket can offer more than one bus of the same kind. ``rigc`` accepts a
role-suffixed form, ``socket,<kind>-<role>`` (for example
``socket,spi-sensors``), next to the plain ``socket,<kind>``. The role
names belong to the **connector type**, never to a board. A board that
wires a type inherits the type's names, so a shield written against the
type can rely on them on any board. This is the same status as the type's
position numbering and stackability. No connector type in bridle declares
a role-suffixed bus today, so for now the mechanism is covered only by
``rigc``'s own test fixtures.

A shield device's bus requirement is matched by **exact string**. A
device that needs ``spi-sensors`` is satisfied only by a socket that
offers exactly ``spi-sensors``. There is no fallback to plain ``spi`` and
no choosing between candidates. A :term:`carrier` passing a bus through
works differently. It asks its parent socket for a bus of the same
*kind*, because the name on the carrier's own side is independent of what
the parent calls its bus. If the parent offers more than one bus of that
kind, the pass-through is refused with ``phys-ambiguous-bus`` rather than
resolved by guessing.

Nested carriers keep their own nexus
--------------------------------------

A module plugged into a carrier names its socket
``<carrier instance>.<socket>``. ``rigc`` could resolve such a module's
signals straight to the SoC pin. It doesn't: for every carrier socket in
use, it **synthesizes a nexus node** named
``<carrier instance>_<socket>``. That node's ``gpio-map``, ``pwm-map`` and
``io-channel-map`` rows chain to the parent socket's nexus, and the
module's references go through it. dtc resolves the chain level by level.
The generated overlay therefore looks like a hand-written nested overlay,
treats a carrier socket the same way as a board socket, and keeps the
routing visible: a reader can see that a signal goes through the
carrier's socket, not only where it ends up. Internally, the analyzer
still resolves every position to its SoC pin for conflict detection, so
the synthesized nexus doesn't weaken any check.

A carrier doesn't choose its own cell counts. It inherits them from the
socket it lands on, and a carrier socket that declares a different
``#pwm-cells`` or ``#io-channel-cells`` from its parent is refused with
``phys-subset``.

Routed and unrouted rows
--------------------------

A carrier socket can re-export a position that its parent socket doesn't
route. How ``rigc`` handles that depends on the signal type:

- **GPIO: the row stays socket-local.** A line that doesn't reach a SoC
  pin is still a real net between the carrier and whatever is plugged
  into it, so ``rigc`` tracks it by socket and position instead of by SoC
  pin.
- **PWM and ADC: an unrouted row is an error** (``phys-subset``). An
  analog or timer position without a controller behind it isn't a net;
  it's a mistake.

The same rule applies on a board socket. A shield that uses a position as
PWM or ADC where the socket has no matching map entry is refused with
``phys-function``. On the Lotus, only ``grove_d2``, ``grove_d3`` and
``grove_d4`` carry a ``pwm-map``, and only ``grove_a0`` and ``grove_a1``
carry an ``io-channel-map``. So ``grove_pwm_led`` is accepted on
``grove_d2`` and refused on ``grove_d5``.

Cell counts follow upstream bindings
--------------------------------------

The number of cells in a reference is set by the upstream controller
bindings, not by ``rigc``. ADC controllers are almost uniformly one-cell
(the channel), so ``rigc`` accepts only ``#io-channel-cells = <1>``. PWM
controllers use two forms: (channel, period), as in the Lotus's
``atmel,sam0-tcc-pwm``, and (channel, period, flags), the more common
upstream form. ``rigc`` accepts both. A socket's own count must equal its
controller's, and any other combination is refused with ``phys-board``.

A plug declares no cell counts at all (``lang-shield-plug-cells``). A
position reference through a plug always uses the generic count for its
function: two cells for GPIO, three for PWM, one for ADC.
``grove_pwm_led`` writes
``pwms = <&gpl_plug GROVE_SIG0 20000000 PWM_POLARITY_NORMAL>``, and
``rigc`` translates the reference into the socket's form. That translation
is how the three cells in the shield became the two cells shown above: the
Lotus socket has no flags cell. If a shield puts a nonzero flags value on
a two-cell socket, ``rigc`` refuses it with ``phys-function`` instead of
dropping the value silently.

Pinctrl: select, never author
-------------------------------

Pin multiplexing is SoC knowledge, and it belongs to the board. For a PWM
or ADC use, ``rigc`` does two things: it enables the controller the
position resolved to (``&tcc0 { status = "okay"; };``), and it lists the
pin-mux requirement in the :term:`config sheet`, for example
"grove_d2 SIG0 → PWM tcc0 ch0: mux the pin to the controller". It never
writes a ``pinctrl-*`` property or a SoC pinmux value. A rig chooses and
names pinmux the board already provides; the Lotus board devicetree
supplies its own TCC and ADC pin control. A rig that authored SoC pinmux
would tie itself to one SoC and undo the separation between board and
rig.

Labels: the defining one, and the others
------------------------------------------

Devicetree allows a node to have several labels, and board files often
add more over time. For example, ``grove_sockets.dtsi`` attaches
``adc0: &adc {};`` to the SAMD21's existing ADC node. ``rigc`` therefore
always uses a node's **defining label**, ``labels[0]``, which is the label
given by the node's own declaring file. dtlib only appends labels and
never reorders them, so later composition can't change which label that
is. The rule applies to socket nodes, GPIO controllers, bus controllers
and ``*-map`` targets alike. That is why the Lotus ADC is emitted as
``&adc`` and not ``&adc0``. A socket node without any label is refused,
because rig content refers to sockets by label.

A socket's other labels become **aliases**: a rig's ``socket:`` value is
looked up in the alias index first, then taken as the defining label.
This is what makes a rig independent of the board. A rig names its
sockets by label, and the board comes only from the build invocation (the
:term:`invocation coordinate`). So a rig that says ``socket: grove_d2``
builds on any board whose Grove socket answers to ``grove_d2``. A board
with different names can adopt a shared name by adding that label to its
own socket node, without renaming anything. Checks that must see the
physical socket, such as the rule that a non-stackable Grove socket takes
only one module, are keyed by the *resolved* socket and not by the name
that was written. Otherwise two names for one connector could get past
the check.

Socket inference is convenience only
--------------------------------------

An :term:`instance` may leave out ``socket:``. ``rigc`` then looks for
the single board socket whose type mates the plug. Exactly one candidate
resolves silently. Zero candidates, or more than one, is a
``phys-socket`` error that lists what the board offers. ``rigc`` never
breaks a tie, because any tie-break would choose hardware for the author.
This lets a single-connector board take a shield with no placement
written, as upstream ``--shield`` does. It doesn't replace naming
sockets: the Lotus has nine Grove sockets, so an omitted ``socket:`` there
is always an error.

Inference considers **board sockets only**, never a carrier's exposed
ones. Carrier sockets come from instances, so including them would make
the set of candidates, and therefore the meaning of a rig, depend on the
order in which instances are declared.
