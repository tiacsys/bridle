# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Base topology parsing and the delta engine: instances, wires, and
the four delta operations (`instances:`, `add-instances:`,
`remove-instances:`, `add-wires:`/`remove-wires:`), all matched against
an in-memory EFFECTIVE topology. Diagnostic code is lang-variant or
lang-rev by STAGE.

`shield:` references resolve against a REAL `ShieldLibrary`
(`loader/library.py`), and `params:`/`config:` are fully applied
(`loader/params.py`). Wire endpoints are checked for label existence
and ambiguity (`resolve_dotted`, via `Shield.by_name`).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from ..deps import Deps, union
from ..diag import Diagnostic, error
from ..model import Instance, Shield, Wire, WireEnd
from .binding import SocketBinding
from .documents import Val, as_mapping, require
from .library import ShieldLibrary
from .params import apply_config_block, apply_params_block, check_restate

log = logging.getLogger(__name__)


@dataclass
class Topology:
    """The rig's EFFECTIVE topology as the delta engine sees it: instances
    keyed by NAME, ORDER preserved separately, the wire list, and which
    STAGE VALUE last removed each now-absent instance name (removed_by --
    the drift-cannot-hide hint: a later stage naming an already-removed
    instance gets told which stage removed it, instead of a bare
    "does not exist").

    `apply_delta` returns a NEW Topology rather than mutating this one in
    place: diagnostics stay the only thing composed as a side value,
    never a mutable accumulator -- and the same discipline extends
    naturally to the value the diagnostics accompany."""

    effective: dict[str, Instance] = field(default_factory=dict)
    order: list[str] = field(default_factory=list)
    wires: list[Wire] = field(default_factory=list)
    removed_by: dict[str, str] = field(default_factory=dict)

    def instances(self) -> list[Instance]:
        return [self.effective[n] for n in self.order if n in self.effective]


def _build_plural_sockets_map(
    sockets_v: Val | None,
    shield: Shield,
    binding: SocketBinding,
    inst_name: str,
) -> tuple[dict[str, str | None], list[Diagnostic]]:
    """`sockets:`'s slot -> reference map (the plural shape): one entry
    per slot of `shield.plugs`, each resolved through `binding.get`. An
    unknown slot name is a loud error listing the shield's real slots;
    an omitted slot carries None, left to per-slot inference.

    Returns (sockets, diagnostics); sockets is a fresh dict the caller
    owns."""
    diags: list[Diagnostic] = []
    raw: dict[str, str] = {}
    if sockets_v is not None and isinstance(sockets_v.value, dict):
        for slot_name, slot_v in sockets_v.value.items():
            if slot_name not in shield.plugs:
                diags.append(
                    error(
                        "lang-instance-socket",
                        f"instance '{inst_name}': sockets: names unknown "
                        f"slot '{slot_name}' of shield '{shield.name}'\n"
                        f"slots: {', '.join(shield.plugs)}",
                        (slot_v.src,),
                    )
                )
                continue
            raw[slot_name] = slot_v.value
    return ({slot: binding.get(raw[slot]) if slot in raw else None for slot in shield.plugs}, diags)


def _parse_sockets_block(
    item: Val, shield: Shield, binding: SocketBinding, inst_name: str
) -> tuple[dict[str, str | None], list[Diagnostic]]:
    """`socket:`/`sockets:` -> `Instance.sockets`: a single-plug shield
    takes `socket:` (one entry keyed by the shield's own one slot name,
    `next(iter(shield.plugs))`, never the literal `"plug"`); a plural
    shield takes `sockets:`, a slot name -> reference MAPPING, each value
    resolved through `binding.get` exactly like `socket:` does. The two
    keys are mutually exclusive, and each is legal only for the matching
    shield SHAPE -- enforced here in rigc's own parser rather than
    deferred to a schema. An unknown slot name is a loud error listing
    the shield's real slots.
    Omitted slots (plural) or an omitted `socket:` (single) carry None --
    unresolved, left to per-slot inference.

    Returns (sockets, diagnostics): `sockets` always has exactly one
    entry per slot of `shield.plugs` (`Instance.sockets`'s own contract),
    a fresh dict the caller owns."""
    socket_v = item.value.get("socket")
    sockets_v = item.value.get("sockets")
    plural = len(shield.plugs) > 1

    if socket_v is not None and sockets_v is not None:
        return (
            {slot: None for slot in shield.plugs},
            [
                error(
                    "lang-instance-socket",
                    f"instance '{inst_name}': declares both socket: and sockets: "
                    "-- mutually exclusive (socket: is the single-plug spelling, "
                    "sockets: the plural one)",
                    (item.src,),
                )
            ],
        )

    diags: list[Diagnostic] = []
    if socket_v is not None and plural:
        diags.append(
            error(
                "lang-instance-socket",
                f"instance '{inst_name}': shield '{shield.name}' plugs "
                f"{len(shield.plugs)} sockets -- use sockets: (a slot -> "
                "socket map), not socket:",
                (socket_v.src,),
            )
        )
    if sockets_v is not None and not plural:
        diags.append(
            error(
                "lang-instance-socket",
                f"instance '{inst_name}': shield '{shield.name}' has a single "
                "plug -- use socket:, not sockets:",
                (sockets_v.src,),
            )
        )

    if plural:
        sockets_map, plural_diags = _build_plural_sockets_map(sockets_v, shield, binding, inst_name)
        diags += plural_diags
        return sockets_map, diags

    # Keyed by the plug's own name (model.py's FunctionRef.plug/Shield.plugs
    # contract), never the literal "plug": a single-plug shield's one
    # slot is whatever its plug node is actually named. `shield.plugs`
    # is empty only when an earlier loader/shields.py diagnostic already
    # rejected this shield (no plug node, or a retired shield,plugs
    # spelling) -- cli.py's has_errors gate stops the run before this
    # map is ever read, so an empty dict here (one entry per slot of
    # shield.plugs, same as every other branch) keeps the contract
    # rather than inventing a slot that does not exist.
    if not shield.plugs:
        return {}, diags
    value = socket_v.value if socket_v is not None else None
    slot = next(iter(shield.plugs))
    return {slot: binding.get(value) if value is not None else None}, diags


def parse_instance(
    item: Val,
    binding: SocketBinding,
    lib: ShieldLibrary,
    rig_name: str,
    workdir: str,
    include_dirs: list[str] | None = None,
) -> tuple[Instance | None, list[Diagnostic], Deps]:
    """One `instances:` entry (base content, or an `add-instances:` item
    -- the identical shape): name/shield required, socket OPTIONAL --
    omitting it carries `None` through to `Instance.socket` unresolved,
    since this loader never sees the board and cannot be the one to
    infer a physical socket; the analyzer resolves it later, alongside
    the existing mating check. `shield:` resolves against the REAL
    library (`lib.resolve`). A DECLARED `socket:` still applies through
    the binding; `config:`/`params:` apply fully against the resolved
    shield.

    Returns (instance, diagnostics, deps); instance is None when a
    required key is missing or the shield reference did not resolve.
    The caller owns the new Instance."""
    name_v, diags = require(item, "name", "instance")
    shield_v, d = require(item, "shield", "instance")
    diags += d
    if name_v is None or shield_v is None:
        return None, diags, frozenset()
    name = str(name_v.value)
    shield, d, deps = lib.resolve(shield_v.value, f"instance '{name}'", shield_v.src)
    diags += d
    if shield is None:
        return None, diags, deps
    sockets_map, d = _parse_sockets_block(item, shield, binding, name)
    diags += d

    inv_v = item.value.get("invert")
    straps, strap_refs, jumpers, jumper_refs, d = apply_config_block(
        item.value.get("config"), name, shield
    )
    diags += d
    tag = f"{rig_name}_{name}"
    params, param_refs, d, pdeps = apply_params_block(
        item.value.get("params"), name, shield, workdir, tag, include_dirs=include_dirs
    )
    diags += d
    deps = union(deps, pdeps)

    inst = Instance(
        name=name,
        shield=shield,
        sockets=sockets_map,
        invert=bool(inv_v.value) if inv_v is not None else False,
        straps=straps,
        strap_refs=strap_refs,
        jumpers=jumpers,
        jumper_refs=jumper_refs,
        params=params,
        param_refs=param_refs,
        src=item.src,
    )
    log.debug("instance '%s': shield=%r sockets=%r", name, shield.name, inst.sockets)
    return inst, diags, deps


def _apply_instance_patch(
    item: Val,
    inst: Instance,
    binding: SocketBinding,
    lib: ShieldLibrary,
    stage: str,
    stage_value: str,
    variant: str | None,
    rig_name: str,
    workdir: str,
    include_dirs: list[str] | None = None,
) -> tuple[Instance, list[Diagnostic], Deps]:
    """Shallow-replace an EXISTING instance's top-level keys: a GIVEN key
    REPLACES; an unspecified key INHERITS. shield/socket/invert/config/params
    are each the deepest merge unit -- no key merges into what was there
    before, it wholesale replaces it. When shield changes, the OLD params
    are keyed to the OLD shield's devices and are therefore meaningless
    against the new one, so they are dropped rather than carried forward.
    The OLD sockets map is carried forward the same way UNLESS the new
    shield's slot-name set differs from it, in which case it is reset the
    same way params are (see the sockets_map assignment below).

    Returns a NEW Instance (never mutates the one it was handed), always
    preserving the ORIGINAL `src` -- so a diagnostic raised many delta
    stages later still anchors at the base instance's own declaration."""
    diags: list[Diagnostic] = []
    deps: Deps = frozenset()
    shield = inst.shield
    shield_changed = False
    if "shield" in item.value:
        shield_v = item.value["shield"]
        new_shield, d, deps = lib.resolve(shield_v.value, f"instance '{inst.name}'", shield_v.src)
        diags += d
        if new_shield is None:
            return inst, diags, deps
        shield = new_shield
        shield_changed = True

    # `socket:`/`sockets:` REPLACES WHOLESALE, same as `params:` -- never
    # a per-key merge. Absent from this patch item, the OLD sockets
    # carry forward untouched, even across a shield change -- the same
    # "unspecified key inherits" shape straps/jumpers already use
    # (reproduced as-is above), rather than an implicit reset. EXCEPT:
    # when the shield changed to one
    # whose slot names differ from the carried-forward map's keys, the
    # old map is meaningless against the new shield (same reasoning as
    # the params reset below) -- reset it to unresolved-per-slot rather
    # than let stale keys silently fall back to per-slot inference with
    # no diagnostic.
    sockets_map = inst.sockets
    if shield_changed and set(sockets_map) != set(shield.plugs):
        sockets_map = {slot: None for slot in shield.plugs}
    if "socket" in item.value or "sockets" in item.value:
        sockets_map, d = _parse_sockets_block(item, shield, binding, inst.name)
        diags += d

    invert = inst.invert
    if "invert" in item.value:
        invert = bool(item.value["invert"].value)

    # A shield swap with no `config:` key alongside it leaves
    # straps/jumpers referencing the OLD shield's config elements
    # untouched -- only params: is unconditionally reset on a shield
    # change. This asymmetry is deliberate; changing it is a
    # golden-changing decision, not something to fix in passing.
    straps, strap_refs, jumpers, jumper_refs = (
        inst.straps,
        inst.strap_refs,
        inst.jumpers,
        inst.jumper_refs,
    )
    if "config" in item.value:
        straps, strap_refs, jumpers, jumper_refs, d = apply_config_block(
            item.value["config"], inst.name, shield
        )
        diags += d

    params, param_refs = inst.params, inst.param_refs
    if shield_changed:
        params, param_refs = {}, {}
    if "params" in item.value:
        params_v = item.value["params"]
        if not shield_changed:
            diags += check_restate(params_v, inst.params, inst.name)
        # A family-wide revision's params landing on a device the
        # POST-VARIANT shield lacks needs the variant named, since the
        # revision stage alone can't otherwise explain why that device
        # is gone.
        context = None
        if stage == "revision" and variant is not None:
            context = f"this instance's shield is '{shield.name}' because of variant '{variant}'"
        tag = f"{rig_name}_{inst.name}"
        params, param_refs, d, pdeps = apply_params_block(
            params_v,
            inst.name,
            shield,
            workdir,
            tag,
            unknown_device_context=context,
            include_dirs=include_dirs,
        )
        diags += d
        deps = union(deps, pdeps)

    new_inst = Instance(
        name=inst.name,
        shield=shield,
        sockets=sockets_map,
        invert=invert,
        straps=straps,
        strap_refs=strap_refs,
        jumpers=jumpers,
        jumper_refs=jumper_refs,
        params=params,
        param_refs=param_refs,
        src=inst.src,
    )
    log.debug(
        "instance '%s': shield=%r sockets=%r (%s stage '%s')",
        inst.name,
        shield.name,
        sockets_map,
        stage,
        stage_value,
    )
    return new_inst, diags, deps


def resolve_dotted(
    ref_v: Val | None, by_name: dict[str, Instance], key: str
) -> tuple[WireEnd | None, list[Diagnostic]]:
    """`<instance>.<node>` -- validates dotted FORM, instance EXISTENCE
    in the effective topology, and node existence/ambiguity WITHIN that
    instance's own resolved shield, via `Shield.by_name`.

    Returns (end, diagnostics); end is None on every rejection shape."""
    if ref_v is None:
        return None, [error("lang-schema", f"wire: required key '{key}' is missing", ())]
    ref = ref_v.value
    if not isinstance(ref, str) or "." not in ref:
        return None, [
            error(
                "lang-wire-ref",
                f"wire {key}: '{ref}' is not an <instance>.<node> reference",
                (ref_v.src,),
            )
        ]
    inst_name, _, node_name = ref.partition(".")
    inst = by_name.get(inst_name)
    if inst is None:
        return None, [
            error(
                "lang-wire-ref",
                f"wire {key}: '{ref}' — no instance named '{inst_name}' in "
                f"this rig\ninstances: {', '.join(sorted(by_name))}",
                (ref_v.src,),
            )
        ]
    hits = inst.shield.by_name(node_name)
    if not hits:
        return None, [
            error(
                "lang-wire-ref",
                f"wire {key}: '{ref}' — shield '{inst.shield.name}' has no "
                f"node '{node_name}'\nreferencable nodes of "
                f"'{inst.shield.name}': {', '.join(inst.shield.names())}",
                (ref_v.src,),
            )
        ]
    if len(hits) > 1:
        return None, [
            error(
                "lang-wire-ref",
                f"wire {key}: '{ref}' is ambiguous within shield "
                f"'{inst.shield.name}' ({len(hits)} matches)",
                (ref_v.src,),
            )
        ]
    return WireEnd(instance_name=inst_name, node=node_name, src=ref_v.src), []


def parse_wire(
    item: Val,
    by_name: dict[str, Instance],
) -> tuple[Wire | None, list[Diagnostic]]:
    """One wires: entry -- both endpoints resolved (resolve_dotted),
    route shape validated (a mapping route must name via:).

    Returns (wire, diagnostics); wire is None when an endpoint or the
    route was rejected. The caller owns the new Wire."""
    frm, diags = resolve_dotted(item.value.get("from"), by_name, "from")
    to, d = resolve_dotted(item.value.get("to"), by_name, "to")
    diags += d
    route_v = item.value.get("route")
    if frm is None or to is None or route_v is None:
        if route_v is None:
            diags.append(error("lang-schema", "wire: required key 'route' is missing", (item.src,)))
        return None, diags
    if isinstance(route_v.value, dict):
        via_v = route_v.value.get("via")
        if via_v is None:
            diags.append(
                error(
                    "lang-schema", "wire: route is a mapping but names no 'via' key", (route_v.src,)
                )
            )
            return None, diags
        route = via_v.value
    else:
        route = route_v.value
    return Wire(frm=frm, to=to, route=route, src=item.src), diags


def find_wire(wires: list[Wire], frm: str | None, to: str | None) -> Wire | None:
    """Match `remove-wires:` by RAW endpoint pair (`<instance>.<node>`
    strings on both sides) -- a wire carries no identity beyond its
    endpoints, so this is the only stable way to find one to remove.
    Needs no shield data at all.

    Returns the first wire whose raw endpoint pair matches, else None;
    wires is read-only."""
    if frm is None or to is None:
        return None
    for w in wires:
        if (
            f"{w.frm.instance_name}.{w.frm.node}" == frm
            and f"{w.to.instance_name}.{w.to.node}" == to
        ):
            return w
    return None


def _apply_instances_key(
    doc: dict[str, Val],
    code: str,
    stage: str,
    stage_value: str,
    effective: dict[str, Instance],
    binding: SocketBinding,
    lib: ShieldLibrary,
    variant: str | None,
    rig_name: str,
    workdir: str,
    include_dirs: list[str] | None,
) -> tuple[list[Diagnostic], Deps]:
    """`instances:` -- matched by name against the EFFECTIVE topology; a
    non-match is always an error (additions are never implicit, that is
    what add-instances: is for).

    Returns (diagnostics, deps); mutates `effective` in place."""
    diags: list[Diagnostic] = []
    deps: Deps = frozenset()
    instances_v = doc.get("instances")
    if instances_v is None:
        return diags, deps
    for item in instances_v.value:
        name_v, d = require(item, "name", f"{stage} instances:")
        diags += d
        if name_v is None:
            continue
        name = name_v.value
        inst = effective.get(name)
        if inst is None:
            diags.append(
                error(
                    code,
                    f"{stage} '{stage_value}': instances: names '{name}', "
                    "which the effective topology does not have",
                    (item.src,),
                )
            )
            continue
        new_inst, d, idep = _apply_instance_patch(
            item, inst, binding, lib, stage, stage_value, variant, rig_name, workdir, include_dirs
        )
        diags += d
        deps = union(deps, idep)
        effective[name] = new_inst
    return diags, deps


def _apply_add_instances_key(
    doc: dict[str, Val],
    code: str,
    stage: str,
    stage_value: str,
    effective: dict[str, Instance],
    order: list[str],
    binding: SocketBinding,
    lib: ShieldLibrary,
    rig_name: str,
    workdir: str,
    include_dirs: list[str] | None,
) -> tuple[list[Diagnostic], Deps]:
    """`add-instances:` -- full declarations; the name must NOT already
    exist.

    Returns (diagnostics, deps); mutates `effective` and `order` in
    place."""
    diags: list[Diagnostic] = []
    deps: Deps = frozenset()
    add_v = doc.get("add-instances")
    if add_v is None:
        return diags, deps
    for item in add_v.value:
        added_inst, d, idep = parse_instance(item, binding, lib, rig_name, workdir, include_dirs)
        diags += d
        deps = union(deps, idep)
        if added_inst is None:
            continue
        if added_inst.name in effective:
            diags.append(
                error(
                    code,
                    f"{stage} '{stage_value}': add-instances: names "
                    f"'{added_inst.name}', which already exists",
                    (item.src,),
                )
            )
            continue
        effective[added_inst.name] = added_inst
        order.append(added_inst.name)
    return diags, deps


def _apply_remove_instances_key(
    doc: dict[str, Val],
    code: str,
    stage: str,
    stage_value: str,
    effective: dict[str, Instance],
    removed_by: dict[str, str],
) -> list[Diagnostic]:
    """`remove-instances:` -- names must exist; if a prior stage already
    removed it, the message NAMES that stage so drift cannot hide.

    Returns diagnostics; mutates `effective` and `removed_by` in place."""
    diags: list[Diagnostic] = []
    remove_v = doc.get("remove-instances")
    if remove_v is None:
        return diags
    for name_v in remove_v.value:
        name = name_v.value
        if name not in effective:
            prior = removed_by.get(name)
            hint = f" (variant '{prior}' already removed it)" if prior else ""
            diags.append(
                error(
                    code,
                    f"{stage} '{stage_value}': remove-instances: names "
                    f"'{name}', which does not exist{hint}",
                    (name_v.src,),
                )
            )
            continue
        del effective[name]
        removed_by[name] = stage_value
    return diags


def _apply_remove_wires_key(
    doc: dict[str, Val],
    code: str,
    stage: str,
    stage_value: str,
    wires: list[Wire],
) -> list[Diagnostic]:
    """`remove-wires:` -- matched by endpoint pair; a re-route is
    remove+add, there is no wire "replace".

    Returns diagnostics; mutates `wires` in place."""
    diags: list[Diagnostic] = []
    remove_wires_v = doc.get("remove-wires")
    if remove_wires_v is None:
        return diags
    for item in remove_wires_v.value:
        frm_v = item.value.get("from")
        to_v = item.value.get("to")
        frm = frm_v.value if frm_v is not None else None
        to = to_v.value if to_v is not None else None
        match = find_wire(wires, frm, to)
        if match is None:
            diags.append(
                error(
                    code,
                    f"{stage} '{stage_value}': remove-wires: names "
                    f"{{from: {frm}, to: {to}}}, which does not exist",
                    (item.src,),
                )
            )
            continue
        wires.remove(match)
    return diags


def _apply_add_wires_key(
    doc: dict[str, Val], effective: dict[str, Instance], wires: list[Wire]
) -> list[Diagnostic]:
    """`add-wires:` -- resolved the same way a base `wires:` entry is.

    Returns diagnostics; mutates `wires` in place; `effective` is
    read-only."""
    diags: list[Diagnostic] = []
    add_wires_v = doc.get("add-wires")
    if add_wires_v is None:
        return diags
    for item in add_wires_v.value:
        wire, d = parse_wire(item, effective)
        diags += d
        if wire is not None:
            wires.append(wire)
    return diags


def apply_delta(
    delta: Val,
    stage: str,
    stage_value: str,
    topology: Topology,
    binding: SocketBinding,
    lib: ShieldLibrary,
    variant: str | None,
    rig_name: str,
    workdir: str,
    include_dirs: list[str] | None = None,
) -> tuple[Topology, list[Diagnostic], Deps]:
    """Apply ONE delta stage ("variant" or "revision") onto the topology,
    returning a NEW Topology plus every diagnostic raised plus every real
    file this stage's shield resolutions touched. `stage_value` is the
    selected axis value itself, folded into the drift-cannot-hide hint's
    wording. `variant` is the RIG's selected variant (the family-wide-
    revision context note's variant, only meaningful when stage ==
    "revision").

    Returns (topology, diagnostics, deps): a NEW Topology -- the input
    one is never mutated -- plus this stage's findings in document
    order and the files its shield resolutions touched."""
    code = "lang-variant" if stage == "variant" else "lang-rev"
    diags: list[Diagnostic] = []
    deps: Deps = frozenset()

    effective = dict(topology.effective)
    order = list(topology.order)
    wires = list(topology.wires)
    removed_by = dict(topology.removed_by)

    doc = as_mapping(delta, f"{stage} delta {delta.src.file}")

    d, idep = _apply_instances_key(
        doc,
        code,
        stage,
        stage_value,
        effective,
        binding,
        lib,
        variant,
        rig_name,
        workdir,
        include_dirs,
    )
    diags += d
    deps = union(deps, idep)

    d, idep = _apply_add_instances_key(
        doc,
        code,
        stage,
        stage_value,
        effective,
        order,
        binding,
        lib,
        rig_name,
        workdir,
        include_dirs,
    )
    diags += d
    deps = union(deps, idep)

    diags += _apply_remove_instances_key(doc, code, stage, stage_value, effective, removed_by)

    diags += _apply_remove_wires_key(doc, code, stage, stage_value, wires)

    diags += _apply_add_wires_key(doc, effective, wires)

    return (
        Topology(effective=effective, order=order, wires=wires, removed_by=removed_by),
        diags,
        deps,
    )
