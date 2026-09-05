# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""The ONE seam every pass and emitter module resolves "the socket a
reference/device targets" through: a resolution is keyed per SLOT
rather than per instance, so `SocketResolution.sockets`/`Solved.sockets`
is `Sockets` below (instance name -> slot name -> socket), never a bare
`Dict[str, BoardSocket]`.

Three functions, matching the two granularities a claim can name a
socket at -- PER-REFERENCE (a gpio/pwm/adc claim names its own plug by
phandle) and PER-BUS-GROUP (a device's bus binds to exactly one plug) --
plus the slot-enumeration helper the per-slot renderers (sheet.py) need.
This is the `buskind.py` precedent one level up: one shared
implementation so a caller gating behavior on "which slot does this
belong to" cannot drift into three copies of the same lookup, instead of
a bare per-instance dict lookup of this map's own two levels appearing
anywhere else in analyzer or emitter code.

Every function here is read-only over its arguments and returns a
reference into the resolution map it was handed, never a copy -- the
returned `BoardSocket` is owned by whichever pass built the map
(analyzer/sockets.py's `resolve_sockets`), never by the caller."""

from __future__ import annotations

from ..model import BoardSocket, Device, FunctionRef, Instance

#: instance name -> slot name -> resolved board socket. A slot absent
#: from the inner map never resolved (skip-don't-abort, exactly as a
#: missing instance entry did before plurality) -- the analyzer already
#: reported why, and every reader here treats absence as None rather
#: than a KeyError.
Sockets = dict[str, dict[str, BoardSocket]]


def slots_of(sockets: Sockets, inst: Instance) -> list[str]:
    """Every slot of `inst` that resolved to a physical socket, in the
    shield's own plug authoring order (`Shield.plugs`' own dict order) --
    a slot missing from the result never resolved. Used by the per-slot
    renderers (emitter/sheet.py) to enumerate what to display; never by
    an analyzer pass, which reaches a socket through `for_ref`/
    `for_bus_device` instead. `sockets`/`inst` are read-only; returns a
    fresh list the caller owns."""
    resolved = sockets.get(inst.name, {})
    return [slot for slot in inst.shield.plugs if slot in resolved]


def for_ref(sockets: Sockets, inst: Instance, ref: FunctionRef) -> BoardSocket | None:
    """The resolved `BoardSocket` `ref` claims through -- keyed by
    `ref.plug`, the slot the reference's own phandle named
    (`loader/shields.py`'s `_parse_pos_ref`), NEVER the device's own bus slot: a
    cross-plug reference can name a plug other than the one its
    device's bus binds to. Returns
    None when that slot of this instance never resolved (the analyzer
    already reported why -- the caller's own skip-don't-abort guard, not
    an error here). `sockets`/`inst`/`ref` are read-only."""
    return sockets.get(inst.name, {}).get(ref.plug)


def for_bus_device(sockets: Sockets, inst: Instance, dev: Device) -> BoardSocket | None:
    """The resolved `BoardSocket` `dev`'s own BUS binds to -- keyed by
    `dev.plug`, the slot its bus group nests under. Calling this on a
    plain-group device (`dev.plug` is None, since it has no bus of its
    own to bind) is a caller bug; every caller already filters to
    bus-kind devices before reaching here (analyzer/cs.py, analyzer/
    addresses.py, emitter/overlay.py's `_bus_devices`). Returns None when
    that slot never resolved. `sockets`/`inst`/`dev` are read-only."""
    assert dev.plug is not None, (
        f"for_bus_device called on plain-group device '{dev.name}' "
        "(no bus, no plug slot to look up)"
    )
    return sockets.get(inst.name, {}).get(dev.plug)


def for_slot(sockets: Sockets, inst: Instance, slot: str) -> BoardSocket | None:
    """The resolved `BoardSocket` of `inst`'s own named `slot`, directly --
    the primitive `for_ref`/`for_bus_device` both delegate to, and the one
    a caller reaches for when neither a `FunctionRef` nor a `Device` is in
    hand (analyzer/wires.py's pad-based routes, which resolve through a
    single-plug instance's own one slot after checking plurality itself --
    a plural FROM instance is refused before this is ever called).
    Returns None when that slot never resolved. `sockets`/`inst` are
    read-only."""
    return sockets.get(inst.name, {}).get(slot)
