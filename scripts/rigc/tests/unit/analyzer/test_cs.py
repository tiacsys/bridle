# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Where and how the final cs-gpios property is calculated:
`allocate_cs_positions` is THE algorithm, extracted from `_allocate_cs(rig,
solved, types, diags)` as a value-shaped contract -- given an ORDERED pool,
the already-taken net identities, and the members of one SPI scope in
their fixed allocation order (some copper-fixed), assign each a position,
or report the pool exhausted. `effective_cs_pool` is the one upstream
pool-MERGE source this module keeps separate from the algorithm ("bus.cs_pool
if not None else ctype.cs_pool[qualified bus name]").

Every test here constructs plain CsMember/CsPlacement values directly --
no Rig, Instance, Shield, Board, or BoardSocket anywhere -- proving the
contract needs no larger scenario to exercise: a reject here is not a unit
concern, it is new coverage of a different subject."""

from __future__ import annotations

from rigc.analyzer.cs import CsMember, CsPlacement, allocate_cs_positions, effective_cs_pool

# ---------------------------------------------------------------- copper-fixed precedence


def test_copper_fixed_member_wins_outright() -> None:
    """A copper-fixed member is placed at its own position regardless of
    the pool -- it is never even consulted against one."""
    members = [CsMember(identity="fixed", fixed=(7, "net-7"))]
    placements, exhausted = allocate_cs_positions(members, occupied=frozenset())
    assert placements == [CsPlacement("fixed", 7, True)]
    assert exhausted == []


def test_copper_fixed_member_is_never_reported_exhausted() -> None:
    """Even when its OWN net identity is already occupied (the frdm_cs_clash
    shape: another instance already claimed the same SoC pin), a
    copper-fixed member still PLACES -- exhaustion is a pool concept, and a
    fixed position draws from no pool at all. The resulting collision is
    the LATER net-conflict check's job (analyzer/gpio.py's check_nets),
    never this function's."""
    members = [CsMember(identity="fixed", fixed=(7, "net-7"))]
    placements, exhausted = allocate_cs_positions(members, occupied=frozenset({"net-7"}))
    assert placements == [CsPlacement("fixed", 7, True)]
    assert exhausted == []


def test_copper_fixed_precedence_over_a_later_pool_member() -> None:
    """A fixed member's position is reserved before a LATER pool member of
    the same scope is considered -- allocation order feeds members here
    already sorted by a named, stable key, and this function processes
    them in that order, so an earlier fixed claim narrows what a later
    free member may still pick."""
    members = [
        CsMember(identity="fixed", fixed=(0, "net-a")),
        CsMember(identity="free", pool=((0, "net-a"), (1, "net-b"))),
    ]
    placements, exhausted = allocate_cs_positions(members, occupied=frozenset())
    assert placements == [
        CsPlacement("fixed", 0, True),
        CsPlacement("free", 1, False),
    ]
    assert exhausted == []


# ---------------------------------------------------------------- pool ordering / first-free


def test_pool_ordering_first_candidate_wins_when_free() -> None:
    members = [CsMember(identity="a", pool=((3, "net-3"), (5, "net-5")))]
    placements, _exhausted = allocate_cs_positions(members, occupied=frozenset())
    assert placements == [CsPlacement("a", 3, False)]


def test_first_free_selection_skips_already_taken_candidates() -> None:
    """The pool is tried IN ORDER; the first candidate whose net identity
    is not already taken wins -- a taken candidate earlier in the pool is
    skipped, never preferred for being first positionally."""
    members = [CsMember(identity="a", pool=((3, "net-3"), (5, "net-5")))]
    placements, _exhausted = allocate_cs_positions(members, occupied=frozenset({"net-3"}))
    assert placements == [CsPlacement("a", 5, False)]


def test_pool_members_of_one_scope_do_not_collide_with_each_other() -> None:
    """Two pool-allocated members of the SAME call take DIFFERENT
    candidates -- each placement's net identity is added to the taken set
    before the next member is considered, a single sequential pass where
    each registration is visible to every later member of the scope."""
    members = [
        CsMember(identity="a", pool=((0, "net-0"), (1, "net-1"))),
        CsMember(identity="b", pool=((0, "net-0"), (1, "net-1"))),
    ]
    placements, exhausted = allocate_cs_positions(members, occupied=frozenset())
    assert placements == [
        CsPlacement("a", 0, False),
        CsPlacement("b", 1, False),
    ]
    assert exhausted == []


# ---------------------------------------------------------------- exhaustion


def test_pool_exhaustion_is_reported_by_identity() -> None:
    """When every candidate is already taken, the member's identity is
    reported exhausted -- it is simply absent from placements, never a
    placement with a bogus position."""
    members = [CsMember(identity="a", pool=((0, "net-0"), (1, "net-1")))]
    placements, exhausted = allocate_cs_positions(members, occupied=frozenset({"net-0", "net-1"}))
    assert placements == []
    assert exhausted == ["a"]


def test_exhaustion_is_per_member_not_all_or_nothing() -> None:
    """One member's pool exhausting does not stop a LATER member (of a
    different, still-open pool) from placing -- exhaustion is reported per
    identity, not by aborting the whole scope."""
    members = [
        CsMember(identity="a", pool=((0, "net-0"),)),
        CsMember(identity="b", pool=((9, "net-9"),)),
    ]
    placements, exhausted = allocate_cs_positions(members, occupied=frozenset({"net-0"}))
    assert placements == [CsPlacement("b", 9, False)]
    assert exhausted == ["a"]


def test_empty_pool_is_exhausted_immediately() -> None:
    members = [CsMember(identity="a", pool=())]
    placements, exhausted = allocate_cs_positions(members, occupied=frozenset())
    assert placements == []
    assert exhausted == ["a"]


# ---------------------------------------------------------------- pool-merge fallback


def test_effective_cs_pool_prefers_the_socket_override() -> None:
    """A shield-SYNTHESIZED socket (carrier/mux composition) may author
    its own socket,cs-pool override -- it wins over the connector type's
    binding default whenever present."""
    assert effective_cs_pool([9, 8], type_default_pool=[0, 1, 2]) == [9, 8]


def test_effective_cs_pool_falls_back_to_the_type_default() -> None:
    """A real board socket whose connector type's binding declares a
    socket,cs-pool default already has it backfilled by edtlib
    (board/project.py) -- but a socket authoring NEITHER (None) falls back to
    the connector type's own default pool."""
    assert effective_cs_pool(None, type_default_pool=[0, 1, 2]) == [0, 1, 2]


def test_effective_cs_pool_treats_an_authored_empty_list_as_an_override() -> None:
    """None means ABSENT (fall back); an authored empty list is a real
    override (a socket that authors socket,cs-pool but declares it empty
    means no CS candidates at all -- distinct from never having declared
    the property)."""
    assert effective_cs_pool([], type_default_pool=[0, 1, 2]) == []
