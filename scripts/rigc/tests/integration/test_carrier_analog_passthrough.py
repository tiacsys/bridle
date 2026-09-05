# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""PWM and ADC through a carrier, end to end. HERMETIC and
non-build, mirroring test_multiplug_carrier.py's own combined-SPI
fixture: a purpose-built fixture board (carrier_analog_board.dts)
declares a real pwm-map/io-channel-map nexus on the connector a fixture
carrier plugs -- a shape none of the real board sockets in the corpus
happen to carry, which is why this witness needs a
fixture board rather than nucleo_grove_farm on nucleo_f401re/frdm_k64f.

Two rigs (both driven through the real CLI, `python -m rigc expand`):

  carrier-analog-passthrough (ACCEPT) -- fixture_analog_carrier
    re-exports ONE socket (ca_out) carrying gpio+pwm+adc rows; a PWM
    consumer and an ADC consumer both mate it. Proves that both
    functions resolve through a carrier-exposed socket, by an emitted
    overlay, and that one synthesized node carries all three maps
    together.

  carrier-analog-passthrough-reject -- two INDEPENDENT reject instance
    pairs in one rig: an unrouted PWM position is an error, never gpio's
    own silent drop, and a carrier's declared #pwm-cells disagreeing
    with the resolved parent's is refused (require-and-check).
"""

from __future__ import annotations

from pathlib import Path

from harness import FIXTURES_DIR, assert_fixture_local, run_expand

_CONNECTOR_BINDINGS = FIXTURES_DIR / "dts" / "carrier-analog-connectors"
_CONNECTOR_INCLUDE = FIXTURES_DIR / "include"
_BOARD_DTS = FIXTURES_DIR / "boards" / "mainboards" / "carrier_analog_board.dts"
_SHIELDS = FIXTURES_DIR / "boards" / "rigs" / "carrier-analog-passthrough" / "shields"
_ACCEPT_RIG = FIXTURES_DIR / "boards" / "rigs" / "carrier-analog-passthrough" / "rig.yml"
_REJECT_RIG = FIXTURES_DIR / "boards" / "rigs" / "carrier-analog-passthrough-reject" / "rig.yml"


def _run(rig_yml: Path, out_dir: Path):
    assert_fixture_local([_BOARD_DTS, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE, _SHIELDS])
    return run_expand(
        rig_yml,
        out_dir,
        board="carrier_analog_fixture_board",
        shield_dirs=[_SHIELDS],
        board_dts=_BOARD_DTS,
        bindings_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
        connector_dirs=[_CONNECTOR_BINDINGS],
    )


def test_accept_both_functions_resolve_through_the_carrier(tmp_path: Path) -> None:
    """A shield needing PWM, and one needing ADC,
    both resolve through a carrier-exposed socket, proven by an emitted
    overlay -- not reasoned about."""
    out_dir = tmp_path / "out"
    result = _run(_ACCEPT_RIG, out_dir)

    assert result.returncode == 0, (
        f"carrier_analog_passthrough: expected accept\n--- stderr ---\n{result.stderr}"
    )

    overlay = (out_dir / "rig-gen.overlay").read_text()
    assert "pwms = <&carrier_ca_out 0 20000000>;" in overlay
    assert "io-channels = <&carrier_ca_out 1>;" in overlay


def test_accept_synthesized_nexus_carries_all_three_maps_on_one_node(tmp_path: Path) -> None:
    """On a mixed socket, ONE synthesized node
    (carrier_ca_out) carries gpio-map AND pwm-map AND io-channel-map --
    never two nodes, never one map silently winning. The nexus's own
    #pwm-cells/#io-channel-cells come from
    the RESOLVED parent (2 / 1), never a hardcoded value."""
    out_dir = tmp_path / "out"
    result = _run(_ACCEPT_RIG, out_dir)
    assert result.returncode == 0, result.stderr

    overlay = (out_dir / "rig-gen.overlay").read_text()
    assert overlay.count("carrier_ca_out: carrier_ca_out {") == 1
    node = overlay.split("carrier_ca_out: carrier_ca_out {")[1].split("\n\t};")[0]

    assert "#gpio-cells = <2>;" in node
    assert "gpio-map = <0 0 &ca_socket 0 0>,\n\t\t\t   <1 0 &ca_socket 1 0>;" in node

    assert "#pwm-cells = <2>;" in node
    assert "pwm-map-mask = <0xffffffff 0x00000000>;" in node
    assert "pwm-map-pass-thru = <0x00000000 0xffffffff>;" in node
    assert "pwm-map = <0 0 &ca_socket 0 0>;" in node

    assert "#io-channel-cells = <1>;" in node
    assert "io-channel-map-mask = <0xffffffff>;" in node
    assert "io-channel-map-pass-thru = <0x00000000>;" in node
    assert "io-channel-map = <1 &ca_socket 1>;" in node

    # the resolved controllers (real hardware behind the carrier) are
    # enabled, exactly as lotus_pwm's own frozen golden does for &tcc0/&adc.
    assert "&ca_pwm { status = \"okay\"; };" in overlay
    assert "&ca_adc { status = \"okay\"; };" in overlay


def test_reject_unrouted_pwm_position_is_a_loud_phys_subset(tmp_path: Path) -> None:
    """A PWM/ADC row whose parent does not
    route it is an ERROR, not a silent drop."""
    out_dir = tmp_path / "out"
    result = _run(_REJECT_RIG, out_dir)

    assert result.returncode != 0, "expected reject (ruling 2 + require-and-check)"
    assert "[phys-subset]" in result.stderr
    assert "carrier '" in result.stderr
    assert "PWM" in result.stderr
    assert "does not route it" in result.stderr
    assert "99" in result.stderr


def test_reject_require_and_check_names_both_counts_and_both_sides(tmp_path: Path) -> None:
    """require-and-check: a
    declared count disagreeing with the resolved parent's is refused,
    naming BOTH numbers and both sides -- the carrier's shield/instance
    name and the parent socket's own label -- so a reader can tell which
    to change without opening either file."""
    out_dir = tmp_path / "out"
    result = _run(_REJECT_RIG, out_dir)

    assert result.returncode != 0
    assert "carrier2" in result.stderr
    assert "ca_socket" in result.stderr
    assert "<3>" in result.stderr
    assert "<2>" in result.stderr
    assert "does not get to choose its own cell count" in result.stderr
