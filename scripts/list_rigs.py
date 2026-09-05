#!/usr/bin/env python3
# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0

# Mirrors zephyr/scripts/list_shields.py, adapted to the rig folder model:
# a rig is a folder `boards/rigs/<dir>/rig.yml`. Following the same convention
# as boards (board.yml) and shields (shield.yml), the rig's IDENTITY is the
# `rig.name` field inside rig.yml — NOT the folder basename. The folder name is
# conventionally the same as the rig name but is not authoritative (exactly as
# list_shields.py takes the name from shield.yml's `name:`, not the folder).
#
# rig.yml holds ONLY metadata (name/revisions/variants) — never a
# hardware description. The assembled topology (instances/wires/dt-includes)
# lives in a separate, required content file, `<rigname>.yml`, which this
# module never opens: everything past the keys read below is the
# rigc loader's job, the canonical content parser.
#
# `board:` is NOT one of those keys:
# a rig has no board of its own to read any more, the invocation's own
# --board/-DBOARD is the only source, so this module never reads one out
# of rig.yml either — every board-shaped field below (Rig has none;
# resolve_target/dump_rig_target render {BOARD} as NOTFOUND unconditionally)
# exists only where a cmake consumer's own format string still expects the
# key.
#
# This is shared code between the build system's rig resolution
# (cmake/modules/boards.cmake's fork, `-DRIG=<target>` -> board; cmake/modules/dts.cmake's
# fork, `-DRIG=<target>` -> rig folder) and any future 'west rigs' extension
# command. If you change it, make sure all consumers still work.
#
# (Imports PyYAML like list_shields.py does — the same Zephyr venv dependency.)

import argparse
import json
import re
import sys
from dataclasses import dataclass, replace
from pathlib import Path

import yaml

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

RIG_YML = 'rig.yml'

# hwmv2-exact rig target grammar (`name[@rev][/variant]`) — the SAME
# three-way split `parse_board_components` (zephyr's
# cmake/modules/boards.cmake) applies to a board target, mirrored here
# for a rig's identity string: a rig target is symmetric with a board
# target, so its grammar and its parser are too.
#
# `[:opts]` extends it for PROMOTED SHIELDS ONLY: a
# promoted shield desugars to exactly ONE instance, so a target can name
# that instance's own fields — `flash_click:socket=quail_sock1`. A
# persisted rig has N instances, so `socket=` would not say WHICH, and
# `resolve_target` refuses opts on one; this parser only SPLITS them off,
# it never decides whether they are allowed (rigc.promote owns their
# content, the resolvers own the namespace rule).
#
# `:` and not `,` as the separator is forced, not chosen: devicetree
# property names contain commas (`zephyr,code`), and this grammar is
# meant to grow the `<device>.<prop>=<value>` parameter form next.
# The name stays `[^@/:]+`, so a `:` can never be read as part of it.
_RIG_TARGET_RE = re.compile(r'^([^@/:]+)(@[^@/:]+)?(/([^:]+))?(:(.+))?$')


@dataclass(frozen=True)
class Rig:
    name: str
    dir: Path
    # DECLARED qualifier axes (rig.yml revisions:/variants:), each
    # {'default': str|None, 'list': [str, ...]} or None if undeclared.
    revisions: dict | None = None
    variants: dict | None = None
    # SELECTED axis values, filled in only by resolve_rig_target (never by
    # find_rigs_in, which just enumerates declarations) -- None until then.
    revision: str | None = None
    variant: str | None = None


def rig_key(rig):
    return rig.name


def _revision_axis_shape(rig_data):
    """rig.yml's `revision:` block (hwmv2's own shape:
    `format:`/`default:`/`exact:`/a plural `revisions:` list of
    `{name:}` mappings), reshaped into the `{'default':, 'list': [...]}`
    this module's OWN `_resolve_axis`/`variant_names` already expect --
    kept in that shape rather than teaching those two hwmv2's own keys,
    since this module predicts cmake-side fragment filenames for the
    plain case (a bare target, or one naming a revision declared
    verbatim) ONLY. It does not implement `rigc.loader.axes`'s
    per-format validation, zero-append or nearest-lower match -- an
    undeclared-but-nearest-lower-eligible revision is rejected HERE,
    before `rigc expand` (the canonical validator, which DOES resolve
    it) ever runs; a known gap, not addressed here.
    None when rig.yml declares no `revision:` block at all."""
    block = rig_data.get('revision')
    if not isinstance(block, dict):
        return None
    names = [
        str(item['name'])
        for item in (block.get('revisions') or [])
        if isinstance(item, dict) and item.get('name') is not None
    ]
    return {'default': block.get('default'), 'list': names}


def variant_names(variants):
    """Bare variant-axis values, whichever shape variants: list: entries
    take -- a scalar, or a {name:} mapping. Display/reporting code that
    only wants the declared NAMES (west rigs' own variants= column) uses
    this rather than assuming every entry is already a bare string."""
    return [
        item.get('name') if isinstance(item, dict) else item
        for item in (variants or {}).get('list') or []
    ]


def find_rigs(args):
    ret = []

    for root in args.board_roots:
        for rig in find_rigs_in(root):
            ret.append(rig)

    return sorted(ret, key=rig_key)


def _load_rig(rig_dir, rig_yml):
    data = yaml.load(rig_yml.read_text(), Loader=SafeLoader) or {}
    rig_data = data.get('rig') or {}
    name = rig_data.get('name')
    if not name:
        sys.exit(f'ERROR: rig has no rig.name: {rig_yml.as_posix()}')
    # Declared axes: read here (not validated for shape -- rig.yml
    # carries only metadata, and this is enough to resolve a bare
    # target's default for filename construction, per
    # resolve_rig_target below; shape validation, and the separate
    # content file's own existence, are the rigc loader's job).
    return Rig(
        name=name,
        dir=rig_dir,
        revisions=_revision_axis_shape(rig_data),
        variants=rig_data.get('variants'),
    )


def _find_rigs_under(directory, ret):
    """Depth-first walk of one directory: a directory containing
    `rig.yml` IS a rig and is not descended
    into any further (a rig's own subdirectory -- e.g. a fixture rig's
    `shields/` -- must never be mistaken for a nested rig); a directory
    without one is purely a grouping folder (`boards/rigs/clash/`, e.g.)
    and is descended into looking for rigs one level down, or several.

    Depth is UNLIMITED by construction rather than capped at one extra
    level: the one known need is `boards/rigs/clash/<rig>/`, but a
    depth limit would be an arbitrary constant somebody hits later, and
    the recursive walk is exactly as much code as a fixed-depth one."""
    rig_yml = directory / RIG_YML
    if rig_yml.is_file():
        ret.append(_load_rig(directory, rig_yml))
        return

    for child in sorted(directory.iterdir()):
        if child.is_dir():
            _find_rigs_under(child, ret)


def find_rigs_in(root):
    rigs_dir = root / 'boards' / 'rigs'
    ret = []

    if not rigs_dir.exists():
        return ret

    for maybe_rig in rigs_dir.iterdir():
        if maybe_rig.is_dir():
            _find_rigs_under(maybe_rig, ret)

    return sorted(ret, key=rig_key)


def parse_rig_target(target):
    """Split a `-DRIG=<target>` value into `(name, revision, variant,
    opts)`, per the grammar above. Every one but `name` is `None` when
    absent (never an empty string), so a caller can tell "bare name"
    apart from a stray empty match cleanly.

    `opts` is the RAW text after the first `:`, unparsed — whether it is
    allowed at all is the resolvers' decision (promotion only), and what
    it means is `rigc.promote.parse_promotion_opts`'s. Splitting it here
    and interpreting it there keeps this module free of rigc imports on
    the bare `--list`/`--json` path.
    """
    m = _RIG_TARGET_RE.match(target)
    if not m:
        sys.exit(
            f"ERROR: invalid rig target syntax: {target!r} (expected name[@rev][/variant][:opts])"
        )
    name = m.group(1)
    revision = m.group(2)[1:] if m.group(2) else None
    variant = m.group(4)
    opts = m.group(6)
    return name, revision, variant, opts


def _resolve_axis(rig_name, axis_kind, decl_key, declared, selected):
    """Resolve one qualifier axis (revision or variant) against its rig.yml
    declaration: an explicitly selected value must be a declared member; a
    bare (unselected) axis takes the declared default, erroring if there is
    none. Mirrors rigc.loader.axes's own axis-resolution rules -- this
    lightweight copy exists so cmake can construct fragment filenames
    BEFORE ever invoking rigc; the loader is still the canonical
    validator once `rigc expand` itself runs (every real build reaches
    it). Returns the resolved value, or None if the axis is undeclared and
    nothing was selected.

    Membership is checked against variant_names(declared), never the raw
    list: entries directly -- a rig's variants: axis may declare its list
    as {name:} mappings, and comparing a selected bare name against a
    stringified MAPPING would never match. revisions: never takes that
    shape, so this is a no-op there."""
    if selected is not None:
        if declared is None:
            sys.exit(
                f"ERROR: rig '{rig_name}' names a {axis_kind} "
                f"({selected!r}), but this rig declares no "
                f"{decl_key}: at all."
            )
        values = [str(v) for v in variant_names(declared)]
        if selected not in values:
            sys.exit(
                f"ERROR: rig '{rig_name}': {axis_kind} '{selected}' is "
                f"not declared -- known {axis_kind}s: "
                f"{', '.join(values) or '(none)'}"
            )
        return selected
    if declared is None:
        return None
    default = declared.get('default')
    if default is not None:
        return str(default)
    values = [str(v) for v in variant_names(declared)]
    sys.exit(
        f"ERROR: rig '{rig_name}' names no {axis_kind}, and this rig "
        f"declares no default {axis_kind} -- choose one of: "
        f"{', '.join(values) or '(none)'}"
    )


def resolve_rig_target(target, args):
    """Resolve a FULL `-DRIG=<target>` string to the ONE rig it names — the
    cmake-facing seam for cmake/modules/boards.cmake's fork (the `-DBOARD`
    exclusivity FATAL) and cmake/modules/dts.cmake's
    fork (rig->folder resolution), plus any future `west rigs --rig
    <target>` use.

    Design rule 1: cmake never parses rig CONTENT — it
    hands this function the target VERBATIM; resolution semantics live here,
    never reimplemented in cmake. `@rev`/`/variant` resolve fully:
    the selected value is validated against the rig's OWN declared
    revisions:/variants: (or defaulted, for a bare target) and returned
    alongside NAME/DIR, so cmake can construct the per-axis fragment
    filenames (`<name>_<variant>.overlay` etc.) without parsing rig.yml
    itself. `rigc expand`, invoked later in the SAME configure, is the
    canonical validator (lang-rev/lang-variant diagnostics) -- this
    resolution exists so cmake has concrete axis strings to build filenames
    from, not to duplicate that diagnostic quality.

    No board is resolved here at all any more: a rig has none of its own
    to declare, so dump_rig_target's own `{BOARD}` key renders NOTFOUND
    unconditionally for every `Rig` this returns.

    Exits (via `sys.exit`, mirroring `find_rigs_in`'s existing error
    convention in this module) rather than raising, so a cmake
    `execute_process` caller sees a clean nonzero exit + stderr message with
    no Python traceback.
    """
    name, revision, variant, opts = parse_rig_target(target)
    rigs = find_rigs(args)
    for rig in rigs:
        if rig.name == name:
            # Promotion options are PROMOTION-only. A persisted rig has N
            # instances, so `socket=` could not say which one it means --
            # refused here rather than silently dropped, which would
            # build something the target did not ask for. Refused at the
            # point the name is KNOWN to be a rig, so the message can say
            # so.
            if opts is not None:
                sys.exit(
                    f"ERROR: -DRIG={target}: '{name}' is a persisted rig, "
                    f"and promotion options ({opts!r}) apply only to a "
                    f"promoted shield -- a rig has its own instances, "
                    f"each already naming its own socket in the rig's "
                    f"content file."
                )
            resolved_revision = _resolve_axis(
                rig.name, 'revision', 'revision', rig.revisions, revision
            )
            resolved_variant = _resolve_axis(rig.name, 'variant', 'variants', rig.variants, variant)
            return replace(rig, revision=resolved_revision, variant=resolved_variant)
    available = ', '.join(r.name for r in rigs) or '(none)'
    sys.exit(f"ERROR: -DRIG={target} does not resolve to a rig.\n  available rigs: {available}")


@dataclass(frozen=True)
class PromotedTarget:
    """A `-DRIG=<target>` that resolved as a promoted SHIELD rather than a
    persisted rig -- `resolve_target`'s other possible return value,
    alongside `Rig`. `name`/
    `revision` are exactly `rigc.promote.promote_shield`'s own two
    arguments; a promoted shield has no variant axis (the resolver already
    refuses one), so there is nothing to carry for it. `dump_rig_target` tells
    this apart from a `Rig` by type and renders `{PROMOTED}=target`,
    `{DIR}=NOTFOUND` (no rig folder exists), `{BOARD}=NOTFOUND` (a shield
    declares none), `{VARIANT}=NOTFOUND`.

    `opts` is the promotion options text (`socket=quail_sock1`), already
    VALIDATED by `rigc.promote.parse_promotion_opts` before this is
    built. `promotion_target` re-renders name+opts as the single string
    `{PROMOTED}` carries and `rigc expand --promote` takes back: cmake
    forwards that value opaquely and never parses it, so the option
    grammar has exactly one parser no matter how many options it grows.
    That is why no new `{PROMOTED_SOCKET}` cmakeformat key and no new
    rigc flag were added -- cmake learns no new concept at all.

    The REVISION is deliberately NOT rendered into it, even though it is
    part of the target the user typed: it already travels on its own
    `{REVISION}` key, which dts.cmake forwards as `--revision`. Rendering
    it here too would reach `promote_shield` twice and desugar to
    `shield: i2c_sensor@2@2`. `test_cmakeformat_line_for_a_revved_
    promoted_shield` is what caught that, which is exactly why it pins
    the whole line rather than just the key under test.
    """

    name: str
    revision: str | None = None
    opts: str | None = None

    @property
    def promotion_target(self):
        """The `--promote` value: this target as rigc will re-parse it.
        Revision excluded on purpose -- see the class docstring."""
        return f"{self.name}:{self.opts}" if self.opts else self.name


@dataclass(frozen=True)
class PromotedListTarget:
    """A `-DRIG=<target>` that resolved as a LIST of promoted shields:
    `target` splits on `;` into two or more elements, each independently
    validated exactly as a single promoted
    shield already is (namespace collision via `promote.both_paths_
    error`, promotability via `promote.check_promotable`, the slot/param
    grammar via `promote.parse_promotion_opts`) plus the two checks a
    list adds -- every element must be a SHIELD, never a persisted rig,
    and no shield name may repeat across elements
    (`promote.list_element_is_a_rig_error`/`promote.check_list_no_
    duplicate_elements`). `resolve_target`'s third possible return
    value, alongside `Rig` and `PromotedTarget`.

    `name` is the desugared rig's own identity (Sec 2's ruling): every
    element's shield name joined with `+`, the identical string
    `rigc.promote.promote_shield_list` writes into the synthesized
    rig.yml's own `name:` field.

    `raw` is `target` itself, VERBATIM -- unlike a single-shield
    `PromotedTarget`, a list has no single shield revision to exclude
    onto a separate `{REVISION}` key (each element carries its OWN
    `@rev`, already inline in `raw`), so there is nothing left to strip;
    `raw` IS the `--promote` value this desugars to, and `cli.py`'s own
    list branch reparses it the identical way (split on `;`, then each
    element exactly as a single `--promote` target already parses).

    `dump_rig_target` tells this apart from `Rig`/`PromotedTarget` by
    type, rendering `{PROMOTED}=raw` (escaped, see `_cmake_list_
    escape`), `{NAME}=name`, `{DIR}=NOTFOUND`, `{BOARD}=NOTFOUND`,
    `{REVISION}=NOTFOUND`, `{VARIANT}=NOTFOUND` -- a list promotion has
    no revision/variant axis of its own to select (each element's own
    `@rev`, if any, already travels inside `raw`)."""

    name: str
    raw: str

    @property
    def promotion_target(self):
        """The `--promote` value: `raw`, verbatim -- see the class
        docstring for why a list needs no revision-stripping the way a
        single-shield `PromotedTarget` does."""
        return self.raw


def _cmake_list_escape(value: str) -> str:
    """Escape every literal `;` in `value` TWICE over, for embedding as
    the `{PROMOTED}` field of this module's own `--cmakeformat` line
    (`dump_rig_target`) when `value` is a list promotion target's raw
    text (the only value any cmakeformat field ever carries a literal
    `;` in -- NAME/DIR/BOARD/REVISION/VARIANT never do: shield/rig
    names, paths and axis values). Verified empirically against this
    tree's own CMake (4.3): `cmake/modules/boards.cmake`'s and `cmake/modules/dts.cmake`'s
    own Step 1/Step 3 each reconstruct NAME/DIR/.../PROMOTED from one
    `execute_process` capture via `cmake_parse_arguments(... ${captured})`
    -- and `cmake_parse_arguments` itself consumes TWO levels of
    unquoted-list-expansion internally, not the one a naive reading of
    "one unquoted hop, one escape level" would predict, so the value
    must survive two rounds of un-escaping to land back as ONE token
    (`_RIG_RESOLVED_PROMOTED`/`_RIG_FALLBACK_PROMOTED`). `cmake/
    dts.cmake` then escapes it AGAIN, twice more, of its own accord
    (its own comment, right before `list(APPEND _rig_debug_argv
    --promote ...)`) to survive the TWO further unquoted hops composing
    and running the actual rigc command makes.

    A value with no `;` at all round-trips through this as an identity
    (nothing to escape). Returns a fresh string the caller owns."""
    escaped = value
    for _ in range(2):
        escaped = escaped.replace(";", "\\;")
    return escaped


def resolve_target(target, args):
    """The actual `-DRIG=<target>` entry point for cmake/modules/boards.cmake's
    and cmake/modules/dts.cmake's forks,
    superseding a bare `resolve_rig_target` call: resolves `target`
    against BOTH namespaces -- a persisted rig (this module's own `find_
    rigs`) wins, a discoverable, PROMOTABLE shield (`rigc.promote`,
    reusing `loader/library.py`'s own scan) is the fallback, and a name
    that is both is an error naming both paths, via the SAME `rigc.
    promote.both_paths_error` `west rigs --explain` already renders --
    one namespace rule, never two independently-worded ones.

    Shield discovery is scanned at the SAME breadth `find_rigs` uses
    (every board_root's own boards/shields) -- `rigc.promote.discover_
    shields`'s own default (the vendored library alone) is narrower, and
    using it here would make a shield in another module invisible to
    `-DRIG` AND silently uncollidable with a same-named rig: the
    namespace rule failing open rather than erroring, exactly the trap
    `--explain`'s own review already caught once.

    A neither-rig-nor-shield target, and a plain rig target (axis
    resolution, the rig-swap comparison inputs), fall through to `resolve_
    rig_target` UNCHANGED -- reused rather than re-derived, per design
    rule 1 (cmake/rig resolution semantics live in exactly one place).

    A target containing `;` is a LIST
    promotion target, delegated to `_resolve_list_target` in full --
    checked FIRST, before `target` is ever handed to `parse_rig_target`
    (whose own `[^@/:]+` name group happily swallows a literal `;` as
    part of a bogus "name", which is exactly why a one-element list
    -- no `;` present at all -- must fall through UNCHANGED to the
    single-target code below rather than through any generalized
    N-element path: splitting on a separator that is not there changes
    nothing, so this file's existing single-target behavior stays
    byte-identical by construction, never by a
    second code path merely proven to agree with it.

    Returns the resolved `Rig` (identical to a bare `resolve_rig_target`
    call), a `PromotedTarget`, or a `PromotedListTarget` -- the caller
    owns whichever came back; `dump_rig_target` tells all three apart by
    `isinstance`. Exits via `sys.exit` on every failure mode (unresolved
    target, both-paths collision, an unpromotable or `/variant`-
    qualified shield, a list element naming a rig, a duplicate shield
    name across elements), matching every other resolution failure in
    this module, so a cmake `execute_process` caller sees a clean
    nonzero exit + stderr with no traceback."""
    if ';' in target:
        return _resolve_list_target(target, args)

    from rigc import promote  # local: a bare `--list`/`--json` listing
    # (this module's OTHER entry point) never needs rigc's own import
    # graph, so it stays untouched by anything importable here.

    name, revision, variant, opts = parse_rig_target(target)
    rigs = find_rigs(args)
    rig = next((r for r in rigs if r.name == name), None)
    shield_dirs = [str(Path(root) / 'boards' / 'shields') for root in args.board_roots]
    shields = promote.discover_shields(shield_dirs)

    if rig is not None and name in shields:
        sys.exit(f'ERROR: {promote.both_paths_error(name, rig.dir, shields[name].dir)}')

    if rig is None and name in shields:
        # Resolved here, ahead of check_promotable and of
        # parse_promotion_opts's own slot-validation grammar:
        # discover_shields' scan is deliberately lazy and never opens
        # the template itself, so the shield's real slot names need
        # their own small parse.
        resolved = promote.resolve_for_promotion(name, shield_dirs)
        err = promote.check_promotable(name, shields[name], variant)
        if err is not None:
            sys.exit(f'ERROR: {err}')
        # Parsed HERE, at resolution time, so a malformed option is a
        # clean cmake-visible exit before rigc runs -- not a
        # traceback three processes deep. The parsed mapping is
        # discarded: rigc re-parses the same text from --promote, and
        # ONE parser owning the grammar is the point (see
        # PromotedTarget). What this call buys is the early refusal.
        parsed = promote.parse_promotion_opts(opts, target, resolved)
        if isinstance(parsed, str):
            sys.exit(f'ERROR: {parsed}')
        return PromotedTarget(name=name, revision=revision, opts=opts)

    return resolve_rig_target(target, args)


def _resolve_list_target(target, args):
    """`resolve_target`'s list-promotion branch: split `target` on `;` and
    resolve/validate every element
    exactly as a single target already does above -- namespace
    collision via `promote.both_paths_error`, promotability via
    `promote.check_promotable`, the slot/param grammar via `promote.
    parse_promotion_opts` -- plus the two checks a list adds: every
    element must be a SHIELD (`promote.list_element_is_a_rig_error` when
    it names a persisted rig instead, `promote.list_element_not_a_
    shield_error` when it names neither), and no shield name may repeat
    across elements (`promote.check_list_no_duplicate_elements`).

    Exits via `sys.exit` on every refusal, matching every other
    resolution failure in this module. Returns a `PromotedListTarget`
    naming the desugared rig (`resolve_target`'s own third return
    shape)."""
    from rigc import promote

    rigs_by_name = {r.name: r for r in find_rigs(args)}
    shield_dirs = [str(Path(root) / 'boards' / 'shields') for root in args.board_roots]
    shields = promote.discover_shields(shield_dirs)

    names = []
    for element in target.split(';'):
        name, _revision, variant, opt_text = parse_rig_target(element)
        rig = rigs_by_name.get(name)
        if rig is not None and name in shields:
            sys.exit(f'ERROR: {promote.both_paths_error(name, rig.dir, shields[name].dir)}')
        if rig is not None:
            sys.exit(f'ERROR: {promote.list_element_is_a_rig_error(name, target, rig.dir)}')
        if name not in shields:
            sys.exit(f'ERROR: {promote.list_element_not_a_shield_error(name, target)}')
        resolved = promote.resolve_for_promotion(name, shield_dirs)
        err = promote.check_promotable(name, shields[name], variant)
        if err is not None:
            sys.exit(f'ERROR: {err}')
        parsed = promote.parse_promotion_opts(opt_text, element, resolved)
        if isinstance(parsed, str):
            sys.exit(f'ERROR: {parsed}')
        names.append(name)

    dup_err = promote.check_list_no_duplicate_elements(names, target)
    if dup_err is not None:
        sys.exit(f'ERROR: {dup_err}')

    return PromotedListTarget(name='+'.join(names), raw=target)


def parse_args():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    add_args(parser)
    add_args_formatting(parser)
    return parser.parse_args()


def add_args(parser):
    parser.add_argument(
        "--board-root",
        dest='board_roots',
        default=[],
        type=Path,
        action='append',
        help='add a board root, may be given more than once',
    )
    parser.add_argument(
        "--rig",
        dest='rig',
        default=None,
        help='resolve a single rig target '
        '(name[@rev][/variant][:opts]) instead of listing '
        'every rig; prints via --cmakeformat if given, '
        'else just the resolved name',
    )


def add_args_formatting(parser):
    parser.add_argument(
        "--json", action='store_true', help='''output list of rigs in JSON format'''
    )
    parser.add_argument(
        "--cmakeformat",
        default=None,
        help='CMake format string for --rig (mirrors '
        "list_boards.py's --board query mode); "
        'available keys: {NAME}, {DIR}, {BOARD}, '
        '{REVISION}, {VARIANT}, {PROMOTED} (the '
        'shield name when --rig resolved as a '
        'promoted shield, the raw `;`-joined '
        'target when it resolved as a promoted '
        'list, NOTFOUND otherwise)',
    )


def dump_rigs(rigs, args):
    """--list / --json never resolves a target axis. 'board' stays a JSON
    key for format stability but is always None now: no rig declares one
    any more, of any shape, so there is nothing left to read into it."""
    if args.json:
        print(
            json.dumps(
                [
                    {
                        'dir': rig.dir.as_posix(),
                        'name': rig.name,
                        'board': None,
                        'revisions': rig.revisions,
                        'variants': rig.variants,
                    }
                    for rig in rigs
                ]
            )
        )
    else:
        for rig in rigs:
            print(f'  {rig.name}')


def dump_rig_target(resolved, args):
    """Renders a `resolve_target` answer -- a `Rig` (unchanged from
    before promoted shields existed), a `PromotedTarget`, or a
    `PromotedListTarget` -- via
    `--cmakeformat`, or just the resolved name without it. A
    `PromotedTarget`/`PromotedListTarget` has no folder and no variant
    of its own by construction; `{PROMOTED}` is the shield
    name (or, for a list, the raw target text) for one of those and
    NOTFOUND for an ordinary `Rig`, so a cmake caller tells them apart
    on that key alone without needing to special-case DIR being empty.
    `{BOARD}` is unconditionally NOTFOUND for ALL THREE -- neither a
    promoted shield, a promoted list, nor a persisted rig has one of its
    own to declare any more; the key stays in the format string only
    because cmake/modules/boards.cmake's fork still parses it.

    A `PromotedListTarget`'s own `{PROMOTED}` value is the ONE field
    ever escaped (`_cmake_list_escape`) -- its raw text legitimately
    carries a `;`, which every other field/branch here never does."""
    if args.cmakeformat is not None:

        def notfound(x):
            return x or 'NOTFOUND'

        if isinstance(resolved, PromotedListTarget):
            info = args.cmakeformat.format(
                NAME='NAME;' + resolved.name,
                DIR='DIR;NOTFOUND',
                BOARD='BOARD;NOTFOUND',
                REVISION='REVISION;NOTFOUND',
                VARIANT='VARIANT;NOTFOUND',
                PROMOTED='PROMOTED;' + _cmake_list_escape(resolved.promotion_target),
            )
        elif isinstance(resolved, PromotedTarget):
            info = args.cmakeformat.format(
                NAME='NAME;' + resolved.name,
                DIR='DIR;NOTFOUND',
                BOARD='BOARD;NOTFOUND',
                REVISION='REVISION;' + notfound(resolved.revision),
                VARIANT='VARIANT;NOTFOUND',
                PROMOTED='PROMOTED;' + resolved.promotion_target,
            )
        else:
            info = args.cmakeformat.format(
                NAME='NAME;' + resolved.name,
                DIR='DIR;' + resolved.dir.as_posix(),
                BOARD='BOARD;NOTFOUND',
                REVISION='REVISION;' + notfound(resolved.revision),
                VARIANT='VARIANT;' + notfound(resolved.variant),
                PROMOTED='PROMOTED;NOTFOUND',
            )
        print(info)
    else:
        print(resolved.name)


if __name__ == '__main__':
    args = parse_args()
    if args.rig is not None:
        dump_rig_target(resolve_target(args.rig, args), args)
    else:
        dump_rigs(find_rigs(args), args)
