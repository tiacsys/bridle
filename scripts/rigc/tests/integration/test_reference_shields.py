# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""The reference shield set (rigs test suite): fixtures/boards/shields/reference
demonstrates the four main shield-authoring patterns as ACCEPTED material —
the opposite of every other fixture in this suite, which is named for the
defect it triggers. A reference implementation nobody exercises is
documentation, and documentation drifts, so this test runs the whole
pipeline (load -> analyze -> emit) end to end through the CLI and asserts
on the accepted result, the same way the corpus emitted goldens do for real
rigs.

The reference shields also #include this fixture tree's own
<dt-bindings/connector/fixture-nexus.h> and claim positions by macro
(FIXTURE_D0, FIXTURE_CS), exactly the idiom a real shield
uses — the same --include-dir list now reaches a .shield template's own
cpp preprocess (dtsio.run_cpp), not only the board .dts and the registry's
header lookup.

The connector-type registry's own proof of configurability
(ctypes_registry.load_types's connector_dirs/header_dirs parameters) lives
in test_connector_bindings.test_fixture_nexus_type_is_registry_visible
rather than here: that test asserts on the real registry's four
connector-type names too (the default-preserving fallback half of the
same proof), which is integration, and no module here may mix the two.

Board + registry pieces are fixture-local (assert_fixture_local, below); the
per-instance parameter values are plain integers rather than zephyr,code
macros specifically so the WHOLE fixture tree stays free of any dependency
outside itself (no shield,param-includes header needed at all).

The honest limit, worth repeating here rather than only in the fixtures'
own comments: this proves the SHAPE is right — that a shield authored
against a registry-complete connector type mates, and that its devices
resolve to the right positions/buses/addresses. It proves nothing about
whether any REAL board's binding agrees with what its schema promises; it
could not have caught the sam0 two-cell PWM bug (test_pwm_nonzero_flags_
golden, test_emitted_corpus.py), which only surfaced against a real
binding. The corpus rigs under boards/rigs/ remain the proof that real
hardware works.
"""

from __future__ import annotations

import sys
from pathlib import Path

from harness import FIXTURES_DIR, REPO_ROOT, assert_fixture_local, run_expand

sys.path.insert(0, str(REPO_ROOT / "scripts"))

_FIXTURE = FIXTURES_DIR / "boards" / "rigs" / "reference-shields"
# Deliberately OUTSIDE fixtures/dts/bindings/: this directory serves as both
# an edtlib bindings dir and the connector-type root (its YAML is a unified
# socket+plug binding). Nested under bindings/, edtlib's recursive scan would
# also load it while reading the unit tree's own bindings, and the two would
# collide on the shared socket,fixture-nexus compatible.
_CONNECTOR_BINDINGS = FIXTURES_DIR / "dts" / "connectors"
_CONNECTOR_INCLUDE = FIXTURES_DIR / "include"


def test_reference_shields_accept(tmp_path: Path) -> None:
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
        f"reference-shields: expected accept\n--- stderr ---\n{result.stderr}"
    )

    overlay = (out_dir / "rig-gen.overlay").read_text()

    # Fixed-address I2C device: reg authored verbatim, address-authority
    # rule satisfied (reg present, shield,addr-from absent).
    assert "&fixture_i2c {" in overlay
    assert "sensor@50" in overlay
    assert 'compatible = "vnd,fixture-sensor";' in overlay
    assert "reg = <0x50>;" in overlay

    # CS-position device: shield,cs-position (FIXTURE_CS, index 4) resolved
    # to a copper-fixed CS net on the SPI bus, not the CS pool.
    assert "&fixture_spi {" in overlay
    assert "cs-gpios = <&fixture_socket_a 4 1" in overlay
    assert "flash@0" in overlay
    assert 'compatible = "vnd,fixture-flash";' in overlay

    # GPIO collection + per-instance parameter: ONE shared collection node,
    # two entries, each carrying its OWN assigned zephyr,code (emitted
    # verbatim) and each resolved against its OWN socket's position.
    assert 'compatible = "vnd,fixture-keys";' in overlay
    assert "button_a_fb_key" in overlay
    assert "button_b_fb_key" in overlay
    assert "zephyr,code = <1>;" in overlay
    assert "zephyr,code = <2>;" in overlay
    assert "&fixture_socket_b 2 0x0" in overlay
    assert "&fixture_socket_c 2 0x0" in overlay

    config_sheet = (out_dir / "config-sheet.md").read_text()
    assert "fixture_socket_a" in config_sheet
    assert "fixture_socket_b" in config_sheet
    assert "fixture_socket_c" in config_sheet
