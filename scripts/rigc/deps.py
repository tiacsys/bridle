# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Dependency data: the real source-tree files one load actually touched
(rig.yml, its content file, `.shield` templates + their cpp-included
files, connector bindings, index headers) -- the input side of the
RIG_DEPENDS handoff. `emitter.context.render` serializes a value of this
type into the sorted, escaped RIG_DEPENDS list cmake/modules/dts.cmake appends to
CMAKE_CONFIGURE_DEPENDS.

Dependency data is a RETURNED/threaded VALUE, never a mutable
accumulator passed down and written into. Every function that opens a
real file returns the paths it touched as part of its own result;
callers compose them upward with `union`, the same way diagnostics
compose upward as list concatenation."""

from __future__ import annotations

import os

#: An immutable set of absolute paths -- deliberately a VALUE type (no
#: `.add`/`.see` mutator), so the only way to grow one is to build a NEW
#: value with `touch`/`union`.
Deps = frozenset[str]

EMPTY: Deps = frozenset()


def touch(path: str) -> Deps:
    """One real file this load touched, normalized to absolute -- the
    smallest Deps value, composed upward by the caller exactly like a
    single Diagnostic is."""
    return frozenset((os.path.abspath(path),))


def union(*deps: Deps) -> Deps:
    """Compose several Deps values into one -- the dependency-data
    analogue of concatenating diagnostic lists."""
    if not deps:
        return EMPTY
    result: set = set()
    for d in deps:
        result |= d
    return frozenset(result)
