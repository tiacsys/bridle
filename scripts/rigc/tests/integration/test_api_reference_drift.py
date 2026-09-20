# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Corpus-level property: the API reference pages
(doc/bridle/rigs4zephyr/reference/api/*.rst) and the set of modules that
actually exist under scripts/rigc/ agree, in BOTH directions.

bridle-specific note: this repo's doc/ is a large, pre-existing Sphinx
site (Zephyr, devicetree, kconfig, cannectivity, bridle's own general
docs). The rig documentation ported alongside this guard lives at
doc/bridle/rigs4zephyr/, a subtree of that site, so API_DIR below points
there rather than at a repo-root doc/reference/api/ as it does in
btr-shields, the single-purpose repo this guard was ported from.

The pages carry no prose ABOUT the modules -- each is a heading plus one
`.. automodule::`, and the text a reader gets is the module's own
docstring, read out of the source at build time. So the usual drift (a
page describing last month's behaviour) cannot happen here by
construction. What CAN happen is the two failures this module rules out:

  forward  -- a module exists under scripts/rigc/ (production only, never
              tests/) and NO page names it, so it is missing from the
              reference entirely. This is the likely one: a new module
              arrives in a slice that never opens doc/.

  reverse  -- a page names a module that does not exist, which after a
              rename or a delete would fail the docs build under -W. This
              is checked here as well as there so that `scripts/check.sh`
              alone catches it: the docs build is a separate gate, and a
              reviewer running only the test suite would otherwise see
              green on a reference pointing at nothing.

Also asserted: EXACTLY ONE page names each module. Two pages documenting
one module renders it twice, and a `:py:mod:` cross-reference to it then
resolves ambiguously.

The module set is derived from the FILESYSTEM (a walk of *.py), not from
an import of the package: a module that fails to import is precisely one
this test should still see, and `pkgutil.walk_packages` would import it to
find it. The page side is a regex over the .rst text rather than a reST
parse, for the same reason test_dts_vocabulary_drift.py scans literals:
the directive has exactly one spelling in these files and never appears
any other way.

A pure file/text scan -- no cmake, no toolchain, no `@pytest.mark.build`.
It lives here beside the other corpus-level laws (test_singleton_identity_
law.py, test_dts_vocabulary_drift.py, test_golden_path_hygiene.py) rather
than in a test_<module>.py, because its subject is the corpus (docs +
source, together) rather than any one unit.
"""

from __future__ import annotations

import re

from harness import REPO_ROOT

PROD_ROOT = REPO_ROOT / "scripts" / "rigc"
API_DIR = REPO_ROOT / "doc" / "bridle" / "rigs4zephyr" / "reference" / "api"

#: `.. automodule:: rigc.some.module`, the only form these pages use.
_AUTOMODULE_RE = re.compile(r"^\.\.\s+automodule::\s+([A-Za-z_][\w.]*)\s*$", re.MULTILINE)


def _production_modules() -> set[str]:
    """Every importable module name under scripts/rigc/, tests excluded --
    `rigc`, `rigc.cli`, `rigc.loader`, ... A package is named by its
    directory (`rigc.loader`), never by its `__init__` (there is no
    `rigc.loader.__init__` to document), which is also the name autodoc
    itself uses.

    Returns a fresh set the caller owns."""
    names: set[str] = set()
    for path in PROD_ROOT.rglob("*.py"):
        rel = path.relative_to(PROD_ROOT)
        if "tests" in rel.parts:
            continue
        parts = list(rel.parts[:-1])
        if rel.stem != "__init__":
            parts.append(rel.stem)
        names.add(".".join(["rigc", *parts]))
    return names


def _documented_modules() -> dict[str, list[str]]:
    """Every `automodule` target across doc/reference/api/, mapped to the
    page filename(s) naming it -- a list, so a module named twice is
    visible as such rather than collapsed."""
    found: dict[str, list[str]] = {}
    for page in sorted(API_DIR.glob("*.rst")):
        for name in _AUTOMODULE_RE.findall(page.read_text()):
            found.setdefault(name, []).append(page.name)
    return found


def test_api_pages_exist_at_all() -> None:
    """The negative control for both directions below: a scan of an empty
    or renamed directory would find no automodules, and "every module is
    documented" would then be trivially false while "every documented
    module exists" would be trivially TRUE. Fail loudly instead."""
    pages = sorted(p.name for p in API_DIR.glob("*.rst"))
    assert "index.rst" in pages, f"doc/reference/api/ holds no index: {pages}"
    assert len(pages) >= 2, f"doc/reference/api/ holds only {pages}"


def test_api_reference_forward_every_module_is_documented() -> None:
    """Every production module under scripts/rigc/ is named by an
    `automodule` on some API reference page. A module nobody documented is
    a module a reader cannot find, and the docs build cannot notice its
    absence -- only this test can."""
    missing = sorted(_production_modules() - set(_documented_modules()))
    assert not missing, (
        "module(s) under scripts/rigc/ with no `.. automodule::` on any "
        f"doc/reference/api/ page: {missing}"
    )


def test_api_reference_reverse_every_documented_module_exists() -> None:
    """Every `automodule` target is a module that really exists. A stale
    target fails the docs build under -W; this catches it from the test
    suite too."""
    real = _production_modules()
    documented = _documented_modules()
    invented = sorted(
        f"{name} ({', '.join(documented[name])})" for name in documented if name not in real
    )
    assert not invented, (
        f"doc/reference/api/ names module(s) that do not exist under scripts/rigc/: {invented}"
    )


def test_api_reference_documents_each_module_exactly_once() -> None:
    """No module is documented on two pages. Autodoc would render it
    twice, and every `:py:mod:`/`:py:func:` reference into it would then
    have two equally good targets."""
    documented = _documented_modules()
    duplicated = sorted(
        f"{name} ({', '.join(pages)})" for name, pages in documented.items() if len(pages) > 1
    )
    assert not duplicated, f"module(s) named by more than one doc/reference/api/ page: {duplicated}"
