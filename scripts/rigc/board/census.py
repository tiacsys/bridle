# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""A text-only census of board rig-extensions, and the query it answers:
`west rigs --boards-for <target>`.

This module is namespace-agnostic and stays that way: `boards_for` takes a
loaded `Rig`, so whether the caller got that Rig from a persisted rig.yml
or from a promoted shield's synthesized pair is settled entirely in
rigs.py before anything here runs. Nothing below needs to learn the
difference.

**The claim, bounded**: reading a board's REAL devicetree
needs cpp + edtlib + a BuildRecipe, and every board this tooling can build
is an hwmv2 extension a standalone catalog scan never sees -- a real
per-board read costs a real cmake configure per candidate. That is not a
query. So this module censuses board rig-extension SOURCES instead
(``*.dts``/``*.dtsi`` text, regex, no dtlib) and answers a narrower, cheaper
question: which boards' typed sockets satisfy a rig's socket requirements
-- reference resolution (defining label or conventional alias), connector-
type mating, bus subset exposure, and stackability. It is NOT a promise
the rig builds there: GPIO position routing, CS-pool allocation, address
domains and net analysis all need the board's real devicetree, which a
text scan cannot see.

**The dash trap**: `compatible = "socket,<type>"` names the
type with dashes (e.g. "arduino-r3") -- project.py's own
`_project_socket` keeps them, since the value feeds `mating_ok` against
`shield.plugs`, which is the identical dashed spelling. This module's
census keeps the SAME dashed form for exactly that reason. A caller
wanting the label-CONVENTION check (does a socket carry a label matching
its type, "<type>" or "<type>_<silkscreen>") underscores it there, once,
for that one comparison only -- never here, and never by mutating a
CensusBoard's type_name in place.

**The partial Board** this census can build: only label,
type_name, buses (membership, not target -- see `census_board`), src and
path are real; gpio_map/pwm_map/adc_map/cs_pool stay empty/None, since a
text scan cannot resolve a ``*-map``'s phandle target or a binding's default.
Its only valid consumer is `analyzer.sockets.resolve_sockets`, which is
exactly what `boards_for` runs -- ONE implementation of the mating/subset/
alias/stackability rule, never restated here. An unrouted gpio_map is
harmless for that rule (`compose_socket` treats an unrouted parent
position as socket-local); bus pass-through still checks, which is the
part that matters. `resolve_sockets`'s stackability sweep indexes
`types[type_name]`, reachable only once a shield has already mated the
socket (so its type is known-valid) -- no `KeyError` is reachable here,
and this module does not "defend" against one with a silent `.get`.

**`--rigs-for` is deliberately NOT implemented**: the
inverse query -- which rigs a given board satisfies -- is the same census
read backwards, but needs every rig loaded, and it is not on the critical
path this slice serves. Noted here as the considered non-implementation,
not an oversight.

**Known limitation, not a bug**: a rig that declares its
board PER VARIANT with a `sockets:` map (`ard_datalogger`) loads its
instances with that variant's board-specific socket labels baked in
(`nucleo_ard` for the default `nucleo` variant) -- so `--boards-for
ard_datalogger` answers nucleo alone, and `--boards-for ard_datalogger/
frdm` answers frdm alone. That is CORRECT under today's coordinate (the
rig's content already commits to one board's labels); it is exactly the
portability gap that content migration to conventional labels and strict
board/rig symmetry exist to open up."""

from __future__ import annotations

import glob
import os
import re
from collections.abc import Iterator
from dataclasses import dataclass, field, replace
from pathlib import Path

import yaml

from ..analyzer.sockets import resolve_sockets
from ..diag import Diagnostic, SourceRef, has_errors
from ..dtsio import MODULE_ROOT
from ..model import Board, BoardSocket, BusRef, ConnectorType, Rig

#: compatible = "socket,<bus>[-<role>]" property name pattern -> the
#: QUALIFIED bus name (kind, or kind-role) resolve_sockets keys
#: BoardSocket.buses by. Mirrors project.py's own `_BUS_PROP_RE` (kept
#: as a separate copy: this module reads raw text, project.py reads an
#: already-built edtlib.EDT -- two different inputs to the same fact, not
#: one shared value to import). Anchored on `\s*=` immediately after the
#: qualified name so a "-cs-pool" property (e.g. "socket,spi-sensors-
#: cs-pool") is never mistaken for a bus: its own trailing "-cs-pool"
#: leaves no "=" adjacent to any qualified-name-length match.
_BUS_PROP_RE = re.compile(r'\bsocket,((?:i2c|spi|uart)(?:-\w+)?)\s*=')

#: Every socket,*-compatible node in this tree is a childless leaf
#: (properties only, no nested node) -- a brace-balanced regex is exact
#: for that shape, and it tolerates a fragment referencing a node its own
#: file never defines (lotus's `adc0: &adc {};`, which this pattern simply
#: never matches: no compatible property to find inside "{}"), so this
#: never needs a real dtlib parse.
_SOCKET_NODE_RE = re.compile(r"(?P<labels>(?:\w+\s*:\s*)+)(?P<name>\w+)\s*\{(?P<body>[^{}]*)\}")
_COMPAT_RE = re.compile(r'compatible\s*=\s*"socket,([\w-]+)"')


@dataclass(frozen=True)
class SocketNode:
    """One socket,*-compatible node, scanned from board-extension .dts/
    .dtsi TEXT. `labels` is every label the node declares, in declaration
    order (labels[0] is the DEFINING one, the rest are aliases -- the same
    split project.project_edt makes off a real edtlib.Node). `name` is
    the node's own name (not a label): the DT path this node projects to
    is "/" + name. `type_name` is the DASHED form straight off
    `compatible = "socket,<type>"` (the dash trap above). `buses` is which
    QUALIFIED bus names (kind, or kind-role) the node's text declares --
    MEMBERSHIP only, never a resolved target (a text scan cannot follow a
    phandle to the controller it names)."""

    labels: list[str]
    name: str
    type_name: str
    buses: list[str]
    filename: str
    line: int


def scan_socket_nodes(filename: str, text: str) -> Iterator[SocketNode]:
    """Every socket,*-compatible node `text` (one *.dts/*.dtsi fragment's
    full contents, `filename` its path for source anchors only) declares.
    Pure over its two string arguments. Shared by `census_board` (the
    production census this module exists to provide) and
    `tests/unit/test_board_project.py`'s conventional-label lint (which
    underscores `type_name` itself, for that one label-comparison, never
    here) -- ONE scanner for the node shape, never a second regex
    restating it."""
    for m in _SOCKET_NODE_RE.finditer(text):
        compat = _COMPAT_RE.search(m.group("body"))
        if compat is None:
            continue
        labels = [lbl.strip() for lbl in m.group("labels").split(":") if lbl.strip()]
        buses = [bm.group(1) for bm in _BUS_PROP_RE.finditer(m.group("body"))]
        line = text.count("\n", 0, m.start()) + 1
        yield SocketNode(
            labels=labels,
            name=m.group("name"),
            type_name=compat.group(1),
            buses=buses,
            filename=filename,
            line=line,
        )


@dataclass(frozen=True)
class CensusBoard:
    """One board rig-extension target and the PARTIAL Board census_board
    could build for it. `target` is the invocation coordinate
    `<extend>/<qualifier>/<variant name>`, constructed --
    never parsed off a directory name. `dir` is the board-extension
    directory this was scanned from; `census_board` (pure over text, no
    filesystem context) always leaves it None, and `census_boards` (the
    edge) fills it in. `board` is read-only to every consumer; its only
    valid use is `analyzer.sockets.resolve_sockets` (via `boards_for`
    below), never a stand-in for a real project.Board."""

    target: str
    dir: Path | None
    board: Board


def board_targets(board_yml_text: str) -> tuple[str | None, list[str]]:
    """The invocation coordinates one board.yml's raw YAML declares, as
    (extended board name, targets). Pure over its one string argument.

    Target construction: `<extend>/<qualifier>/<variant
    name>`, JOINED from the declared parts -- never parsed off a directory
    name. A board.yml this rule cannot turn into a target -- no
    `board.extend`, no `board.variants`, or a variant entry missing
    `name`/`qualifier` -- contributes no target for that entry; one with
    neither shape at all yields `(None, [])`. This is a considered SKIP
    (the census's scope is board rig-extensions), never an error.

    Split out from `census_board` so the EDGE can decide whether a
    board.yml is in scope BEFORE reading the fragments beside it: a real
    workspace's board roots hold ~1000 board.yml files with ~2800 .dts/
    .dtsi files between them, and reading all of those only to discard
    them is the difference between a query and a file sweep. The caller
    owns the returned list."""
    doc = yaml.safe_load(board_yml_text) or {}
    board_block = doc.get("board") or {}
    extend = board_block.get("extend")
    variants = board_block.get("variants")
    if not extend or not variants:
        return None, []

    targets = []
    for variant in variants:
        if not isinstance(variant, dict):
            continue
        name = variant.get("name")
        qualifier = variant.get("qualifier")
        if name is None or qualifier is None:
            continue
        targets.append(f"{extend}/{qualifier}/{name}")
    return (extend if targets else None), targets


def census_board(
    board_yml_text: str,
    fragments: list[tuple[str, str]],
) -> list[CensusBoard]:
    """Pure over text values: `board_yml_text` is one
    board.yml's raw YAML; `fragments` is [(filename, text), ...] for every
    *.dts/*.dtsi the caller found directly beside it (census_boards' own
    job -- this function never touches a filesystem).

    Targets come from `board_targets` above, including its skip rule: a
    board.yml naming no constructible target returns an empty list, and
    the fragments are then never even looked at.

    Every socket,* node scan_socket_nodes finds across ALL fragments
    builds ONE shared socket set (a board-extension's sockets don't vary
    per declared variant): Board.sockets keyed by each node's defining
    label (labels[0]), Board.aliases carrying every additional label --
    the identical split project.project_edt makes off a real EDT.

    Returns one CensusBoard per constructible variant target, ALL sharing
    that one socket set, each with `dir=None` (this function has no
    filesystem context to fill it with). The caller owns the list and
    every Board it holds; nothing here is shared with another call's
    result."""
    extend, targets = board_targets(board_yml_text)
    if extend is None:
        return []

    sockets: dict[str, BoardSocket] = {}
    aliases: dict[str, str] = {}
    for filename, text in fragments:
        for node in scan_socket_nodes(filename, text):
            label = node.labels[0]
            # buses: MEMBERSHIP only (see SocketNode's own docstring) --
            # the BusRef value is a placeholder, since resolve_sockets'
            # subset check (analyzer/sockets.py's subset_gaps) tests dict
            # KEY presence alone; a synthesized carrier composition that
            # passes one of these buses through simply carries the same
            # placeholder forward, never inspecting it further.
            buses = {kind: BusRef(label="", path="") for kind in node.buses}
            sockets[label] = BoardSocket(
                label=label,
                path=f"/{node.name}",
                type_name=node.type_name,
                gpio_map={},
                buses=buses,
                src=SourceRef(node.filename, node.line, label),
            )
            for alias in node.labels[1:]:
                aliases[alias] = label

    board = Board(name=extend, sockets=sockets, aliases=aliases)
    return [CensusBoard(target=t, dir=None, board=board) for t in targets]


def census_boards(board_roots: list[str] | None = None) -> list[CensusBoard]:
    """The edge: globs `<root>/boards/**/board.yml` for
    every root in `board_roots` (default: [MODULE_ROOT], this module's own
    tree), reads each board.yml plus every *.dts/*.dtsi directly beside it
    -- NOT recursive: a board rig-extension keeps its
    socket fragment(s) beside its own board.yml, never in a subdirectory
    -- and delegates all parsing to `census_board`, the only pure logic
    in this module.

    Scanning every module board root (west's own `west rigs` front end
    already assembles this list at rigs.py:109-116, for rig discovery)
    rather than only MODULE_ROOT costs little, but only because the
    in-scope test runs FIRST: `board_targets` reads one small YAML and
    answers from it, so the ~2800 .dts/.dtsi files beside a real
    workspace's ~1000 board.yml files are never opened. Zero real zephyr
    board.yml declares `extend:`, so scanning that tree also never
    manufactures a spurious target.

    Returns every CensusBoard census_board built, across every matched
    board.yml, sorted by target; the caller owns the list."""
    roots = board_roots if board_roots is not None else [MODULE_ROOT]
    out: list[CensusBoard] = []
    for root in roots:
        pattern = os.path.join(str(root), "boards", "**", "board.yml")
        for board_yml in sorted(glob.glob(pattern, recursive=True)):
            board_dir = Path(board_yml).parent
            with open(board_yml) as f:
                board_yml_text = f.read()
            if not board_targets(board_yml_text)[1]:
                continue
            fragments = []
            for glob_pattern in ("*.dts", "*.dtsi"):
                for frag_path in sorted(board_dir.glob(glob_pattern)):
                    fragments.append((str(frag_path), frag_path.read_text()))
            for cb in census_board(board_yml_text, fragments):
                out.append(replace(cb, dir=board_dir))
    return sorted(out, key=lambda cb: cb.target)


@dataclass(frozen=True)
class BoardVerdict:
    """One census board's conformance verdict against a rig. `conforms`
    is `not has_errors(diags)` over `analyzer.sockets.resolve_sockets`'s
    own run against this board -- mating, bus-subset, alias-aware
    resolution and stackability, all through that ONE rule, never
    restated here. `diags` is kept, not discarded, at no cost now: a
    later "why not this board" affordance (--explain) and any
    --boards-for diagnostic surface both want it."""

    target: str
    conforms: bool
    diags: list[Diagnostic] = field(default_factory=list)


def boards_for(
    rig: Rig, types: dict[str, ConnectorType], boards: list[CensusBoard]
) -> list[BoardVerdict]:
    """Runs `resolve_sockets(rig, cb.board, types)` for every `cb` in
    `boards` -- pure over its arguments (rig, types and every
    CensusBoard.board are read-only to this call). Returns one
    BoardVerdict per candidate, in `boards`' own order; the caller owns
    the list.

    This answers the query bounded in this module's own docstring: a
    conforming board satisfies mating + bus-subset exposure + alias-aware
    reference resolution + stackability against `rig`'s socket
    requirements -- never a promise the rig actually BUILDS there."""
    verdicts = []
    for cb in boards:
        _resolution, diags = resolve_sockets(rig, cb.board, types)
        verdicts.append(BoardVerdict(target=cb.target, conforms=not has_errors(diags), diags=diags))
    return verdicts
