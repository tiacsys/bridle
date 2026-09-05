# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Shield parsing: a `.shield` translation unit -> model.Shield.
Loader-side validation done here:

  - shield,plugs names a known connector type
  - bus proxy nodes are allowed by the plug binding
  - position references target one of THIS shield's plugs and exist in
    that plug's connector type
  - exactly one of reg / shield,addr-from on addressable-bus devices
    (forgot-vs-deferred: address authority rule)
  - authored reg matches the unit-address; symbolic unit-addresses are
    linted against the addr-from target

**ONE authored form**: N plug nodes, N >= 1, each a child of the
template with `compatible = "shield,plug"` and its own `shield,plugs`
naming that plug's connector type. The child's NODE NAME is the slot
name (shield-owned); `plug` is the conventional name for a shield with
one, and carries no special meaning. Plurality is a COUNT, never an
authored form -- which is what every consumer below this module always
tested (`len(shield.plugs) > 1`).

Placement, the same rule at either count:

  bus groups NEST UNDER their owning plug node -- that nesting is what
    dissolves the sibling-name collision two same-kind buses would
    otherwise have; a bus-shaped group at template level is rejected.
  plain (non-bus) device groups stay at TEMPLATE level, plug-agnostic --
    their devices' refs each carry their own plug by phandle ("one of
    this shield's plugs"); a plain group nested under a plug is
    rejected. With exactly one plug, such a device is attributed to it;
    with more, to none.

  `pads` and `config` are template-level too, whatever the plug count:
    they are shield-level facts. Promotion and routing jumpers are
    refused above one plug -- straps are unaffected (bus-scoped, not
    plug-scoped). A carrier of any plug count may declare an exposed
    socket: its gpio-map rows and socket,<bus> properties each resolve
    through one of the carrier's plugs, exactly like a device's own
    cross-plug refs.

**A plug node declares no cell counts.** `#gpio-cells`/`#pwm-cells`/
`#io-channel-cells` are refused there: every value the corpus ever gave
one was `_FUNCTION_DEFAULT_CELLS` restated, the node is never emitted so
nothing validates it, and a wrong value silently changed a reference's
arity. The `_ncells` mechanism stays for the nodes that genuinely
differ -- a routing jumper's own `<1>`.

**Diagnostics are RETURN values**: every parse function below returns
(value, diagnostics) rather than writing into a diags parameter handed
in from outside -- the local list a function builds and returns is not
the banned accumulator shape (nothing outside this module ever mutates
one), it is composition-by-return exactly like every other rigc module.

**The cpp/unit-test seam**: everything here operates on a `dtlib.DT`
that ALREADY EXISTS -- it never calls cpp itself -- so it is
unit-testable directly against a synthetic, cpp-free `.dts` text parsed
with `dtsio.get_dtlib().DT(path)`."""

from __future__ import annotations

from typing import Any

from ..buskind import BUS_PROP_RE as _BUS_PROP_RE
from ..buskind import CS_POOL_PROP_RE as _CS_POOL_PROP_RE
from ..buskind import bus_kind_of, is_bus_kind
from ..diag import Diagnostic, error, warning
from ..dtsio import get_dtlib, render_prop, src_of, words
from ..model import ConnectorType, Device, ExposedSocket, FunctionRef, Jumper, Pad, Shield, Strap

#: socket,<kind> or socket,<kind>-<role> -- an exposed socket's own bus
#: vocabulary is the qualified multi-bus pattern, the same shared pattern
#: board/project.py/registry.py read off their own inputs (a connector type's
#: bus names mean the same thing on either side of a pass-through) --
#: see buskind.py for the regex itself and why it lives there.
#:
#: socket,<kind>-<role>-cs-pool -- a named bus's own authored cs-pool
#: override on an exposed socket node, keyed the same qualified way. The
#: legacy, role-less "socket,cs-pool" (every carrier's own spelling
#: today) is handled separately below: it carries no kind in its own
#: name, so it is not this pattern's concern.

#: template-level group names that are NOT device groups. `plug` is
#: deliberately absent: a plug node is recognized structurally by its
#: `compatible` (`_is_plug_node`) and skipped by identity, so reserving
#: the name buys nothing. What keeps groups an author nests under a plug
#: from leaking into the template-level walk is the per-plug walk over
#: `nodes_by_slot` below, not this set.
_RESERVED = {"pads", "config"}
_MODEL_PROPS = {
    "reg",
    "compatible",
    "shield,addr-from",
    "shield,cs-position",
    "shield,collect",
    "shield,params",
    "shield,param-includes",
}

#: path -> (slot name, connector type) for every plug this shield declares
#: -- one entry per plug node, at any count -- the map
#: `_parse_pos_ref` resolves a phandle against to decide which slot a
#: reference names and to validate its position, so a reference may name
#: "one of the shield's plugs" rather than assuming there is only one.
PlugsByPath = dict[str, tuple[str, ConnectorType | None]]


def parse_shields(
    dt,
    types: dict[str, ConnectorType],
) -> tuple[dict[str, Shield], list[Diagnostic]]:
    """Every `.shield` file has exactly one shield node under the
    `shield-templates` wrapper (a marker that distinguishes a TEMPLATE
    from a real Zephyr shield's applied `<name>.overlay`)."""
    shields: dict[str, Shield] = {}
    diags: list[Diagnostic] = []
    root = dt.root.nodes.get("shield-templates")
    if root is None:
        return shields, diags
    for node in root.nodes.values():
        shield, d = _parse_shield(node, types)
        diags += d
        shields[shield.name] = shield
    return shields, diags


def _is_plug_node(g) -> bool:
    return "compatible" in g.props and g.props["compatible"].to_string() == "shield,plug"


def _is_exposed_node(g) -> bool:
    return "compatible" in g.props and g.props["compatible"].to_string().startswith("socket,")


def _require_label(node, kind: str, shield_name: str) -> tuple[str, list[Diagnostic]]:
    """The DTS label a rig->shield reference (`config:`/`wires:`/
    `socket:`) resolves against, for a device, pad, strap, jumper or
    exposed socket. A node with none is refused rather than silently
    addressed by its own node name: falling back to the node name would
    reopen exactly the two-spellings ambiguity (label vs. name) a label
    exists to remove.

    Returns (label, diagnostics): label is `node.labels[0]` when
    present; otherwise it is the node's own name, a placeholder that
    lets the caller still build a well-formed model object -- the
    accompanying error means the run fails regardless of what value
    ends up here -- and diagnostics carries the one error naming the
    node and what it needs."""
    if node.labels:
        return node.labels[0], []
    return node.name, [
        error(
            "lang-shield-label",
            f"{kind} '{node.name}' of shield '{shield_name}' has no DTS "
            "label -- rig-facing references (config:/wires:/socket:) "
            "resolve by label, never by node name -- give it one",
            (src_of(node),),
        )
    ]


def _parse_shield(
    node,
    types: dict[str, ConnectorType],
) -> tuple[Shield, list[Diagnostic]]:
    diags: list[Diagnostic] = []
    label = node.labels[0] if node.labels else node.name
    plugs_prop = node.props.get("shield,plugs")
    plug_children = [c for c in node.nodes.values() if _is_plug_node(c)]

    if plugs_prop is not None:
        diags.append(
            error(
                "lang-shield-plug",
                f"shield '{node.name}' declares shield,plugs on the TEMPLATE "
                "node -- that spelling is retired: move it onto the plug node "
                "itself, beside a 'compatible = \"shield,plug\"', so one plug "
                "and many are declared the same way",
                (src_of(plugs_prop),),
            )
        )
        return Shield(name=node.name, label=label, plugs={}, src=src_of(node)), diags

    shield = Shield(name=node.name, label=label, plugs={}, src=src_of(node))
    shield.by_path[node.path] = shield

    if not plug_children:
        diags.append(
            error(
                "lang-shield-plug",
                f"shield '{shield.name}' declares no 'shield,plug'-compatible "
                "child -- the plug is the position reference frame, and a "
                "shield names its connector type on it",
                (src_of(node),),
            )
        )
        return shield, diags

    ctypes_by_slot, nodes_by_slot, plugs_by_path, d = _parse_plugs(plug_children, shield, types)
    diags += d

    #: the slot a plug-agnostic (plain-group) device belongs to: the only
    #: one when there IS only one, else none. Replaces the retired single
    #: form's hardcoded `"plug"`, which was right only for a shield whose
    #: plug node happened to carry that name.
    only_slot = next(iter(shield.plugs)) if len(shield.plugs) == 1 else None

    # two-phase: pads/config first -- devices reference straps
    # (shield,addr-from) regardless of group order in the file. Both stay
    # TEMPLATE-LEVEL regardless of plurality (shield-level facts) -- a
    # routing jumper is the one exception: its position domain has no
    # plug axis, so a plural shield declaring one is refused rather than
    # silently mishandled; straps are address-domain and bus-scoped,
    # unaffected either way.
    diags += _parse_pads_and_config(node, shield)

    # device groups FIRST -- an exposed socket may reference a device as
    # its scope root (a mux channel), so the device must be in by_path
    # already.
    # template-level groups: plug-agnostic (plain groups) only -- a group
    # whose name is bus-shaped is rejected, since bus groups nest under
    # their owning plug (the placement rule), never sit at template level.
    # This holds at ONE plug exactly as at many.
    diags += _parse_template_groups(
        node, shield, plug_children, ctypes_by_slot, plugs_by_path, only_slot
    )

    # each plug's OWN bus groups, matched against ITS OWN connector
    # type's bus_proxies -- the plug binding, structural. A group nested
    # under a plug that is NEITHER a bus this plug's ctype allows NOR
    # bus-kind-named at all is a plain group in the wrong place: the
    # placement rule keeps plain groups at template level (plug-agnostic),
    # so nesting one under a plug is rejected here rather than silently
    # recorded with Device.plug = slot -- the same symmetry the
    # template-level walk above applies to a misplaced BUS group (its own
    # lang-shield-proxy branch).
    diags += _parse_plug_groups(shield, nodes_by_slot, ctypes_by_slot, plugs_by_path)

    # then re-exported sockets, pass-through or scope creation -- a
    # plural shield may declare one too: each gpio-map row and each
    # socket,<bus> resolves through ONE of the carrier's plugs, per
    # plugs_by_path, exactly as a device's own cross-plug refs do.
    diags += _parse_exposed_sockets(node, shield, plug_children, plugs_by_path, types)
    return shield, diags


def _parse_plugs(
    plug_children,
    shield: Shield,
    types: dict[str, ConnectorType],
) -> tuple[dict[str, ConnectorType | None], dict[str, Any], PlugsByPath, list[Diagnostic]]:
    """Every plug child in authoring order: validates its cell counts and
    resolves its connector type, and records `shield.plugs[slot]` (in that
    same order -- shield.plugs' own ordering contract) alongside the three
    lookup maps the rest of `_parse_shield` walks against."""
    diags: list[Diagnostic] = []
    ctypes_by_slot: dict[str, ConnectorType | None] = {}
    nodes_by_slot: dict[str, Any] = {}
    plugs_by_path: PlugsByPath = {}
    for child in plug_children:
        slot = child.name
        for cells in _FUNCTION_CELLS.values():
            if cells in child.props:
                diags.append(
                    error(
                        "lang-shield-plug-cells",
                        f"shield '{shield.name}': plug '{slot}' declares "
                        f"{cells} -- a plug node declares no cell counts. A "
                        "position reference through a plug carries the generic "
                        "count for its function (2 gpio, 3 pwm, 1 adc); only a "
                        "node that genuinely differs, such as a routing "
                        "jumper, says so",
                        (src_of(child.props[cells]),),
                    )
                )
        type_v = child.props.get("shield,plugs")
        if type_v is None:
            diags.append(
                error(
                    "lang-shield-type",
                    f"shield '{shield.name}': plug '{slot}' declares no "
                    "shield,plugs of its own -- every plug names its own "
                    "connector type",
                    (src_of(child),),
                )
            )
            continue
        type_name = type_v.to_string()
        ctype = types.get(type_name)
        if ctype is None:
            diags.append(
                error(
                    "lang-shield-type",
                    f"shield '{shield.name}': plug '{slot}' plugs unknown "
                    f"connector type '{type_name}'\nknown types: "
                    f"{', '.join(sorted(types))}",
                    (src_of(type_v),),
                )
            )
        shield.plugs[slot] = type_name
        ctypes_by_slot[slot] = ctype
        nodes_by_slot[slot] = child
        plugs_by_path[child.path] = (slot, ctype)
    return ctypes_by_slot, nodes_by_slot, plugs_by_path, diags


def _parse_pads_and_config(node, shield: Shield) -> list[Diagnostic]:
    """The `pads` and `config` template-level groups, in that authoring
    order. A `config` child with `shield,position-domain` is a routing
    jumper (refused above one plug); every other `config` child is a
    strap."""
    diags: list[Diagnostic] = []
    for group in node.nodes.values():
        if group.name == "pads":
            for pnode in group.nodes.values():
                pad, d = _parse_pad(pnode, shield.name)
                diags += d
                shield.pads[pad.name] = pad
                shield.by_path[pnode.path] = pad
        elif group.name == "config":
            for snode in group.nodes.values():
                if "shield,position-domain" in snode.props:
                    if len(shield.plugs) > 1:
                        diags.append(
                            error(
                                "lang-shield-plurality",
                                f"shield '{shield.name}': a shield with more "
                                f"than one plug cannot declare a routing "
                                f"jumper ('{snode.name}') -- the position "
                                "domain has no plug axis",
                                (src_of(snode),),
                            )
                        )
                        continue
                    jmp, d = _parse_jumper(snode, shield.name)
                    diags += d
                    shield.jumpers[jmp.name] = jmp
                    shield.by_path[snode.path] = jmp
                else:
                    strap, d = _parse_strap(snode, shield.name)
                    diags += d
                    shield.straps[strap.name] = strap
                    shield.by_path[snode.path] = strap
    return diags


def _parse_template_groups(
    node,
    shield: Shield,
    plug_children,
    ctypes_by_slot: dict[str, ConnectorType | None],
    plugs_by_path: PlugsByPath,
    only_slot: str | None,
) -> list[Diagnostic]:
    """Plug-agnostic device groups at template level. A bus-shaped group
    here is rejected -- bus groups nest under their owning plug -- but its
    devices are still parsed, so a misplaced group's own diagnostics don't
    mask its devices' problems."""
    diags: list[Diagnostic] = []
    for group in node.nodes.values():
        if group.name in _RESERVED or _is_exposed_node(group) or group in plug_children:
            continue
        if bus_kind_of(group.name) is not None:
            candidates = sorted(
                slot for slot, ct in ctypes_by_slot.items() if ct and group.name in ct.bus_proxies
            )
            diags.append(
                error(
                    "lang-shield-proxy",
                    f"shield '{shield.name}' has a '{group.name}' bus proxy "
                    "at template level -- bus groups nest under their owning "
                    "plug" + (f" — candidate plugs: {', '.join(candidates)}" if candidates else ""),
                    (src_of(group),),
                )
            )
        for dnode in group.nodes.values():
            dev, d = _parse_device(dnode, shield, plugs_by_path, None, group.name, only_slot)
            diags += d
            shield.devices.append(dev)
            shield.by_path[dnode.path] = dev
    return diags


def _parse_plug_groups(
    shield: Shield,
    nodes_by_slot: dict[str, Any],
    ctypes_by_slot: dict[str, ConnectorType | None],
    plugs_by_path: PlugsByPath,
) -> list[Diagnostic]:
    """Each plug's own nested groups, matched against its own connector
    type's bus_proxies. A group that is neither an allowed bus proxy nor
    bus-kind-named at all is a plain group in the wrong place; either way
    its devices are still parsed and attributed to this plug."""
    diags: list[Diagnostic] = []
    for slot, plug_node in nodes_by_slot.items():
        ctype = ctypes_by_slot[slot]
        for group in plug_node.nodes.values():
            bus = group.name if ctype and group.name in ctype.bus_proxies else None
            if bus is None:
                if ctype and bus_kind_of(group.name) is not None:
                    diags.append(
                        error(
                            "lang-shield-proxy",
                            f"shield '{shield.name}': plug '{slot}' has a "
                            f"'{group.name}' bus proxy but the '{ctype.name}' "
                            f"plug binding allows only: "
                            f"{', '.join(ctype.bus_proxies)}",
                            (src_of(group),),
                        )
                    )
                else:
                    diags.append(
                        error(
                            "lang-shield-proxy",
                            f"shield '{shield.name}': plug '{slot}' has a "
                            f"'{group.name}' group nested under it -- plain "
                            "device groups belong at template level "
                            "(plug-agnostic; their devices' refs each carry "
                            "their own plug by phandle)",
                            (src_of(group),),
                        )
                    )
            for dnode in group.nodes.values():
                dev, d = _parse_device(
                    dnode,
                    shield,
                    plugs_by_path,
                    bus,
                    None if bus else group.name,
                    slot if bus else None,
                )
                diags += d
                shield.devices.append(dev)
                shield.by_path[dnode.path] = dev
    return diags


def _parse_exposed_sockets(
    node, shield: Shield, plug_children, plugs_by_path: PlugsByPath, types: dict[str, ConnectorType]
) -> list[Diagnostic]:
    """Every re-exported socket at template level, in authoring order."""
    diags: list[Diagnostic] = []
    for group in node.nodes.values():
        if group.name in _RESERVED or not _is_exposed_node(group) or group in plug_children:
            continue
        exp, d = _parse_exposed(group, plugs_by_path, shield, types)
        diags += d
        shield.exposes[exp.name] = exp
        shield.by_path[group.path] = exp
    return diags


def _parse_device_addressing(
    node,
    shield: Shield,
    bus,
    unit: str,
) -> tuple[int | None, str | None, list[Diagnostic]]:
    """reg / shield,addr-from / unit-address, together: the address
    authority rule requires exactly one of reg / addr-from on an
    addressable bus, and the unit-address (when present) must agree with
    whichever of the two actually authors the address.

    Returns (reg, addr_from, diagnostics): addr_from is the strap's own
    name when shield,addr-from resolves, else None."""
    diags: list[Diagnostic] = []
    reg = node.props["reg"].to_num() if "reg" in node.props else None
    addr_from = None
    if "shield,addr-from" in node.props:
        target = node.props["shield,addr-from"].to_node()
        strap = shield.by_path.get(target.path)
        if not isinstance(strap, Strap):
            diags.append(
                error(
                    "lang-addr-from",
                    f"shield,addr-from on '{shield.name}/{node.name}' does not "
                    "point at a config strap of this shield",
                    (src_of(node.props["shield,addr-from"]),),
                )
            )
        else:
            addr_from = strap.name

    # exactly-one-of rule: forgot-reg is detectable, deferred is explicit
    if is_bus_kind(bus, "i2c") and (reg is None) == (addr_from is None):
        which = "both" if reg is not None else "neither"
        diags.append(
            error(
                "lang-addr-authority",
                f"device '{shield.name}/{node.name}' on an addressable bus "
                f"carries {which} of reg / shield,addr-from — exactly one "
                "is required (address authority rule)",
                (src_of(node),),
            )
        )

    # authored reg == unit-address (validated); symbolic
    # unit-address is a documentation marker linted against the addr-from
    # target
    if unit and reg is not None:
        try:
            if int(unit, 16) != reg:
                diags.append(
                    error(
                        "lang-unit-addr",
                        f"'{node.name}': unit-address @{unit} != authored reg "
                        f"<{reg:#x}> — they must be a matching pair",
                        (src_of(node),),
                    )
                )
        except ValueError:
            diags.append(
                error(
                    "lang-unit-addr",
                    f"'{node.name}': symbolic unit-address with authored reg "
                    "— symbolic markers are for deferred addresses only",
                    (src_of(node),),
                )
            )
    elif unit and addr_from and unit.replace("-", "_") != addr_from.replace("-", "_"):
        diags.append(
            warning(
                "lang-unit-addr",
                f"'{node.name}': symbolic unit-address @{unit} does not match "
                f"its resolver '{addr_from}' (lint: marker must name the "
                "addr-from target)",
                (src_of(node),),
            )
        )
    return reg, addr_from, diags


def _parse_device(
    node, shield: Shield, plugs_by_path: PlugsByPath, bus, group, dev_plug: str | None
) -> tuple[Device, list[Diagnostic]]:
    diags: list[Diagnostic] = []
    name, _, unit = node.name.partition("@")
    compat = node.props["compatible"].to_string() if "compatible" in node.props else None

    reg, addr_from, d = _parse_device_addressing(node, shield, bus, unit)
    diags += d

    cs_position = None
    if "shield,cs-position" in node.props:
        cs_position = node.props["shield,cs-position"].to_num()

    collect = None
    if "shield,collect" in node.props:
        collect = node.props["shield,collect"].to_string()

    declared_params: list[str] = []
    if "shield,params" in node.props:
        declared_params = list(node.props["shield,params"].to_strings())

    # The vocabulary declared_params' own tokens resolve against: a
    # device-node property, sibling to shield,params, since the header
    # is a contract of the parameter, not an accident of what the
    # template happened to #include.
    declared_param_includes: list[str] = []
    if "shield,param-includes" in node.props:
        declared_param_includes = list(node.props["shield,param-includes"].to_strings())

    label, d = _require_label(node, "device", shield.name)
    diags += d
    dev = Device(
        name=name,
        label=label,
        compatible=compat,
        bus=bus,
        group=group,
        reg=reg,
        addr_from=addr_from,
        cs_position=cs_position,
        plug=dev_plug,
        collect=collect,
        declared_params=declared_params,
        declared_param_includes=declared_param_includes,
        src=src_of(node),
    )

    for prop in node.props.values():
        if prop.name in _MODEL_PROPS or prop.name == "phandle":
            continue
        fn = _function_of(prop.name)
        if fn is not None:
            refs, d = _parse_pos_ref(prop, fn, shield, plugs_by_path)
            dev.function_refs.extend(refs)
            diags += d
            continue
        dtlib = get_dtlib()
        if prop.type is dtlib.Type.PHANDLES_AND_NUMS:
            diags.append(
                warning(
                    "lang-prop",
                    f"phandle property '{prop.name}' of "
                    f"'{shield.name}/{node.name}' is not a recognized function "
                    "ref (gpios/pwms/io-channels) — dropped",
                    (src_of(prop),),
                )
            )
            continue
        rendered = render_prop(prop)
        if rendered is None:
            diags.append(
                warning(
                    "lang-prop",
                    f"property '{prop.name}' of '{shield.name}/{node.name}' "
                    "has a type the prototype cannot pass through — dropped "
                    "from output",
                    (src_of(prop),),
                )
            )
        elif prop.name != "compatible":
            dev.extra_props.append((prop.name, rendered))
    if compat:
        dev.extra_props.insert(0, ("compatible", f'compatible = "{compat}";'))
    return dev, diags


_FUNCTION_CELLS = {"gpio": "#gpio-cells", "pwm": "#pwm-cells", "adc": "#io-channel-cells"}
_FUNCTION_DEFAULT_CELLS = {"gpio": 2, "pwm": 3, "adc": 1}


def _function_of(prop_name: str) -> str | None:
    """Which function-nexus a property resolves through, by name."""
    if prop_name == "gpios" or prop_name.endswith("-gpios"):
        return "gpio"
    if prop_name == "pwms":
        return "pwm"
    if prop_name == "io-channels":
        return "adc"
    return None


def _parse_pos_ref(
    prop,
    function: str,
    shield: Shield,
    plugs_by_path: PlugsByPath,
) -> tuple[list[FunctionRef], list[Diagnostic]]:
    """Nexus-aware position reference, per function. A plug is a
    multi-function nexus: a claim reads the plug's #<fn>-cells cells.
    Granularity is PER-REFERENCE: the phandle names WHICH of the
    shield's plugs this claim resolves through, independent of which
    plug the surrounding device's own bus binds to -- a cross-plug
    reference is zero new syntax, just a wider set of valid targets."""
    refs: list[FunctionRef] = []
    diags: list[Diagnostic] = []
    cells = words(prop)
    dt = prop.node.dt
    i = 0
    while i < len(cells):
        target = dt.phandle2node.get(cells[i])
        ncells = _ncells(target, function)
        args = cells[i + 1 : i + 1 + ncells]
        i += 1 + ncells
        if target is None or len(args) < ncells:
            diags.append(
                error(
                    "lang-pos-ref",
                    f"'{prop.name}' has a malformed {function} entry",
                    (src_of(prop),),
                )
            )
            return refs, diags

        elem = shield.by_path.get(target.path)
        plug_entry = plugs_by_path.get(target.path)
        if plug_entry is not None:  # fixed position
            slot, ctype = plug_entry
            pos = args[0]
            ok, d = _valid_position(prop, pos, ctype)
            diags += d
            if not ok:
                continue
            if function == "gpio":
                refs.append(
                    FunctionRef(
                        prop=prop.name,
                        position=pos,
                        flags=args[1],
                        function="gpio",
                        src=src_of(prop),
                        plug=slot,
                    )
                )
            elif function == "pwm":
                refs.append(
                    FunctionRef(
                        prop=prop.name,
                        position=pos,
                        period=args[1],
                        flags=args[2],
                        function="pwm",
                        src=src_of(prop),
                        plug=slot,
                    )
                )
            else:  # adc
                refs.append(
                    FunctionRef(
                        prop=prop.name,
                        position=pos,
                        flags=0,
                        function="adc",
                        src=src_of(prop),
                        plug=slot,
                    )
                )
        elif function == "gpio" and isinstance(elem, Jumper):  # deferred position
            flags = args[0] if args else 0
            refs.append(
                FunctionRef(
                    prop=prop.name,
                    position=None,
                    flags=flags,
                    jumper=elem.name,
                    function="gpio",
                    src=src_of(prop),
                )
            )
        else:
            where = target.path if target else "?"
            if len(plugs_by_path) > 1:
                what = "one of this shield's plug nodes"
            else:
                what = "THIS shield's plug node"
            diags.append(
                error(
                    "lang-pos-ref",
                    f"'{prop.name}' must reference {what} (fixed position)"
                    + ("" if function != "gpio" else " or one of its routing jumpers")
                    + f" — it points at {where}",
                    (src_of(prop),),
                )
            )
    return refs, diags


def _ncells(node, function: str) -> int:
    prop = _FUNCTION_CELLS[function]
    if node is not None and prop in node.props:
        return node.props[prop].to_num()
    return _FUNCTION_DEFAULT_CELLS[function]


def _valid_position(prop, pos: int, ctype) -> tuple[bool, list[Diagnostic]]:
    if ctype and pos not in ctype.index2name:
        return False, [
            error(
                "lang-position",
                f"'{prop.name}' claims position index {pos}, which does not "
                f"exist on connector type '{ctype.name}'",
                (src_of(prop),),
            )
        ]
    if ctype and ctype.index2name[pos] not in ctype.positions:
        return False, [
            error(
                "lang-position",
                f"'{prop.name}' claims {ctype.index2name[pos]} — bus copper, "
                f"not a claimable position of '{ctype.name}' (electrical "
                "realization is not modeled)",
                (src_of(prop),),
            )
        ]
    return True, []


def _parse_gpio_map(
    node,
    plugs_by_path: PlugsByPath,
    is_plural: bool,
) -> tuple[dict[int, tuple[str, int, int]], list[Diagnostic]]:
    """gpio-map's own 5-cell rows: child pos, child flags, phandle, parent
    pos, parent flags. Each phandle must land on one of the carrier's own
    plugs (pass-through); RECORDS which slot it named, per row."""
    diags: list[Diagnostic] = []
    gpio_map: dict[int, tuple[str, int, int]] = {}
    if "gpio-map" in node.props:
        cells = words(node.props["gpio-map"])
        dt = node.dt
        for i in range(0, len(cells) - len(cells) % 5, 5):
            pos, _f, phandle, parent_pos, parent_flags = cells[i : i + 5]
            target = dt.phandle2node.get(phandle)
            plug_entry = plugs_by_path.get(target.path) if target is not None else None
            if plug_entry is None:
                what = "one of the carrier's plugs" if is_plural else "the carrier's plug"
                diags.append(
                    error(
                        "lang-exposed",
                        f"exposed socket '{node.name}': gpio-map parent must "
                        f"be {what} (pass-through)",
                        (src_of(node),),
                    )
                )
                continue
            slot, _pctype = plug_entry
            gpio_map[pos] = (slot, parent_pos, parent_flags)
    return gpio_map, diags


def _parse_exposed_buses(
    node,
    shield: Shield,
    plugs_by_path: PlugsByPath,
    ctype: ConnectorType | None,
    type_name: str,
    is_plural: bool,
) -> tuple[dict[str, tuple[str, str]], list[Diagnostic]]:
    """The socket,<bus> (and role-qualified) properties, in sorted
    property-name order: each is either a pass-through of one of the
    carrier's plugs or a new scope rooted at a device of the shield."""
    diags: list[Diagnostic] = []
    buses: dict[str, tuple[str, str]] = {}
    qualified_props = sorted(name for name in node.props if _BUS_PROP_RE.match(name))
    for prop_name in qualified_props:
        kind = prop_name[len("socket,") :]
        if ctype is not None and kind not in ctype.bus_proxies:
            diags.append(
                error(
                    "lang-exposed",
                    f"exposed socket '{node.name}': {prop_name} names a bus "
                    f"'{kind}' that connector type '{type_name}' does not "
                    "declare -- declared buses: "
                    f"{', '.join(sorted(ctype.bus_proxies)) or 'none'}",
                    (src_of(node),),
                )
            )
            continue
        target = node.props[prop_name].to_node()
        by_path = shield.by_path.get(target.path)
        plug_entry = plugs_by_path.get(target.path)
        if plug_entry is not None:
            slot, _pctype = plug_entry
            buses[kind] = ("plug", slot)  # pass-through
        elif isinstance(by_path, Device):
            buses[kind] = ("scope", by_path.label)  # new scope
        else:
            what = "one of the carrier's plugs" if is_plural else "<&plug>"
            diags.append(
                error(
                    "lang-exposed",
                    f"exposed socket '{node.name}': {prop_name} must be "
                    f"{what} (pass-through) or <&device> (new scope)",
                    (src_of(node),),
                )
            )
    return buses, diags


def _parse_exposed(
    node,
    plugs_by_path: PlugsByPath,
    shield: Shield,
    types: dict[str, ConnectorType],
) -> tuple[ExposedSocket, list[Diagnostic]]:
    """A re-exported socket, potentially composed from SEVERAL named
    parents. gpio-map binds exposed positions to ONE of the carrier's own
    plug positions (pass-through) -- RECORDING which slot the phandle
    named, per row, exactly as `_parse_pos_ref` widens "must be THIS
    shield's plug" to "one of this shield's plugs". socket,<bus> (bare,
    or role-qualified per the multi-bus vocabulary) is either <&some-plug>
    (pass through THAT plug's own bus) or <&device> (a NEW scope rooted
    in that device of the shield). The CHILD-side qualified name is the
    EXPOSED connector type's OWN vocabulary -- validated exact-match
    against its declared bus_proxies, no fallback, independent of
    whichever parent-side bus a pass-through eventually selects (that
    selection is compose_socket's own job, by KIND, once the parent is a
    real resolved socket)."""
    diags: list[Diagnostic] = []
    type_name = node.props["compatible"].to_string().split(",", 1)[1]
    ctype = types.get(type_name)
    is_plural = len(plugs_by_path) > 1

    gpio_map, d = _parse_gpio_map(node, plugs_by_path, is_plural)
    diags += d

    pwm_map, pwm_cells, d = _parse_channel_map(
        node, "pwm-map", "#pwm-cells", "pwm", plugs_by_path, is_plural
    )
    diags += d
    adc_map, adc_cells, d = _parse_channel_map(
        node, "io-channel-map", "#io-channel-cells", "adc", plugs_by_path, is_plural
    )
    diags += d

    buses, d = _parse_exposed_buses(node, shield, plugs_by_path, ctype, type_name, is_plural)
    diags += d

    cs_pool: dict[str, list[int]] = {}
    if "socket,cs-pool" in node.props:
        cs_pool["spi"] = list(node.props["socket,cs-pool"].to_nums())
    for prop_name in sorted(node.props):
        m = _CS_POOL_PROP_RE.match(prop_name)
        if m is None:
            continue
        cs_pool[m.group(1)] = list(node.props[prop_name].to_nums())

    channel = node.props["shield,channel"].to_num() if "shield,channel" in node.props else None
    label, d = _require_label(node, "exposed socket", shield.name)
    diags += d
    return ExposedSocket(
        name=node.name,
        label=label,
        type_name=type_name,
        gpio_map=gpio_map,
        buses=buses,
        pwm_map=pwm_map,
        pwm_cells=pwm_cells,
        adc_map=adc_map,
        adc_cells=adc_cells,
        cs_pool=cs_pool,
        channel=channel,
        src=src_of(node),
    ), diags


def _parse_channel_map(
    node,
    prop_name: str,
    cells_prop: str,
    function: str,
    plugs_by_path: PlugsByPath,
    is_plural: bool,
) -> tuple[dict[int, tuple[str, int, int]], int | None, list[Diagnostic]]:
    """The pwm-map / io-channel-map twin of gpio-map's own loop above,
    factored out because PWM and ADC share this one function's shape end
    to end and because their STRIDE, unlike gpio-map's, is not a
    tree-wide constant: with `#pwm-cells = <2>` a row is 5 words (2 child
    + phandle + 2 parent); with `#io-channel-cells = <1>` it is 3 --
    derived below from the declared cell counts, never hardcoded.

    require-and-check: `prop_name` without `cells_prop` alongside
    it, or the reverse pairing, is a parse-time lang-exposed error -- the
    carrier author's declared count is what compose_socket later checks
    against the resolved parent's, so a map with no declared count (or a
    count with no map to describe) is malformed before that check could
    ever run. `function` selects `#<fn>-cells`'s fallback-to-generic-
    Zephyr-form default (_FUNCTION_DEFAULT_CELLS) for whatever the
    PHANDLE TARGET (the carrier's own plug, a template placeholder) itself
    declares -- the row's PARENT-specifier length -- exactly the same
    lookup `_parse_pos_ref` already applies to a device's own pwm/adc ref.

    Returns (map, declared_cells, diagnostics): map is `{}`/declared_cells
    is None when the node authors neither property (declared by absence,
    matching gpio_map's own convention) or when parsing fails outright."""
    diags: list[Diagnostic] = []
    has_map = prop_name in node.props
    has_cells = cells_prop in node.props
    if has_map and not has_cells:
        diags.append(
            error(
                "lang-exposed",
                f"exposed socket '{node.name}': {prop_name} needs a "
                f"{cells_prop} declaration alongside it (require-and-check: "
                "the carrier states its own cell count, "
                "the analyzer checks it against the resolved parent's)",
                (src_of(node),),
            )
        )
        return {}, None, diags
    if has_cells and not has_map:
        diags.append(
            error(
                "lang-exposed",
                f"exposed socket '{node.name}': {cells_prop} needs a "
                f"{prop_name} declaration alongside it (require-and-check)",
                (src_of(node),),
            )
        )
        return {}, None, diags
    if not has_map:
        return {}, None, diags

    declared_cells = node.props[cells_prop].to_num()
    cells = words(node.props[prop_name])
    dt = node.dt
    result: dict[int, tuple[str, int, int]] = {}
    i = 0
    while i < len(cells):
        if i + declared_cells + 1 > len(cells):
            diags.append(
                error(
                    "lang-exposed",
                    f"exposed socket '{node.name}': {prop_name} has a "
                    f"malformed entry (expected {declared_cells}-cell child "
                    f"specifiers, per {cells_prop})",
                    (src_of(node),),
                )
            )
            break
        pos = cells[i]
        phandle = cells[i + declared_cells]
        target = dt.phandle2node.get(phandle)
        parent_cells = _ncells(target, function)
        row_len = declared_cells + 1 + parent_cells
        if i + row_len > len(cells):
            diags.append(
                error(
                    "lang-exposed",
                    f"exposed socket '{node.name}': {prop_name} has a truncated entry",
                    (src_of(node),),
                )
            )
            break
        plug_entry = plugs_by_path.get(target.path) if target is not None else None
        if plug_entry is None:
            what = "one of the carrier's plugs" if is_plural else "the carrier's plug"
            diags.append(
                error(
                    "lang-exposed",
                    f"exposed socket '{node.name}': {prop_name} parent must "
                    f"be {what} (pass-through)",
                    (src_of(node),),
                )
            )
            i += row_len
            continue
        slot, _pctype = plug_entry
        parent_pos = cells[i + declared_cells + 1]
        result[pos] = (slot, parent_pos, 0)
        i += row_len
    return result, declared_cells, diags


def _parse_pad(node, shield_name: str) -> tuple[Pad, list[Diagnostic]]:
    diags: list[Diagnostic] = []
    role = node.props["shield,role"].to_string() if "shield,role" in node.props else "bidir"
    if role not in ("driver", "listener", "bidir"):
        diags.append(
            error(
                "lang-pad-role",
                f"pad '{node.name}': unknown role '{role}' (driver / listener / bidir)",
                (src_of(node),),
            )
        )
    of = None
    if "shield,of" in node.props:
        of = node.props["shield,of"].to_node().name.partition("@")[0]
    label, d = _require_label(node, "pad", shield_name)
    diags += d
    return Pad(name=node.name, label=label, role=role, of=of, src=src_of(node)), diags


def _parse_strap(node, shield_name: str) -> tuple[Strap, list[Diagnostic]]:
    dom = node.props["shield,domain"].to_nums()
    domain = [(dom[i], dom[i + 1]) for i in range(0, len(dom), 2)]
    label, diags = _require_label(node, "strap", shield_name)
    return Strap(
        name=node.name, label=label, domain=domain, sheet_label=_sheet_label(node), src=src_of(node)
    ), diags


def _parse_jumper(node, shield_name: str) -> tuple[Jumper, list[Diagnostic]]:
    dom = node.props["shield,position-domain"].to_nums()
    domain = [(dom[i], dom[i + 1]) for i in range(0, len(dom), 2)]
    label, diags = _require_label(node, "jumper", shield_name)
    return Jumper(
        name=node.name, label=label, domain=domain, sheet_label=_sheet_label(node), src=src_of(node)
    ), diags


def _sheet_label(node) -> str:
    if "shield,sheet-label" in node.props:
        return node.props["shield,sheet-label"].to_string()
    return ""
