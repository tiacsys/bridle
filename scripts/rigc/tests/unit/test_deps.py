# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: deps -- dependency data is a returned, threaded value: never a
mutable accumulator passed in and written to. `touch`/`union` are the
two primitives every recording point (registry.py, loader/library.py)
composes upward with.
"""

from __future__ import annotations

import os

from rigc.deps import EMPTY, touch, union


def test_touch_normalizes_to_an_absolute_path() -> None:
    result = touch("relative/path.yaml")
    assert result == frozenset({os.path.abspath("relative/path.yaml")})


def test_touch_is_already_absolute_for_an_absolute_input() -> None:
    assert touch("/a/b.yaml") == frozenset({"/a/b.yaml"})


def test_union_of_nothing_is_empty() -> None:
    assert union() == EMPTY


def test_union_combines_and_dedups() -> None:
    a = touch("/a.yaml")
    b = touch("/b.yaml")
    assert union(a, b, a) == frozenset({"/a.yaml", "/b.yaml"})


def test_union_never_mutates_its_inputs() -> None:
    a = touch("/a.yaml")
    b = touch("/b.yaml")
    union(a, b)
    assert a == frozenset({"/a.yaml"})
    assert b == frozenset({"/b.yaml"})


def test_deps_value_is_immutable() -> None:
    """Deps is a frozenset -- a value, with no `.add`/`.see` mutator: a
    caller cannot accumulate into it in place, only combine via `union`."""
    d = touch("/a.yaml")
    assert not hasattr(d, "add")
    assert not hasattr(d, "see")
