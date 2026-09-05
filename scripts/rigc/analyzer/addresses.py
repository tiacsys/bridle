# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Address allocation. Per I2C-bus SCOPE (a mux channel is its own NEW
scope), a fixed (copper `reg`) member wins outright, a pinned
(`config:` strap) member resolves through the strap's own domain, and
everything else allocates freely from that same domain -- each group
sorted through the one stable allocation order
(analyzer/ordering.py's `allocation_key`), never rig-file declaration
order.

**The value-shaped core**: `allocate_scope_addresses` is the pure
contract this module exists to make unit-testable on its own -- given
one scope's members in allocation order (some copper-fixed, some
rig-pinned, some free), each already carrying its OWN address domain
where one applies, assign each an address (+ strap state), or report a
same-address conflict or a free member's domain exhaustion. No
Rig/Instance/Shield/BoardSocket needed to call it, mirroring
`analyzer/cs.py`'s `allocate_cs_positions`/`CsMember` exactly.
`_allocate_scope` is the WIRING: it builds one scope's `AddressMember`
list from the rig model (in the three groups' allocation order), calls
the core, and translates its placements/problems back into this pass's
own `AddressAllocation` fields and diagnostics -- the only place strap
names, device labels, and bus labels ever enter the picture.

A rig-pinned member's domain membership (`phys-pin`) is checked INSIDE
the core, in the same single ordered pass as everything else, rather
than by the wrapper up front -- it must interleave with same-address
conflicts and free-domain exhaustion in exactly the members' own
discovery order, which only a single shared pass can guarantee."""

from __future__ import annotations

import logging
from collections.abc import Sequence
from dataclasses import dataclass, field

from ..buskind import is_bus_kind
from ..diag import Diagnostic, error
from ..model import BoardSocket, Device, Instance, Rig, Strap
from .ordering import allocation_key
from .socketmap import Sockets, for_bus_device

#: One scope member ready for grouping: the rig-model triple every group
#: (fixed/pinned/free) sorts and translates the same way.
_ScopeMember = tuple[Instance, Device, BoardSocket]

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class AddressMember:
    """One I2C-scope member's address-allocation input, already in
    allocation order BY GROUP (fixed, then pinned, then free -- the
    caller's own grouping and sort; this function trusts the given order
    and never re-sorts). `fixed` is a copper `reg` address -- wins
    outright, no domain to consult. `pin` is (the rig-authored wanted
    address, the owning strap's own domain) when this member is pinned --
    checked against the domain HERE, in this same pass, not by the
    caller, so an out-of-domain pin interleaves with a same-address
    conflict in the same relative order the single shared loop
    produces. `free` is the strap's own ordered domain when this member
    allocates freely; empty when the member is not free."""

    identity: str
    fixed: int | None = None
    pin: tuple[int, tuple[tuple[int, int], ...]] | None = None
    free: tuple[tuple[int, int], ...] = ()


@dataclass(frozen=True)
class AddressPlacement:
    identity: str
    address: int
    state: int | None  # the strap state claimed (pinned/free); None for fixed
    kind: str  # "fixed" | "pinned" | "free"


@dataclass(frozen=True)
class AddressProblem:
    """One allocation problem, in DISCOVERY order (interleaved across the
    fixed/pinned/free groups exactly as the scope's members were
    processed): `kind` is "out-of-domain" (a pinned member's wanted
    address is not in its strap's own domain -- `address`/`first` unused),
    "conflict" (two members both resolve to `address`; `first` is the
    identity that claimed it earlier), or "exhausted" (a free member's
    domain has nothing left; `occupied` is the domain's full occupancy
    snapshot, address-sorted, AS OF this exact moment in the pass)."""

    kind: str
    identity: str
    address: int | None = None
    first: str | None = None
    occupied: tuple[tuple[int, str], ...] = ()


def allocate_scope_addresses(
    members: Sequence[AddressMember],
) -> tuple[list[AddressPlacement], list[AddressProblem]]:
    """The address-allocation contract: given a scope's members in
    allocation order, each already carrying its own address(es), assign
    every member an address -- or report why not. Members are processed
    IN THE GIVEN ORDER, one shared `taken` map growing as each is
    placed, so a conflict or an exhaustion always sees exactly what
    every EARLIER member (of any kind) in this same call already
    claimed."""
    taken: dict[int, str] = {}
    placements: list[AddressPlacement] = []
    problems: list[AddressProblem] = []

    def claim(address: int, state: int | None, kind: str, identity: str) -> None:
        if address in taken:
            problems.append(
                AddressProblem("conflict", identity, address=address, first=taken[address])
            )
            return
        taken[address] = identity
        placements.append(AddressPlacement(identity, address, state, kind))

    for m in members:
        if m.fixed is not None:
            claim(m.fixed, None, "fixed", m.identity)
        elif m.pin is not None:
            want, domain = m.pin
            match = next(((a, s) for a, s in domain if a == want), None)
            if match is None:
                problems.append(AddressProblem("out-of-domain", m.identity))
                continue
            claim(match[0], match[1], "pinned", m.identity)
        else:
            pick = next(((a, s) for a, s in m.free if a not in taken), None)
            if pick is None:
                problems.append(
                    AddressProblem("exhausted", m.identity, occupied=tuple(sorted(taken.items())))
                )
                continue
            claim(pick[0], pick[1], "free", m.identity)
    return placements, problems


@dataclass
class AddressAllocation:
    addr: dict[tuple[str, str], int] = field(default_factory=dict)  # (inst, dev) -> address
    straps: list[tuple[Instance, Strap, int, int]] = field(
        default_factory=list
    )  # (inst, strap, state, addr)
    bus_label: dict[str, str] = field(default_factory=dict)  # bus path -> label


def allocate_addresses(
    rig: Rig,
    sockets: Sockets,
) -> tuple[AddressAllocation, list[Diagnostic]]:
    diags: list[Diagnostic] = []
    result = AddressAllocation()
    scopes: dict[str, list[tuple[Instance, Device, BoardSocket]]] = {}
    for inst in rig.instances:
        for dev in inst.shield.devices:
            if not is_bus_kind(dev.bus, "i2c"):
                continue
            socket = for_bus_device(sockets, inst, dev)
            if socket is None or dev.bus not in socket.buses:
                continue
            bus = socket.buses[dev.bus]
            result.bus_label[bus.path] = bus.label
            scopes.setdefault(bus.path, []).append((inst, dev, socket))

    for bus_path, members in sorted(scopes.items()):
        diags += _allocate_scope(bus_path, members, result)
    return result, diags


def _address_member(
    kind: str,
    inst: Instance,
    dev: Device,
) -> tuple[AddressMember, Strap | None] | None:
    """Build one member's `AddressMember` plus the strap its domain comes
    from (None for a fixed member, which has no domain to consult), or
    None to skip the member entirely -- a "free" member with no
    `addr_from` strap, which the loader already reported as an
    addr-authority violation."""
    identity = f"{inst.name}/{dev.name}"
    if kind == "fixed":
        assert dev.reg is not None
        return AddressMember(identity=identity, fixed=dev.reg), None
    if kind == "pinned":
        assert dev.addr_from is not None
        strap = inst.shield.straps[dev.addr_from]
        want = inst.straps[dev.addr_from]
        return AddressMember(identity=identity, pin=(want, tuple(strap.domain))), strap
    free_strap = inst.shield.straps.get(dev.addr_from) if dev.addr_from else None
    if free_strap is None:
        return None
    return AddressMember(identity=identity, free=tuple(free_strap.domain)), free_strap


def _how(
    identity: str,
    by_identity: dict[str, _ScopeMember],
    kind_of: dict[str, str],
    strap_of: dict[str, Strap],
) -> str:
    """How one member came to hold its address, for a conflict/exhaustion
    diagnostic's own two-sided listing."""
    _inst, dev, _socket = by_identity[identity]
    kind = kind_of[identity]
    if kind == "fixed":
        return f"address domain {{{dev.reg:#04x}}}, fixed by copper (no address-select)"
    if kind == "pinned":
        return f"pinned via rig (strap '{strap_of[identity].name}')"
    return f"allocated (strap '{strap_of[identity].name}')"


def _address_problem_diagnostics(
    bus_label: str,
    problems: list[AddressProblem],
    by_identity: dict[str, _ScopeMember],
    kind_of: dict[str, str],
    strap_of: dict[str, Strap],
) -> list[Diagnostic]:
    """Translate the core's problems (already in discovery order) into
    this pass's own diagnostics -- the only place strap names, device
    labels, and bus labels enter the picture."""
    diags: list[Diagnostic] = []
    for problem in problems:
        inst, dev, socket = by_identity[problem.identity]
        if problem.kind == "out-of-domain":
            assert dev.addr_from is not None  # only a pinned member reaches here
            strap = strap_of[problem.identity]
            want = inst.straps[dev.addr_from]
            diags.append(
                error(
                    "phys-pin",
                    f"instance '{inst.name}': pinned address {want:#04x} is not in the "
                    f"domain of strap '{strap.name}' "
                    f"({{{', '.join(f'{a:#04x}' for a, _ in strap.domain)}}}) — "
                    "the copper cannot select it",
                    tuple(x for x in (inst.strap_refs.get(dev.addr_from), strap.src) if x),
                )
            )
        elif problem.kind == "conflict":
            assert problem.first is not None  # the core always sets it for a conflict
            o_inst, o_dev, o_socket = by_identity[problem.first]
            diags.append(
                error(
                    "phys-addr",
                    f"I2C address {problem.address:#04x} is required twice on bus "
                    f"&{bus_label} (one address space per scope):\n"
                    f"- {o_inst.name} (socket {o_socket.label}): {o_dev.name} — "
                    f"{_how(problem.first, by_identity, kind_of, strap_of)}\n"
                    f"- {inst.name} (socket {socket.label}): {dev.name} — "
                    f"{_how(problem.identity, by_identity, kind_of, strap_of)}\n"
                    "two devices cannot share one address on one bus. This topology is "
                    "not realizable as assembled: use a second I2C bus, put one device "
                    "behind an I2C mux (scope creation), or drop one instance.",
                    tuple(x for x in (o_dev.src, o_inst.src, dev.src, inst.src) if x),
                )
            )
        else:  # "exhausted"
            strap = strap_of[problem.identity]
            diags.append(
                error(
                    "phys-addr",
                    f"address domain of '{inst.name}/{dev.name}' is exhausted on bus "
                    f"&{bus_label}: every selectable address "
                    f"{{{', '.join(f'{a:#04x}' for a, _ in strap.domain)}}} is already "
                    "taken by:\n"
                    + "\n".join(
                        f"- {by_identity[occ_id][0].name}: {by_identity[occ_id][1].name} "
                        f"at {a:#04x}"
                        for a, occ_id in problem.occupied
                    ),
                    tuple(x for x in (dev.src, inst.src) if x),
                )
            )
    return diags


def _allocate_scope(
    bus_path: str, members: list[_ScopeMember], result: AddressAllocation
) -> list[Diagnostic]:
    """Build this scope's `AddressMember` list in allocation order
    (fixed, then pinned, then free -- three separately-sorted groups,
    concatenated), call the value-shaped core, and translate its
    placements/problems into diagnostics plus this pass's own
    `AddressAllocation` fields."""
    bus_label = result.bus_label[bus_path]
    by_identity: dict[str, _ScopeMember] = {}
    kind_of: dict[str, str] = {}
    strap_of: dict[str, Strap] = {}

    fixed_scope: list[_ScopeMember] = []
    pinned_scope: list[_ScopeMember] = []
    free_scope: list[_ScopeMember] = []
    for inst, dev, socket in members:
        if dev.reg is not None:
            fixed_scope.append((inst, dev, socket))
        elif dev.addr_from and dev.addr_from in inst.straps:
            pinned_scope.append((inst, dev, socket))
        else:
            free_scope.append((inst, dev, socket))

    address_members: list[AddressMember] = []
    for group, kind in ((fixed_scope, "fixed"), (pinned_scope, "pinned"), (free_scope, "free")):
        for inst, dev, socket in sorted(group, key=lambda m: allocation_key(m[0], m[1], m[2])):
            built = _address_member(kind, inst, dev)
            if built is None:
                continue
            member, strap = built
            by_identity[member.identity] = (inst, dev, socket)
            kind_of[member.identity] = kind
            if strap is not None:
                strap_of[member.identity] = strap
            address_members.append(member)

    placements, problems = allocate_scope_addresses(address_members)
    diags = _address_problem_diagnostics(bus_label, problems, by_identity, kind_of, strap_of)

    for placement in placements:
        inst, dev, _socket = by_identity[placement.identity]
        result.addr[(inst.name, dev.name)] = placement.address
        log.debug(
            "instance '%s': device '%s' allocated address %#04x (%s)",
            inst.name,
            dev.name,
            placement.address,
            placement.kind,
        )
        if placement.kind != "fixed":
            assert placement.state is not None  # only a bare "fixed" claim omits it
            strap = strap_of[placement.identity]
            result.straps.append((inst, strap, placement.state, placement.address))

    return diags
