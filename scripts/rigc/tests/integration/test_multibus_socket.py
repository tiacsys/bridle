# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Multi-bus sockets: a socket may offer more than one bus of the same
kind (multi-bus-socket schema). Proved with a NEW fixture connector type
only (socket,fixture-multibus, tests/fixtures/dts/multibus-connectors/)
-- no real board or shield in the corpus needs this, following the same
fixture-connector precedent socket,fixture-nexus already established for
test_reference_shields.py.

`multibus_board.dts` offers ONE socket with two independent, named SPI
buses (socket,spi-sensors / socket,spi-motors), each with its own
binding-default cs_pool, mated by two fixture shields on the SAME socket
instance (accept case, below) plus a third shield naming a bus the
connector type's vocabulary allows but no socket ever wires (reject
case). No golden is frozen here, the same shape test_reference_shields.py
already uses for a fixture-only accept scenario: this feature adds no
new corpus consumer for a golden to protect, and every assertion below
targets the specific fact under test rather than the whole artifact.

The real-toolchain round trip (test_multibus_expand_and_build_round_trip,
@pytest.mark.build) needs a real corpus board (nucleo_f401re/stm32f401xe/
rig, a board extension under boards/extend/st/nucleo_f401re/ in the
repository the rigs are defined in)
to supply the toolchain -- that dependency is exactly what this suite's
integration/integration_stay split is drawn on, so that test lives on the
stay side, in test_multibus_socket_build.py, alongside a small duplicated
copy of this module's own fixture-path constants and _run helper (see that
module's own docstring for why duplicating rather than importing across
the split was the right call here).
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from harness import FIXTURES_DIR, assert_fixture_local, run_expand

_BOARD_DTS = FIXTURES_DIR / "boards" / "mainboards" / "multibus_board.dts"
# A directory of its own, deliberately separate from
# tests/fixtures/dts/connectors/ (fixture-nexus.yaml's own home): that
# directory's OWN registry test (test_connector_bindings.py) asserts it
# holds EXACTLY {"fixture-nexus"}, so adding a second type there would
# perturb an existing, unrelated fixture's own precise assertion.
_CONNECTOR_BINDINGS = FIXTURES_DIR / "dts" / "multibus-connectors"
_CONNECTOR_INCLUDE = FIXTURES_DIR / "include"
_SHIELDS = FIXTURES_DIR / "boards" / "rigs" / "multibus-sockets" / "shields"
_ACCEPT_RIG = FIXTURES_DIR / "boards" / "rigs" / "multibus-sockets" / "rig.yml"
_REJECT_RIG = FIXTURES_DIR / "boards" / "rigs" / "multibus-sockets-reject" / "rig.yml"


def _run(rig_yml: Path, out_dir: Path) -> subprocess.CompletedProcess[str]:
    assert_fixture_local([_BOARD_DTS, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE, _SHIELDS])
    return run_expand(
        rig_yml,
        out_dir,
        board="multibus_fixture_board",
        shield_dirs=[_SHIELDS],
        board_dts=_BOARD_DTS,
        bindings_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
        connector_dirs=[_CONNECTOR_BINDINGS],
    )


def test_multibus_accept_both_devices_land_at_cs_index_zero(tmp_path: Path) -> None:
    """Accept case: fixture_spi_sensor (bus: "spi-sensors") and
    fixture_spi_motor (bus: "spi-motors") both mate multibus_socket and
    both build. The negative control this project's discipline demands:
    both devices may legally share the SAME
    cs-pool INDEX (0) without collision, since they sit on DIFFERENT
    physical SPI buses -- CS allocation is scoped by bus.path, never by
    kind string. Without this assertion, a regression that accidentally
    merged the two buses' CS namespaces back into one would still pass
    every other check (it would only ever place ONE of the two devices,
    reporting the other's single-candidate pool exhausted -- itself
    caught by the plain accept assertion below, but the shared-index
    claim is the more specific, mutation-resistant one)."""
    out_dir = tmp_path / "out"
    result = _run(_ACCEPT_RIG, out_dir)

    assert result.returncode == 0, (
        f"multibus_sockets: expected accept\n--- stderr ---\n{result.stderr}"
    )

    overlay = (out_dir / "rig-gen.overlay").read_text()
    assert "&multibus_spi_sensors {" in overlay
    assert "&multibus_spi_motors {" in overlay
    # Both devices are the sole member of their own bus's scope, so both
    # land at cs-gpios array index 0 (the FIRST, and only, cs-gpios entry
    # in each of their two &<bus> blocks) -- the shared-index claim.
    sensors_block = overlay.split("&multibus_spi_sensors {")[1].split("};")[0]
    motors_block = overlay.split("&multibus_spi_motors {")[1].split("};")[0]
    assert "sensor@0" in sensors_block
    assert "driver@0" in motors_block


def test_multibus_reject_unknown_named_bus_is_phys_subset(tmp_path: Path) -> None:
    """Reject case: fixture_spi_unknown declares bus: "spi-unknown-name"
    -- allowed by the fixture-multibus connector type's own bus_proxies
    vocabulary (so it mates the socket and passes lang-shield-proxy), but
    no socket of that type ever wires a matching phandle. subset_gaps'
    exact-string membership check (needed - set(offered)) rejects it
    without any fallback, confirmed with a genuinely novel string rather
    than a name that happens to coincide with something else in the
    corpus."""
    out_dir = tmp_path / "out"
    result = _run(_REJECT_RIG, out_dir)

    assert result.returncode != 0, "multibus_sockets_reject: expected reject (phys-subset)"
    assert "phys-subset" in result.stderr
    assert "spi-unknown-name" in result.stderr
