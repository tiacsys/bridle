# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Board DT reader -- analyzer-side input: the analyzer reads the board
DT to find socket nodes by compatible. Delegates entirely to
project/edt_build's edtlib.EDT reader over the board's own devicetree.

This module keeps two responsibilities of its own, both about board
RESOLUTION rather than DT mechanics (those live in project/edt_build):

  * board NAME -> .dts path, explicit (the in-build path: dts.cmake already
    resolved BOARD_DIR via boards.cmake, so it passes --board-dts directly)
    or discovered (the standalone/CLI fallback, via zephyr's own
    list_boards.py -- consumed, not forked).

  * the two board-level diagnostics that keep "phys-board" physically
    meaningful: a board that does not exist at all (discovery finds no such
    directory) vs. a board that exists but never opted in (its devicetree
    declares no socket,* node).

**Diagnostics and dependency data are RETURN values**: `load_board`
returns `(Board | None, diagnostics, Deps)` rather than writing into
accumulators handed in from outside -- the board's own .dts joins the
same returned-value deps shape every other reader in this package
already uses."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

from ..deps import Deps, touch
from ..diag import Diagnostic, LoadError, anchor_path, error
from ..dtsio import MODULE_ROOT
from ..model import Board
from . import project
from .edt_build import BuildRecipe

log = logging.getLogger(__name__)


def load_board(
    name: str,
    workdir: str,
    board_dts: str | None = None,
    recipe: BuildRecipe | None = None,
) -> tuple[Board | None, list[Diagnostic], Deps]:
    """Resolve board name to a model.Board, or (None, diagnostics) if it
    can't be read at all.

    board_dts / recipe are the two inputs project.load_board needs (see
    edt_build.BuildRecipe). The in-build path (dts.cmake) always passes both
    explicitly -- BOARD_DIR is already resolved by boards.cmake long before
    the analyzer runs, and dts.cmake computes the recipe itself. Leaving
    board_dts None triggers the standalone/CLI discovery fallback below;
    leaving recipe None (whether or not board_dts was given) is a
    caller-configuration gap, reported the same way as any other
    board-resolution failure -- see the recipe is None branch.

    The returned Deps records the board's own .dts (not its cpp-included
    files -- those are the board's own concern, covered elsewhere; a rig
    build's dependency tracking cares about the ONE file naming the board,
    matching what --board-dts itself takes as a single path).

    Returns (board, diagnostics, deps): board is None when the board
    could not be read at all (a phys-board finding says why); deps
    names the files this resolution touched. Inputs are read-only."""
    if board_dts is None:
        board_dts, d = _discover_board_dts(name)
        if board_dts is None:
            return None, d, frozenset()
    elif not os.path.isfile(board_dts):
        return (
            None,
            [error("phys-board", f"board '{name}': no such devicetree file\n  {board_dts}")],
            frozenset(),
        )

    if recipe is None:
        return (
            None,
            [
                error(
                    "phys-board",
                    f"board '{name}': no devicetree-reading recipe available "
                    f"({board_dts})\n"
                    "pass --include-dir/--bindings-dir (repeatable), or --build-info "
                    "<build_info.yml> from a real build, to read its devicetree — a "
                    "rig build (dts.cmake) supplies this automatically",
                )
            ],
            frozenset(),
        )

    deps = touch(board_dts)
    try:
        board = project.load_board(name, board_dts, recipe, workdir)
    except LoadError as e:
        # A malformed socket,* nexus (a PWM/ADC controller whose own
        # declared cell count rigc does not support) raises
        # LoadError rather than crashing with an unhandled ValueError --
        # this is the catch
        # boundary that turns it into the ordinary (None, diagnostics,
        # deps) shape every other board-resolution failure in this
        # function already returns, exactly as dtsio.py's own LoadError
        # raises are caught at THEIR boundary (loader/library.py,
        # loader/__init__.py).
        return None, list(e.diags), deps
    if not board.sockets:
        return (
            None,
            [
                error(
                    "phys-board",
                    # anchor_path, not relpath: a cwd-relative path renders
                    # differently depending on where the tool was invoked from, so a
                    # reproduction of the same failure would not reproduce the same
                    # text (see the rerun-script note in the integration conftest).
                    f"board '{name}' has a devicetree ({anchor_path(board_dts)}) "
                    "but declares no socket,* nodes — it exists, but is not "
                    "rig-enabled (a board opts in with a typed socket node)",
                )
            ],
            deps,
        )
    log.info("board '%s' resolved: %s", name, board_dts)
    return board, [], deps


def _discover_board_dts(name: str) -> tuple[str | None, list[Diagnostic]]:
    """Standalone/CLI fallback: resolve a board NAME to its own .dts by
    consuming zephyr's own scripts/list_boards.py (not forking it). Searches
    only this module's own board root (MODULE_ROOT) -- a narrower catalog
    than a real build sees.

    name may carry hwmv2 qualifiers (<board>/<qualifiers...>, e.g. an
    extension variant nucleo_f401re/stm32f401xe/rig --
    boards/extend/st/nucleo_f401re/): the qualifiers select a
    <board>_<qualifiers>[.dts] file (full form, falling back to the
    single-SoC short form that drops the leading SoC segment -- the same
    two candidates dts.cmake's own dts_configuration_files() tries), never
    a bespoke naming rule.

    Known gap: every board this tooling can build today is an hwmv2
    extension whose base lives outside MODULE_ROOT (a real upstream board
    in $ZEPHYR_BASE, or another Zephyr module) -- list_boards.find_v2_boards()
    only attaches a board.yml extend: entry to a base it can already see, so
    a MODULE_ROOT-only scan never learns of any of them, and this
    fallback's own board catalog is consequently always empty. The
    in-build path (dts.cmake) never hits this: BOARD_DIR/BOARD_DIRECTORIES
    are already resolved by boards.cmake (which scans every real
    BOARD_ROOT) long before the analyzer runs, so --board-dts is always
    passed explicitly for a real build."""
    zephyr_base = os.environ["ZEPHYR_BASE"]
    scripts_dir = os.path.join(zephyr_base, "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import list_boards  # noqa: E402  (zephyr script, consumed not forked)

    board_name, _, qualifiers = name.partition("/")
    args = argparse.Namespace(
        board_roots=[Path(MODULE_ROOT)], soc_roots=[Path(zephyr_base)], board=None, board_dir=[]
    )
    boards = list_boards.find_v2_boards(args)
    if board_name not in boards:
        return None, [
            error(
                "phys-board",
                f"unknown board '{name}'\n"
                # anchor_path, not relpath: a cwd-relative path renders
                # differently depending on where the tool was invoked from, so a
                # reproduction of the same failure would not reproduce the same
                # text (see the rerun-script note in the integration conftest).
                f"no such board directory under {anchor_path(MODULE_ROOT)}/boards\n"
                "this standalone lookup only searches that one root; every "
                "board this tooling can build today extends a base that lives "
                "elsewhere (a real Zephyr board, or another Zephyr module), so "
                "it is never listed here either way -- run west boards for "
                "the full catalog, or pass --board-dts directly",
            )
        ]

    board = boards[board_name]
    directories = board.directories if isinstance(board.directories, list) else [board.directories]
    if not qualifiers:
        candidates = [board_name]
    else:
        segments = qualifiers.split("/")
        candidates = ["_".join([board_name] + segments)]
        socs = len(board.socs) if board.socs else 0
        if socs == 1 and len(segments) > 1:
            candidates.append("_".join([board_name] + segments[1:]))

    # Later directories win on a naming collision, matching dts.cmake's own
    # (no-break, last-match-overwrites) BOARD_DIRECTORIES search loop.
    for directory in reversed(directories):
        for candidate in candidates:
            path = directory / f"{candidate}.dts"
            if path.is_file():
                return str(path), []

    return None, [
        error(
            "phys-board",
            f"unknown board '{name}'\n"
            f"no '{candidates[0]}.dts' (or short form) found in any of: "
            f"{', '.join(str(d) for d in directories)}",
        )
    ]
