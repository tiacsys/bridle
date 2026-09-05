# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Net identity, GPIO/PWM/ADC claims, jumper resolution, and the final net
conflict report, value-shaped throughout.

Net IDENTITY is sharing: `soc_net` resolves a socket position through
the board's own gpio-map down to the actual SoC pin, so two DIFFERENT
sockets whose positions map to the same pin are the SAME net -- a pure
function of (socket, position), directly unit-testable. `role_of` is
the other already-value-shaped contract this module keeps.

`collect_gpio_nets` is the pass: it walks every resolved instance's
device gpio/pwm/adc refs, building the net-claim map plus jumper-resolved
positions and pwm/adc channel resolutions, entirely as a RETURNED value
(`GpioNets`) -- `check_nets` is a SEPARATE, later function: net
collection happens before CS allocation, but net CONFLICT checking
happens after, since CS allocation contributes further claims into the
same net-claim map -- see analyzer/cs.py and analyzer/__init__.py's
composer, which merges the two claim sets before calling check_nets."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import NamedTuple

from ..diag import Diagnostic, SourceRef, error
from ..model import BoardSocket, ConnectorType, Device, FunctionRef, Instance, Jumper, Rig
from .socketmap import Sockets, for_ref

_DRIVER_HINTS = ("int", "irq")

#: fn -> the REAL DTS property a socket would need to author for this
#: function's channel map to resolve, for use in diagnostic text only:
#: "socket,{fn}-map" is NOT a real property name either function is
#: ever spelled with -- pwm-map / io-channel-map are the standard nexus
#: names edtlib.Node.maps() resolves ("pwm"/"io-channel" being the
#: specifier space, stripped of "-map"), matching what board/project.py
#: itself reads.
_MAP_PROP = {"pwm": "pwm-map", "adc": "io-channel-map"}

#: A net's identity: ("soc", controller label, pin) for a position the
#: board's gpio-map actually routes to a real SoC pin (shared
#: across sockets); ("pos", socket path, position) for a per-socket
#: dedicated line the board fragment doesn't route; ("chan", controller
#: label, channel) for a PWM/ADC controller CHANNEL (exclusive use of one
#: timer/adc channel, independent of which pin reaches it).
NetKey = tuple[object, ...]


@dataclass(frozen=True)
class NetClaim:
    instance: Instance
    device: Device | None
    what: str  # "rtc@…: int1-gpios" / "sdhc: CS (copper-fixed)" / pad name
    role: str  # driver | listener | dedicated
    socket: BoardSocket
    position: int
    src: SourceRef | None = None


#: Every net's claims, keyed by NetKey -- composed upward by simple dict
#: merge (`merge_nets`), the same way diagnostic lists compose by
#: concatenation.
Nets = dict[NetKey, list[NetClaim]]


def merge_nets(*nets: Nets) -> Nets:
    """Compose several Nets values into one, preserving claim order within
    each key (earlier collections' claims first) -- the net-claim analogue
    of `deps.union`/list-concatenating diagnostics.

    Returns a FRESH map with fresh lists: neither the input maps nor
    their claim lists are shared with the result -- a caller extending
    the result must never alias into one of the inputs instead."""
    result: Nets = {}
    for n in nets:
        for key, claims in n.items():
            result.setdefault(key, []).extend(claims)
    return result


def role_of(prop_name: str) -> str:
    """Endpoint role, inferred from the property name (a prototype
    stopgap: int*/irq* = device drives; everything else = device
    listens; pads/CS claims are always 'dedicated', never routed
    through this function)."""
    stem = prop_name[:-6] if prop_name.endswith("-gpios") else prop_name
    if any(h in stem for h in _DRIVER_HINTS):
        return "driver"  # device output (interrupt line etc.)
    return "listener"  # MCU-driven towards the device


def soc_net(socket: BoardSocket, position: int) -> NetKey:
    """Net IDENTITY: resolve the socket position through the gpio-map
    down to the actual SoC pin. Two DIFFERENT sockets whose positions
    map to the same SoC pin are the SAME net (e.g. Grove 5/6 -> gpio0
    26). Positions not in the gpio-map (per-socket dedicated lines the
    board fragment doesn't route, e.g. mikroBUS INT) stay socket-local."""
    mapping = socket.gpio_map.get(position)
    if mapping is not None:
        ctrl, pin, _flags = mapping
        return ("soc", ctrl, pin)
    return ("pos", socket.path, position)


class ChannelResolution(NamedTuple):
    """One resolved PWM/ADC channel claim, the value type of
    `GpioNets.channels`/`Solved.channels` (keyed by (instance, device,
    prop)). `fn` is "pwm" or "adc"; `period` is populated only for pwm
    (an ADC io-channel-map row carries no period cell)."""

    fn: str
    ctrl: str
    channel: int
    period: int | None
    flags: int
    position: int


@dataclass
class GpioNets:
    nets: Nets = field(default_factory=dict)
    positions: dict[tuple[str, str, str], int] = field(default_factory=dict)
    jumpers_set: list[tuple[Instance, Jumper, int | None, int]] = field(default_factory=list)
    channels: dict[tuple[str, str, str], ChannelResolution] = field(default_factory=dict)
    controllers: dict[str, str] = field(default_factory=dict)


def collect_gpio_nets(
    rig: Rig,
    sockets: Sockets,
    types: dict[str, ConnectorType],
) -> tuple[GpioNets, list[Diagnostic]]:
    """The gpio/pwm/adc claim-collection pass: every device ref resolves
    through ITS OWN plug's socket (`ref.plug`, PER-REFERENCE granularity)
    into net claims -- a device sitting on one plug's bus may still
    carry a cross-plug reference to another.

    Returns (nets, diagnostics): a fresh claim map the caller owns --
    later passes read it but must never append into its lists."""
    diags: list[Diagnostic] = []
    result = GpioNets()

    def claim(
        key: NetKey,
        socket: BoardSocket,
        position: int,
        inst: Instance,
        device: Device | None,
        what: str,
        role: str,
        src: SourceRef | None,
    ) -> None:
        result.nets.setdefault(key, []).append(
            NetClaim(
                instance=inst,
                device=device,
                what=what,
                role=role,
                socket=socket,
                position=position,
                src=src,
            )
        )

    for inst in rig.instances:
        for dev in inst.shield.devices:
            for ref in dev.function_refs:
                socket = for_ref(sockets, inst, ref)
                if socket is None:
                    continue
                ctype = types[socket.type_name]
                if ref.function == "gpio":
                    _collect_gpio(inst, dev, ref, socket, ctype, result, claim, diags)
                else:
                    _collect_channel(inst, dev, ref, socket, ctype, result, claim, diags)
    return result, diags


def _collect_gpio(
    inst: Instance,
    dev: Device,
    ref: FunctionRef,
    socket: BoardSocket,
    ctype: ConnectorType,
    result: GpioNets,
    claim,
    diags: list[Diagnostic],
) -> None:
    pos = ref.position
    if ref.jumper is not None:
        resolved = _resolve_jumper(inst, dev, ref, ctype, result, diags)
        if resolved is None:
            return
        pos = resolved
        result.positions[(inst.name, dev.name, ref.prop)] = pos
    assert pos is not None
    claim(
        soc_net(socket, pos),
        socket,
        pos,
        inst,
        dev,
        f"{dev.name}: {ref.prop}",
        role_of(ref.prop),
        ref.src,
    )


def _collect_channel(
    inst: Instance,
    dev: Device,
    ref: FunctionRef,
    socket: BoardSocket,
    ctype: ConnectorType,
    result: GpioNets,
    claim,
    diags: list[Diagnostic],
) -> None:
    """PWM/ADC: the same position is reachable as a channel of a
    controller. Register TWO net claims -- the PIN (exclusive: the pin
    can't also be GPIO or another function) and the CHANNEL (exclusive:
    two consumers can't share one timer/adc channel)."""
    fn = ref.function
    # pwm/adc refs always carry a fixed position at parse time (loader/shields.py):
    # jumper deferral is a gpio-only shape.
    assert ref.position is not None
    pos = ref.position
    fmap = socket.pwm_map if fn == "pwm" else socket.adc_map
    resolved = fmap.get(pos)
    if resolved is None:
        diags.append(
            error(
                "phys-function",
                f"'{inst.name}/{dev.name}: {ref.prop}' uses position "
                f"{ctype.posname(pos)} as {fn.upper()}, but socket "
                f"'{socket.label}' offers no {fn} on it (no {_MAP_PROP[fn]} entry)",
                tuple(x for x in (ref.src, socket.src) if x),
            )
        )
        return
    if fn == "pwm" and ref.flags and socket.pwm_cells == 2:
        # CONDITIONAL on the SOCKET's own cell count, never a blanket
        # refusal: a 2-cell socket (lotus's atmel,sam0-tcc-pwm shape)
        # has genuinely nowhere to put a flags value, but a 3-cell one
        # (the common upstream shape) has a real cell for it.
        diags.append(
            error(
                "phys-function",
                f"'{inst.name}/{dev.name}: {ref.prop}' authors PWM flags "
                f"{ref.flags:#x} at position {ctype.posname(pos)}, "
                f"but socket '{socket.label}' is a {socket.pwm_cells}-cell "
                "(channel, period) PWM socket — there is no cell for flags",
                tuple(x for x in (ref.src, socket.src) if x),
            )
        )
        return
    ctrl, channel = resolved
    result.channels[(inst.name, dev.name, ref.prop)] = ChannelResolution(
        fn=fn, ctrl=ctrl, channel=channel, period=ref.period, flags=ref.flags, position=pos
    )
    result.controllers[ctrl] = fn
    label = "PWM" if fn == "pwm" else "ADC"
    # PIN net -- exclusive use of the physical pin
    claim(
        soc_net(socket, pos),
        socket,
        pos,
        inst,
        dev,
        f"{dev.name}: {ref.prop} ({label} pin)",
        "dedicated",
        ref.src,
    )
    # CHANNEL net -- exclusive use of the controller channel
    claim(
        ("chan", ctrl, channel),
        socket,
        pos,
        inst,
        dev,
        f"{dev.name}: {ref.prop} ({label} {ctrl} ch{channel})",
        "dedicated",
        ref.src,
    )


def _resolve_jumper(
    inst: Instance,
    dev: Device,
    ref: FunctionRef,
    ctype: ConnectorType,
    result: GpioNets,
    diags: list[Diagnostic],
) -> int | None:
    """A routing jumper's position must be pinned by the rig (explicit
    config:; non-CS positions are never auto-allocated). Returns the
    resolved index or None (+ diagnostic)."""
    assert ref.jumper is not None  # only called when the caller already checked
    jmp = inst.shield.jumpers[ref.jumper]
    dom = ", ".join(ctype.posname(p) for p in jmp.positions())
    sel = inst.jumpers.get(ref.jumper)
    if sel is None:
        diags.append(
            error(
                "phys-position",
                f"'{inst.name}/{dev.name}: {ref.prop}' routes through jumper "
                f"'{ref.jumper}' whose position must be selected — add "
                f"config: {{ {jmp.label}: <position> }} to the instance "
                f"(domain: {dom})",
                tuple(x for x in (ref.src, jmp.src) if x),
            )
        )
        return None
    # `sel` is the RAW rig-file value (Instance.jumpers is dict[str, object] on
    # purpose): either a position NAME to look up, or a position index given
    # directly. Anything else -- and any index outside the jumper's domain --
    # falls through to the one domain diagnostic below, which is why the
    # isinstance guard joins that condition rather than raising its own.
    pos: object = (
        ctype.positions[sel].index if isinstance(sel, str) and sel in ctype.positions else sel
    )
    if not isinstance(pos, int) or pos not in jmp.positions():
        diags.append(
            error(
                "phys-position",
                f"instance '{inst.name}': jumper '{ref.jumper}' selection '{sel}' is "
                f"not in its position domain ({dom}) — the copper cannot route it",
                tuple(x for x in (inst.jumper_refs.get(ref.jumper), jmp.src) if x),
            )
        )
        return None
    result.jumpers_set.append((inst, jmp, jmp.state_of(pos), pos))
    return pos


def _net_descr(key: NetKey, claims: list[NetClaim], types: dict[str, ConnectorType]) -> str:
    """Describe where a net lives, from its identity key: a controller
    channel (pwm/adc), a single socket position, or a SoC pin shared
    across sockets."""
    if key[0] == "chan":
        return f"{key[1]} channel {key[2]}"
    where = {(c.socket.label, c.position) for c in claims}
    if len(where) == 1:
        c = claims[0]
        return (
            f"position {types[c.socket.type_name].posname(c.position)} of socket '{c.socket.label}'"
        )
    if key[0] == "soc":
        return f"the shared SoC net {key[1]} pin {key[2]}"
    return "a shared net"


def _claim_line(c: NetClaim, types: dict[str, ConnectorType]) -> str:
    pos = types[c.socket.type_name].posname(c.position)
    return f"- {c.instance.name} (socket {c.socket.label}, {pos}): {c.what}"


def _exclusive_verdict(
    key: NetKey, descr: str, claims: list[NetClaim], types: dict[str, ConnectorType]
) -> list[Diagnostic] | None:
    """The exclusive-resource half of one net's verdict: two exclusive
    claims conflict outright; one exclusive claim plus any signal claims
    on the same net is also a conflict, since an exclusive resource
    cannot also carry a shared signal. Returns None when neither applies
    -- the caller then falls through to the driver-count check."""
    dedicated = [c for c in claims if c.role == "dedicated"]
    if len(dedicated) > 1:
        return [_exclusive_conflict(key, descr, dedicated, types)]
    if dedicated and len(claims) > 1:
        others = [c for c in claims if c.role != "dedicated"]
        return [
            error(
                "phys-net",
                f"{descr} is claimed exclusively "
                f"({dedicated[0].instance.name}: {dedicated[0].what}) but is also "
                "claimed as a signal by:\n" + "\n".join(_claim_line(c, types) for c in others),
                tuple(c.src for c in claims if c.src),
            )
        ]
    return None


def _driver_verdict(
    descr: str, claims: list[NetClaim], types: dict[str, ConnectorType]
) -> list[Diagnostic]:
    """The shared-net half of one net's verdict, reached only once the
    exclusive-resource check above found nothing: more than one DRIVER
    on a shared net is a conflict; 1 driver + N listeners, or MCU-driven
    + N listeners, is a net and legal."""
    drivers = [c for c in claims if c.role == "driver"]
    if len(drivers) > 1:
        return [
            error(
                "phys-net",
                f"{len(drivers)} drivers on one net — {descr}:\n"
                + "\n".join(_claim_line(c, types) + " (device output)" for c in drivers)
                + "\nnote: if these outputs are open-drain, wired-AND sharing is "
                "physically legal — drive-type on roles is a pending refinement "
                "(would downgrade this to a warning).",
                tuple(c.src for c in drivers if c.src),
            )
        ]
    return []


def _net_verdict(
    key: NetKey, descr: str, claims: list[NetClaim], types: dict[str, ConnectorType]
) -> list[Diagnostic]:
    """One net's verdict (`check_nets`' own per-key logic, lifted out).
    At most one finding per net -- the driver check never runs once the
    exclusive-resource check already fired, matching `check_nets`' own
    `continue`-per-branch shape."""
    exclusive = _exclusive_verdict(key, descr, claims, types)
    if exclusive is not None:
        return exclusive
    return _driver_verdict(descr, claims, types)


def check_nets(nets: Nets, types: dict[str, ConnectorType]) -> list[Diagnostic]:
    diags: list[Diagnostic] = []
    for key, claims in sorted(nets.items(), key=lambda kv: str(kv[0])):
        descr = _net_descr(key, claims, types)
        diags += _net_verdict(key, descr, claims, types)
    return diags


def _exclusive_conflict(
    key: NetKey, descr: str, claims: list[NetClaim], types: dict[str, ConnectorType]
) -> Diagnostic:
    """Two exclusive claims on one resource. The resource kind (from the
    net key) tailors the code and the fix hint."""
    if key[0] == "chan":
        code, tail = (
            "phys-channel",
            (
                "\ntwo consumers need the same controller channel — it cannot drive "
                "both independently. Use a different socket/channel, or one device."
            ),
        )
    else:
        code, tail = (
            "phys-cs",
            (
                "\ntwo exclusive claims resolve to the same pin — shorted together, "
                "not realizable. If a CS is copper-fixed the pool cannot route around "
                "it: use different sockets, positions, or rework the copper."
            ),
        )
    return error(
        code,
        f"exclusive-resource conflict at {descr}:\n"
        + "\n".join(_claim_line(c, types) for c in claims)
        + tail,
        tuple(c.src for c in claims if c.src),
    )
