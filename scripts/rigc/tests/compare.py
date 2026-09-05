# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Structural comparison of generated artifacts against their actual
contracts, never their bytes.

context.cmake's contract is a key -> value mapping cmake/modules/dts.cmake
include()s. RIG_DEPENDS denotes a SET of dependency paths --
cmake/modules/dts.cmake only ever appends the whole list to
CMAKE_CONFIGURE_DEPENDS, which cares which files it depends on, never in
what order the eager scan visited them. RIG_SHIELDS stays an ORDERED
list (documented as distinct-in-rig-order, and dts.cmake iterates it);
every other variable is an ordinary scalar. Comment lines carry no
contract for this artifact -- the only comment context.cmake has is the
provenance banner.

config-sheet.md's contract is the facts a human reader relies on: which
instance sits on which socket, which address, which CS index, which
strap state -- never its rendering. Heading wording, table column-header
text, and a section's own surrounding prose are free to change; every
datum (instance, shield, socket, device, address, index, position name,
controller, channel, state, property, value) is pinned, and section
presence is compared as a SET while each section's rows are compared as
an ORDERED list (the emitter sorts them deterministically, so a
reordering is a real regression, not noise).

rig-gen.overlay is not compared here at all in the structural sense the
two artifacts above are: it is a cpp fragment (an unresolved #include,
unresolved <MACRO> tokens, &label references that only the board's own
devicetree can resolve), not a parseable devicetree, so its SEMANTICS
ride the existing zephyr.dts + dts_equiv.py comparison instead -- already
post-resolution, and strictly stronger than any overlay-only comparator
could be. compare_overlay targets only the three facts that VANISH on
resolution and that dts_equiv.py therefore cannot see: a rig-assigned
param's verbatim macro token (zephyr.dts shows only the resolved
number), the quoted #include that must open the file for the needed
param-includes headers to resolve with no -I plumbing, and the
human-facing comments (gpio position/inverted annotations, the PWM/ADC
pinctrl note) dtlib discards entirely when parsing. One golden directory
(shield-uart-subset-frdm) has no zephyr.dts at all and stays
byte-compared instead -- overlay_is_byte_compared names that exception.

rig-gen-includes.dtsi's contract is the ORDERED list of headers a rig's
own parameter assignments actually need (emitter._needed_param_includes,
the union of the owning shield devices' own
declared_param_includes) -- cpp include order can matter (a later header
may depend on macros an earlier one defines), so this is a list, never a
set, unlike RIG_DEPENDS above. The provenance banner is its only comment
and carries no contract, same as the other two artifacts.

Every function in this module is pure over the text values it is given;
IO (reading the golden, running the tool under test) stays at the
conftest seam that calls compare_context_cmake / compare_config_sheet,
so this module needs no pytest import and a unit test can exercise it
with no golden file and no subprocess.
"""

from __future__ import annotations

import itertools
import re
from dataclasses import dataclass

_SET_HEAD_RE = re.compile(r'set\((\w+)\s*"')


class ContextCmakeParseError(ValueError):
    """Raised by parse_context_cmake when a line is neither a comment nor
    a set(VAR "value") assignment. An unrecognized shape must never be
    silently skipped: dropping it would let a truncated or malformed
    artifact compare equal to whatever mapping the rest of the file
    happened to produce."""


def _scan_quoted_value(line: str, start: int) -> tuple[str, int]:
    """Scan a set(VAR "...")'s quoted value, starting right after the
    opening quote, honoring CMake's backslash escaping so an escaped
    quote never terminates the value early.

    Returns the value's raw text (escapes left intact -- unescaping is
    the concern of whoever interprets a specific variable's contract,
    not of finding where the literal ends) and the index of the line
    immediately after the closing quote."""
    chars: list[str] = []
    i = start
    escaped = False
    while i < len(line):
        ch = line[i]
        if escaped:
            chars.append(ch)
            escaped = False
        elif ch == "\\":
            chars.append(ch)
            escaped = True
        elif ch == '"':
            return "".join(chars), i + 1
        else:
            chars.append(ch)
        i += 1
    raise ContextCmakeParseError(f"unterminated quoted value: {line!r}")


def parse_context_cmake(text: str) -> dict[str, str]:
    """Parse context.cmake source into {VAR: raw value}, one entry per
    set(VAR "value") line. VAR is verbatim; value is the literal quoted
    content with CMake's list-escaping (backslash-backslash, backslash-
    quote, backslash-semicolon) left INTACT -- only RIG_DEPENDS' contract
    needs it interpreted as a list (split_dependency_set, below, is the
    one caller that does), every other variable's contract is the raw
    string itself.

    Comment lines (leading "#", after stripping surrounding whitespace)
    and blank lines are ignored. Every other line must be exactly one
    set(VAR "value") assignment; anything else raises
    ContextCmakeParseError rather than being dropped.

    Returns a fresh dict the caller owns; text is read-only and never
    mutated."""
    mapping: dict[str, str] = {}
    for lineno, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = _SET_HEAD_RE.match(line)
        if match is None:
            raise ContextCmakeParseError(
                f"line {lineno}: not a comment or a set(VAR \"value\") assignment: {raw_line!r}"
            )
        name = match.group(1)
        value, end = _scan_quoted_value(line, match.end())
        if line[end:] != ")":
            raise ContextCmakeParseError(
                f"line {lineno}: trailing content after the closing quote: {raw_line!r}"
            )
        mapping[name] = value
    return mapping


def split_dependency_set(raw_value: str) -> frozenset[str]:
    """Split RIG_DEPENDS' raw (still list-escaped) value into its
    dependency-path elements, undoing emitter/context.py's
    _cmake_list_escape per element in one left-to-right scan -- so an
    escaped semicolon inside a path is never mistaken for a delimiter,
    and the delimiters themselves never leak into an element.

    Returned as a frozenset: RIG_DEPENDS is a SET by contract, and a
    dependency listed twice is exactly as satisfied as one listed once."""
    elements: list[str] = []
    current: list[str] = []
    escaped = False
    for ch in raw_value:
        if escaped:
            current.append(ch)
            escaped = False
        elif ch == "\\":
            escaped = True
        elif ch == ";":
            elements.append("".join(current))
            current = []
        else:
            current.append(ch)
    elements.append("".join(current))
    return frozenset(elements)


# The one variable whose contract is a SET rather than a scalar (or, for
# RIG_SHIELDS, an order-sensitive list compared as the plain string it
# is -- see the module docstring).
_UNORDERED_SET_VARS = frozenset({"RIG_DEPENDS"})


def compare_context_cmake(expected: str, actual: str) -> str | None:
    """Compare two context.cmake texts against the artifact's real
    contract instead of byte-for-byte:

    * RIG_DEPENDS compares as a SET -- reordering its entries is not a
      mismatch; a missing or an extra entry is.
    * every other variable (RIG_NAME, RIG_BOARD, RIG_SHIELDS,
      RIG_REVISION, RIG_VARIANT, RIG_SHIELD_REVISIONS) compares as an
      ordinary scalar, exact-match -- RIG_SHIELDS included: it is
      documented as distinct-in-rig-order and dts.cmake iterates it, so
      treating it as a set would hide a real ordering regression.
    * a variable declared on one side and absent on the other is always
      a mismatch. RIG_REVISION/RIG_VARIANT/RIG_SHIELD_REVISIONS follow
      the "no declaration, no artifact" rule (emitter/context.py), so
      their absence is meaningful, never incidental.

    Returns None when the two texts are contract-equivalent; otherwise a
    human-readable report of every mismatch found (not just the first),
    with RIG_DEPENDS' own mismatch broken down into missing/unexpected
    entries. Text that fails to parse at all is reported as a mismatch
    too, never raised past this function, so a caller can treat "the
    golden doesn't parse" and "the golden doesn't match" uniformly."""
    try:
        expected_vars = parse_context_cmake(expected)
    except ContextCmakeParseError as exc:
        return f"golden context.cmake failed to parse: {exc}"
    try:
        actual_vars = parse_context_cmake(actual)
    except ContextCmakeParseError as exc:
        return f"actual context.cmake failed to parse: {exc}"

    problems: list[str] = []
    for name in sorted(set(expected_vars) | set(actual_vars)):
        if name not in actual_vars:
            problems.append(f"{name}: present in golden, absent from actual")
            continue
        if name not in expected_vars:
            problems.append(
                f"{name}: absent from golden, present in actual ({actual_vars[name]!r})"
            )
            continue
        if name in _UNORDERED_SET_VARS:
            expected_set = split_dependency_set(expected_vars[name])
            actual_set = split_dependency_set(actual_vars[name])
            if expected_set != actual_set:
                missing = sorted(expected_set - actual_set)
                unexpected = sorted(actual_set - expected_set)
                parts = []
                if missing:
                    parts.append("missing: " + ", ".join(missing))
                if unexpected:
                    parts.append("unexpected: " + ", ".join(unexpected))
                problems.append(f"{name}: " + "; ".join(parts))
        elif expected_vars[name] != actual_vars[name]:
            problems.append(
                f"{name}: golden {expected_vars[name]!r} != actual {actual_vars[name]!r}"
            )
    if not problems:
        return None
    return "\n".join(problems)


# --------------------------------------------------------------------------
# config-sheet.md: a fact sheet, not a byte sequence.


class ConfigSheetParseError(ValueError):
    """Raised by parse_config_sheet when a non-blank line matches none of
    the sheet's recognised shapes (title, banner, board line, section
    heading, table header/separator/row, a section's own bullet form, or
    a single tolerated paragraph between a heading and that section's
    first row). An unrecognised line must never be silently skipped: that
    is exactly how a fact extractor drops a fact while still reporting
    green.

    The prose tolerance is deliberately ASYMMETRIC and bounded to one
    paragraph per section (_parse_section_body enforces both): prose
    BEFORE a section's rows is never compared, prose AFTER them is a
    parse error."""


@dataclass
class ConfigSheetFacts:
    """The facts one config-sheet.md carries: read-only once returned by
    parse_config_sheet, and owned by the caller.

    rig_name/board come from the header block. sections maps a SECTION
    KIND (one of "socket_assignment", "straps_jumpers", "chip_selects",
    "pwm", "wires", "parameters") to its rows, each row a tuple of the
    data fields that section's bullet or table form carries -- in the
    ORDER the document presents them, because the emitter sorts rows
    deterministically and a swap is a real regression. Which kinds are
    present is compared as a SET; only a kind common to both documents
    has its row order compared."""

    rig_name: str
    board: str
    sections: dict[str, tuple[tuple[str, ...], ...]]


_TITLE_RE = re.compile(r"^#\s+.*`(?P<name>[^`]+)`\s*$")
_BANNER_RE = re.compile(r"^<!--.*-->$")
_BOARD_RE = re.compile(r"^Board: \*\*(?P<board>.+)\*\*$")
_HEADING_RE = re.compile(r"^##\s+\S")

_STRAP_RE = re.compile(
    r"^- \*\*(?P<inst>[^*]+)\*\* \((?P<socket>[^)]+)\): set \*\*(?P<label>[^*]+)\*\* "
    r"to state (?P<state>\S+) → device address (?P<addr>0x[0-9a-fA-F]+)$"
)
_JUMPER_RE = re.compile(
    r"^- \*\*(?P<inst>[^*]+)\*\* \((?P<socket>[^)]+)\): set \*\*(?P<label>[^*]+)\*\* "
    r"to state (?P<state>\S+) → routed to pin (?P<pos>\S+)$"
)
_PWM_RE = re.compile(
    r"^- (?P<inst>[^/]+)/(?P<dev>\S+) \((?P<socket>\S+) (?P<pos>[^)]+)\) → "
    r"(?P<fn>[A-Z]+) (?P<ctrl>\S+) ch(?P<ch>\d+): mux the pin to the controller$"
)
_WIRE_RE = re.compile(r"^- connect \*\*(?P<frm>[^*]+)\*\* → \*\*(?P<to>[^*]+)\*\* — (?P<route>.+)$")
_CS_RE = re.compile(
    r"^- (?P<inst>[^/]+)/(?P<dev>[^:]+): CS index (?P<index>\d+), (?P<pos>\S+)"
    r"(?: → SoC (?P<ctrl>\S+) pin (?P<pin>\S+))?$"
)


def _split_table_row(line: str, lineno: int) -> tuple[str, ...]:
    """Split one "| a | b | c |" line into its cell values, stripped.
    Column HEADER TEXT is never the contract -- only how many
    columns a row carries, which is what tells socket-assignment's table
    apart from parameters' -- so callers read cell values, never the
    header row's own text."""
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|") and len(stripped) >= 2):
        raise ConfigSheetParseError(f"line {lineno}: not a table row: {line!r}")
    return tuple(cell.strip() for cell in stripped[1:-1].split("|"))


def _is_table_separator(line: str) -> bool:
    """True for a markdown table separator row ("|---|---|---|", any run
    of "-"/":" per cell) -- checked structurally rather than via
    _split_table_row so a malformed line here is "not a separator",
    never a parse exception raised from the wrong call site."""
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|") and len(stripped) >= 2):
        return False
    cells = stripped[1:-1].split("|")
    return all(cell.strip() != "" and set(cell.strip()) <= {"-", ":"} for cell in cells)


def _match_bullet(line: str, lineno: int) -> tuple[str, tuple[str, ...]]:
    """Match one bullet line against every recognised shape and return
    (section kind, fact tuple). Raises ConfigSheetParseError when none of
    the shapes match -- an unrecognised bullet is a mismatch, never a
    line the section silently drops."""
    m = _STRAP_RE.match(line)
    if m is not None:
        return "straps_jumpers", (
            "strap",
            m.group("inst"),
            m.group("socket"),
            m.group("label"),
            m.group("state"),
            m.group("addr"),
        )
    m = _JUMPER_RE.match(line)
    if m is not None:
        return "straps_jumpers", (
            "jumper",
            m.group("inst"),
            m.group("socket"),
            m.group("label"),
            m.group("state"),
            m.group("pos"),
        )
    m = _PWM_RE.match(line)
    if m is not None:
        return "pwm", (
            m.group("inst"),
            m.group("dev"),
            m.group("socket"),
            m.group("pos"),
            m.group("fn"),
            m.group("ctrl"),
            m.group("ch"),
        )
    m = _WIRE_RE.match(line)
    if m is not None:
        return "wires", (m.group("frm"), m.group("to"), m.group("route"))
    m = _CS_RE.match(line)
    if m is not None:
        return "chip_selects", (
            m.group("inst"),
            m.group("dev"),
            m.group("index"),
            m.group("pos"),
            m.group("ctrl") or "",
            m.group("pin") or "",
        )
    raise ConfigSheetParseError(f"line {lineno}: unrecognised bullet: {line!r}")


def _parse_table_section(
    lines: list[str],
    i: int,
    n: int,
) -> tuple[str, tuple[tuple[str, ...], ...], int]:
    header_lineno = i + 1
    header_cells = _split_table_row(lines[i], i + 1)
    ncols = len(header_cells)
    i += 1
    if i >= n or not _is_table_separator(lines[i]):
        raise ConfigSheetParseError(
            f"line {i + 1}: expected a table separator row after the header"
        )
    i += 1
    rows: list[tuple[str, ...]] = []
    while i < n and lines[i].strip() != "" and lines[i].lstrip().startswith("|"):
        row = _split_table_row(lines[i], i + 1)
        if len(row) != ncols:
            raise ConfigSheetParseError(
                f"line {i + 1}: table row carries {len(row)} columns, "
                f"header carries {ncols}: {lines[i]!r}"
            )
        rows.append(row)
        i += 1
    if ncols == 3:
        kind = "socket_assignment"
    elif ncols == 4:
        kind = "parameters"
    else:
        raise ConfigSheetParseError(f"line {header_lineno}: unrecognised {ncols}-column table")
    return kind, tuple(rows), i


def _parse_bullet_section(
    lines: list[str],
    i: int,
    n: int,
) -> tuple[str, tuple[tuple[str, ...], ...], int]:
    kind: str | None = None
    rows: list[tuple[str, ...]] = []
    while i < n and lines[i].strip() != "" and lines[i].lstrip().startswith("- "):
        bullet_kind, fact = _match_bullet(lines[i].strip(), i + 1)
        if kind is None:
            kind = bullet_kind
        elif bullet_kind != kind:
            raise ConfigSheetParseError(
                f"line {i + 1}: bullet shape {bullet_kind!r} mixed into a "
                f"{kind!r} section: {lines[i]!r}"
            )
        rows.append(fact)
        i += 1
    assert kind is not None  # caller only enters here on a line starting "- "
    return kind, tuple(rows), i


def _skip_blank(lines: list[str], i: int, n: int) -> int:
    while i < n and lines[i].strip() == "":
        i += 1
    return i


def _parse_section_body(
    lines: list[str],
    i: int,
    n: int,
) -> tuple[str, tuple[tuple[str, ...], ...], int]:
    """Dispatch a section's body by its actual shape, never its heading
    text (heading wording is never the contract). A table starts with
    "|"; bullets start with "- ".

    Prose is tolerated in exactly ONE place and never compared: a single
    paragraph between a heading and that section's first row (the PWM
    section's own intro is the only one the emitter produces today). The
    bound is enforced here rather than merely described -- a SECOND
    paragraph, or prose appearing anywhere after a section's rows, is an
    unmatched line like any other. Without the bound, arbitrary text
    could sit at the head of every section, including a sentence
    contradicting the facts below it, and still compare equal."""
    if lines[i].lstrip().startswith("|"):
        return _parse_table_section(lines, i, n)
    if lines[i].lstrip().startswith("- "):
        return _parse_bullet_section(lines, i, n)

    prose_start = i
    j = i
    while (
        j < n
        and lines[j].strip() != ""
        and not lines[j].lstrip().startswith("- ")
        and not lines[j].lstrip().startswith("|")
        and not _HEADING_RE.match(lines[j])
    ):
        j += 1
    j = _skip_blank(lines, j, n)
    if j >= n or _HEADING_RE.match(lines[j]):
        raise ConfigSheetParseError(
            f"line {prose_start + 1}: prose paragraph not followed by any "
            f"recognised table or bullet: {lines[prose_start]!r}"
        )
    if lines[j].lstrip().startswith("|"):
        return _parse_table_section(lines, j, n)
    if lines[j].lstrip().startswith("- "):
        return _parse_bullet_section(lines, j, n)
    raise ConfigSheetParseError(
        f"line {j + 1}: a section tolerates at most ONE intro paragraph "
        f"before its rows: {lines[j]!r}"
    )


def parse_config_sheet(text: str) -> ConfigSheetFacts:
    """Parse config-sheet.md into the facts it carries: the header block
    (rig name from the title's backtick-quoted name, and the board line)
    plus every section's rows, keyed by section KIND rather than its
    (tolerated, reworded-at-will) heading text.

    The provenance banner comment is recognised structurally (it must be
    present, right after the title) but its own text is never read --
    the tool-identity leak this comparator exists to stop mattering.

    Every non-blank line must be consumed by exactly one recogniser;
    anything else raises ConfigSheetParseError rather than being
    dropped, so a truncated or malformed artifact can never compare
    equal to whatever facts the rest of the document happens to carry.

    Returns a fresh ConfigSheetFacts the caller owns; text is read-only."""
    lines = text.splitlines()
    n = len(lines)

    def skip_blank(i: int) -> int:
        return _skip_blank(lines, i, n)

    i = skip_blank(0)
    if i >= n:
        raise ConfigSheetParseError("empty document")
    m = _TITLE_RE.match(lines[i])
    if m is None:
        raise ConfigSheetParseError(
            f"line {i + 1}: expected a title line carrying the rig name in backticks: {lines[i]!r}"
        )
    rig_name = m.group("name")
    i = skip_blank(i + 1)

    if i >= n or _BANNER_RE.match(lines[i]) is None:
        raise ConfigSheetParseError(
            "expected the provenance banner comment (<!-- ... -->) after the title"
        )
    i = skip_blank(i + 1)

    if i >= n:
        raise ConfigSheetParseError("expected a Board: **<board>** line")
    m = _BOARD_RE.match(lines[i])
    if m is None:
        raise ConfigSheetParseError(
            f"line {i + 1}: expected a Board: **<board>** line: {lines[i]!r}"
        )
    board = m.group("board")
    i = skip_blank(i + 1)

    sections: dict[str, tuple[tuple[str, ...], ...]] = {}
    while i < n:
        if not _HEADING_RE.match(lines[i]):
            raise ConfigSheetParseError(
                f"line {i + 1}: expected a ## section heading: {lines[i]!r}"
            )
        heading_lineno = i + 1
        i = skip_blank(i + 1)
        if i >= n:
            raise ConfigSheetParseError(f"section heading at line {heading_lineno} has no body")
        kind, rows, i = _parse_section_body(lines, i, n)
        if kind in sections:
            raise ConfigSheetParseError(f"section kind {kind!r} appears more than once")
        sections[kind] = rows
        i = skip_blank(i)

    return ConfigSheetFacts(rig_name=rig_name, board=board, sections=sections)


def _describe_section_mismatch(
    kind: str, expected_rows: tuple[tuple[str, ...], ...], actual_rows: tuple[tuple[str, ...], ...]
) -> str:
    lines = [f"section {kind!r}: rows differ (order is contract)"]
    for idx, (exp, act) in enumerate(
        itertools.zip_longest(expected_rows, actual_rows, fillvalue=None)
    ):
        if exp != act:
            lines.append(f"  row {idx}: golden {exp!r} != actual {act!r}")
    return "\n".join(lines)


def compare_config_sheet(expected: str, actual: str) -> str | None:
    """Compare two config-sheet.md texts against the sheet's real
    contract -- the facts a reader relies on -- instead of byte-for-byte:

    * the rig name (from the title) and the board line compare exact.
    * which SECTION KINDS are present compares as a SET: a missing or
      extra section is a mismatch regardless of where it would have
      sorted.
    * within a section common to both documents, rows compare as an
      ORDERED list -- the emitter sorts them deterministically, so a
      reordering is a real regression, not noise.
    * heading wording, table column-header text, and the single paragraph
      a section may carry between its heading and its first row are read
      structurally and never compared as text; the provenance banner is
      recognised as present but never read at all. Section ORDER is not
      compared either, since section presence is a set -- a deliberate
      loosening relative to byte comparison.

    Returns None when the two texts are contract-equivalent; otherwise a
    human-readable report of every mismatch found (not just the first).
    Text that fails to parse at all is reported as a mismatch too, never
    raised past this function, so a caller can treat "the golden doesn't
    parse" and "the golden doesn't match" uniformly."""
    try:
        expected_facts = parse_config_sheet(expected)
    except ConfigSheetParseError as exc:
        return f"golden config-sheet.md failed to parse: {exc}"
    try:
        actual_facts = parse_config_sheet(actual)
    except ConfigSheetParseError as exc:
        return f"actual config-sheet.md failed to parse: {exc}"

    problems: list[str] = []
    if expected_facts.rig_name != actual_facts.rig_name:
        problems.append(
            f"rig name: golden {expected_facts.rig_name!r} != actual {actual_facts.rig_name!r}"
        )
    if expected_facts.board != actual_facts.board:
        problems.append(f"board: golden {expected_facts.board!r} != actual {actual_facts.board!r}")

    expected_kinds = set(expected_facts.sections)
    actual_kinds = set(actual_facts.sections)
    for kind in sorted(expected_kinds - actual_kinds):
        problems.append(f"section {kind!r}: present in golden, absent from actual")
    for kind in sorted(actual_kinds - expected_kinds):
        problems.append(f"section {kind!r}: absent from golden, present in actual")
    for kind in sorted(expected_kinds & actual_kinds):
        expected_rows = expected_facts.sections[kind]
        actual_rows = actual_facts.sections[kind]
        if expected_rows != actual_rows:
            problems.append(_describe_section_mismatch(kind, expected_rows, actual_rows))

    if not problems:
        return None
    return "\n".join(problems)


# --------------------------------------------------------------------------
# rig-gen.overlay's contract is split across two comparisons. This
# module deliberately does NOT parse the overlay into a devicetree -- it
# cannot: cpp has not run, so #include/<MACRO> are still unresolved, and
# &label references only the board's own devicetree can chase. Semantics
# ride the zephyr.dts + dts_equiv.py comparison instead; what follows
# targets only the facts that comparison structurally cannot see, because
# they no longer exist once cpp and dtc have resolved everything.

# emitter/overlay.py's own docstring: "rig-gen.overlay stays readable
# (zephyr,code = <INPUT_KEY_1>;, not a bare number)" -- _instance_extra_
# props renders a rig-assigned param as "<name> = <TOKEN>;" with TOKEN the
# raw, unresolved identifier. Deliberately excludes a bare numeric literal
# (reg = <0x48>;, an int authored directly) and a phandle reference
# (gpios = <&label ...>;, has a "&"), neither of which is this contract.
_PARAM_TOKEN_RE = re.compile(
    r"^\s*(?P<name>[\w,.\-]+) = <(?P<token>[A-Za-z_]\w*)>;\s*$", re.MULTILINE
)

# The quoted include that must open the file (emitter/overlay.py:
# render_overlay, emitted if and only if emitter._needed_param_includes(rig) is
# non-empty) -- quoted-include resolution against the file's OWN directory
# is what lets rig-gen.overlay
# and rig-gen-includes.dtsi simply sit side by side in <build>/rig/ with
# no -I plumbing; a displaced or missing include line breaks exactly that.
_INCLUDES_LINE = '#include "rig-gen-includes.dtsi"'

# _device_node/_collection_entry's shared trailing-comment idiom (emitter/
# overlay.py): a property assignment ending "...>;", a literal tab, then
# "/* <posname>[ inverted] */" on the SAME physical line -- the gpio/pwm/
# adc position annotation. Distinct in shape from the multi-line
# provenance banner (never follows a ">;") and from _synth_nexus_nodes'
# standalone comment (not a property-assignment line), so neither is
# mistaken for one of these.
#
# The POSITION CELL is captured alongside the comment so the two are
# compared as a pair. A comment naming a pin the ref did not resolve to is
# the one way this artifact can lie to the human reading it, and a
# resolved zephyr.dts cannot see comments at all, so nothing else in the
# suite could notice. The node LABEL stays uncaptured (&\w+ matches it
# without binding it), which is what keeps the parked label scheme free.
_ANNOTATION_RE = re.compile(
    r"^\s*(?P<prop>[\w,.\-]+) = <&\w+ (?P<pos>\d+)[^>]*>;\t(?P<comment>/\*[^*]*\*/)\s*$",
    re.MULTILINE,
)

# emitter/overlay.py's cs-gpios cell list carries its own inline
# "/* ACTIVE_LOW */" per entry -- inside the cell, not after a ">;", so the
# annotation idiom above cannot see it. Present in 11 of the 19 overlay
# goldens: the numeric flag survives into zephyr.dts and is compared
# there, but the human-readable annotation exists only here.
_CS_FLAG_RE = re.compile(r"<&(?:\w+) \d+ 1 (/\* ACTIVE_LOW \*/)>")

# emitter/overlay.py's _controllers(): fixed, non-templated text (only the
# controller names rendered below it vary per rig) -- present whenever the
# rig resolved any PWM/ADC claim at all. Character-for-character, matching
# tests/unit/emitter/test_overlay.py's own frozen assertion of the same
# string, em dash included.
_PINCTRL_NOTE = (
    "/* PWM/ADC: enable the resolved controllers; the pin-mux (pinctrl)\n"
    " * for each muxed pin is board-provided and must be applied —\n"
    " * stubbed here, see the config sheet. */"
)

# The one accept rig with a rig-gen.overlay golden but no zephyr.dts (no
# tier-2 build), so under the split contract it would otherwise lose
# semantic checking entirely -- kept
# byte-compared as an explicit, interim exception. Retire this constant
# once shield-uart-subset-frdm gets a tier-2 build.
_BYTE_COMPARED_OVERLAY_RIGS = frozenset({"shield-uart-subset-frdm"})


def overlay_is_byte_compared(rig_name: str) -> bool:
    """True for the one golden directory (named by its boards/rigs/ or
    synthetic-fixture folder) whose rig-gen.overlay stays byte-compared
    rather than routed through compare_overlay: it has no zephyr.dts
    golden, so no resolved devicetree stands behind it.

    That overlay carries no devicetree content today -- it is the
    provenance banner and nothing else, since the rig exists to exercise
    subset-exposure acceptance -- so the exception costs nothing and buys
    nothing measurable either way. It keeps the artifact byte-frozen
    against the day it gains content, and retires when a tier-2 build for
    that rig can protect real content instead. Every other rig's overlay
    compares through compare_overlay."""
    return rig_name in _BYTE_COMPARED_OVERLAY_RIGS


def _param_tokens(text: str) -> frozenset[tuple[str, str]]:
    """Every (property name, verbatim macro token) pair rig-gen.overlay
    carries -- a token that has been resolved to a bare number, or
    dropped outright, is simply absent from the returned set; there is
    nothing to parse-fail on, since this artifact is not otherwise parsed
    at all."""
    return frozenset((m.group("name"), m.group("token")) for m in _PARAM_TOKEN_RE.finditer(text))


def _annotation_comments(text: str) -> frozenset[tuple[str, str, str]]:
    """Every gpio/pwm/adc trailing annotation rig-gen.overlay carries, as
    (property name, position cell, literal "/* ... */" comment) triples,
    plus each cs-gpios entry's inline ACTIVE_LOW annotation as a
    ("cs-gpios", position, comment) triple.

    Returned as a set, so node/property REORDERING never affects it, while
    the property-and-position binding still ties each comment to the pin
    it claims to describe. Compared for EQUALITY by the caller, not
    containment: an annotation the artifact gained is as much a defect as
    one it lost, since a spurious comment misinforms a reader exactly like
    a wrong one."""
    triples = {
        (m.group("prop"), m.group("pos"), m.group("comment")) for m in _ANNOTATION_RE.finditer(text)
    }
    triples |= {("cs-gpios", m.group(0).split()[1], m.group(1)) for m in _CS_FLAG_RE.finditer(text)}
    return frozenset(triples)


def compare_overlay(expected: str, actual: str) -> str | None:
    """Compare two rig-gen.overlay texts against only the facts this
    artifact carries that a post-resolution zephyr.dts comparison
    structurally cannot see -- everything else (node/property presence,
    ordering, whitespace, the provenance banner) is free to differ, since
    the SEMANTICS this artifact denotes are asserted elsewhere (the
    zephyr.dts + dts_equiv.py comparison for the same rig, strictly
    stronger than any comparison of the overlay in isolation could be).

    Checks: (1) every rig-assigned param token expected carries verbatim
    is still present verbatim in actual, never resolved to a bare number
    nor dropped; (2) if expected opens with the quoted
    #include "rig-gen-includes.dtsi" line, actual opens with the
    identical line too -- catching both a dropped include and one merely
    displaced elsewhere in the file; (3) every gpio/pwm/adc position
    annotation and the PWM/ADC pinctrl note expected carries is still
    present in actual.

    Returns None when actual preserves every one of expected's targeted
    facts; otherwise a human-readable report of every mismatch found (not
    just the first). Unlike compare_context_cmake/compare_config_sheet
    this never reports a parse failure -- rig-gen.overlay is not parsed
    into a full fact set here at all, only scanned for these three
    specific shapes."""
    problems: list[str] = []

    lost_tokens = _param_tokens(expected) - _param_tokens(actual)
    if lost_tokens:
        problems.append(
            "verbatim param token(s) no longer emitted unresolved: "
            + ", ".join(f"{name} = <{token}>" for name, token in sorted(lost_tokens))
        )

    expected_lines = expected.splitlines()
    actual_lines = actual.splitlines()
    if (
        expected_lines
        and expected_lines[0] == _INCLUDES_LINE
        and (not actual_lines or actual_lines[0] != _INCLUDES_LINE)
    ):
        problems.append(
            f"{_INCLUDES_LINE!r} must be the first line (quoted-include "
            "resolution depends on it) but is missing or displaced"
        )

    expected_annotations = _annotation_comments(expected)
    actual_annotations = _annotation_comments(actual)
    if expected_annotations != actual_annotations:
        lost = sorted(expected_annotations - actual_annotations)
        gained = sorted(actual_annotations - expected_annotations)
        parts = []
        if lost:
            parts.append(
                "dropped: " + ", ".join(f"{prop}@{pos} {comment}" for prop, pos, comment in lost)
            )
        if gained:
            parts.append(
                "added: " + ", ".join(f"{prop}@{pos} {comment}" for prop, pos, comment in gained)
            )
        problems.append("gpio/pwm/adc position annotation(s) differ -- " + "; ".join(parts))

    if _PINCTRL_NOTE in expected and _PINCTRL_NOTE not in actual:
        problems.append("the PWM/ADC pinctrl note was dropped")

    if not problems:
        return None
    return "\n".join(problems)


# --------------------------------------------------------------------------
# rig-gen-includes.dtsi: nothing but the headers the rig's own parameter
# assignments actually need (emitter._needed_param_includes -- the union
# of the owning shield devices' own declared_param_includes), emitted if and only if
# that list is non-empty (today, only lotus_buttons). Unlike RIG_DEPENDS,
# this is compared as an ORDERED list -- it is the declaring shield
# device's own header order, and cpp include order can matter (a later
# header may rely on a macro an earlier one defines), so a comparator
# that tolerated reordering could hide a real regression.

_INCLUDES_BANNER_RE = re.compile(r"^/\*.*\*/$")
_INCLUDE_LINE_RE = re.compile(r"^#include <(?P<header>[^>]+)>$")


class IncludesDtsiParseError(ValueError):
    """Raised by parse_includes_dtsi when a non-blank line is neither the
    provenance banner nor an angle-bracket #include <header> line. An unrecognised
    line must never be silently skipped: dropping it would let a
    truncated or malformed artifact compare equal to whatever header list
    the rest of the text happens to carry."""


def parse_includes_dtsi(text: str) -> tuple[str, ...]:
    """Parse rig-gen-includes.dtsi into the ORDERED tuple of headers the
    rig's own parameter assignments needed
    (emitter._needed_param_includes), in the order the declaring shield
    device wrote them (and emitter/__init__.py._render_includes_dtsi
    preserves).

    The provenance banner comment (one line, /* ... */) is recognised
    structurally as the artifact's first non-blank line but its own text
    is never read -- the same tool-identity leak compare_context_cmake and
    compare_config_sheet already treat as free to differ. Every remaining
    non-blank line must be an angle-bracket #include <header> line; blank lines
    carry no contract and are skipped freely.

    Returns a fresh tuple the caller owns; text is read-only."""
    lines = text.splitlines()
    n = len(lines)
    i = 0
    while i < n and lines[i].strip() == "":
        i += 1
    if i >= n or _INCLUDES_BANNER_RE.match(lines[i].strip()) is None:
        raise IncludesDtsiParseError(
            "expected the provenance banner comment (/* ... */) as the first non-blank line"
        )
    i += 1
    headers: list[str] = []
    while i < n:
        line = lines[i].strip()
        if line == "":
            i += 1
            continue
        m = _INCLUDE_LINE_RE.match(line)
        if m is None:
            raise IncludesDtsiParseError(
                f"line {i + 1}: not an angle-bracket #include <header> line: {lines[i]!r}"
            )
        headers.append(m.group("header"))
        i += 1
    return tuple(headers)


def compare_includes_dtsi(expected: str, actual: str) -> str | None:
    """Compare two rig-gen-includes.dtsi texts against the artifact's real
    contract -- the ordered header list -- instead of byte-for-byte.

    A missing, extra, or reordered header is a mismatch: declaration order
    is the rig author's, and cpp include order can matter, so this is
    compared as a LIST, never a set (unlike context.cmake's RIG_DEPENDS).
    The provenance banner is recognised as present but never read.

    Returns None when the two texts declare the identical header list in
    the identical order; otherwise a human-readable mismatch report. Text
    that fails to parse at all is reported as a mismatch too, never raised
    past this function, matching compare_context_cmake/compare_config_sheet."""
    try:
        expected_headers = parse_includes_dtsi(expected)
    except IncludesDtsiParseError as exc:
        return f"golden rig-gen-includes.dtsi failed to parse: {exc}"
    try:
        actual_headers = parse_includes_dtsi(actual)
    except IncludesDtsiParseError as exc:
        return f"actual rig-gen-includes.dtsi failed to parse: {exc}"

    if expected_headers == actual_headers:
        return None
    return (
        "header list differs (declaration order is contract): golden "
        f"{list(expected_headers)!r} != actual {list(actual_headers)!r}"
    )
