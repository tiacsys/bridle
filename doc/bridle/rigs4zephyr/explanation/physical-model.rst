.. _rigs4zephyr_explanation_physical-model:

The physical model rigc checks against
========================================

A ``phys-*`` diagnostic is a claim about copper: this rig, assembled as
written, cannot work. :ref:`rigs4zephyr_reference_diagnostics` lists every
such claim by code. This page explains the model behind them — what
:term:`rigc` treats as the basic physical facts of a
:term:`rig`, why sharing and conflicts are *computed* from those facts
rather than declared, and where the model deliberately stops.

Nets are the primitive
------------------------

The smallest thing ``rigc`` reasons about is a *net*: one piece of copper
that is electrically the same everywhere it reaches. Sockets, plugs,
positions and buses are all structure laid over nets. A :term:`socket`'s
``gpio-map`` says which net each of its :term:`position`\ s lands on, and a
device in a :term:`shield template` says which position it uses; neither
statement mentions the other, and ``rigc`` joins them.

What identifies a net is the SoC pin it reaches, not the socket position
that named it. The analyzer resolves every claimed position through the
socket's ``gpio-map`` down to a controller and pin, and uses that pair as
the net's key. Two positions on two *different* sockets that the board
routes to the same pin therefore key to the same net, and every claim on
either of them lands in the same list.

The Seeeduino Lotus shows why this matters. Its Grove sockets are
daisy-laced: the second signal of each digital socket is the first signal
of the next one (``boards/seeed/seeeduino_lotus/grove_sockets.dtsi``).

.. graphviz::

   digraph lotus_lacing {
      rankdir=LR;
      node [shape=box, fontname="sans-serif", fontsize=10];
      edge [fontname="sans-serif", fontsize=9];

      subgraph cluster_sockets {
         label="Grove sockets"; style=dashed;
         d2 [label="grove_d2"];
         d3 [label="grove_d3"];
         d4 [label="grove_d4"];
      }
      subgraph cluster_pins {
         label="SoC pins (net keys)"; style=dashed;
         pa14 [label="porta 14", shape=ellipse];
         pa9  [label="porta 9",  shape=ellipse];
         pa8  [label="porta 8",  shape=ellipse];
         pa15 [label="porta 15", shape=ellipse];
      }
      d2 -> pa14 [label="SIG0"];
      d2 -> pa9  [label="SIG1"];
      d3 -> pa9  [label="SIG0"];
      d3 -> pa8  [label="SIG1"];
      d4 -> pa8  [label="SIG0"];
      d4 -> pa15 [label="SIG1"];
   }

A module on ``grove_d3`` using ``GROVE_SIG0`` and a module on ``grove_d2``
using ``GROVE_SIG1`` sit on different sockets and use differently named
positions, yet both claim ``porta 9``. No rig author and no shield author
wrote down that the two share anything, and neither needs to: the sharing
is a consequence of the board's own ``gpio-map`` rows, and ``rigc`` finds
it by comparing net keys. A model that keyed nets by *(socket, position)*
would see two unrelated lines and accept the rig.

The same key is what catches conflicts across :term:`carrier` layers. A
carrier's exposed socket is composed against the socket the carrier itself
is plugged into, so its positions resolve to the same SoC pins the board
socket underneath reaches. A chip-select a module claims two carriers deep
and a GPIO a module claims directly on the board socket compare equal as
soon as they reach the same pin, whatever path each took to get there.

One consequence of keying on the resolved pin is that a position the
board's ``gpio-map`` does *not* route has no pin to key on. Such a position
stays socket-local — a net of its own, keyed by socket and position — so
two sockets can never be found to share it.

Functions belong to endpoints, not nets
------------------------------------------

A net has no function of its own. The same pin is a GPIO, a PWM output or
an ADC input depending on how the SoC muxes it; what differs is the
*endpoint* a device attaches to the net with. A shield template picks the
function by which property it writes — ``gpios``, ``pwms`` or
``io-channels`` — and ``rigc`` resolves the position through the socket's
matching nexus: ``gpio-map``, ``pwm-map`` or ``io-channel-map`` (see
:ref:`rigs4zephyr_reference_board-socket`). A PWM or ADC reference to a
position the socket offers no such nexus row for is refused as
``phys-function``.

A PWM or ADC claim registers on **two** things. The first is the pin, as
an exclusive claim: a pin driven by a timer cannot also be someone's GPIO.
The second is the controller channel, keyed by controller and channel
number, also exclusive: two consumers cannot share one timer or ADC
channel, even when they reach it through different pins. On the Lotus,
``grove_d2`` and ``grove_d4`` put ``GROVE_SIG0`` on different pins
(``porta 14`` and ``porta 8``) but both route it to channel 0 of ``tcc0``.
Two PWM LEDs on those two sockets never touch the same copper, and are
still refused, as ``phys-channel``, because the claim on the channel
collides. ``lotus_pwm_led`` uses ``grove_d2`` and ``grove_d3`` for that
reason.

Every claim also carries a *role* on its net, and the final net check reads
the roles:

- Two exclusive claims on one key are refused — ``phys-channel`` when the
  key is a controller channel, ``phys-cs`` when it is a pin.
- One exclusive claim plus any other claim on the same net is refused as
  ``phys-net``: an exclusive resource cannot also carry a shared signal.
- More than one *driver* on a net is refused as ``phys-net``. One driver
  and any number of listeners, or an MCU-driven line with several
  listeners, is an ordinary shared net and is accepted.

The role of a GPIO claim is inferred from the property name: a property
named for an interrupt (``int``, ``irq``) makes the device a driver,
anything else makes it a listener. PWM, ADC and chip-select claims are
always exclusive. Because roles come from names, two plain ``gpios``
claims on one net are both listeners and are accepted, even when the
hardware behind them drives the line. Open-drain wired-AND sharing is not
modelled either: two interrupt outputs on one net are refused even when
wiring them together would be electrically fine.

Addressing mode is a second axis
-----------------------------------

How many nets a link uses says nothing about how several targets share it.
That is a separate axis, the *addressing mode*, and it decides which check
applies:

.. list-table::
   :widths: 22 24 54
   :header-rows: 1

   * - Addressing
     - Regime
     - What ``rigc`` checks
   * - none (GPIO, PWM, ADC)
     - dedicated
     - The net claims above. Attaching means taking the line, so the
       claim check is the whole story.
   * - in-band (I²C)
     - shared bus
     - Address-set feasibility per address scope. A copper-fixed ``reg``
       wins outright, a strap the rig pins must name an address in the
       strap's domain (``phys-pin``), a free strap takes the first address
       still unclaimed, and two devices on one address — or a free
       strap with nothing left — is ``phys-addr``. Chosen strap states go
       to the :term:`config sheet`.
   * - out-of-band (SPI)
     - shared pool
     - Chip-select allocation per SPI scope. Each target needs a CS
       line of its own, so ``rigc`` gives it the first candidate of the
       socket's ordered ``socket,cs-pool`` whose net is still unclaimed.
       A copper-fixed ``shield,cs-position`` takes its line without
       consulting the pool. Each placement becomes an exclusive net claim,
       so a CS that lands on a pin someone else already uses is caught by
       the same net check as everything else.

Because a pool candidate is skipped when its *net* is already claimed, the
allocator routes around a pin that a GPIO claim, or a chip-select on
another socket, already holds. A copper-fixed CS cannot be routed around:
if its pin is taken, the rig is refused. Any other claim — on the pin, a
channel or an address — is not allocated. If it does not fit, the rig is
refused, never quietly moved.

UART sits in the dedicated row in principle, but ``rigc`` does not check
it today: a UART-needing module is checked for whether its socket exposes
``socket,uart`` (``phys-subset``), and two modules on one UART controller
reached through two different sockets are not detected. Bus lines
themselves — SDA, SCL, SCK, MOSI, MISO — are not claimable positions
(``lang-position``), so a GPIO claim on a pin the board also uses as bus
copper does not appear as a net conflict.

Scopes: pass-through keeps nets, scope creation makes new copper
--------------------------------------------------------------------

Carriers come in two electrically different kinds, and the model treats
them differently:

- A **pass-through** exposed socket binds its positions to the same nets
  as the carrier's own plug, possibly reordered or renamed, and forwards
  the parent's bus as-is. Net identity survives the carrier, so every
  claim behind it is checked against every claim in front of it.
- A **scope-creating** exposed socket — one channel of an I²C multiplexer,
  marked with ``shield,channel`` and a ``socket,<bus>`` pointing at the mux
  device rather than at a plug — is new copper. The bus behind a mux
  channel is not electrically the parent bus, so it is a scope of its own:
  addresses there are unique within the channel only. The same fixed
  address is legal once on each channel. The mux device itself sits on
  the parent bus and takes its address there, like any other device.

Address and chip-select scopes are keyed on the **bus path**, never on the
bus kind. A pass-through bus carries the parent controller's devicetree
path, so two sockets whose ``socket,i2c`` reaches the same controller are
one scope, and a fixed address repeated across them is ``phys-addr``. Two
independent SPI buses on one socket are two scopes with separate CS pools.
A mux channel's path is its own ``<carrier>.<channel socket>`` reference,
shared by every module plugged into that channel. Because the key is the
physical bus, two sockets that name one controller through different
labels still share a scope, and two controllers of the same kind never
do.

For the vocabulary behind each carrier kind, see
:ref:`rigs4zephyr_reference_shield-template` ("Carriers and exposed
sockets") and :ref:`rigs4zephyr_reference_board-socket` ("Bus proxies").

The devicetree is the MCU's projection of the rig
----------------------------------------------------

A rig is more than any single file ``rigc`` produces. The overlay is the
rig as the MCU sees it: which devices it can reach, through which
controllers, behind which mux channels, at which addresses and
chip-selects. Everything in that view becomes an ordinary devicetree
construct — nexus nodes, ``cs-gpios``, ``reg``, mux channel nodes — so the
Zephyr build downstream sees nothing it would not see in a hand-written
overlay.

What the MCU cannot see, a person has to do by hand: plug each module into
the socket the solution assumed, set each address strap and
:term:`routing jumper` to the state the allocator chose, lay any ad-hoc
wire. That set is the complement of the projection, and it is exactly what
the :term:`config sheet` records. The two outputs are two halves of one
solved rig, split by what the MCU can observe. A third,
``expectations.yml``, names what can only be confirmed by running the
image on real hardware. It is emitted for every accepted rig, but no test
checks its contents yet.

A board is the PCBA whose MCU runs this image
------------------------------------------------

Several PCBAs in a rig may carry processors of their own — a Wi-Fi module
with its own firmware is still a shield. What makes one PCBA *the board*
is not that it has an MCU, but that its MCU runs the image this build
produces. That MCU is where the projection is taken from, and every
devicetree node the overlay adds is a node in that image's tree.

This is also why the model holds exactly one board, and why the board
comes from the :term:`invocation coordinate` rather than from the rig
files. Rigs with two boards or two images — two MCUs cabled together, or a
dual-core part building one image per core — would need one projection
per image. The model does not cover them.

Where the model ends
-----------------------

The model assumes single-ended nets and point-in-time attachment, and
stops at a handful of known edges. None of the following is checked;
a rig that depends on them is accepted or refused on the facts the model
does cover, and nothing more:

- **Differential pairs and lanes.** CAN, USB, Ethernet and MIPI links
  attach as pairs or lanes, not as single nets. ``rigc`` has no grouped-net
  concept and no lane-width matching.
- **Bus-wide constraints.** Termination count on a CAN bus (exactly two),
  or a parameter that every endpoint on a bus must agree on (a CAN
  bitrate), has no representation. An SPI-attached CAN controller is an
  ordinary SPI device to ``rigc``; the CAN bus behind it is not modelled.
- **In-path devices.** Transceivers and PHYs sit *in* a link, changing its
  electrical form without adding addresses. Nothing in the model
  represents a device between a controller and its bus.
- **Ad-hoc wires as nets.** A ``wires:`` entry joins two pads and is
  checked for exactly one driver (``phys-wire``), but the wire's endpoints
  are not merged into the net map, so a wire is not compared against the
  claims made through sockets.
- **Power, ground, and pin-mux.** Voltage domains, current budgets and
  whether the board's pinctrl can actually select the requested function
  on a pin are not checked. The board supplies the pinctrl fragments; the
  config sheet lists the PWM/ADC controllers a rig relies on so a person
  can confirm them.

Why a rig fails as ``phys-*`` rather than ``lang-*``
------------------------------------------------------

The split between the two diagnostic families follows from this model.
A ``lang-*`` code is raised before any board is read: the files are
malformed, a reference dangles, a device is missing its address authority.
A ``phys-*`` code can only be raised once the board's devicetree is in
hand, because every fact the checks above run on — which pin a position
reaches, which controller a bus proxy names, which channel a PWM row
selects — comes from the board. The same rig can be ``phys``-clean on one
board and refused on another, which is exactly what should happen when
two boards route their sockets differently. The full list is in
:ref:`rigs4zephyr_reference_diagnostics`; the reasoning behind cutting the
pipeline along that line is in :ref:`rigs4zephyr_explanation_architecture`.
