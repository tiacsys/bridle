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


def _socket(
    cs_pool=None,
    gpio_map=None,
    path="/spi0",
    existing_cs_gpios=(),
    existing_child_regs=frozenset(),
) -> BoardSocket:
    return BoardSocket(
        label="sock",
        path=path,
        type_name="t",
        gpio_map=gpio_map or {},
        buses={
            "spi": BusRef(
                label="spi0",
                path=path,
                cs_pool=cs_pool,
                existing_cs_gpios=existing_cs_gpios,
                existing_child_regs=existing_child_regs,
            )
        },
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


# ---------------------------------------------------------------- board-authored SPI wiring


def test_board_authored_cs_gpios_offsets_past_it_and_preserves_it_verbatim() -> None:
    """The mikroe_quail/spi3 shape: a board-authored `cs-gpios` array on
    the controller a rig wants to place a device on. Offset-and-preserve
    (as distinct from step 1's blunt refusal): the rig's own device is
    numbered starting AFTER the board's own array (index 3, not 0 -- the
    truncation bug this whole check exists to prevent), and the board's
    own entries are carried into `cs_gpios_existing` verbatim, ready for
    the emitter to render them first."""
    dev = _dev("eth")
    inst = _inst("adapter", dev)
    rig = Rig(name="r", instances=[inst])
    existing = (("gpiod", 11, 1), ("gpiod", 1, 1), ("gpioa", 13, 1))
    socket = _socket(gpio_map={16: ("gpiod", 0, 0)}, existing_cs_gpios=existing)

    result, diags = allocate_cs(rig, {"adapter": {"plug": socket}}, {"t": _ctype()}, {})

    assert diags == []
    assert result.cs[("adapter", "eth")] == (3, 16)  # offset past the 3 existing entries
    assert result.cs_gpios["/spi0"] == [(socket, 16)]
    assert result.cs_gpios_existing["/spi0"] == list(existing)


def test_existing_child_reg_inside_the_existing_array_is_not_a_collision() -> None:
    """A pre-existing child whose own `reg` falls WITHIN the board's own
    cs-gpios array (mikroe_quail.dts's flash1: reg <2>, array length 3 --
    every real board this corpus carries shapes it this way) is not
    disturbed by the offset: the rig's own device starts at index 3,
    never anywhere near index 2. A board authoring a child whose reg
    falls OUTSIDE its own array is the collision check's own concern,
    covered separately below."""
    dev = _dev("eth")
    inst = _inst("adapter", dev)
    rig = Rig(name="r", instances=[inst])
    socket = _socket(
        gpio_map={16: ("gpiod", 0, 0)},
        existing_cs_gpios=(("gpiod", 11, 1), ("gpiod", 1, 1), ("gpioa", 13, 1)),
        existing_child_regs=frozenset({2}),
    )

    result, diags = allocate_cs(rig, {"adapter": {"plug": socket}}, {"t": _ctype()}, {})

    assert diags == []
    assert result.cs[("adapter", "eth")] == (3, 16)


def test_existing_child_reg_past_the_array_collides_with_the_offset() -> None:
    """The sparse/unusual arrangement the offset alone cannot see: a
    board authoring a child whose own `reg` falls OUTSIDE (>=) its own
    cs-gpios array length -- legal DT (SPI_CS_GPIOS_DT_SPEC_GET_OR
    tolerates an out-of-range index, yielding an empty gpio_dt_spec for
    a no-CS/software-controlled device) but exactly the index
    offset-and-preserve would otherwise hand the rig's own next device.
    A 1-entry array with an existing child at reg <1> (one past the
    array) collides with the very first index the offset computes."""
    dev = _dev("eth")
    inst = _inst("adapter", dev)
    rig = Rig(name="r", instances=[inst])
    socket = _socket(
        gpio_map={16: ("gpiod", 0, 0)},
        existing_cs_gpios=(("gpiod", 11, 1),),
        existing_child_regs=frozenset({1}),
    )

    result, diags = allocate_cs(rig, {"adapter": {"plug": socket}}, {"t": _ctype()}, {})

    assert len(diags) == 1
    assert diags[0].code == "phys-cs"
    assert "spi0" in diags[0].message  # names the controller
    assert "reg <1>" in diags[0].message
    assert "adapter/eth" in diags[0].message
    assert result.cs_gpios["/spi0"] == []  # refused, never emitted through the nexus


def test_board_with_no_existing_spi_wiring_is_unaffected() -> None:
    """The common case -- a board that authors nothing of its own on the
    controller -- is not this check's concern at all: unchanged pass-
    through allocation, same as every other test in this module."""
    dev = _dev("eth")
    inst = _inst("adapter", dev)
    rig = Rig(name="r", instances=[inst])
    socket = _socket(gpio_map={16: ("gpiod", 0, 0)})  # existing_* both empty (the default)

    result, diags = allocate_cs(rig, {"adapter": {"plug": socket}}, {"t": _ctype()}, {})

    assert diags == []
    assert result.cs[("adapter", "eth")] == (0, 16)


# --------------------------------------------------------- reuse-not-append (Task A)


def test_placement_reuses_an_existing_entry_naming_the_same_soc_pin() -> None:
    """THE reuse rule this module's own task exists for: MikroE Quail's
    own repro (quail_temp_farm) -- a rig-placed device's own resolved
    pin (position 16 here, through gpio_map, exactly the way soc_net
    compares two claims) is the SAME pin the board's own existing
    cs-gpios array already names at index 1 ("gpiod", 11) -- so the
    device REUSES that index rather than appending a duplicate entry
    for a pin the array already carries. cs_gpios (the RIG-appended
    suffix) stays empty; cs_gpios_existing is untouched."""
    dev = _dev("eth")
    inst = _inst("adapter", dev)
    rig = Rig(name="r", instances=[inst])
    existing = (("gpiod", 1, 1), ("gpiod", 11, 1), ("gpioa", 13, 1))
    socket = _socket(gpio_map={16: ("gpiod", 11, 0)}, existing_cs_gpios=existing)

    result, diags = allocate_cs(rig, {"adapter": {"plug": socket}}, {"t": _ctype()}, {})

    assert diags == []
    assert result.cs[("adapter", "eth")] == (1, 16)  # reused index 1, not appended at 3
    assert result.cs_gpios["/spi0"] == []  # nothing appended
    assert result.cs_gpios_existing["/spi0"] == list(existing)


def test_placement_with_no_matching_existing_pin_still_appends_past_it() -> None:
    """The negative control: a placement whose own pin is genuinely
    ABSENT from the board's own array (WINC1500's own pool-allocated D9
    shape -- a pin the board never wired) still appends, numbered past
    the board's own array length, exactly as before reuse existed."""
    dev = _dev("eth")
    inst = _inst("adapter", dev)
    rig = Rig(name="r", instances=[inst])
    existing = (("gpiod", 1, 1), ("gpiod", 11, 1))
    socket = _socket(gpio_map={16: ("gpioc", 7, 0)}, existing_cs_gpios=existing)  # not in existing

    result, diags = allocate_cs(rig, {"adapter": {"plug": socket}}, {"t": _ctype()}, {})

    assert diags == []
    assert result.cs[("adapter", "eth")] == (2, 16)  # appended past the 2 existing entries
    assert result.cs_gpios["/spi0"] == [(socket, 16)]


def test_one_device_reuses_and_a_second_appends_in_the_same_scope() -> None:
    """Mixed scope, the shape THE BUG's own reproduction (mikroe_quail's
    spi1) and quail_can_span/quail_sockets's own goldens carry: one
    device's own pin already names an existing entry (reused, no
    append), a SECOND device's own pin is genuinely new (appended past
    the existing array) -- proving reuse is decided per-PLACEMENT, not
    once for the whole scope, and that an appended index still starts
    at the existing array's own length, never at the reused device's
    own index + 1."""
    existing = (("gpioa", 3, 1), ("gpioe", 0, 1))  # quail spi1's own 2-entry array
    reused_dev = _dev("logflash", cs_position=2)  # -> gpioe 0, ALREADY index 1
    new_dev = _dev("can0", cs_position=5)  # -> gpiob 5, genuinely new
    inst = _inst("adapter", reused_dev, new_dev)
    rig = Rig(name="r", instances=[inst])
    socket = _socket(
        gpio_map={2: ("gpioe", 0, 0), 5: ("gpiob", 5, 0)},
        existing_cs_gpios=existing,
    )

    result, diags = allocate_cs(rig, {"adapter": {"plug": socket}}, {"t": _ctype()}, {})

    assert diags == []
    assert result.cs[("adapter", "logflash")] == (1, 2)  # reused index 1
    assert result.cs[("adapter", "can0")] == (2, 5)  # appended past the 2 existing, not 3
    assert result.cs_gpios["/spi0"] == [(socket, 5)]  # only the genuinely-new one
    assert result.cs_gpios_existing["/spi0"] == list(existing)


def test_reused_flags_come_from_the_boards_own_verbatim_entry_not_a_rig_placed_one() -> None:
    """The flags sub-decision, pinned at the allocation level: a reused
    placement contributes NOTHING to `cs_gpios` (the rig-appended
    entries the emitter renders with a freshly-authored `1 /* ACTIVE_LOW
    */` flags word) -- the array position it lands on is rendered
    exclusively from `cs_gpios_existing`'s own verbatim (ctrl, pin,
    flags) tuple (emitter/overlay.py's `_spi_scopes`), so a board entry
    authored with a NON-trivial flags word (nucleo_f401re's own
    `<&gpiob 6 17>`, GPIO_ACTIVE_LOW | GPIO_PULL_UP) is never overwritten
    or shadowed by a second, differently-flagged entry for the same
    pin."""
    dev = _dev("sdhc")
    inst = _inst("logger", dev)
    rig = Rig(name="r", instances=[inst])
    existing = (("gpiob", 6, 17),)  # nucleo's own ACTIVE_LOW|PULL_UP entry
    socket = _socket(gpio_map={16: ("gpiob", 6, 0)}, existing_cs_gpios=existing)

    result, diags = allocate_cs(rig, {"logger": {"plug": socket}}, {"t": _ctype()}, {})

    assert diags == []
    assert result.cs[("logger", "sdhc")] == (0, 16)
    assert result.cs_gpios["/spi0"] == []  # no second entry for this pin
    assert result.cs_gpios_existing["/spi0"] == [("gpiob", 6, 17)]  # the ONLY entry, verbatim


def test_reused_index_still_collides_with_an_in_array_existing_child_reg() -> None:
    """Step 3's collision check, RE-DERIVED for reuse (not just the
    append path test_existing_child_reg_past_the_array_collides_with_
    the_offset already covers): mikroe_quail's own flash1 shape, but
    with the rig's OWN placement landing on the SAME in-array index a
    board child already holds -- e.g. a rig device whose own pin happens
    to be the board's own CS2 (index 2), which mikroe_quail.dts's flash1
    already claims as ITS reg. Reuse must not silently hand a second
    device node the SAME reg flash1 already has; refused exactly like
    the past-the-array case, just reached by the reuse path instead of
    the offset path."""
    dev = _dev("eth")
    inst = _inst("adapter", dev)
    rig = Rig(name="r", instances=[inst])
    socket = _socket(
        gpio_map={16: ("gpioa", 13, 0)},  # resolves to existing index 2
        existing_cs_gpios=(("gpiod", 11, 1), ("gpiod", 1, 1), ("gpioa", 13, 1)),
        existing_child_regs=frozenset({2}),  # flash1's own reg, SAME index reuse would pick
    )

    result, diags = allocate_cs(rig, {"adapter": {"plug": socket}}, {"t": _ctype()}, {})

    assert len(diags) == 1
    assert diags[0].code == "phys-cs"
    assert "reg <2>" in diags[0].message
    assert result.cs_gpios["/spi0"] == []  # refused, never emitted through the nexus


def test_two_placements_reusing_the_same_entry_is_an_exclusive_net_conflict() -> None:
    """The two-rig-devices-share-one-board-entry sub-decision: does the
    NET-conflict machinery already refuse it, with no special-casing
    needed in this pass? Two devices on TWO DIFFERENT board sockets that
    happen to share ONE physical SPI controller (bus.path) and whose own
    CS pins BOTH resolve to the pin the board's existing array names at
    index 0 -- both copper-fixed (`shield,cs-position`), the one shape
    that bypasses allocate_cs_positions's own same-call `taken` guard
    (an ordinary pool-drawn pair could never collide THIS way -- the
    pool guard already prevents two pool members from choosing the same
    net within one call). allocate_cs itself raises no diagnostic (the
    reuse-vs-collision checks above are index/reg-shaped, not net-
    shaped) -- but both placements register a `dedicated` NetClaim on
    the SAME key, and merging that into check_nets (analyzer/__init__.py's
    own composer order, reproduced by hand here) is what actually
    refuses it, exactly like any other two-exclusive-claims-one-pin
    conflict (test_gpio.py's own
    test_check_nets_two_dedicated_claims_are_an_exclusive_conflict)."""
    from rigc.analyzer.gpio import check_nets, merge_nets

    existing = (("gpiod", 11, 1),)
    socket_a = _socket(gpio_map={16: ("gpiod", 11, 0)}, existing_cs_gpios=existing)
    socket_b = _socket(gpio_map={5: ("gpiod", 11, 0)}, existing_cs_gpios=existing)
    dev_a = _dev("a", cs_position=16)
    dev_b = _dev("b", cs_position=5)
    inst_a = _inst("left", dev_a)
    inst_b = _inst("right", dev_b)
    rig = Rig(name="r", instances=[inst_a, inst_b])

    result, diags = allocate_cs(
        rig, {"left": {"plug": socket_a}, "right": {"plug": socket_b}}, {"t": _ctype()}, {}
    )
    assert diags == []  # this pass alone sees nothing wrong

    net_diags = check_nets(merge_nets({}, result.nets), {"t": _ctype()})

    assert len(net_diags) == 1
    assert net_diags[0].code == "phys-cs"
    assert "exclusive-resource conflict" in net_diags[0].message
