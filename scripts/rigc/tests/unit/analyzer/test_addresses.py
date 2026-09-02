# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Where and how the final I2C address is calculated: `allocate_scope_addresses`
is THE algorithm, extracted from `_allocate_scope` as a value-shaped contract
-- given one scope's members in their fixed allocation order (some
copper-fixed, some rig-pinned, some free), each already carrying its own
address(es), assign every member an address (+ strap state), or report why
not (an out-of-domain pin, a same-address conflict, or a free member's
domain exhausted).

Every test here constructs plain AddressMember values directly -- no
Rig, Instance, Shield, Device, or BoardSocket anywhere -- proving the
contract needs no larger scenario to exercise: a reject here is not a unit
concern, it is new coverage of a different subject, the same standard
`test_cs.py` already meets for CS allocation."""

from __future__ import annotations

from rigc.analyzer.addresses import (
    AddressMember,
    AddressPlacement,
    AddressProblem,
    allocate_scope_addresses,
)

# ---------------------------------------------------------------- fixed wins outright


def test_fixed_member_is_claimed_verbatim() -> None:
    members = [AddressMember(identity="a", fixed=0x50)]
    placements, problems = allocate_scope_addresses(members)
    assert placements == [AddressPlacement("a", 0x50, None, "fixed")]
    assert problems == []


def test_two_fixed_members_at_the_same_address_conflict() -> None:
    members = [AddressMember(identity="a", fixed=0x5F), AddressMember(identity="b", fixed=0x5F)]
    placements, problems = allocate_scope_addresses(members)
    assert placements == [AddressPlacement("a", 0x5F, None, "fixed")]
    assert problems == [AddressProblem("conflict", "b", address=0x5F, first="a")]


# ------------------------------------------- pinned resolves through its domain


def test_pinned_member_resolves_through_its_domain() -> None:
    members = [AddressMember(identity="a", pin=(0x11, ((0x10, 0), (0x11, 1))))]
    placements, problems = allocate_scope_addresses(members)
    assert placements == [AddressPlacement("a", 0x11, 1, "pinned")]
    assert problems == []


def test_pinned_member_outside_its_domain_is_out_of_domain() -> None:
    members = [AddressMember(identity="a", pin=(0x99, ((0x10, 0),)))]
    placements, problems = allocate_scope_addresses(members)
    assert placements == []
    assert problems == [AddressProblem("out-of-domain", "a")]


def test_a_fixed_claim_can_collide_with_a_later_pinned_member() -> None:
    """Allocation order (fixed, then pinned) feeds members here already
    grouped -- an earlier fixed claim narrows what a LATER pinned member
    may still claim, exactly like CS's fixed-precedence-over-pool test."""
    members = [
        AddressMember(identity="fixed", fixed=0x50),
        AddressMember(identity="pinned", pin=(0x50, ((0x50, 0),))),
    ]
    placements, problems = allocate_scope_addresses(members)
    assert placements == [AddressPlacement("fixed", 0x50, None, "fixed")]
    assert problems == [AddressProblem("conflict", "pinned", address=0x50, first="fixed")]


# ---------------------------------------------------------------- free allocation


def test_free_member_picks_the_first_unclaimed_domain_address() -> None:
    members = [AddressMember(identity="a", free=((0x10, 0), (0x11, 1)))]
    placements, problems = allocate_scope_addresses(members)
    assert placements == [AddressPlacement("a", 0x10, 0, "free")]
    assert problems == []


def test_free_member_skips_an_already_taken_candidate() -> None:
    members = [
        AddressMember(identity="taken", fixed=0x10),
        AddressMember(identity="free", free=((0x10, 0), (0x11, 1))),
    ]
    placements, problems = allocate_scope_addresses(members)
    assert placements == [
        AddressPlacement("taken", 0x10, None, "fixed"),
        AddressPlacement("free", 0x11, 1, "free"),
    ]
    assert problems == []


def test_free_domain_exhaustion_reports_the_full_occupancy_snapshot() -> None:
    members = [
        AddressMember(identity="taken", fixed=0x10),
        AddressMember(identity="free", free=((0x10, 0),)),
    ]
    placements, problems = allocate_scope_addresses(members)
    assert placements == [AddressPlacement("taken", 0x10, None, "fixed")]
    assert problems == [AddressProblem("exhausted", "free", occupied=((0x10, "taken"),))]


def test_exhaustion_is_per_member_not_all_or_nothing() -> None:
    """One free member's domain exhausting does not stop a LATER free
    member (of a different, still-open domain) from placing."""
    members = [
        AddressMember(identity="taken", fixed=0x10),
        AddressMember(identity="a", free=((0x10, 0),)),
        AddressMember(identity="b", free=((0x20, 0),)),
    ]
    placements, problems = allocate_scope_addresses(members)
    assert [p.identity for p in placements] == ["taken", "b"]
    assert problems == [AddressProblem("exhausted", "a", occupied=((0x10, "taken"),))]


def test_two_free_members_of_one_call_do_not_collide_with_each_other() -> None:
    """Each placement's address is added to the shared `taken` map before
    the next member is considered: a single sequential pass where each
    registration is visible to every later member of the scope."""
    members = [
        AddressMember(identity="a", free=((0x10, 0), (0x11, 1))),
        AddressMember(identity="b", free=((0x10, 0), (0x11, 1))),
    ]
    placements, problems = allocate_scope_addresses(members)
    assert placements == [
        AddressPlacement("a", 0x10, 0, "free"),
        AddressPlacement("b", 0x11, 1, "free"),
    ]
    assert problems == []
