# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""The composer: `analyze()` assembles every pass's piece into one Solved
value, in a fixed pass order -- sockets -> gpio nets -> addresses -> CS ->
wires -> net conflicts -> labels. This module's OWN subject is the
ASSEMBLY, not any one pass's algorithm (those are covered where they are
named: test_sockets.py, test_gpio.py, test_addresses.py, test_cs.py,
test_wires.py, test_labels.py) -- so it exercises the composer end to end
over one tiny rig, pinning that Solved's fields actually come from the
pass results (never a mutable accumulator any pass writes into from
outside), that skip-don't-abort survives composition, and that
diagnostics stay ordered pass-by-pass."""

from __future__ import annotations

from rigc.analyzer import analyze
from rigc.model import Board, BoardSocket, ConnectorType, Device, Instance, Rig, Shield


def _ctype() -> ConnectorType:
    return ConnectorType(
        name="t", positions={}, index2name={}, bus_proxies=[], stackable=True, cs_pool={}
    )


def _dev(name: str, reg=None) -> Device:
    return Device(
        name=name,
        label=name,
        compatible=None,
        bus="i2c",
        group=None,
        reg=reg,
        addr_from=None,
        cs_position=None,
    )


def _inst(name: str, socket: str, *devices: Device) -> Instance:
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=list(devices))
    return Instance(name=name, shield=shield, sockets={"plug": socket})


def test_analyze_assembles_every_pass_into_one_solved_value() -> None:
    from rigc.model import BusRef

    board = Board(
        name="b",
        sockets={
            "ard": BoardSocket(
                label="ard",
                path="/ard",
                type_name="t",
                gpio_map={},
                buses={"i2c": BusRef("i2c1", "/i2c1")},
            )
        },
    )
    inst = _inst("i1", "ard", _dev("sensor", reg=0x50))
    rig = Rig(name="r", instances=[inst])

    solved, diags = analyze(rig, board, {"t": _ctype()})

    assert diags == []
    assert solved.sockets["i1"]["plug"].label == "ard"
    assert solved.addr[("i1", "sensor")] == 0x50


def test_analyze_skip_dont_abort_across_the_whole_pipeline() -> None:
    """An instance whose mating fails is simply absent from every later
    field -- addresses, CS, nets -- never an exception, never a partial
    rig aborting analysis of the REST."""
    board = Board(name="b", sockets={})  # no sockets at all -> every mating fails
    inst = _inst("orphan", "no-such-socket", _dev("sensor", reg=0x50))
    rig = Rig(name="r", instances=[inst])

    solved, diags = analyze(rig, board, {"t": _ctype()})

    assert solved.sockets == {}
    assert solved.addr == {}
    assert len(diags) == 1
    assert diags[0].code == "phys-socket"


def test_analyze_diagnostics_are_ordered_pass_by_pass() -> None:
    """A phys-socket finding (the sockets pass, first) must precede a
    phys-label finding (the labels pass, last) regardless of which
    instance in rig.instances triggered which."""
    board = Board(name="b", sockets={})
    bad = _inst("bad", "nowhere", _dev("x"))
    dup_a = _inst("dup", "also-nowhere", _dev("y", reg=None))
    dup_a.shield.devices.append(_dev("y2"))
    dup_a.shield.devices[0].label = "same"
    dup_a.shield.devices[1].label = "same"
    rig = Rig(name="r", instances=[bad, dup_a])

    _solved, diags = analyze(rig, board, {"t": _ctype()})

    codes = [d.code for d in diags]
    assert "phys-socket" in codes
    assert "phys-label" in codes
    assert codes.index("phys-socket") < codes.index("phys-label")


def test_analyze_never_returns_none() -> None:
    """Once a Board is in hand, the composer always produces a Solved,
    even when passes append errors along the way -- board-load failure
    itself is handled upstream (cli.py), never inside this composer."""
    board = Board(name="b", sockets={})
    rig = Rig(name="r", instances=[])

    solved, diags = analyze(rig, board, {})

    assert solved is not None
    assert diags == []
