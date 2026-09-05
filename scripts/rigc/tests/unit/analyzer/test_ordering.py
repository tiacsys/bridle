# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Allocation ordering: `allocation_key` is a named, stable sort key --
allocation order is socket, then instance, then device, never rig-file
declaration order. It needs only a plain Instance/Device pair plus the
instance's own resolved BoardSocket -- no Shield/Rig/Board -- so ordering
is asserted directly against constructed values, not a scenario."""

from __future__ import annotations

from rigc.analyzer.ordering import allocation_key
from rigc.model import BoardSocket, Device, Instance, Shield


def _inst(name: str, socket: str | None) -> Instance:
    return Instance(
        name=name, shield=Shield(name="s", label="s", plugs={"plug": "t"}), sockets={"plug": socket}
    )


def _dev(name: str) -> Device:
    return Device(
        name=name,
        label=name,
        compatible=None,
        bus=None,
        group=None,
        reg=None,
        addr_from=None,
        cs_position=None,
    )


def _socket(label: str) -> BoardSocket:
    return BoardSocket(label=label, path=f"/{label}", type_name="t", gpio_map={}, buses={})


def test_key_is_socket_then_instance_then_device() -> None:
    assert allocation_key(_inst("i", "sock"), _dev("d"), _socket("sock")) == ("sock", "i", "d")


def test_ordering_is_by_socket_first_regardless_of_declaration_order() -> None:
    """Sorting by allocation_key must ignore the order members are handed
    in -- the stable contract is socket, then instance, then device."""
    late_socket = (_inst("a_inst", "z_sock"), _dev("d"), _socket("z_sock"))
    early_socket = (_inst("z_inst", "a_sock"), _dev("d"), _socket("a_sock"))
    members = [late_socket, early_socket]

    ordered = sorted(members, key=lambda m: allocation_key(m[0], m[1], m[2]))

    assert ordered == [early_socket, late_socket]


def test_ordering_breaks_ties_by_instance_name_then_device_name() -> None:
    same_socket = "sock"
    members = [
        (_inst("b", same_socket), _dev("y"), _socket(same_socket)),
        (_inst("b", same_socket), _dev("x"), _socket(same_socket)),
        (_inst("a", same_socket), _dev("z"), _socket(same_socket)),
    ]

    ordered = sorted(members, key=lambda m: allocation_key(m[0], m[1], m[2]))

    assert [(i.name, d.name) for i, d, _sock in ordered] == [("a", "z"), ("b", "x"), ("b", "y")]


def test_ordering_never_reads_rig_file_declaration_order() -> None:
    """The key is a pure function of (socket, instance name, device name)
    alone -- it carries no notion of "the order instances appeared in the
    rig file", so two members swapped in declaration order but identical
    in these three fields are genuinely indistinguishable (stable sort
    keeps their relative order, which is the ONLY thing declaration order
    could still influence -- never which one allocates first when the
    keys differ)."""
    a = (_inst("same", "sock"), _dev("dev"), _socket("sock"))
    b = (_inst("same", "sock"), _dev("dev"), _socket("sock"))
    assert allocation_key(*a) == allocation_key(*b)


def test_key_falls_back_to_the_resolved_socket_label_when_none_was_declared() -> None:
    """An inferred instance (Instance.socket is None) carries no authored
    reference string to sort by -- the resolved socket's own label is the
    only fallback that keeps allocation order stable and independent of
    which physical socket inference happened to pick (declared-else-
    resolved, the same shape config-sheet.md uses)."""
    assert allocation_key(_inst("i", None), _dev("d"), _socket("ard")) == ("ard", "i", "d")
