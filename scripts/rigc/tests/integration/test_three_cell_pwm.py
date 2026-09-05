# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""3-cell PWM controllers, end to end. HERMETIC and non-build, mirroring
test_carrier_analog_passthrough.py's own shape: purpose-built fixture
boards (three_cell_pwm_board.dts and two deliberately-bad siblings)
declare real pwm-map nexuses a shape none of the real board sockets in
the corpus happen to carry, which is why this witness needs
fixture boards rather than a real nucleo_f401re/frdm_k64f.

Five rigs, each driven through the real CLI (`python -m rigc expand`):

  three-cell-pwm-plain (ACCEPT) -- a plain shield mates the board's own
    3-cell PWM socket directly, authoring a nonzero PWM flags value.
    Proves a four-word pwms property is emitted, and that a nonzero
    flags word is accepted on a 3-cell socket.

  three-cell-pwm-carrier (ACCEPT) -- the same nonzero-flags claim,
    mated through a pure-copper carrier's exposed socket instead.
    Proves the synthesized nexus resolves at
    #pwm-cells = <3>, with mask/pass-thru/row shapes derived from the
    resolved parent, and that the same nonzero flags word is accepted
    through a carrier too.

  three-cell-pwm-2cell-reject (REJECT) -- the identical nonzero-flags
    claim, mated against the SAME board's 2-cell PWM socket instead.
    Proves the reject half of the accept/reject pair above: the pair is
    the whole point, and one without the other proves nothing.

  three-cell-pwm-mismatch (REJECT) -- a board whose one socket disagrees
    with its own parent controller's cell count (3 vs 2), both
    individually supported. Proves the mismatch is refused at
    board-load time.

  three-cell-pwm-unsupported (REJECT) -- a board whose one socket and
    parent controller agree with EACH OTHER at a count (4) outside the
    supported set {2, 3}. Proves the existing
    "not supported yet" wording still applies to a genuinely unsupported
    count.
"""

from __future__ import annotations

from pathlib import Path

from harness import FIXTURES_DIR, assert_fixture_local, run_expand

_CONNECTOR_BINDINGS = FIXTURES_DIR / "dts" / "three-cell-pwm-connectors"
_CONNECTOR_INCLUDE = FIXTURES_DIR / "include"
_BOARDS_DIR = FIXTURES_DIR / "boards" / "mainboards"
_RIGS_DIR = FIXTURES_DIR / "boards" / "rigs"

_GOOD_BOARD = _BOARDS_DIR / "three_cell_pwm_board.dts"
_MISMATCH_BOARD = _BOARDS_DIR / "three_cell_pwm_mismatch_board.dts"
_UNSUPPORTED_BOARD = _BOARDS_DIR / "three_cell_pwm_unsupported_board.dts"


def _run(rig_dir_name: str, board_dts: Path, board_name: str, out_dir: Path, shields: bool = True):
    fixture_dir = _RIGS_DIR / rig_dir_name
    shield_dirs = [fixture_dir / "shields"] if shields else []
    assert_fixture_local([board_dts, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE] + shield_dirs)
    return run_expand(
        fixture_dir / "rig.yml",
        out_dir,
        board=board_name,
        shield_dirs=shield_dirs,
        board_dts=board_dts,
        bindings_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
        connector_dirs=[_CONNECTOR_BINDINGS],
    )


# ----------------------------------------------------------- plain shield (accept)


def test_accept_plain_shield_on_3cell_socket_emits_four_word_pwms(tmp_path: Path) -> None:
    """A 3-cell PWM controller resolves end to
    end, proven by an emitted overlay containing a four-word pwms
    property (position, period, flags -- FOUR words counting the
    phandle). The flags word is nonzero,
    carried rather than refused, because the socket itself is 3-cell."""
    out_dir = tmp_path / "out"
    result = _run("three-cell-pwm-plain", _GOOD_BOARD, "three_cell_pwm_fixture_board", out_dir)

    assert result.returncode == 0, (
        f"three_cell_pwm_plain: expected accept\n--- stderr ---\n{result.stderr}"
    )

    overlay = (out_dir / "rig-gen.overlay").read_text()
    assert "pwms = <&tc_socket3 0 20000000 0x1>;" in overlay


# ----------------------------------------------------------- through a carrier


def test_accept_through_carrier_synthesizes_a_3cell_nexus(tmp_path: Path) -> None:
    """The same claim resolves through a
    carrier-exposed socket, with the synthesized nexus's own
    #pwm-cells/mask/pass-thru/row shape all derived from the RESOLVED
    parent's cell count (3), never a hardcoded 2 --
    confirmed here by an emitted overlay rather than reasoning about it.
    The row is SEVEN words: 3 child (pos, 0, 0) + phandle + 3 parent
    (channel, 0, 0)."""
    out_dir = tmp_path / "out"
    result = _run("three-cell-pwm-carrier", _GOOD_BOARD, "three_cell_pwm_fixture_board", out_dir)

    assert result.returncode == 0, (
        f"three_cell_pwm_carrier: expected accept\n--- stderr ---\n{result.stderr}"
    )

    overlay = (out_dir / "rig-gen.overlay").read_text()
    assert overlay.count("carrier_tc_out: carrier_tc_out {") == 1
    node = overlay.split("carrier_tc_out: carrier_tc_out {")[1].split("\n\t};")[0]

    assert "#pwm-cells = <3>;" in node
    assert "pwm-map-mask = <0xffffffff 0x00000000 0x00000000>;" in node
    assert "pwm-map-pass-thru = <0x00000000 0xffffffff 0xffffffff>;" in node
    assert "pwm-map = <0 0 0 &tc_socket3 0 0 0>;" in node

    # the claim itself resolves through the synthesized nexus, carrying
    # the nonzero flags word exactly like the plain rig does directly.
    assert "pwms = <&carrier_tc_out 0 20000000 0x1>;" in overlay

    # the resolved real controller (behind the carrier) is enabled.
    assert '&tc_pwm3 { status = "okay"; };' in overlay


# ----------------------------------------------------------- 2-cell socket (reject)


def test_reject_nonzero_flags_on_a_2cell_socket_names_socket_and_count(tmp_path: Path) -> None:
    """The IDENTICAL nonzero-flags
    claim, on the SAME board's 2-cell socket, is still refused --
    analyzer/gpio.py's _collect_channel, now conditional on the socket's
    own pwm_cells rather than unconditional. The refusal names the
    socket and its cell count."""
    out_dir = tmp_path / "out"
    result = _run(
        "three-cell-pwm-2cell-reject", _GOOD_BOARD, "three_cell_pwm_fixture_board", out_dir
    )

    assert result.returncode != 0, "nonzero PWM flags on a 2-cell socket must be rejected"
    assert "[phys-function]" in result.stderr
    assert "PWM flags" in result.stderr
    assert "tc_socket2" in result.stderr
    assert "2-cell" in result.stderr


# ----------------------------------------------------------- child/parent mismatch


def test_reject_child_parent_cell_count_mismatch_names_both_counts(tmp_path: Path) -> None:
    """A socket declaring #pwm-cells
    = <3> whose own pwm-map's target controller declares <2> is refused
    at board-load time, naming both counts. No shield/instance is
    needed: board/project.py's project_edt walks every socket,* node
    unconditionally."""
    out_dir = tmp_path / "out"
    result = _run(
        "three-cell-pwm-mismatch",
        _MISMATCH_BOARD,
        "three_cell_pwm_mismatch_fixture_board",
        out_dir,
        shields=False,
    )

    assert result.returncode != 0, "a child/parent cell-count mismatch must be rejected"
    assert "[phys-board]" in result.stderr
    assert "tc_socket_mismatch" in result.stderr
    assert "<3>" in result.stderr and "<2>" in result.stderr
    assert "must equal" in result.stderr


# ----------------------------------------------------------- unsupported cell count


def test_reject_unsupported_cell_count_keeps_old_style_wording(tmp_path: Path) -> None:
    """A 4-cell PWM parent (self-consistent with
    its own socket, but outside the supported set {2, 3}) is still
    refused with the existing phys-board wording -- only the accepted
    set of cell counts widens."""
    out_dir = tmp_path / "out"
    result = _run(
        "three-cell-pwm-unsupported",
        _UNSUPPORTED_BOARD,
        "three_cell_pwm_unsupported_fixture_board",
        out_dir,
        shields=False,
    )

    assert result.returncode != 0, "an unsupported PWM cell count must be rejected"
    assert "[phys-board]" in result.stderr
    assert "tc_socket4" in result.stderr
    assert "<4>" in result.stderr
    assert "supports only" in result.stderr
