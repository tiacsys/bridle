# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""A rig's abstract `socket:` references resolve through ONE
`SocketBinding` value, applied at exactly one seam (instance
construction, loader/delta.py) -- the delta engine itself never
touches a socket map, only abstract references. `rig.yml` no longer
has a `board:`/`sockets:` grammar of its own; `resolve_board` is the
one place the invocation's `--board` becomes `rig.board`, so a later
change to how a board reaches this pipeline touches only this module.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SocketBinding:
    """The abstract-socket map an instance's `socket:` resolves through:
    `get(name)` returns the mapped board-socket label, or NAME ITSELF if
    the map does not cover it -- an unmapped name is a BOARD-side
    question, never a loader-level error. Nothing in rig.yml's own
    grammar populates `_map` today, so every rig resolves through an
    empty instance; the map stays a constructor argument rather than a
    bare identity function so a later mechanism (a board-side alias
    table, say) has a seam to populate without every call site changing
    shape."""

    _map: dict[str, str] = field(default_factory=dict)

    def get(self, name: str) -> str:
        return self._map.get(name, name)


def resolve_board(injected_board: str | None = None) -> str:
    """The board this rig actually builds: the invocation's own
    `--board`, unconditionally, or "" when none was given.

    Returning "" rather than raising is deliberate: a rig's TOPOLOGY
    (this loader's own job) never needs a board to assemble. Something
    downstream that actually needs a real board devicetree (cli.py,
    right before board.load_board) is where a still-empty board
    becomes a diagnostic; a bare load (`west rigs --boards-for`'s own
    census, `rigc.promote`'s round-trip check) never reaches that
    point and so never needs one either."""
    return injected_board if injected_board is not None else ""
