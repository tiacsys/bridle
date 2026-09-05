# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Diagnostics core: diagnostics are DATA, returned upward.

No mutable accumulator threaded in and written to, no whole-model
parameters where a value would do, no side channel: a function that
finds something wrong RETURNS Diagnostic values (alone or beside its
result); composition is list concatenation at the caller.

ONE renderer produces the frozen stderr format the goldens specify:

    error[<code>]: <message first line>
        <message continuation lines, four-space indented>
        at <path>:<line> (<key>)

Anchor-path rule, module-agnostic: if the path lies under a
`scripts/<module>/` component, it renders relative to that component;
otherwise it renders absolute. anchor_path() is a pure function of the
path value alone -- deliberately no module-scope dirname(__file__)
constant -- so unit tests exercise it with synthetic roots."""

from __future__ import annotations

import os
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Literal

#: Severity vocabulary, closed at the TYPE level: this is the module
#: where a severity typo becomes wrong frozen bytes, so mypy gets to
#: veto one. The taxonomy carries over from the goldens: "lang-*" codes
#: come from the loader, "phys-*" codes from the analyzer.
Severity = Literal["error", "warning"]
ERROR: Severity = "error"
WARNING: Severity = "warning"


@dataclass(frozen=True)
class SourceRef:
    """One source anchor: file path (absolute as loaded), 1-based line,
    and the human key label (YAML key path, node path, or DTS label)."""

    file: str
    line: int
    key: str = ""


@dataclass(frozen=True)
class Diagnostic:
    """One finding, as a value. message's first line is the claim;
    following lines are detail (rendered indented)."""

    severity: Severity
    code: str  # "lang-*" | "phys-*"
    message: str
    # None entries are LEGAL and skipped at render time: callers pass
    # (dev.src, inst.src)-shaped tuples whose members may be absent
    # without filtering at every site.
    refs: tuple[SourceRef | None, ...] = ()


def error(code: str, message: str, refs: Sequence[SourceRef | None] = ()) -> Diagnostic:
    """Returns one ERROR-severity Diagnostic value; refs may contain
    None entries (skipped at render time). The caller owns the value."""
    return Diagnostic(ERROR, code, message, tuple(refs))


def warning(code: str, message: str, refs: Sequence[SourceRef | None] = ()) -> Diagnostic:
    """Returns one WARNING-severity Diagnostic value; same refs contract
    as error()."""
    return Diagnostic(WARNING, code, message, tuple(refs))


def has_errors(diags: Iterable[Diagnostic]) -> bool:
    return any(d.severity == ERROR for d in diags)


def anchor_path(path: str) -> str:
    """The anchor-path rule, module-agnostic: render a path under
    a `scripts/<module>/` component relative to that component (the
    DEEPEST such component wins, the most specific reading), otherwise
    render it unchanged. A file directly under a `scripts/` component has
    no module below it and stays unchanged."""
    parts = path.split(os.sep)
    # Need parts[i] == "scripts", a module at i+1, and content below it.
    for i in range(len(parts) - 3, -1, -1):
        if parts[i] == "scripts":
            return os.sep.join(parts[i + 2 :])
    return path


def _render_one(diag: Diagnostic) -> str:
    head, *rest = diag.message.splitlines()
    lines = [f"{diag.severity}[{diag.code}]: {head}"]
    lines += [f"    {line}" for line in rest]
    seen: set[str] = set()
    for ref in diag.refs:
        if ref is None:  # legal absent anchor (see Diagnostic.refs)
            continue
        anchor = f"{anchor_path(ref.file)}:{ref.line}"
        if ref.key:
            anchor = f"{anchor} ({ref.key})"
        if anchor not in seen:  # duplicates render once, order kept
            seen.add(anchor)
            lines.append(f"    at {anchor}")
    return "\n".join(lines)


def render(diags: Iterable[Diagnostic]) -> str:
    """THE renderer -- the only place diagnostics become text. One line
    block per diagnostic, joined by newlines (no trailing newline; the
    caller's print() supplies it)."""
    return "\n".join(_render_one(d) for d in diags)


class LoadError(Exception):
    """A fatal loader failure (a YAML/DTS parse error, cpp preprocessing
    that failed outright) -- loading cannot continue past this point at
    all, unlike an ordinary Diagnostic finding, which composes upward as
    data and lets the caller keep going. Carries the DIAGNOSTICS to
    render: the fatal finding itself, plus -- prepended at each
    accumulation boundary that the raise unwinds through (library scan,
    loader orchestration) -- everything that boundary had already
    gathered, so a raise never silently drops a prior finding from the
    rendered output."""

    def __init__(self, *diags: Diagnostic) -> None:
        # A LoadError with nothing to render would exit 1 with EMPTY
        # stderr -- a silent reject, the one outcome this design forbids.
        assert diags, "LoadError requires at least one Diagnostic"
        self.diags = diags
        super().__init__(diags[-1].message)
