# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: loader.binding -- the SocketBinding seam and the invocation's
board -> rig.board.

The stable contracts: SocketBinding's own lookup-else-identity semantics
(the ONE seam a socket: reference resolves through), and resolve_board's
trivial rule -- the injected board, or "". Nothing in rig.yml's own
grammar can produce a `board:`/`sockets:` value for this function to
read, so there is nothing here to reject."""

from __future__ import annotations

from rigc.loader.binding import SocketBinding, resolve_board

# ------------------------------------------------------------ SocketBinding


def test_binding_maps_a_known_name() -> None:
    binding = SocketBinding({"ard": "nucleo_ard"})
    assert binding.get("ard") == "nucleo_ard"


def test_binding_falls_back_to_identity_for_an_unmapped_name() -> None:
    binding = SocketBinding({"ard": "nucleo_ard"})
    assert binding.get("other") == "other"


def test_empty_binding_is_pure_identity() -> None:
    binding = SocketBinding()
    assert binding.get("anything") == "anything"


# --------------------------------------------------------------- resolve_board


def test_no_injection_returns_the_empty_string() -> None:
    """Legal, not an error: a rig's topology never needed a board to
    assemble, and nothing left in rig.yml's own grammar could supply one
    anyway. A caller that actually needs a real board (cli.py, right
    before load_board) is where an empty board becomes a
    diagnostic -- not here."""
    assert resolve_board() == ""
    assert resolve_board(None) == ""


def test_injection_is_returned_unconditionally() -> None:
    assert resolve_board("given/s/rig") == "given/s/rig"
