# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""expectations.yml: a runtime-harness stub naming what must be observed
on real hardware. Emitted for every accepted rig, but gated by no golden
(test_emitted_corpus.py's own docstring: "expectations.yml is
deliberately excluded -- it is emitted but never gated").

**Reads `solved.wires`, never `rig.wires`** -- same reasoning as
sheet.py's Wires section.
"""

from __future__ import annotations

from ..analyzer import Solved
from ..analyzer.socketmap import for_bus_device
from ..model import Device, Instance, Rig
from .banner import GEN


def _find_instance_device(
    rig: Rig,
    inst_name: str,
    dev_name: str,
) -> tuple[Instance | None, Device | None]:
    """The Instance/Device objects (inst_name, dev_name) name, recovered by
    name since Solved.addr/Solved.cs key by plain strings, never the
    objects themselves. Either may be None when `rig` carries no matching
    content -- this function is also called against a synthetic Solved
    built directly for a test, with no backing rig content at all; every
    ENTRY a real analyzer run actually produces always has a matching
    instance and device, so the fallback is inert on that path."""
    inst = next((i for i in rig.instances if i.name == inst_name), None)
    if inst is None:
        return None, None
    dev = next((d for d in inst.shield.devices if d.name == dev_name), None)
    return inst, dev


def _bus_name(rig: Rig, inst_name: str, dev_name: str, default: str) -> str:
    """The qualified Device.bus name recorded for (inst_name, dev_name).
    Falls back to `default` (the bare kind) when no matching
    Instance/Device is found (see `_find_instance_device`)."""
    _inst, dev = _find_instance_device(rig, inst_name, dev_name)
    if dev is None or dev.bus is None:
        return default
    return dev.bus


def render_expectations(rig: Rig, s: Solved) -> str:
    """expectations.yml's full text. rig/s are read-only; returns a fresh
    string the caller owns."""
    out = [
        f"# {GEN}",
        "# test expectations stub: what a runtime harness must observe",
        f"rig: {rig.name}",
        f"board: {rig.board}",
        "expect:",
    ]
    for (inst_name, dev_name), addr in sorted(s.addr.items()):
        inst, dev = _find_instance_device(rig, inst_name, dev_name)
        socket = (
            for_bus_device(s.sockets, inst, dev) if inst is not None and dev is not None else None
        )
        bus = dev.bus if dev is not None and dev.bus is not None else "i2c"
        socket_label = socket.buses[bus].label if socket is not None else "?"
        out.append(
            f"  - {{instance: {inst_name}, device: {dev_name}, "
            f"bus: {socket_label}, address: {addr:#04x}, "
            "check: probe}"
        )
    for (inst_name, dev_name), (index, _pos) in sorted(s.cs.items()):
        inst, dev = _find_instance_device(rig, inst_name, dev_name)
        socket = (
            for_bus_device(s.sockets, inst, dev) if inst is not None and dev is not None else None
        )
        bus = dev.bus if dev is not None and dev.bus is not None else "spi"
        socket_label = socket.buses[bus].label if socket is not None else "?"
        out.append(
            f"  - {{instance: {inst_name}, device: {dev_name}, "
            f"bus: {socket_label}, cs-index: {index}, "
            "check: probe}"
        )
    for w in s.wires:
        out.append(
            f"  - {{signal: {w.frm.instance_name}.{w.frm.node} -> "
            f"{w.to.instance_name}.{w.to.node}, check: manual}}"
        )
    return "\n".join(out) + "\n"
