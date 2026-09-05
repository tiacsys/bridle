# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""The vendored data roots a unit test hands to the library entry points.

Three of rigc's roots have a module-relative fallback that only resolves
inside this repository -- `registry.BINDINGS` (the connector-type
bindings), the headers those bindings index against, and
`loader.library.SHIELDS_DIR` (the shield corpus). Every one of them is
documented as a dev/test convenience rather than the production path: a
real build threads `--connector-dir`, `--include-dir` and `--shield-dir`
explicitly, and cmake/modules/dts.cmake does exactly that.

A unit test that takes those fallbacks is therefore tethered to this
repository's own `dts/`, `include/` and `boards/` -- it passes here and
fails anywhere else, which is precisely what running the suite in a
downstream workspace revealed. The roots below are the vendored copies
under tests/fixtures/, so a test that uses them exercises the same code
against data that travels with it.

`fixture_types()` is memoised because parsing the binding set is the
expensive part and it is immutable once built; callers must treat the
returned mapping as read-only, since they share one instance.

This is the unit-suite counterpart of `tests/integration/harness.py`'s
deliberate refusal to default `shield_dirs` -- same rule, same reason.
"""

from __future__ import annotations

import functools
from pathlib import Path

from rigc.model import ConnectorType
from rigc.registry import load_types

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"

#: The connector-type bindings, byte-identical to dts/bindings/connectors/
#: and guarded as such by integration_stay/test_vendored_connector_drift.py.
CONNECTOR_DIR = FIXTURES_DIR / "dts" / "unified-connectors"

#: The position-index headers those bindings resolve <type>.h against.
INCLUDE_DIR = FIXTURES_DIR / "include"

#: The vendored shield corpus: byte-identical copies of their boards/shields/
#: originals, deliberately NOT drift-guarded -- pinning them is the point, so a
#: production shield may move without silently rewriting what a test asserts.
SHIELD_DIR = FIXTURES_DIR / "boards" / "shields"


def shield_dirs() -> list[str]:
    """The vendored shield library, as `load`/`discover_shields` want it."""
    return [str(SHIELD_DIR)]


def include_dirs() -> list[str]:
    """The vendored headers as cpp `-I` roots, for `load`'s `include_dirs`.

    A shield template `#include`s its connector's position-index header by
    the same `<dt-bindings/connector/...>` spelling a board does, so a test
    that loads one needs this as well as `shield_dirs()`. Its own
    module-relative fallback is the third of the three, and the least
    obvious: omitting it does not raise, it fails cpp with a missing
    include several frames down.
    """
    return [str(INCLUDE_DIR)]


@functools.cache
def fixture_types() -> dict[str, ConnectorType]:
    """The connector-type registry built from the vendored bindings.

    Returns a SHARED, read-only mapping -- memoised across the suite. A
    caller that needs to mutate one must copy it first.
    """
    types, _deps = load_types([str(CONNECTOR_DIR)], [str(INCLUDE_DIR)])
    return types
