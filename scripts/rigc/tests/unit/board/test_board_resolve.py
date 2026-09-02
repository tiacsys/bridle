# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Board resolution's own value-shaped decision points: board.load_board's
early-exit shapes (a --board-dts naming no real file; no usable recipe)
need no real devicetree or edtlib call at all to reach, so they are
asserted directly. The success / not-rig-enabled outcomes DO need
project.load_board's own result -- stubbed via monkeypatch here rather
than a real board .dts + cpp, exactly like cli.py's own
`test_accept_path_refuses_rather_than_accepting` does: board reading
invokes cpp, so it is integration-only by construction, the same seam
that makes shield-side parsing integration-only -- `_discover_board_dts`
needs no cpp itself (zephyr's list_boards.py over a real MODULE_ROOT scan
is plain YAML/filesystem reading), so its not-found path is exercised
directly below too, alongside the frozen suite's unknown-board golden.

Wording stays out of these tests; code, return shape, and which branch
fired are what's asserted. Diagnostic wording for the two shapes with no
frozen golden (no-recipe, missing-file) is instead verified by comparing
this module's output against a hand-written reference by eye."""

from __future__ import annotations

import os
from pathlib import Path
from textwrap import dedent

import pytest

from rigc.board import resolve
from rigc.board.edt_build import BuildRecipe
from rigc.diag import LoadError, error
from rigc.model import Board, BoardSocket


def test_missing_board_dts_file_is_phys_board_with_no_edtlib_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A --board-dts naming a file that does not exist is caught before
    ANY devicetree machinery runs -- project.load_board is never even
    imported down to a call, proven by monkeypatching it to explode if
    reached."""

    def _boom(*a: object, **kw: object) -> Board:
        raise AssertionError("project.load_board must not be called")

    monkeypatch.setattr("rigc.board.project.load_board", _boom)

    board, diags, deps = resolve.load_board(
        "some_board",
        str(tmp_path),
        board_dts=str(tmp_path / "no-such-file.dts"),
        recipe=BuildRecipe(include_dirs=[], bindings_dirs=[]),
    )

    assert board is None
    assert deps == frozenset()
    assert len(diags) == 1
    assert diags[0].code == "phys-board"


def test_no_recipe_is_phys_board_with_no_edtlib_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """recipe=None (a caller-configuration gap: neither --build-info nor
    --include-dir/--bindings-dir was usable) is its own phys-board
    diagnostic, reached before any devicetree read is attempted."""

    def _boom(*a: object, **kw: object) -> Board:
        raise AssertionError("project.load_board must not be called")

    monkeypatch.setattr("rigc.board.project.load_board", _boom)

    real_dts = tmp_path / "board.dts"
    real_dts.write_text(
        dedent("""\
        /dts-v1/;
        / {};
        """)
    )

    board, diags, deps = resolve.load_board(
        "some_board", str(tmp_path), board_dts=str(real_dts), recipe=None
    )

    assert board is None
    assert deps == frozenset()
    assert len(diags) == 1
    assert diags[0].code == "phys-board"


def test_a_board_with_no_socket_nodes_is_not_rig_enabled(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A board .dts that exists and reads clean but declares no socket,*
    node is the DISTINCT "exists, but is not rig-enabled" diagnostic --
    never confused with "unknown board". Declaring at least one socket,*
    node is how a board opts into rig support."""
    real_dts = tmp_path / "board.dts"
    real_dts.write_text(
        dedent("""\
        /dts-v1/;
        / {};
        """)
    )
    monkeypatch.setattr(
        "rigc.board.project.load_board",
        lambda name, dts_path, recipe, workdir: Board(name=name, sockets={}),
    )

    board, diags, deps = resolve.load_board(
        "socketless_board",
        str(tmp_path),
        board_dts=str(real_dts),
        recipe=BuildRecipe(include_dirs=[], bindings_dirs=[]),
    )

    assert board is None
    assert len(diags) == 1
    assert diags[0].code == "phys-board"
    assert "not rig-enabled" in diags[0].message
    # dependency data is recorded even on THIS rejection -- the board's
    # own .dts was genuinely read.
    assert deps == frozenset({os.path.abspath(str(real_dts))})


def test_a_board_with_sockets_loads_clean(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    real_dts = tmp_path / "board.dts"
    real_dts.write_text(
        dedent("""\
        /dts-v1/;
        / {};
        """)
    )
    fake_board = Board(
        name="b",
        sockets={
            "ard": BoardSocket(label="ard", path="/ard", type_name="t", gpio_map={}, buses={})
        },
    )
    monkeypatch.setattr(
        "rigc.board.project.load_board", lambda name, dts_path, recipe, workdir: fake_board
    )

    board, diags, deps = resolve.load_board(
        "some_board",
        str(tmp_path),
        board_dts=str(real_dts),
        recipe=BuildRecipe(include_dirs=[], bindings_dirs=[]),
    )

    assert board is fake_board
    assert diags == []
    assert deps == frozenset({os.path.abspath(str(real_dts))})


def test_a_malformed_socket_load_error_becomes_the_normal_reject_shape(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A malformed socket makes project.load_board
    raise LoadError (a 3-cell PWM parent it does not support,
    or any other malformed-socket case a checked read there catches) must
    become the ORDINARY (None, diagnostics, deps) shape here -- never an
    unhandled exception escaping load_board -- exactly like every other
    board-resolution failure this module already returns. Dependency data
    (the board's own .dts was genuinely touched before the raise) is still
    recorded, matching test_a_board_with_no_socket_nodes_is_not_rig_enabled's
    own assertion just above."""
    real_dts = tmp_path / "board.dts"
    real_dts.write_text(
        dedent("""\
        /dts-v1/;
        / {};
        """)
    )

    def _boom(name: str, dts_path: str, recipe: object, workdir: str) -> Board:
        raise LoadError(
            error(
                "phys-board",
                "socket 'ard': PWM controller 'pwm0' declares #pwm-cells = <3>, "
                "but rigc supports only a 2-cell PWM parent today",
            )
        )

    monkeypatch.setattr("rigc.board.project.load_board", _boom)

    board, diags, deps = resolve.load_board(
        "some_board",
        str(tmp_path),
        board_dts=str(real_dts),
        recipe=BuildRecipe(include_dirs=[], bindings_dirs=[]),
    )

    assert board is None
    assert len(diags) == 1
    assert diags[0].code == "phys-board"
    assert "#pwm-cells" in diags[0].message
    assert deps == frozenset({os.path.abspath(str(real_dts))})


def test_unknown_board_message_is_cwd_independent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The unknown-board diagnostic anchors MODULE_ROOT via the
    anchor_path renderer, not a bare os.path.relpath -- rendered from two
    different process working directories, the message must come out
    byte-identical. This is the control the CWD-relative wart existed for
    want of: os.path.relpath would fail this assertion, since a relative
    path computed against two different cwds differs."""
    cwd_a = tmp_path / "a"
    cwd_b = tmp_path / "elsewhere" / "b"
    cwd_a.mkdir()
    cwd_b.mkdir(parents=True)

    monkeypatch.chdir(cwd_a)
    _, diags_a = resolve._discover_board_dts("nonexistent_board_xyz")
    monkeypatch.chdir(cwd_b)
    _, diags_b = resolve._discover_board_dts("nonexistent_board_xyz")

    assert len(diags_a) == 1 and len(diags_b) == 1
    assert diags_a[0].message == diags_b[0].message
