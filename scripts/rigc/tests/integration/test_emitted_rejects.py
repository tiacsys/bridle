# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Emitted goldens: the fixture-only rejects. HERMETIC, and INTEGRATION.

Every test here freezes python -m rigc expand's verdict + rendered
diagnostics against a SYNTHETIC fixture under tests/fixtures/, never a real
corpus rig, and none reaches analyzer.analyze (board/,
which needs a real board recipe) -- each one is rejected by loader_yml.load
alone, on YAML/schema shape (or, for test_no_board_declared_golden, by
cli.py itself, before load_board is ever asked to read a board), before any
board devicetree would even be read. Verified per test, not assumed: every
diagnostic code this module asserts on is either a `lang-*` loader finding
or the one `phys-board` "no board given" check, none of which reach
board/project.py's real edtlib.EDT build -- `phys-socket`
(test_unmapped_socket_golden) is the one exception, and it already reads
its OWN dedicated fixture board (unmapped_socket_board.dts), never this
module's shared one.

Both labels above are true at once, and the distinction is the point. These
are now genuinely HERMETIC, not merely fast: no $ZEPHYR_BASE bindings/
includes DATA, no real board .dts, no cmake/west build, nothing from
REPO_ROOT/dts, REPO_ROOT/include, or REPO_ROOT/boards/shields
(harness.assert_fixture_local is the structural proof, applied to every
test's own board/shield recipe). They are nonetheless INTEGRATION, for two
reasons that have nothing to do with hermeticity:

  - they reach the code through the FRONT DOOR, as a subprocess running the
    real CLI, and a unit reached through the CLI is being integration-tested
    whatever the test is labelled;
  - what each one pins is a REJECT -- an outcome against a scenario. A
    scenario does not exist at unit level; it is consumed by the system
    as a whole. There is no unit whose specification says "this
    assembly is unrealizable".

So hermetic-and-fast is a property of the COST axis, not of the unit
boundary. These stay exactly as they are: what they uniquely protect is the
user-facing WORDING of a system verdict, which no unit test asserts.

Some of these fixtures name a shield (adafruit_data_logger, grove_btn,
flash_click, i2c_sensor, pilot_alt_button) as ordinary instance content.
Each is now a VENDORED, byte-identical copy under tests/fixtures/boards/
shields/ (never the real boards/shields/ tree), the same pattern
test_connector_bindings.py already established for the real connector-type
bindings it needs. This module's own shield-library root
(_SHIELD_DIR, below) is that vendored directory, not boards/shields/ --
so every instance naming one of these five resolves from the fixture copy,
and every OTHER call still performs the same unconditional shield-library
scan (see test_no_board_declared_golden below, which touches no shield at
all and still incurs the same scan), just against a small, known set
instead of the whole real corpus. These five are deliberately NOT held to
production by a drift guard, unlike the vendored connector-type bindings
(test_vendored_connector_drift.py): that guard exists because those files
are the schema a real build resolves, so a stale copy would mean the
travelling test validating something the build no longer uses. These are
the opposite case -- pinned inputs whose only job is to make a diagnostic
render the same words every run. Holding them byte-identical to production
would hand every edit of a real shield the power to churn 36 byte-compared
goldens for a reason none of these tests are about. Refresh one only when
this module's own subject needs it.

_BOARD_DTS (tests/fixtures/boards/mainboards/emitted_rejects_board.dts) is
this module's own shared fixture board, typed against the same vendored
unified-connectors bindings test_connector_bindings.py reads, carrying the
two socket names (nucleo_ard, grove_d2) these fixture rigs already mate --
see that file's own comment for why a synthetic board keeps a real board's
socket-label vocabulary. Nothing in this module ever actually reads its
content (every reject fires before board reading), so this is built for
correctness/future-proofing, not because any test today needs it parsed.

test_unknown_board_golden is the sibling case that reads the opposite way:
its own fixture rig.yml is just as synthetic, but its diagnostic is reached
by NAME DISCOVERY scanning the real board tree (board/resolve.py/list_boards.py,
"no such board directory under ./boards") -- a genuine dependency on
production board-tree content, which is why it lives in
test_emitted_corpus.py instead, marked integration despite never running a
build.

Refreeze: set RIGC_REFREEZE=1 in the environment to rewrite the fixtures
under tests/goldens/<rig-name>/ instead of asserting against them. Always
inspect git diff tests/goldens before committing a refreeze -- it must
reflect an INTENTIONAL, understood behavior change, never silent drift.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from harness import (
    FIXTURES_DIR,
    GOLDENS_DIR,
    REPO_ROOT,
    RIGC_COMPILE,
    assert_fixture_local,
    freeze_or_assert,
    normalize,
    run_expand,
    zephyr_base,
)

# This module's own vendored shield library (adafruit_data_logger,
# grove_btn, flash_click, i2c_sensor, pilot_alt_button -- byte-identical
# copies of their real boards/shields/ originals, see the module docstring)
# and its own shared fixture board (nucleo_ard/grove_d2, the two socket
# names these fixture rigs already mate) -- never boards/shields/ or a
# real board .dts.
_SHIELD_DIR = FIXTURES_DIR / "boards" / "shields"
# The connector-type registry and its position-index headers, vendored like
# everything else this module reads. Threaded EXPLICITLY on every call for the
# same reason shield_dirs is: cli.py's --connector-dir and --include-dir both
# fall back to a module-relative default, so a call that omits them does not
# fail -- it silently reads the production bindings next to rigc's own source,
# and passes only in the repository those bindings live in.
_CONNECTOR_BINDINGS = FIXTURES_DIR / "dts" / "unified-connectors"
_CONNECTOR_INCLUDE = FIXTURES_DIR / "include"
_BOARD = "emitted_rejects_board"
_BOARD_DTS = FIXTURES_DIR / "boards" / "mainboards" / "emitted_rejects_board.dts"


def _run_promoted(
    target: str,
    out_dir: Path,
    board: str,
    board_dts: Path,
) -> subprocess.CompletedProcess[str]:
    """`python -m rigc expand --promote <target>`, the promoted-side
    counterpart to `run_expand`'s positional rig.yml path -- every OTHER
    reject fixture in this module compares an AUTHORED rig.yml by path,
    which `run_expand` takes no `--promote` form to reach. Shares run_
    expand's own env/cwd/timeout recipe (ZEPHYR_BASE pinned, PYTHONPATH
    set, cwd at REPO_ROOT) so a rendered diagnostic's own paths normalize
    the same way -- and, UNLIKE before this module went fixture-local,
    passes --board-dts and --shield-dir explicitly (this module's own
    _BOARD_DTS/_SHIELD_DIR), so the promotion target (grove_btn, this
    module's own vendored copy) resolves from the fixture shield library
    rather than the real one."""
    zb = zephyr_base()
    env = dict(os.environ)
    env["ZEPHYR_BASE"] = zb
    env["PYTHONPATH"] = str(REPO_ROOT / "scripts")
    cmd = [
        sys.executable,
        "-m",
        RIGC_COMPILE,
        "expand",
        "--promote",
        target,
        "--board",
        board,
        "--board-dts",
        str(board_dts),
        "--shield-dir",
        str(_SHIELD_DIR),
        # Same rule as run_expand's callers: the connector registry and its
        # headers are threaded, never left to cli.py's module-relative
        # fallback -- promotion parses a shield template and needs both.
        "--connector-dir",
        str(_CONNECTOR_BINDINGS),
        "--include-dir",
        str(_CONNECTOR_INCLUDE),
        "--out-dir",
        str(out_dir),
    ]
    return subprocess.run(
        cmd, env=env, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=60
    )


def test_route_no_via_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a wire route: that is a mapping without a via:
    key must be rejected by the LOADER with a lang-schema diagnostic --
    an ambiguous route is a loader-level authoring error, never a silently
    resolved default. No corpus rig uses wires, so only this fixture locks
    that path. Fast: the loader rejects before any board recipe is needed."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "route-no-via" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "route:{} without via: must be rejected"
    assert "[lang-schema]" in result.stderr, result.stderr
    assert "names no 'via' key" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "route-no-via"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_param_undeclared_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a params: entry
    naming a property the device did not declare via shield,params (typo
    protection) must be rejected. Fast: the loader rejects before any board
    recipe is needed."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "param-undeclared" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "an undeclared params: property must be rejected"
    assert "[lang-param]" in result.stderr, result.stderr
    assert "declares no parameter" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "param-undeclared"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_param_required_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a declared,
    REQUIRED (no default authored) parameter an instance never assigns must
    be rejected, not left as a silently-inert missing property."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "param-required" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "an unassigned required parameter must be rejected"
    assert "[lang-param]" in result.stderr, result.stderr
    assert "required" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "param-required"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_param_unknown_device_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a params: entry
    naming a device label the shield has no device for must be rejected."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "param-unknown-device" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "an unknown params: device label must be rejected"
    assert "[lang-param]" in result.stderr, result.stderr
    assert "names no device" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "param-unknown-device"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_promoted_param_undeclared_golden(tmp_path: Path) -> None:
    """A `--promote`
    target's `<device>.<prop>` assignment naming a REAL device
    (grove_btn's gb_key) but a property it never declared via
    shield,params must be rejected with the SAME diagnostic an
    authored rig.yml's params: block gets (test_param_undeclared_golden,
    above) -- confirms the undeclared-property and unknown-device checks
    fire identically for a promoted
    assignment as for an authored one, rather than assuming it from the
    shared-codepath argument (promote.promote_shield's own docstring):
    apply_params_block cannot tell a promoted document's params: block
    from an authored one, and this is what proves it, not merely states
    it.

    The target ALSO assigns gb_key's own required `zephyr,code` (the
    parameter test_param_required_golden pins, the one grove_btn's
    shield,params declares with no default authored) so that the
    required-parameter check fires nowhere in this golden --
    without it, it would fire ALONGSIDE the undeclared-property check for
    the unrelated reason
    that the instance never assigns a required parameter, which is not
    what this test exists to demonstrate. The authored-fixture control
    above stays a clean single diagnostic; this one matches it."""
    out_dir = tmp_path / "out"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = _run_promoted(
        "grove_btn:gb_key.bogus_prop=INPUT_KEY_0:gb_key.zephyr,code=INPUT_KEY_0",
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
    )

    assert result.returncode != 0, (
        "an undeclared params: property reached via promotion must be rejected"
    )
    assert "[lang-param]" in result.stderr, result.stderr
    assert "declares no parameter" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "promoted-param-undeclared"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_param_unresolvable_golden(tmp_path: Path) -> None:
    """Synthetic fixture: an assigned token
    that does not resolve against the OWNING SHIELD DEVICE's own declared
    param-includes must be rejected, naming
    the fix."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "param-unresolvable" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "an unresolvable parameter token must be rejected"
    assert "[lang-dt-include]" in result.stderr, result.stderr
    assert "does not resolve" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "param-unresolvable"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_param_shield_no_includes_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a shield declares shield,params with NO shield,param-includes
    at all, and a rig assigns a symbolic (non-literal) token to it.
    check_param_token's vocabulary is the owning device's own
    declared_param_includes, so an empty list still reaches cpp and still
    fails to resolve, naming the empty vocabulary rather than silently
    accepting."""
    out_dir = tmp_path / "out"
    fixture = FIXTURES_DIR / "boards" / "rigs" / "param-shield-no-includes"
    assert_fixture_local([_BOARD_DTS, fixture / "shields"])
    result = run_expand(
        fixture / "rig.yml",
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[fixture / "shields"],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, (
        "a symbolic token against a shield declaring no param-includes must be rejected"
    )
    assert "[lang-dt-include]" in result.stderr, result.stderr
    assert "does not resolve" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "param-shield-no-includes"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


# ---------------------------------------------------------------- qualifier rejects


def test_unknown_revision_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a --revision naming a value outside the
    declared revisions: list. Loader-level (fires before any board recipe
    is needed), like the other synthetic fixtures above."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "unknown-revision" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
        revision="99",
    )

    assert result.returncode != 0, "an undeclared revision must be rejected"
    assert "[lang-rev]" in result.stderr, result.stderr
    assert "not declared" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "unknown-revision"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_unknown_variant_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a --variant naming a value outside the
    declared variants: list."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "unknown-variant" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
        variant="nope",
    )

    assert result.returncode != 0, "an undeclared variant must be rejected"
    assert "[lang-variant]" in result.stderr, result.stderr
    assert "not declared" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "unknown-variant"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_no_default_variant_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a bare target (no --variant) against a
    declared axis with values but no declared default, naming the axis and
    listing its values."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "no-default-variant" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "no selection + no default must be rejected"
    assert "[lang-variant]" in result.stderr, result.stderr
    assert "no default variant" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "no-default-variant"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_variant_revision_collision_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a declared variant name equal to a
    declared revision id, so the constructed fragment filenames
    (<rigname>_<id>...) would be ambiguous between the two axes.
    Checked unconditionally once both axes are declared, so a bare
    invocation already triggers it."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "variant-revision-collision" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "a variant/revision id collision must be rejected"
    assert "[lang-variant]" in result.stderr, result.stderr
    assert "construct the same fragment stem" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "variant-revision-collision"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_variant_no_fragment_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a selected NON-DEFAULT axis value none of
    whose constructed fragment files (.overlay/_defconfig/.yml) exist,
    naming the files that were looked for. A value that
    changes nothing is meaningless, so it is an authoring error. The value
    must be non-default to reach this check: the declared default is
    exempt, since the base rig file is that value's content (the pilot
    family covers the exempt half, where revision 1 carries no fragment
    and is accepted)."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "variant-no-fragment" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
        variant="ghost",
    )

    assert result.returncode != 0, "a variant contributing nothing must be rejected"
    assert "[lang-variant]" in result.stderr, result.stderr
    assert "contributes nothing" in result.stderr, result.stderr
    assert "variant-no-fragment_ghost.overlay" in result.stderr, result.stderr
    assert "variant-no-fragment_ghost_defconfig" in result.stderr, result.stderr
    assert "variant-no-fragment_ghost.yml" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "variant-no-fragment"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_widened_variant_revision_collision_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a
    variant literally named 'variant_a_2' constructs the SAME fragment
    stem as variant 'variant_a' + revision '2' combined, even though
    neither axis value equals the other outright -- the same collision
    check test_variant_revision_collision_golden pins, but on a stem the
    two axes only construct TOGETHER rather than on either value alone."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "combined-fragment-collision" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "a combined-fragment stem collision must be rejected"
    assert "[lang-variant]" in result.stderr, result.stderr
    assert "construct the same fragment stem" in result.stderr, result.stderr
    assert "combined-fragment-collision_variant_a_2" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "combined-fragment-collision"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_no_such_axis_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a target naming an axis (--variant) this rig does
    not declare AT ALL gets a DISTINCT message from
    test_unknown_variant_golden's "not a
    declared member", pointing the author at the missing declaration
    itself rather than implying a typo in an existing one."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "no-such-axis" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
        variant="anything",
    )

    assert result.returncode != 0, "a qualifier against an undeclared axis must be rejected"
    assert "[lang-variant]" in result.stderr, result.stderr
    assert "declares no variants:" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "no-such-axis"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_empty_revisions_list_golden(tmp_path: Path) -> None:
    """Synthetic fixture: revisions: declared with list: [] --
    axes.parse_axis_decl's own "'list' must be a non-empty list" guard
    (lang-schema). The code path was already covered by a unit test that
    asserted only the diagnostic CODE; this pins the WORDING itself, since
    a reject-corpus stderr.txt is where this suite pins user-facing
    wording (see this file's own module docstring)."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "empty-revisions-list" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "an empty revisions: list must be rejected"
    assert "[lang-schema]" in result.stderr, result.stderr
    assert "'revisions' must be a non-empty list" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "empty-revisions-list"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


# ---------------------------------------------------------------- delta engine rejects

# A delta fragment carrying `board:` is not special: it
# is silently ignored, the same as any other unrecognized key -- board:
# left rig.yml's own grammar entirely, so documents.reject_metadata_keys
# has nothing rig.yml-shaped left to reject a delta fragment for.


def test_instances_delta_unknown_instance_golden(tmp_path: Path) -> None:
    """Synthetic fixture: an instances: delta naming an instance
    the effective topology does not have (additions are never implicit)."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "instances-delta-unknown-instance" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
        variant="b",
    )

    assert result.returncode != 0, "instances: naming an unknown instance must be rejected"
    assert "[lang-variant]" in result.stderr, result.stderr
    assert "does not have" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "instances-delta-unknown-instance"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_add_instances_already_exists_golden(tmp_path: Path) -> None:
    """Synthetic fixture: add-instances: naming an instance that
    already exists."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "add-instances-already-exists" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
        variant="b",
    )

    assert result.returncode != 0, "add-instances: naming an existing instance must be rejected"
    assert "[lang-variant]" in result.stderr, result.stderr
    assert "already exists" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "add-instances-already-exists"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_remove_instance_drift_golden(tmp_path: Path) -> None:
    """Synthetic fixture: remove-instances: naming an absent
    instance. variant 'b' removes 'logger' first; the family-wide revision
    '2' delta then tries removing it again -- the message must NAME the
    variant that already removed it, so drift cannot hide."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "remove-instance-drift" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
        variant="b",
        revision="2",
    )

    assert result.returncode != 0, "remove-instances: naming an absent instance must be rejected"
    assert "[lang-rev]" in result.stderr, result.stderr
    assert "does not exist" in result.stderr, result.stderr
    assert "variant 'b' already removed it" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "remove-instance-drift"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_remove_wire_missing_golden(tmp_path: Path) -> None:
    """Synthetic fixture: remove-wires: naming an endpoint pair
    that does not exist (the real wire is x.dl_sq -> y.dl_led1; the delta
    tries x.dl_sq -> y.dl_led2 -- dl_led2 is a real label, just the wrong
    endpoint)."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "remove-wire-missing" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
        variant="b",
    )

    assert result.returncode != 0, "remove-wires: naming a nonexistent pair must be rejected"
    assert "[lang-variant]" in result.stderr, result.stderr
    assert "remove-wires:" in result.stderr, result.stderr
    assert "does not exist" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "remove-wire-missing"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_restate_check_golden(tmp_path: Path) -> None:
    """Synthetic fixture: the params restate-check. variant b
    does not change sensor_1's shield but supplies params: for it,
    forgetting to restate vnd,threshold -- which wholesale replace would
    otherwise silently revert to the shield's authored default."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "restate-check" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        variant="b",
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "an un-restated optional parameter must be rejected"
    assert "[lang-param]" in result.stderr, result.stderr
    assert "without restating" in result.stderr, result.stderr
    assert "vnd,threshold" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "restate-check"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_revision_crosses_variant_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a family-wide revision whose params
    names a device the POST-VARIANT topology does not have (variant hpm
    substituted sensor_1's shield, so 'rf_sensor' no longer exists) --
    unavoidable by construction, so the error must name the variant."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "revision-crosses-variant" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        variant="hpm",
        revision="2",
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "a revision crossing a variant's shield swap must be rejected"
    assert "[lang-param]" in result.stderr, result.stderr
    assert "names no device 'rf_sensor'" in result.stderr, result.stderr
    assert "because of variant 'hpm'" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "revision-crosses-variant"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_dotted_revision_no_fragment_golden(tmp_path: Path) -> None:
    """Synthetic fixture: hwmv2's revision dot-normalization -- a dotted
    revision id ('1.5') constructs a
    fragment filename with the dot replaced by an underscore
    (..._1_5_defconfig), never the literal dot. The same
    missing-fragment check test_variant_no_fragment_golden pins fires
    since no
    such fragment exists, naming the NORMALIZED filename -- proof the
    normalization happened, not just that the check still works."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "dotted-revision-no-fragment" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
        revision="1.5",
    )

    assert result.returncode != 0, "a dotted revision contributing nothing must be rejected"
    assert "[lang-rev]" in result.stderr, result.stderr
    assert "dotted-revision-no-fragment_1_5_0_defconfig" in result.stderr, result.stderr
    assert "dotted-revision-no-fragment_1.5_defconfig" not in result.stderr, (
        "the dot must be NORMALIZED to an underscore, per hwmv2's own "
        f"convention, not left literal\n{result.stderr}"
    )

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "dotted-revision-no-fragment"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


# ---------------------------------------------------------------- shield revisions


def test_shield_undeclared_revision_golden(tmp_path: Path) -> None:
    """Synthetic fixture: shield: <name>@<rev> naming a revision
    shield.yml does not declare. i2c_sensor (a production shield)
    declares "1"/"2" only. Loader-level
    (shield resolution fires before any board recipe is needed), like the
    other synthetic fixtures above."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "shield-undeclared-revision" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "an undeclared shield revision must be rejected"
    assert "[lang-rev]" in result.stderr, result.stderr
    assert "is not declared" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "shield-undeclared-revision"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_shield_no_revisions_declared_golden(tmp_path: Path) -> None:
    """Synthetic fixture: @rev against a shield declaring no revisions: at
    all -- the shield-side analogue of the rig axis "declares no such
    axis" wording test_no_such_axis_golden pins, mirrored via
    _resolve_axis's own
    three failure shapes. flash_click is a production shield with no
    revisions: block."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "shield-no-revisions-declared" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, (
        "an @rev against a shield declaring no revisions: must be rejected"
    )
    assert "[lang-rev]" in result.stderr, result.stderr
    assert "declares no revisions: at all" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "shield-no-revisions-declared"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_shield_missing_fragment_golden(tmp_path: Path) -> None:
    """Synthetic fixture: the missing non-default shield-revision fragment
    check -- the shield-side analogue of test_variant_no_fragment_golden's
    check, same default exemption
    (the default MAY carry a fragment, it just must not be REQUIRED to).
    rev_fixture (fixture-only shield) declares revision "2" but ships
    neither rev_fixture_2.shield nor rev_fixture_2.conf."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "shield-missing-fragment" / "rig.yml"
    assert_fixture_local(
        [_BOARD_DTS, FIXTURES_DIR / "boards" / "rigs" / "shield-missing-fragment" / "shields"]
    )
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[FIXTURES_DIR / "boards" / "rigs" / "shield-missing-fragment" / "shields"],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "a shield revision contributing nothing must be rejected"
    assert "[lang-rev]" in result.stderr, result.stderr
    assert "contributes nothing" in result.stderr, result.stderr
    assert "rev_fixture_2.shield" in result.stderr, result.stderr
    assert "rev_fixture_2.conf" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "shield-missing-fragment"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_shield_revision_param_invariant_golden(tmp_path: Path) -> None:
    """Proves the per-stage parameter invariant claim
    BY TEST rather than by inspection: a shield
    REVISION (not a rig delta) introduces a new required parameter
    (paramrev_2.shield adds shield,params with no default to pr_dev), and
    _check_param_invariant -- already re-checked fresh after resolving
    each instance's shield, with no special case for a shield-revision-
    introduced requirement -- must still reject an instance that never
    assigns it."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "shield-revision-param-invariant" / "rig.yml"
    assert_fixture_local(
        [
            _BOARD_DTS,
            FIXTURES_DIR / "boards" / "rigs" / "shield-revision-param-invariant" / "shields",
        ]
    )
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[
            FIXTURES_DIR / "boards" / "rigs" / "shield-revision-param-invariant" / "shields"
        ],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, (
        "a shield-revision-introduced required parameter must be rejected when unassigned"
    )
    assert "[lang-param]" in result.stderr, result.stderr
    assert "declares 'vnd,threshold' as" in result.stderr, result.stderr
    assert "required" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "shield-revision-param-invariant"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_missing_content_file_golden(tmp_path: Path) -> None:
    """Synthetic fixture: metadata that resolves with NO content file beside
    it. The content file is REQUIRED, and the distinction the diagnostic has
    to keep is between a rig whose instances: list is EMPTY (legal, and how
    the axis-rule fixtures are written) and a rig whose content file is
    absent (an authoring mistake). The message names the path that was
    constructed from the rig's own identity, since that name is never
    parsed from the folder and is therefore not obvious from the layout."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "missing-content-file" / "rig.yml"
    assert_fixture_local([_BOARD_DTS, _SHIELD_DIR, _CONNECTOR_BINDINGS, _CONNECTOR_INCLUDE])
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "a missing content file must be rejected"
    assert "[lang-content]" in result.stderr, result.stderr
    assert "missing-content-file.yml" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "missing-content-file"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_shield_bad_revisions_block_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a malformed revisions: block in a SHIELD's own
    shield.yml is blamed on that shield, BY NAME. One parser serves both
    rig.yml and shield.yml (the same {default:, list: []} shape, learned
    once), so it has to be told which file it is reading -- otherwise every
    shield.yml shape defect reports "rig revisions: ...", blaming the rig for
    a declaration it has no part in and naming no shield at all.

    Its own exclusive shield-library scan root, because a shape defect is
    reported at library-scan time for every folder scanned: sharing a root
    with any other shield would add this diagnostic to every other
    fixture's output too."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "shield-bad-revisions-block" / "rig.yml"
    assert_fixture_local(
        [_BOARD_DTS, FIXTURES_DIR / "boards" / "rigs" / "shield-bad-revisions-block" / "shields"]
    )
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[FIXTURES_DIR / "boards" / "rigs" / "shield-bad-revisions-block" / "shields"],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "a malformed shield.yml revisions: block must be rejected"
    assert "[lang-schema]" in result.stderr, result.stderr
    assert "shield 'badyml_fixture' revisions:" in result.stderr, result.stderr
    assert "rig revisions:" not in result.stderr, (
        f"a shield.yml defect must not be blamed on the rig\n{result.stderr}"
    )

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "shield-bad-revisions-block"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_shield_node_name_mismatch_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a .shield template whose node name disagrees with
    the folder it lives in. Shield.name remains the DT node name, but the
    RESOLUTION key is the folder basename -- it is what <name>.shield
    discovery constructs, what shield.yml is read beside, and what an
    instance's shield: reference carries into RIG_SHIELDS. The two must
    agree, nothing else in the tree enforces it, and resolving to whichever
    single shield the file happened to define would leave the folder name
    and the node name disagreeing about what was built."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "shield-node-name-mismatch" / "rig.yml"
    assert_fixture_local(
        [_BOARD_DTS, FIXTURES_DIR / "boards" / "rigs" / "shield-node-name-mismatch" / "shields"]
    )
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[FIXTURES_DIR / "boards" / "rigs" / "shield-node-name-mismatch" / "shields"],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "a .shield node name not matching its folder must be rejected"
    assert "[lang-shield-name]" in result.stderr, result.stderr
    assert "misnamed_fixture" in result.stderr, result.stderr
    assert "other_name" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "shield-node-name-mismatch"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_shield_template_missing_file_golden(tmp_path: Path) -> None:
    """Synthetic fixture: shield.yml declares `template: true` for a name with no
    matching `<name>.shield` beside it. The folder's own basename-keyed
    discovery never looks at this name on its own; this check exists
    because the folder's authoring intent -- this name
    IS meant to be a rig template -- is known by name once shield.yml
    says so. Its own exclusive shield-library scan root, because the
    defect is reported at library-scan time for every folder scanned."""
    out_dir = tmp_path / "out"
    fixture = FIXTURES_DIR / "boards" / "rigs" / "shield-template-missing-file"
    assert_fixture_local([_BOARD_DTS, fixture / "shields"])
    result = run_expand(
        fixture / "rig.yml",
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[fixture / "shields"],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, (
        "a template: true entry with no matching <name>.shield must be rejected"
    )
    assert "[lang-shield-template]" in result.stderr, result.stderr
    assert "ghost_template" in result.stderr, result.stderr
    assert "does not exist" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "shield-template-missing-file"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_shield_plural_node_name_mismatch_golden(tmp_path: Path) -> None:
    """Synthetic fixture: the DECLARED-name half of the shield-name-
    mismatch check -- a `shields:` entry's own `name:`
    (decl_beta) disagrees with its `<name>.shield` node name (wrong_node),
    in a folder that ALSO declares a well-formed sibling entry
    (decl_alpha) in the same list, so the mismatch is blamed on decl_beta
    alone. test_shield_node_name_mismatch_golden above is the sibling
    fixture for the folder-name half, which must keep working unchanged."""
    out_dir = tmp_path / "out"
    fixture = FIXTURES_DIR / "boards" / "rigs" / "shield-plural-node-name-mismatch"
    assert_fixture_local([_BOARD_DTS, fixture / "shields"])
    result = run_expand(
        fixture / "rig.yml",
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[fixture / "shields"],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, (
        "a shields: entry's declared name not matching its own .shield node name must be rejected"
    )
    assert "[lang-shield-name]" in result.stderr, result.stderr
    assert "decl_beta" in result.stderr, result.stderr
    assert "wrong_node" in result.stderr, result.stderr
    assert "shield.yml itself declares" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "shield-plural-node-name-mismatch"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_shield_plural_duplicate_name_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a duplicate name WITHIN one `shields:` list --
    newly reachable only because plurality lets one list declare more
    than one name at all (a duplicate ACROSS folders/roots stays the
    existing silent last-wins policy, out of scope; this is the
    in-scope, single-list case). No
    instance references either name -- the defect is scan-time and
    unconditional, so nothing needs to reference it to trigger."""
    out_dir = tmp_path / "out"
    fixture = FIXTURES_DIR / "boards" / "rigs" / "shield-plural-duplicate-name"
    assert_fixture_local([_BOARD_DTS, fixture / "shields"])
    result = run_expand(
        fixture / "rig.yml",
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[fixture / "shields"],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "a name repeated within one shields: list must be rejected"
    assert "[lang-schema]" in result.stderr, result.stderr
    assert "dup_name" in result.stderr, result.stderr
    assert "declared more than once" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "shield-plural-duplicate-name"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_shield_plural_not_a_list_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a `shields:` block authored one dash short, so
    it parses as a mapping and yields no entries at all. The folder ships
    a `never_declared.shield` beside it, so nothing else in the scan can
    tell the folder meant to declare a shield -- which is exactly why a
    silent drop here would surface only much later, as an unresolvable
    shield: reference blaming the rig instead of this file."""
    out_dir = tmp_path / "out"
    fixture = FIXTURES_DIR / "boards" / "rigs" / "shield-plural-not-a-list"
    assert_fixture_local([_BOARD_DTS, fixture / "shields"])
    result = run_expand(
        fixture / "rig.yml",
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[fixture / "shields"],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "a shields: block that is not a list must be rejected"
    assert "[lang-schema]" in result.stderr, result.stderr
    assert "must be a list" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "shield-plural-not-a-list"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_shield_plural_missing_name_golden(tmp_path: Path) -> None:
    """Synthetic fixture: a `shields:` entry with no `name:` key at all --
    rigc parses shield.yml with its own `parse_marked`, never jsonschema,
    so a malformed entry is this code's own problem to catch. The
    well-formed sibling entry
    (has_name) in the same list proves the malformed one is dropped, not
    fatal to the whole document."""
    out_dir = tmp_path / "out"
    fixture = FIXTURES_DIR / "boards" / "rigs" / "shield-plural-missing-name"
    assert_fixture_local([_BOARD_DTS, fixture / "shields"])
    result = run_expand(
        fixture / "rig.yml",
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[fixture / "shields"],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "a shields: entry with no name: must be rejected"
    assert "[lang-schema]" in result.stderr, result.stderr
    assert "required key 'name' is missing" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "shield-plural-missing-name"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


# ---------------------------------------------------------------- board-per-variant

# A variants: entry declares nothing but its own name, so a variant
# restating nothing simply contributes nothing -- the case
# test_variant_no_fragment_golden covers.


def test_unmapped_socket_golden(tmp_path: Path) -> None:
    """Synthetic fixture: an instance naming a socket the board does not
    have -- it passes through SocketBinding's own lookup-else-identity
    (an empty binding: nothing populates one), and the board simply has
    no socket by that
    literal name (the pre-existing phys-socket diagnostic).

    The board is incidental to this: any board with any socket set
    demonstrates the same "unresolved name falls through to a real-socket
    lookup" property. So this uses a mainboards/ fixture board (built
    against the fixture connector type under fixtures/dts/connectors/,
    never a real one) instead of a real corpus board -- no plain build,
    hence unmarked like fixtures/boards/rigs/not-rig-enabled's sibling
    test. board is INJECTED (the harness, not a rig.yml declaration --
    no rig.yml can declare a board), matching its own fixture .dts's
    name."""
    fixture = FIXTURES_DIR / "boards" / "rigs" / "unmapped-socket"
    board_dts = FIXTURES_DIR / "boards" / "mainboards" / "unmapped_socket_board.dts"
    bindings_dirs = [FIXTURES_DIR / "dts" / "connectors"]
    include_dirs = [FIXTURES_DIR / "include"]
    # adafruit_data_logger (the instance's own shield: reference) now
    # resolves from this module's own vendored copy too -- _SHIELD_DIR,
    # not boards/shields/ -- even though this test's own subject (an
    # unmapped socket NAME) has nothing to do with shields.
    assert_fixture_local([board_dts, *bindings_dirs, *include_dirs, _SHIELD_DIR])
    out_dir = tmp_path / "out"
    result = run_expand(
        fixture / "rig.yml",
        out_dir,
        board="unmapped_socket_board",
        board_dts=board_dts,
        bindings_dirs=bindings_dirs,
        include_dirs=include_dirs,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
    )

    assert result.returncode != 0, (
        "an instance socket name absent from the declared map must be "
        "rejected against the board's own socket set"
    )
    assert "[phys-socket]" in result.stderr, result.stderr
    assert "no socket 'other'" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "unmapped-socket"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


# ---------------------------------------------------------------- board resolution

# upstream's revision: shape IS mapping entries with name:.
#
# binding.resolve_board carries no per-variant-board coherence rules: no
# rig.yml can declare a board at all (top-level or per-variant), so
# resolve_board itself is a one-line injection (loader/binding.py), with
# no declaration left to be incoherent about. A content file naming
# `board:` or `sockets:` is just an unrecognized key, silently ignored
# like any other -- documents.reject_metadata_keys has nothing rig.yml-
# only left to police on the content side either.


def test_no_board_declared_golden(tmp_path: Path) -> None:
    """A rig with no board INJECTED (no --board, and no declaration
    exists to fall back to) is rejected: a rig has no board of its own to
    build against. The diagnostic lives in cli.py, not binding.py
    (binding.resolve_board never rejects; the loader assembles a
    boardless topology just fine), right before cli.py would otherwise
    ask load_board to read a board literally named "" -- so this
    fixture's rig.yml carries no `board:` key at all (there is nothing
    left to declare), and the diagnostic is phys-board, unanchored, the
    same family every other board-reading diagnostic uses, rather than a
    lang-schema finding anchored at a rig.yml line."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "no-board-declared" / "rig.yml"
    assert_fixture_local([_SHIELD_DIR])
    result = run_expand(
        rig_yml,
        out_dir,
        shield_dirs=[_SHIELD_DIR],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, "a rig with no board injected at all must be rejected"
    assert "[phys-board]" in result.stderr, result.stderr
    assert "no board given" in result.stderr, result.stderr

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "no-board-declared"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))


def test_shield_revisions_mapping_entry_golden(tmp_path: Path) -> None:
    """The identical mapping-entry rejection, raised from a SHIELD's own
    shield.yml revisions: list rather than a rig's: blamed on the shield,
    BY NAME, since the axis parser is shared with rig.yml and would
    otherwise report "rig revisions: ...", naming no shield at all.

    NOT retired alongside test_revision_mapping_entry_golden (rig.yml's
    own axis, which DID adopt upstream's mapping-entry shape): a shield's
    revisions: axis stays on its PRE-hwmv2 shape permanently -- the
    pinned zephyr tree carries its own schema restricting a shield.yml
    revisions: block to exactly {default:, list: []}
    (`loader.axes.parse_legacy_revision_decl`'s own docstring has the
    measured reason), so a mapping entry here is still exactly as illegal
    as it always was. Its own fixture shields root, because the defect is
    reported at library-scan time for every folder scanned."""
    out_dir = tmp_path / "out"
    rig_yml = FIXTURES_DIR / "boards" / "rigs" / "shield-revisions-mapping-entry" / "rig.yml"
    assert_fixture_local(
        [
            _BOARD_DTS,
            FIXTURES_DIR / "boards" / "rigs" / "shield-revisions-mapping-entry" / "shields",
        ]
    )
    result = run_expand(
        rig_yml,
        out_dir,
        board=_BOARD,
        board_dts=_BOARD_DTS,
        shield_dirs=[
            FIXTURES_DIR / "boards" / "rigs" / "shield-revisions-mapping-entry" / "shields"
        ],
        connector_dirs=[_CONNECTOR_BINDINGS],
        include_dirs=[_CONNECTOR_INCLUDE],
    )

    assert result.returncode != 0, (
        "a mapping entry in a shield's own revisions: list must be rejected"
    )
    assert "[lang-schema]" in result.stderr, result.stderr
    assert "shield 'mapentry_fixture' revisions:" in result.stderr, result.stderr
    assert "legal only in a rig's variants: list" in result.stderr, result.stderr
    assert "rig revisions:" not in result.stderr, (
        f"a shield.yml defect must not be blamed on the rig\n{result.stderr}"
    )

    zb = zephyr_base()
    golden_dir = GOLDENS_DIR / "shield-revisions-mapping-entry"
    freeze_or_assert(golden_dir / "exit_code", f"{result.returncode}\n")
    freeze_or_assert(golden_dir / "stderr.txt", normalize(result.stderr, zb))
