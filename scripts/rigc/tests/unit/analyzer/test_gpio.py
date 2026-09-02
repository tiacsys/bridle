# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Net identity and GPIO/PWM/ADC claim collection.
`role_of` and `soc_net` are two value-shaped contracts: both are pure
functions of a property name / (socket, position) pair, asserted here
with no scenario at all. `check_nets` is exercised directly against constructed
NetClaim/Nets values -- no Rig needed, since a net's conflict-or-not
outcome is a function of its claim list alone. `collect_gpio_nets` (the
pass itself) gets one minimal constructed Rig, to pin position/jumper
resolution and pwm/adc channel collection together."""

from __future__ import annotations

from rigc.analyzer.gpio import (
    NetClaim,
    Nets,
    check_nets,
    collect_gpio_nets,
    merge_nets,
    role_of,
    soc_net,
)
from rigc.model import (
    BoardSocket,
    ConnectorType,
    Device,
    FunctionRef,
    Instance,
    Jumper,
    Position,
    Rig,
    Shield,
)

# ---------------------------------------------------------------- role_of


def test_role_of_int_prefixed_prop_is_driver() -> None:
    assert role_of("int1-gpios") == "driver"


def test_role_of_irq_prefixed_prop_is_driver() -> None:
    assert role_of("irq-gpios") == "driver"


def test_role_of_anything_else_is_listener() -> None:
    assert role_of("cs-gpios") == "listener"
    assert role_of("reset-gpios") == "listener"


def test_role_of_strips_the_gpios_suffix_before_matching() -> None:
    """'interrupt-gpios' must match on its STEM ('interrupt'), not the
    literal suffix -- proven by a prop whose suffix alone would not
    contain the hint but whose stem does."""
    assert role_of("interrupt-gpios") == "driver"


# ---------------------------------------------------------------- soc_net


def _socket(gpio_map=None, path="/socket@0", label="s1") -> BoardSocket:
    return BoardSocket(label=label, path=path, type_name="t", gpio_map=gpio_map or {}, buses={})


def test_soc_net_resolves_through_the_gpio_map() -> None:
    socket = _socket(gpio_map={0: ("gpioa", 5, 0)})
    assert soc_net(socket, 0) == ("soc", "gpioa", 5)


def test_soc_net_two_sockets_sharing_a_pin_are_the_same_net() -> None:
    """Two DIFFERENT sockets whose positions map to the same SoC pin
    are the SAME net identity."""
    a = _socket(gpio_map={0: ("gpioa", 5, 0)}, path="/a", label="a")
    b = _socket(gpio_map={3: ("gpioa", 5, 0)}, path="/b", label="b")
    assert soc_net(a, 0) == soc_net(b, 3)


def test_soc_net_unrouted_position_stays_socket_local() -> None:
    """A position the board fragment doesn't route through the gpio-map
    (e.g. mikroBUS INT) stays socket-local, keyed by (socket path,
    position) -- never confused with a routed SoC pin."""
    socket = _socket(gpio_map={}, path="/socket@0")
    assert soc_net(socket, 9) == ("pos", "/socket@0", 9)


# ---------------------------------------------------------------- check_nets


def _inst(name="i") -> Instance:
    return Instance(
        name=name, shield=Shield(name="s", label="s", plugs={"plug": "t"}), sockets={"plug": "sock"}
    )


def _dev(name="d") -> Device:
    return Device(
        name=name,
        label=name,
        compatible=None,
        bus=None,
        group=None,
        reg=None,
        addr_from=None,
        cs_position=None,
    )


def _claim(role: str, what: str = "x", position: int = 0, socket=None) -> NetClaim:
    return NetClaim(
        instance=_inst(),
        device=_dev(),
        what=what,
        role=role,
        socket=socket or _socket(),
        position=position,
    )


def test_check_nets_two_dedicated_claims_are_an_exclusive_conflict() -> None:
    key = ("soc", "gpioa", 0)
    nets: Nets = {key: [_claim("dedicated", "a"), _claim("dedicated", "b")]}
    diags = check_nets(nets, types={"t": _ctype()})
    assert len(diags) == 1
    assert diags[0].code == "phys-cs"


def test_check_nets_two_channel_claims_are_phys_channel() -> None:
    key = ("chan", "tcc0", 0)
    nets: Nets = {key: [_claim("dedicated", "a"), _claim("dedicated", "b")]}
    diags = check_nets(nets, types={"t": _ctype()})
    assert diags[0].code == "phys-channel"


def test_check_nets_dedicated_plus_signal_is_phys_net() -> None:
    key = ("soc", "gpioa", 0)
    nets: Nets = {key: [_claim("dedicated", "a"), _claim("listener", "b")]}
    diags = check_nets(nets, types={"t": _ctype()})
    assert len(diags) == 1
    assert diags[0].code == "phys-net"


def test_check_nets_two_drivers_is_phys_net() -> None:
    key = ("soc", "gpioa", 0)
    nets: Nets = {key: [_claim("driver", "a"), _claim("driver", "b")]}
    diags = check_nets(nets, types={"t": _ctype()})
    assert len(diags) == 1
    assert diags[0].code == "phys-net"


def test_check_nets_one_driver_many_listeners_is_legal() -> None:
    key = ("soc", "gpioa", 0)
    nets: Nets = {key: [_claim("driver", "a"), _claim("listener", "b"), _claim("listener", "c")]}
    assert check_nets(nets, types={"t": _ctype()}) == []


def test_check_nets_a_single_claim_is_never_a_conflict() -> None:
    key = ("soc", "gpioa", 0)
    nets: Nets = {key: [_claim("dedicated", "a")]}
    assert check_nets(nets, types={"t": _ctype()}) == []


def test_merge_nets_concatenates_claims_preserving_order() -> None:
    key = ("soc", "gpioa", 0)
    first: Nets = {key: [_claim("listener", "a")]}
    second: Nets = {key: [_claim("driver", "b")]}
    merged = merge_nets(first, second)
    assert [c.what for c in merged[key]] == ["a", "b"]


# ---------------------------------------------------------------- collect_gpio_nets


def _ctype() -> ConnectorType:
    return ConnectorType(
        name="t",
        positions={"D7": Position(name="D7", index=7, function="gpio")},
        index2name={7: "D7"},
        bus_proxies=[],
        stackable=False,
        cs_pool={},
    )


def test_collect_gpio_nets_registers_a_fixed_position_claim() -> None:
    socket = _socket(gpio_map={7: ("gpioa", 5, 0)}, label="nucleo_ard")
    dev = _dev("rtc")
    dev.function_refs.append(FunctionRef(prop="int1-gpios", position=7, flags=0, src=None))  # type: ignore[arg-type]
    inst = _inst("logger_1")
    inst.shield.devices.append(dev)
    rig = Rig(name="r", instances=[inst])

    result, diags = collect_gpio_nets(rig, {"logger_1": {"plug": socket}}, {"t": _ctype()})

    assert diags == []
    key = ("soc", "gpioa", 5)
    assert key in result.nets
    assert result.nets[key][0].role == "driver"


def test_collect_gpio_nets_skips_instances_without_a_resolved_socket() -> None:
    """Skip-don't-abort: an instance absent from `sockets` (its mating
    failed) contributes NOTHING here -- never an exception, never a net."""
    dev = _dev("rtc")
    dev.function_refs.append(FunctionRef(prop="int1-gpios", position=7, flags=0, src=None))  # type: ignore[arg-type]
    inst = _inst("orphan")
    inst.shield.devices.append(dev)
    rig = Rig(name="r", instances=[inst])

    result, diags = collect_gpio_nets(rig, {}, {})

    assert result.nets == {}
    assert diags == []


def test_collect_gpio_nets_jumper_deferred_position_needs_a_pin_selection() -> None:
    """A gpio ref through a routing jumper with no `config:` selection is
    a phys-position rejection -- resolved only when the rig pins it."""
    socket = _socket(gpio_map={0: ("gpioa", 0, 0), 1: ("gpioa", 1, 0)})
    jmp = Jumper(name="irq_jmp", label="irq_jmp", domain=[(0, 0), (1, 1)], sheet_label="")
    dev = _dev("wifi")
    dev.function_refs.append(
        FunctionRef(prop="irq-gpios", position=None, flags=0, jumper="irq_jmp", src=None)  # type: ignore[arg-type]
    )
    inst = _inst("wifi_1")
    inst.shield.devices.append(dev)
    inst.shield.jumpers["irq_jmp"] = jmp
    rig = Rig(name="r", instances=[inst])

    result, diags = collect_gpio_nets(rig, {"wifi_1": {"plug": socket}}, {"t": _ctype()})

    assert result.nets == {}
    assert len(diags) == 1
    assert diags[0].code == "phys-position"


def test_collect_gpio_nets_channel_ref_registers_pin_and_channel_claims() -> None:
    socket = _socket(gpio_map={0: ("gpioa", 3, 0)})
    socket.pwm_map[0] = ("tcc0", 1)
    dev = _dev("servo")
    dev.function_refs.append(
        FunctionRef(prop="pwms", position=0, flags=0, function="pwm", period=1000, src=None)  # type: ignore[arg-type]
    )
    inst = _inst("servo_1")
    inst.shield.devices.append(dev)
    rig = Rig(name="r", instances=[inst])

    result, diags = collect_gpio_nets(rig, {"servo_1": {"plug": socket}}, {"t": _ctype()})

    assert diags == []
    assert ("soc", "gpioa", 3) in result.nets  # PIN net
    assert ("chan", "tcc0", 1) in result.nets  # CHANNEL net
    assert result.channels[("servo_1", "servo", "pwms")][:3] == ("pwm", "tcc0", 1)
    assert result.controllers["tcc0"] == "pwm"


def test_collect_gpio_nets_channel_ref_missing_map_entry_is_phys_function() -> None:
    socket = _socket()  # no pwm_map at all
    dev = _dev("servo")
    dev.function_refs.append(
        FunctionRef(prop="pwms", position=0, flags=0, function="pwm", period=0, src=None)  # type: ignore[arg-type]
    )
    inst = _inst("servo_1")
    inst.shield.devices.append(dev)
    rig = Rig(name="r", instances=[inst])

    result, diags = collect_gpio_nets(rig, {"servo_1": {"plug": socket}}, {"t": _ctype()})

    assert result.nets == {}
    assert len(diags) == 1
    assert diags[0].code == "phys-function"
    # The diagnostic must name the real DTS property, "pwm-map" -- never
    # the nonexistent "socket,pwm-map".
    assert "pwm-map" in diags[0].message
    assert "socket,pwm-map" not in diags[0].message


def test_collect_gpio_nets_channel_ref_missing_map_entry_names_the_real_adc_property() -> None:
    """The ADC twin of the case above: the diagnostic names the real DTS
    property, "io-channel-map", never the nonexistent "socket,adc-map"."""
    socket = _socket()  # no adc_map at all
    dev = _dev("sensor")
    dev.function_refs.append(
        FunctionRef(prop="io-channels", position=0, flags=0, function="adc", src=None)  # type: ignore[arg-type]
    )
    inst = _inst("sensor_1")
    inst.shield.devices.append(dev)
    rig = Rig(name="r", instances=[inst])

    result, diags = collect_gpio_nets(rig, {"sensor_1": {"plug": socket}}, {"t": _ctype()})

    assert result.nets == {}
    assert len(diags) == 1
    assert diags[0].code == "phys-function"
    assert "io-channel-map" in diags[0].message
    assert "socket,adc-map" not in diags[0].message


def test_collect_gpio_nets_nonzero_pwm_flags_is_phys_function_on_a_2cell_socket() -> None:
    """A 2-cell socket's PWM emission carries only (position, period) -- no
    cell for flags -- so a nonzero flags value is rejected rather than
    silently dropped (pwm-nonzero-flags). This depends on the socket's own
    pwm_cells count -- pinned to 2 here, the genuinely-nowhere-to-put-it
    case; see the 3-cell twin below for the other half of the pair."""
    socket = _socket(gpio_map={0: ("gpioa", 3, 0)})
    socket.pwm_map[0] = ("tcc0", 0)
    socket.pwm_cells = 2
    dev = _dev("servo")
    dev.function_refs.append(
        FunctionRef(prop="pwms", position=0, flags=1, function="pwm", period=0, src=None)  # type: ignore[arg-type]
    )
    inst = _inst("servo_1")
    inst.shield.devices.append(dev)
    rig = Rig(name="r", instances=[inst])

    result, diags = collect_gpio_nets(rig, {"servo_1": {"plug": socket}}, {"t": _ctype()})

    assert result.nets == {}
    assert len(diags) == 1
    assert diags[0].code == "phys-function"
    assert "PWM flags" in diags[0].message
    assert "socket 's1'" in diags[0].message
    assert "2-cell" in diags[0].message


def test_collect_gpio_nets_nonzero_pwm_flags_is_carried_on_a_3cell_socket() -> None:
    """The other half of the pair: a 3-cell socket has a real cell for
    flags, so the identical nonzero flags value is carried through to
    result.channels, never refused."""
    socket = _socket(gpio_map={0: ("gpioa", 3, 0)})
    socket.pwm_map[0] = ("tcc0", 0)
    socket.pwm_cells = 3
    dev = _dev("servo")
    dev.function_refs.append(
        FunctionRef(prop="pwms", position=0, flags=1, function="pwm", period=20000000, src=None)  # type: ignore[arg-type]
    )
    inst = _inst("servo_1")
    inst.shield.devices.append(dev)
    rig = Rig(name="r", instances=[inst])

    result, diags = collect_gpio_nets(rig, {"servo_1": {"plug": socket}}, {"t": _ctype()})

    assert diags == []
    assert result.channels[("servo_1", "servo", "pwms")] == ("pwm", "tcc0", 0, 20000000, 1, 0)
