# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Allocation ordering. Every allocator (addresses, CS) sorts its scope
members through this ONE function before assigning anything, so a rig
author reordering `instances:` never changes what gets allocated where
-- deterministic, order-independent, pinnable.

`(socket, instance name, device name)`, read straight off the
Instance/Device values already in hand plus the resolved socket the
caller already has -- no Rig needed, which is what makes it a value
function on its own."""

from __future__ import annotations

from ..model import BoardSocket, Device, Instance

#: The stable allocation order: (the sort key's socket component, then
#: instance name, then device name). The socket component is the
#: AUTHORED reference string of `dev`'s OWN slot (`dev.plug` -- never
#: the resolved BoardSocket's label) wherever the instance declared one;
#: only a slot left to inference (`Instance.sockets[slot] is None`)
#: falls back to the resolved label, since it has no authored string to
#: sort by (the same declared-else-resolved shape config-sheet.md's
#: socket column uses).
AllocationKey = tuple[str, str, str]


def allocation_key(inst: Instance, dev: Device, socket: BoardSocket) -> AllocationKey:
    """socket is `dev`'s OWN already-resolved BoardSocket (every caller
    has one in hand from the same scope member, resolved through
    `dev.plug`'s slot); read-only, used only as the None fallback below."""
    # dev.plug is already the real slot name for every bus device (set
    # at parse time from its own bus group's actual plug node); the
    # "plug" fallback below is never live, since both allocators build
    # their scope from bus-kind devices only, and a plain-group device
    # (dev.plug is None) never reaches here.
    slot = dev.plug or "plug"
    ref = inst.sockets.get(slot)
    if ref is None:
        ref = socket.label
    return (ref, inst.name, dev.name)
