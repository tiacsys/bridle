# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Shield plurality: the ACCEPT proof for a
folder declaring N shields via `shields:`, named neither of them --
run through the CLI front door exactly like test_reference_shields.py's
accept case.

Not a frozen golden: neither exit_code nor stderr.txt is asserted against
tests/goldens/ -- this fixture pins the SHAPE (two distinct names out of
one folder resolve to two distinct templates), not a rendered diagnostic's
wording, so freeze_or_assert has nothing to freeze here.

The rejection fixtures for shield plurality (a `template: true`
entry with no matching `<name>.shield`; a `shields:` entry whose declared
name disagrees with the folder's basename; a duplicate name within one
`shields:` list; a `shields:` entry missing `name:`) are frozen-golden
cases instead, and live alongside their siblings in
test_emitted_rejects.py rather than here.
"""

from __future__ import annotations

import sys
from pathlib import Path

from harness import FIXTURES_DIR, REPO_ROOT, assert_fixture_local, run_expand

sys.path.insert(0, str(REPO_ROOT / "scripts"))

_FIXTURE = FIXTURES_DIR / "boards" / "rigs" / "shield-plurality-accept"
# Reused verbatim from test_reference_shields.py's own fixture board and
# connector-type root: this scenario needs no new board or binding, only a
# second .shield file in the SAME folder, so borrowing avoids yet another
# fixture board no test would ever tell apart from the first.
_CONNECTOR_BINDINGS = FIXTURES_DIR / "dts" / "connectors"
_CONNECTOR_INCLUDE = FIXTURES_DIR / "include"


def test_two_names_from_one_folder_resolve_to_two_distinct_templates(tmp_path: Path) -> None:
    """`shields/plural_pair/` declares `fx_alpha` and
    `fx_beta` -- a folder named neither -- and a rig instancing both by
    name loads, expands and emits, each resolving to its OWN `<name>.
    shield` translation unit (not, e.g., both collapsing onto whichever
    node the folder's basename would have picked pre-plurality)."""
    board_dts = FIXTURES_DIR / "boards" / "mainboards" / "board.dts"
    bindings_dirs = [_CONNECTOR_BINDINGS]
    include_dirs = [_CONNECTOR_INCLUDE]
    connector_dirs = [_CONNECTOR_BINDINGS]
    shield_dirs = [_FIXTURE / "shields"]
    assert_fixture_local([board_dts, *bindings_dirs, *include_dirs, *connector_dirs, *shield_dirs])

    out_dir = tmp_path / "out"
    result = run_expand(
        _FIXTURE / "rig.yml",
        out_dir,
        board="reference_board",
        shield_dirs=shield_dirs,
        board_dts=board_dts,
        bindings_dirs=bindings_dirs,
        include_dirs=include_dirs,
        connector_dirs=connector_dirs,
    )

    assert result.returncode == 0, (
        f"shield-plurality-accept: expected accept\n--- stderr ---\n{result.stderr}"
    )

    overlay = (out_dir / "rig-gen.overlay").read_text()
    # Each instance's own device, resolved against its OWN socket -- proof
    # the two names parsed as two SEPARATE translation units (a single
    # shared one could not produce two distinctly-labelled led nodes wired
    # to two different sockets).
    assert "alpha_fxa_led" in overlay
    assert "beta_fxb_led" in overlay
    assert "&fixture_socket_b 2 0x0" in overlay
    assert "&fixture_socket_c 2 0x0" in overlay

    config_sheet = (out_dir / "config-sheet.md").read_text()
    assert "fx_alpha" in config_sheet
    assert "fx_beta" in config_sheet
