# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: BSD-3-Clause
"""Unit tests for edt_build.py, the generic devicetree/edtlib reader layer:
it knows nothing about rigs, sockets, or any other product concept -- only
devicetree/edtlib mechanics plus one piece of Zephyr CMake convention (a
build_info.yml's cmake.devicetree section), so it is the candidate for
upstreaming into python-devicetree itself. Its tests mirror upstream
python-devicetree's test_edtlib.py coverage shape (BSD-3): module-level
test_* functions, plain asserts, no rigc product imports."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from rigc.board import edt_build


def test_recipe_from_build_info(tmp_path: Path) -> None:
    """recipe_from_build_info reads exactly the
    cmake.devicetree.include-dirs / bindings-dirs keys a real
    build_info.yml carries, against a tiny hand-written fixture."""
    build_info = tmp_path / "build_info.yml"
    build_info.write_text(
        dedent("""\
        cmake:
          devicetree:
            include-dirs:
              - /a/include
              - /b/include
            bindings-dirs:
              - /a/dts/bindings
              - /b/dts/bindings
        """)
    )
    recipe = edt_build.recipe_from_build_info(str(build_info))
    assert recipe.include_dirs == ["/a/include", "/b/include"]
    assert recipe.bindings_dirs == ["/a/dts/bindings", "/b/dts/bindings"]


def test_recipe_from_build_info_appends_board_path(tmp_path: Path) -> None:
    """cmake.board.path (boards.cmake's own build_info(board path ...))
    appends onto include_dirs -- an hwmv2 extension variant's own .dts
    lives in a DIFFERENT directory than the base board it quote-includes,
    so that base directory must be on the cpp search path too."""
    build_info = tmp_path / "build_info.yml"
    build_info.write_text(
        dedent("""\
        cmake:
          devicetree:
            include-dirs: [/a/include]
            bindings-dirs: [/a/dts/bindings]
          board:
            path: [/boards/ext, /boards/base]
        """)
    )
    recipe = edt_build.recipe_from_build_info(str(build_info))
    assert recipe.include_dirs == ["/a/include", "/boards/ext", "/boards/base"]


def test_recipe_from_build_info_board_path_may_be_a_bare_string(tmp_path: Path) -> None:
    """A plain (non-extension) board's build_info.yml carries exactly one
    board directory, sometimes recorded as a bare string rather than a
    single-element list -- both shapes normalize to a one-element list."""
    build_info = tmp_path / "build_info.yml"
    build_info.write_text(
        dedent("""\
        cmake:
          devicetree:
            include-dirs: []
            bindings-dirs: []
          board:
            path: /boards/plain
        """)
    )
    recipe = edt_build.recipe_from_build_info(str(build_info))
    assert recipe.include_dirs == ["/boards/plain"]


def test_recipe_from_build_info_board_path_absent_is_fine(tmp_path: Path) -> None:
    """cmake.board may be entirely absent (a hand-written/older
    build_info.yml) -- no board directory to append, not an error."""
    build_info = tmp_path / "build_info.yml"
    build_info.write_text(
        dedent("""\
        cmake:
          devicetree:
            include-dirs: [/a/include]
            bindings-dirs: [/a/dts/bindings]
        """)
    )
    recipe = edt_build.recipe_from_build_info(str(build_info))
    assert recipe.include_dirs == ["/a/include"]
