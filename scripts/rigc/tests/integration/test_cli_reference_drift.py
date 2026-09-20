# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Corpus-level property: doc/bridle/rigs4zephyr/reference/commands.rst
and the two real argument parsers agree on what options exist, in BOTH
directions.

bridle-specific note: DOC_PAGE below points into doc/bridle/rigs4zephyr/,
the subtree the rig documentation was ported into within this repo's
large, pre-existing Sphinx site, rather than at a repo-root
doc/reference/ as in btr-shields, the single-purpose repo this guard was
ported from. The west-subcommand-vocabulary scan further down is likewise
scoped to that subtree rather than the whole of doc/ -- bridle's doc/
also mirrors Zephyr's own documentation, which is not this guard's
concern and not something this PR is responsible for keeping consistent.

The two surfaces the page documents (a rig build is no longer its own
west command -- see below -- so it contributes no parser of its own to
check here; the page's own prose mentions of `-b`/`--board` and `--shield`
are Zephyr's `west build`/cmake flags, admitted via
`_INHERITED_FROM_WEST_BUILD` below rather than declared by anything this
repo owns):

  `rigc expand`          -- rigc.cli.build_parser(), the REAL parser,
                            imported and interrogated (it is importable
                            with no Zephyr tree present, which is the
                            whole reason cli.py keeps build_parser
                            public).
  `west rigs`            -- scripts/west_commands/rigs.py, plus the
                            options `list_rigs.add_args()` contributes to
                            it (that ONE function, not the whole module:
                            `add_args_formatting`'s `--json`/
                            `--cmakeformat` belong to the standalone
                            resolver cmake calls, which `west rigs` does
                            not expose and this page does not document)

The west surface is scanned as TEXT (a regex over `add_argument(` calls)
rather than imported: `rigs.py` locates the Zephyr script tree at import
time, so importing it drags a whole Zephyr checkout into a test whose
subject is a documentation page. The regex is crude in the same way
test_dts_vocabulary_drift.py's literal scan is crude, and sufficient for
the same reason: an option is declared exactly one way in this file.

Two directions, both checked:

  forward  -- every LONG option (`--thing`) any of the three parsers
              declares has its OWN ENTRY on the page: a definition-list
              term, or the first cell of a list-table row. A passing
              mention in someone else's prose does not count -- that is
              test_dts_vocabulary_drift.py's own hard-won rule (it scans
              heading text for exactly this reason), and it earns its
              keep here immediately: this page's prose names `--explain`
              and `--boards-for` while describing what they do to `-f`,
              so a whole-page scan would keep passing after either one's
              entry was renamed away.

  reverse  -- every `--thing` token ON the page (prose included, this
              time) is a real option of one of the three, or a member of
              the inherited-from-`west build` allowlist below. This is the
              direction that catches the actual historical failure mode:
              the page (like the help strings before it) describing a flag
              that was renamed or retired.

Short options are deliberately not checked. `-b`, `-s`, `-p`, `-f`, `-n`,
`-v` are one character and appear inside ordinary prose constantly; the
long form is the one an option is identified by here.

A pure file/text scan plus one in-process import -- no cmake, no
toolchain, no `@pytest.mark.build`.

A SECOND, narrower law lives here too: every `west <subcommand>` named
ANYWHERE under doc/ (not just this page -- a tutorial teaches commands
too) must be either a command THIS repo declares (`scripts/
west-commands.yml`), or a real command of upstream west itself --
`west build`, `west flash`, ... This is the guard the retirement of
`west build-rig` showed was missing: four tutorial pages kept teaching
it, and the checks above stayed green throughout, because they scan only
commands.rst's own OPTIONS, never any page's SUBCOMMAND names. The
failure mode this catches is specific -- a doc naming a subcommand this
repo used to provide and no longer does, or a plain typo -- not "every
west feature is documented here" (most of upstream west's own surface
has no business appearing on this page at all).

The known-real set is assembled from two sources, neither a hardcoded
guess: west's own BUILTIN_COMMAND_GROUPS (a real pip dependency already
-- scripts/west_commands/rigs.py imports `west.commands` -- interrogated
by instantiating each command class and reading its own `.name`, exactly
as `_expand_parser()` below interrogates rigc's own parser rather than
re-deriving it from source text), and Zephyr's own
`$ZEPHYR_BASE/scripts/west-commands.yml` (`build`, `flash`, `boards`,
`shields`, ... -- the extension commands Zephyr itself contributes,
read the same way this repo's own manifest is, never a spelled-out
list that would silently fall behind whichever version of Zephyr this
workspace pins).

A mention counts only in the two shapes this doc set actually spells a
runnable command in -- a `$ west <subcommand>` prompt line inside a
`.. code-block:: console` block, or a `` ``west <subcommand>`` ``
double-backtick inline literal -- never a bare "west" in running prose
("a west workspace", "west's own manifest"), which is common and never a
command name. Restricting to these two shapes is what keeps this narrow
enough to hold: every REAL west-build-rig-shaped mention in this doc
set's own history used one of them, and a whole-page "west\\s+\\w+" scan
was tried and rejected here for exactly the reason `_INHERITED_FROM_
WEST_BUILD` above exists for options -- "west workspace" alone would
require an ever-growing allowlist of ordinary nouns rather than one of
real commands.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path
from typing import Any, cast

import yaml
from harness import REPO_ROOT, zephyr_base

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from rigc.cli import build_parser  # noqa: E402

DOC_PAGE = REPO_ROOT / "doc" / "bridle" / "rigs4zephyr" / "reference" / "commands.rst"
WEST_COMMANDS = (REPO_ROOT / "scripts" / "west_commands" / "rigs.py",)
LIST_RIGS = REPO_ROOT / "scripts" / "list_rigs.py"
#: The subtree the west-subcommand-vocabulary scan below walks -- the rig
#: documentation only, not the whole of this repo's doc/ (which also
#: mirrors Zephyr's own documentation and is not this guard's concern).
RIGS_DOC_ROOT = REPO_ROOT / "doc" / "bridle" / "rigs4zephyr"

#: The one `list_rigs.py` function `west rigs` actually calls on its own
#: parser. Scanned by name so that an option added to a DIFFERENT function
#: in that module -- one only cmake's resolver ever sees -- does not start
#: demanding a place on a page about human-facing commands.
LIST_RIGS_SHARED_FUNC = "add_args"

#: A long option as declared in an `add_argument("--thing", ...)` call,
#: either quoting style.
_DECL_RE = re.compile(r"""add_argument\(\s*["'](--[a-z][a-z0-9-]*)["']""")

#: The same, as it appears anywhere on the page: inside double backticks,
#: since this page writes every option as an inline literal.
_DOC_RE = re.compile(r"``(--[a-z][a-z0-9-]*)")

#: A list-table row whose first cell is an option: `   * - ``--thing```.
_DOC_CELL_RE = re.compile(r"^\s*\* - ``(--[a-z][a-z0-9-]*)")

#: A definition-list TERM: the option at the very start of a line. Not
#: sufficient on its own -- a paragraph that merely BEGINS with an option
#: literal looks identical, and this page has two of those ("``--explain``
#: alike — is either the name of..."), so `_documented_entries` also
#: requires the next line to be indented, which is what makes a term a
#: term in reST. Without that second condition the forward check silently
#: accepted a renamed entry, observed by mutating the page.
_DOC_TERM_RE = re.compile(r"^``(--[a-z][a-z0-9-]*)")

#: Zephyr's own `west build`/cmake flags, documented by Zephyr rather than
#: here, that the page's prose still legitimately names: a rig build is
#: `west build` (or a bare `cmake`) with one added `-DRIG=`, and the page
#: says where that acquires a rule of its own -- the board becoming
#: mandatory, `--shield` becoming a configure error -- without this repo
#: declaring either flag itself (rigc.cli's OWN `--board`, for `rigc
#: expand`'s standalone recipe, already covers that token in
#: `_declared_options()` too; it stays listed here so the reverse check
#: does not depend on which of the two reasons happens to cover it).
#: Spelled out rather than pattern-matched: an unknown `--flag` on the
#: page should have to be added HERE, deliberately, with this comment in
#: view.
_INHERITED_FROM_WEST_BUILD = {"--board", "--shield"}


def _declared_options() -> set[str]:
    """Every long option the three real surfaces declare: rigc's own
    parser (interrogated), plus the two west commands and the shared
    resolver argument block (scanned). A fresh set the caller owns."""
    found: set[str] = set()
    for action in _expand_parser()._actions:
        found.update(opt for opt in action.option_strings if opt.startswith("--"))
    for path in WEST_COMMANDS:
        found.update(_DECL_RE.findall(path.read_text()))
    found.update(_DECL_RE.findall(_shared_resolver_args()))
    found.discard("--help")
    return found


def _expand_parser() -> argparse.ArgumentParser:
    """The `expand` SUBparser out of rigc's own real parser. argparse
    offers no public route to a registered subparser, so this reaches for
    `_SubParsersAction.choices` -- the narrowest private touch available,
    and preferable to a second text scan: what this test wants is the
    surface argv is actually checked against, not the surface cli.py's
    source appears to declare."""
    for action in build_parser()._actions:
        if isinstance(action, argparse._SubParsersAction):
            return action.choices["expand"]
    raise AssertionError("rigc.cli.build_parser() registers no subcommands")


def _shared_resolver_args() -> str:
    """The source text of list_rigs.LIST_RIGS_SHARED_FUNC alone. An AST
    walk rather than a line-range slice, so moving the function inside its
    module cannot silently reduce this to an empty scan (which would make
    the forward check below pass by finding nothing)."""
    tree = ast.parse(LIST_RIGS.read_text())
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == LIST_RIGS_SHARED_FUNC:
            segment = ast.get_source_segment(LIST_RIGS.read_text(), node)
            assert segment, f"could not recover the source of {LIST_RIGS_SHARED_FUNC}"
            return segment
    raise AssertionError(
        f"{LIST_RIGS.name} declares no {LIST_RIGS_SHARED_FUNC}() any more -- "
        "west rigs shares its parser arguments with something else now, and "
        "this test is scanning nothing"
    )


def _documented_options() -> set[str]:
    """Every option token anywhere on the page, prose included."""
    return set(_DOC_RE.findall(DOC_PAGE.read_text()))


def _documented_entries() -> set[str]:
    """Every option with an ENTRY of its own on the page: a list-table
    row's first cell, or a definition-list term (an option at column 0
    whose next line is indented -- reST's own definition of one). A subset
    of `_documented_options()`."""
    found: set[str] = set()
    lines = DOC_PAGE.read_text().splitlines()
    for i, line in enumerate(lines):
        cell = _DOC_CELL_RE.match(line)
        if cell:
            found.add(cell.group(1))
            continue
        term = _DOC_TERM_RE.match(line)
        if not term:
            continue
        following = lines[i + 1] if i + 1 < len(lines) else ""
        if following.strip() and following[:1].isspace():
            found.add(term.group(1))
    return found


def test_commands_page_documents_something_at_all() -> None:
    """The negative control: an empty or renamed page would make the
    reverse check below trivially true. Both real parsers contribute a
    dozen options between them, so a page naming a handful is already
    wrong."""
    entries = _documented_entries()
    assert len(entries) >= 10, (
        f"doc/reference/commands.rst gives an entry to only {sorted(entries)}"
    )


def test_cli_reference_forward_every_option_is_documented() -> None:
    """Every long option of `rigc expand` and `west rigs` has its own
    entry on doc/reference/commands.rst -- not merely a mention somewhere
    in its prose."""
    missing = sorted(_declared_options() - _documented_entries())
    assert not missing, (
        f"option(s) declared by a real parser and absent from doc/reference/commands.rst: {missing}"
    )


def test_cli_reference_reverse_every_documented_option_is_real() -> None:
    """Every option the page names is one a real parser declares, or one
    inherited from `west build`. Catches a page that outlived a rename."""
    invented = sorted(_documented_options() - _declared_options() - _INHERITED_FROM_WEST_BUILD)
    assert not invented, (
        f"doc/reference/commands.rst names option(s) no parser declares: {invented}"
    )


# --------------------------------------------- west SUBCOMMAND vocabulary
# The narrower law described at the top of this module's docstring: every
# `west <subcommand>` named anywhere under doc/ is either declared by this
# repo, or a real command of upstream west itself.

#: A `west <subcommand>` invocation at a shell prompt inside a
#: `.. code-block:: console` block -- this doc set's own convention for a
#: runnable example.
_DOC_WEST_PROMPT_RE = re.compile(r"^\s*\$\s+west\s+([a-z][a-z0-9_-]*)", re.MULTILINE)

#: The same, as a double-backtick inline literal -- this doc set's own
#: convention for naming a command in running prose or a heading
#: (`` ``west build`` ``, `` ``west rigs`` ``).
_DOC_WEST_LITERAL_RE = re.compile(r"``west\s+([a-z][a-z0-9_-]*)")


def _repo_declared_west_commands() -> set[str]:
    """Every subcommand name THIS repo's own scripts/west-commands.yml
    declares -- `rigs`, today. Read the same way west itself reads it
    (yaml, the `west-commands:` -> `commands:` -> `name:` shape), never
    hardcoded, so a second command added here is picked up automatically."""
    manifest = REPO_ROOT / "scripts" / "west-commands.yml"
    data = yaml.safe_load(manifest.read_text())
    return {cmd["name"] for entry in data["west-commands"] for cmd in entry["commands"]}


def _upstream_west_builtin_commands() -> set[str]:
    """Every command name west's OWN package ships built in -- `init`,
    `update`, `list`, `manifest`, ... Interrogated by instantiating each
    class `west.app.main.BUILTIN_COMMAND_GROUPS` registers and reading its
    real `.name`, rather than a spelled-out list: west is already a real
    dependency of this codebase (scripts/west_commands/rigs.py imports
    `west.commands`), and this import touches only the west PACKAGE, never
    a Zephyr tree -- unlike importing rigs.py itself (see this module's
    own docstring for why THAT import is avoided)."""
    from west.app.main import BUILTIN_COMMAND_GROUPS

    # west ships no stub for this module, and the dict LITERAL's own
    # inferred type collapses its heterogeneous class lists to `object`
    # (not iterable, so far as mypy is concerned) -- cast once, here,
    # to the shape west's own __init__ already relies on (`for group,
    # classes in BUILTIN_COMMAND_GROUPS.items(): [cls() for cls in
    # classes]`) rather than let that untyped collapse leak into a
    # `# type: ignore` at every call site.
    groups = cast(dict[str, list[Any]], BUILTIN_COMMAND_GROUPS)
    return {cls().name for cls_list in groups.values() for cls in cls_list}


def _upstream_west_extension_commands() -> set[str]:
    """Every command name Zephyr ITSELF contributes as a west extension --
    `build`, `flash`, `boards`, `shields`, ... -- read from
    `$ZEPHYR_BASE/scripts/west-commands.yml`, the identical manifest shape
    `_repo_declared_west_commands()` reads for this repo's own one command.
    Real data from the pinned Zephyr tree, never a spelled-out list that
    would silently fall behind whichever version of Zephyr this workspace
    pins."""
    manifest = Path(zephyr_base()) / "scripts" / "west-commands.yml"
    data = yaml.safe_load(manifest.read_text())
    return {cmd["name"] for entry in data["west-commands"] for cmd in entry["commands"]}


def _known_west_commands() -> set[str]:
    """The union of all three real sources: this repo's own, west's
    builtins, and Zephyr's own extensions. A fresh set the caller owns."""
    return (
        _repo_declared_west_commands()
        | _upstream_west_builtin_commands()
        | _upstream_west_extension_commands()
    )


def _doc_west_mentions() -> set[str]:
    """Every `west <subcommand>` mentioned anywhere under
    doc/bridle/rigs4zephyr/, in either of the two shapes this doc set
    actually spells a command in (a `$ west ...` prompt line, or a
    `` ``west ...`` `` inline literal) -- never a bare "west" in running
    prose, which names no subcommand at all. A fresh set the caller
    owns."""
    found: set[str] = set()
    for page in sorted(RIGS_DOC_ROOT.rglob("*.rst")):
        if "_build" in page.parts:
            continue
        text = page.read_text()
        found.update(_DOC_WEST_PROMPT_RE.findall(text))
        found.update(_DOC_WEST_LITERAL_RE.findall(text))
    return found


def test_doc_mentions_a_west_subcommand_at_all() -> None:
    """The negative control: an empty doc/ tree, or a regex that matched
    nothing, would make the check below trivially pass. This doc set
    mentions `west build` and `west rigs` a couple dozen times between
    them across the tutorials and the reference pages, so a floor of 2
    (one for each) is already a real, non-vacuous assertion -- run the
    mutation below; do not reason about it."""
    mentions = _doc_west_mentions()
    assert len(mentions) >= 2, (
        f"doc/ mentions only {sorted(mentions)} west subcommand(s) in the "
        "prompt/inline-literal shapes this scan looks for -- the regex is "
        "very likely finding far fewer mentions than are actually there"
    )


def test_doc_never_names_a_retired_or_invented_west_subcommand() -> None:
    """Every `west <subcommand>` named anywhere under doc/ is either
    declared by this repo's own scripts/west-commands.yml, or a real
    command of upstream west (built in, or contributed by Zephyr's own
    extension manifest). This is the check that would have caught `west
    build-rig` surviving in four tutorial pages after the command itself
    was retired -- see this module's own docstring."""
    invented = sorted(_doc_west_mentions() - _known_west_commands())
    assert not invented, (
        "doc/ names west subcommand(s) that are neither declared by this "
        "repo's scripts/west-commands.yml nor a real command of upstream "
        f"west: {invented}"
    )
