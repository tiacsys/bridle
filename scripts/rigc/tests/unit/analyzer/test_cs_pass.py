# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""The `allocate_cs` PASS wrapper (as distinct from the acid-test
algorithm in test_cs.py): wiring a scope's members' copper-fixed/pool
sources through to `allocate_cs_positions`, and folding placements into
`cs`/`cs_gpios`/new net claims. The algorithm itself is covered value-
shaped, without a scenario, in test_cs.py; this module's subject is the
WIRING -- so it necessarily needs a minimal constructed Rig/Instance/
BoardSocket scope, the same shape test_addresses.py already uses for its
own pass."""

from __future__ import annotations

from rigc.analyzer.cs import allocate_cs
from rigc.model import BoardSocket, BusRef, ConnectorType, Device, Instance, Rig, Shield


def _socket(cs_pool=None, gpio_map=None, path="/spi0") -> BoardSocket:
    return BoardSocket(
        label="sock",
        path=path,
        type_name="t",
        gpio_map=gpio_map or {},
        buses={"spi": BusRef(label="spi0", path=path, cs_pool=cs_pool)},
    )


def _ctype(cs_pool=None) -> ConnectorType:
    return ConnectorType(
        name="t",
        positions={},
        index2name={},
        bus_proxies=[],
        stackable=True,
        cs_pool={"spi": cs_pool or [16, 15, 14]},
    )


def _dev(name: str, cs_position=None) -> Device:
    return Device(
        name=name,
        label=name,
        compatible=None,
        bus="spi",
        group=None,
        reg=None,
        addr_from=None,
        cs_position=cs_position,
    )


def _inst(name: str, *devices: Device) -> Instance:
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=list(devices))
    return Instance(name=name, shield=shield, sockets={"plug": "sock"})


def test_copper_fixed_device_is_placed_at_its_authored_position() -> None:
    dev = _dev("sdhc", cs_position=16)
    inst = _inst("logger", dev)
    rig = Rig(name="r", instances=[inst])
    socket = _socket(gpio_map={16: ("gpiod", 0, 0)})

    result, diags = allocate_cs(rig, {"logger": {"plug": socket}}, {"t": _ctype()}, {})

    assert diags == []
    assert result.cs[("logger", "sdhc")] == (0, 16)
    assert result.cs_gpios["/spi0"] == [(socket, 16)]


def test_pool_allocated_device_picks_the_type_default_pool() -> None:
    dev = _dev("eth")
    inst = _inst("adapter", dev)
    rig = Rig(name="r", instances=[inst])
    socket = _socket(gpio_map={16: ("gpiod", 0, 0)})  # cs_pool=None -> ctype fallback

    result, diags = allocate_cs(rig, {"adapter": {"plug": socket}}, {"t": _ctype()}, {})

    assert diags == []
    assert result.cs[("adapter", "eth")] == (0, 16)


def test_socket_cs_pool_override_wins_over_the_type_default() -> None:
    dev = _dev("eth")
    inst = _inst("adapter", dev)
    rig = Rig(name="r", instances=[inst])
    socket = _socket(cs_pool=[9], gpio_map={9: ("gpiod", 3, 0)})

    result, _diags = allocate_cs(rig, {"adapter": {"plug": socket}}, {"t": _ctype()}, {})

    assert result.cs[("adapter", "eth")] == (0, 9)


def test_exhaustion_across_a_shared_scope_is_phys_cs() -> None:
    devs = [_dev(f"d{i}") for i in range(4)]  # 4 devices, pool of 3
    insts = [_inst(f"i{i}", devs[i]) for i in range(4)]
    rig = Rig(name="r", instances=insts)
    socket = _socket(gpio_map={p: (f"gpio{p}", p, 0) for p in (16, 15, 14)})
    sockets = {f"i{i}": {"plug": socket} for i in range(4)}

    result, diags = allocate_cs(rig, sockets, {"t": _ctype()}, {})

    assert len(diags) == 1
    assert diags[0].code == "phys-cs"
    assert "exhausted" in diags[0].message
    assert len(result.cs) == 3


def test_position_with_no_gpio_map_entry_is_phys_cs() -> None:
    """A CS position the board fragment doesn't route through the
    gpio-map cannot emit cs-gpios at all -- rejected rather than silently
    emitting an unroutable position."""
    dev = _dev("sdhc", cs_position=16)
    inst = _inst("logger", dev)
    rig = Rig(name="r", instances=[inst])
    socket = _socket(gpio_map={})  # no entry for position 16

    result, diags = allocate_cs(rig, {"logger": {"plug": socket}}, {"t": _ctype()}, {})

    assert len(diags) == 1
    assert diags[0].code == "phys-cs"
    assert result.cs_gpios["/spi0"] == []


def test_prior_nets_from_the_gpio_pass_count_as_already_taken() -> None:
    """`nets_before` (the gpio pass's own claims) narrows the pool exactly
    like a same-call placement does -- a position already claimed by a
    plain GPIO ref is unavailable to CS allocation too."""
    from rigc.analyzer.gpio import NetClaim, soc_net

    dev = _dev("eth")
    inst = _inst("adapter", dev)
    rig = Rig(name="r", instances=[inst])
    socket = _socket(gpio_map={16: ("gpiod", 0, 0), 15: ("gpiod", 1, 0)})
    taken_key = soc_net(socket, 16)
    nets_before = {
        taken_key: [
            NetClaim(
                instance=inst, device=None, what="x", role="listener", socket=socket, position=16
            )
        ]
    }

    result, diags = allocate_cs(rig, {"adapter": {"plug": socket}}, {"t": _ctype()}, nets_before)

    assert diags == []
    assert result.cs[("adapter", "eth")] == (0, 15)  # skipped the taken D10 (16)


def test_instances_without_a_resolved_socket_are_skipped() -> None:
    dev = _dev("eth")
    inst = _inst("orphan", dev)
    rig = Rig(name="r", instances=[inst])

    result, diags = allocate_cs(rig, {}, {}, {})

    assert result.cs == {}
    assert diags == []


def test_allocate_cs_never_mutates_the_gpio_passes_nets() -> None:
    """`nets_before` is ANOTHER pass's returned value: allocate_cs may
    read it (occupancy) but never write into it -- the symmetric twin of
    test_wires' own never-mutates contract. A copper-fixed CS landing on
    an already-claimed net must add its own claim to THIS pass's result
    only, never append into the caller's `nets_before` claim lists (a
    shared list there would double-count the claim after merge_nets and
    corrupt the composer's merged net view)."""
    from rigc.analyzer.gpio import NetClaim, merge_nets, soc_net

    dev = _dev("flash", cs_position=16)  # copper-fixed: placed regardless
    inst = _inst("logger", dev)
    rig = Rig(name="r", instances=[inst])
    socket = _socket(gpio_map={16: ("gpiod", 0, 0)})
    shared_key = soc_net(socket, 16)
    gpio_claim = NetClaim(
        instance=inst, device=None, what="led: gpios", role="listener", socket=socket, position=16
    )
    nets_before = {shared_key: [gpio_claim]}

    result, _diags = allocate_cs(rig, {"logger": {"plug": socket}}, {"t": _ctype()}, nets_before)

    # The caller's value is untouched...
    assert nets_before == {shared_key: [gpio_claim]}
    # ...the CS claim exists exactly once, in THIS pass's own result...
    assert len(result.nets[shared_key]) == 1
    # ...and the merged view holds exactly the two real claimants.
    assert [c.what for c in merge_nets(nets_before, result.nets)[shared_key]] == [
        "led: gpios",
        "flash: CS copper-fixed at position 16 (shield,cs-position)",
    ]
