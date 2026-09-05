# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: the tests' own conftest — the hermeticity enforcement.

assert_fixture_local is the structural proof a hermetic test leans on;
if the enforcement is broken, the boundary decays silently -- so the
enforcement gets its own unit coverage, against a synthetic root.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from rigc.tests.conftest import assert_fixture_local


def test_paths_inside_the_root_pass(tmp_path: Path) -> None:
    inside = tmp_path / "boards" / "rigs" / "r" / "rig.yml"
    assert_fixture_local([inside, tmp_path], fixtures_dir=tmp_path)


def test_path_outside_the_root_fails(tmp_path: Path) -> None:
    with pytest.raises(AssertionError):
        assert_fixture_local([tmp_path / ".." / "elsewhere.yml"], fixtures_dir=tmp_path)


def test_sibling_with_root_as_prefix_fails(tmp_path: Path) -> None:
    """/root-extra must not pass a /root check (prefix, not component)."""
    sibling = tmp_path.parent / (tmp_path.name + "-extra") / "f.yml"
    with pytest.raises(AssertionError):
        assert_fixture_local([sibling], fixtures_dir=tmp_path)
