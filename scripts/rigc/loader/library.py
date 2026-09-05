# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""The shield library: scan, axes, lazy revision resolution.
`resolve()` returns a REAL `Shield`, or diagnostics explaining why not.

**Discovery**, per folder under a shield-library root:
  - no shield.yml -> the name is this folder's own basename; it is a
    rig template if and only if `<dir>/<name>.shield` exists, silently skipped
    otherwise (a legacy shield, or not a shield at all).
  - shield.yml present -> one name per `shield:` (a single mapping) or
    `shields:` (a list, the mutually exclusive plural form upstream
    `b836fcdd709` added) entry -- NAME comes from the entry's own `name:`
    now, never the folder. An entry is a rig template if and only if it declares
    `template: true` AND `<dir>/<name>.shield` exists; one that declares
    `template: true` with no matching file is a loud `lang-shield-template`
    finding, not a silent skip (this folder's authoring intent is known,
    unlike the yml-less case); one that omits the flag is a legacy shield
    carrying metadata, discoverable (`promote.discover_shields`'s wider
    census) but never a rig template. Never a `*.shield` glob either way
    (`Kconfig.shield` ends in the literal substring and would be
    mis-globbed).

**shield.yml** supplies the declared NAME -- the folder name no longer
is one -- and, per template entry, its own
`revisions:` axis, parsed by `loader.axes.parse_legacy_revision_decl` --
its OWN pre-hwmv2 shape (`{default:, list: []}`), NOT the hwmv2 block
rig.yml's own `revision:` axis takes. This is a hard external
constraint, not a choice: the pinned zephyr tree carries its own schema
restricting a shield's `revisions:` block to exactly that shape (see
`parse_legacy_revision_decl`'s own docstring). `resolve_axis_selection`
still applies -- a shield revision axis with `format is None` runs
exact-membership resolution only, no nearest-lower.

**Eager vs lazy**: discovery (the folder walk, the `<name>.shield`
presence probe, `shield.yml`'s own entries and axis reads) is ALWAYS
eager -- it is cheap, has no subprocess, and is what builds the
known-shields census `lang-instance-shield` prints. Parsing a template --
base or revision -- never happens at scan time; every discovered shield
is recorded as `_Pending` and its template parses on `resolve()`'s first
reference, whether or not it declares a `revisions:` axis. Eagerly
parsing every discovered shield regardless of use would do needless
cpp/dtlib work (a rig referencing 2 of 14 discovered shields has no
business preprocessing the other 12) and leak an unreferenced template's
path into dependency data; eagerly combining every declared REVISION of a
referenced shield would repeat the same mistake one level down, so that
stays deferred to each revision's own first selection too.

A base parse that fails (its template defines no node matching the
folder name) is memoized in `ShieldLibrary.failed` so a second reference
reports nothing new; a lazy re-parse per reference would otherwise
re-run cpp and re-report the same defect once per referencing instance.

**Diagnostics and dependency data are RETURN values**: `resolve()`
never writes into an accumulator handed in from outside.
`ShieldLibrary.shields` IS mutated in place by `resolve()` -- that is
the lazy-parse MEMOIZATION cache the whole design requires, a
self-contained value the library keeps about itself, not a side
channel written into by many unrelated callers.
"""

from __future__ import annotations

import glob
import logging
import os
from dataclasses import dataclass, field

from ..deps import Deps, touch, union
from ..diag import Diagnostic, LoadError, SourceRef, error
from ..dtsio import MODULE_ROOT, parse_tu, source_files
from ..model import AxisDecl, ConnectorType, Shield
from ..registry import load_types
from .axes import normalize_revision, parse_legacy_revision_decl, resolve_axis_selection
from .documents import Val, parse_marked, require
from .shields import parse_shields

log = logging.getLogger(__name__)

#: The vendored default shield library (direct API / test use only -- the
#: CLI always resolves --shield-dir roots and threads them down instead).
SHIELDS_DIR = os.path.join(MODULE_ROOT, "boards", "shields")


@dataclass(frozen=True)
class _Pending:
    """A discovered RIG TEMPLATE whose template has NOT been parsed yet --
    every discovered template gets one of these, whether or not it
    declares a `revisions:` axis. `decl` is `None` for an axis-less
    shield (its base template is what `resolve()` parses on first bare
    reference) or the parsed `AxisDecl` for a revisioned one (each
    revision, including the declared default, parses on its own first
    selection). `yml_path` is `None` for a name with no shield.yml at
    all (the legacy, folder-basename-derived case) or the shield.yml this
    name's own NAME came from -- `_pick_shield`'s own diagnostic reads it
    to say which of the two ever named this shield in the first place."""

    shield_dir: str
    base_file: str
    decl: AxisDecl | None
    yml_path: str | None = None


@dataclass
class ShieldLibrary:
    """The discovered shield library. `axes` and `pending` name EVERY
    discovered shield -- `axes` is the known-shields census a
    lang-instance-shield diagnostic prints, `pending` is what each one
    needs to parse itself on first reference -- while `shields` holds
    only what has actually been PARSED so far, filled in by `resolve()`
    as references arrive rather than by the scan.

    `shields` is keyed by the CONSTRUCTED stems `resolve()` builds and
    reads against -- "<name>" (a revision-less shield, or a revisioned
    one's DEFAULT) and "<name>@<rev>" (any declared revision, once
    resolved) -- never by the `.shield` DT node name alone, which is
    IDENTICAL across a shield's own revisions."""

    shields: dict[str, Shield]
    axes: dict[str, AxisDecl | None]
    pending: dict[str, _Pending]
    # name -> shield.yml, for EVERY name any shield.yml declares -- a rig
    # template's own metadata (also in `pending`) as well as a legacy
    # shield's (declared, but never a template): the wider set
    # `promote.discover_shields`'s census reads. `resolve()` only ever
    # looks a name up here after finding it in `axes` first, so a
    # non-template name's presence here is inert to everything below.
    ymls: dict[str, str]
    types: dict[str, ConnectorType]
    workdir: str
    include_dirs: list[str] | None = None
    #: Axis-less shields whose base parse has already failed once (a
    #: template that defines no node matching its folder name) -- checked
    #: before a second reference would re-run cpp and re-report the same
    #: defect. `_resolve_revision`'s own failures are deliberately NOT
    #: recorded here (see its docstring): this asymmetry is a decision,
    #: not an oversight.
    failed: set[str] = field(default_factory=set)
    # Every name `ymls` carries, mapped to THIS ENTRY's own `template:`
    # flag -- read once, at scan time, from the SAME shield.yml parse
    # `ymls`/`axes`/`pending` already did, so `promote.discover_shields`
    # never re-opens a shield.yml this module already read. A name
    # missing from `ymls` is also missing here (has_yml=False implies
    # not-promotable, never looked up).
    # True records what the entry DECLARED, never that a template was
    # found: an entry declaring `template: true` with no matching
    # `<name>.shield` stays True here (and in `ymls`) while never
    # entering `pending`, so this must not be read as "resolvable". The
    # scan's own lang-shield-template finding is what reports that case,
    # and `check_promotable` defers to it rather than inventing a second
    # vocabulary for the same defect.
    promotable: dict[str, bool] = field(default_factory=dict)

    def resolve(
        self,
        ref: str,
        ctx: str,
        src: SourceRef,
    ) -> tuple[Shield | None, list[Diagnostic], Deps]:
        """`<name>` or `<name>@<rev>` -> the Shield, parsing a
        not-yet-parsed template on first use --
        the base template of an axis-less shield exactly like a
        revisioned shield's own selected revision. The three failure
        shapes (not declared at all / not a member / no default) are
        `loader.axes.resolve_axis_selection`'s shared decision, the same
        one a rig's own qualified target resolves against -- reported as
        lang-rev here -- plus lang-instance-shield for a name this
        library never discovered at all. `ctx` names the caller (e.g.
        "instance 'sensor_0'") for that diagnostic's message.

        Returns (shield, diagnostics, deps); shield is None when
        resolution failed (the diagnostics say why) or when this
        shield's base parse already failed on an earlier reference (the
        failure was reported then, silently now). The library memoizes
        parsed shields (and axis-less parse failures) in place -- its own
        cache, not a shared accumulator; the caller owns diagnostics and
        deps."""
        name, sep, rev = ref.partition("@")
        if name not in self.axes:
            return (
                None,
                [
                    error(
                        "lang-instance-shield",
                        f"{ctx}: unknown shield '{name}'\n"
                        # An EMPTY library is the interesting case, and the
                        # join alone rendered it as "known shields: " -- a
                        # dangling label with trailing whitespace that told
                        # the reader nothing. An empty library almost always
                        # means the shield roots were wrong, so say that
                        # instead of trailing off.
                        + (
                            f"known shields: {', '.join(sorted(self.axes))}"
                            if self.axes
                            else "no shields were found at all -- check the "
                            "shield library roots (--shield-dir)"
                        ),
                        (src,),
                    )
                ],
                frozenset(),
            )
        # This reference makes the shield's OWN shield.yml load-bearing
        # for this rig: recorded here (not at scan time) so a rig depends
        # only on the metadata of shields it actually names.
        deps: Deps = touch(self.ymls[name]) if name in self.ymls else frozenset()
        decl = self.axes[name]
        if not sep and name in self.shields:
            return self.shields[name], [], deps
        requested = rev if sep else None
        # The shared decision (loader.axes.resolve_axis_selection): which
        # revision string applies -- the RESOLVED value (nearest-lower
        # match already applied WHEN decl.format is set; a shield's own
        # axis never has one today, see parse_legacy_revision_decl --
        # requested vs resolved kept apart via `requested` above regardless) -- or
        # None when this is a bare reference to an axis-less shield
        # (nothing declared, nothing selected -- legitimate, not a
        # failure). It does no parsing; the branches below own turning
        # that value into a Shield. decl_key is "revisions" (plural),
        # matching the actual YAML key a shield.yml declares (its own
        # pre-hwmv2 shape) -- NOT the rig's singular "revision".
        value, verdict = resolve_axis_selection(
            "shield", name, "revision", "revisions", decl, requested, src
        )
        if verdict:
            return None, verdict, deps
        if value is None:
            if name in self.failed:
                return None, [], deps
            pending = self.pending[name]
            shield, parse_diags, pdeps = _parse_shield_template(
                name,
                pending.base_file,
                [pending.base_file],
                f"shield-{name}.dts",
                self.workdir,
                self.include_dirs,
                self.types,
                pending.yml_path,
            )
            deps = union(deps, touch(pending.base_file), pdeps)
            if shield is None:
                self.failed.add(name)
                return None, parse_diags, deps
            self.shields[name] = shield
            return shield, parse_diags, deps
        # resolve_axis_selection only returns a non-None value when decl
        # is itself not None (a selected member, or a declared default);
        # narrow it explicitly since the shared decision's own return
        # type can't express that invariant to mypy.
        assert decl is not None
        shield, d, rdeps = self._resolve_revision(name, value, requested, decl, src)
        return shield, d, union(deps, rdeps)

    def _resolve_revision(
        self,
        name: str,
        rev: str,
        requested: str | None,
        decl: AxisDecl,
        src: SourceRef,
    ) -> tuple[Shield | None, list[Diagnostic], Deps]:
        """A single revision's own lazy parse -- deliberately UNMEMOIZED
        on failure (unlike the axis-less base parse `resolve()` handles
        directly): a bad revision re-reports on every reference. This is
        a decision, not an oversight; revisiting it is out of scope here.

        `rev` is the RESOLVED value (nearest-lower match already applied
        by `resolve_axis_selection`) -- every stem this method constructs,
        and the memoization key below, are built from it; `requested` is
        the raw `<name>@<rev>` string a reference actually named (kept on
        the returned Shield for provenance only, never for filenames)."""
        key = f"{name}@{rev}"
        cached = self.shields.get(key)
        if cached is not None:
            return cached, [], frozenset()
        pending = self.pending[name]
        rev_norm = normalize_revision(rev)
        rev_file = os.path.join(pending.shield_dir, f"{name}_{rev_norm}.shield")
        rev_conf = os.path.join(pending.shield_dir, f"{name}_{rev_norm}.conf")
        has_rev_file = os.path.isfile(rev_file)
        is_default = rev == decl.default
        # Shield-side analogue of the contributes-nothing check
        # (loader/fragments.py): a NON-DEFAULT revision that
        # contributes NOTHING is an authoring error; the default is
        # exempt (the base template IS its content).
        if not is_default and not (has_rev_file or os.path.isfile(rev_conf)):
            return (
                None,
                [
                    error(
                        "lang-rev",
                        f"shield '{name}': revision '{rev}' contributes nothing "
                        f"-- looked for {name}_{rev_norm}.shield and "
                        f"{name}_{rev_norm}.conf, neither exists",
                        (src,),
                    )
                ],
                frozenset(),
            )
        includes = [pending.base_file] + ([rev_file] if has_rev_file else [])
        # The base template is touched explicitly (not left to cpp
        # linemarker recovery alone): a revision fragment that defines no
        # node of its own still #includes the base, but a base that
        # defined no node EITHER would otherwise drop out of
        # dependency data entirely.
        deps: Deps = touch(pending.base_file)
        if has_rev_file:
            deps = union(deps, touch(rev_file))
        shield, diags, pdeps = _parse_shield_template(
            name,
            pending.base_file,
            includes,
            f"shield-{name}-{rev_norm}.dts",
            self.workdir,
            self.include_dirs,
            self.types,
            pending.yml_path,
        )
        deps = union(deps, pdeps)
        if shield is None:
            return None, diags, deps
        shield.revisions = decl
        shield.revision = rev
        shield.revision_requested = requested
        self.shields[key] = shield
        if is_default:
            self.shields[name] = shield
        return shield, diags, deps


def _parse_shield_template(
    name: str,
    template: str,
    includes: list[str],
    dts_name: str,
    workdir: str,
    include_dirs: list[str] | None,
    types: dict[str, ConnectorType],
    yml_path: str | None,
) -> tuple[Shield | None, list[Diagnostic], Deps]:
    """Build one shield translation unit (`parse_tu`) and pick its node
    (`_pick_shield`) -- the parse body `resolve()`'s axis-less path and
    `_resolve_revision` both need, factored so neither hand-duplicates
    the cpp/dtlib wiring. May raise LoadError (a real cpp/dtlib failure);
    callers decide whether that failure gets memoized. `yml_path` is
    threaded through to `_pick_shield` unchanged -- this function reads
    it for nothing else.

    Returns (shield, diagnostics, deps); shield is None only when the
    template parsed but defined no node named `name` (`_pick_shield`'s
    own diagnostic is included). `deps` are the real source files THIS
    parse touched, recovered from cpp linemarkers (`source_files`) --
    never `includes` themselves, since only the caller knows whether
    those are a base template or a revision fragment and which of the
    two dependency rules applies."""
    log.debug("shield library: parsing %s (%s)", name, os.path.basename(template))
    dt = parse_tu(includes, workdir, dts_name, include_dirs)
    deps = frozenset(source_files(dt, workdir))
    parsed, diags = parse_shields(dt, types)
    shield, pd = _pick_shield(parsed, name, template, yml_path)
    return shield, diags + pd, deps


def _pick_shield(
    parsed: dict[str, Shield],
    name: str,
    template: str,
    yml_path: str | None = None,
) -> tuple[Shield | None, list[Diagnostic]]:
    """The shield a template's translation unit defines, looked up by
    `name` -- the shield's DECLARED name, never whatever node name
    `parse_shields` happened to return. `yml_path`, when given, says
    the declared name came from that shield.yml rather than the
    folder's own basename -- the mismatch diagnostic below names
    whichever is true, since "must match the folder" is only ever
    correct for the yml-less legacy case now."""
    shield = parsed.get(name)
    if shield is not None:
        return shield, []
    defined = ", ".join(sorted(parsed)) or "none"
    source = (
        "the name shield.yml itself declares"
        if yml_path is not None
        else "the folder it lives in (it declares no shield.yml)"
    )
    return None, [
        error(
            "lang-shield-name",
            f"shield template {os.path.basename(template)} defines no shield "
            f"node named '{name}' -- a .shield node name must match the name "
            f"declared for the shield, which here is {source}: that name is "
            "what shield discovery and an instance's shield: reference both "
            f"resolve against\nnodes defined here: {defined}",
            (SourceRef(template, 1),),
        )
    ]


def _shield_yml_entries(
    shield_dir: str,
) -> tuple[str | None, list[tuple[str, Val, bool]], list[Diagnostic]]:
    """The declared names one folder's shield.yml carries, if it has one
    at all -- the SOLE IO this discovery rule performs per folder beside
    the `<name>.shield` presence probes its own caller does. One entry
    per `shield:` (a single mapping) or `shields:` (a list, upstream
    `b836fcdd709`'s mutually exclusive plural form -- `shield:` wins if a
    folder authors both, which the zephyr-side schema forbids and this
    parse therefore never has to adjudicate); `promotable` is THIS
    entry's own `template:` flag. A `shields:` block that is not a list
    at all, a `shields:` entry missing `name:`, and a name repeated
    within this SAME document are each dropped after their own
    lang-schema diagnostic -- rigc parses shield.yml with its own
    `parse_marked`, never jsonschema, so a malformed entry is this
    code's problem, not the schema's. None of the three may be dropped
    SILENTLY: every name a folder loses this way disappears from the
    shield namespace, and the only later symptom is an instance's
    shield: reference failing to resolve, a diagnostic pointing at the
    innocent rig rather than at the shield.yml that actually broke.

    Returns (yml_path, entries, diagnostics): `yml_path` is `None` (with
    `entries`/`diagnostics` both empty) when `shield_dir` has no
    shield.yml at all -- the caller's own signal to fall back to the
    legacy, folder-basename-derived name. `entries` and `diagnostics` are
    fresh lists the caller owns; `entries` preserves declaration order."""
    yml_path = os.path.join(shield_dir, "shield.yml")
    if not os.path.isfile(yml_path):
        return None, [], []
    doc = parse_marked(yml_path)  # Unimplemented on a YAML parse
    # failure -- no frozen golden
    # covers this shape
    diags: list[Diagnostic] = []
    out: list[tuple[str, Val, bool]] = []
    shield_v = doc.value.get("shield")
    raw: list[tuple[str, Val]]
    if shield_v is not None:
        raw = [("shield", shield_v)]
    else:
        plural_v = doc.value.get("shields")
        raw = []
        if plural_v is not None:
            if isinstance(plural_v.value, list):
                raw = [("shields", v) for v in plural_v.value]
            else:
                # One dash short: `shields:` with the entry's own keys
                # indented straight under it parses as a mapping, and a
                # mapping has no entries to yield. Reported here because
                # every name in this folder is lost by it -- the shield
                # simply ceases to exist, with nothing else in the scan
                # able to notice the folder ever meant to declare one.
                diags.append(
                    error(
                        "lang-schema",
                        "shield.yml: 'shields' must be a list of shield "
                        "entries -- use 'shield' for a single shield",
                        (plural_v.src,),
                    )
                )
    seen: set[str] = set()
    for key, entry_v in raw:
        name_v, d = require(entry_v, "name", f"shield.yml {key} entry")
        diags += d
        if name_v is None:
            continue
        name = str(name_v.value)
        if name in seen:
            diags.append(
                error(
                    "lang-schema",
                    f"shield.yml: '{name}' is declared more than once in this {key}: list",
                    (name_v.src,),
                )
            )
            continue
        seen.add(name)
        template_v = entry_v.value.get("template")
        promotable = bool(template_v.value) if template_v is not None else False
        out.append((name, entry_v, promotable))
    return yml_path, out, diags


def load_shield_library(
    workdir: str,
    shield_dirs: list[str] | None = None,
    types: dict[str, ConnectorType] | None = None,
    include_dirs: list[str] | None = None,
) -> tuple[ShieldLibrary, list[Diagnostic], Deps]:
    """Load every shield template. Each `.shield` file (base + any
    resolved revision fragment) is its OWN translation unit -- labels
    are shield-scoped, no cross-shield prefix discipline needed.

    `shield_dirs` is a LIST of shield-library roots, unioned into one
    library; None falls back to the vendored default (direct API / test
    use only). `types` is the connector-type registry every shield's plug
    is checked against; None falls back to `registry.load_types()`.

    Returns (library, diagnostics, deps): the library, with every
    discovered RIG TEMPLATE recorded as pending -- NOTHING parsed yet,
    regardless of whether it declares a `revisions:` axis; every
    scan-time finding in discovery order (a shield's own `revisions:`
    shape, a malformed `shields:` entry, a `template: true` entry with
    no matching `<name>.shield` -- see module docstring Sec "Discovery");
    and every file the scan actually READ (every shield.yml under
    `shield_dirs`, template or not, plus the connector-type registry) --
    a discovered `.shield` template is not itself a dependency until
    something references it (Sec 2.3). The caller owns all three."""
    diags: list[Diagnostic] = []
    deps: Deps = frozenset()
    if types is None:
        types, tdeps = load_types()
        deps = union(deps, tdeps)
    shields: dict[str, Shield] = {}
    axes: dict[str, AxisDecl | None] = {}
    pending: dict[str, _Pending] = {}
    ymls: dict[str, str] = {}
    promotable: dict[str, bool] = {}
    directories = shield_dirs if shield_dirs is not None else [SHIELDS_DIR]
    # A malformed member hard-errors the whole scan, but the members
    # already scanned may have reported findings of their own.
    # Re-raising with this scan's priors prepended ensures the boundary
    # that catches this exception renders every finding gathered so
    # far, not just the fatal one.
    try:
        for directory in directories:
            for shield_dir in sorted(glob.glob(os.path.join(directory, "*"))):
                if not os.path.isdir(shield_dir):
                    continue
                yml_path, entries, entry_diags = _shield_yml_entries(shield_dir)
                diags += entry_diags
                if yml_path is None:
                    # Legacy, yml-less folder (module docstring
                    # "Discovery", first bullet): the name is this
                    # folder's own basename.
                    name = os.path.basename(shield_dir)
                    base_file = os.path.join(shield_dir, name + ".shield")
                    if os.path.isfile(base_file):
                        axes[name] = None
                        pending[name] = _Pending(shield_dir, base_file, None)
                    continue
                for name, entry_v, entry_promotable in entries:
                    # The template itself is NOT touched here: a rig
                    # depends on a discovered shield's translation unit
                    # only once something actually references it,
                    # recorded by resolve()/_resolve_revision at that
                    # point instead.
                    ymls[name] = yml_path
                    promotable[name] = entry_promotable
                    if not entry_promotable:
                        continue  # a legacy shield carrying metadata
                    base_file = os.path.join(shield_dir, name + ".shield")
                    if not os.path.isfile(base_file):
                        diags.append(
                            error(
                                "lang-shield-template",
                                f"shield.yml declares '{name}' with template: "
                                f"true, but {base_file} does not exist -- a rig "
                                "template needs its own <name>.shield beside "
                                "shield.yml",
                                (entry_v.src,),
                            )
                        )
                        continue
                    decl, d = parse_legacy_revision_decl(
                        entry_v, "revisions", owner=f"shield '{name}'"
                    )
                    diags += d
                    axes[name] = decl
                    pending[name] = _Pending(shield_dir, base_file, decl, yml_path)
    except LoadError as e:
        raise LoadError(*diags, *e.diags) from None
    log.info("shield library: %d shields discovered", len(pending))
    lib = ShieldLibrary(
        shields=shields,
        axes=axes,
        pending=pending,
        ymls=ymls,
        types=types,
        workdir=workdir,
        include_dirs=include_dirs,
        promotable=promotable,
    )
    return lib, diags, deps
