# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Corpus-level property: doc/bridle/rigs4zephyr/reference/diagnostics.rst
and the actual diagnostic codes scripts/rigc/'s own production code
raises agree, in BOTH directions.

bridle-specific note: DOC_PAGE below points into doc/bridle/rigs4zephyr/,
the subtree the rig documentation was ported into within this repo's
large, pre-existing Sphinx site, rather than at a repo-root
doc/reference/ as in btr-shields, the single-purpose repo this guard was
ported from.

The page is a hand-written catalogue -- one entry per code, in prose --
rather than an autodoc render, so it CAN fall behind the source the
ordinary way a hand-written page does: a new call site added with no
entry for it, or an entry left behind after its call site was deleted or
renamed. This is a law about the CORPUS (docs + production source,
together) rather than about any one module, so it lives here beside the
other corpus-level laws (test_api_reference_drift.py,
test_dts_vocabulary_drift.py, test_cli_reference_drift.py) rather than in
a test_<module>.py mirroring no single unit. It is a pure file/text scan
-- no cmake, no toolchain, no `@pytest.mark.build`.

Two directions, both checked:

  forward  -- every `lang-*`/`phys-*` code string literal passed to
              diag.error()/diag.warning() anywhere in scripts/rigc/'s own
              PRODUCTION source (every *.py under scripts/rigc/,
              excluding anything under a `tests/` directory) has its own
              entry on doc/reference/diagnostics.rst.

  reverse  -- every code named on that page is one some production call
              site actually raises.

The source side is a regex over string literals, the same crude-but-
sufficient technique test_dts_vocabulary_drift.py already uses for
`shield,*`/`plug,*`/`socket,*` properties, for the identical reason: a
diagnostic code has exactly one spelling in real source, a double-quoted
or single-quoted string literal passed as error()/warning()'s first
positional argument, and never appears any other way (diag.py's own
Severity/Diagnostic types make the code a plain `str`, never an enum
whose members this scan would otherwise need to chase through an
import). Scoped to PRODUCTION files only, deliberately: the golden test
corpus under scripts/rigc/tests/goldens/ reuses some of the same code
spellings as GOLDEN DIRECTORY NAMES (`shield-uart-subset-frdm/`, not a
diagnostic), and a scan that did not exclude tests/ entirely would count
those as if they were construction sites.

The page side is a regex over the same shape, double-backtick-quoted --
every entry names its own code as an inline literal (`` ``lang-foo`` ``),
matching the convention this project's other reference pages already use
for the same purpose (test_dts_vocabulary_drift.py's property tokens,
test_cli_reference_drift.py's `--options`).
"""

from __future__ import annotations

import re

from harness import REPO_ROOT

PROD_ROOT = REPO_ROOT / "scripts" / "rigc"
DOC_PAGE = REPO_ROOT / "doc" / "bridle" / "rigs4zephyr" / "reference" / "diagnostics.rst"

#: A `lang-*`/`phys-*` code exactly as it appears as a quoted Python
#: string literal in real source -- the production-code side. Matches
#: error()/warning()'s own first positional argument (and nothing else:
#: no other string in this codebase is shaped `(lang|phys)-<ident>`).
_CODE_LITERAL_RE = re.compile(r'''["']((?:lang|phys)-[a-z][a-z0-9-]*)["']''')

#: The identical code shape, double-backtick-quoted -- the reference-page
#: side, where every entry names its own code as an inline literal.
_DOC_CODE_RE = re.compile(r'``((?:lang|phys)-[a-z][a-z0-9-]*)``')


def _production_py_files():
    for path in sorted(PROD_ROOT.rglob("*.py")):
        if "tests" in path.relative_to(PROD_ROOT).parts:
            continue
        yield path


def _code_literals() -> set[str]:
    """Every `lang-*`/`phys-*` code string literal in scripts/rigc/'s own
    PRODUCTION source (never tests/, so a golden directory name reusing
    the same spelling is never counted) -- a fresh set the caller owns."""
    found: set[str] = set()
    for path in _production_py_files():
        found.update(_CODE_LITERAL_RE.findall(path.read_text()))
    return found


def _documented_codes() -> set[str]:
    """Every code named as its own double-backtick inline literal
    anywhere on doc/reference/diagnostics.rst -- a fresh set the caller
    owns."""
    return set(_DOC_CODE_RE.findall(DOC_PAGE.read_text()))


def test_diagnostics_page_documents_something_at_all() -> None:
    """The negative control for both directions below: an empty or
    renamed page would make the reverse check trivially true and the
    forward check trivially fail loudly enough to be caught anyway -- but
    a page that documented only a HANDFUL of codes (a stale partial
    catalogue) would still pass a bare non-empty check. Scripts/rigc/'s
    own source raises 45 codes today (31 lang-*, 14 phys-*); a fixed
    floor well under that catches a regex that silently matches almost
    nothing without hardcoding the exact count here too."""
    documented = _documented_codes()
    assert len(documented) >= 40, (
        f"doc/reference/diagnostics.rst gives an entry to only "
        f"{len(documented)} code(s): {sorted(documented)}"
    )


def test_diagnostics_forward_every_raised_code_is_documented() -> None:
    """Every `lang-*`/`phys-*` code scripts/rigc/'s own production source
    actually raises has its own entry on doc/reference/diagnostics.rst.
    A code nobody documented is one a reader who just hit it has nowhere
    to look it up, and the docs build cannot notice its absence -- only
    this test can."""
    code = _code_literals()
    assert len(code) >= 40, (
        f"only {len(code)} code(s) found in scripts/rigc/'s own "
        "production source -- the literal scan is finding far fewer "
        "than the known 45, so it is very likely broken rather than the "
        "catalogue having shrunk"
    )
    missing = sorted(code - _documented_codes())
    assert not missing, (
        f"code(s) raised by scripts/rigc/ with no entry on doc/reference/diagnostics.rst: {missing}"
    )


def test_diagnostics_reverse_every_documented_code_is_real() -> None:
    """Every code doc/reference/diagnostics.rst names is one some real
    call site in scripts/rigc/ actually raises. Catches a page that
    outlived a code's rename or removal -- the retired-command failure
    mode (see test_cli_reference_drift.py's own docstring) applied to
    diagnostic codes instead of `west` options."""
    invented = sorted(_documented_codes() - _code_literals())
    assert not invented, (
        "doc/reference/diagnostics.rst documents code(s) no production "
        f"call site raises: {invented}"
    )
