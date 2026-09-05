# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""The `--rig <shield>` desugaring and the namespace rule that decides
when a bare name resolves as a shield at all -- everything
`west rigs --explain` (west_commands/rigs.py) needs, factored so the
printer stays a thin caller over pure values.

Three things:

  promote_shield()   -- the natural mapping a -> [a], PURE: a shield
                        name (+ optional revision) -> the rig.yml/
                        content-file TEXT a checked-in rig meaning the
                        same thing would have to contain.
  discover_shields() -- the IO edge: which names ARE shields at all,
                        reusing loader/library.py's OWN scan verbatim
                        (never a second glob restating it, so
                        "resolvable by rigc" and "known here"
                        cannot drift apart) -- plus, per shield.yml, its
                        `template:` flag, the SECOND authority that
                        marks a shield PROMOTABLE.
  check_promotable() / both_paths_error() -- the promotability gate and
                        the namespace rule's "both" branch, pure
                        decisions over already-discovered facts.

No cmake, no cpp, no board: printing a promoted shield's two documents
needs none of rigc's heavier machinery -- `promote_shield` never touches
a filesystem. `rigc.loader.load` is what PROVES the printed text is real
(the round-trip test); this module never imports it."""

from __future__ import annotations

import os
import re
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from .diag import SourceRef
from .loader.library import load_shield_library
from .loader.params import device_required_params
from .model import ConnectorType, Shield


@dataclass(frozen=True)
class ShieldInfo:
    """One name `discover_shields` found -- a rig template
    (`loader/library.py`'s own `pending`) or a legacy shield whose
    shield.yml merely declares metadata (never a `<name>.shield` marker
    of its own kind that library.py resolves against). `template` is
    THIS entry's own `template:` flag, the PROMOTABLE authority -- since
    a folder may host more than one shield name, a name's OWN entry
    carries this flag, not its folder's, so two names sharing one folder
    may answer differently. `has_yml` distinguishes "no shield.yml at
    all" from "shield.yml present but omits the flag" -- the two reasons
    `check_promotable`'s error tells apart."""

    name: str
    dir: str
    template: bool
    has_yml: bool


def discover_shields(
    shield_dirs: list[str] | None = None,
    types: dict[str, ConnectorType] | None = None,
    include_dirs: list[str] | None = None,
) -> dict[str, ShieldInfo]:
    """Every name `loader/library.py`'s own scan discovers, keyed by
    name -- every resolvable rig template (`lib.pending`) UNION every
    name any shield.yml under `shield_dirs` declares (`lib.ymls`), since
    a legacy shield with metadata but no matching `<name>.shield` is
    still a name `check_promotable` must be able to name and explain.
    Reuses that ONE scan verbatim (`load_shield_library`) rather than a
    second glob,
    so a name this module calls a shield and a name rigc can
    actually resolve `shield:` against never disagree; `template` reads
    `lib.promotable` -- the same per-entry `template:` flag the scan
    already read off shield.yml -- rather than re-opening any file this
    module's own caller already paid to parse.

    `types` is the connector-type registry every scanned shield's plug is
    checked against; None falls back to `registry.load_types()`, whose own
    default root is module-relative and therefore a dev/test convenience
    only -- a caller running outside this module's own repository (a test
    against vendored fixtures, or a downstream consumer) must pass one, or
    the fallback raises. Threaded here for the same reason
    `load_shield_library` already accepts it.

    `shield_dirs` defaults to the vendored shield library
    (`load_shield_library`'s own default), which is narrower than the rig
    namespace a caller resolves against: `west rigs` finds rigs under EVERY
    module board root, so a caller comparing the two namespaces must pass
    the matching `<root>/boards/shields` list, or a shield in another
    module is invisible here and the both-a-rig-and-a-shield collision
    goes undetected. A root with no `boards/shields` simply contributes
    nothing. The scan's `workdir` argument
    is never touched by a scan that resolves nothing -- no `.resolve()`
    call happens here -- so an inert placeholder is passed rather than
    creating a real temporary directory for what is a read-only query.

    Discovery-time diagnostics (a malformed shield.yml `revisions:`
    block, a `template: true` entry with no matching `<name>.shield`)
    are discarded here: they concern a shield's own template/axis shape,
    orthogonal to the promotability question this function answers, and
    a caller that actually loads a rig (never this function alone) is
    what surfaces them. Returns a dict the caller owns."""
    lib, _diags, _deps = load_shield_library(
        "<rigc-promote-discovery-unused>", shield_dirs, types=types, include_dirs=include_dirs
    )
    out: dict[str, ShieldInfo] = {}
    for name in set(lib.pending) | set(lib.ymls):
        has_yml = name in lib.ymls
        shield_dir = (
            lib.pending[name].shield_dir if name in lib.pending else os.path.dirname(lib.ymls[name])
        )
        template = lib.promotable.get(name, False) if has_yml else False
        out[name] = ShieldInfo(name=name, dir=shield_dir, template=template, has_yml=has_yml)
    return out


@dataclass(frozen=True)
class PromotedRig:
    """The two documents `promote_shield` synthesizes, plus the content
    file's own NAME -- returned together so a caller never re-derives the
    filename from the rig name itself (documents.content_file_name's own
    convention, restated here in text form since `promote_shield` is pure
    and takes no rig directory to build a real path from). Every string
    is newline-terminated; copied verbatim into
    `boards/rigs/<name>/rig.yml` and `boards/rigs/<name>/<content_name>`
    respectively, the two files load through `rigc.loader.load` with no
    diagnostics given a board (the printed rig.yml
    declares no board of its own, so an INJECTED one is what a real
    build -- or this module's own round-trip test -- supplies) -- that
    is this dataclass's whole contract."""

    rig_yml: str
    content_name: str
    content: str


#: The promotion options a target string may carry after `:`. A CLOSED
#: set, deliberately: `socket` alone to start, everything else later.
#: Two names are excluded on purpose rather than merely absent --
#: `name`, because the singleton desugaring law pins the desugared
#: instance name to the shield name and that name reaches
#: config-sheet.md, so a CLI slot for it would let a user break the law
#: from the command line; and `shield`, which is the target itself.
#:
#: A key containing a literal `.` is never a member of this tuple, and
#: never will be: it is either a `<device>.<prop>` parameter assignment
#: or, when the device-label half is exactly `socket`, a per-slot
#: `socket.<slot>=<value>` option -- a REFINEMENT of this one existing
#: key, not a new fixed keyword growing this set. Consequence, made
#: loud rather than latent: a shield device labeled literally `socket`
#: can no longer receive a promotion parameter through this grammar.
#:
#: `config` is `socket`'s exact analogue: when the device-label half of
#: a dotted key is exactly `config`, the property-name half is a
#: config-element LABEL (a strap or routing jumper,
#: `Shield.config_element`), not a device property, and the assignment
#: routes to `ParsedPromotionOpts.config` instead of `params` --
#: reserved unconditionally, the same trade `socket` already accepted:
#: a shield device labeled literally `config` can no longer receive a
#: promotion parameter through this grammar (and, one layer down, a
#: shield's own DTS already reserves `config` as its config-elements
#: node name, so this collision was accepted there first).
_PROMOTION_OPTS = ("socket",)


@dataclass(frozen=True)
class ParsedPromotionOpts:
    """A parsed promotion target's `:`-separated assignment list, split
    into its four grammar categories: `fixed`, the closed
    `_PROMOTION_OPTS` keywords other than the slot form (today just bare
    `socket=`, single-plug only); `sockets`, every `socket.<slot>=<value>`
    slot assignment (slot name -> board socket label, plural shields
    only); `config`, every `config.<label>=<value>` config-element
    assignment (config-element LABEL -> value -- the routing-jumper/
    strap analogue of `sockets`, reserved the same unconditional way);
    and `params`, every other `<device>.<prop>=<value>` assignment --
    device label -> property name -> value, the identical shape
    `Instance.params` (model.py) already carries, so `promote_shield` can
    print it with the SAME structure a real rig.yml's own params: block
    already uses. A flat `Dict[str, str]` cannot hold all four without
    overloading one key namespace with unrelated meanings, so each lives
    in its own field.

    All four are fresh dicts/mappings the caller owns."""

    fixed: dict[str, str]
    params: dict[str, dict[str, str]]
    sockets: dict[str, str] = field(default_factory=dict)
    config: dict[str, str] = field(default_factory=dict)


def parse_promotion_opts(
    opts: str | None,
    target: str,
    shield: Shield | None = None,
) -> ParsedPromotionOpts | str:
    """Parse the `:`-separated assignment list a promotion target may
    carry -- `<shield>[@rev][:<key>=<value>[:<key>=<value>...]]` -- into
    a `ParsedPromotionOpts` for the ONE desugared instance.

    Returns the parsed opts, or an ERROR MESSAGE string when the text
    does not parse (the same return convention `check_promotable` uses,
    so a caller handles both refusals the same way). `None`/empty opts
    parses to an empty `ParsedPromotionOpts`, never an error.

    EXPLICIT `key=value` ONLY, with no bare-word shorthand for the
    common case: `flash_click:quail_sock1` is refused, not read as a
    socket. A positional rule would have to be re-litigated the moment
    a second option lands.

    `:` separates, NOT `,` -- and that is a hard constraint, not a
    preference: real devicetree property names contain commas
    (`zephyr,code` is exactly the property the two param-blocked shields
    need), so a comma-separated list could never carry the parameter
    syntax this grammar is designed to grow into.

    A key containing a literal `.` is split on the FIRST dot only
    (`str.partition`, never `str.split`), into a device label and a
    property name, everything after the first dot -- dots included --
    staying part of the property name (devicetree property names may
    legally contain a literal `.` themselves; shield-local device labels
    in this corpus never do, so the first dot is always the real
    boundary). When the device-label half is exactly `socket`, the
    property-name half is a SLOT name, not a property, and the
    assignment routes to `sockets` -- reserved unconditionally, never
    checked against a shield's real device labels (`promote_shield`
    never validates device/property existence either; that stays the
    loader's job). When the device-label half is exactly `config`, the
    property-name half is a config-element LABEL, not a property, and
    the assignment routes to `config` -- the exact same analogy, reserved
    unconditionally and
    never validated against the shield's real config elements here: a
    label naming no strap/jumper of the shield is refused by the loader
    (`rigc.loader.params.apply_config_block`), which already renders the
    valid labels on a miss, not by this function. An empty label or an
    empty value under `config.` is refused with its own sentence, and a
    label given more than once within one target is refused
    unconditionally, mirroring `sockets`'/`params`' own duplicate rule
    exactly.

    `shield`, when given -- the caller's own already-resolved
    `resolve_for_promotion` result -- supplies the slot-validation
    context the `socket.<slot>=`/bare-`socket=` grammar needs against
    ITS real slots: a bare `socket=` on a plural shield, a
    `socket.<slot>=` on a single-plug one, and a `socket.<slot>=`
    naming a slot the shield does not have are each refused with their
    own sentence. `None` (the default) skips all three checks --
    backward-compatible for a caller that has not resolved the shield
    at all. A duplicate slot assignment within one target is refused
    unconditionally, needing no shield at all (it is a property of the
    target string alone, exactly like a duplicate fixed key or
    parameter)."""
    if not opts:
        return ParsedPromotionOpts(fixed={}, params={}, sockets={}, config={})
    fixed: dict[str, str] = {}
    params: dict[str, dict[str, str]] = {}
    sockets: dict[str, str] = {}
    config: dict[str, str] = {}
    plural = shield is not None and shield_is_multiplug(shield)
    for assignment in opts.split(":"):
        key, sep, value = assignment.partition("=")
        if not sep:
            return (
                f"'{target}': promotion option '{assignment}' is not "
                f"'<key>=<value>' -- promotion options are explicit "
                f"assignments (known keys: "
                f"{', '.join(_PROMOTION_OPTS)})"
            )
        if "." in key:
            err = _route_dotted_promotion_assignment(
                key, value, target, shield, plural, sockets, config, params
            )
            if err is not None:
                return err
            continue
        if key not in _PROMOTION_OPTS:
            return (
                f"'{target}': unknown promotion option '{key}' "
                f"(known keys: {', '.join(_PROMOTION_OPTS)})"
            )
        if key == "socket" and plural:
            assert shield is not None  # plural is only True when shield is
            return (
                f"'{target}': shield plugs {len(shield.plugs)} "
                f"sockets -- use socket.<slot>=<label> (slots: "
                f"{', '.join(shield.plugs)}), not bare socket=<label>"
            )
        if key in fixed:
            return f"'{target}': promotion option '{key}' given more than once"
        if not value:
            return f"'{target}': promotion option '{key}=' has an empty value"
        fixed[key] = value
    return ParsedPromotionOpts(fixed=fixed, params=params, sockets=sockets, config=config)


def _route_dotted_promotion_assignment(
    key: str,
    value: str,
    target: str,
    shield: Shield | None,
    plural: bool,
    sockets: dict[str, str],
    config: dict[str, str],
    params: dict[str, dict[str, str]],
) -> str | None:
    """Route one dotted `<label>.<name>=<value>` promotion assignment
    (`key` already confirmed to contain a `.`) to whichever of
    sockets/config/params its label half selects -- `socket` and
    `config` are the two reserved labels (`parse_promotion_opts`'s own
    docstring), any other label a device parameter. Mutates whichever
    of sockets/config/params the assignment belongs to in place; shield
    is read-only. Returns an error message naming why the assignment is
    refused, or None once it has been recorded."""
    dev_label, _, prop_name = key.partition(".")
    if not dev_label or not prop_name:
        return (
            f"'{target}': promotion parameter '{key}' is not "
            f"'<device>.<prop>=<value>' -- both the device "
            f"label and the property name must be non-empty"
        )
    if dev_label == "socket":
        return _parse_socket_slot_assignment(prop_name, value, target, shield, plural, sockets)
    if dev_label == "config":
        return _parse_config_label_assignment(prop_name, value, target, config)
    return _parse_promotion_param_assignment(dev_label, prop_name, value, target, params)


def _parse_socket_slot_assignment(
    slot_name: str,
    value: str,
    target: str,
    shield: Shield | None,
    plural: bool,
    sockets: dict[str, str],
) -> str | None:
    """Route one `socket.<slot>=<value>` assignment against `shield`'s
    real slots -- reserved unconditionally, never checked against a
    shield's real device labels. Mutates sockets in place; shield is
    read-only. Returns an error message on a malformed, unknown-slot,
    or duplicate assignment, None once recorded."""
    if shield is not None and not plural:
        return (
            f"'{target}': shield has a single plug -- use "
            f"socket=<label>, not socket.{slot_name}="
            f"<label>"
        )
    if shield is not None and slot_name not in shield.plugs:
        return (
            f"'{target}': socket.{slot_name} names unknown "
            f"slot '{slot_name}' -- known slots: "
            f"{', '.join(shield.plugs)}"
        )
    if slot_name in sockets:
        return f"'{target}': slot 'socket.{slot_name}' given more than once"
    if not value:
        return f"'{target}': promotion slot option 'socket.{slot_name}=' has an empty value"
    sockets[slot_name] = value
    return None


def _parse_config_label_assignment(
    label_name: str, value: str, target: str, config: dict[str, str]
) -> str | None:
    """Route one `config.<label>=<value>` assignment -- `socket`'s exact
    analogue, reserved unconditionally and never validated against the
    shield's real config elements here (`rigc.loader.params.
    apply_config_block` is the one place a miss already renders the
    valid labels). Mutates config in place. Returns an error message on
    a duplicate or empty-value assignment, None once recorded."""
    if label_name in config:
        return f"'{target}': config label 'config.{label_name}' given more than once"
    if not value:
        return f"'{target}': promotion config option 'config.{label_name}=' has an empty value"
    config[label_name] = value
    return None


def _parse_promotion_param_assignment(
    dev_label: str, prop_name: str, value: str, target: str, params: dict[str, dict[str, str]]
) -> str | None:
    """Route one `<device>.<prop>=<value>` parameter assignment -- the
    residual dotted-key case once `socket`/`config` are ruled out.
    Mutates params in place. Returns an error message on a duplicate or
    empty-value assignment, None once recorded."""
    if prop_name in params.get(dev_label, {}):
        return f"'{target}': parameter '{dev_label}.{prop_name}' given more than once"
    if not value:
        return f"'{target}': promotion parameter '{dev_label}.{prop_name}=' has an empty value"
    params.setdefault(dev_label, {})[prop_name] = value
    return None


def _render_instance(
    name: str,
    revision: str | None = None,
    socket: str | None = None,
    sockets: dict[str, str] | None = None,
    config: dict[str, str] | None = None,
    params: dict[str, dict[str, str]] | None = None,
) -> str:
    """One `instances:` list entry, exactly the text `promote_shield`
    prints for its single instance -- factored out so `promote_shield`
    (unchanged behavior) and `promote_shield_list` render every instance
    through the identical code, which is what makes a one-element list
    byte-identical to `promote_shield`'s
    own output BY CONSTRUCTION rather than by two hand-synchronized
    string builders. See `promote_shield`'s own docstring for what each
    argument means; this function differs only in returning the ONE
    instance's own block (`  - name: ...` through its trailing
    `params:`, if any) rather than a full `PromotedRig`.

    Print order is FIXED: `socket:`/`sockets:`, then `config:`, then
    `params:` -- exactly where `boards/rigs/nucleo_wifi_logger_ok/
    nucleo_wifi_logger_ok.yml` puts its own `config:` block, and
    matching `_promotion_target`'s own CLI-option order
    (test_singleton_identity_law.py) so the two sides of the singleton
    law cannot drift.

    Returns a fresh string the caller owns, always ending in `\\n`."""
    shield_ref = f"{name}@{revision}" if revision else name
    block = f"  - name: {name}\n    shield: {shield_ref}\n"
    if sockets:
        block += "    sockets:\n"
        for slot_name, label in sockets.items():
            block += f"      {slot_name}: {label}\n"
    elif socket is not None:
        block += f"    socket: {socket}\n"
    if config:
        block += "    config:\n"
        for label, value in config.items():
            block += f"      {label}: {value}\n"
    if params:
        block += "    params:\n"
        for dev_label, props in params.items():
            block += f"      {dev_label}:\n"
            for prop_name, value in props.items():
                block += f"        {prop_name}: {value}\n"
    return block


def promote_shield(
    name: str,
    revision: str | None = None,
    socket: str | None = None,
    sockets: dict[str, str] | None = None,
    config: dict[str, str] | None = None,
    params: dict[str, dict[str, str]] | None = None,
) -> PromotedRig:
    """The natural mapping `a -> [a]`, written out: a rig.yml with NO
    `board:` (a promoted rig's board reaches it only by INJECTION;
    rig.yml has no `board:` key at all any more, promoted or persisted)
    and a content file with exactly one instance, socket-LESS BY
    DEFAULT (the unique-by-type inference resolves it board-agnostically
    at analysis time, once a board is actually in play).

    `socket`, when given, emits `socket: <label>` on that instance and
    inference never runs for it -- the single-plug spelling, BYTE-
    UNTOUCHED by the slot form below. This is what makes a shield
    promotable onto a board carrying MORE THAN ONE socket of its type,
    where inference is right to refuse: four mikrobus shields
    (eth_click, flash_click, temp_click, temp_hum_click) cannot be
    promoted onto mikroe_quail without it, because quail offers four
    mikrobus sockets and the desugared instance names none of them.

    `sockets`, when given (slot name -> board socket label, the identical
    shape `ParsedPromotionOpts.sockets`/`Instance.sockets` both carry,
    minus the unassigned slots -- those stay OMITTED, per `Instance.
    sockets`'s own "missing slot -> None, left to inference" contract),
    prints a `sockets:` block instead, one entry per GIVEN slot, in the
    same shape a persisted plural instance's own `sockets:` map already
    uses -- the plural counterpart of `socket`, and mutually exclusive
    with it by construction (a caller threading `ParsedPromotionOpts`
    populates at most one of the two, since `parse_promotion_opts` itself
    refuses a bare `socket=` on a plural shield and a `socket.<slot>=` on
    a single-plug one). This function does not itself enforce the
    exclusion -- it is a pure printer, and validating its own arguments'
    mutual consistency would be a second authority for a rule
    `parse_promotion_opts` already owns; a caller passing both gets
    `sockets:` printed and `socket` silently ignored.

    Neither `socket` nor a `sockets` entry is checked to exist on any
    board; that is the analyzer's job, and it already renders the
    candidates (error[phys-socket]). The label(s) are BOARD-SPECIFIC
    (`quail_sock1`, not `mikrobus`), which is correct: board-specific
    labels stay out of CONTENT, which must stay portable. An invocation
    already names the board -- it is the one place a board-specific
    label belongs.

    The instance is named after THE SHIELD ITSELF, never a placeholder
    like "inst": instance names reach config-sheet.md (emitter/
    sheet.py:48), so a checked-in rig this desugaring is ever compared
    against (the singleton identity law) must use the identical name.

    `revision`, when given, desugars to `shield: <name>@<revision>` --
    the SHIELD's own revision axis; rig.yml is unaffected, since a
    promoted rig has no revision axis of its own to declare. This
    function never checks whether `revision` is actually declared by the
    shield -- that validation belongs to `rigc.loader.load`, the one
    place a shield's `revisions:` axis is already read; duplicating it
    here would be a second authority for the same fact.

    `config`, when given (config-element LABEL -> value, the identical
    shape `ParsedPromotionOpts.config` carries -- a strap/routing-jumper
    assignment, resolved by DTS LABEL, not node name), prints one
    `config:` block onto the same instance,
    positioned after `socket:`/`sockets:` and before `params:` (`_render_
    instance`'s own fixed print order), in the SAME shape a checked-in
    rig.yml's own `config:` block already uses (4-space `config:`,
    6-space `<label>: <value>`) -- exactly `nucleo_wifi_logger_ok.yml`'s
    own spelling, value a position NAME like `D2`, never an index. This
    function performs NO validation of its own against the shield's real
    config elements -- that stays `rigc.loader.params.apply_config_block`'s
    job, the one place a miss already renders the valid labels; a second
    check here would be a second authority for the same fact. An empty
    or absent mapping omits the block entirely.

    `params`, when given (device label -> property name -> value, the
    identical shape `ParsedPromotionOpts.params`/`Instance.params` both
    carry), prints one `params:` block onto the same instance, in the
    SAME shape any authored rig.yml already uses (4-space `params:`,
    6-space device label, 8-space `<prop>: <value>`). This function
    performs NO validation of its own against device or property
    existence, declared-parameter membership, or token resolution --
    the printed text flows through the identical `rigc.loader.load`
    path every promoted document already goes through (`PromotedRig`'s
    own contract, above), which is the one place those facts are
    already checked; a second check here would be a second authority
    for facts the loader already owns. An empty or absent mapping omits
    the block entirely, matching params-less promotion exactly as
    before.

    Pure over its arguments: no filesystem, no promotability or
    namespace decision (the caller's job, via `check_promotable`,
    before this ever runs). Returns a PromotedRig the caller owns."""
    rig_yml = f"rig:\n  name: {name}\n"
    content = "instances:\n" + _render_instance(
        name, revision, socket=socket, sockets=sockets, config=config, params=params
    )
    return PromotedRig(rig_yml=rig_yml, content_name=f"{name}.yml", content=content)


def promote_shield_list(
    elements: list[tuple[str, str | None, ParsedPromotionOpts]],
) -> PromotedRig:
    """The list generalization of `promote_shield`'s `a -> [a]` mapping:
    N `(name, revision, parsed opts)` triples -- one per `;`-separated
    target element, already resolved and validated by the caller (every
    element a real, promotable shield; no duplicate name; never a
    persisted rig -- `list_rigs.py`'s and `west_commands/rigs.py`'s own
    namespace resolution, this function trusts entirely and re-checks
    nothing) -- desugar to ONE synthetic rig carrying N instances, one
    per element, in the given order.

    Each instance is rendered by the IDENTICAL `_render_instance` helper
    `promote_shield` itself uses, so a single-element list is byte-
    identical to a bare `promote_shield` call by construction rather
    than by two string builders kept in sync by hand.

    The desugared rig's own NAME -- the string that reaches artifacts
    and RIG_* provenance -- is every element's shield name joined with
    `+`: deterministic, and filename-/cmake-safe since
    a shield name is itself restricted to that same safe character set.
    The content file's name follows `PromotedRig`'s own convention
    (`<rig-name>.yml`), exactly as `promote_shield` already does for one
    name.

    Pure: no filesystem, no duplicate/namespace validation of its own.
    Returns a PromotedRig the caller owns."""
    rig_name = "+".join(name for name, _revision, _opts in elements)
    content = "instances:\n" + "".join(
        _render_instance(
            name,
            revision,
            socket=opts.fixed.get("socket"),
            sockets=opts.sockets or None,
            config=opts.config or None,
            params=opts.params or None,
        )
        for name, revision, opts in elements
    )
    return PromotedRig(
        rig_yml=f"rig:\n  name: {rig_name}\n", content_name=f"{rig_name}.yml", content=content
    )


def shield_is_multiplug(shield: Shield) -> bool:
    """Whether `shield` declares more than one plug. A plural shield
    promotes per slot, not through a single `:socket=`; the caller is
    `parse_promotion_opts`, which needs exactly this fact to decide
    whether a bare `socket=` or a `socket.<slot>=` is the shield's legal
    spelling. Pure: `shield` is read-only."""
    return len(shield.plugs) > 1


def resolve_for_promotion(
    name: str,
    shield_dirs: list[str] | None = None,
    types: dict[str, ConnectorType] | None = None,
    include_dirs: list[str] | None = None,
) -> Shield | None:
    """Resolve `name`'s own template -- the IO edge a promotion caller
    reaches for when it needs a fact `discover_shields`'s cheap scan does
    not carry (its real slot names, for `parse_promotion_opts`'s
    slot-validation grammar and `promote_shield`'s own `sockets:` map): a
    SEPARATE, small parse from `discover_shields`'s own scan, on purpose,
    since that scan is deliberately lazy (module docstring, `loader/
    library.py`) and answering "what are this shield's slots" needs the
    template's actual plug nodes.

    Returns the resolved Shield, or None when resolution fails for any
    reason (an unknown name, a malformed template) -- the caller's own
    subsequent `promote_shield`/`loader.load` call is what surfaces the
    real diagnostic; this function exists only to answer the slot
    question cheaply and is not itself a diagnostic source. The caller
    owns the returned Shield.

    `types` is threaded to the scan exactly as in `discover_shields`: None
    takes `registry.load_types()`'s module-relative default, which only
    resolves inside this module's own repository. `include_dirs` is the cpp
    `-I` list the template's own `#include <dt-bindings/connector/...>`
    resolves against -- this function actually preprocesses, so omitting it
    does not fall back quietly, it fails cpp with a missing header.

    Unlike `discover_shields`'s own inert placeholder workdir, this
    function actually PARSES the template (cpp + dtlib), so it needs a
    real scratch directory -- a fresh `TemporaryDirectory`, removed
    before this returns, so no workdir is left behind for a query."""
    with tempfile.TemporaryDirectory(prefix="rigc-promote-plug-count-") as workdir:
        lib, _diags, _deps = load_shield_library(
            workdir, shield_dirs, types=types, include_dirs=include_dirs
        )
        shield, _diags2, _deps2 = lib.resolve(
            name, "promotion slot probe", SourceRef("<promote>", 0)
        )
        return shield


def check_promotable(name: str, info: ShieldInfo, variant: str | None) -> str | None:
    """Whether `name` -- already known to `discover_shields` (`info` is
    its own entry, read-only to this call) -- may be promoted at all, in
    the order a user's own target string is checked: a `/variant` names
    an axis a promoted shield does not have (`@rev` is the shield's own
    revision, and that is the only axis a promoted shield has to select
    from), then `template: true`, naming whichever of the two ways a
    shield falls short of it -- missing shield.yml entirely, or one that
    omits the flag. A plural shield (more than one plug) promotes per
    slot (`socket.<slot>=<label>`) rather than being refused outright --
    `parse_promotion_opts` is where that grammar's own refusals live
    (bare `socket=` on a plural shield, `socket.<slot>=` on a
    single-plug one, an unknown slot), not here.

    Returns an error message naming why promotion is refused, or None
    when `promote_shield` may run. Pure: makes no filesystem call of its
    own."""
    if variant is not None:
        return (
            f"'{name}/{variant}': a promoted shield has no variant "
            "axis to select from -- '@rev' is the only axis it "
            "promotes with, and it selects the SHIELD's own "
            "revision, never a rig variant"
        )
    if not info.template:
        missing = (
            "no shield.yml" if not info.has_yml else "shield.yml does not declare 'template: true'"
        )
        return f"shield '{name}' is discoverable but not promotable to a rig -- {missing}"
    return None


def shield_declares_required_params(shield: Shield) -> bool:
    """Whether ANY device of `shield` declares a `shield,params` name with
    no authored default -- `params.device_required_params` applied across
    every device, never re-derived a second time (a second hand-rolled
    copy of "declared, no default" is a review finding). This is the
    singleton-law census's own eligibility predicate: a shield this
    returns True for can never be promoted, because a promoted rig's
    content file has no `params:` slot to satisfy
    `params.check_param_invariant` with -- `check_promotable` does not
    itself gate on this (it only gates on `template:`/`@variant`), so a
    caller building the LAW's own domain applies this separately, over
    an already-resolved
    Shield (not a bare name -- resolving one needs the shield library's
    own lazy parse, `ShieldLibrary.resolve`, which this module's `promote_
    shield` deliberately never touches).

    Pure: makes no filesystem call of its own; shield is read-only."""
    return any(device_required_params(dev) for dev in shield.devices)


def both_paths_error(name: str, rig_dir: Path, shield_dir: str) -> str:
    """The namespace rule's third branch, spelled out: `name` matches
    BOTH a persisted rig folder and a discovered shield -- ruled an
    error rather than a guess, the same tie-break discipline the socket
    inference already refuses to make between two equally plausible
    candidates.

    BOTH paths are real, DISCOVERED ones, never constructed from `name`:
    `rig_dir` is list_rigs.find_rigs's own Rig.dir and `shield_dir` is
    ShieldInfo.dir, straight off library.py's scan. A message that told
    the user to go look at a path nobody had actually found would be
    wrong for any shield outside the vendored library -- exactly the
    cross-module case that makes a name collide in the first place.

    Pure: builds a message from its three arguments alone."""
    return (
        f"'{name}' names both a rig ({rig_dir}) and a shield "
        f"({shield_dir}) -- rename one; a name that is both "
        "is ambiguous by construction, never guessed between"
    )


def list_element_is_a_rig_error(name: str, target: str, rig_dir: str | Path) -> str:
    """The list-promotion grammar's own "every element must be a SHIELD"
    ruling, spelled out for the specific element `name` of the
    `;`-separated `target` that names a persisted
    rig with no colliding same-named shield (a collision is `both_paths_
    error`'s own branch instead, checked by the caller BEFORE this one --
    a rig is already a container, and a list mixing containers with
    elements has no coherent desugaring, so an element naming one is
    refused regardless of whether that name is ALSO a shield).

    `rig_dir` is the DISCOVERED rig folder (`list_rigs.find_rigs`'s own
    `Rig.dir`), never reconstructed from `name`, mirroring `both_paths_
    error`'s own discipline of naming only paths a caller actually found.

    Pure: builds a message from its three arguments alone."""
    return (
        f"'{target}': list element '{name}' names a persisted rig "
        f"({rig_dir}), not a shield -- every element of a list "
        f"promotion target must be a shield; a rig is already a "
        f"container, and a list mixing containers with elements has "
        f"no coherent desugaring"
    )


def list_element_not_a_shield_error(name: str, target: str) -> str:
    """The list-promotion grammar's refusal for an element that names
    NEITHER a persisted rig nor a discoverable shield (a plain unknown
    name, or a typo) -- the residual case `list_element_is_a_rig_error`/
    `both_paths_error` do not cover, still needing its own sentence
    naming the offending element and the whole target it came from
    rather than falling through to a generic "target does not resolve"
    message that never mentions WHICH element was the problem.

    Pure: builds a message from its two arguments alone."""
    return f"'{target}': list element '{name}' does not name a discoverable shield"


def check_list_no_duplicate_elements(names: list[str], target: str) -> str | None:
    """`[a, a]` is REFUSED, not desugared -- a repeated shield name has no
    instance-naming rule yet (instance name = shield name is the
    singleton desugaring's own fixed convention, and two instances
    cannot share one name), so a list naming the same shield twice is a
    loud error rather than a silent last-wins or an invented suffix.

    Needs no namespace/discovery information at all -- a duplicate is a
    property of the target STRING alone, checkable the moment every
    element's bare name is known, which is why every caller (`list_rigs.
    py`'s cmake seam, `west_commands/rigs.py`'s `--explain`/
    `--boards-for`, `cli.py`'s own `--promote`) can run this identically
    over its own already-split element names.

    Returns an error message naming the FIRST name seen more than once,
    or None when every name in `names` is unique. Pure: makes no
    filesystem call of its own."""
    seen = set()
    for name in names:
        if name in seen:
            return (
                f"'{target}': shield '{name}' is named more than "
                f"once in this list -- list promotion needs one "
                f"instance per element (indexed naming for a "
                f"repeated shield is future work)"
            )
        seen.add(name)
    return None


#: One element of a `;`-split `--promote` LIST value:
#: `<shield>[@rev][:opts]`, no `/variant` (every element must
#: be a shield, which has no variant axis to select -- list_rigs.py's/
#: west_commands/rigs.py's own namespace resolution already refused one
#: before this ever runs, `check_promotable`'s own gate). Package-local
#: rather than importing `list_rigs.py`'s own `_RIG_TARGET_RE`: that
#: module is a standalone script outside this package, already importing
#: `rigc.promote` the other way, so importing it back here would cycle.
_LIST_ELEMENT_RE = re.compile(r"^([^@:]+)(@[^@:]+)?(:(.+))?$")


def _split_list_element(element: str) -> tuple[str, str | None, str | None]:
    """Parse one list-promotion element into (name, revision, opt_text).
    A malformed element (the regex fails to match at all -- practically
    unreachable via the west/cmake front doors, which already validated
    every element before ever forwarding this value, but cli.py's
    --promote is also directly invocable on its own) falls back to
    treating the WHOLE text as the name: `resolve_for_promotion`'s own
    failure to resolve it, surfaced once the synthesized `shield:`
    reference reaches the loader, is what a caller sees -- the same
    "trust the upstream namespace validation" boundary `parse_promotion_
    opts`'s own single-target grammar already keeps."""
    m = _LIST_ELEMENT_RE.match(element)
    if not m:
        return element, None, None
    name = m.group(1)
    revision = m.group(2)[1:] if m.group(2) else None
    opt_text = m.group(4)
    return name, revision, opt_text


def parse_promotion_list(
    target: str,
    shield_dirs: list[str] | None = None,
    types: dict[str, ConnectorType] | None = None,
    include_dirs: list[str] | None = None,
) -> list[tuple[str, str | None, ParsedPromotionOpts]] | str:
    """Parse a `;`-separated `--promote` LIST target into one (name,
    revision, parsed opts) triple per element, in the given order.

    A list target carries EACH element's own `@rev` inline (unlike a
    single `--promote` target's `--revision` flag): there is no single
    scalar flag that could carry N separate per-element revisions, so a
    list target is never revision-stripped the way a single target is
    (list_rigs.PromotedListTarget's own docstring). `check_promotable`/
    the rig-in-a-list/duplicate refusals are deliberately NOT re-checked
    here, mirroring `parse_promotion_opts`'s own single-target "trust
    the upstream namespace validation" boundary -- list_rigs.py/
    west_commands/rigs.py already ran them before ever forwarding a
    target this far.

    Returns the parsed elements in order, or an ERROR MESSAGE string
    (the same return convention every other refusal in this module
    uses) naming the first element that failed to parse or the first
    duplicate name. shield_dirs is read-only; the returned list and its
    elements are the caller's own."""
    elements: list[tuple[str, str | None, ParsedPromotionOpts]] = []
    for element in target.split(";"):
        shield_name, elem_revision, opt_text = _split_list_element(element)
        resolved = resolve_for_promotion(shield_name, shield_dirs, types, include_dirs)
        opts = parse_promotion_opts(opt_text, element, resolved)
        if isinstance(opts, str):
            return opts
        elements.append((shield_name, elem_revision, opts))
    dup_err = check_list_no_duplicate_elements([name for name, _rev, _opts in elements], target)
    if dup_err is not None:
        return dup_err
    return elements
