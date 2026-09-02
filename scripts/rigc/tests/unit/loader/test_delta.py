# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: loader.delta -- base topology parsing and the delta engine.

The stable contracts: delta operations over a synthetic effective
topology (match/add/remove for instances and wires, `removed_by`
propagation), and diagnostic ORDERING on a multi-error synthetic input --
composed upward in document/traversal order, never accumulated into a
side channel.

`parse_instance`/`apply_delta` resolve `shield:` against a REAL
(synthetic, hermetic) `ShieldLibrary` built in-process from a
hand-constructed `Shield` value -- never a filesystem scan, never cpp.
Params/pin application and wire node-existence/ambiguity checks get
their own unit coverage in test_params.py; this module's tests exercise
the SHIELD RESOLUTION seam itself (a resolve() that succeeds, fails
"unknown shield", or is never reached because a required key is
missing) plus everything that needs no shield data at all
(removal/collision/ordering mechanics).
"""

from __future__ import annotations

from textwrap import dedent

from rigc.diag import SourceRef
from rigc.loader.binding import SocketBinding
from rigc.loader.delta import (
    Topology,
    apply_delta,
    find_wire,
    parse_instance,
    parse_wire,
    resolve_dotted,
)
from rigc.loader.documents import Val, parse_marked
from rigc.loader.library import ShieldLibrary
from rigc.model import Device, Instance, Pad, Shield, Strap, Wire, WireEnd

_BINDING = SocketBinding()


def _shield(name: str = "sh", pads=(), devices=()) -> Shield:
    shield = Shield(
        name=name, label=name, plugs={"plug": "synthetic-type"}, src=SourceRef("synthetic", 1)
    )
    for pad_name in pads:
        shield.pads[pad_name] = Pad(name=pad_name, label=pad_name, role="bidir", of=None)
    for dev in devices:
        shield.devices.append(dev)
    return shield


def _library(*shields: Shield) -> ShieldLibrary:
    """A hermetic, in-memory library: every shield already PARSED (no
    scan, no cpp) -- the synthetic value the cpp/unit-test seam calls
    for."""
    return ShieldLibrary(
        shields={s.name: s for s in shields},
        axes={s.name: None for s in shields},
        pending={},
        ymls={},
        types={},
        workdir="/nonexistent",
    )


def _inst(name: str, shield: Shield, socket: str = "s") -> Instance:
    src = SourceRef("synthetic", 1, name)
    return Instance(name=name, shield=shield, sockets={"plug": socket}, src=src)


def _plural_shield(name: str = "sh2", plugs=None) -> Shield:
    return Shield(
        name=name,
        label=name,
        plugs=dict(plugs or {"left": "t", "right": "t"}),
        src=SourceRef("synthetic", 1),
    )


def _doc(tmp_path, text: str, name: str = "d.yml") -> Val:
    path = tmp_path / name
    path.write_text(dedent(text))
    return parse_marked(str(path))


# ---------------------------------------------------------------- parse_instance


def test_parse_instance_resolves_the_shield_against_the_library(tmp_path) -> None:
    lib = _library(_shield("sh"))
    item = _doc(
        tmp_path,
        """\
        name: a
        shield: sh
        socket: nucleo_ard
        """,
    )
    inst, diags, _deps = parse_instance(item, _BINDING, lib, "rig", str(tmp_path))
    assert diags == []
    assert inst is not None
    assert inst.name == "a"
    assert inst.shield.name == "sh"
    assert inst.sockets["plug"] == "nucleo_ard"


def test_parse_instance_unknown_shield_is_rejected(tmp_path) -> None:
    lib = _library()
    item = _doc(
        tmp_path,
        """\
        name: a
        shield: ghost
        socket: s
        """,
    )
    inst, diags, _deps = parse_instance(item, _BINDING, lib, "rig", str(tmp_path))
    assert inst is None
    assert len(diags) == 1
    assert diags[0].code == "lang-instance-shield"


def test_parse_instance_applies_the_socket_binding(tmp_path) -> None:
    lib = _library(_shield("sh"))
    item = _doc(
        tmp_path,
        """\
        name: a
        shield: sh
        socket: ard
        """,
    )
    inst, _diags, _deps = parse_instance(
        item, SocketBinding({"ard": "nucleo_ard"}), lib, "rig", str(tmp_path)
    )
    assert inst is not None
    assert inst.sockets["plug"] == "nucleo_ard"


def test_parse_instance_socket_is_optional(tmp_path) -> None:
    """The loader never sees the board and so must not be the one
    requiring a socket to be named -- omitting socket: parses cleanly,
    carrying `None` through for the analyzer to infer later."""
    lib = _library(_shield("sh"))
    item = _doc(
        tmp_path,
        """\
        name: a
        shield: sh
        """,
    )  # no socket:
    inst, diags, _deps = parse_instance(item, _BINDING, lib, "rig", str(tmp_path))
    assert diags == []
    assert inst is not None
    assert inst.sockets["plug"] is None


def test_parse_instance_missing_required_key_returns_diagnostic(tmp_path) -> None:
    item = _doc(
        tmp_path,
        """\
        name: a
        socket: s
        """,
    )  # no shield:
    inst, diags, _deps = parse_instance(item, _BINDING, _library(), "rig", str(tmp_path))
    assert inst is None
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"


# ---------------------------------------------------------- sockets:/socket:


def test_parse_instance_plural_shield_builds_the_sockets_map(tmp_path) -> None:
    lib = _library(_plural_shield("sh2"))
    item = _doc(
        tmp_path,
        """\
        name: a
        shield: sh2
        sockets:
          left: quail_sock2
          right: quail_sock3
        """,
    )
    inst, diags, _deps = parse_instance(item, _BINDING, lib, "rig", str(tmp_path))
    assert diags == []
    assert inst is not None
    assert inst.sockets == {"left": "quail_sock2", "right": "quail_sock3"}


def test_parse_instance_plural_shield_omitted_slot_carries_none(tmp_path) -> None:
    lib = _library(_plural_shield("sh2"))
    item = _doc(
        tmp_path,
        """\
        name: a
        shield: sh2
        sockets:
          left: quail_sock2
        """,
    )  # "right" omitted -> None, left to per-slot inference
    inst, diags, _deps = parse_instance(item, _BINDING, lib, "rig", str(tmp_path))
    assert diags == []
    assert inst is not None
    assert inst.sockets == {"left": "quail_sock2", "right": None}


def test_parse_instance_socket_on_a_plural_shield_is_rejected(tmp_path) -> None:
    lib = _library(_plural_shield("sh2"))
    item = _doc(
        tmp_path,
        """\
        name: a
        shield: sh2
        socket: quail_sock2
        """,
    )
    inst, diags, _deps = parse_instance(item, _BINDING, lib, "rig", str(tmp_path))
    assert inst is not None
    assert len(diags) == 1
    assert diags[0].code == "lang-instance-socket"
    assert "plugs 2 sockets" in diags[0].message


def test_parse_instance_sockets_on_a_single_plug_shield_is_rejected(tmp_path) -> None:
    lib = _library(_shield("sh"))
    item = _doc(
        tmp_path,
        """\
        name: a
        shield: sh
        sockets:
          plug: quail_sock1
        """,
    )
    inst, diags, _deps = parse_instance(item, _BINDING, lib, "rig", str(tmp_path))
    assert inst is not None
    assert len(diags) == 1
    assert diags[0].code == "lang-instance-socket"
    assert "single plug" in diags[0].message


def test_parse_instance_both_socket_and_sockets_keys_is_rejected(tmp_path) -> None:
    lib = _library(_plural_shield("sh2"))
    item = _doc(
        tmp_path,
        """\
        name: a
        shield: sh2
        socket: quail_sock2
        sockets:
          left: quail_sock2
        """,
    )
    inst, diags, _deps = parse_instance(item, _BINDING, lib, "rig", str(tmp_path))
    assert inst is not None
    assert len(diags) == 1
    assert diags[0].code == "lang-instance-socket"
    assert "mutually exclusive" in diags[0].message


def test_parse_instance_sockets_unknown_slot_is_rejected(tmp_path) -> None:
    lib = _library(_plural_shield("sh2"))
    item = _doc(
        tmp_path,
        """\
        name: a
        shield: sh2
        sockets:
          bogus: quail_sock2
        """,
    )
    inst, diags, _deps = parse_instance(item, _BINDING, lib, "rig", str(tmp_path))
    assert inst is not None
    assert len(diags) == 1
    assert diags[0].code == "lang-instance-socket"
    assert "unknown slot 'bogus'" in diags[0].message
    assert "left" in diags[0].message and "right" in diags[0].message


def test_parse_instance_single_plug_shield_named_other_than_plug_keys_by_its_own_name(
    tmp_path,
) -> None:
    """model.py's own contract (FunctionRef.plug/Shield.plugs docstrings): a
    single-plug shield's one slot is the plug node's OWN name, never the
    literal "plug". A shield whose plug node is named 'north' must get
    its authored socket: keyed 'north' -- keying it 'plug' instead would
    match no slot of `shield.plugs` and silently fall back to per-slot
    inference."""
    shield = Shield(
        name="sh4", label="sh4", plugs={"north": "synthetic-type"}, src=SourceRef("synthetic", 1)
    )
    lib = _library(shield)
    item = _doc(
        tmp_path,
        """\
        name: a
        shield: sh4
        socket: quail_sock
        """,
    )
    inst, diags, _deps = parse_instance(item, _BINDING, lib, "rig", str(tmp_path))
    assert diags == []
    assert inst is not None
    assert inst.sockets == {"north": "quail_sock"}


def test_apply_delta_sockets_patch_replaces_wholesale_never_merges(tmp_path) -> None:
    """The params: rule: sockets: on a patch REPLACES the whole map, never
    a per-key merge -- an omitted slot on the RESTATED map still carries
    None, even though the base instance had it resolved."""
    delta = _doc(
        tmp_path,
        """\
        instances: [{name: a, sockets: {left: quail_sock9}}]
        """,
    )
    lib = _library(_plural_shield("sh2"))
    base = Instance(
        name="a",
        shield=_plural_shield("sh2"),
        sockets={"left": "quail_sock2", "right": "quail_sock3"},
        src=SourceRef("synthetic", 1, "a"),
    )
    topology = Topology(effective={"a": base}, order=["a"])
    new_topology, diags, _deps = apply_delta(
        delta, "variant", "b", topology, _BINDING, lib, None, "rig", str(tmp_path)
    )
    assert diags == []
    assert new_topology.effective["a"].sockets == {"left": "quail_sock9", "right": None}
    # the ORIGINAL is untouched
    assert topology.effective["a"].sockets == {"left": "quail_sock2", "right": "quail_sock3"}


# --------------------------------------------------------------- resolve_dotted


def test_resolve_dotted_valid_reference_resolves_the_node(tmp_path) -> None:
    doc = _doc(tmp_path, "x: a.sq\n")
    by_name = {"a": _inst("a", _shield("sh", pads=["sq"]))}
    end, diags = resolve_dotted(doc.value["x"], by_name, "from")
    assert diags == []
    assert end == WireEnd(instance_name="a", node="sq", src=doc.value["x"].src)


def test_resolve_dotted_rejects_non_dotted_form(tmp_path) -> None:
    doc = _doc(tmp_path, "x: nodot\n")
    end, diags = resolve_dotted(doc.value["x"], {}, "from")
    assert end is None
    assert diags[0].code == "lang-wire-ref"


def test_resolve_dotted_rejects_unknown_instance(tmp_path) -> None:
    doc = _doc(tmp_path, "x: ghost.sq\n")
    by_name = {"a": _inst("a", _shield("sh", pads=["sq"]))}
    end, diags = resolve_dotted(doc.value["x"], by_name, "from")
    assert end is None
    assert diags[0].code == "lang-wire-ref"


def test_resolve_dotted_rejects_unknown_node_in_the_shield(tmp_path) -> None:
    """Node existence is validated via Shield.by_name (no frozen golden
    covers this wording)."""
    doc = _doc(
        tmp_path,
        """\
        x: a.no-such-node
        """,
    )
    by_name = {"a": _inst("a", _shield("sh", pads=["sq"]))}
    end, diags = resolve_dotted(doc.value["x"], by_name, "from")
    assert end is None
    assert diags[0].code == "lang-wire-ref"
    assert "has no node 'no-such-node'" in diags[0].message


def test_resolve_dotted_rejects_ambiguous_node(tmp_path) -> None:
    """A LABEL matching more than one of pads/devices/straps is ambiguous
    (Shield.by_name's own contract: the scope resolves by label) --
    exercised here via a pad and a device sharing a LABEL while their
    node names differ, the simplest synthetic collision that survives
    the move off node-name matching."""
    shield = _shield("sh")
    shield.pads["dup"] = Pad(name="dup", label="dup", role="bidir", of=None)
    shield.by_path["p1"] = shield.pads["dup"]
    # Shield.by_name scans self.pads.values() by LABEL match, so a
    # single dict cannot itself hold two same-labeled pads -- simulate
    # the ambiguity the way the model actually allows it: a device
    # sharing the pad's LABEL under a different node name.
    shield.devices.append(
        Device(
            name="dup_dev",
            label="dup",
            compatible=None,
            bus=None,
            group="gpio",
            reg=None,
            addr_from=None,
            cs_position=None,
        )
    )
    doc = _doc(tmp_path, "x: a.dup\n")
    by_name = {"a": _inst("a", shield)}
    end, diags = resolve_dotted(doc.value["x"], by_name, "from")
    assert end is None
    assert diags[0].code == "lang-wire-ref"
    assert "is ambiguous" in diags[0].message


def test_resolve_dotted_missing_key() -> None:
    end, diags = resolve_dotted(None, {}, "from")
    assert end is None
    assert diags[0].code == "lang-schema"


# ------------------------------------------------------------------- parse_wire


def test_parse_wire_bare_string_route(tmp_path) -> None:
    item = _doc(
        tmp_path,
        """\
        from: a.sq
        to: b.led
        route: adhoc
        """,
    )
    by_name = {
        "a": _inst("a", _shield("sh_a", pads=["sq"])),
        "b": _inst("b", _shield("sh_b", pads=["led"])),
    }
    wire, diags = parse_wire(item, by_name)
    assert diags == []
    assert wire is not None
    assert wire.route == "adhoc"


def test_parse_wire_via_mapping_route(tmp_path) -> None:
    item = _doc(
        tmp_path,
        """\
        from: a.sq
        to: b.led
        route: {via: D2}
        """,
    )
    by_name = {
        "a": _inst("a", _shield("sh_a", pads=["sq"])),
        "b": _inst("b", _shield("sh_b", pads=["led"])),
    }
    wire, diags = parse_wire(item, by_name)
    assert diags == []
    assert wire is not None
    assert wire.route == "D2"


def test_parse_wire_mapping_route_without_via_is_rejected(tmp_path) -> None:
    item = _doc(
        tmp_path,
        """\
        from: a.sq
        to: b.led
        route: {}
        """,
    )
    by_name = {
        "a": _inst("a", _shield("sh_a", pads=["sq"])),
        "b": _inst("b", _shield("sh_b", pads=["led"])),
    }
    wire, diags = parse_wire(item, by_name)
    assert wire is None
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"
    assert "via" in diags[0].message


def test_parse_wire_missing_route_key_is_rejected(tmp_path) -> None:
    item = _doc(
        tmp_path,
        """\
        from: a.sq
        to: b.led
        """,
    )
    by_name = {
        "a": _inst("a", _shield("sh_a", pads=["sq"])),
        "b": _inst("b", _shield("sh_b", pads=["led"])),
    }
    wire, diags = parse_wire(item, by_name)
    assert wire is None
    assert diags[0].code == "lang-schema"


# ------------------------------------------------------------------- find_wire


def test_find_wire_matches_raw_endpoint_pair_with_no_shield_data() -> None:
    end_a = WireEnd(instance_name="x", node="sq", src=SourceRef("s", 1))
    end_b = WireEnd(instance_name="y", node="led-1", src=SourceRef("s", 1))
    wire = Wire(frm=end_a, to=end_b, route="adhoc", src=SourceRef("s", 1))
    assert find_wire([wire], "x.sq", "y.led-1") is wire
    assert find_wire([wire], "x.sq", "y.led-2") is None


def test_find_wire_none_endpoint_never_matches() -> None:
    assert find_wire([], None, "y.led-1") is None


# ------------------------------------------------------------------- apply_delta


def _topology_with(*names: str, shield=None) -> Topology:
    sh = shield or _shield("sh")
    effective = {n: _inst(n, sh) for n in names}
    return Topology(effective=effective, order=list(names))


def _apply(
    delta,
    stage,
    stage_value,
    topology,
    lib=None,
    binding=_BINDING,
    variant=None,
    rig_name="rig",
    workdir="/nonexistent",
):
    return apply_delta(
        delta,
        stage,
        stage_value,
        topology,
        binding,
        lib or _library(_shield("sh")),
        variant,
        rig_name,
        workdir,
    )


def test_instances_patch_matching_by_name_replaces_socket(tmp_path) -> None:
    delta = _doc(
        tmp_path,
        """\
        instances: [{name: a, socket: new_ard}]
        """,
    )
    topology = _topology_with("a")
    new_topology, diags, _deps = _apply(delta, "variant", "b", topology)
    assert diags == []
    assert new_topology.effective["a"].sockets["plug"] == "new_ard"
    # the ORIGINAL topology's instance is untouched -- a new value, not a
    # mutation of the one handed in.
    assert topology.effective["a"].sockets["plug"] == "s"


def test_instances_patch_config_replaces_pins(tmp_path) -> None:
    """`_apply_instance_patch`'s config: branch -- the shallow-replace
    site, the second of delta.py's two `apply_config_block` reads and
    the one easiest to miss since it duplicates `parse_instance`'s own
    call rather than sharing a helper. Resolves by LABEL, same as the
    base parse."""
    delta = _doc(
        tmp_path,
        """\
        instances: [{name: a, config: {addr_strap: 73}}]
        """,
    )
    shield = _shield("sh")
    shield.straps["addr-strap"] = Strap(
        name="addr-strap", label="addr_strap", domain=[(0x48, 0), (0x49, 1)], sheet_label=""
    )
    topology = _topology_with("a", shield=shield)
    new_topology, diags, _deps = _apply(delta, "variant", "b", topology)
    assert diags == []
    assert new_topology.effective["a"].straps == {"addr-strap": 73}


def test_instances_patch_config_rejects_node_name(tmp_path) -> None:
    delta = _doc(
        tmp_path,
        """\
        instances: [{name: a, config: {addr-strap: 73}}]
        """,
    )
    shield = _shield("sh")
    shield.straps["addr-strap"] = Strap(
        name="addr-strap", label="addr_strap", domain=[(0x48, 0), (0x49, 1)], sheet_label=""
    )
    topology = _topology_with("a", shield=shield)
    _, diags, _deps = _apply(delta, "variant", "b", topology)
    assert len(diags) == 1
    assert diags[0].code == "lang-config"


def test_instances_patch_unknown_name_is_rejected(tmp_path) -> None:
    delta = _doc(
        tmp_path,
        """\
        instances: [{name: ghost, socket: x}]
        """,
    )
    topology = _topology_with("a")
    _, diags, _deps = _apply(delta, "variant", "b", topology)
    assert len(diags) == 1
    assert diags[0].code == "lang-variant"
    assert "does not have" in diags[0].message


def test_instances_patch_can_swap_the_shield(tmp_path) -> None:
    delta = _doc(
        tmp_path,
        """\
        instances: [{name: a, shield: sh2}]
        """,
    )
    topology = _topology_with("a")
    lib = _library(_shield("sh"), _shield("sh2"))
    new_topology, diags, _deps = _apply(delta, "variant", "b", topology, lib=lib)
    assert diags == []
    assert new_topology.effective["a"].shield.name == "sh2"


def test_instances_patch_unknown_shield_is_rejected(tmp_path) -> None:
    delta = _doc(
        tmp_path,
        """\
        instances: [{name: a, shield: ghost}]
        """,
    )
    topology = _topology_with("a")
    _, diags, _deps = _apply(delta, "variant", "b", topology)
    assert len(diags) == 1
    assert diags[0].code == "lang-instance-shield"


def test_add_instances_new_name_is_appended_to_order(tmp_path) -> None:
    delta = _doc(
        tmp_path,
        """\
        add-instances: [{name: c, shield: sh, socket: s}]
        """,
    )
    topology = _topology_with("a")
    new_topology, diags, _deps = _apply(delta, "variant", "b", topology)
    assert diags == []
    assert new_topology.order == ["a", "c"]
    assert "c" in new_topology.effective


def test_add_instances_existing_name_is_rejected(tmp_path) -> None:
    delta = _doc(
        tmp_path,
        """\
        add-instances: [{name: a, shield: sh, socket: s}]
        """,
    )
    topology = _topology_with("a")
    _, diags, _deps = _apply(delta, "variant", "b", topology)
    assert len(diags) == 1
    assert diags[0].code == "lang-variant"
    assert "already exists" in diags[0].message


def test_remove_instances_removes_and_records_removed_by(tmp_path) -> None:
    delta = _doc(
        tmp_path,
        """\
        remove-instances: [a]
        """,
    )
    topology = _topology_with("a")
    new_topology, diags, _deps = _apply(delta, "variant", "b", topology)
    assert diags == []
    assert "a" not in new_topology.effective
    assert new_topology.removed_by["a"] == "b"


def test_remove_instances_absent_name_is_rejected_and_names_prior_remover(tmp_path) -> None:
    delta = _doc(
        tmp_path,
        """\
        remove-instances: [a]
        """,
    )
    topology = Topology(removed_by={"a": "b"})  # already removed by variant b
    _, diags, _deps = _apply(delta, "revision", "2", topology)
    assert len(diags) == 1
    assert diags[0].code == "lang-rev"
    # The prior remover is NAMED (data presence, not wording -- the exact
    # phrasing belongs to the remove-instance-drift golden alone).
    assert "'b'" in diags[0].message


def test_remove_wires_matches_endpoint_pair(tmp_path) -> None:
    delta = _doc(
        tmp_path,
        """\
        remove-wires: [{from: x.sq, to: y.led-1}]
        """,
    )
    end_a = WireEnd(instance_name="x", node="sq", src=SourceRef("s", 1))
    end_b = WireEnd(instance_name="y", node="led-1", src=SourceRef("s", 1))
    wire = Wire(frm=end_a, to=end_b, route="adhoc", src=SourceRef("s", 1))
    topology = Topology(wires=[wire])
    new_topology, diags, _deps = _apply(delta, "variant", "b", topology)
    assert diags == []
    assert new_topology.wires == []


def test_remove_wires_missing_pair_is_rejected(tmp_path) -> None:
    delta = _doc(
        tmp_path,
        """\
        remove-wires: [{from: x.sq, to: y.led-2}]
        """,
    )
    topology = Topology()
    _, diags, _deps = _apply(delta, "variant", "b", topology)
    assert len(diags) == 1
    assert diags[0].code == "lang-variant"
    assert "does not exist" in diags[0].message


def test_add_wires_parses_like_base_wires(tmp_path) -> None:
    delta = _doc(
        tmp_path,
        """\
        add-wires: [{from: a.sq, to: b.led, route: adhoc}]
        """,
    )
    shield = _shield("sh", pads=["sq", "led"])
    topology = _topology_with("a", "b", shield=shield)
    new_topology, diags, _deps = _apply(delta, "variant", "b", topology)
    assert diags == []
    assert len(new_topology.wires) == 1


def test_multiple_delta_errors_compose_in_document_order(tmp_path) -> None:
    """Diagnostic ordering: several operations in ONE delta each raise,
    and the composed order must equal document/traversal order -- never
    a mutable side channel's own append order."""
    delta = _doc(
        tmp_path,
        """\
        instances: [{name: ghost1, socket: s}]
        remove-instances: [ghost2]
        """,
    )
    topology = _topology_with("a")
    _, diags, _deps = _apply(delta, "variant", "b", topology)
    assert len(diags) == 2
    assert "ghost1" in diags[0].message
    assert "ghost2" in diags[1].message


def test_apply_delta_never_mutates_the_topology_it_was_given(tmp_path) -> None:
    delta = _doc(
        tmp_path,
        """\
        add-instances: [{name: c, shield: sh, socket: s}]
        """,
    )
    topology = _topology_with("a")
    _apply(delta, "variant", "b", topology)
    assert topology.order == ["a"]
    assert "c" not in topology.effective


# ------------------------------------------------ apply_delta <-> params glue


def test_instance_patch_shield_swap_drops_the_old_params(tmp_path) -> None:
    """When shield: changes, the OLD params are keyed to the OLD
    shield's devices and are dropped rather than carried forward -- the
    glue `_apply_instance_patch` itself owns (params.py's own functions
    are pure and know nothing about a "previous" shield)."""
    dev = Device(
        name="d",
        label="dl",
        compatible=None,
        bus="i2c",
        group=None,
        reg=None,
        addr_from=None,
        cs_position=None,
    )
    old_shield = _shield("sh", devices=[dev])
    new_shield = _shield("sh2")
    topology = _topology_with("a", shield=old_shield)
    topology.effective["a"].params = {"dl": {"x": "1"}}
    delta = _doc(
        tmp_path,
        """\
        instances: [{name: a, shield: sh2}]
        """,
    )
    lib = _library(old_shield, new_shield)
    new_topology, diags, _deps = _apply(delta, "variant", "b", topology, lib=lib)
    assert diags == []
    assert new_topology.effective["a"].params == {}


def test_instance_patch_shield_swap_to_differently_shaped_shield_resets_stale_sockets(
    tmp_path,
) -> None:
    """Swapping to a shield whose slot-name set differs from the
    carried-forward sockets map (single<->plural, or between
    differently-shaped plurals) with no `sockets:`/`socket:` restatement
    must not leave stale keys behind -- every slot would otherwise
    silently fall back to per-slot inference with no diagnostic. Mirrors
    the params reset immediately above."""
    old_shield = _plural_shield("sh2", plugs={"left": "t", "right": "t"})
    new_shield = _shield("sh3")  # single-plug: one slot, named "plug"
    topology = _topology_with("a", shield=old_shield)
    topology.effective["a"].sockets = {"left": "quail_sock2", "right": "quail_sock3"}
    delta = _doc(
        tmp_path,
        """\
        instances: [{name: a, shield: sh3}]
        """,
    )
    lib = _library(old_shield, new_shield)
    new_topology, diags, _deps = _apply(delta, "variant", "b", topology, lib=lib)
    assert diags == []
    assert new_topology.effective["a"].sockets == {"plug": None}


def test_instance_patch_shield_swap_to_same_shaped_shield_carries_sockets_forward(tmp_path) -> None:
    """The existing behavior must not change: swapping between two
    shields whose slot-name SETS match (same shape) carries the sockets
    map forward untouched, exactly like pins/jumpers do on a shield swap
    with no matching restatement key."""
    old_shield = _plural_shield("sh2", plugs={"left": "t", "right": "t"})
    new_shield = _plural_shield("sh3", plugs={"left": "t2", "right": "t2"})
    topology = _topology_with("a", shield=old_shield)
    topology.effective["a"].sockets = {"left": "quail_sock2", "right": "quail_sock3"}
    delta = _doc(
        tmp_path,
        """\
        instances: [{name: a, shield: sh3}]
        """,
    )
    lib = _library(old_shield, new_shield)
    new_topology, diags, _deps = _apply(delta, "variant", "b", topology, lib=lib)
    assert diags == []
    assert new_topology.effective["a"].sockets == {"left": "quail_sock2", "right": "quail_sock3"}


def test_instance_patch_params_without_shield_change_runs_the_restate_check(tmp_path) -> None:
    """params: for an instance whose shield: is UNCHANGED must restate
    every already-assigned property -- omitting one is rejected, not
    silently kept. The glue that decides WHEN to call check_restate
    lives in `_apply_instance_patch`."""
    dev = Device(
        name="d",
        label="dl",
        compatible=None,
        bus="i2c",
        group=None,
        reg=None,
        addr_from=None,
        cs_position=None,
        declared_params=["vnd,threshold"],
    )
    shield = _shield("sh", devices=[dev])
    topology = _topology_with("a", shield=shield)
    topology.effective["a"].params = {"dl": {"vnd,threshold": "10"}}
    delta = _doc(
        tmp_path,
        """\
        instances: [{name: a, params: {dl: {}}}]
        """,
    )
    lib = _library(shield)
    _, diags, _deps = _apply(delta, "variant", "b", topology, lib=lib)
    assert len(diags) == 1
    assert diags[0].code == "lang-param"
    assert "without restating" in diags[0].message
