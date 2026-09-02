# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""CS pool allocation: where and how the final cs-gpios property is
calculated, split into a value-shaped contract:

  effective_cs_pool     -- the pool-MERGE fallback: a socket's own
                            authored override wins, else the connector
                            type's binding default.
  allocate_cs_positions -- THE algorithm, and the part this module exists
                            to make unit-testable on its own: given an
                            ORDERED pool (as (position, net-identity)
                            pairs -- net identity, not a bare position
                            index, because two DIFFERENT sockets in one
                            SPI scope are compared through the SAME SoC
                            pin), the net identities ALREADY taken,
                            and the scope's members in allocation
                            order (some copper-fixed), assign each a
                            position or report the pool exhausted. No
                            Rig/Instance/Shield/Board needed to call it.
  allocate_cs           -- the PASS: walks rig.instances, groups SPI-bus
                            members into scopes (a mux channel is its own
                            new scope), builds each member's CsMember from
                            its resolved socket + connector type, and
                            folds the placements into cs/cs_gpios plus the
                            NEW net claims (for the composer to merge into
                            the shared net-claim map before the final
                            conflict check, analyzer/gpio.py's
                            `check_nets`)."""

from __future__ import annotations

import logging
from collections.abc import Sequence
from dataclasses import dataclass, field

from ..buskind import is_bus_kind
from ..diag import Diagnostic, error
from ..model import BoardSocket, ConnectorType, Device, Instance, Rig
from .gpio import NetClaim, NetKey, Nets, soc_net
from .ordering import allocation_key
from .socketmap import Sockets, for_bus_device

log = logging.getLogger(__name__)


def effective_cs_pool(bus_cs_pool: list[int] | None, type_default_pool: list[int]) -> list[int]:
    """The cs_pool None-if-absent merge: a real board socket whose
    connector type's binding declares a cs-pool default for this bus
    already has it backfilled by edtlib
    (board/project.py), making this merge inert there -- but a
    shield-SYNTHESIZED socket (carrier/mux composition, analyzer/
    sockets.py's `compose_socket`) comes from a plain dtlib parse with no
    binding-default backfill, so this is very much alive for that path."""
    return bus_cs_pool if bus_cs_pool is not None else type_default_pool


@dataclass(frozen=True)
class CsMember:
    """One SPI-scope member's CS-allocation input, already in
    allocation order by the time the caller builds a list of these:
    `identity` is opaque (used only for reporting which member exhausted
    its pool), `fixed` is (position, net-identity) when copper-fixed
    (`shield,cs-position`), else None and `pool` carries the member's OWN
    ordered (position, net-identity) candidates -- different members in
    one scope may draw from DIFFERENT pools (different sockets), which is
    exactly why the pool travels with the member rather than the call."""

    identity: str
    fixed: tuple[int, object] | None = None
    pool: tuple[tuple[int, object], ...] = ()


@dataclass(frozen=True)
class CsPlacement:
    identity: str
    position: int
    fixed: bool


def allocate_cs_positions(
    members: Sequence[CsMember],
    occupied: frozenset[object],
) -> tuple[list[CsPlacement], list[str]]:
    """The CS-allocation algorithm: given an ordered pool, the
    already-taken net identities, and the members of one SPI scope in
    allocation order (some copper-fixed), assign each a position -- or
    report the pool exhausted. Copper-fixed members win OUTRIGHT (never
    consulted against the pool, never reported exhausted); everything
    else takes the first pool candidate whose net identity is not yet
    taken, checked against BOTH `occupied` and every identity already
    placed earlier IN THIS SAME CALL, so each registration is visible to
    every later member of the scope, fixed or free alike.
    Returns (placements in input order, identities whose pool was
    exhausted)."""
    taken = set(occupied)
    placements: list[CsPlacement] = []
    exhausted: list[str] = []
    for m in members:
        if m.fixed is not None:
            pos, net_key = m.fixed
            placements.append(CsPlacement(m.identity, pos, True))
            taken.add(net_key)
            continue
        choice = next(((p, k) for p, k in m.pool if k not in taken), None)
        if choice is None:
            exhausted.append(m.identity)
            continue
        pos, net_key = choice
        placements.append(CsPlacement(m.identity, pos, False))
        taken.add(net_key)
    return placements, exhausted


def _cs_members_for_scope(
    members: Sequence[tuple[Instance, Device, BoardSocket]],
    types: dict[str, ConnectorType],
) -> tuple[list[CsMember], dict[str, tuple[Instance, Device, BoardSocket]]]:
    """Build one scope's ordered `CsMember` list (allocate_cs's own
    per-scope wiring, lifted out) plus the identity -> (inst, dev,
    socket) lookup every later step needs, from members already in
    allocation order."""
    cs_members: list[CsMember] = []
    by_identity: dict[str, tuple[Instance, Device, BoardSocket]] = {}
    for inst, dev, socket in members:
        ctype = types[socket.type_name]
        identity = f"{inst.name}/{dev.name}"
        by_identity[identity] = (inst, dev, socket)
        if dev.cs_position is not None:
            pos = dev.cs_position
            cs_members.append(CsMember(identity=identity, fixed=(pos, soc_net(socket, pos))))
        else:
            assert dev.bus is not None  # narrowed by the scope-building filter above
            bus = socket.buses[dev.bus]
            pool = effective_cs_pool(bus.cs_pool, ctype.cs_pool.get(dev.bus, []))
            cs_members.append(
                CsMember(identity=identity, pool=tuple((p, soc_net(socket, p)) for p in pool))
            )
    return cs_members, by_identity


def _fold_cs_placements(
    bus_path: str,
    placements: list[CsPlacement],
    exhausted: list[str],
    by_identity: dict[str, tuple[Instance, Device, BoardSocket]],
    types: dict[str, ConnectorType],
    seen: set[NetKey],
    result: CsAllocation,
) -> list[Diagnostic]:
    """The placements/exhausted -> `CsAllocation` translation (allocate_cs's
    own folding step, lifted out): an exhausted member becomes a phys-cs
    diagnostic; a placement becomes a NEW net claim (`seen` grows so a
    LATER scope in this same call sees it) plus this scope's cs/cs_gpios
    entries, in placement order."""
    diags: list[Diagnostic] = []
    for identity in exhausted:
        inst, dev, socket = by_identity[identity]
        ctype = types[socket.type_name]
        assert dev.bus is not None  # narrowed by the scope-building filter above
        bus = socket.buses[dev.bus]
        pool = effective_cs_pool(bus.cs_pool, ctype.cs_pool.get(dev.bus, []))
        diags.append(
            error(
                "phys-cs",
                f"CS pool of socket '{socket.label}' is exhausted for "
                f"'{identity}': candidates "
                f"{', '.join(ctype.posname(p) for p in pool)} are all claimed",
                tuple(x for x in (dev.src, inst.src) if x),
            )
        )

    placed = []
    for placement in placements:
        inst, dev, socket = by_identity[placement.identity]
        ctype = types[socket.type_name]
        what = (
            f"{dev.name}: CS copper-fixed at {ctype.posname(placement.position)} "
            "(shield,cs-position)"
            if placement.fixed
            else f"{dev.name}: CS allocated at {ctype.posname(placement.position)}"
        )
        log.debug(
            "instance '%s': device '%s' allocated CS position %s (%s)",
            inst.name,
            dev.name,
            placement.position,
            "fixed" if placement.fixed else "pool",
        )
        key = soc_net(socket, placement.position)
        claim = NetClaim(
            instance=inst,
            device=dev,
            what=what,
            role="dedicated",
            socket=socket,
            position=placement.position,
            src=dev.src,
        )
        result.nets.setdefault(key, []).append(claim)
        seen.add(key)
        placed.append((inst, dev, socket, placement.position))

    entries: list[tuple[BoardSocket, int]] = []
    for index, (inst, dev, socket, pos) in enumerate(placed):
        result.cs[(inst.name, dev.name)] = (index, pos)
        if socket.gpio_map.get(pos) is None:  # must resolve to a real SoC pin
            ctype = types[socket.type_name]
            diags.append(
                error(
                    "phys-cs",
                    f"socket '{socket.label}' has no gpio-map entry for position "
                    f"{ctype.posname(pos)} — the board fragment "
                    "cannot route this CS",
                    tuple(x for x in (socket.src, dev.src) if x),
                )
            )
            continue
        entries.append((socket, pos))  # emitted through the nexus
    result.cs_gpios[bus_path] = entries
    return diags


@dataclass
class CsAllocation:
    cs: dict[tuple[str, str], tuple[int, int]] = field(
        default_factory=dict
    )  # (inst, dev) -> (index, position)
    cs_gpios: dict[str, list[tuple[BoardSocket, int]]] = field(
        default_factory=dict
    )  # bus path -> [(socket, pos)]
    bus_label: dict[str, str] = field(default_factory=dict)  # bus path -> label
    nets: Nets = field(default_factory=dict)  # NEW claims only


def allocate_cs(
    rig: Rig,
    sockets: Sockets,
    types: dict[str, ConnectorType],
    nets_before: Nets,
) -> tuple[CsAllocation, list[Diagnostic]]:
    diags: list[Diagnostic] = []
    result = CsAllocation()
    scopes: dict[str, list[tuple[Instance, Device, BoardSocket]]] = {}
    for inst in rig.instances:
        for dev in inst.shield.devices:
            if not is_bus_kind(dev.bus, "spi"):
                continue
            socket = for_bus_device(sockets, inst, dev)
            if socket is None or dev.bus not in socket.buses:
                continue
            bus = socket.buses[dev.bus]
            result.bus_label[bus.path] = bus.label
            scopes.setdefault(bus.path, []).append((inst, dev, socket))

    # A running view of CLAIMED NET KEYS (a position claimed while
    # processing one bus scope is visible to the next) -- LOCAL to this
    # one function call, never a cross-module accumulator. Built as a
    # KEY SET, deliberately: copying only the keys out of `nets_before`,
    # never the per-key claim lists, is what guarantees the append below
    # can never mutate a claim list another pass returned.
    seen: set[NetKey] = set(nets_before)

    for bus_path, raw_members in sorted(scopes.items()):
        members = sorted(raw_members, key=lambda m: allocation_key(m[0], m[1], m[2]))
        cs_members, by_identity = _cs_members_for_scope(members, types)

        occupied = frozenset(seen)
        placements, exhausted = allocate_cs_positions(cs_members, occupied)

        diags += _fold_cs_placements(
            bus_path, placements, exhausted, by_identity, types, seen, result
        )

    return result, diags
