# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: diag — the diagnostics core.

Two contracts, both diag.py's own: rendering into the frozen stderr
format (structure only, with synthetic content: the `severity[code]:
head` line, four-space continuation lines, `    at <path>:<line> (<key>)`
anchors, anchor ordering and de-duplication — per-diagnostic message
WORDING is asserted ONLY by the frozen stderr goldens), and anchor-path
rendering (the module-agnostic rule: a path under a
`scripts/<module>/` component renders relative to that component;
anything else renders unchanged — a pure function of the path value,
exercised with synthetic roots).
"""

from __future__ import annotations

from rigc.diag import Diagnostic, SourceRef, anchor_path, error, has_errors, render

# ------------------------------------------------ the frozen render format


def test_single_error_no_refs() -> None:
    assert render([error("x-code", "the claim")]) == "error[x-code]: the claim"


def test_message_continuation_lines_indent_four() -> None:
    out = render([error("x-code", "the claim\nfirst detail\nsecond detail")])
    assert out == ("error[x-code]: the claim\n    first detail\n    second detail")


def test_anchor_line_shape_with_key() -> None:
    ref = SourceRef("/syn/boards/rigs/r/rig.yml", 7, "rig")
    out = render([error("x-code", "claim", (ref,))])
    assert out.splitlines()[1] == "    at /syn/boards/rigs/r/rig.yml:7 (rig)"


def test_anchor_line_shape_without_key() -> None:
    ref = SourceRef("/syn/boards/rigs/r/rig.yml", 3)
    out = render([error("x-code", "claim", (ref,))])
    assert out.splitlines()[1] == "    at /syn/boards/rigs/r/rig.yml:3"


def test_duplicate_anchors_render_once_order_kept() -> None:
    a = SourceRef("/syn/a.yml", 1, "k")
    b = SourceRef("/syn/b.yml", 2)
    out = render([error("x-code", "claim", (a, b, a))])
    assert out.splitlines()[1:] == ["    at /syn/a.yml:1 (k)", "    at /syn/b.yml:2"]


def test_warning_severity_renders_as_warning() -> None:
    d = Diagnostic("warning", "x-code", "soft claim")
    assert render([d]) == "warning[x-code]: soft claim"


def test_multiple_diagnostics_join_with_newline() -> None:
    out = render([error("one", "a"), error("two", "b")])
    assert out == "error[one]: a\nerror[two]: b"


def test_has_errors_distinguishes_severity() -> None:
    warning = Diagnostic("warning", "x-code", "m")
    assert not has_errors([])
    assert not has_errors([warning])
    assert has_errors([warning, error("x-code", "m")])


# ------------------------------------------------- anchor-path rendering


def test_under_a_scripts_module_renders_relative() -> None:
    assert (
        anchor_path("/syn/repo/scripts/rigexp/tests/fixtures/r/rig.yml")
        == "tests/fixtures/r/rig.yml"
    )


def test_module_agnostic_any_module_name() -> None:
    """Anchor-path rendering does not depend on the module name in the
    path: the same relative-rendering rule applies under any
    scripts/<module>/ path, so the reject goldens' anchor lines don't
    move when fixtures relocate between modules."""
    assert (
        anchor_path("/syn/repo/scripts/rigc/tests/fixtures/r/rig.yml") == "tests/fixtures/r/rig.yml"
    )


def test_outside_scripts_renders_unchanged() -> None:
    assert anchor_path("/syn/repo/boards/rigs/r/rig.yml") == "/syn/repo/boards/rigs/r/rig.yml"


def test_file_directly_under_scripts_renders_unchanged() -> None:
    """scripts/<file> has no module component below scripts/."""
    assert anchor_path("/syn/repo/scripts/check.sh") == "/syn/repo/scripts/check.sh"


def test_file_directly_under_the_module_renders_relative() -> None:
    assert anchor_path("/syn/repo/scripts/mod/thing.yml") == "thing.yml"


def test_deepest_scripts_component_wins() -> None:
    assert anchor_path("/a/scripts/m1/scripts/m2/f.yml") == "f.yml"


def test_relative_input_with_scripts_component() -> None:
    assert anchor_path("scripts/mod/tests/f.yml") == "tests/f.yml"


# ------------------------------------------------------------------ LoadError


def test_load_error_carries_every_diagnostic_it_unwound_past() -> None:
    """The fatal-path contract: a LoadError renders as if
    every finding had been returned normally -- so boundaries prepend
    their accumulated diagnostics and NOTHING is lost to the raise. The
    exception's own message is the fatal (last) finding's."""
    from rigc.diag import LoadError

    prior = error("lang-shield-name", "scanned earlier, must survive")
    fatal = error("lang-parse", "the fatal finding")
    e = LoadError(prior, fatal)
    assert e.diags == (prior, fatal)
    assert str(e) == "the fatal finding"
