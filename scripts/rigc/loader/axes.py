# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Qualifier axes: declaration parsing, selection resolution, the
constructed-fragment-stem collision check, and revision normalization,
matching hwmv2's own revision semantics (the format/exact/nearest-lower
machinery `extensions.cmake` implements).

**The hwmv2 seam**: this module is the ONLY place a `revision:`/
`revisions:`/`variants:` declaration's raw YAML is read
(`parse_revision_decl`/`parse_legacy_revision_decl`/`parse_variant_decl`)
or a selection resolved against it (`resolve_axis_selection`): a rig's
own axis resolution (`resolve_axis`, below) and `ShieldLibrary.resolve`
(`loader/library.py`) both delegate to that one function rather than
each re-deriving the three failure shapes (not-declared-at-all /
not-a-member / no-default) with their own wording. `normalize_revision`
applies ONLY at filename construction, and only to a RESOLVED value,
never a requested one.

`variants:` keeps its own `{default:, list: []}` shape: each entry is
either a bare name or a mapping `{name:}` (only `name:` is read; any
other key is ignored). A revision entry (`parse_revision_decl` below)
must always be a mapping -- the two axes' entry shapes differ, and
that difference is deliberate, not an oversight to fix.

A rig.yml revision axis (singular key `revision:`) takes upstream's own
board.yml block: `format:` (required, one of letter/number/major.minor.
patch/custom), `default:`, `exact:` (optional), and a plural
`revisions:` list of `{name:}` mappings -- copying the SHAPE, not a
near-miss, so a reviewer can diff our schema against upstream's
board-schema.yaml. Only `letter`/`number`/`major.minor.patch` are
implemented; `format: custom` is a valid declaration (upstream's schema
allows it) but is rejected at resolution time, loudly, since upstream's
`custom` means the board author supplies their own `revision.cmake`
calling `board_check_revision` itself -- arbitrary cmake feeding a Python
resolver is out of scope here.

A shield.yml revision axis does NOT get that shape: it keeps its
PRE-hwmv2 one (`parse_legacy_revision_decl`'s own docstring has the
full reason) -- the pinned zephyr tree carries its own schema
restricting a shield's `revisions:` block to exactly `{default:, list:
[]}`, enforced by Zephyr's own `list_shields.py` on every real configure,
whether or not the shield in question is used. `resolve_axis_selection`
reads `decl.format is None` as "run no hwmv2 machinery, exact membership
only" -- a property of the DATA, not of which caller (`owner_kind`)
passed it, so the function needs no shield/rig branching and the day
that schema changes, nothing here does either.
"""

from __future__ import annotations

import re

from ..diag import Diagnostic, SourceRef, error
from ..model import AxisDecl
from .documents import Val, require

#: hwmv2's own per-format id shapes (extensions.cmake:1048 family, ported
#: unchanged): `letter` is a single uppercase letter, `number` is digits
#: only, `major.minor.patch` is three dot-separated non-negative integers
#: with no leading zero (except the literal "0" component itself).
_REVISION_PATTERNS = {
    "letter": re.compile(r"^[A-Z]$"),
    "number": re.compile(r"^\d+$"),
    "major.minor.patch": re.compile(r"^((0|[1-9][0-9]*)(\.[0-9]+)(\.[0-9]+))$"),
}

#: Every format upstream's board-schema.yaml accepts, for the SCHEMA-level
#: check (declaring `format: custom` is legal YAML, just not an
#: implemented resolution -- rejected instead in `resolve_axis_selection`,
#: where "this axis is actually used" is decided).
_ALL_REVISION_FORMATS = ("letter", "number", "major.minor.patch", "custom")

_FORMAT_DESCRIPTIONS = {
    "letter": "a single uppercase letter (A-Z)",
    "number": "digits only",
    "major.minor.patch": "major.minor.patch, e.g. 1.2.3",
}


def normalize_revision(rev: str) -> str:
    """hwmv2's own revision normalization (zephyr_build_string,
    extensions.cmake:1772): a dotted revision id becomes underscores in
    the CONSTRUCTED filename only (1.2 -> 1_2). Applies to the RESOLVED
    value only -- the value a selection actually resolved to, nearest-lower
    match included -- never to a declared name or the raw requested
    string."""
    return rev.replace(".", "_")


def variant_fragment_name(rig_name: str, variant: str) -> str:
    """<rigname>_<variant>.yml -- the variant delta-fragment stem, from
    the RAW selected value: normalization is a REVISION concept (hwmv2
    dots-in-ids) only, never applied to variants -- the two axes
    construct their stems differently. Lives beside normalize_revision
    because stem construction IS the hwmv2 seam: the collision
    enumerator below builds the same stems."""
    return f"{rig_name}_{variant}.yml"


def revision_fragment_name(rig_name: str, revision: str) -> str:
    """<rigname>_<norm(rev)>.yml -- the revision delta-fragment stem,
    normalized in exactly ONE place (normalize_revision above). `revision`
    must already be the RESOLVED value (nearest-lower match applied) --
    callers never pass the raw requested string here."""
    return f"{rig_name}_{normalize_revision(revision)}.yml"


def _zero_append(fmt: str, value: str) -> str:
    """hwmv2's loose typing for major.minor.patch (extensions.cmake:
    1092-1103): a REQUESTED value with fewer than three dot-separated
    components gets the missing ones padded with zero, BEFORE the format's
    own pattern is matched -- "1" becomes "1.0.0", "1.2" becomes "1.2.0".
    A no-op for every other format and for a value that already has three
    or more components. Declared names are never passed through this --
    they must already be full triples (extensions.cmake never rewrites
    VALID_REVISIONS, only BOARD_REVISION)."""
    if fmt != "major.minor.patch":
        return value
    parts = value.split(".")
    while len(parts) < 3:
        parts.append("0")
    return ".".join(parts)


def _format_matches(fmt: str, value: str) -> bool:
    pattern = _REVISION_PATTERNS.get(fmt)
    return pattern is None or bool(pattern.match(value))


def _revision_sort_key(fmt: str, value: str) -> tuple[int, ...]:
    """The per-format ordering hwmv2's nearest-lower match compares by
    (extensions.cmake:1133-1152's VERSION_/STRGREATER/GREATER split):
    `number` and `major.minor.patch` compare numerically component by
    component; `letter` is a single character, so its ordinal already
    matches STRGREATER's lexicographic order. Callers only ever pass an
    already format-validated value."""
    if fmt == "number":
        return (int(value),)
    if fmt == "major.minor.patch":
        return tuple(int(p) for p in value.split("."))
    return (ord(value),)


def _nearest_lower(fmt: str, declared: list[str], candidate: str) -> str | None:
    """The highest declared revision <= candidate, per-format compared --
    hwmv2's nearest-lower match (extensions.cmake:1133-1152). None when
    every declared revision is greater than candidate (no fallback
    exists); declared values are read-only."""
    candidate_key = _revision_sort_key(fmt, candidate)
    best: str | None = None
    best_key: tuple[int, ...] | None = None
    for value in declared:
        key = _revision_sort_key(fmt, value)
        if key <= candidate_key and (best_key is None or key > best_key):
            best, best_key = value, key
    return best


def parse_variant_decl(
    container_v: Val,
    key: str = "variants",
    owner: str = "rig",
) -> tuple[AxisDecl | None, list[Diagnostic]]:
    """A rig's `variants:` declaration block: {default:, list: []}.
    Absent key -> no axis declared (None, no diagnostics). `list:` must be
    non-empty and `default:` (if given) must be one of its own members --
    both lang-schema, since they are defects of the declaring FILE, not of
    a particular selection.

    Each list entry is either a bare name, or a mapping {name:} -- ONLY
    name: is read off a mapping entry. A stray board:/sockets: key on an
    entry is silently ignored, the same as an unrecognized key anywhere
    else in this grammar: rig.yml has had no board:/sockets: grammar
    since the board left it entirely, and nothing downstream has anywhere
    to put such a value.

    Returns (decl, diagnostics): the parsed declaration, or None when the
    key is absent or its shape was rejected -- the diagnostics distinguish
    the two."""
    axis_v = container_v.value.get(key)
    if axis_v is None:
        return None, []
    diags: list[Diagnostic] = []
    axis_map = axis_v.value if isinstance(axis_v.value, dict) else {}
    list_v = axis_map.get("list")
    values: list[str] = []
    for item_v in list_v.value if list_v is not None else []:
        if isinstance(item_v.value, dict):
            name_v, d = require(item_v, "name", f"{owner} {key} entry")
            diags += d
            if name_v is None:
                continue
            values.append(str(name_v.value))
        else:
            values.append(str(item_v.value))
    if not values:
        diags.append(
            error("lang-schema", f"{owner} {key}: 'list' must be a non-empty list", (axis_v.src,))
        )
        return None, diags
    default_v = axis_map.get("default")
    if default_v is None:
        return AxisDecl(values=values), diags
    default = str(default_v.value)
    if default not in values:
        diags.append(
            error(
                "lang-schema",
                f"{owner} {key}: default '{default}' is not one of the declared "
                f"values ({', '.join(values)})",
                (default_v.src,),
            )
        )
        return None, diags
    return AxisDecl(values=values, default=default), diags


def _parse_revision_entries(
    list_v: Val | None, fmt: str, key: str, owner: str
) -> tuple[list[str], list[Diagnostic]]:
    """Each `revisions:` list entry: a mapping {name:} whose name: is a
    quoted string matching `fmt`'s own pattern. An unquoted numeric-
    looking id is rejected rather than coerced (it is exactly the value
    a `major.minor.patch` axis invites an author to type, and YAML would
    silently read it as a number); a name that does not match `fmt` is
    likewise rejected here, since a malformed DECLARED name is this
    file's own defect.

    Returns (values, diagnostics): only the entries that passed every
    check, in list order."""
    diags: list[Diagnostic] = []
    values: list[str] = []
    for item_v in list_v.value if list_v is not None else []:
        if not isinstance(item_v.value, dict):
            diags.append(
                error(
                    "lang-schema",
                    f"{owner} {key}: a revisions: entry must be a mapping "
                    "{name:} -- this axis takes no bare scalar entries",
                    (item_v.src,),
                )
            )
            continue
        name_v, d = require(item_v, "name", f"{owner} {key} entry")
        diags += d
        if name_v is None:
            continue
        if not isinstance(name_v.value, str):
            diags.append(
                error(
                    "lang-schema",
                    f"{owner} {key}: revision id {name_v.value!r} must be a "
                    "quoted string -- an unquoted id can parse as a YAML "
                    "number and silently change value",
                    (name_v.src,),
                )
            )
            continue
        name = name_v.value
        if not _format_matches(fmt, name):
            diags.append(
                error(
                    "lang-schema",
                    f"{owner} {key}: revision '{name}' does not match format "
                    f"{fmt!r} (expected {_FORMAT_DESCRIPTIONS[fmt]})",
                    (name_v.src,),
                )
            )
            continue
        values.append(name)
    return values, diags


def parse_revision_decl(
    container_v: Val,
    key: str = "revision",
    owner: str = "rig",
) -> tuple[AxisDecl | None, list[Diagnostic]]:
    """A rig.yml `revision:` declaration block (singular key): upstream's
    own board.yml shape -- `format:` (required, one of letter/number/
    major.minor.patch/custom), `default:`, optional `exact:`, and a
    plural `revisions:` list of `{name:}` mappings. Absent key -> no axis
    declared (None, no diagnostics). NOT used for shield.yml -- see
    `parse_legacy_revision_decl`.

    Every declared id must be a quoted STRING (upstream's `name:
    {type: string}`) -- a non-string is rejected, never coerced, since an
    unquoted numeric-looking id is exactly the value a `major.minor.patch`
    axis invites an author to type. Each id is additionally validated
    against `format:`'s own pattern here (board-schema.yaml's own
    conditional block does the same for declared names, independent of
    any particular selection) -- a malformed DECLARED name is a defect of
    this file, `lang-schema`; a malformed REQUESTED value is instead
    `resolve_axis_selection`'s concern, since it is a defect of the
    SELECTION, not the declaration.

    `format: custom` is accepted here (it is valid upstream YAML) and
    rejected only in `resolve_axis_selection`, once the axis is actually
    used -- see this module's own docstring.

    Returns (decl, diagnostics): the parsed declaration, or None when the
    key is absent or its shape was rejected -- the diagnostics distinguish
    the two."""
    axis_v = container_v.value.get(key)
    if axis_v is None:
        return None, []
    diags: list[Diagnostic] = []
    axis_map = axis_v.value if isinstance(axis_v.value, dict) else {}

    format_v = axis_map.get("format")
    if format_v is None:
        diags.append(
            error(
                "lang-schema",
                f"{owner} {key}: 'format' is required -- one of {', '.join(_ALL_REVISION_FORMATS)}",
                (axis_v.src,),
            )
        )
        return None, diags
    fmt = format_v.value
    if not isinstance(fmt, str) or fmt not in _ALL_REVISION_FORMATS:
        diags.append(
            error(
                "lang-schema",
                f"{owner} {key}: 'format' must be one of "
                f"{', '.join(_ALL_REVISION_FORMATS)} (got {fmt!r})",
                (format_v.src,),
            )
        )
        return None, diags

    list_v = axis_map.get("revisions")
    values, entry_diags = _parse_revision_entries(list_v, fmt, key, owner)
    diags += entry_diags
    if not values:
        diags.append(
            error(
                "lang-schema", f"{owner} {key}: 'revisions' must be a non-empty list", (axis_v.src,)
            )
        )
        return None, diags

    exact_v = axis_map.get("exact")
    exact = bool(exact_v.value) if exact_v is not None else False

    default_v = axis_map.get("default")
    if default_v is None:
        return AxisDecl(values=values, format=fmt, exact=exact), diags
    if not isinstance(default_v.value, str):
        diags.append(
            error(
                "lang-schema", f"{owner} {key}: 'default' must be a quoted string", (default_v.src,)
            )
        )
        return None, diags
    default = default_v.value
    if default not in values:
        diags.append(
            error(
                "lang-schema",
                f"{owner} {key}: default '{default}' is not one of the declared "
                f"revisions ({', '.join(values)})",
                (default_v.src,),
            )
        )
        return None, diags
    return AxisDecl(values=values, default=default, format=fmt, exact=exact), diags


def parse_legacy_revision_decl(
    container_v: Val,
    key: str = "revisions",
    owner: str = "rig",
) -> tuple[AxisDecl | None, list[Diagnostic]]:
    """shield.yml's `revisions:` declaration, kept in its PRE-hwmv2 shape
    (`{default:, list: []}`, bare scalar ids only) -- NOT the hwmv2
    `revision:` block `parse_revision_decl` gives rig.yml.

    This is a hard external constraint, discovered by running a REAL
    cmake configure against a migrated shield.yml, not a choice: the
    PINNED zephyr tree carries its own schema for shield.yml
    (`zephyr/scripts/schemas/shield-schema.yaml`, commit `8da5b3a0f60`,
    "schemas: shield: allow a revisions: block in shield.yml"), which
    `additionalProperties: false`-restricts a shield's `revisions:` block
    to exactly `default:`/`list:` -- no `format:`, no `exact:`, no plural
    `revisions:` sub-list. Zephyr's own `list_shields.py` validates EVERY
    shield.yml under EVERY board root against that schema at ordinary
    `find_package(Zephyr)` time, for every configure, whether or not the
    shield in question is ever referenced -- so a `revision:`/`format:`
    key on any shield.yml fails EVERY real build in the workspace, not
    just ones naming that shield. zephyr/ is a separate module and not
    ours to patch (a schema change there is its own, out-of-scope,
    ruling), so shield.yml keeps this shape until it does.

    Returns (decl, diagnostics): the parsed declaration (`format`/`exact`
    always at their defaults, None/False -- `resolve_axis_selection`
    reads `format is None` as "run no hwmv2 machinery, exact membership
    only"), or None when the key is absent or its shape was rejected."""
    axis_v = container_v.value.get(key)
    if axis_v is None:
        return None, []
    diags: list[Diagnostic] = []
    axis_map = axis_v.value if isinstance(axis_v.value, dict) else {}
    list_v = axis_map.get("list")
    values: list[str] = []
    for item_v in list_v.value if list_v is not None else []:
        if isinstance(item_v.value, dict):
            diags.append(
                error(
                    "lang-schema",
                    f"{owner} {key}: a mapping entry (name:) is legal only in "
                    "a rig's variants: list -- this axis takes bare names",
                    (item_v.src,),
                )
            )
            continue
        values.append(str(item_v.value))
    if not values:
        diags.append(
            error("lang-schema", f"{owner} {key}: 'list' must be a non-empty list", (axis_v.src,))
        )
        return None, diags
    default_v = axis_map.get("default")
    if default_v is None:
        return AxisDecl(values=values), diags
    default = str(default_v.value)
    if default not in values:
        diags.append(
            error(
                "lang-schema",
                f"{owner} {key}: default '{default}' is not one of the declared "
                f"values ({', '.join(values)})",
                (default_v.src,),
            )
        )
        return None, diags
    return AxisDecl(values=values, default=default), diags


def check_axis_collision(
    rig_name: str, variants: AxisDecl | None, revisions: AxisDecl | None, src: SourceRef
) -> list[Diagnostic]:
    """The fragment-stem collision check: no two distinct (variant,
    revision) SELECTIONS may construct the same fragment stem.
    Enumerates every stem the declared axes could ever construct -- each
    axis alone, plus every combined (variant, revision) pair -- and
    reports every collision; a variant name equal to a revision id is
    the single-axis case of this same collision.

    Returns the collision findings, possibly empty; the declarations
    are read-only."""
    variant_values = variants.values if variants is not None else []
    revision_values = revisions.values if revisions is not None else []
    origins: dict[str, list[str]] = {}

    def note(stem: str, origin: str) -> None:
        origins.setdefault(stem, []).append(origin)

    for v in variant_values:
        note(f"{rig_name}_{v}", f"variant '{v}'")
    for r in revision_values:
        note(f"{rig_name}_{normalize_revision(r)}", f"revision '{r}'")
    for v in variant_values:
        for r in revision_values:
            note(f"{rig_name}_{v}_{normalize_revision(r)}", f"variant '{v}' + revision '{r}'")

    diags: list[Diagnostic] = []
    for stem in sorted(origins):
        stem_origins = origins[stem]
        if len(stem_origins) > 1:
            diags.append(
                error(
                    "lang-variant",
                    f"rig '{rig_name}': {' and '.join(stem_origins)} all "
                    f"construct the same fragment stem '{stem}' -- the "
                    "constructed filenames would be ambiguous about which "
                    "selection a fragment belongs to",
                    (src,),
                )
            )
    return diags


def _resolve_revision_selection(
    owner_kind: str,
    owner_name: str,
    axis_kind: str,
    code: str,
    decl: AxisDecl,
    selected: str | None,
    src: SourceRef,
) -> tuple[str | None, list[Diagnostic]]:
    """The hwmv2 revision-resolution machinery (extensions.cmake:1048
    family), reached only once `decl.format is not None`: `format:
    custom` is rejected loudly the moment the axis is used at all, even
    via its default, naming the three formats rigc implements. A
    `selected` value gets hwmv2's own loose typing for
    `major.minor.patch` (missing trailing components zero-appended)
    before format validation and membership are checked; a value that
    does not match the declared format at all is rejected. A value that
    IS a declared member resolves to itself; otherwise, unless
    `decl.exact`, hwmv2's nearest-lower match resolves DOWN to the
    highest declared revision <= the requested one. An unselected axis
    takes the declared default exactly like a non-hwmv2 axis does.

    Returns (value, diagnostics): the RESOLVED axis value (nearest-lower
    already applied where it applies), or None either legitimately (no
    default, nothing selected -- reported) or after a reported failure.
    `decl` is read-only."""
    if decl.format not in _REVISION_PATTERNS:
        supported = ", ".join(_REVISION_PATTERNS)
        return None, [
            error(
                code,
                f"{owner_kind} '{owner_name}' declares revision format "
                f"{decl.format!r} -- rigc supports {supported} only "
                "(format: custom is not implemented)",
                (src,),
            )
        ]

    if selected is None:
        if decl.default is not None:
            return decl.default, []
        return None, [
            error(
                code,
                f"{owner_kind} '{owner_name}': no {axis_kind} selected, and "
                f"this {owner_kind} declares no default {axis_kind} -- choose "
                f"one of: {', '.join(decl.values)}",
                (src,),
            )
        ]

    assert decl.format is not None  # narrowed by the check above
    candidate = _zero_append(decl.format, selected)
    if not _format_matches(decl.format, candidate):
        return None, [
            error(
                code,
                f"{owner_kind} '{owner_name}': revision '{selected}' does "
                f"not match this axis's declared format {decl.format!r} -- "
                f"expected {_FORMAT_DESCRIPTIONS[decl.format]}",
                (src,),
            )
        ]
    if candidate in decl.values:
        return candidate, []
    if not decl.exact:
        lower = _nearest_lower(decl.format, decl.values, candidate)
        if lower is not None:
            return lower, []
    return None, [
        error(
            code,
            f"{owner_kind} '{owner_name}': revision '{candidate}' is not "
            f"declared -- known revisions: {', '.join(decl.values)}",
            (src,),
        )
    ]


def resolve_axis_selection(
    owner_kind: str,
    owner_name: str,
    axis_kind: str,
    decl_key: str,
    decl: AxisDecl | None,
    selected: str | None,
    src: SourceRef,
) -> tuple[str | None, list[Diagnostic]]:
    """The shared decision a qualifier-axis resolution makes, over values
    -- shared by a rig's own axis resolution (`resolve_axis`, below) and
    `ShieldLibrary.resolve` (`loader/library.py`).

    A `selected` value naming an axis its owner does not declare AT ALL
    says so by name ("this rig declares no revision:" / "this shield
    declares no revision:") rather than the generic not-a-member wording
    -- it points the author at the right place. A bare (unselected) axis
    takes the declared default; if the axis is declared but has none,
    that is an error.

    For a REVISION axis (`axis_kind == "revision"`), `decl.format` governs
    the rest of resolution, hwmv2-ported (extensions.cmake:1048 family):
    `format: custom` is rejected loudly, naming the three formats rigc
    implements, whenever this axis is used at all (even a bare reference
    to its default) -- a declared-but-never-selected custom axis is still
    "used" the moment a rig/shield resolves ITS OWN axis. A `selected`
    value gets hwmv2's own loose typing for `major.minor.patch` (missing
    trailing components zero-appended) BEFORE format validation and
    membership are checked; a value that doesn't match the declared
    format at all is rejected. A value that IS a declared member resolves
    to itself. Otherwise, unless `decl.exact` is set, hwmv2's
    nearest-lower match resolves DOWN to the highest declared revision
    <= the requested one (per-format compared); `exact: true` disables
    that, reproducing this axis's pre-hwmv2 behaviour (an undeclared
    value is unconditionally fatal) bit for bit. A VARIANT axis
    (`axis_kind == "variant"`) takes none of this: a selected value must
    be an exact declared member.

    `owner_kind` ("rig" or "shield") constructs both the quoted-name
    prefix and the possessive ("this rig" / "this shield") -- the two
    callers' wording differs in exactly that one word, nowhere else.
    `axis_kind` ("revision" or "variant") and `decl_key` (the declaring
    YAML key: "revision" or "variants") construct the rest; a shield
    always passes ("shield", name, "revision", "revision"), since a
    shield declares only that one axis. This function does no IO and
    triggers no parsing -- callers that need to act on the RESOLVED value
    (constructing a fragment filename, parsing a shield revision's
    template) do that themselves, around this decision.

    A revision axis whose declaration carries NO `format` at all
    (`decl.format is None`) runs NONE of the hwmv2 machinery above --
    exact membership only, same as a variant axis. This is not a
    shortcut; it is what `parse_legacy_revision_decl` (this module)
    always produces, and every shield.yml revision axis is parsed by
    THAT function, never `parse_revision_decl` -- see its own docstring
    for why. `decl.format` is therefore the discriminator this function
    reads, not `owner_kind`: the day a shield.yml CAN carry `format:`,
    nothing here needs to change.

    Returns (value, diagnostics): the RESOLVED axis value (nearest-lower
    already applied, when hwmv2 applies at all), or None either
    legitimately (no axis declared and nothing selected) or after a
    reported failure -- an error in the list is what distinguishes them.
    `decl` is read-only to this function."""
    code = "lang-rev" if axis_kind == "revision" else "lang-variant"
    hwmv2 = axis_kind == "revision" and decl is not None and decl.format is not None

    if hwmv2:
        assert decl is not None
        return _resolve_revision_selection(
            owner_kind, owner_name, axis_kind, code, decl, selected, src
        )

    if selected is not None:
        if decl is None:
            return None, [
                error(
                    code,
                    f"{owner_kind} '{owner_name}' names a {axis_kind} "
                    f"({selected!r}), but this {owner_kind} declares no "
                    f"{decl_key}: at all",
                    (src,),
                )
            ]
        if selected not in decl.values:
            return None, [
                error(
                    code,
                    f"{owner_kind} '{owner_name}': {axis_kind} '{selected}' "
                    f"is not declared -- known {axis_kind}s: "
                    f"{', '.join(decl.values)}",
                    (src,),
                )
            ]
        return selected, []
    if decl is None:
        return None, []
    if decl.default is not None:
        return decl.default, []
    return None, [
        error(
            code,
            f"{owner_kind} '{owner_name}': no {axis_kind} selected, and this "
            f"{owner_kind} declares no default {axis_kind} -- choose one of: "
            f"{', '.join(decl.values)}",
            (src,),
        )
    ]


def resolve_axis(
    rig_name: str,
    axis_kind: str,
    decl_key: str,
    decl: AxisDecl | None,
    selected: str | None,
    src: SourceRef,
) -> tuple[str | None, list[Diagnostic]]:
    """Resolve ONE of a rig's own qualifier axes (`revision` or
    `variant`) to its final RESOLVED value -- the rig-owned instance of
    `resolve_axis_selection`'s shared decision (`owner_kind="rig"`). For
    a revision axis this may differ from `selected` (nearest-lower match,
    or hwmv2's major.minor.patch zero-append) -- callers that need the
    raw requested value for provenance keep it themselves (it is exactly
    what they already passed in as `selected`).

    Returns (value, diagnostics): the selected axis value, or None
    either legitimately (no axis declared and nothing selected) or
    after a reported failure -- an error in the list is what
    distinguishes them."""
    return resolve_axis_selection("rig", rig_name, axis_kind, decl_key, decl, selected, src)
