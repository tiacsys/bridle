# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""The unified connector-type files (dts/bindings/connectors/<type>.yaml)
are REAL edtlib bindings — socket schema plus the plug contract as plug,*
vendor-namespaced extension keys (opaque to edtlib, preserved in
Binding.raw; zephyr rig-branch commit 1a657124349).

Why edtlib-loading them matters: edtlib's binding scan is content-sniffing
— pass 2 only ever parses a binding file whose compatible string appears
in the current devicetree. socket,i2c-port never does (its sockets are
shield-synthesized and lowered to plain mux children with no compatible),
so WITHOUT a test like this one that file is validated by nothing: it
could go schema-invalid and no build would notice until the day some DT
carries the compatible. This test is that day, every run.

This module reads a VENDORED copy of the four bindings
(tests/fixtures/dts/unified-connectors/, plus the matching headers under
tests/fixtures/include/dt-bindings/connector/) rather than the production
originals under dts/bindings/connectors/ -- dts/bindings/connectors/ stays
with the hardware definitions when scripts/rigc/ (and this tests/
tree) migrates out to bridle, so this test needs its own copy to keep
travelling with the transpiler. tests/integration_stay/
test_vendored_connector_drift.py is what keeps that copy honest: the
production-tethered assertions (the real four-type census, BINDINGS'
own path) and the byte-identity drift guard both live there instead.
"""

from __future__ import annotations

import glob
import os
import sys

from harness import FIXTURES_DIR, REPO_ROOT, assert_fixture_local, zephyr_base

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from rigc.board.edt_build import ensure_devicetree_on_path  # noqa: E402
from rigc.registry import load_types  # noqa: E402

ensure_devicetree_on_path()
from devicetree import edtlib  # noqa: E402

_VENDORED = FIXTURES_DIR / "dts" / "unified-connectors"
_HEADER_DIR = FIXTURES_DIR / "include"


def _fname2path() -> dict[str, str]:
    """Basename→path over zephyr's OWN bindings tree, enough to resolve
    the include: chains of the vendored connector bindings (gpio-nexus.yaml,
    base.yaml -- both upstream Zephyr bindings, never repo-production
    content) -- the same mapping shape edtlib.EDT itself builds over its
    bindings dirs. None of the four vendored types include one another, so
    no entry for tests/fixtures/dts/unified-connectors/ itself is needed
    here; $ZEPHYR_BASE is not FIXTURES_DIR-local content and is not asserted
    hermetic (see harness.assert_fixture_local's own docstring)."""
    mapping: dict[str, str] = {}
    root = os.path.join(zephyr_base(), "dts", "bindings")
    for path in glob.glob(os.path.join(root, "**", "*.yaml"), recursive=True):
        mapping.setdefault(os.path.basename(path), path)
    return mapping


def test_unified_connector_bindings_are_valid_edtlib_bindings() -> None:
    assert_fixture_local([_VENDORED, _HEADER_DIR])
    files = sorted(glob.glob(os.path.join(str(_VENDORED), "*.yaml")))
    assert files, f"no vendored connector-type bindings found under {_VENDORED}"

    fname2path = _fname2path()
    types, deps = load_types(connector_dirs=[str(_VENDORED)], header_dirs=[str(_HEADER_DIR)])
    assert set(types) == {"arduino-r3", "grove", "i2c-port", "mikrobus"}

    # One trap this vendored copy is exposed to that the production
    # directory never was: dtsio.parse_header_indices ALWAYS appends
    # MODULE_INC (this repo's own include/) to the header search list as a
    # last resort. If a vendored header under _HEADER_DIR were missing,
    # load_types would silently resolve it through repo-production content
    # instead and still pass every assertion above -- assert_fixture_local
    # cannot catch that, since this test never names that fallback path
    # directly. deps is every real file load_types actually opened
    # (four .yaml + four .h when nothing fell through); asserting each one
    # resolves under FIXTURES_DIR is what makes the hermeticity claim
    # non-vacuous rather than decorative.
    assert deps, "load_types recorded no dependencies -- the check below would be vacuous"
    assert_fixture_local(sorted(deps))

    for path in files:
        name = os.path.splitext(os.path.basename(path))[0]
        binding = edtlib.Binding(path, fname2path, require_compatible=True)
        # Identity: filename and compatible agree (the loader keys types by
        # filename; pass 2 keys the same file by compatible).
        assert binding.compatible == f"socket,{name}", path
        # The plug contract rides as plug,* extension keys and survives
        # edtlib parsing (Binding.raw round-trip).
        assert "plug,positions" in binding.raw, path
        assert "plug,bus-proxies" in binding.raw, path
        # And the rig loader assembled a ConnectorType from the same file.
        assert name in types, path


def test_fixture_nexus_type_is_registry_visible() -> None:
    """registry.load_types can see the fixture connector type when
    pointed at its directory explicitly -- fully fixture-local, unlike
    the production-tethered half of what used to be this same test (the
    real four-type census and BINDINGS' own path), which now lives in
    tests/integration_stay/test_vendored_connector_drift.py: no module
    here may mix a fixture-only assertion with one that reaches
    production content."""
    fixture_types, _deps = load_types(
        connector_dirs=[str(FIXTURES_DIR / "dts" / "connectors")],
        header_dirs=[str(FIXTURES_DIR / "include")],
    )
    assert set(fixture_types) == {"fixture-nexus"}
    ctype = fixture_types["fixture-nexus"]
    assert set(ctype.positions) == {"D0", "D1", "CS"}
    assert ctype.bus_proxies == ["i2c", "spi"]
    assert ctype.cs_pool == {"spi": [4]}
