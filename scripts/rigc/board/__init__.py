# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""The board reader: the board's own devicetree, read for real.

  resolve.py    -- board NAME -> .dts path (explicit --board-dts, or
                    standalone discovery) plus the two board-level
                    diagnostics (unknown board, board not rig-enabled)
  project.py    -- edtlib.EDT -> model.Board projection: every socket,*
                    node's gpio/pwm/adc maps, buses and cs-pool default
  edt_build.py  -- the generic edtlib.EDT construction (cpp + bindings),
                    BSD-3-Clause, no product imports (see its own header)
  census.py     -- the text-only `west rigs --boards-for` census, over
                    board sources rather than a real edtlib read

`resolve.load_board` is the production entry point (cli.py calls it
right before the analyzer runs); `project.load_board`/`project_edt` are
its edtlib-side counterpart, callable directly against an already-built
EDT (the unit tests' path, no cpp). `census.census_boards`/`boards_for`
serve the `--boards-for` query and never touch a real devicetree."""

from .census import boards_for, census_boards
from .edt_build import BuildRecipe, recipe_from_build_info
from .project import project_edt
from .resolve import load_board

__all__ = [
    "BuildRecipe",
    "boards_for",
    "census_boards",
    "load_board",
    "project_edt",
    "recipe_from_build_info",
]
