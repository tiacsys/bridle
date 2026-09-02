# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Generic harness plumbing for the rigc integration tests --
path discovery (self-locating -- no workspace-name literals), the
rigc subprocess runner, normalization, and the freeze/assert
primitives.

This module carries nothing corpus-tethered: no boards/rigs/,
boards/shields/, or boards/extend/ content, and no knowledge of any one
rig or shield. tests/integration/'s own test modules import it directly
(`from harness import ...`); tests/integration_stay/'s corpus.py imports
it too, and layers the corpus table, the board catalog, and the
cached-plain-build machinery on top (see corpus.py's own docstring for
that half). conftest.py in this directory is a thin re-export of this
module, kept only because pytest wants a conftest.py in the directory --
no test module should import from it directly any more, since a sibling
conftest.py under tests/integration_stay/ would otherwise silently
cross-wire under Python's plain `from conftest import ...` idiom (both
directories carry no __init__.py, so sys.modules["conftest"] is
first-wins across them).
"""

from __future__ import annotations

import difflib
import logging
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

_LOGGER = logging.getLogger(__name__)

# This file lives in tests/integration/, alongside
# the frozen suite's other own modules; TESTS_DIR is tests/ itself, one
# level up, where fixtures/ and goldens/ actually sit (siblings of
# integration/, not children of it -- fixtures/ in particular must land at
# exactly this depth for diag.anchor_path()'s "scripts/<module>/"-relative
# rendering to reproduce every frozen anchor line byte-for-byte).
TESTS_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = TESTS_DIR.parents[2]  # scripts/rigc/tests -> the repo root
GOLDENS_DIR = TESTS_DIR / "goldens"
FIXTURES_DIR = TESTS_DIR / "fixtures"


def assert_fixture_local(paths: list[Path | str]) -> None:
    """Structural proof of hermeticity for a test that claims to need no
    real Zephyr tree and no repo-production devicetree content: every
    path it hands to board/edtlib as a --board-dts/--bindings-dir/
    --include-dir resolves under FIXTURES_DIR, never under $ZEPHYR_BASE
    or REPO_ROOT/dts or REPO_ROOT/include.

    $ZEPHYR_BASE may still be SET for such a test (it locates the
    devicetree package itself, which this workspace's zephyr branch
    patches -- board.edt_build.ensure_devicetree_on_path -- so it is not
    something a test can or should route around); what this asserts is
    that none of its DATA leaks in. Checking the caller's own recipe
    inputs (rather than, say, the ABSENCE of $ZEPHYR_BASE) is what makes
    "hermetic" a property of what the test actually reads, not an
    accident of how it was invoked."""
    for p in paths:
        resolved = Path(p).resolve()
        assert str(resolved) == str(FIXTURES_DIR) or str(resolved).startswith(
            str(FIXTURES_DIR) + os.sep
        ), (
            f"{resolved} is outside {FIXTURES_DIR} -- a test asserting "
            "hermeticity must reference only its own fixture-tree paths"
        )


def _find_west_topdir(start: Path) -> Path:
    """Walk upward from start to the west workspace root (the directory
    holding .west/) — self-locating, no hardcoded workspace-name literal."""
    for candidate in (start, *start.parents):
        if (candidate / ".west").is_dir():
            return candidate
    raise RuntimeError(f"no .west/ found above {start} — is this a west workspace?")


WEST_TOPDIR = _find_west_topdir(REPO_ROOT)
_VENV_WEST = WEST_TOPDIR / ".venv" / "bin" / "west"
WEST_EXE = str(_VENV_WEST) if _VENV_WEST.is_file() else "west"

# RIGC_REFREEZE=1 rewrites goldens instead of asserting against them (both
# emitted and resolved). Always inspect git diff tests/goldens after a
# refreeze — it must reflect an INTENTIONAL, understood behavior change,
# never silent drift.
REFREEZE = bool(os.environ.get("RIGC_REFREEZE"))

# RIGC_COMPILE: the module knob -- the
# Python module name of the CLI under test, read ONCE here from the
# environment (same name as cmake/modules/dts.cmake's own cache variable of the same
# name, deliberately: most subprocesses this suite launches inherit this
# process's environment wholesale, e.g. via env=dict(os.environ), so that
# cache variable's own environment fallback picks up the SAME value without
# every call site needing to thread an explicit -D). rigc is the only
# module this name may resolve to today.
RIGC_COMPILE = os.environ.get("RIGC_COMPILE", "rigc")


def subprocess_timeout(default: int) -> int | None:
    """The default for every long-running subprocess.run() timeout across
    the integration tests, overridable via RIGC_SUBPROCESS_TIMEOUT (seconds;
    0 disables the timeout). subprocess.run's timeout clock runs in the
    pytest process and is oblivious to a debugger paused inside the child --
    past the timeout it kills that child regardless, ending the debug
    session out from under you. Set RIGC_SUBPROCESS_TIMEOUT=0 (e.g. via a
    project-local .env picked up by nvim-dap-python) while debugging into a
    subprocess.run child. Not applied to the short dts_equiv.py comparisons,
    which carry no timeout of their own."""
    raw = os.environ.get("RIGC_SUBPROCESS_TIMEOUT")
    if not raw:
        return default
    value = int(raw)
    return value if value > 0 else None


# rigc's workdir is <--out-dir>/rigc-generated (cli.WORKDIR_NAME), so
# the leading part varies per run -- a pytest tmp_path here, a real build
# directory under cmake. Match the whole absolute path up to and including
# the fixed trailing component: anchoring on "rigc-generated" alone would
# leave the run-specific prefix in the text, and matching a bare
# "/generated" would collide with zephyr's own include/generated.
_WORKDIR_RE = re.compile(r"/[^\s]*rigc-generated")

# A resolved zephyr.dts's own DT provenance comments (/* in PATH:LINE */,
# /* node 'X' defined in PATH:LINE */) render PATH relative to the build's
# cwd (WEST_TOPDIR) — e.g. ../../../tmp/pytest-of-<user>/pytest-52/
# test_resolved_accept_zephyr_dt0/build/rig/rig-gen.overlay:25 — which embeds
# pytest's OWN per-session tmp dir (tmp_path, a fresh directory every test
# run: test_resolved_corpus._run_build builds into tmp_path / "build").
# Byte-freezing that raw text would make every refreeze session rewrite
# every resolved golden on this fragment alone, with no content change at
# all. (?:\.\./)+ (not a fixed count) tolerates whatever depth WEST_TOPDIR
# sits at under the filesystem root on a given machine.
_DTS_BUILD_PROVENANCE_RE = re.compile(
    r"(?:\.\./)+tmp/pytest-of-[^/\s]+/pytest-\d+/[^/\s]+/build/(rig/[^:\s*]+):(\d+)"
)


def normalize_dts_provenance(text: str) -> str:
    """Replace a resolved zephyr.dts's pytest-tmp-dir-dependent provenance
    comment paths with a stable placeholder, keeping the meaningful
    generated-file-relative part (rig/<file>:<line>) intact — comments
    only, so dts_equiv.py's structural comparison (which ignores comments)
    is unaffected either way; this exists purely so a refreeze's diff shows
    real content changes, not tmp-path churn."""
    return _DTS_BUILD_PROVENANCE_RE.sub(r"<RIGC_BUILD>/\1:\2", text)


def zephyr_base() -> str:
    """The zephyr tree rigc / dts_equiv.py need, from $ZEPHYR_BASE."""
    value = os.environ.get("ZEPHYR_BASE")
    if not value:
        pytest.fail(
            "ZEPHYR_BASE is not set — export it (the zephyr-rigs tree), the "
            "same way scripts/check.sh requires."
        )
    return value


def normalize(text: str, zb: str | None) -> str:
    """Replace machine-/run-specific absolute paths with stable placeholders
    before freezing/comparing: rigc's own temp workdir,
    $ZEPHYR_BASE, and the repo root (in that order — repo root and zephyr
    base can each be a prefix of the other under a shared workspace topdir, so
    the more specific substitutions must land first). This function only
    replaces machine-specific paths; WHETHER what is left compares
    byte-exact or by contract is freeze_or_assert's decision, per artifact.

    zb is None for a golden-comparing test that needs no real Zephyr tree at
    all (a hermetic fixture) -- that one substitution is skipped rather than
    forcing every such caller through zephyr_base()'s hard failure just to
    normalize output that never contained a $ZEPHYR_BASE path to begin
    with. Every other substitution still applies unconditionally."""
    text = _WORKDIR_RE.sub("<RIGC_WORKDIR>", text)
    if zb is not None:
        text = text.replace(zb, "<ZEPHYR_BASE>")
    text = text.replace(str(REPO_ROOT), "<REPO_ROOT>")
    text = text.replace(str(WEST_TOPDIR), "<WEST_TOPDIR>")
    return text


def render_argv(result: subprocess.CompletedProcess[str]) -> str:
    """Shell-quoted rendering of a completed subprocess's own argv, for a
    failure assertion to interpolate alongside stdout/stderr -- .args is
    exactly what subprocess.run was given, so this needs no extra plumbing
    at any call site: -s cannot show a captured subprocess's command (only
    the test process's own stdout), and no assertion in this suite named
    the command that produced a failure until this existed."""
    return shlex.join(str(part) for part in result.args)


def write_rerun_script(script_dir: Path, cwd: Path, cmd: list[str], env: dict[str, str]) -> Path:
    """Write an executable rerun.sh into script_dir: a standalone re-run of
    this exact subprocess invocation, mirroring cmake/modules/dts.cmake's own
    rerun-expand.sh (shebang, set -e, the env-then-argv shape) -- written
    BEFORE the subprocess runs, so it survives even a failing invocation,
    exactly like the cmake precedent keeps its script after a FAILED
    configure. Composes with pytest's tmp_path_retention_policy (default
    failed): a failing test's tmp dir, and therefore this script, is kept
    without any extra flag; -o tmp_path_retention_policy=all keeps a
    passing one's too.

    cwd is recorded as an explicit cd line rather than left to whatever
    directory the script happens to be run from: a diagnostic that renders
    a process-cwd-relative path would otherwise reproduce DIFFERENTLY than
    the original failure, defeating the point of a reproduction script.

    Only the env entries this invocation's caller added on top of the
    inherited environment are exported -- recording every inherited
    variable would bury the ones that actually distinguish this
    invocation, and would embed values (e.g. a caller's current PATH) that
    have nothing to do with reproducing it."""
    lines = [
        "#!/bin/sh",
        "# regenerate: rewritten on every test run -- edits here do not persist.",
        "# Standalone re-run of this test's own subprocess invocation, e.g. under",
        f"# a debugger: copy the env + argv below into 'python3 -m pdb -m {RIGC_COMPILE} ...'.",
        "set -e",
        f"cd {shlex.quote(str(cwd))}",
    ]
    for key, value in env.items():
        if os.environ.get(key) != value:
            lines.append(f"export {key}={shlex.quote(value)}")
    lines.append("exec " + " ".join(shlex.quote(str(c)) for c in cmd) + ' "$@"')
    script_dir.mkdir(parents=True, exist_ok=True)
    script = script_dir / "rerun.sh"
    script.write_text("\n".join(lines) + "\n")
    script.chmod(0o755)
    return script


# The artifact filenames the emitter may produce, shared by
# test_emitted_rejects.py and test_emitted_corpus.py. Order is stable so a
# refreeze's git diff stays readable. rig-gen-includes.dtsi is emitted only
# when a rig's own parameter assignments need a header at all (today, only
# lotus_buttons -- emitter._needed_param_includes) -- assert_absent_or_
# refreeze covers the "correctly absent" case for every other corpus rig,
# the same way it already does for rig-gen.conf.
EMITTED_FILES = (
    "rig-gen.overlay",
    "rig-gen-includes.dtsi",
    "context.cmake",
    "config-sheet.md",
    "rig-gen.conf",
)


def freeze_or_assert(golden_path: Path, content: str) -> None:
    """Write content as the golden (RIGC_REFREEZE=1) or assert it matches
    the committed fixture, with a readable failure message on mismatch.

    context.cmake, config-sheet.md, and rig-gen-includes.dtsi
    (golden_path.name, not a directory check -- this is the single seam
    every EMITTED_FILES artifact passes through) compare STRUCTURALLY:
    context.cmake as a key -> value mapping, with RIG_DEPENDS as a set;
    config-sheet.md as the facts it carries (instance/socket/address/
    index/... -- see compare.py), never its prose rendering;
    rig-gen-includes.dtsi as the ORDERED header list the owning shield
    devices' own shield,param-includes declared. rig-gen.overlay compares
    through compare_overlay (targeted
    assertions only -- its semantics ride the zephyr.dts + dts_equiv.py
    comparison instead) EXCEPT for golden_path.parent.name (the rig's own
    golden directory) satisfying overlay_is_byte_compared -- the one rig
    with no zephyr.dts, which stays byte-compared so it keeps SOME check
    on this artifact.

    What remains byte-compared is exit_code and stderr.txt, and those two
    stay that way PERMANENTLY -- not pending a comparator. The reject
    corpus's rendered diagnostic wording is a user-facing product surface
    (a rig author reads it), which is the whole reason those goldens
    exist; loosening that comparison is out of scope."""
    if REFREEZE:
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(content)
        return
    if not golden_path.is_file():
        pytest.fail(
            f"golden missing: {golden_path}\n"
            f"(run with RIGC_REFREEZE=1 to create it, then inspect + "
            f"commit deliberately)"
        )
    expected = golden_path.read_text()
    if golden_path.name == "context.cmake":
        mismatch = compare_context_cmake(expected, content)
        if mismatch is not None:
            pytest.fail(f"golden mismatch: {golden_path}\n{mismatch}")
        return
    if golden_path.name == "config-sheet.md":
        mismatch = compare_config_sheet(expected, content)
        if mismatch is not None:
            pytest.fail(f"golden mismatch: {golden_path}\n{mismatch}")
        return
    if golden_path.name == "rig-gen-includes.dtsi":
        mismatch = compare_includes_dtsi(expected, content)
        if mismatch is not None:
            pytest.fail(f"golden mismatch: {golden_path}\n{mismatch}")
        return
    if golden_path.name == "rig-gen.overlay" and not overlay_is_byte_compared(
        golden_path.parent.name
    ):
        mismatch = compare_overlay(expected, content)
        if mismatch is not None:
            pytest.fail(f"golden mismatch: {golden_path}\n{mismatch}")
        return
    if expected != content:
        diff = "\n".join(
            difflib.unified_diff(
                expected.splitlines(),
                content.splitlines(),
                fromfile=str(golden_path),
                tofile="<observed>",
                lineterm="",
            )
        )
        pytest.fail(f"golden mismatch: {golden_path}\n{diff}")


def assert_absent_or_refreeze(golden_path: Path) -> None:
    """The counterpart of freeze_or_assert for an artifact the current run did
    NOT produce: under refreeze, drop a now-stale golden; otherwise assert
    none is committed — a golden for a file rigc no longer emits is
    itself a drift worth catching, not something to pass silently."""
    if REFREEZE:
        if golden_path.is_file():
            golden_path.unlink()
        return
    assert not golden_path.is_file(), (
        f"golden {golden_path} exists but this run produced no such file"
    )


# This directory carries no __init__.py (the frozen suite's own modules
# import each other as plain top-level names, e.g. "from conftest import
# ..."), so it is never part of the rigc package chain pytest walks to put
# scripts/ on sys.path by itself -- every integration module that needs an
# in-process rigc import inserts scripts/ explicitly (test_board_read.py,
# test_reference_shields.py, etc.); this is that same idiom, for the
# comparators context.cmake and config-sheet.md need structurally rather
# than byte-for-byte.
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from rigc.tests.compare import (  # noqa: E402
    compare_config_sheet,
    compare_context_cmake,
    compare_includes_dtsi,
    compare_overlay,
    overlay_is_byte_compared,
)


def run_expand(
    rig_yml: Path,
    out_dir: Path,
    shield_dirs: list[Path] | None = None,
    board: str | None = None,
    board_dts: Path | None = None,
    build_info: Path | None = None,
    bindings_dirs: list[Path] | None = None,
    include_dirs: list[Path] | None = None,
    revision: str | None = None,
    variant: str | None = None,
    connector_dirs: list[Path] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run python -m <RIGC_COMPILE> expand exactly as dts.cmake does
    (modulo the recipe form: dts.cmake passes --include-dir/--bindings-dir
    explicitly;
    this harness reuses a cached plain build's --build-info instead, per the
    cached-plain-build pattern — see plain_build_for) — a real subprocess,
    cwd pinned to the repo root so any process-cwd-relative path a
    diagnostic renders is reproducible regardless of the caller's cwd.

    shield_dirs is explicit here, with no repo-shield default: this
    harness copy carries none of boards/shields/'s own tether, so a
    caller in this directory (or any other hermetic caller) must pass its
    own --shield-dir list, or none at all. tests/integration_stay/
    corpus.py's own run_expand wrapper restores the old
    [SHIELD_DIR] default for its corpus-tethered callers.

    include_dirs is the cpp -I side of the explicit recipe (cli.py
    --include-dir); a hermetic fixture board whose .dts #includes its own
    fixture-local header needs this alongside bindings_dirs -- board_dts/
    build_info were the only two forms the harness needed until a fixture
    board required an #include of its own, so this was never plumbed
    through until now.

    board_dts/build_info are both None for the unknown-board fixture —
    deliberately, so the CLI exercises board.resolve's own name->dts DISCOVERY
    (list_boards.py) and its "board not found" diagnostic, exactly as a bare
    standalone invocation would.

    board threads cli.py's own --board: the board the INVOCATION supplies,
    winning over whatever the rig declares (nothing -- no corpus rig.yml
    declares a board) unconditionally. Omitted (None) means no injection
    at all -- the rig must declare its own board, or the loader rejects
    it exactly as an ordinary `rigc expand` with no -DBOARD would. Every
    corpus rig call site passes this now (RigCase.board); a caller
    wanting the un-injected diagnostic path itself (no-board-declared)
    leaves it unset on purpose.

    revision/variant carry the SELECTED qualifier axis values -- the
    harness's stand-in for what cmake/modules/dts.cmake's fork would resolve via
    list_rigs.py before invoking this same CLI. Omitted (None) means a
    bare target: the loader applies the rig's own declared default, if
    any.

    connector_dirs is cli.py's --connector-dir (repeatable): a fixture rig
    that must MATE a shield against a synthetic connector type needs this,
    since ctypes_registry's default is the real dts/bindings/connectors
    directory alone. Each type's header still resolves through
    include_dirs, not a separate list — see cli.py's own docstring."""
    zb = zephyr_base()
    env = dict(os.environ)
    env["ZEPHYR_BASE"] = zb
    env["PYTHONPATH"] = str(REPO_ROOT / "scripts")
    dirs = shield_dirs if shield_dirs is not None else []
    cmd = [sys.executable, "-m", RIGC_COMPILE, "expand", str(rig_yml)]
    for d in dirs:
        cmd += ["--shield-dir", str(d)]
    if board is not None:
        cmd += ["--board", board]
    if board_dts is not None:
        cmd += ["--board-dts", str(board_dts)]
    if build_info is not None:
        cmd += ["--build-info", str(build_info)]
    for b in bindings_dirs or []:
        cmd += ["--bindings-dir", str(b)]
    for i in include_dirs or []:
        cmd += ["--include-dir", str(i)]
    for c in connector_dirs or []:
        cmd += ["--connector-dir", str(c)]
    if revision is not None:
        cmd += ["--revision", revision]
    if variant is not None:
        cmd += ["--variant", variant]
    cmd += ["--out-dir", str(out_dir)]
    _LOGGER.info("expand argv: %s", shlex.join(cmd))
    write_rerun_script(out_dir, REPO_ROOT, cmd, env)
    return subprocess.run(
        cmd,
        env=env,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=subprocess_timeout(120),
    )
