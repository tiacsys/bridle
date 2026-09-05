# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""config-sheet.md -- the physical configuration sheet: the ONE place a
symbol's resolved value is shown to a human; emission itself never
resolves anything (overlay.py emits params verbatim), so without this
table a rig-assigned INPUT_KEY_1 would mean nothing to a reader who has
not memorized the header.

**Reads `solved.wires`, never `rig.wires`**: the Wires section is the
one place in this module a wire's raw `Rig` data would silently diverge
from what got resolved -- `solved.wires` carries the route already
resolved to a connector-type position index.

**Slot qualifier rendered only for a plural shield**: a single-plug
instance's Socket-assignment row is a plain socket name; a plural
instance gets one row per slot, its socket cell spelled
`<slot>: <ref-or-label>`.
"""

from __future__ import annotations

from ..analyzer import Solved
from ..analyzer.socketmap import for_bus_device, for_ref, for_slot
from ..dtsio import is_int_literal, resolve_token
from ..model import BoardSocket, ConnectorType, Device, Instance, Rig, Strap
from .banner import GEN


def _socket_display(inst: Instance, s: Solved, slot: str) -> str:
    """The socket name a bench instruction shows for one slot: the
    instance's own declared reference wherever it authored one for that
    slot, else the label inference resolved to -- `for_slot` always
    finds an entry here, since the emitter only ever runs on an accepted
    rig where every slot's socket already resolved. Read-only over its
    arguments; returns a plain str the caller owns."""
    ref = inst.sockets.get(slot)
    if ref is not None:
        return ref
    socket = for_slot(s.sockets, inst, slot)
    return socket.label if socket is not None else "?"


def _strap_owner_slot(inst: Instance, strap: Strap) -> str:
    """The slot the device THIS strap resolves an address for sits on --
    straps are address-domain and bus-scoped, unaffected by plurality,
    but still need a slot to display a socket cell for. Falls back to
    `inst`'s shield's own one slot name when no device of `inst`'s
    shield actually names this strap, which never happens for an
    accepted rig but keeps this total."""
    dev = next((d for d in inst.shield.devices if d.addr_from == strap.name), None)
    if dev is not None and dev.plug is not None:
        return dev.plug
    return next(iter(inst.shield.plugs), "plug")


def _find_instance(rig: Rig, name: str) -> Instance | None:
    return next((i for i in rig.instances if i.name == name), None)


def _find_device(inst: Instance, name: str) -> Device | None:
    return next((d for d in inst.shield.devices if d.name == name), None)


def _device_socket(
    rig: Rig,
    s: Solved,
    inst_name: str,
    dev_name: str,
) -> BoardSocket | None:
    """The resolved socket `dev_name`'s own bus binds to, recovered by
    name since `Solved.cs` keys by plain strings, never the Device
    object itself -- the same recovery `emitter/expectations.py`'s
    `_bus_name` performs, routed through the ONE accessor
    (analyzer/socketmap.py)."""
    inst = _find_instance(rig, inst_name)
    dev = _find_device(inst, dev_name) if inst is not None else None
    if inst is None or dev is None:
        return None
    return for_bus_device(s.sockets, inst, dev)


def _ref_socket(
    rig: Rig,
    s: Solved,
    inst_name: str,
    dev_name: str,
    prop: str,
) -> BoardSocket | None:
    """The resolved socket the `prop` gpio/pwm/adc ref of `dev_name`
    claims through -- per-reference granularity, so a cross-plug ref's
    own slot is what this recovers, never the device's bus slot."""
    inst = _find_instance(rig, inst_name)
    dev = _find_device(inst, dev_name) if inst is not None else None
    if inst is None or dev is None:
        return None
    ref = next((r for r in dev.function_refs if r.prop == prop), None)
    if ref is None:
        return None
    return for_ref(s.sockets, inst, ref)


def _socket_table(rig: Rig, s: Solved) -> list[str]:
    """The Socket assignment table: one row per single-plug instance, one
    row per slot for a plural instance. rig/s are read-only; returns fresh
    lines the caller owns."""
    out = ["## Socket assignment", "", "| instance | shield | socket |", "|---|---|---|"]
    for inst in sorted(rig.instances, key=lambda i: i.name):
        if len(inst.shield.plugs) <= 1:
            slot = next(iter(inst.shield.plugs), "plug")
            out.append(f"| {inst.name} | {inst.shield.name} | {_socket_display(inst, s, slot)} |")
        else:
            for slot in inst.shield.plugs:
                out.append(
                    f"| {inst.name} | {inst.shield.name} | "
                    f"{slot}: {_socket_display(inst, s, slot)} |"
                )
    return out


def _straps_section(rig: Rig, s: Solved, types: dict[str, ConnectorType]) -> list[str]:
    """The Straps / jumpers section: one bullet per resolved strap, then one
    per set routing jumper. rig/s/types are read-only; returns fresh lines
    the caller owns, empty when there is nothing to report."""
    if not (s.straps or s.jumpers_set):
        return []
    out = ["", "## Straps / jumpers", ""]
    for inst, strap, state, addr in sorted(s.straps, key=lambda t: (t[0].name, t[1].name)):
        sheet = strap.sheet_label or strap.name
        slot = _strap_owner_slot(inst, strap)
        out.append(
            f"- **{inst.name}** ({_socket_display(inst, s, slot)}): set **{sheet}** to state "
            f"{state} → device address {addr:#04x}"
        )
    for inst, jmp, jmp_state, pos in sorted(s.jumpers_set, key=lambda t: (t[0].name, t[1].name)):
        # Routing jumpers are refused outright on a plural shield --
        # inst.shield.plugs always has exactly one entry here, whatever
        # its plug node is actually named.
        sheet = jmp.sheet_label or jmp.name
        slot = next(iter(inst.shield.plugs), "plug")
        socket = for_slot(s.sockets, inst, slot)
        assert socket is not None
        posname = types[socket.type_name].posname(pos)
        out.append(
            f"- **{inst.name}** ({_socket_display(inst, s, slot)}): set **{sheet}** to state "
            f"{jmp_state} → routed to pin {posname}"
        )
    return out


def _channels_section(rig: Rig, s: Solved, types: dict[str, ConnectorType]) -> list[str]:
    """The PWM / analog pin-mux section: one bullet per resolved channel
    claim. rig/s/types are read-only; returns fresh lines the caller owns,
    empty when there are no channels."""
    if not s.channels:
        return []
    out = [
        "",
        "## PWM / analog pin-mux (board-provided pinctrl)",
        "",
        "rigc enables these controllers; the SoC pin-mux for "
        "each pin is board-provided and must be applied (stubbed):",
        "",
    ]
    # keys are (instance NAME, device NAME, prop) strings, unlike the
    # Instance/Strap/Jumper OBJECTS the straps/jumpers loops above bind
    # -- named distinctly (inst_name/dev_name) so the two shapes never
    # share a variable name of two different types.
    for (inst_name, dev_name, prop), res in sorted(s.channels.items()):
        socket = _ref_socket(rig, s, inst_name, dev_name, prop)
        assert socket is not None
        posname = types[socket.type_name].posname(res.position)
        out.append(
            f"- {inst_name}/{dev_name} ({socket.label} {posname}) → "
            f"{res.fn.upper()} {res.ctrl} ch{res.channel}: mux the pin to the controller"
        )
    return out


def _wires_section(s: Solved) -> list[str]:
    """The Wires section: one bullet per resolved wire, reading only
    `s.wires` (never `rig.wires`, see the module docstring). s is
    read-only; returns fresh lines the caller owns, empty when there are
    no wires."""
    if not s.wires:
        return []
    out = ["", "## Wires", ""]
    for w in s.wires:
        route = (
            "ad-hoc jumper wire (in no connector)"
            if w.route == "adhoc"
            else f"via header position {w.route}"
        )
        out.append(
            f"- connect **{w.frm.instance_name}.{w.frm.node}** → "
            f"**{w.to.instance_name}.{w.to.node}** — {route}"
        )
    return out


def _cs_section(rig: Rig, s: Solved, types: dict[str, ConnectorType]) -> list[str]:
    """The Chip-selects section: one bullet per resolved CS index. rig/s/
    types are read-only; returns fresh lines the caller owns, empty when
    there are no chip-selects."""
    if not s.cs:
        return []
    out = ["", "## Chip-selects", ""]
    for (inst_name, dev_name), (index, pos) in sorted(s.cs.items()):
        socket = _device_socket(rig, s, inst_name, dev_name)
        assert socket is not None
        posname = types[socket.type_name].posname(pos)
        mapping = socket.gpio_map.get(pos)
        soc = f" → SoC {mapping[0]} pin {mapping[1]}" if mapping else ""
        out.append(f"- {inst_name}/{dev_name}: CS index {index}, {posname}{soc}")
    return out


def render_sheet(
    rig: Rig,
    s: Solved,
    types: dict[str, ConnectorType],
    workdir: str,
    include_dirs: list[str] | None = None,
) -> str:
    """config-sheet.md's full text. rig/s/types are read-only; returns a
    fresh string the caller owns. workdir/include_dirs feed the params
    table's own token resolution (a synthetic cpp/dtlib TU, the same
    mechanism the loader's own per-instance-parameter resolution uses --
    see dtsio.resolve_token)."""
    out = [
        f"# Physical configuration sheet — rig `{rig.name}`",
        "",
        f"<!-- {GEN} -->",
        "",
        f"Board: **{rig.board}**",
        "",
    ]
    out += _socket_table(rig, s)
    out += _straps_section(rig, s, types)
    out += _channels_section(rig, s, types)
    out += _wires_section(s)
    out += _cs_section(rig, s, types)
    out += _params_table(rig, workdir, include_dirs)
    return "\n".join(out) + "\n"


def _params_table(rig: Rig, workdir: str, include_dirs: list[str] | None = None) -> list[str]:
    """Per-instance parameter assignments: the ONE place a symbol's
    resolved value is shown to a human -- emission itself never resolves
    anything, so without this table a rig-assigned INPUT_KEY_1 would
    mean nothing to a reader who has not memorized the header. Empty (no
    section at all) for every rig that assigns none.

    Each row resolves against its OWN device's declared_param_includes --
    the vocabulary is the owning shield device's, never a rig-wide list,
    so two rows on different devices may resolve against entirely
    different headers."""
    rows = []
    for inst in sorted(rig.instances, key=lambda i: i.name):
        devices_by_label = {d.label: d for d in inst.shield.devices}
        for dev_label, props in sorted(inst.params.items()):
            for prop, value in sorted(props.items()):
                display = value
                if not is_int_literal(value):
                    dev = devices_by_label.get(dev_label)
                    headers = dev.declared_param_includes if dev is not None else []
                    tag = f"sheet_{inst.name}_{dev_label}_{prop}"
                    resolved = resolve_token(value, headers, workdir, tag, include_dirs)
                    if resolved is not None:
                        display = f"{value} ({resolved})"
                rows.append((inst.name, dev_label, prop, display))
    if not rows:
        return []
    out = ["", "## Parameters", "", "| instance | device | property | value |", "|---|---|---|---|"]
    for inst_name, dev_label, prop, display in rows:
        out.append(f"| {inst_name} | {dev_label} | {prop} | {display} |")
    return out
