Board socket properties
==========================

Every ``socket,*`` property a typed board socket node may declare, plus
the connector-type binding's own ``plug,*`` extension keys. The authority
is ``scripts/rigc/board/project.py`` (what a real board socket node projects
into), ``scripts/rigc/registry.py`` (what a connector-type binding
declares) and ``scripts/rigc/buskind.py`` (the shared bus-name patterns
both, and the shield-side exposed-socket parser in
``scripts/rigc/loader/shields.py``, read). Every example below is copied
verbatim (only re-indented, or trimmed to the relevant socket, for this
page) from a real board devicetree fragment or connector binding in this
tree.

A shield's exposed socket (a carrier's re-export, documented on
:doc:`shield-template`) is authored inside a ``.shield`` file but carries
the **identical** ``socket,*`` vocabulary described here — everything
below applies to both a real board socket and a carrier's exposed one,
except where noted.

Declaring the connector type
-------------------------------

A node becomes a socket purely by its ``compatible`` starting with
``"socket,"`` — ``scripts/rigc/board/project.py::project_edt`` scans every node
of a board's devicetree for exactly that, keyed by the node's own
defining label (``node.labels[0]``; a socket node with no label at all is
refused outright, ``ValueError`` from ``_project_socket`` — a board
authoring bug, not a rig-content one, so it has no diagnostic code of its
own). The part after the comma names the :term:`connector type`; this
project's own connector-type registry
(``dts/bindings/connectors/*.yaml``) defines four today.

``socket,arduino-r3``
~~~~~~~~~~~~~~~~~~~~~~~

:Where: a board devicetree node.
:Type: ``compatible`` string; the socket is a GPIO nexus (below) shaped
   like the upstream ``arduino-header-r3`` binding.
:Required or optional: this is what opts a board into the ``arduino-r3``
   connector type — 20 claimable positions (``A0``-``A5``,
   ``D0``-``D15``), stackable (see ``socket,stackable`` below).
:Refuses: a shield naming ``shield,plugs = "arduino-r3"`` against a board
   with no matching socket is ``phys-socket`` (documented under "Mating
   multiplicity" below); a shield of a *different* connector type plugged
   explicitly onto an ``arduino-r3`` socket is ``phys-mating``.

Example — ``boards/extend/st/nucleo_f401re/arduino_r3_socket.dtsi``:

.. code-block:: devicetree

   nucleo_ard: arduino_r3: connector_arduino_r3 {
           compatible = "socket,arduino-r3";
           #gpio-cells = <2>;
   };

``socket,grove``
~~~~~~~~~~~~~~~~~~

:Where: a board devicetree node.
:Type: ``compatible`` string; two claimable positions (``SIG0``/``SIG1``).
:Required or optional: not stackable (no ``socket,stackable`` in
   ``dts/bindings/connectors/grove.yaml``) and no ``socket,cs-pool`` at all
   — a Grove socket never exposes SPI/CS.
:Refuses: same as ``socket,arduino-r3`` above.

Example — ``boards/extend/seeed/seeeduino_lotus/grove_sockets.dtsi``:

.. code-block:: devicetree

   grove_d2: connector_grove_d2 {
           compatible = "socket,grove";
           #gpio-cells = <2>;
           gpio-map-mask = <0xffffffff 0xffffffc0>;
           gpio-map-pass-thru = <0 0x3f>;
           gpio-map = <GROVE_SIG0 0 &porta 14 0>, <GROVE_SIG1 0 &porta 9 0>;
   };

``socket,mikrobus``
~~~~~~~~~~~~~~~~~~~~~

:Where: a board devicetree node.
:Type: ``compatible`` string; five claimable positions (``AN``, ``RST``,
   ``CS``, ``PWM``, ``INT`` — ``SCK``/``MISO``/``MOSI``/``RX``/``TX``/
   ``SCL``/``SDA`` exist in the header as bus copper but are not
   independently claimable positions).
:Required or optional: **not** stackable — absence of ``socket,stackable``
   in ``dts/bindings/connectors/mikrobus.yaml`` is itself the type-level
   fact (one module per socket). Its ``socket,cs-pool`` default is a
   single-element pool (``[2]``, the dedicated ``MIKROBUS_CS`` position) —
   present for symmetry with the pool allocator even though there is only
   ever one candidate.
:Refuses: same as ``socket,arduino-r3`` above.

Example — ``boards/extend/mikroe/quail/mikrobus_sockets.dtsi``:

.. code-block:: devicetree

   quail_sock1: mikrobus_1: connector_mikrobus_1 {
           compatible = "socket,mikrobus";
           #gpio-cells = <2>;
           gpio-map = <MIKROBUS_AN   0 &gpioa 6  0>,
                      <MIKROBUS_RST  0 &gpioa 2  0>;
           socket,spi = <&spi1>;
           socket,i2c = <&i2c1>;
           socket,uart = <&usart3>;
   };

``socket,i2c-port``
~~~~~~~~~~~~~~~~~~~~~

:Where: **never a real board node** — this type claims no GPIO positions
   (``plug,positions: {}`` in ``dts/bindings/connectors/i2c-port.yaml``),
   so it only ever appears **shield-synthesized**: an I2C-mux channel or a
   bare I2C port authored inside a ``.shield`` file's own devicetree.
:Type: ``compatible`` string; a bare I2C consumer, no GPIO nexus at all.
:Required or optional: stackable (an I2C bus may host many devices);
   ``socket,cs-pool`` defaults to empty — an I2C port allocates no
   chip-select.
:Refuses: same mating/subset rules as the other three types, applied to a
   shield-synthesized socket instead of a real board one.

Example — ``boards/shields/i2c_mux/i2c_mux.shield`` (four channels of one
TCA9548A mux, each a ``socket,i2c-port`` new scope — see
:doc:`shield-template`'s ``shield,channel`` entry for the full snippet):

.. code-block:: devicetree

   ch0: ch0 { compatible = "socket,i2c-port"; socket,i2c = <&mux>; shield,channel = <0>; };

The GPIO nexus
----------------

``gpio-map`` / ``gpio-map-mask`` / ``gpio-map-pass-thru`` / ``#gpio-cells``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Where: every real board socket node (not ``socket,i2c-port``, which
   claims no positions).
:Type: the standard Zephyr GPIO-nexus quartet — ``gpio-map`` a compound of
   ``<child-specifier &controller parent-specifier>`` rows,
   ``gpio-map-mask``/``gpio-map-pass-thru`` the standard nexus match/pass
   arrays, ``#gpio-cells`` the child specifier's own cell count (always
   ``<2>`` in this project — pin, flags).
:Required or optional: required on every real board socket — this is the
   position → real-SoC-pin mapping every other property in this project
   ultimately resolves through (:term:`position`). ``project_edt`` /
   ``_project_socket`` read it via ``edtlib.Node.maps()``, the standard
   Zephyr nexus mechanism, not a bespoke parser.
:Refuses: not applicable at the property level — a shield claiming a
   position this socket's ``gpio-map`` does not carry surfaces as a net
   with nowhere to route (caught downstream, not by this property
   directly).

Example — ``boards/extend/st/nucleo_f401re/arduino_r3_socket.dtsi``:

.. code-block:: devicetree

   gpio-map-mask = <0xffffffff 0xffffffc0>;
   gpio-map-pass-thru = <0 0x3f>;
   gpio-map = <ARDUINO_HEADER_R3_A0  0 &gpioa 0  0>,
              <ARDUINO_HEADER_R3_A1  0 &gpioa 1  0>;

The PWM/ADC nexuses
----------------------

``pwm-map`` / ``pwm-map-mask`` / ``pwm-map-pass-thru`` / ``#pwm-cells``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Where: a board socket that carries PWM-capable positions (not every
   socket does).
:Type: the same standard nexus shape as ``gpio-map``, targeting a PWM
   controller. ``#pwm-cells`` is checked against a **supported set**
   (``scripts/rigc/board/project.py::_CHANNEL_FN``): 2-cell (channel, period)
   or 3-cell (channel, period, flags) — both real shapes in upstream
   Zephyr's own PWM bindings.
:Required or optional: optional — declared by absence, exactly like
   ``gpio-map`` is not. Not every digital position reaches a timer
   channel; a socket authoring no ``pwm-map`` simply offers no PWM at all
   (``BoardSocket.pwm_map == {}``, ``pwm_cells is None``).
:Refuses: ``phys-board`` (the socket's own ``#pwm-cells``, or the parent
   PWM controller's, declares a cell count outside ``{2, 3}``; or the two
   sides declare *different* counts from each other).

Example — 3-cell, ``boards/extend/st/nucleo_f401re/arduino_r3_socket.dtsi``:

.. code-block:: devicetree

   #pwm-cells = <3>;
   pwm-map-mask = <0xffffffff 0x00000000 0x00000000>;
   pwm-map-pass-thru = <0x00000000 0xffffffff 0xffffffff>;
   pwm-map = <ARDUINO_HEADER_R3_D2  0 0 &pwm1 3 0 0>;

Example — 2-cell (the ``atmel,sam0-tcc-pwm`` shape — no flags cell),
``boards/extend/seeed/seeeduino_lotus/grove_sockets.dtsi``:

.. code-block:: devicetree

   #pwm-cells = <2>;
   pwm-map-mask = <0xffffffff 0x00000000>;
   pwm-map-pass-thru = <0x00000000 0xffffffff>;
   pwm-map = <GROVE_SIG0 0 &tcc0 0 0>, <GROVE_SIG1 0 &tcc0 1 0>;

``io-channel-map`` / ``io-channel-map-mask`` / ``io-channel-map-pass-thru`` / ``#io-channel-cells``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Where: a board socket that carries ADC-capable positions.
:Type: the ADC twin of the PWM nexus above, targeting an ADC controller.
   ``#io-channel-cells`` is checked against a supported set of ``{1}``
   only — upstream ADC bindings are almost uniformly 1-cell.
:Required or optional: optional, declared by absence, identically to
   ``pwm-map``: a socket authoring no ``io-channel-map`` offers no ADC
   reachability at all.
:Refuses: ``phys-board`` (declared cell count is not ``1``, or the
   socket's own count disagrees with the ADC controller's).

Example — ``boards/extend/seeed/seeeduino_lotus/grove_sockets.dtsi``:

.. code-block:: devicetree

   #io-channel-cells = <1>;
   io-channel-map-mask = <0xffffffff>;
   io-channel-map-pass-thru = <0x00000000>;
   io-channel-map = <GROVE_SIG0 &adc0 0>, <GROVE_SIG1 &adc0 1>;

Bus proxies
-------------

``socket,i2c`` / ``socket,spi`` / ``socket,uart`` (bare, or role-qualified ``socket,<kind>-<role>``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Where: a board socket, or a shield's exposed socket node.
:Type: phandle to a bus controller. The bare form (``socket,i2c``) is the
   ordinary case; a connector type may also name an *additional* bus of
   the same kind by suffixing it with a role — ``socket,<kind>-<role>``
   (``socket,spi-sensors``/``socket,spi-motors``) — matched everywhere by
   one shared pattern, ``scripts/rigc/buskind.py::BUS_PROP_RE``.
:Required or optional: every bus endpoint is optional — **subset exposure,
   declared by absence**. A board exposes only the buses it actually
   wires: ``boards/extend/st/nucleo_f401re/arduino_r3_socket.dtsi``
   declares ``socket,i2c``/``socket,spi`` but no ``socket,uart``, and says
   so in its own comment ("no socket,uart: subset exposure, declared by
   absence... neither usart1 nor usart2 is routed"). On a **shield's**
   exposed socket, the same property is either a pass-through
   (``<&plug>``, forwarding the carrier's own bus) or a new scope
   (``<&device>``, rooting a fresh bus scope on one of the shield's own
   devices — an I2C-mux channel).
:Refuses: on a real board socket, nothing directly (absence is the
   mechanism, not an error). A shield needing a bus its resolved socket
   does not expose is ``phys-subset``. On a shield's exposed socket:
   ``lang-exposed`` (the property names neither one of the carrier's
   plugs nor a device of the same shield); ``phys-ambiguous-bus`` (a
   pass-through's parent socket offers *more than one* bus of the
   requested kind — ambiguous, not supported); ``phys-subset`` again (the
   parent socket offers none of the requested kind at all).

Example — board side, ``boards/extend/mikroe/quail/mikrobus_sockets.dtsi``:

.. code-block:: devicetree

   socket,spi = <&spi1>;
   socket,i2c = <&i2c1>;
   socket,uart = <&usart3>;

Example — pass-through, shield side,
``boards/shields/arduino_uno_click/arduino_uno_click.shield``:

.. code-block:: devicetree

   socket,spi = <&auc_plug>;
   socket,i2c = <&auc_plug>;

Example — new scope, shield side, ``boards/shields/i2c_mux/i2c_mux.shield``:

.. code-block:: devicetree

   socket,i2c = <&mux>;

Example — role-qualified (**test-fixture only**; no production board in
this tree authors a named multi-bus socket yet),
``scripts/rigc/tests/unit/board/test_board_project.py`` (``_multibus_edt``):

.. code-block:: devicetree

   socket,spi-sensors = <&spi_a>;
   socket,spi-motors = <&spi_b>;

Chip-select pool
-------------------

``socket,cs-pool`` (bare, or role-qualified ``socket,<kind>-<role>-cs-pool``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Where: a board socket, or a connector-type binding (as a schema
   ``default:``), or a shield's exposed socket.
:Type: an array of ``<u32>`` position indices, in **allocation order** —
   the candidates ``shield,cs-position``-less SPI devices draw from. The
   bare, role-less spelling always means the ``spi`` bus (chip-select only
   ever applies to SPI); a multi-bus connector type's *named* SPI buses
   each get their own ``socket,<kind>-<role>-cs-pool``.
:Required or optional: a board socket authoring none inherits the
   connector type's own binding default (``edtlib`` backfills it — the
   merge in ``scripts/rigc/analyzer/cs.py::effective_cs_pool`` is inert for
   that path). A **shield's synthesized** socket (a carrier's exposed
   node) gets no such backfill at all: authoring nothing there means an
   empty pool, full stop, since a plain ``dtlib`` parse never consults the
   binding's schema default. No production board socket in this tree
   authors an explicit override today — every real one relies on the
   connector type's own default, shown below.
:Refuses: ``phys-cs`` (the pool is exhausted — see
   :doc:`shield-template`'s ``shield,cs-position`` entry).

Example — connector-type default, ``dts/bindings/connectors/arduino-r3.yaml``:

.. code-block:: yaml

   socket,cs-pool:
     type: array
     default: [16, 15, 14]
     description: ordered chip-select candidate positions (D10, D9, D8) for expander CS-pool allocation

Example — role-qualified (**test-fixture only**; no production board
authors a named multi-bus CS pool yet),
``scripts/rigc/tests/unit/board/test_board_project.py`` (``_multibus_edt``):

.. code-block:: devicetree

   socket,spi-sensors-cs-pool = <10>;
   socket,spi-motors-cs-pool = <11>;

Example — a carrier's own override, both bare and qualified forms in one
node (**test-fixture only**; no production carrier authors this yet),
``scripts/rigc/tests/unit/loader/test_shields_exposed.py``
(``test_exposed_socket_cs_pool_qualified_and_bare_both_parse``):

.. code-block:: devicetree

   socket,cs-pool = <3 4>;
   socket,spi-sensors-cs-pool = <5 6>;

Mating multiplicity
----------------------

``socket,stackable``
~~~~~~~~~~~~~~~~~~~~~~

:Where: a connector-type binding's schema (a type-level fact, not a
   per-socket one — every socket of a stackable type is stackable) and,
   correspondingly, every real socket node of that type.
:Type: boolean (a bare, valueless devicetree property).
:Required or optional: optional, and **the presence itself is the fact**:
   its absence means the connector type mates exactly one shield per
   socket (``arduino-r3``/``i2c-port`` declare it; ``grove``/``mikrobus``
   do not — a mikroBUS socket is one module per socket by design, its own
   binding says so directly).
:Refuses: ``phys-mating`` (more than one instance resolves to the same
   physical socket, and its connector type is not stackable).

Example — ``boards/extend/st/nucleo_f401re/arduino_r3_socket.dtsi``:

.. code-block:: devicetree

   socket,stackable;

The connector-type binding's own keys
----------------------------------------

Authored once per :term:`connector type`, in
``dts/bindings/connectors/<type>.yaml`` — the unified socket+plug contract
(the socket-side properties above are also declared here, as the real
edtlib binding; these two are the shield-side extension, opaque to
edtlib's own schema, read directly off the raw YAML by
``scripts/rigc/registry.py``).

``plug,positions``
~~~~~~~~~~~~~~~~~~~~~

:Where: a connector-type binding's top level.
:Type: a mapping of position name → ``{function: gpio|analog, optional:
   bool}``. The name must also appear in the type's own
   ``dt-bindings/connector/<type>.h`` index header — the loader raises a
   plain ``KeyError`` at load time if it does not (an authoring-time
   binding defect, not a rig-content one, so it has no diagnostic code).
:Required or optional: a position absent from this mapping exists in the
   header (real bus copper — SCK/MISO/MOSI, say) but is **not
   claimable**: a shield reference naming it is refused
   (``lang-position``, "bus copper, not a claimable position"). Each
   entry's own ``optional: true`` sub-key is parsed into
   ``model.Position.optional`` (``scripts/rigc/registry.py``) but —
   confirmed while re-deriving this page — nothing else in the loader or
   analyzer reads that field back out; it is authored metadata with no
   observable effect today, on the one position that carries it
   (mikroBUS's ``PWM``).
:Refuses: ``lang-position`` (a reference claims an index that either does
   not exist in the header at all, or exists there but is not one of
   these claimable positions).

Example — ``dts/bindings/connectors/mikrobus.yaml``:

.. code-block:: yaml

   plug,positions:
     AN:  {function: analog}
     RST: {function: gpio}
     CS:  {function: gpio}
     PWM: {function: gpio, optional: true}
     INT: {function: gpio}

``plug,bus-proxies``
~~~~~~~~~~~~~~~~~~~~~~~

:Where: a connector-type binding's top level.
:Type: an array of bus-proxy names (``["i2c", "spi", "uart"]``,
   ``["i2c"]``, ...) — the group names a shield of this connector type may
   use for a bus-scoped device group.
:Required or optional: names the **complete set** a shield of this type
   may nest a bus device group under; a shield group whose name is
   bus-shaped (matches ``scripts/rigc/buskind.py::bus_kind_of``) but is not
   in this list is refused. An empty list restricts a shield of that type
   to exactly those proxies — ``i2c-port.yaml``/``grove.yaml`` both
   declare only ``[i2c]``, so a Grove module may never declare a
   ``spi``/``uart`` group.
:Refuses: ``lang-shield-proxy`` (a shield group named after a bus kind
   this connector type's binding does not list).

Example — ``dts/bindings/connectors/arduino-r3.yaml``:

.. code-block:: yaml

   plug,bus-proxies: [i2c, spi, uart]
