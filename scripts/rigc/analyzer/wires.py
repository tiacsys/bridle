# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Wires and emission feasibility of routes. No frozen golden covers
this family (phys-wire) -- every diagnostic here is checked by hand
differential rather than a golden byte comparison.

Value-shaped and non-mutating: a `route: via <name>` string resolves to
its connector-type position INDEX without mutating `wire.route` in
place -- this module returns a NEW list of Wire values with the route
already resolved, so the pass composes like every other one here
(`(its piece, diagnostics)`), never writing into a Rig it was handed."""

from __future__ import annotations

from ..diag import Diagnostic, error
from ..model import ConnectorType, Instance, Rig, Wire
from .socketmap import Sockets, for_slot


def _resolve_via_route(
    wire: Wire,
    route: str,
    by_name: dict[str, Instance],
    sockets: Sockets,
    types: dict[str, ConnectorType],
) -> tuple[str | int, list[Diagnostic]]:
    """The `route: via <position name>` branch of `check_wires`, lifted
    out: resolved to the connector type's own position INDEX, through
    the FROM end's socket. Ambiguous for a plural FROM instance (which
    of its several plugs would the position even be relative to?) --
    refused loudly rather than guessed at. Returns the route UNCHANGED
    (still the raw name) whenever it does not resolve, so the caller
    always builds the same Wire either way, refusal or not."""
    diags: list[Diagnostic] = []
    frm_inst = by_name.get(wire.frm.instance_name)
    if frm_inst is not None and len(frm_inst.shield.plugs) > 1:
        diags.append(
            error(
                "phys-wire",
                f"route 'via {route}': instance '{frm_inst.name}' plugs "
                f"more than one socket -- via-routing is not supported "
                "for a multi-plug instance yet",
                (wire.src,),
            )
        )
        return route, diags
    socket = (
        for_slot(sockets, frm_inst, next(iter(frm_inst.shield.plugs)))
        if frm_inst is not None
        else None
    )
    ctype = types[socket.type_name] if socket is not None else None
    if ctype is not None and route in ctype.positions:
        return ctype.positions[route].index, diags
    diags.append(
        error(
            "phys-wire",
            f"route 'via {route}': no such position on connector type "
            f"'{ctype.name if ctype is not None else '?'}'",
            (wire.src,),
        )
    )
    return route, diags


def check_wires(
    rig: Rig,
    sockets: Sockets,
    types: dict[str, ConnectorType],
) -> tuple[list[Wire], list[Diagnostic]]:
    """The wire pass: endpoints checked against resolved sockets, route
    names resolved to positions.

    Returns (wires, diagnostics): a NEW list of resolved Wire values --
    rig.wires is never mutated, which is why the emitter must read
    solved.wires, never rig.wires (they differ: resolved route vs raw
    via name)."""
    diags: list[Diagnostic] = []
    by_name: dict[str, Instance] = {i.name: i for i in rig.instances}
    resolved: list[Wire] = []

    for wire in rig.wires:
        roles = []
        for end in (wire.frm, wire.to):
            inst = by_name.get(end.instance_name)
            pad = inst.shield.pads.get(end.node) if inst is not None else None
            if pad is None:
                diags.append(
                    error(
                        "phys-wire",
                        f"wire end '{end.instance_name}.{end.node}' is not a pad — "
                        "only pads (arity-1 connectors) are wireable in the prototype",
                        (end.src,),
                    )
                )
                continue
            roles.append((end, pad.role))
        if len(roles) < 2:
            resolved.append(wire)
            continue

        drivers = [e for e, r in roles if r == "driver"]
        if len(drivers) != 1:
            claims = ", ".join(f"{e.instance_name}.{e.node} ({r})" for e, r in roles)
            diags.append(
                error(
                    "phys-wire",
                    f"a net needs exactly one driver and ≥1 listener; "
                    f"wire has {len(drivers)} drivers: {claims}",
                    (wire.src,),
                )
            )

        route = wire.route
        if isinstance(route, str) and route != "adhoc":
            # ad-hoc routes never reach this branch at all.
            route, d = _resolve_via_route(wire, route, by_name, sockets, types)
            diags += d
        resolved.append(Wire(frm=wire.frm, to=wire.to, route=route, src=wire.src))
    return resolved, diags
