# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Mating and socket resolution, with carrier/mux composition,
value-shaped throughout: `resolve_sockets` returns the instance->slot->
BoardSocket map plus every mux-channel scope entry composition creates,
alongside its diagnostics -- no mutable accumulator, no `diags` side
channel.

Two pieces are pulled out as PURE value functions on their own:

  mating_ok / subset_gaps  -- plug-type-vs-socket-type and needed-vs-offered
                              bus decisions, each a one-line predicate over
                              plain strings/sets.
  compose_socket           -- (parent socket, exposure) -> synthesized
                              socket + scope entries, over PLAIN
                              ExposedSocket/BoardSocket values -- no
                              Instance/Rig/Shield needed to call it.

`resolve_sockets` is the pass: it walks `rig.instances`, recursing through
carrier chains (stack-guarded against cycles, memoizing into the returned
map as it goes), and folds in the stackability check once every instance's
socket is known. Skip-don't-abort is structural here: an instance whose
socket never resolves is simply absent from the returned map, and every
later pass already skips a missing entry rather than aborting.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field

from ..buskind import bus_kind_of, is_bus_kind
from ..diag import Diagnostic, SourceRef, error
from ..model import Board, BoardSocket, BusRef, ConnectorType, ExposedSocket, Instance, Rig

log = logging.getLogger(__name__)

#: One mux-channel scope this rig's composition created: scope PATH (the
#: composing instance's own socket reference string) -> (mux root label,
#: channel index).
ScopeEntry = tuple[str, tuple[str, int]]


@dataclass
class SocketResolution:
    # instance name -> slot name -> resolved socket: a slot absent from
    # the inner map never resolved. A shield with one plug has one
    # entry, keyed by that plug's name. Consumed ONLY through
    # analyzer/socketmap.py's accessor family -- this pass, and this
    # module's own `resolve_sockets`, are the sole exception (they
    # BUILD the map).
    sockets: dict[str, dict[str, BoardSocket]] = field(default_factory=dict)
    scopes: dict[str, tuple[str, int]] = field(default_factory=dict)


def mating_ok(plug_type: str, socket_type: str) -> bool:
    """A shield's plug type must equal the socket's own connector
    type -- the mating decision as a pure value function."""
    return plug_type == socket_type


def subset_gaps(needed: set[str], offered: Iterable[str]) -> list[str]:
    """Which of the buses a shield's devices actually use are NOT
    among the buses the socket exposes -- subset exposure is declared by
    ABSENCE (a socket offering no socket,uart rejects a uart-needing plug).
    Sorted so a caller renders a stable, deterministic list."""
    return sorted(needed - set(offered))


def _compose_buses(
    socket_label: str,
    carrier_name: str,
    exposed: ExposedSocket,
    parents: dict[str, BoardSocket],
    inst_src: SourceRef | None,
    is_plural: bool,
) -> tuple[dict[str, BusRef], list[Diagnostic], list[ScopeEntry]]:
    """The bus half of `compose_socket`'s composition, lifted out: a
    pass-through bus resolves through the named parent's controller of
    the same KIND, never an exact-name match; a scope-creating bus
    synthesizes a new `BusRef` rooted at this carrier instance and
    records the scope entry the caller must fold into the pass's own
    scope map. Pure over its arguments, exactly like `compose_socket`
    itself."""
    diags: list[Diagnostic] = []
    scope_entries: list[ScopeEntry] = []
    buses: dict[str, BusRef] = {}
    for kind, marker in exposed.buses.items():
        if marker[0] == "plug":  # pass-through
            slot = marker[1]
            parent = parents[slot]
            kind_query = bus_kind_of(kind) or kind
            candidates = sorted(b for b in parent.buses if is_bus_kind(b, kind_query))
            slot_note = f" (slot '{slot}')" if is_plural else ""
            refs = tuple(x for x in (exposed.src, parent.src, inst_src) if x)
            if len(candidates) > 1:
                diags.append(
                    error(
                        "phys-ambiguous-bus",
                        f"carrier '{carrier_name}' passes {kind.upper()} through socket "
                        f"'{exposed.name}' from parent socket '{parent.label}'{slot_note}, "
                        f"which offers more than one {kind_query.upper()} bus "
                        f"({', '.join(candidates)}) -- ambiguous pass-through is not "
                        "supported yet",
                        refs,
                    )
                )
            elif len(candidates) == 1:
                parent_bus = parent.buses[candidates[0]]
                buses[kind] = BusRef(
                    label=parent_bus.label, path=parent_bus.path, cs_pool=exposed.cs_pool.get(kind)
                )
            else:
                diags.append(
                    error(
                        "phys-subset",
                        f"carrier '{carrier_name}' passes {kind.upper()} through socket "
                        f"'{exposed.name}', but its parent socket '{parent.label}'{slot_note} "
                        f"offers no socket,{kind} (pass-through needs the parent to provide it)",
                        refs,
                    )
                )
        else:  # new scope: ("scope", dev-label)
            # A scope-creating exposed socket carries a shield,channel --
            # it is what selects which downstream bus this composition
            # creates -- so it is never None once this branch is reached.
            assert exposed.channel is not None
            root = f"{carrier_name}_{marker[1]}"
            scope_path = socket_label  # per (carrier, channel); shared by co-plugged modules
            buses[kind] = BusRef(label=f"{root}_ch{exposed.channel}", path=scope_path)
            scope_entries.append((scope_path, (root, exposed.channel)))
    return buses, diags, scope_entries


def compose_socket(
    socket_label: str,
    carrier_name: str,
    exposed: ExposedSocket,
    parents: dict[str, BoardSocket],
    inst_src: SourceRef | None,
) -> tuple[BoardSocket, list[Diagnostic], list[ScopeEntry]]:
    """Pass-through composition over one or more named parents: exposed
    positions resolve to the NAMED parent's SoC pins, exposed buses to
    the named parent's controllers -- each gpio-map row and each
    pass-through bus carries its OWN slot, so a mixed-parent exposed
    socket routes different rows/buses through different parents. Pure
    over its arguments -- no Instance/Rig/Shield needed, only the
    exposure and the ALREADY-resolved parents (every one of the
    carrier's slots; the caller -- `resolve_one` -- guarantees this
    before ever calling in) -- so this is directly unit-testable
    against synthetic ExposedSocket/BoardSocket values. `parents` has
    exactly one entry, keyed by that slot's own name, for a single-plug
    carrier.

    A pass-through selects the named parent's bus of the same KIND, never
    an exact-name match -- the child-side qualified name (validated at
    parse time against the exposed type's own vocabulary) is independent
    of whatever the parent happens to call its own bus. A parent
    offering MORE than one bus of that kind is a loud, not-yet-supported
    ambiguity (phys-ambiguous-bus) rather than a guess.

    Returns (socket, diagnostics, scopes): a NEW synthesized
    BoardSocket, the findings, and any scope entries the composition
    created. Its inputs are read-only; the caller owns all three."""
    diags: list[Diagnostic] = []
    scope_entries: list[ScopeEntry] = []
    is_plural = len(parents) > 1

    gpio_map: dict[int, tuple[str, int, int]] = {}
    nexus_rows: list[tuple[int, str, int]] = []
    for pos, (slot, parent_pos, _flags) in exposed.gpio_map.items():
        parent = parents[slot]
        nexus_rows.append((pos, parent.nexus_label or parent.label, parent_pos))
        if parent_pos in parent.gpio_map:
            gpio_map[pos] = parent.gpio_map[parent_pos]
        # else: parent fragment doesn't route it -> stays socket-local (net key)

    pwm_map, pwm_nexus_rows, pwm_cells, d = _compose_channel_map(
        "pwm",
        exposed.pwm_map,
        exposed.pwm_cells,
        carrier_name,
        exposed,
        parents,
        inst_src,
        is_plural,
    )
    diags += d
    adc_map, adc_nexus_rows, adc_cells, d = _compose_channel_map(
        "adc",
        exposed.adc_map,
        exposed.adc_cells,
        carrier_name,
        exposed,
        parents,
        inst_src,
        is_plural,
    )
    diags += d

    buses, d, bus_scope_entries = _compose_buses(
        socket_label, carrier_name, exposed, parents, inst_src, is_plural
    )
    diags += d
    scope_entries += bus_scope_entries

    # Single-parent composition anchors the composed path to that one
    # parent's own path plus the exposed node's name -- golden-frozen
    # for every existing single-plug shield. A multi-parent composition
    # has no single parent path to anchor to, so it uses the
    # socket_label instead -- the <carrier>.<exposed> reference string,
    # unique per carrier instance and deterministic.
    if len(parents) == 1:
        (only_parent,) = parents.values()
        path = f"{only_parent.path}/{exposed.name}"
    else:
        path = socket_label

    socket = BoardSocket(
        label=socket_label,
        path=path,
        type_name=exposed.type_name,
        gpio_map=gpio_map,
        buses=buses,
        pwm_map=pwm_map,
        pwm_cells=pwm_cells,
        adc_map=adc_map,
        adc_cells=adc_cells,
        src=exposed.src,
        nexus_label=f"{carrier_name}_{exposed.name}",
        nexus_rows=nexus_rows,
        pwm_nexus_rows=pwm_nexus_rows,
        adc_nexus_rows=adc_nexus_rows,
        parents=dict(parents),
    )
    return socket, diags, scope_entries


def _require_matching_cells(
    fn: str,
    prop: str,
    exposed_map: dict[int, tuple[str, int, int]],
    declared_cells: int | None,
    carrier_name: str,
    exposed: ExposedSocket,
    parents: dict[str, BoardSocket],
    inst_src: SourceRef | None,
    is_plural: bool,
    parent_cells_of: Callable[[BoardSocket], int | None],
) -> tuple[set[str], list[Diagnostic]]:
    """The require-and-check rule (see `_compose_channel_map`'s own
    docstring), lifted out: each distinct slot a row draws from must
    declare the same #<prop>-cells as the carrier itself, checked ONCE
    per slot (not once per row, so a plural carrier passing several
    positions through one mismatched slot gets one finding, not N
    duplicates). Returns the refused ("bad") slots plus the diagnostics
    naming both counts and both sides."""
    diags: list[Diagnostic] = []
    bad_slots: set[str] = set()
    for slot in sorted({slot for slot, _pp, _f in exposed_map.values()}):
        parent = parents[slot]
        parent_cells = parent_cells_of(parent)
        if parent_cells == declared_cells:
            continue
        bad_slots.add(slot)
        slot_note = f" (slot '{slot}')" if is_plural else ""
        refs = tuple(x for x in (exposed.src, parent.src, inst_src) if x)
        diags.append(
            error(
                "phys-subset",
                f"carrier '{carrier_name}' declares #{prop}-cells = <{declared_cells}> "
                f"on exposed socket '{exposed.name}', but its parent socket "
                f"'{parent.label}'{slot_note} declares #{prop}-cells = "
                f"<{parent_cells}> -- a carrier does not get to choose its own "
                "cell count, it inherits whatever the board it lands on declares",
                refs,
            )
        )
    return bad_slots, diags


def _compose_channel_map(
    fn: str,
    exposed_map: dict[int, tuple[str, int, int]],
    declared_cells: int | None,
    carrier_name: str,
    exposed: ExposedSocket,
    parents: dict[str, BoardSocket],
    inst_src: SourceRef | None,
    is_plural: bool,
) -> tuple[dict[int, tuple[str, int]], list[tuple[int, str, int]], int | None, list[Diagnostic]]:
    """The pwm/adc twin of `compose_socket`'s own gpio_map loop above,
    factored out because PWM and ADC need IDENTICAL treatment -- a
    branch handling one function while leaving a silent hole for the
    other is exactly the divergence this factoring rules out -- at BOTH
    of the places gpio and pwm/adc genuinely differ:

      A row whose parent does not route it is an ERROR here, never
      gpio_map's own "stays socket-local" silent drop: an unrouted
      analog position is not a meaningful net, it is a mistake.

      The carrier's own declared cell count (`declared_cells`,
      ExposedSocket.pwm_cells/.adc_cells) must equal the resolved
      parent's (BoardSocket.pwm_cells/.adc_cells) or the whole slot is
      refused up front, naming BOTH counts and BOTH sides (the
      carrier's shield name and the parent socket's own label) --
      checked ONCE per distinct slot a row actually draws from, not once
      per row, so a plural carrier passing several positions through one
      mismatched slot gets one finding, not N duplicates.

    `fn` is "pwm" or "adc"; `exposed_map`/`declared_cells` are that
    function's own ExposedSocket fields. Returns (composed map, nexus
    rows, this socket's OWN carried cell count, diagnostics) -- the cell
    count is None whenever nothing actually composed (mirrors nexus_rows
    being empty in the same case: a socket with no resolved rows for a
    function has no nexus to synthesize for it either)."""
    diags: list[Diagnostic] = []
    if not exposed_map:
        return {}, [], None, diags

    prop = "pwm" if fn == "pwm" else "io-channel"
    parent_map_of = (lambda p: p.pwm_map) if fn == "pwm" else (lambda p: p.adc_map)
    parent_cells_of = (lambda p: p.pwm_cells) if fn == "pwm" else (lambda p: p.adc_cells)

    bad_slots, d = _require_matching_cells(
        fn,
        prop,
        exposed_map,
        declared_cells,
        carrier_name,
        exposed,
        parents,
        inst_src,
        is_plural,
        parent_cells_of,
    )
    diags += d

    composed: dict[int, tuple[str, int]] = {}
    nexus_rows: list[tuple[int, str, int]] = []
    for pos, (slot, parent_pos, _filler) in exposed_map.items():
        if slot in bad_slots:
            continue
        parent = parents[slot]
        parent_map = parent_map_of(parent)
        if parent_pos not in parent_map:
            slot_note = f" (slot '{slot}')" if is_plural else ""
            refs = tuple(x for x in (exposed.src, parent.src, inst_src) if x)
            diags.append(
                error(
                    "phys-subset",
                    f"carrier '{carrier_name}' passes {fn.upper()} through socket "
                    f"'{exposed.name}' at position {pos}, but its parent socket "
                    f"'{parent.label}'{slot_note} does not route it there (no "
                    f"{prop}-map entry at parent position {parent_pos})",
                    refs,
                )
            )
            continue
        composed[pos] = parent_map[parent_pos]
        nexus_rows.append((pos, parent.nexus_label or parent.label, parent_pos))

    cells = declared_cells if composed else None
    return composed, nexus_rows, cells, diags


def _subject(inst: Instance, slot: str) -> str:
    """The diagnostic subject phrase for one (instance, slot): bare
    `instance '<name>'` for a single-slot shield, golden-frozen
    byte-for-byte since a single-slot shield has nothing to
    disambiguate; slot-qualified for a plural one. Pure: builds a
    string from its two arguments alone."""
    if len(inst.shield.plugs) > 1:
        return f"instance '{inst.name}': slot '{slot}'"
    return f"instance '{inst.name}'"


@dataclass
class _ResolveState:
    """The mutable working state one `resolve_sockets` call threads
    through its recursion: the board and instance-by-name lookup every
    call needs, the diagnostics collected so far, and the socket/scope
    maps being built (memoized as resolution proceeds, so a socket
    resolved once is never resolved twice). NOT this pass's own
    returned value -- `resolve_sockets` assembles a fresh
    `SocketResolution` from `sockets`/`scopes` once resolution is
    complete, so no caller ever sees this state directly."""

    board: Board
    by_name: dict[str, Instance]
    diags: list[Diagnostic] = field(default_factory=list)
    sockets: dict[str, dict[str, BoardSocket]] = field(default_factory=dict)
    scopes: dict[str, tuple[str, int]] = field(default_factory=dict)


def _infer_socket(
    state: _ResolveState, inst: Instance, slot: str, plug_type: str
) -> BoardSocket | None:
    """Socket inference, per slot: `mating_ok` run in REVERSE across
    every board socket for THIS slot's own connector type, keeping the
    candidates instead of a boolean -- board sockets only, never a
    carrier's own exported ones (those come from instances, so the
    candidate set would change as instances are parsed, making
    inference order-dependent). Exactly one candidate resolves
    silently; zero or two-or-more is always an error, never a guess --
    an implementation that picks between several reasonable candidates
    is wrong however sensible its tie-break looks. No bipartite
    matching between slots either: two same-type slots on a
    two-candidate board both refuse independently -- the explicit
    `sockets:` map is the answer, not a tie-break of this function's
    own."""
    board = state.board
    subject = _subject(inst, slot)
    candidates = [s for s in board.sockets.values() if mating_ok(plug_type, s.type_name)]
    if not candidates:
        state.diags.append(
            error(
                "phys-socket",
                f"{subject}: shield '{inst.shield.name}' plugs "
                f"'{plug_type}', but no socket of board "
                f"'{board.name}' offers a matching type -- add an explicit "
                "socket: to a socket of a different type, or use a "
                "different board\n"
                f"sockets of {board.name}: "
                + ", ".join(f"{s.label} ({s.type_name})" for s in board.sockets.values()),
                (inst.src,) if inst.src else (),
            )
        )
        return None
    if len(candidates) > 1:
        state.diags.append(
            error(
                "phys-socket",
                f"{subject}: shield '{inst.shield.name}' plugs "
                f"'{plug_type}', which mates more than one socket "
                f"of board '{board.name}' -- add an explicit socket: to "
                "pick one\n"
                "candidates: " + ", ".join(s.label for s in candidates),
                (inst.src,) if inst.src else (),
            )
        )
        return None
    return candidates[0]


def _resolve_carrier_socket(
    state: _ResolveState,
    inst: Instance,
    subject: str,
    ref: str,
    stack: tuple[str, ...],
) -> BoardSocket | None:
    """The carrier-exported-socket branch of `_resolve_one`
    ("<carrier instance>.<exposed socket>"): a carrier's exposed socket
    may draw from ANY of its own plugs -- resolve EVERY slot the
    carrier declares before composing, regardless of which ones the
    NAMED exposed socket actually uses; any slot failing to resolve
    fails the whole composition (skip-don't-abort)."""
    carrier_name, _, exp_name = ref.partition(".")
    if inst.name in stack or carrier_name in stack:
        state.diags.append(
            error(
                "phys-socket",
                f"{subject}: socket nesting is cyclic ({ref})",
                (inst.src,) if inst.src else (),
            )
        )
        return None
    carrier = state.by_name.get(carrier_name)
    if carrier is None:
        state.diags.append(
            error(
                "phys-socket",
                f"{subject}: socket '{ref}' names no instance "
                f"'{carrier_name}' in this rig\n"
                f"instances: {', '.join(sorted(state.by_name))}",
                (inst.src,) if inst.src else (),
            )
        )
        return None
    parents: dict[str, BoardSocket] = {}
    for carrier_slot in carrier.shield.plugs:
        parent = _resolve_one(state, carrier, carrier_slot, stack + (inst.name,))
        if parent is None:
            return None
        parents[carrier_slot] = parent
    # resolved by the exposed node's DTS LABEL -- the same naming
    # authority config:/params:/wires: already share; a node name that
    # differs from its own label does not resolve.
    exposed = carrier.shield.exposed_socket(exp_name)
    if exposed is None:
        state.diags.append(
            error(
                "phys-socket",
                f"{subject}: carrier '{carrier_name}' (shield "
                f"'{carrier.shield.name}') exposes no socket '{exp_name}'\n"
                "exposed sockets: "
                + (', '.join(sorted(e.label for e in carrier.shield.exposes.values())) or 'none'),
                tuple(x for x in (inst.src, carrier.src) if x),
            )
        )
        return None
    socket, d, scope_entries = compose_socket(ref, carrier.name, exposed, parents, inst.src)
    state.diags.extend(d)
    for path, entry in scope_entries:
        state.scopes[path] = entry
    return socket


def _resolve_one(
    state: _ResolveState, inst: Instance, slot: str, stack: tuple[str, ...]
) -> BoardSocket | None:
    board = state.board
    cached = state.sockets.get(inst.name, {}).get(slot)
    if cached is not None:
        return cached
    subject = _subject(inst, slot)
    ref = inst.sockets.get(slot)
    plug_type = inst.shield.plugs[slot]
    if ref is None:  # inferred board socket
        socket = _infer_socket(state, inst, slot, plug_type)
    elif "." not in ref:  # board socket
        socket = board.resolve(ref)
        if socket is None:
            state.diags.append(
                error(
                    "phys-socket",
                    f"{subject}: board '{board.name}' has no socket "
                    f"'{ref}'\n"
                    f"sockets of {board.name}: "
                    + ", ".join(f"{s.label} ({s.type_name})" for s in board.sockets.values()),
                    (inst.src,) if inst.src else (),
                )
            )
    else:  # carrier-exported socket
        socket = _resolve_carrier_socket(state, inst, subject, ref, stack)
    if socket is not None:
        state.sockets.setdefault(inst.name, {})[slot] = socket
    return socket


def _mating_diagnostic(
    inst: Instance, slot: str, plug_type: str, socket: BoardSocket
) -> Diagnostic | None:
    """Per slot: the socket this slot resolved to must actually
    mate the shield's own plug type. Returns the phys-mating finding, or
    None when it mates."""
    if mating_ok(plug_type, socket.type_name):
        return None
    return error(
        "phys-mating",
        f"{_subject(inst, slot)}: shield '{inst.shield.name}' plugs "
        f"'{plug_type}' but socket '{socket.label}' is a "
        f"'{socket.type_name}' socket — the connectors do not mate",
        tuple(x for x in (inst.src, socket.src) if x),
    )


def _subset_exposure_diagnostics(
    inst: Instance, slot: str, socket: BoardSocket
) -> list[Diagnostic]:
    """Per slot: which of the buses this slot's devices actually
    use are not among the ones its resolved socket exposes -- a bus
    needed only by ANOTHER slot must never be demanded of this one's
    socket."""
    used = {d.bus for d in inst.shield.devices if d.bus and d.plug == slot}
    diags: list[Diagnostic] = []
    for bus in subset_gaps(used, socket.buses):
        diags.append(
            error(
                "phys-subset",
                f"{_subject(inst, slot)}: shield '{inst.shield.name}' needs the "
                f"socket's {bus.upper()} but '{socket.label}' does not expose "
                f"socket,{bus} (subset exposure is declared by absence)",
                tuple(x for x in (inst.src, socket.src) if x),
            )
        )
    return diags


def _distinct_slot_diagnostics(
    inst: Instance,
    resolved_slots: dict[str, BoardSocket],
) -> list[Diagnostic]:
    """Distinct slots of ONE instance must resolve to DISTINCT physical
    sockets -- one physical connector cannot take two plugs at
    once, checked regardless of the per-slot mating outcome (the
    impossibility is physical, not a function of whether the connector
    TYPES happen to agree). The stackability census below would only
    ever catch this as a non-stackable-type collision, and with a
    message that counts "instances" rather than slots -- a genuinely
    miscounting message for this case, which is exactly why this gets
    its own, precise diagnostic."""
    diags: list[Diagnostic] = []
    if len(resolved_slots) <= 1:
        return diags
    by_label: dict[str, list[str]] = {}
    for slot, socket in resolved_slots.items():
        by_label.setdefault(socket.label, []).append(slot)
    for label, slots in sorted(by_label.items()):
        if len(slots) > 1:
            diags.append(
                error(
                    "phys-socket",
                    f"instance '{inst.name}': slots "
                    f"{', '.join(repr(s) for s in sorted(slots))} both "
                    f"resolve to physical socket '{label}' — one "
                    "physical connector cannot take two plugs at once",
                    (inst.src,) if inst.src else (),
                )
            )
    return diags


def _stackability_diagnostics(
    per_socket: dict[str, list[tuple[Instance, BoardSocket]]], types: dict[str, ConnectorType]
) -> list[Diagnostic]:
    """The stackability sweep (final pass, over sorted RESOLVED socket
    labels): more than one instance mating a socket of a non-stackable
    connector type is refused."""
    diags: list[Diagnostic] = []
    for label, entries in sorted(per_socket.items()):
        if len(entries) < 2:
            continue
        ctype = types[entries[0][1].type_name]
        if not ctype.stackable:
            diags.append(
                error(
                    "phys-mating",
                    f"{len(entries)} instances mate socket '{label}' but connector type "
                    f"'{ctype.name}' takes exactly one module (not stackable): "
                    + ", ".join(inst.name for inst, _socket in entries),
                    tuple(inst.src for inst, _socket in entries if inst.src),
                )
            )
    return diags


def resolve_sockets(
    rig: Rig,
    board: Board,
    types: dict[str, ConnectorType],
) -> tuple[SocketResolution, list[Diagnostic]]:
    """The pass, PER SLOT: inference, mating, and subset exposure each
    run once per (instance, slot), independently (no bipartite matching
    between two slots of one instance). Returns the resolution (sockets
    + scopes) alongside every diagnostic, in a fixed discovery order
    that is golden-frozen: per-instance, per-slot-in-authoring-order
    mating/subset checks in rig.instances order, recursing into
    not-yet-resolved carriers depth-first; the stackability sweep last,
    over sorted RESOLVED socket labels. A single-plug shield has
    exactly one slot -- its name is read from `shield.plugs`, never
    assumed to be "plug" -- so it iterates exactly once and this order
    is trivially stable for it."""
    state = _ResolveState(board=board, by_name={i.name: i for i in rig.instances})
    diags = state.diags
    sockets = state.sockets
    # keyed by the RESOLVED socket's own label, never the reference string
    # that named it -- a board socket can be named by either its defining
    # label or a conventional alias, so two instances (or two slots of
    # ONE instance) naming the SAME physical socket by DIFFERENT strings
    # must still land in the same bucket for the exclusivity check below
    # to see them.
    per_socket: dict[str, list[tuple[Instance, BoardSocket]]] = {}

    for inst in rig.instances:
        resolved_slots: dict[str, BoardSocket] = {}
        for slot, plug_type in inst.shield.plugs.items():
            socket = _resolve_one(state, inst, slot, ())
            if socket is None:
                continue
            log.debug(
                "instance '%s': slot '%s': resolved socket '%s' (%s)",
                inst.name,
                slot,
                socket.label,
                socket.type_name,
            )
            resolved_slots[slot] = socket
            mating_diag = _mating_diagnostic(inst, slot, plug_type, socket)
            if mating_diag is not None:
                diags.append(mating_diag)
                continue
            per_socket.setdefault(socket.label, []).append((inst, socket))
            diags.extend(_subset_exposure_diagnostics(inst, slot, socket))

        diags.extend(_distinct_slot_diagnostics(inst, resolved_slots))

    diags.extend(_stackability_diagnostics(per_socket, types))

    return SocketResolution(sockets=sockets, scopes=state.scopes), diags
