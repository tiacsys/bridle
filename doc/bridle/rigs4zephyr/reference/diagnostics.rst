.. _rigs4zephyr_reference_diagnostics:

Diagnostic codes
==================

Every diagnostic :term:`rigc` can print, by code. **Forty-four**
today — thirty ``lang-*`` and fourteen ``phys-*`` — derived straight from
``scripts/rigc/``'s own construction sites (every ``error(...)``/
``warning(...)`` call in production source, never the golden test
fixtures, whose *directory names* happen to reuse some of the same
strings). ``test_diagnostics_reference_drift.py`` keeps this page and
that source in sync, in both directions: a new call site with no entry
here fails the test suite, and so does an entry naming a code no source
line raises any more.

Each entry names the pipeline stage that raises it (see
:ref:`rigs4zephyr_reference_api_index` for what each stage does) and what to check
first. The severity in ``error[code]``/``warning[code]`` is fixed per
call site, not per code — a handful of codes below are raised as a
warning at one site; that is called out where it applies.

.. contents::
   :local:
   :depth: 1


The two ways a rig can be wrong
----------------------------------

:ref:`rigs4zephyr_explanation_architecture` explains *why* the pipeline is cut where
it is; the short version a diagnostic code encodes directly: a ``lang-*``
code is something wrong with the rig's or shield's *files* — a dangling
reference, an illegal axis, a shape YAML never declared — caught by the
:ref:`rigs4zephyr_reference_api_loader` before a board is ever read. A ``phys-*``
code is something wrong with the *hardware* the files describe — two
devices at one address, a connector that doesn't mate, a chip-select pool
with nothing left — caught by the :ref:`rigs4zephyr_reference_api_board` reader or
the :ref:`rigs4zephyr_reference_api_analyzer` once a real board devicetree is in
hand. Neither check can substitute for the other: a ``lang-*`` pass never
sees a board, and a ``phys-*`` pass never re-derives a fact the loader
already settled.


``lang-*`` — an authoring error in the rig or shield source
----------------------------------------------------------------

.. list-table::
   :widths: 20 12 68
   :header-rows: 1

   * - Code
     - Stage
     - Meaning, and what to check
   * - ``lang-addr-authority``
     - :ref:`rigs4zephyr_reference_api_loader`
     - An addressable-bus (I2C) device carries both ``reg`` and
       ``shield,addr-from``, or neither — exactly one is required (the
       address-authority rule: copper-fixed, or rig-selectable, never
       both, never neither). Check the device node's ``reg``/
       ``shield,addr-from`` pair.
   * - ``lang-addr-from``
     - :ref:`rigs4zephyr_reference_api_loader`
     - A device's ``shield,addr-from`` phandle does not point at a config
       strap of the same shield. Check the phandle's target node.
   * - ``lang-config``
     - :ref:`rigs4zephyr_reference_api_loader`
     - An instance's ``config:`` block names a config element (strap or
       jumper) the shield does not declare. Check the label against the
       shield's own straps/jumpers, listed in the message.
   * - ``lang-connector-root``
     - :ref:`rigs4zephyr_reference_api_loader`
     - No ``--connector-dir`` was given and the built-in dev/test
       fallback directory does not exist. A real build always threads
       ``--connector-dir`` explicitly (see :ref:`rigs4zephyr_reference_commands`); this fires
       only for a standalone invocation missing it, or a workspace where
       ``rigc``'s own source has moved. Check that ``--connector-dir`` is
       passed.
   * - ``lang-content``
     - :ref:`rigs4zephyr_reference_api_loader`
     - No content file (``<rig-name>.yml``) exists beside ``rig.yml``.
       Check the path the message names.
   * - ``lang-cpp``
     - :ref:`rigs4zephyr_reference_api_loader`
     - The C preprocessor failed (non-zero exit) while building a
       shield's translation unit — an unresolvable ``#include``, a macro
       error. Check gcc's own stderr, embedded verbatim in the message,
       and the ``--include-dir`` search path.
   * - ``lang-dt-include``
     - :ref:`rigs4zephyr_reference_api_loader`
     - Either a ``shield,param-includes`` header named on a device does
       not exist or fails to preprocess, or a ``params:``/``config:``
       value does not resolve against any header the device's
       ``shield,param-includes`` actually lists. Check the header name on
       the device node, and that the assigned token is genuinely defined
       there.
   * - ``lang-exposed``
     - :ref:`rigs4zephyr_reference_api_loader`
     - A carrier's exposed-socket declaration is malformed: a
       gpio-map/pwm-map/adc-map/bus-proxy row's phandle does not target
       one of the carrier's own plugs, a ``#<fn>-cells`` declaration is
       missing its matching ``-map`` property (or vice versa), a row is
       truncated, or a bus-proxy names a bus the exposed connector type
       does not declare. Check the exposed socket node's map/cells
       properties and phandle targets.
   * - ``lang-instance-shield``
     - :ref:`rigs4zephyr_reference_api_loader`
     - An instance's ``shield:`` reference names a shield the library
       never scanned. Check the name against the message's own "known
       shields" list, and the ``--shield-dir`` roots actually searched.
   * - ``lang-instance-socket``
     - :ref:`rigs4zephyr_reference_api_loader`
     - An instance's ``socket:``/``sockets:`` key is malformed: both
       given at once, ``socket:`` used on a multi-plug shield (or
       ``sockets:`` on a single-plug one), or a ``sockets:`` map naming a
       slot the shield does not declare. Check the key against the
       shield's own plug count.
   * - ``lang-parse``
     - :ref:`rigs4zephyr_reference_api_loader`
     - ``dtlib`` itself failed to parse the preprocessed shield
       translation unit — a devicetree syntax error in the shield's own
       ``.shield`` source, or in something it ``#include``\ s. Check the
       file dtlib flagged and the line the message names; a plain syntax
       mistake (a missing brace, a stray property) is the common cause.
   * - ``lang-pad-role``
     - :ref:`rigs4zephyr_reference_api_loader`
     - A pad's ``shield,role`` is not one of ``driver``/``listener``/
       ``bidir``. Check the role value.
   * - ``lang-param``
     - :ref:`rigs4zephyr_reference_api_loader`
     - A ``params:`` block names a device the shield does not have, or a
       property the device does not declare (``shield,params``); a
       required parameter (no default) was left unassigned; or a delta
       supplies some of a device's params without restating one the
       effective topology already assigns. Check the device label and
       property name against the shield's own declared parameters, both
       listed in the message.
   * - ``lang-pos-ref``
     - :ref:`rigs4zephyr_reference_api_loader`
     - A ``gpios``/``pwms``/``io-channels`` reference is malformed (wrong
       cell count), or its phandle does not target one of the shield's
       own plug nodes (or a jumper, for gpio). Check the phandle target.
   * - ``lang-position``
     - :ref:`rigs4zephyr_reference_api_loader`
     - A claimed position index does not exist on the plug's connector
       type, or names bus copper rather than a claimable position
       (electrical realization is not modeled). Check the index against
       the connector type's declared positions.
   * - ``lang-promote-opts``
     - :ref:`rigs4zephyr_reference_api_cli`
     - A ``--promote``/``-DRIG=`` promotion target's option grammar
       failed to parse — the ``;``-separated list, or the ``:``-separated
       ``socket=``/``config.<label>=``/etc. assignments. Check the target
       string itself against the grammar in :ref:`rigs4zephyr_reference_promotion`.
   * - ``lang-prop``
     - :ref:`rigs4zephyr_reference_api_loader`
     - **Warning.** A device property has a phandle type that is not a
       recognized function ref, or a type the prototype cannot pass
       through — it is dropped from the emitted output rather than
       rejecting the whole shield. Check whether the dropped property was
       load-bearing.
   * - ``lang-rev``
     - :ref:`rigs4zephyr_reference_api_loader`
     - Anything about the ``revision:``/``revisions:`` axis: a revision
       id that does not match the declared ``format:``, an unknown or
       undeclared selection, no default when none was selected, a
       selected non-default revision whose fragment files do not exist,
       or a delta stage naming an instance a later stage already removed.
       Check the axis declaration and the requested revision id against
       the "known revisions" the message lists.
   * - ``lang-schema``
     - :ref:`rigs4zephyr_reference_api_loader`
     - The generic malformed-YAML catch-all: a required key missing, a
       value of the wrong shape (a scalar where a mapping was needed, a
       list that is not a list, a duplicate name declared twice), a wire
       missing ``route:``. Check the YAML at the anchored line — the
       message spells out exactly which key or shape is wrong.
   * - ``lang-shield-label``
     - :ref:`rigs4zephyr_reference_api_loader`
     - A rig-facing node (plug, pad, strap, jumper, ...) has no DTS
       label. Every rig-facing reference (``config:``/``wires:``/
       ``socket:``) resolves by label, never by node name. Check that the
       node has one.
   * - ``lang-shield-name``
     - :ref:`rigs4zephyr_reference_api_loader`
     - A ``.shield`` translation unit defines no top-level shield node
       whose *name* matches the identity shield discovery expects (the
       ``shield.yml``-declared name, or the folder name when there is no
       ``shield.yml``). Check the node name(s) actually defined, listed
       in the message, against what names the shield.
   * - ``lang-shield-plug``
     - :ref:`rigs4zephyr_reference_api_loader`
     - Either ``shield,plugs`` is authored on the shield's TEMPLATE node
       (a retired spelling — it belongs on the plug node itself), or the
       shield declares no ``shield,plug``-compatible child at all. Check
       that ``shield,plugs`` sits on a child node with
       ``compatible = "shield,plug"``.
   * - ``lang-shield-plug-cells``
     - :ref:`rigs4zephyr_reference_api_loader`
     - A plug node declares a ``#<fn>-cells`` count of its own
       (``#gpio-cells``, ``#pwm-cells``, ``#io-channel-cells``) — a plug
       node never does; only a node that genuinely differs (a routing
       jumper) does. Check for a stray cell-count property on the plug
       node.
   * - ``lang-shield-plurality``
     - :ref:`rigs4zephyr_reference_api_loader`
     - A shield with more than one plug declares a routing jumper
       (``shield,position-domain``) — the position domain has no plug
       axis to be relative to on a multi-plug shield. Check the jumper
       node against the shield's plug count.
   * - ``lang-shield-proxy``
     - :ref:`rigs4zephyr_reference_api_loader`
     - A bus-proxy-shaped group (uart/spi/i2c/...) sits at template level
       instead of nested under its owning plug, a plug's binding does not
       allow the bus kind nested under it, or a plain (non-bus) group is
       nested under a plug instead of staying at template level. Check
       where the group node sits in the ``.shield`` tree, and the plug's
       declared bus proxies.
   * - ``lang-shield-template``
     - :ref:`rigs4zephyr_reference_api_loader`
     - ``shield.yml`` declares an entry with ``template: true`` but the
       matching ``<name>.shield`` file does not exist beside it. Check
       that the promotable entry has its own ``.shield`` file.
   * - ``lang-shield-type``
     - :ref:`rigs4zephyr_reference_api_loader`
     - A plug declares no ``shield,plugs`` of its own, or names a
       connector type the registry does not know. Check the plug's
       ``shield,plugs`` value against the known connector types listed in
       the message — a typo, or a missing ``--connector-dir``.
   * - ``lang-unit-addr``
     - :ref:`rigs4zephyr_reference_api_loader`
     - A node's ``@<unit-address>`` does not match its authored ``reg``
       (error), or a symbolic unit-address does not name its own
       ``shield,addr-from`` resolver (**warning** — a lint, not a
       rejection). Check the unit-address against ``reg`` or the
       ``addr-from`` target.
   * - ``lang-variant``
     - :ref:`rigs4zephyr_reference_api_loader`
     - Anything about the ``variant:``/``variants:`` axis: an unknown or
       undeclared selection, no default when none was selected, a
       selected non-default variant whose fragment files do not exist,
       two axis values that would construct the same fragment stem, or a
       delta stage naming an instance a later stage already removed.
       Check the axis declaration and that the selected value actually
       has a fragment file backing it.
   * - ``lang-wire-ref``
     - :ref:`rigs4zephyr_reference_api_loader`
     - A wire endpoint (``<instance>.<node>``) does not parse, names no
       such instance, names a node the shield does not have, or is
       ambiguous (matches more than one node). Check the instance/node
       name in the wire's ``from``/``to`` against the instance list and
       the shield's own referencable node names, both printed in the
       message.


``phys-*`` — a physical or topological impossibility
---------------------------------------------------------

.. list-table::
   :widths: 20 12 68
   :header-rows: 1

   * - Code
     - Stage
     - Meaning, and what to check
   * - ``phys-addr``
     - :ref:`rigs4zephyr_reference_api_analyzer`
     - Two devices resolve to the same I2C address in one address scope
       (a bus, or a mux channel), or a free-allocating device's strap
       domain is exhausted — every address already claimed. Check the
       conflicting devices/addresses the message names; fix by moving one
       behind a mux, using a second bus, or dropping an instance.
   * - ``phys-ambiguous-bus``
     - :ref:`rigs4zephyr_reference_api_analyzer`
     - A carrier's pass-through bus resolves to more than one candidate
       bus of the same kind on the named parent socket — ambiguous
       pass-through is not supported. Check the candidates listed;
       disambiguate by giving the parent socket only one bus of that
       kind, or choose a different parent slot.
   * - ``phys-board``
     - :ref:`rigs4zephyr_reference_api_board`
     - Everything about whether the named board can be read at all: no
       board was given (checked by the :ref:`rigs4zephyr_reference_api_cli` itself,
       before the board reader ever runs — a rig names no board of its
       own), the name does not resolve to any devicetree, the devicetree
       exists but declares no ``socket,*`` node (not rig-enabled), no
       build recipe was available to read it, or a socket's PWM/ADC nexus
       declares a cell count ``rigc`` does not support. Check the board
       name/``--board-dts`` path, and whether its devicetree actually
       declares typed sockets.
   * - ``phys-channel``
     - :ref:`rigs4zephyr_reference_api_analyzer`
     - Two consumers need the same PWM/ADC controller channel — a channel
       is exclusive, unlike a shared GPIO net. Check the claims listed;
       use a different socket/channel, or one device.
   * - ``phys-cs``
     - :ref:`rigs4zephyr_reference_api_analyzer`
     - A chip-select pool is exhausted for a scope member, a CS position
       has no gpio-map entry the board can route, or two exclusive claims
       resolve to the same SoC pin. Check the CS pool/candidates the
       message names against what is already claimed.
   * - ``phys-function``
     - :ref:`rigs4zephyr_reference_api_analyzer`
     - A PWM/ADC function reference targets a socket position that offers
       no such channel (no ``pwm-map``/``io-channel-map`` entry), or
       authors PWM flags on a 2-cell (channel, period) socket that has no
       cell to carry them. Check the socket's own PWM/ADC map at that
       position.
   * - ``phys-label``
     - :ref:`rigs4zephyr_reference_api_analyzer`
     - The deterministic ``<instance>_<shield-label>`` output-label
       scheme collides between two devices in the rig. Check the message
       for the two instances producing the same label; rename one.
   * - ``phys-mating``
     - :ref:`rigs4zephyr_reference_api_analyzer`
     - A resolved socket's connector type does not match the shield's
       plug type (the connectors do not mate), or more than one instance
       mates a non-stackable socket. Check the socket's/plug's connector
       type, and whether that type is genuinely stackable.
   * - ``phys-net``
     - :ref:`rigs4zephyr_reference_api_analyzer`
     - A resolved net (a shared SoC pin or controller channel) has more
       than one driver, or an exclusively-claimed net is also claimed as
       a shared signal. Check every claim line the message lists against
       that one physical net.
   * - ``phys-pin``
     - :ref:`rigs4zephyr_reference_api_analyzer`
     - A rig-pinned strap selection names an address that is not in the
       strap's own domain — the copper cannot select it. Check the pinned
       address against the strap's declared domain, both printed.
   * - ``phys-position``
     - :ref:`rigs4zephyr_reference_api_analyzer`
     - A routing jumper's position was never selected (``config:``
       needed), or the selected position is not in the jumper's own
       domain. Check the jumper's ``config:`` entry against its position
       domain, printed in the message.
   * - ``phys-socket``
     - :ref:`rigs4zephyr_reference_api_analyzer`
     - Socket resolution failed outright: no board socket (or none
       unambiguous) mates the shield's plug type, an explicitly-named
       ``socket:``/carrier-exported socket does not exist, socket nesting
       is cyclic, or two distinct plug slots of one instance resolved to
       the same physical socket. Check the board's own socket list
       (printed) and the instance's ``socket:``/``sockets:`` value.
   * - ``phys-subset``
     - :ref:`rigs4zephyr_reference_api_analyzer`
     - A shield's devices need a bus the resolved socket does not expose
       — subset exposure is declared by absence — or, for a carrier, a
       pass-through/PWM/ADC-map row's declared cell count or routed
       position does not match what the named parent socket actually
       offers. Check the socket's declared ``socket,<bus>`` set, or the
       carrier's exposed-socket cell counts, against the parent.
   * - ``phys-wire``
     - :ref:`rigs4zephyr_reference_api_analyzer`
     - A ``wires:`` entry's endpoint is not a wireable pad, a net has
       other than exactly one driver, a ``route: via <name>`` targets an
       instance that plugs more than one socket, or the named position
       does not exist on the connector type. Check the wire's endpoints
       and its ``route:`` value.
