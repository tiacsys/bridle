# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: analyzer.socketmap -- the one accessor family every downstream
pass and emitter module reaches a per-slot socket through. Each function
is a pure lookup over hand-built values; no Rig/Board/dtlib needed."""

from __future__ import annotations

from rigc.analyzer.socketmap import for_bus_device, for_ref, for_slot, slots_of
from rigc.model import BoardSocket, Device, FunctionRef, Instance, Shield


def _socket(label: str) -> BoardSocket:
    return BoardSocket(label=label, path=f"/{label}", type_name="t", gpio_map={}, buses={})


def _inst(sockets: dict, plugs: dict) -> Instance:
    shield = Shield(name="sh", label="sh", plugs=plugs)
    return Instance(name="i1", shield=shield, sockets=sockets)


# ---------------------------------------------------------------- for_slot / slots_of


def test_for_slot_returns_the_resolved_socket() -> None:
    sock = _socket("s1")
    resolved = {"i1": {"plug": sock}}
    inst = _inst({"plug": "s1"}, {"plug": "t"})
    assert for_slot(resolved, inst, "plug") is sock


def test_for_slot_returns_none_when_the_slot_never_resolved() -> None:
    inst = _inst({"plug": None}, {"plug": "t"})
    assert for_slot({}, inst, "plug") is None


def test_for_slot_returns_none_for_an_unresolved_instance_entirely() -> None:
    inst = _inst({"left": None, "right": None}, {"left": "t", "right": "t"})
    assert for_slot({}, inst, "left") is None


def test_slots_of_lists_only_resolved_slots_in_authoring_order() -> None:
    right = _socket("r")
    resolved = {"i1": {"right": right}}  # "left" never resolved
    inst = _inst({"left": "x", "right": "y"}, {"left": "t1", "right": "t2"})
    assert slots_of(resolved, inst) == ["right"]


def test_slots_of_empty_when_instance_absent_from_the_map() -> None:
    inst = _inst({"plug": None}, {"plug": "t"})
    assert slots_of({}, inst) == []


def test_slots_of_preserves_shield_plugs_authoring_order_not_dict_order_of_resolved() -> None:
    """The order comes from Shield.plugs (authoring order), never from
    whatever order happened to land in the resolution map."""
    a, b = _socket("a"), _socket("b")
    resolved = {"i1": {"second": b, "first": a}}  # resolved out of order
    inst = _inst({"first": "x", "second": "y"}, {"first": "t1", "second": "t2"})
    assert slots_of(resolved, inst) == ["first", "second"]


# ---------------------------------------------------------------- for_ref


def test_for_ref_resolves_through_the_refs_own_plug() -> None:
    left, right = _socket("l"), _socket("r")
    resolved = {"i1": {"left": left, "right": right}}
    inst = _inst({"left": "x", "right": "y"}, {"left": "t1", "right": "t2"})
    ref = FunctionRef(
        prop="int-gpios",
        position=0,
        flags=0,
        src=None,  # type: ignore[arg-type]
        plug="right",
    )

    assert for_ref(resolved, inst, ref) is right


def test_for_ref_a_cross_plug_reference_ignores_the_devices_own_bus_slot() -> None:
    """A ref's plug is independent of any device it happens to sit on --
    for_ref never consults Device at all, only ref.plug."""
    left, right = _socket("l"), _socket("r")
    resolved = {"i1": {"left": left, "right": right}}
    inst = _inst({"left": "x", "right": "y"}, {"left": "t1", "right": "t2"})
    # A device "sitting" on the left plug's bus, but its own ref names right.
    ref = FunctionRef(
        prop="int-gpios",
        position=0,
        flags=0,
        src=None,  # type: ignore[arg-type]
        plug="right",
    )

    assert for_ref(resolved, inst, ref) is right
    assert for_ref(resolved, inst, ref) is not left


def test_for_ref_returns_none_when_that_slot_never_resolved() -> None:
    inst = _inst({"plug": None}, {"plug": "t"})
    ref = FunctionRef(
        prop="int-gpios",
        position=0,
        flags=0,
        src=None,  # type: ignore[arg-type]
        plug="plug",
    )
    assert for_ref({}, inst, ref) is None


def test_for_ref_single_form_default_plug_resolves() -> None:
    sock = _socket("s1")
    resolved = {"i1": {"plug": sock}}
    inst = _inst({"plug": "s1"}, {"plug": "t"})
    ref = FunctionRef(prop="int-gpios", position=0, flags=0, src=None)  # type: ignore[arg-type]
    assert ref.plug == "plug"  # the dataclass default
    assert for_ref(resolved, inst, ref) is sock


# ---------------------------------------------------------------- for_bus_device


def test_for_bus_device_resolves_through_the_devices_own_plug() -> None:
    left, right = _socket("l"), _socket("r")
    resolved = {"i1": {"left": left, "right": right}}
    inst = _inst({"left": "x", "right": "y"}, {"left": "t1", "right": "t2"})
    dev = Device(
        name="d",
        label="d",
        compatible=None,
        bus="i2c",
        group=None,
        reg=None,
        addr_from=None,
        cs_position=None,
        plug="right",
    )

    assert for_bus_device(resolved, inst, dev) is right


def test_for_bus_device_returns_none_when_that_slot_never_resolved() -> None:
    inst = _inst({"plug": None}, {"plug": "t"})
    dev = Device(
        name="d",
        label="d",
        compatible=None,
        bus="i2c",
        group=None,
        reg=None,
        addr_from=None,
        cs_position=None,
        plug="plug",
    )
    assert for_bus_device({}, inst, dev) is None


def test_for_bus_device_asserts_on_a_plain_group_device() -> None:
    """Calling this on a plug-agnostic (plain-group) device is a caller
    bug -- every real caller filters to bus-kind devices first."""
    import pytest

    inst = _inst({"plug": "x"}, {"plug": "t"})
    dev = Device(
        name="d",
        label="d",
        compatible=None,
        bus=None,
        group="gpio",
        reg=None,
        addr_from=None,
        cs_position=None,
        plug=None,
    )
    with pytest.raises(AssertionError):
        for_bus_device({}, inst, dev)
