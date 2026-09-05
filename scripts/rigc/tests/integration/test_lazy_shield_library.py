# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Integration verification for the lazy shield-library parse: a LAZILY-
resolved axis-less base template that fails to preprocess raises
LoadError out of `ShieldLibrary.resolve()`, reached mid-loop inside
`loader._build_topology`'s phase-3 instance loop. That phase carries a
try/except boundary (the same shape `load_shield_library`'s own scan loop
uses) so a lazily-resolved template's raise still carries every
diagnostic collected before it, whether the template is a REVISION or an
axis-less BASE.

Not a frozen golden: no `freeze_or_assert` call, nothing under
tests/goldens/ read or written. The fixture only needs to prove the
boundary carries prior diagnostics through a raise, not pin the tool's
exact wording.
"""

from __future__ import annotations

from pathlib import Path

from harness import FIXTURES_DIR, run_expand

_FIXTURE = FIXTURES_DIR / "boards" / "rigs" / "shield-lazy-parse-preserves-priors"


def test_broken_referenced_shield_preserves_earlier_diagnostics(tmp_path: Path) -> None:
    """rig.yml's first instance names `misnamed_fixture` (its .shield
    node name disagrees with its folder -- a lang-shield-name diagnostic
    RETURNED by resolve(), no raise) and its second names `broken_cpp`
    (a template that fails to preprocess -- a real cpp subprocess
    failure, raised as LoadError). Both must render: the first
    diagnostic already sat in _build_topology's `diags` list when the
    second instance's resolve() raised, and the phase's own except
    clause re-raises with those priors prepended (loader/__init__.py's
    `_build_topology`, mirroring `load_shield_library`'s own try/except
    shape)."""
    out_dir = tmp_path / "out"
    result = run_expand(
        _FIXTURE / "rig.yml",
        out_dir,
        board="nucleo_f401re/stm32f401xe/rig",
        shield_dirs=[_FIXTURE / "shields"],
        connector_dirs=[FIXTURES_DIR / "dts" / "unified-connectors"],
        include_dirs=[FIXTURES_DIR / "include"],
    )

    assert result.returncode != 0, "a shield template that fails to preprocess must reject the rig"
    assert "[lang-shield-name]" in result.stderr, result.stderr
    assert "misnamed_fixture" in result.stderr, result.stderr
    assert "[lang-cpp]" in result.stderr, result.stderr
