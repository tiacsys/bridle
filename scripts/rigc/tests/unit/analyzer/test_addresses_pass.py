# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""The `allocate_addresses` PASS wrapper (as distinct from the acid-test
algorithm in test_addresses.py): grouping a scope's members into
fixed/pinned/free, building each member's AddressMember, and translating
`allocate_scope_addresses`' placements/problems into diagnostics plus the
pass's own `AddressAllocation` fields. The algorithm itself is covered
value-shaped, without a scenario, in test_addresses.py; this module's
subject is the WIRING -- so it necessarily needs a minimal constructed
Rig/Instance/Shield/BoardSocket scope, the same shape test_cs_pass.py
already uses for its own pass."""

from __future__ import annotations

from rigc.analyzer.addresses import allocate_addresses
from rigc.model import BoardSocket, BusRef, Device, Instance, Rig, Shield, Strap


def _socket(path: str = "/i2c1") -> BoardSocket:
    return BoardSocket(
        label="sock",
        path=path,
        type_name="t",
        gpio_map={},
        buses={"i2c": BusRef(label="i2c1", path=path)},
    )


def _shield(straps=None) -> Shield:
    return Shield(name="sh", label="sh", plugs={"plug": "t"}, straps=straps or {})


def _dev(name: str, reg=None, addr_from=None) -> Device:
    return Device(
        name=name,
        label=name,
        compatible=None,
        bus="i2c",
        group=None,
        reg=reg,
        addr_from=addr_from,
        cs_position=None,
    )


def _inst(name: str, shield: Shield, straps=None) -> Instance:
    return Instance(name=name, shield=shield, sockets={"plug": "sock"}, straps=straps or {})


def test_fixed_address_is_claimed_verbatim() -> None:
    dev = _dev("sensor", reg=0x50)
    inst = _inst("i1", _shield())
    inst.shield.devices.append(dev)
    rig = Rig(name="r", instances=[inst])

    result, diags = allocate_addresses(rig, {"i1": {"plug": _socket()}})

    assert diags == []
    assert result.addr[("i1", "sensor")] == 0x50


def test_two_fixed_addresses_on_one_bus_collide() -> None:
    a = _dev("a", reg=0x5F)
    b = _dev("b", reg=0x5F)
    inst_a = _inst("i1", _shield())
    inst_a.shield.devices.append(a)
    inst_b = _inst("i2", _shield())
    inst_b.shield.devices.append(b)
    rig = Rig(name="r", instances=[inst_a, inst_b])

    _result, diags = allocate_addresses(rig, {"i1": {"plug": _socket()}, "i2": {"plug": _socket()}})

    assert len(diags) == 1
    assert diags[0].code == "phys-addr"


def test_pinned_address_resolves_through_the_strap_domain() -> None:
    strap = Strap(name="addr", label="addr", domain=[(0x10, 0), (0x11, 1)], sheet_label="")
    shield = _shield(straps={"addr": strap})
    dev = _dev("sensor", addr_from="addr")
    inst = _inst("i1", shield, straps={"addr": 0x11})
    inst.shield.devices.append(dev)
    rig = Rig(name="r", instances=[inst])

    result, diags = allocate_addresses(rig, {"i1": {"plug": _socket()}})

    assert diags == []
    assert result.addr[("i1", "sensor")] == 0x11
    assert result.straps == [(inst, strap, 1, 0x11)]


def test_pinned_address_outside_the_strap_domain_is_phys_pin() -> None:
    strap = Strap(name="addr", label="addr", domain=[(0x10, 0)], sheet_label="")
    shield = _shield(straps={"addr": strap})
    dev = _dev("sensor", addr_from="addr")
    inst = _inst("i1", shield, straps={"addr": 0x99})
    inst.shield.devices.append(dev)
    rig = Rig(name="r", instances=[inst])

    _result, diags = allocate_addresses(rig, {"i1": {"plug": _socket()}})

    assert len(diags) == 1
    assert diags[0].code == "phys-pin"


def test_free_allocation_picks_first_unclaimed_domain_address() -> None:
    strap = Strap(name="addr", label="addr", domain=[(0x10, 0), (0x11, 1)], sheet_label="")
    shield = _shield(straps={"addr": strap})
    dev = _dev("sensor", addr_from="addr")
    inst = _inst("i1", shield)  # no config: -- free allocation
    inst.shield.devices.append(dev)
    rig = Rig(name="r", instances=[inst])

    result, diags = allocate_addresses(rig, {"i1": {"plug": _socket()}})

    assert diags == []
    assert result.addr[("i1", "sensor")] == 0x10
    assert result.straps == [(inst, strap, 0, 0x10)]


def test_free_allocation_exhaustion_is_phys_addr() -> None:
    strap = Strap(name="addr", label="addr", domain=[(0x10, 0)], sheet_label="")
    taken = _dev("taken", reg=0x10)
    free = _dev("free", addr_from="addr")
    inst_a = _inst("i1", _shield(straps={"addr": strap}))
    inst_a.shield.devices.append(taken)
    inst_b = _inst("i2", _shield(straps={"addr": strap}))
    inst_b.shield.devices.append(free)
    rig = Rig(name="r", instances=[inst_a, inst_b])

    _result, diags = allocate_addresses(rig, {"i1": {"plug": _socket()}, "i2": {"plug": _socket()}})

    assert len(diags) == 1
    assert diags[0].code == "phys-addr"
    assert "exhausted" in diags[0].message


def test_allocation_is_scoped_per_bus_not_shared_globally() -> None:
    """Two DIFFERENT I2C buses (different socket paths) each get their
    OWN address space -- the same fixed address on two separate buses is
    not a conflict."""
    a = _dev("a", reg=0x50)
    b = _dev("b", reg=0x50)
    inst_a = _inst("i1", _shield())
    inst_a.shield.devices.append(a)
    inst_b = _inst("i2", _shield())
    inst_b.shield.devices.append(b)
    rig = Rig(name="r", instances=[inst_a, inst_b])

    result, diags = allocate_addresses(
        rig, {"i1": {"plug": _socket(path="/i2c1")}, "i2": {"plug": _socket(path="/i2c2")}}
    )

    assert diags == []
    assert result.addr[("i1", "a")] == 0x50
    assert result.addr[("i2", "b")] == 0x50


def test_a_mux_channel_is_a_new_scope() -> None:
    """A composed (mux-channel) socket's own path IS its scope identity --
    two fixed-same-address devices on the SAME channel still collide
    (proven above by test_two_fixed_addresses_on_one_bus_collide re-used
    at a channel path), but a device on a DIFFERENT channel path does
    not, which is what this test pins."""
    a = _dev("a", reg=0x48)
    b = _dev("b", reg=0x48)
    inst_a = _inst("sensor_a", _shield())
    inst_a.shield.devices.append(a)
    inst_b = _inst("sensor_b", _shield())
    inst_b.shield.devices.append(b)
    rig = Rig(name="r", instances=[inst_a, inst_b])

    result, diags = allocate_addresses(
        rig,
        {
            "sensor_a": {"plug": _socket(path="/mux_1/ch0")},
            "sensor_b": {"plug": _socket(path="/mux_1/ch1")},
        },
    )

    assert diags == []
    assert result.addr == {("sensor_a", "a"): 0x48, ("sensor_b", "b"): 0x48}


def test_instances_without_a_resolved_socket_are_skipped() -> None:
    dev = _dev("sensor", reg=0x50)
    inst = _inst("orphan", _shield())
    inst.shield.devices.append(dev)
    rig = Rig(name="r", instances=[inst])

    result, diags = allocate_addresses(rig, {})

    assert result.addr == {}
    assert diags == []
