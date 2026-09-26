# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""`west rigs` sees a Zephyr module joined through EXTRA_ZEPHYR_MODULES,
exactly as a build does.

A build accepts extra modules that are not west projects via
EXTRA_ZEPHYR_MODULES (a cmake variable or an environment variable,
`;`-separated; zephyr_module.cmake). `west rigs` has no cmake cache, so the
environment variable is its only form -- scripts/west_commands/rigs.py
leaves it to zephyr_module.parse_modules, which reads it. What that module
contributes must then reach every part of the command, not only the rig
listing: its board root (rigs, shields, boards to census) AND its dts root
(connector types under dts/bindings/connectors, their headers under
include), the same two roots cmake/modules/dts.cmake threads for a real
build.

The cmake seam has the same need one step earlier: boards.cmake and
dts.cmake resolve a `-DRIG=<shield>` promotion target through
scripts/list_rigs.py before rigc ever runs, and that resolution parses the
shield's template -- so they pass every DTS_ROOT as `--dts-root`, and the
last test below pins that flag on list_rigs.py directly.

The fixture module, tests/fixtures/extra_module/, is a module no west
project names. Its rig, its shield, the connector type that shield plugs
and the header that shield includes exist nowhere else, so each assertion
below can only pass through that module's own roots. Driven as a
subprocess: `west rigs` configures nothing, so this is not a build test.
"""

from __future__ import annotations

import os
import subprocess
import sys

from harness import (
    FIXTURES_DIR,
    REPO_ROOT,
    WEST_EXE,
    WEST_TOPDIR,
    subprocess_timeout,
    zephyr_base,
)

_MODULE = FIXTURES_DIR / "extra_module"


def _west_rigs(*args: str, extra_modules: str | None) -> subprocess.CompletedProcess[str]:
    """`west rigs <args>` from the workspace topdir, with
    EXTRA_ZEPHYR_MODULES set to `extra_modules` -- or removed from the
    environment entirely when None, so an ambient value cannot leak in."""
    env = dict(os.environ)
    env["ZEPHYR_BASE"] = zephyr_base()
    env.pop("EXTRA_ZEPHYR_MODULES", None)
    env.pop("ZEPHYR_EXTRA_MODULES", None)
    if extra_modules is not None:
        env["EXTRA_ZEPHYR_MODULES"] = extra_modules
    return subprocess.run(
        [WEST_EXE, "rigs", *args],
        cwd=str(WEST_TOPDIR),
        env=env,
        capture_output=True,
        text=True,
        timeout=subprocess_timeout(60),
    )


def test_the_listing_includes_an_extra_modules_rig_only_when_the_module_is_named() -> None:
    """The pair is the point: without the variable the fixture rig is
    absent, so its presence with the variable is the variable's doing and
    not a board root found some other way."""
    without = _west_rigs(extra_modules=None)
    assert without.returncode == 0, without.stderr
    assert "extra_module_rig" not in without.stdout.split()

    joined = _west_rigs(extra_modules=str(_MODULE))
    assert joined.returncode == 0, joined.stderr
    assert "extra_module_rig" in joined.stdout.split()


def test_a_semicolon_separated_list_is_honored_like_a_builds() -> None:
    """The same `;`-separated list form a build accepts; an empty element
    (a trailing `;`) is skipped, not an error."""
    result = _west_rigs(extra_modules=f"{_MODULE};")
    assert result.returncode == 0, result.stderr
    assert "extra_module_rig" in result.stdout.split()


def test_explain_promotes_a_shield_plugging_the_modules_own_connector_type() -> None:
    """Promoting the fixture shield resolves its template, which includes
    the connector type's header from the module's own include/. That
    header exists nowhere else, so the module's dts root has to have been
    threaded as an include root."""
    result = _west_rigs("--explain", "extra_module_shield", extra_modules=str(_MODULE))
    assert result.returncode == 0, result.stderr
    assert "shield: extra_module_shield" in result.stdout


def test_boards_for_loads_a_rig_whose_shield_plugs_the_modules_own_connector_type() -> None:
    """--boards-for loads the rig through rigc's loader, which checks the
    shield's plug against the connector-type registry: the type is
    declared only under the module's own dts/bindings/connectors, so a
    registry built from rigc's defaults would reject the rig (exit 1)
    instead of answering. No board carries this socket type, so the
    answer itself is empty -- a fact, exit 0."""
    for target in ("extra_module_rig", "extra_module_shield"):
        result = _west_rigs("--boards-for", target, extra_modules=str(_MODULE))
        assert result.returncode == 0, f"--boards-for {target}:\n{result.stderr}"
        assert result.stdout.strip() == "", result.stdout


def test_list_rigs_resolves_a_promotion_target_against_its_dts_roots() -> None:
    """The cmake seam's resolver, given the module as both a board root and
    a dts root -- what boards.cmake passes for a module in the build.
    Resolving a promotion target parses the shield's template, whose
    header lives only under the module's own include/, so the same query
    without `--dts-root` cannot resolve it; the pair shows the flag is what
    makes the difference."""
    cmd = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "list_rigs.py"),
        f"--board-root={_MODULE}",
        "--rig=extra_module_shield",
        "--cmakeformat={NAME};{PROMOTED}",
    ]
    env = {**os.environ, "ZEPHYR_BASE": zephyr_base()}

    def run(extra: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            cmd + extra,
            env=env,
            capture_output=True,
            text=True,
            timeout=subprocess_timeout(60),
        )

    with_root = run([f"--dts-root={_MODULE}"])
    assert with_root.returncode == 0, with_root.stderr
    assert with_root.stdout.strip() == "NAME;extra_module_shield;PROMOTED;extra_module_shield"

    without_root = run([])
    assert without_root.returncode != 0, without_root.stdout
