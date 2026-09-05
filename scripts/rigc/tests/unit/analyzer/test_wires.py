# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Wires and route resolution. No frozen golden covers this family
(phys-wire) -- diagnostic wording here is not frozen, so these tests
assert structure (code, which endpoint, resolved route) rather than exact
message text, keeping wording out of unit tests."""

from __future__ import annotations

from rigc.diag import SourceRef
from rigc.model import ConnectorType, Instance, Pad, Position, Rig, Shield, Wire, WireEnd

_SRC = SourceRef("f.yml", 1, "w")


def _end(inst_name: str, node: str) -> WireEnd:
    return WireEnd(instance_name=inst_name, node=node, src=_SRC)


def _shield_with_pads(**pads: str) -> Shield:
    """pads maps pad NAME -> role."""
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"})
    for name, role in pads.items():
        shield.pads[name] = Pad(name=name, label=name, role=role, of=None)
    return shield


def _inst(name: str, shield: Shield) -> Instance:
    return Instance(name=name, shield=shield, sockets={"plug": "sock"})


def _ctype() -> ConnectorType:
    return ConnectorType(
        name="t",
        positions={"D7": Position(name="D7", index=7, function="gpio")},
        index2name={7: "D7"},
        bus_proxies=[],
        stackable=False,
        cs_pool={},
    )


def test_a_wire_between_one_driver_and_one_listener_is_legal() -> None:
    from rigc.analyzer.wires import check_wires

    a = _inst("a", _shield_with_pads(out="driver"))
    b = _inst("b", _shield_with_pads(in_="listener"))
    wire = Wire(frm=_end("a", "out"), to=_end("b", "in_"), route="adhoc", src=_SRC)
    rig = Rig(name="r", instances=[a, b], wires=[wire])

    resolved, diags = check_wires(rig, {}, {})

    assert diags == []
    assert resolved == [wire]


def test_wire_endpoint_that_is_not_a_pad_is_phys_wire() -> None:
    from rigc.analyzer.wires import check_wires

    a = _inst("a", Shield(name="sh", label="sh", plugs={"plug": "t"}))  # no pads at all
    b = _inst("b", _shield_with_pads(in_="listener"))
    wire = Wire(frm=_end("a", "not_a_pad"), to=_end("b", "in_"), route="adhoc", src=_SRC)
    rig = Rig(name="r", instances=[a, b], wires=[wire])

    _resolved, diags = check_wires(rig, {}, {})

    assert len(diags) == 1
    assert diags[0].code == "phys-wire"


def test_wire_with_zero_drivers_is_phys_wire() -> None:
    from rigc.analyzer.wires import check_wires

    a = _inst("a", _shield_with_pads(x="listener"))
    b = _inst("b", _shield_with_pads(y="listener"))
    wire = Wire(frm=_end("a", "x"), to=_end("b", "y"), route="adhoc", src=_SRC)
    rig = Rig(name="r", instances=[a, b], wires=[wire])

    _resolved, diags = check_wires(rig, {}, {})

    assert len(diags) == 1
    assert diags[0].code == "phys-wire"


def test_wire_with_two_drivers_is_phys_wire() -> None:
    from rigc.analyzer.wires import check_wires

    a = _inst("a", _shield_with_pads(x="driver"))
    b = _inst("b", _shield_with_pads(y="driver"))
    wire = Wire(frm=_end("a", "x"), to=_end("b", "y"), route="adhoc", src=_SRC)
    rig = Rig(name="r", instances=[a, b], wires=[wire])

    _resolved, diags = check_wires(rig, {}, {})

    assert len(diags) == 1
    assert diags[0].code == "phys-wire"


def test_route_via_a_position_name_resolves_to_its_index() -> None:
    from rigc.analyzer.sockets import SocketResolution
    from rigc.analyzer.wires import check_wires
    from rigc.model import BoardSocket

    # An anchor, not a dependency: SocketResolution is what the docstring
    # above names, and asserting on it means a rename breaks this test
    # rather than rotting the prose silently. Naming it in an assertion
    # rather than importing it unused also spares the file one suppression
    # comment per linter -- ruff's F401 and pylint's W0611 both.
    assert SocketResolution.__name__ == "SocketResolution"

    a = _inst("a", _shield_with_pads(x="driver"))
    b = _inst("b", _shield_with_pads(y="listener"))
    wire = Wire(frm=_end("a", "x"), to=_end("b", "y"), route="D7", src=_SRC)
    rig = Rig(name="r", instances=[a, b], wires=[wire])
    socket = BoardSocket(label="s", path="/s", type_name="t", gpio_map={}, buses={})

    resolved, diags = check_wires(rig, {"a": {"plug": socket}}, {"t": _ctype()})

    assert diags == []
    assert resolved[0].route == 7


def test_route_via_an_unknown_position_name_is_phys_wire() -> None:
    from rigc.analyzer.wires import check_wires
    from rigc.model import BoardSocket

    a = _inst("a", _shield_with_pads(x="driver"))
    b = _inst("b", _shield_with_pads(y="listener"))
    wire = Wire(frm=_end("a", "x"), to=_end("b", "y"), route="NOPE", src=_SRC)
    rig = Rig(name="r", instances=[a, b], wires=[wire])
    socket = BoardSocket(label="s", path="/s", type_name="t", gpio_map={}, buses={})

    _resolved, diags = check_wires(rig, {"a": {"plug": socket}}, {"t": _ctype()})

    assert len(diags) == 1
    assert diags[0].code == "phys-wire"


def test_via_route_from_a_multiplug_instance_is_refused() -> None:
    """A `via: <position>` route resolves through the FROM end's socket's
    connector type, which is ambiguous when the FROM instance plugs more
    than one socket -- a loud refusal naming the instance, rather than a
    guessed-at plug."""
    from rigc.analyzer.wires import check_wires

    plural_shield = Shield(name="sh2", label="sh2", plugs={"left": "t", "right": "t"})
    plural_shield.pads["x"] = Pad(name="x", label="x", role="driver", of=None)
    a = Instance(name="a", shield=plural_shield, sockets={"left": "sl", "right": "sr"})
    b = _inst("b", _shield_with_pads(y="listener"))
    wire = Wire(frm=_end("a", "x"), to=_end("b", "y"), route="D7", src=_SRC)
    rig = Rig(name="r", instances=[a, b], wires=[wire])

    resolved, diags = check_wires(rig, {}, {"t": _ctype()})

    assert len(diags) == 1
    assert diags[0].code == "phys-wire"
    assert "instance 'a' plugs more than one socket" in diags[0].message
    assert "via-routing is not supported for a multi-plug instance yet" in diags[0].message
    # the wire is passed through un-resolved (route stays the raw name),
    # not dropped -- the pass never shrinks rig.wires on a refusal.
    assert resolved[0].route == "D7"


def test_check_wires_never_mutates_the_original_wire() -> None:
    """Value-shaped, non-mutating: resolving `route: via <name>` never
    mutates wire.route in place; this module returns a NEW Wire list
    instead, leaving rig.wires' own objects untouched."""
    from rigc.analyzer.wires import check_wires
    from rigc.model import BoardSocket

    a = _inst("a", _shield_with_pads(x="driver"))
    b = _inst("b", _shield_with_pads(y="listener"))
    wire = Wire(frm=_end("a", "x"), to=_end("b", "y"), route="D7", src=_SRC)
    rig = Rig(name="r", instances=[a, b], wires=[wire])
    socket = BoardSocket(label="s", path="/s", type_name="t", gpio_map={}, buses={})

    resolved, _diags = check_wires(rig, {"a": {"plug": socket}}, {"t": _ctype()})

    assert wire.route == "D7"  # the ORIGINAL is untouched
    assert resolved[0] is not wire
    assert resolved[0].route == 7
