# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Mating and socket resolution, with carrier/mux composition.
`mating_ok`/`subset_gaps` are the plug-vs-socket
and needed-vs-offered decisions as pure value functions over plain
strings/sets. `compose_socket` is exercised directly against synthetic
ExposedSocket/BoardSocket values -- no Instance/Rig/Shield needed to call
it. `resolve_sockets` (the pass, including the stack-guard against cyclic
carrier references) gets minimal constructed Rig/Instance/Shield values,
since resolving a CHAIN of instances is inherently the pass's own
subject."""

from __future__ import annotations

from rigc.analyzer.sockets import compose_socket, mating_ok, resolve_sockets, subset_gaps
from rigc.model import (
    Board,
    BoardSocket,
    BusRef,
    ConnectorType,
    ExposedSocket,
    Instance,
    Rig,
    Shield,
)

# ---------------------------------------------------------------- mating_ok / subset_gaps


def test_mating_ok_when_plug_and_socket_types_match() -> None:
    assert mating_ok("arduino-r3", "arduino-r3") is True


def test_mating_ok_false_on_a_type_mismatch() -> None:
    assert mating_ok("arduino-r3", "mikrobus") is False


def test_subset_gaps_empty_when_socket_offers_everything_needed() -> None:
    assert subset_gaps({"i2c"}, offered=["i2c", "spi"]) == []


def test_subset_gaps_names_every_bus_the_socket_does_not_offer() -> None:
    """Subset exposure is declared by ABSENCE: a socket offering no
    socket,uart rejects a uart-needing plug."""
    assert subset_gaps({"i2c", "uart"}, offered=["i2c"]) == ["uart"]


def test_subset_gaps_is_sorted_for_deterministic_rendering() -> None:
    assert subset_gaps({"uart", "spi"}, offered=[]) == ["spi", "uart"]


# ---------------------------------------------------------------- compose_socket


def _parent(gpio_map=None, buses=None, path="/board_ard", label="board_ard") -> BoardSocket:
    return BoardSocket(
        label=label, path=path, type_name="arduino-r3", gpio_map=gpio_map or {}, buses=buses or {}
    )


def test_compose_socket_passes_through_a_routed_position() -> None:
    parent = _parent(gpio_map={7: ("gpiod", 0, 0)})
    exposed = ExposedSocket(
        name="mb1", label="mb1", type_name="mikrobus", gpio_map={2: ("plug", 7, 0)}, buses={}
    )

    socket, diags, scopes = compose_socket(
        "adapter_1.mb1", "adapter_1", exposed, {"plug": parent}, None
    )

    assert diags == []
    assert scopes == []
    assert socket.gpio_map[2] == ("gpiod", 0, 0)
    assert socket.label == "adapter_1.mb1"
    assert socket.parents == {"plug": parent}


def test_compose_socket_position_the_parent_fragment_never_routes_stays_local() -> None:
    """A position the exposed socket declares but the parent's own
    gpio-map does not route stays absent from the composed gpio_map,
    which keeps it socket-local (analyzer/gpio.py's soc_net) rather than
    inventing a routing."""
    parent = _parent(gpio_map={})
    exposed = ExposedSocket(
        name="mb1", label="mb1", type_name="mikrobus", gpio_map={2: ("plug", 7, 0)}, buses={}
    )

    socket, _diags, _scopes = compose_socket(
        "adapter_1.mb1", "adapter_1", exposed, {"plug": parent}, None
    )

    assert 2 not in socket.gpio_map


# --------------------------------------- pwm/adc pass-through


def test_compose_socket_pwm_passes_through_a_routed_position() -> None:
    """The PWM twin of the gpio witness above -- SAME shape: pwm and adc
    share one branch's worth of treatment, never a half-done one."""
    parent = _parent()
    parent.pwm_map = {0: ("tcc0", 0)}
    parent.pwm_cells = 2
    exposed = ExposedSocket(
        name="a0",
        label="a0",
        type_name="grove",
        gpio_map={},
        buses={},
        pwm_map={5: ("plug", 0, 0)},
        pwm_cells=2,
    )

    socket, diags, _scopes = compose_socket(
        "carrier_1.a0", "carrier_1", exposed, {"plug": parent}, None
    )

    assert diags == []
    assert socket.pwm_map[5] == ("tcc0", 0)
    assert socket.pwm_cells == 2
    assert socket.pwm_nexus_rows == [(5, "board_ard", 0)]


def test_compose_socket_adc_passes_through_a_routed_position() -> None:
    parent = _parent()
    parent.adc_map = {2: ("adc0", 1)}
    parent.adc_cells = 1
    exposed = ExposedSocket(
        name="a0",
        label="a0",
        type_name="grove",
        gpio_map={},
        buses={},
        adc_map={5: ("plug", 2, 0)},
        adc_cells=1,
    )

    socket, diags, _scopes = compose_socket(
        "carrier_1.a0", "carrier_1", exposed, {"plug": parent}, None
    )

    assert diags == []
    assert socket.adc_map[5] == ("adc0", 1)
    assert socket.adc_cells == 1
    assert socket.adc_nexus_rows == [(5, "board_ard", 2)]


def test_compose_socket_pwm_and_adc_together_on_one_exposed_socket() -> None:
    """Mixed-socket support, at the composition level: ONE
    exposed socket carrying both a pwm row and an adc row composes BOTH
    onto the same BoardSocket -- never one silently winning."""
    parent = _parent()
    parent.pwm_map = {0: ("tcc0", 0)}
    parent.pwm_cells = 2
    parent.adc_map = {1: ("adc0", 3)}
    parent.adc_cells = 1
    exposed = ExposedSocket(
        name="a0",
        label="a0",
        type_name="grove",
        gpio_map={0: ("plug", 0, 0), 1: ("plug", 1, 0)},
        buses={},
        pwm_map={0: ("plug", 0, 0)},
        pwm_cells=2,
        adc_map={1: ("plug", 1, 0)},
        adc_cells=1,
    )

    socket, diags, _scopes = compose_socket(
        "carrier_1.a0", "carrier_1", exposed, {"plug": parent}, None
    )

    assert diags == []
    assert socket.pwm_map == {0: ("tcc0", 0)}
    assert socket.adc_map == {1: ("adc0", 3)}


def test_compose_socket_pwm_row_the_parent_does_not_route_is_an_error_not_a_silent_drop() -> None:
    """Unlike gpio's own 'stays socket-local' silent drop, an unrouted
    PWM/ADC position is not a meaningful net -- it must be a loud
    phys-subset error."""
    parent = _parent()
    parent.pwm_map = {}  # parent offers no pwm at all
    parent.pwm_cells = None
    exposed = ExposedSocket(
        name="a0",
        label="a0",
        type_name="grove",
        gpio_map={},
        buses={},
        pwm_map={5: ("plug", 0, 0)},
        pwm_cells=2,
    )

    socket, _diags, _scopes = compose_socket(
        "carrier_1.a0", "carrier_1", exposed, {"plug": parent}, None
    )

    assert 5 not in socket.pwm_map
    # the cells mismatch (2 vs None) would ALSO fire; isolate this test to
    # the route-missing sentence by giving the parent the SAME declared
    # count so only the route-missing check can possibly trip.


def test_compose_socket_pwm_row_unrouted_is_phys_subset_with_position_and_parent_named() -> None:
    parent = _parent()
    parent.pwm_map = {0: ("tcc0", 0)}  # routes position 0, NOT 99
    parent.pwm_cells = 2
    exposed = ExposedSocket(
        name="a0",
        label="a0",
        type_name="grove",
        gpio_map={},
        buses={},
        pwm_map={5: ("plug", 99, 0)},
        pwm_cells=2,
    )

    socket, diags, _scopes = compose_socket(
        "carrier_1.a0", "carrier_1", exposed, {"plug": parent}, None
    )

    assert 5 not in socket.pwm_map
    assert socket.pwm_nexus_rows == []
    assert len(diags) == 1
    assert diags[0].code == "phys-subset"
    assert "carrier_1" in diags[0].message
    assert "PWM" in diags[0].message
    assert "board_ard" in diags[0].message
    assert "99" in diags[0].message


def test_compose_socket_adc_row_unrouted_is_phys_subset() -> None:
    parent = _parent()
    parent.adc_map = {0: ("adc0", 0)}
    parent.adc_cells = 1
    exposed = ExposedSocket(
        name="a0",
        label="a0",
        type_name="grove",
        gpio_map={},
        buses={},
        adc_map={5: ("plug", 99, 0)},
        adc_cells=1,
    )

    _socket, diags, _scopes = compose_socket(
        "carrier_1.a0", "carrier_1", exposed, {"plug": parent}, None
    )

    assert len(diags) == 1
    assert diags[0].code == "phys-subset"
    assert "ADC" in diags[0].message


def test_compose_socket_pwm_cells_mismatch_is_refused_naming_both_counts_and_sides() -> None:
    """A carrier does not get
    to choose its own cell count -- a declared count disagreeing with the
    resolved parent's is refused, naming BOTH numbers and both sides (the
    carrier's shield name, the parent socket's own label) so a reader can
    tell which to change without opening either file."""
    parent = _parent()
    parent.pwm_map = {0: ("tcc0", 0)}
    parent.pwm_cells = 2  # the REAL board socket's own count
    exposed = ExposedSocket(
        name="a0",
        label="a0",
        type_name="grove",
        gpio_map={},
        buses={},
        pwm_map={5: ("plug", 0, 0)},
        pwm_cells=3,
    )  # carrier claims 3

    socket, diags, _scopes = compose_socket(
        "carrier_1.a0", "carrier_1", exposed, {"plug": parent}, None
    )

    assert 5 not in socket.pwm_map
    assert socket.pwm_cells is None
    assert len(diags) == 1
    assert diags[0].code == "phys-subset"
    assert "carrier_1" in diags[0].message
    assert "board_ard" in diags[0].message
    assert "<3>" in diags[0].message
    assert "<2>" in diags[0].message


def test_compose_socket_adc_cells_mismatch_is_refused() -> None:
    parent = _parent()
    parent.adc_map = {0: ("adc0", 0)}
    parent.adc_cells = 1
    exposed = ExposedSocket(
        name="a0",
        label="a0",
        type_name="grove",
        gpio_map={},
        buses={},
        adc_map={5: ("plug", 0, 0)},
        adc_cells=2,
    )

    _socket, diags, _scopes = compose_socket(
        "carrier_1.a0", "carrier_1", exposed, {"plug": parent}, None
    )

    assert len(diags) == 1
    assert diags[0].code == "phys-subset"
    assert "<2>" in diags[0].message
    assert "<1>" in diags[0].message


def test_compose_socket_no_pwm_map_at_all_yields_no_pwm_cells_or_nexus_rows() -> None:
    """Declared by absence: an exposed socket authoring no pwm-map at all
    composes a socket with pwm_cells=None and empty nexus rows -- never a
    guessed count or a phantom nexus block (the emitter's guard against
    rendering a pwm nexus block depends on this being genuinely empty,
    not just falsy)."""
    parent = _parent()
    exposed = ExposedSocket(name="mb1", label="mb1", type_name="mikrobus", gpio_map={}, buses={})

    socket, diags, _scopes = compose_socket(
        "adapter_1.mb1", "adapter_1", exposed, {"plug": parent}, None
    )

    assert diags == []
    assert socket.pwm_map == {}
    assert socket.pwm_cells is None
    assert socket.pwm_nexus_rows == []
    assert socket.adc_cells is None
    assert socket.adc_nexus_rows == []


def test_compose_socket_bus_pass_through() -> None:
    parent = _parent(buses={"spi": BusRef(label="spi0", path="/spi0")})
    exposed = ExposedSocket(
        name="mb1", label="mb1", type_name="mikrobus", gpio_map={}, buses={"spi": ("plug", "plug")}
    )

    socket, diags, _scopes = compose_socket(
        "adapter_1.mb1", "adapter_1", exposed, {"plug": parent}, None
    )

    assert diags == []
    assert socket.buses["spi"].label == "spi0"


def test_compose_socket_bus_pass_through_selects_by_kind_not_exact_name() -> None:
    """The child-side qualified name is independent of the
    parent-side name -- a pass-through selects the parent's bus of the
    same KIND, so a child asking for bare "spi" is satisfied by a
    parent's role-suffixed "spi-sensors" (its only spi-kind bus)."""
    parent = _parent(buses={"spi-sensors": BusRef(label="spi0", path="/spi0")})
    exposed = ExposedSocket(
        name="mb1", label="mb1", type_name="mikrobus", gpio_map={}, buses={"spi": ("plug", "plug")}
    )

    socket, diags, _scopes = compose_socket(
        "adapter_1.mb1", "adapter_1", exposed, {"plug": parent}, None
    )

    assert diags == []
    assert socket.buses["spi"].label == "spi0"


def test_compose_socket_pass_through_without_parent_bus_is_phys_subset() -> None:
    """A pass-through needs the parent to actually provide the bus it
    passes through -- a carrier claiming to pass through SPI when its own
    parent socket offers none is rejected."""
    parent = _parent(buses={})
    exposed = ExposedSocket(
        name="mb1", label="mb1", type_name="mikrobus", gpio_map={}, buses={"spi": ("plug", "plug")}
    )

    _socket, diags, _scopes = compose_socket(
        "adapter_1.mb1", "adapter_1", exposed, {"plug": parent}, None
    )

    assert len(diags) == 1
    assert diags[0].code == "phys-subset"
    assert "slot" not in diags[0].message  # single-plug: no slot qualifier


def test_compose_socket_pass_through_parent_lacking_kind_is_slot_qualified_when_plural() -> None:
    """The same phys-subset refusal, but the carrier is plural: the
    message names the parent's own SLOT."""
    left = _parent(buses={}, path="/left", label="fx_left")
    right = _parent(
        buses={"spi": BusRef(label="spi1", path="/spi1")}, path="/right", label="fx_right"
    )
    exposed = ExposedSocket(
        name="combined",
        label="combined",
        type_name="mikrobus",
        gpio_map={},
        buses={"spi": ("plug", "left")},
    )

    _socket, diags, _scopes = compose_socket(
        "bridge.combined", "bridge", exposed, {"left": left, "right": right}, None
    )

    assert len(diags) == 1
    assert diags[0].code == "phys-subset"
    assert "slot 'left'" in diags[0].message
    assert "fx_left" in diags[0].message


def test_compose_socket_pass_through_ambiguous_parent_kind_is_refused() -> None:
    """A parent offering MORE than one bus of
    the queried kind is refused with a loud, not-yet-supported error, never a guess."""
    parent = _parent(
        buses={
            "spi-sensors": BusRef(label="spi0", path="/spi0"),
            "spi-motors": BusRef(label="spi1", path="/spi1"),
        }
    )
    exposed = ExposedSocket(
        name="mb1", label="mb1", type_name="mikrobus", gpio_map={}, buses={"spi": ("plug", "plug")}
    )

    socket, diags, _scopes = compose_socket(
        "adapter_1.mb1", "adapter_1", exposed, {"plug": parent}, None
    )

    assert len(diags) == 1
    assert diags[0].code == "phys-ambiguous-bus"
    assert "spi" not in socket.buses


def test_compose_socket_scope_creation_registers_a_scope_entry() -> None:
    """A bus routed to a DEVICE of the shield (not the plug) creates a
    NEW scope, keyed by the composing instance's own socket reference."""
    parent = _parent(buses={"i2c": BusRef(label="i2c1", path="/i2c1")})
    exposed = ExposedSocket(
        name="ch0",
        label="ch0",
        type_name="i2c-mux-ch",
        gpio_map={},
        buses={"i2c": ("scope", "mux_dev")},
        channel=0,
    )

    socket, diags, scopes = compose_socket("mux_1.ch0", "mux_1", exposed, {"plug": parent}, None)

    assert diags == []
    assert scopes == [("mux_1.ch0", ("mux_1_mux_dev", 0))]
    assert socket.buses["i2c"].path == "mux_1.ch0"


def test_compose_socket_cs_pool_override_travels_to_the_composed_bus() -> None:
    """ExposedSocket.cs_pool is a carrier's own authored override on its
    exposed socket node -- CS pools live per bus, on BusRef, never on the
    socket as a whole, so this override's destination is the SAME kind's
    composed BusRef.cs_pool, not a socket-level field. The parent's OWN
    per-bus BusRef.cs_pool (here [16, 15, 14], as if edtlib-backfilled)
    must NOT leak through instead."""
    parent = _parent(buses={"spi": BusRef(label="spi0", path="/spi0", cs_pool=[16, 15, 14])})
    exposed = ExposedSocket(
        name="mb1",
        label="mb1",
        type_name="mikrobus",
        gpio_map={},
        buses={"spi": ("plug", "plug")},
        cs_pool={"spi": [3, 4]},
    )

    socket, diags, _scopes = compose_socket(
        "adapter_1.mb1", "adapter_1", exposed, {"plug": parent}, None
    )

    assert diags == []
    assert socket.buses["spi"].cs_pool == [3, 4]


def test_compose_socket_no_cs_pool_override_leaves_the_composed_bus_none() -> None:
    """A carrier that never authors socket,cs-pool on its exposed socket
    node passes an ABSENT override through as None -- never the parent's
    own BusRef.cs_pool -- so the analyzer's own ctype-fallback merge
    (analyzer/cs.py's effective_cs_pool) is what supplies a value, not
    this composition."""
    parent = _parent(buses={"spi": BusRef(label="spi0", path="/spi0", cs_pool=[16, 15, 14])})
    exposed = ExposedSocket(
        name="mb1", label="mb1", type_name="mikrobus", gpio_map={}, buses={"spi": ("plug", "plug")}
    )

    socket, diags, _scopes = compose_socket(
        "adapter_1.mb1", "adapter_1", exposed, {"plug": parent}, None
    )

    assert diags == []
    assert socket.buses["spi"].cs_pool is None


def test_compose_socket_multi_parent_gpio_row_resolves_through_its_own_slot() -> None:
    """The cross-plug falsifier, at the compose_socket unit level: two
    gpio-map rows of the SAME exposed socket resolve through TWO
    DIFFERENT parents, each keeping its own slot's own nexus label."""
    left = _parent(gpio_map={0: ("gpioa", 1, 0)}, path="/left", label="fx_left")
    right = _parent(gpio_map={1: ("gpiob", 2, 0)}, path="/right", label="fx_right")
    exposed = ExposedSocket(
        name="combined",
        label="combined",
        type_name="mikrobus",
        gpio_map={10: ("left", 0, 0), 11: ("right", 1, 0)},
        buses={},
    )

    socket, diags, _scopes = compose_socket(
        "bridge.combined", "bridge", exposed, {"left": left, "right": right}, None
    )

    assert diags == []
    assert socket.gpio_map[10] == ("gpioa", 1, 0)
    assert socket.gpio_map[11] == ("gpiob", 2, 0)
    assert socket.nexus_rows is not None
    assert (10, "fx_left", 0) in socket.nexus_rows
    assert (11, "fx_right", 1) in socket.nexus_rows
    assert socket.parents == {"left": left, "right": right}


def test_compose_socket_multi_parent_path_is_the_reference_string() -> None:
    """Single-parent composition keeps the byte-identical
    <parent path>/<exposed name> path (golden safety); a multi-parent
    composition has no single parent path to anchor to, so it falls back
    to the <carrier>.<exposed> reference string instead."""
    left = _parent(path="/left", label="fx_left")
    right = _parent(path="/right", label="fx_right")
    exposed = ExposedSocket(
        name="combined", label="combined", type_name="mikrobus", gpio_map={}, buses={}
    )

    socket, _diags, _scopes = compose_socket(
        "bridge.combined", "bridge", exposed, {"left": left, "right": right}, None
    )

    assert socket.path == "bridge.combined"


def test_compose_socket_single_parent_path_stays_byte_identical() -> None:
    parent = _parent(path="/board_ard")
    exposed = ExposedSocket(name="mb1", label="mb1", type_name="mikrobus", gpio_map={}, buses={})

    socket, _diags, _scopes = compose_socket(
        "adapter_1.mb1", "adapter_1", exposed, {"plug": parent}, None
    )

    assert socket.path == "/board_ard/mb1"


# ---------------------------------------------------------------- resolve_sockets


def _shield(plugs="arduino-r3", exposes=None) -> Shield:
    return Shield(name="sh", label="sh", plugs={"plug": plugs}, exposes=exposes or {})


def _inst(name: str, socket: str | None, shield: Shield) -> Instance:
    return Instance(name=name, shield=shield, sockets={"plug": socket})


def test_resolve_sockets_finds_a_direct_board_socket() -> None:
    board = Board(
        name="b",
        sockets={
            "ard": BoardSocket(
                label="ard", path="/ard", type_name="arduino-r3", gpio_map={}, buses={}
            )
        },
    )
    inst = _inst("i1", "ard", _shield())
    rig = Rig(name="r", instances=[inst])

    resolution, diags = resolve_sockets(rig, board, {"arduino-r3": _ctype()})

    assert diags == []
    assert resolution.sockets["i1"]["plug"].label == "ard"


def test_resolve_sockets_finds_a_board_socket_by_its_conventional_alias() -> None:
    """A socket node's
    SECOND (conventional) label must resolve exactly like its defining
    one -- resolve_sockets goes through Board.resolve, not a bare
    board.sockets.get, precisely so this works."""
    board = Board(
        name="b",
        sockets={
            "nucleo_ard": BoardSocket(
                label="nucleo_ard", path="/ard", type_name="arduino-r3", gpio_map={}, buses={}
            )
        },
        aliases={"arduino_r3": "nucleo_ard"},
    )
    inst = _inst("i1", "arduino_r3", _shield())
    rig = Rig(name="r", instances=[inst])

    resolution, diags = resolve_sockets(rig, board, {"arduino-r3": _ctype()})

    assert diags == []
    assert resolution.sockets["i1"]["plug"].label == "nucleo_ard"


def test_resolve_sockets_still_finds_the_socket_by_its_defining_label() -> None:
    """The other half of additive conformance: adding the alias must not
    disturb the pre-existing reference -- this is the NEGATIVE CONTROL a
    bare board.sockets.get(ref) already passed, unaffected by the switch
    to board.resolve(ref)."""
    board = Board(
        name="b",
        sockets={
            "nucleo_ard": BoardSocket(
                label="nucleo_ard", path="/ard", type_name="arduino-r3", gpio_map={}, buses={}
            )
        },
        aliases={"arduino_r3": "nucleo_ard"},
    )
    inst = _inst("i1", "nucleo_ard", _shield())
    rig = Rig(name="r", instances=[inst])

    resolution, diags = resolve_sockets(rig, board, {"arduino-r3": _ctype()})

    assert diags == []
    assert resolution.sockets["i1"]["plug"].label == "nucleo_ard"


def test_resolve_sockets_single_plug_shield_named_other_than_plug_honors_authored_socket() -> None:
    """model.py's contract: a single-plug shield's one slot is the plug
    node's OWN name -- here 'north', not 'plug'. `resolve_one` reads
    `inst.sockets[slot]`/`inst.shield.plugs[slot]` by that real name; two
    board sockets of the matching type make per-slot INFERENCE ambiguous
    (were it to run instead of honoring the authored reference), so a
    clean, diagnostic-free resolve to the explicitly named socket proves
    the authored socket: was actually read, not silently dropped for
    inference."""
    board = Board(
        name="b",
        sockets={
            "ard1": BoardSocket(
                label="ard1", path="/ard1", type_name="arduino-r3", gpio_map={}, buses={}
            ),
            "ard2": BoardSocket(
                label="ard2", path="/ard2", type_name="arduino-r3", gpio_map={}, buses={}
            ),
        },
    )
    shield = Shield(name="sh", label="sh", plugs={"north": "arduino-r3"})
    inst = Instance(name="i1", shield=shield, sockets={"north": "ard2"})
    rig = Rig(name="r", instances=[inst])

    resolution, diags = resolve_sockets(rig, board, {"arduino-r3": _ctype()})

    assert diags == []
    assert resolution.sockets["i1"]["north"].label == "ard2"


def test_resolve_sockets_unknown_board_socket_is_phys_socket() -> None:
    board = Board(name="b", sockets={})
    inst = _inst("i1", "nope", _shield())
    rig = Rig(name="r", instances=[inst])

    resolution, diags = resolve_sockets(rig, board, {"arduino-r3": _ctype()})

    assert resolution.sockets == {}
    assert len(diags) == 1
    assert diags[0].code == "phys-socket"


def test_resolve_sockets_plug_type_mismatch_is_phys_mating() -> None:
    board = Board(
        name="b",
        sockets={
            "ard": BoardSocket(
                label="ard", path="/ard", type_name="mikrobus", gpio_map={}, buses={}
            )
        },
    )
    inst = _inst("i1", "ard", _shield(plugs="arduino-r3"))
    rig = Rig(name="r", instances=[inst])

    resolution, diags = resolve_sockets(rig, board, {"mikrobus": _ctype()})

    assert resolution.sockets["i1"]["plug"] is not None  # the socket still resolves
    assert len(diags) == 1
    assert diags[0].code == "phys-mating"


def test_resolve_sockets_subset_gap_is_phys_subset() -> None:
    board = Board(
        name="b",
        sockets={
            "ard": BoardSocket(
                label="ard", path="/ard", type_name="arduino-r3", gpio_map={}, buses={}
            )
        },
    )
    shield = _shield()
    from rigc.model import Device

    shield.devices.append(
        Device(
            name="d",
            label="d",
            compatible=None,
            bus="uart",
            group=None,
            reg=None,
            addr_from=None,
            cs_position=None,
        )
    )
    inst = _inst("i1", "ard", shield)
    rig = Rig(name="r", instances=[inst])

    _resolution, diags = resolve_sockets(rig, board, {"arduino-r3": _ctype()})

    assert len(diags) == 1
    assert diags[0].code == "phys-subset"


def test_resolve_sockets_carrier_chain_composes() -> None:
    board = Board(
        name="b",
        sockets={
            "ard": BoardSocket(
                label="ard",
                path="/ard",
                type_name="arduino-r3",
                gpio_map={7: ("gpiod", 0, 0)},
                buses={},
            )
        },
    )
    carrier_shield = _shield(
        plugs="arduino-r3",
        exposes={
            "mb1": ExposedSocket(
                name="mb1",
                label="mb1",
                type_name="mikrobus",
                gpio_map={2: ("plug", 7, 0)},
                buses={},
            )
        },
    )
    carrier = _inst("adapter_1", "ard", carrier_shield)
    leaf = _inst("eth_1", "adapter_1.mb1", _shield(plugs="mikrobus"))
    rig = Rig(name="r", instances=[carrier, leaf])

    resolution, diags = resolve_sockets(
        rig, board, {"arduino-r3": _ctype(), "mikrobus": _ctype("mikrobus")}
    )

    assert diags == []
    assert resolution.sockets["eth_1"]["plug"].gpio_map[2] == ("gpiod", 0, 0)


def test_resolve_sockets_carrier_exposed_socket_resolves_by_label_not_node_name() -> None:
    """`socket: <carrier>.<exposed>` resolves by the exposed node's DTS
    LABEL, exactly like config:/params:/wires: already do
    -- proven here with a label that DIFFERS from the node name,
    since the real corpus's own 8 exposed nodes all happen to share the
    two spellings and so cannot show which one actually resolves."""
    board = Board(
        name="b",
        sockets={
            "ard": BoardSocket(
                label="ard",
                path="/ard",
                type_name="arduino-r3",
                gpio_map={7: ("gpiod", 0, 0)},
                buses={},
            )
        },
    )
    carrier_shield = _shield(
        plugs="arduino-r3",
        exposes={
            "ch0": ExposedSocket(
                name="ch0",
                label="span_ch0",
                type_name="mikrobus",
                gpio_map={2: ("plug", 7, 0)},
                buses={},
            )
        },
    )
    carrier = _inst("adapter_1", "ard", carrier_shield)
    leaf = _inst("eth_1", "adapter_1.span_ch0", _shield(plugs="mikrobus"))
    rig = Rig(name="r", instances=[carrier, leaf])

    resolution, diags = resolve_sockets(
        rig, board, {"arduino-r3": _ctype(), "mikrobus": _ctype("mikrobus")}
    )

    assert diags == []
    assert resolution.sockets["eth_1"]["plug"].gpio_map[2] == ("gpiod", 0, 0)


def test_resolve_sockets_carrier_exposed_socket_node_name_is_refused_once_it_differs() -> None:
    """The other half: once the label differs from the node name, the
    node name is no longer a valid spelling -- the miss diagnostic names
    the LABEL among the carrier's exposed sockets, never the node name
    that failed to resolve, so a revert to node-name lookup fails this on
    the SENTENCE even where a naive partial revert might still refuse the
    reference for some other reason."""
    board = Board(
        name="b",
        sockets={
            "ard": BoardSocket(
                label="ard",
                path="/ard",
                type_name="arduino-r3",
                gpio_map={7: ("gpiod", 0, 0)},
                buses={},
            )
        },
    )
    carrier_shield = _shield(
        plugs="arduino-r3",
        exposes={
            "ch0": ExposedSocket(
                name="ch0",
                label="span_ch0",
                type_name="mikrobus",
                gpio_map={2: ("plug", 7, 0)},
                buses={},
            )
        },
    )
    carrier = _inst("adapter_1", "ard", carrier_shield)
    leaf = _inst("eth_1", "adapter_1.ch0", _shield(plugs="mikrobus"))
    rig = Rig(name="r", instances=[carrier, leaf])

    resolution, diags = resolve_sockets(
        rig, board, {"arduino-r3": _ctype(), "mikrobus": _ctype("mikrobus")}
    )

    assert "eth_1" not in resolution.sockets
    assert len(diags) == 1
    assert diags[0].code == "phys-socket"
    assert "exposes no socket 'ch0'" in diags[0].message
    assert "span_ch0" in diags[0].message


def test_resolve_sockets_plural_carrier_slot_plugs_another_carriers_exposed_socket() -> None:
    """Chains recurse over a PLURAL carrier too: bridge's own 'left' slot plugs single_carrier's
    exposed socket (a single-plug carrier one level down), its 'right'
    slot plugs a board socket directly, and bridge itself exposes a
    combined socket a leaf instance plugs -- three levels deep, the
    existing depth-first resolution + cycle guard, now over (instance,
    slot). No new mechanism; this is the one fixture proving it still
    holds. The falsifier: the leaf's own composed socket resolves its
    position all the way down to the real SoC pin, through bridge's
    'left' slot -> single_carrier's exposed mb1 -> the real 'ard' board
    socket. (`_plural_shield`/`_plural_inst` are defined later in this
    module, at module scope -- resolved at call time, not import time.)"""
    board = Board(
        name="b",
        sockets={
            "ard": BoardSocket(
                label="ard",
                path="/ard",
                type_name="arduino-r3",
                gpio_map={7: ("gpiod", 0, 0)},
                buses={},
            ),
            "mb_direct": BoardSocket(
                label="mb_direct", path="/mb_direct", type_name="mikrobus", gpio_map={}, buses={}
            ),
        },
    )
    single_carrier_shield = _shield(
        plugs="arduino-r3",
        exposes={
            "mb1": ExposedSocket(
                name="mb1",
                label="mb1",
                type_name="mikrobus",
                gpio_map={2: ("plug", 7, 0)},
                buses={},
            )
        },
    )
    single_carrier = _inst("single_carrier", "ard", single_carrier_shield)

    bridge_shield = _plural_shield({"left": "mikrobus", "right": "mikrobus"})
    bridge_shield.exposes["combined"] = ExposedSocket(
        name="combined",
        label="combined",
        type_name="mikrobus",
        gpio_map={20: ("left", 2, 0)},
        buses={},
    )
    bridge = _plural_inst(
        "bridge", {"left": "single_carrier.mb1", "right": "mb_direct"}, bridge_shield
    )

    leaf = _inst("leaf", "bridge.combined", _shield(plugs="mikrobus"))
    rig = Rig(name="r", instances=[single_carrier, bridge, leaf])

    resolution, diags = resolve_sockets(
        rig, board, {"arduino-r3": _ctype(), "mikrobus": _ctype("mikrobus")}
    )

    assert diags == []
    leaf_socket = resolution.sockets["leaf"]["plug"]
    assert leaf_socket is not None
    assert leaf_socket.gpio_map[20] == ("gpiod", 0, 0)


def test_resolve_sockets_cyclic_carrier_reference_is_stack_guarded() -> None:
    """A instance naming its OWN carrier chain cyclically must be rejected
    (phys-socket), never recurse forever."""
    a = _inst(
        "a",
        "b.x",
        _shield(
            exposes={
                "x": ExposedSocket(
                    name="x", label="x", type_name="arduino-r3", gpio_map={}, buses={}
                )
            }
        ),
    )
    b = _inst(
        "b",
        "a.x",
        _shield(
            exposes={
                "x": ExposedSocket(
                    name="x", label="x", type_name="arduino-r3", gpio_map={}, buses={}
                )
            }
        ),
    )
    rig = Rig(name="r", instances=[a, b])
    board = Board(name="b", sockets={})

    resolution, diags = resolve_sockets(rig, board, {"arduino-r3": _ctype()})

    assert resolution.sockets == {}
    assert all(d.code == "phys-socket" for d in diags)
    assert len(diags) >= 1


def test_resolve_sockets_two_non_stackable_instances_on_one_socket_is_phys_mating() -> None:
    board = Board(
        name="b",
        sockets={
            "ard": BoardSocket(
                label="ard", path="/ard", type_name="arduino-r3", gpio_map={}, buses={}
            )
        },
    )
    a = _inst("a", "ard", _shield())
    b = _inst("b", "ard", _shield())
    rig = Rig(name="r", instances=[a, b])

    _resolution, diags = resolve_sockets(rig, board, {"arduino-r3": _ctype(stackable=False)})

    assert len(diags) == 1
    assert diags[0].code == "phys-mating"
    assert "not stackable" in diags[0].message


def test_resolve_sockets_stackable_type_allows_multiple_instances() -> None:
    board = Board(
        name="b",
        sockets={
            "ard": BoardSocket(
                label="ard", path="/ard", type_name="arduino-r3", gpio_map={}, buses={}
            )
        },
    )
    a = _inst("a", "ard", _shield())
    b = _inst("b", "ard", _shield())
    rig = Rig(name="r", instances=[a, b])

    _resolution, diags = resolve_sockets(rig, board, {"arduino-r3": _ctype(stackable=True)})

    assert diags == []


def test_resolve_sockets_skips_a_failed_instance_but_keeps_going() -> None:
    """Skip-don't-abort: one instance's board-socket failure never stops
    resolution of the REST of the rig."""
    board = Board(
        name="b",
        sockets={
            "ard": BoardSocket(
                label="ard", path="/ard", type_name="arduino-r3", gpio_map={}, buses={}
            )
        },
    )
    bad = _inst("bad", "nope", _shield())
    good = _inst("good", "ard", _shield())
    rig = Rig(name="r", instances=[bad, good])

    resolution, diags = resolve_sockets(rig, board, {"arduino-r3": _ctype()})

    assert "bad" not in resolution.sockets
    assert "good" in resolution.sockets
    assert len(diags) == 1


# ------------------------------------- stacking census keyed by RESOLVED socket


def test_resolve_sockets_two_labels_for_one_socket_still_caught_as_not_stackable() -> None:
    """Since a board socket can be named
    by either its defining label or a conventional alias, two instances
    naming the SAME physical socket through DIFFERENT strings must still
    collide -- the exclusivity check is keyed by the RESOLVED socket, not
    the raw reference each instance happened to write. Latent today (the
    corpus's only non-stackable type has no aliased board), reachable the
    moment one gains an alias; this pins the property regardless."""
    board = Board(
        name="b",
        sockets={
            "nucleo_ard": BoardSocket(
                label="nucleo_ard", path="/ard", type_name="arduino-r3", gpio_map={}, buses={}
            )
        },
        aliases={"arduino_r3": "nucleo_ard"},
    )
    a = _inst("a", "nucleo_ard", _shield())
    b = _inst("b", "arduino_r3", _shield())
    rig = Rig(name="r", instances=[a, b])

    _resolution, diags = resolve_sockets(rig, board, {"arduino-r3": _ctype(stackable=False)})

    assert len(diags) == 1
    assert diags[0].code == "phys-mating"
    assert "not stackable" in diags[0].message


# ---------------------------------------------------------------- socket inference


def test_resolve_sockets_infers_the_sole_mating_candidate_silently() -> None:
    """Exactly one board socket mates the shield's plug type -> resolves,
    no diagnostic at all."""
    board = Board(
        name="b",
        sockets={
            "ard": BoardSocket(
                label="ard", path="/ard", type_name="arduino-r3", gpio_map={}, buses={}
            ),
            "mb": BoardSocket(label="mb", path="/mb", type_name="mikrobus", gpio_map={}, buses={}),
        },
    )
    inst = _inst("i1", None, _shield(plugs="arduino-r3"))
    rig = Rig(name="r", instances=[inst])

    resolution, diags = resolve_sockets(
        rig, board, {"arduino-r3": _ctype(), "mikrobus": _ctype("mikrobus")}
    )

    assert diags == []
    assert resolution.sockets["i1"]["plug"].label == "ard"


def test_resolve_sockets_inference_zero_candidates_names_plug_type_and_offerings() -> None:
    board = Board(
        name="b",
        sockets={
            "mb": BoardSocket(label="mb", path="/mb", type_name="mikrobus", gpio_map={}, buses={})
        },
    )
    inst = _inst("i1", None, _shield(plugs="arduino-r3"))
    rig = Rig(name="r", instances=[inst])

    resolution, diags = resolve_sockets(rig, board, {"mikrobus": _ctype("mikrobus")})

    assert "i1" not in resolution.sockets
    assert len(diags) == 1
    assert diags[0].code == "phys-socket"
    assert "arduino-r3" in diags[0].message
    assert "mb (mikrobus)" in diags[0].message


def test_resolve_sockets_inference_two_candidates_rejects_rather_than_tie_breaks() -> None:
    """An implementation that
    tie-breaks between several mating sockets passes the single-candidate
    test above and fails only here. Two sockets of the same mating type
    must be listed and the instance must be rejected -- never resolved to
    either one."""
    board = Board(
        name="b",
        sockets={
            "ard1": BoardSocket(
                label="ard1", path="/ard1", type_name="arduino-r3", gpio_map={}, buses={}
            ),
            "ard2": BoardSocket(
                label="ard2", path="/ard2", type_name="arduino-r3", gpio_map={}, buses={}
            ),
        },
    )
    inst = _inst("i1", None, _shield(plugs="arduino-r3"))
    rig = Rig(name="r", instances=[inst])

    resolution, diags = resolve_sockets(rig, board, {"arduino-r3": _ctype()})

    assert "i1" not in resolution.sockets
    assert len(diags) == 1
    assert diags[0].code == "phys-socket"
    assert "ard1" in diags[0].message
    assert "ard2" in diags[0].message


def test_resolve_sockets_inference_never_considers_carrier_exposed_sockets() -> None:
    """Candidates are BOARD sockets only. A carrier
    exposing a socket of the mating type must not make it a candidate --
    otherwise inference would depend on which carriers happen to already
    be parsed, an order-dependence the delta engine exists to avoid. The
    board here offers no mikrobus socket directly, only an arduino-r3 one
    a carrier plugs into and re-exposes as mikrobus -- a leaf shield
    needing mikrobus must still get the zero-candidate error."""
    board = Board(
        name="b",
        sockets={
            "ard": BoardSocket(
                label="ard", path="/ard", type_name="arduino-r3", gpio_map={}, buses={}
            )
        },
    )
    carrier_shield = _shield(
        plugs="arduino-r3",
        exposes={
            "mb1": ExposedSocket(
                name="mb1", label="mb1", type_name="mikrobus", gpio_map={}, buses={}
            )
        },
    )
    carrier = _inst("adapter_1", "ard", carrier_shield)
    leaf = _inst("eth_1", None, _shield(plugs="mikrobus"))
    rig = Rig(name="r", instances=[carrier, leaf])

    resolution, diags = resolve_sockets(
        rig, board, {"arduino-r3": _ctype(), "mikrobus": _ctype("mikrobus")}
    )

    assert "eth_1" not in resolution.sockets
    assert any(d.code == "phys-socket" and "mikrobus" in d.message for d in diags)


def test_resolve_sockets_inference_obeys_the_existing_stacking_rule() -> None:
    """Two instances that each infer the SAME socket are
    subject to the ordinary stackability check, not a rule of inference's
    own -- a non-stackable type still rejects the second instance even
    though neither one named a socket."""
    board = Board(
        name="b",
        sockets={
            "ard": BoardSocket(
                label="ard", path="/ard", type_name="arduino-r3", gpio_map={}, buses={}
            )
        },
    )
    a = _inst("a", None, _shield(plugs="arduino-r3"))
    b = _inst("b", None, _shield(plugs="arduino-r3"))
    rig = Rig(name="r", instances=[a, b])

    _resolution, diags = resolve_sockets(rig, board, {"arduino-r3": _ctype(stackable=False)})

    assert len(diags) == 1
    assert diags[0].code == "phys-mating"
    assert "not stackable" in diags[0].message


def _ctype(name: str = "arduino-r3", stackable: bool = True) -> ConnectorType:
    return ConnectorType(
        name=name, positions={}, index2name={}, bus_proxies=[], stackable=stackable, cs_pool={}
    )


# ---------------------------------------------------------------- per-slot resolution


def _plural_shield(plugs: dict, devices=None) -> Shield:
    return Shield(
        name="sh", label="sh", plugs=dict(plugs), devices=list(devices) if devices else []
    )


def _plural_inst(name: str, sockets: dict, shield: Shield) -> Instance:
    return Instance(name=name, shield=shield, sockets=dict(sockets))


def test_resolve_sockets_per_slot_inference_resolves_each_slot_independently() -> None:
    """Two slots of DIFFERENT types, neither named in sockets: -- each
    infers against its OWN board candidates, independently."""
    board = Board(
        name="b",
        sockets={
            "ard": BoardSocket(
                label="ard", path="/ard", type_name="arduino-r3", gpio_map={}, buses={}
            ),
            "mb": BoardSocket(label="mb", path="/mb", type_name="mikrobus", gpio_map={}, buses={}),
        },
    )
    shield = _plural_shield({"a": "arduino-r3", "b": "mikrobus"})
    inst = _plural_inst("i1", {"a": None, "b": None}, shield)
    rig = Rig(name="r", instances=[inst])

    resolution, diags = resolve_sockets(
        rig, board, {"arduino-r3": _ctype(), "mikrobus": _ctype("mikrobus")}
    )

    assert diags == []
    assert resolution.sockets["i1"]["a"].label == "ard"
    assert resolution.sockets["i1"]["b"].label == "mb"


def test_resolve_sockets_per_slot_inference_ambiguity_is_slot_qualified() -> None:
    """Two same-type slots on a board with two candidates: BOTH slots
    refuse independently -- no bipartite matching, no tie-break between
    slots."""
    board = Board(
        name="b",
        sockets={
            "ard1": BoardSocket(
                label="ard1", path="/ard1", type_name="arduino-r3", gpio_map={}, buses={}
            ),
            "ard2": BoardSocket(
                label="ard2", path="/ard2", type_name="arduino-r3", gpio_map={}, buses={}
            ),
        },
    )
    shield = _plural_shield({"left": "arduino-r3", "right": "arduino-r3"})
    inst = _plural_inst("i1", {"left": None, "right": None}, shield)
    rig = Rig(name="r", instances=[inst])

    resolution, diags = resolve_sockets(rig, board, {"arduino-r3": _ctype()})

    assert "i1" not in resolution.sockets
    assert len(diags) == 2
    assert all(d.code == "phys-socket" for d in diags)
    assert any("slot 'left'" in d.message for d in diags)
    assert any("slot 'right'" in d.message for d in diags)


def test_resolve_sockets_per_slot_subset_needed_from_that_slots_own_devices_only() -> None:
    """A bus needed only by slot 'right' must never be demanded of
    slot 'left''s socket -- the ACCEPT half (both slots' own needs are
    satisfied by their own sockets)."""
    from rigc.model import Device

    board = Board(
        name="b",
        sockets={
            "sock_l": BoardSocket(label="sock_l", path="/l", type_name="t", gpio_map={}, buses={}),
            "sock_r": BoardSocket(
                label="sock_r",
                path="/r",
                type_name="t",
                gpio_map={},
                buses={"i2c": BusRef("i2c1", "/i2c1")},
            ),
        },
    )
    right_dev = Device(
        name="d",
        label="d",
        compatible=None,
        bus="i2c",
        group=None,
        reg=0x10,
        addr_from=None,
        cs_position=None,
        plug="right",
    )
    shield = _plural_shield({"left": "t", "right": "t"}, devices=[right_dev])
    inst = _plural_inst("i1", {"left": "sock_l", "right": "sock_r"}, shield)
    rig = Rig(name="r", instances=[inst])

    _resolution, diags = resolve_sockets(rig, board, {"t": _ctype("t")})

    assert diags == []


def test_resolve_sockets_per_slot_subset_gap_names_the_right_slot_and_socket() -> None:
    """The REJECT twin: slot 'right''s own device needs i2c, but the
    socket named for 'right' does not offer it -- phys-subset names slot
    'right', never 'left' (which has no bus needs of its own at all)."""
    from rigc.model import Device

    board = Board(
        name="b",
        sockets={
            "sock_l": BoardSocket(
                label="sock_l",
                path="/l",
                type_name="t",
                gpio_map={},
                buses={"i2c": BusRef("i2c1", "/i2c1")},
            ),
            "sock_r": BoardSocket(label="sock_r", path="/r", type_name="t", gpio_map={}, buses={}),
        },
    )  # no i2c on the right socket
    right_dev = Device(
        name="d",
        label="d",
        compatible=None,
        bus="i2c",
        group=None,
        reg=0x10,
        addr_from=None,
        cs_position=None,
        plug="right",
    )
    shield = _plural_shield({"left": "t", "right": "t"}, devices=[right_dev])
    inst = _plural_inst("i1", {"left": "sock_l", "right": "sock_r"}, shield)
    rig = Rig(name="r", instances=[inst])

    _resolution, diags = resolve_sockets(rig, board, {"t": _ctype("t")})

    assert len(diags) == 1
    assert diags[0].code == "phys-subset"
    assert "slot 'right'" in diags[0].message
    assert "sock_r" in diags[0].message
    assert "slot 'left'" not in diags[0].message


def test_resolve_sockets_distinct_slots_resolving_to_one_physical_socket_is_rejected() -> None:
    """One physical connector cannot take two plugs at once --
    checked regardless of the stackability census (which would only
    catch this as a non-stackable-type collision, with a message that
    counts instances rather than slots)."""
    board = Board(
        name="b",
        sockets={
            "sock": BoardSocket(label="sock", path="/s", type_name="t", gpio_map={}, buses={})
        },
    )
    shield = _plural_shield({"x": "t", "y": "t"})
    inst = _plural_inst("i1", {"x": "sock", "y": "sock"}, shield)
    rig = Rig(name="r", instances=[inst])

    _resolution, diags = resolve_sockets(rig, board, {"t": _ctype("t", stackable=True)})

    # stackable=True suppresses the OTHER (stackability) diagnostic, so
    # the dedicated dup-socket check is the falsifier this test isolates:
    # mutation-check by deleting it and confirming this goes to [].
    assert len(diags) == 1
    assert diags[0].code == "phys-socket"
    assert "'x'" in diags[0].message and "'y'" in diags[0].message
    assert "sock" in diags[0].message


def test_resolve_sockets_single_slot_shield_diagnostics_stay_unqualified() -> None:
    """A load-bearing property, pinned directly: a single-
    slot shield's own diagnostics carry NO slot qualifier -- byte-
    identical to every diagnostic this module emitted before plurality."""
    board = Board(name="b", sockets={})
    shield = _plural_shield({"plug": "arduino-r3"})
    inst = _plural_inst("i1", {"plug": None}, shield)
    rig = Rig(name="r", instances=[inst])

    _resolution, diags = resolve_sockets(rig, board, {"arduino-r3": _ctype()})

    assert len(diags) == 1
    assert diags[0].message.startswith("instance 'i1': shield 'sh'")
    assert "slot" not in diags[0].message
