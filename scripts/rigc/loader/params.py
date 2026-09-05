# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Params, config elements, per-instance-parameter vocabulary: `shield:`
references resolve against a real `ShieldLibrary`, and this is where
`params:`/`config:` apply fully against the resolved shield. The
rig-side key is `config:`, resolving by DTS label, never by node name.

Every function here takes the NARROW values it needs (a shield, a
params: Val, a rig NAME) rather than a whole `Rig` or `Instance` --
"whole-model inputs where a value would do": the caller
(loader/delta.py) already holds these pieces and assigns the result
onto a freshly constructed Instance, matching its own no-mutation
discipline.

**The vocabulary a param token resolves against is the OWNING DEVICE's
own `declared_param_includes`, never a rig-level declaration** -- the
shield that declares a parameter declares the vocabulary that
parameter is drawn from, so `check_param_token` takes the device's own
header list, not something threaded down from rig.yml.
"""

from __future__ import annotations

from ..deps import Deps, touch, union
from ..diag import Diagnostic, SourceRef, error
from ..dtsio import MODULE_INC, check_include, is_int_literal, resolve_token, zephyr_inc
from ..model import Device, Shield, Strap
from .documents import Val


def device_required_params(dev: Device) -> list[str]:
    """The subset of `dev.declared_params` (`shield,params` names) with NO
    authored default -- i.e. no matching entry in `dev.extra_props` -- the
    exact per-device rule `check_param_invariant` applies to every
    instance's effective shield. Factored out so a caller holding only a
    SHIELD (no instance, no assignment in play -- promote.py's
    `shield_declares_required_params`) can ask the identical question
    without re-deriving "declared, no default" a second time. Pure; dev
    is read-only, returns a fresh list the caller owns."""
    return [
        pname
        for pname in dev.declared_params
        if not any(name == pname for name, _ in dev.extra_props)
    ]


def check_param_invariant(instances) -> list[Diagnostic]:
    """The per-stage invariant, re-checked fresh after EVERY delta
    stage: every instance's EFFECTIVE shield/params must have every
    declared, no-default-authored parameter ASSIGNED. Covers all three
    sources of a parameter-set change (a base assignment, a shield swap,
    a shield REVISION introducing a new requirement) with no special
    casing, since it only ever looks at the CURRENT shield + CURRENT
    params.

    Returns one error per required-but-unassigned parameter; instances
    are read-only."""
    diags: list[Diagnostic] = []
    for inst in instances:
        shield = inst.shield
        assigned = inst.params
        refs = (inst.src,) if inst.src is not None else ()
        for dev in shield.devices:
            pset = assigned.get(dev.label, {})
            for pname in device_required_params(dev):
                if pname in pset:
                    continue
                diags.append(
                    error(
                        "lang-param",
                        f"instance '{inst.name}': device '{dev.label}' of "
                        f"shield '{shield.name}' declares '{pname}' as "
                        "required (shield,params, no default authored) but "
                        f"this instance does not assign it — add params: "
                        f"{{{dev.label}: {{{pname}: <value>}}}}",
                        refs,
                    )
                )
    return diags


def check_param_token(
    raw: str,
    param_includes: list[str],
    workdir: str,
    tag: str,
    inst_name: str,
    dev_label: str,
    shield_name: str,
    prop_name: str,
    ref: SourceRef,
    include_dirs: list[str] | None = None,
) -> tuple[list[Diagnostic], Deps]:
    """The per-instance-parameter header and token-resolution checks,
    collapsed into one shape now that the vocabulary is the owning
    device's own, not a rig-level list: every header in
    `param_includes` (`dev.declared_param_includes`, the caller's own
    copy) must exist and preprocess cleanly on its own, and an assigned
    token that is not a bare integer literal must resolve against that
    same list. The header check runs here, per device, rather than once
    per shield at parse time, because this is the only call site that
    already has a reason to preprocess each header at all (a device
    whose parameters are never assigned a non-literal token never pays
    for it); `emitter._needed_param_includes` independently re-derives
    the same "which headers does this rig need" answer from the SOLVED
    side -- a change here that stops walking every declared header must
    be mirrored there.

    Returns (diagnostics, deps): one diagnostic per header that is
    missing or fails to preprocess, plus one more if the token itself
    still fails to resolve once every header is confirmed good; empty
    when both checks pass. deps is the union of every real file each of
    `param_includes`' own preprocess opened (dtsio.check_include),
    recorded whether or not either check succeeds -- a header the token
    actually resolves against is a real dependency of this rig
    (RIG_DEPENDS), and it is exactly the file an author is about to edit
    when it does not. Inputs are read-only; the caller owns the returned
    Deps."""
    deps: Deps = frozenset()
    diags: list[Diagnostic] = []
    searched = ", ".join([*(include_dirs or []), zephyr_inc(), MODULE_INC])
    for i, header in enumerate(param_includes):
        detail, files = check_include(header, workdir, f"{tag}_{i}", include_dirs)
        deps = union(deps, *(touch(f) for f in files))
        if detail is not None:
            diags.append(
                error(
                    "lang-dt-include",
                    f"instance '{inst_name}': device '{dev_label}' of shield "
                    f"'{shield_name}' declares param-includes header "
                    f"'{header}' that is not found or fails to preprocess "
                    f"(searched {searched})\n{detail}",
                    (ref,),
                )
            )
    if resolve_token(raw, param_includes, workdir, tag, include_dirs) is not None:
        return diags, deps
    diags.append(
        error(
            "lang-dt-include",
            f"instance '{inst_name}': device '{dev_label}' property "
            f"'{prop_name}' assigns '{raw}', which does not resolve against "
            f"the param-includes shield '{shield_name}' declares for this "
            f"device ({', '.join(param_includes) or 'none'}) — add the header "
            f"that defines it to shield,param-includes on '{dev_label}'",
            (ref,),
        )
    )
    return diags, deps


def apply_params_block(
    params_v: Val | None,
    inst_name: str,
    shield: Shield,
    workdir: str,
    tag_prefix: str,
    unknown_device_context: str | None = None,
    include_dirs: list[str] | None = None,
) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, SourceRef]], list[Diagnostic], Deps]:
    """Parse ONE params: block -- the base assignment, OR a delta's
    wholesale replacement -- into (params, param_refs, diagnostics, deps),
    a PURE function of its inputs: never mutates the Instance it
    describes, the caller assigns the result onto a freshly constructed
    one. The undeclared-property and unknown-device checks fire
    immediately against the CURRENT shield; token resolution (against
    the owning device's own declared_param_includes) too. Whether every
    required parameter is assigned is deliberately NOT checked here --
    that is the per-stage invariant, run once per stage over every
    instance, since a LATER stage may still supply what an EARLIER one
    left required-but-unassigned.

    `unknown_device_context`, if given, is folded into the
    unknown-device message when it fires: a family-wide revision's
    params naming a device the POST-VARIANT shield does not have is
    unavoidable by construction whenever a variant already substituted
    the shield.

    Returns (params, refs, diagnostics, deps): fresh values the caller
    owns; deps is the union of every real file a non-literal token's
    resolution attempt opened (check_param_token), empty when every
    assigned value is a bare integer literal. Nothing handed in is
    touched."""
    if params_v is None:
        return {}, {}, [], frozenset()
    diags: list[Diagnostic] = []
    deps: Deps = frozenset()
    params: dict[str, dict[str, str]] = {}
    param_refs: dict[str, dict[str, SourceRef]] = {}
    devices_by_label = {d.label: d for d in shield.devices}
    for dev_label, props_v in params_v.value.items():
        dev = devices_by_label.get(dev_label)
        if dev is None:
            context = f" ({unknown_device_context})" if unknown_device_context else ""
            diags.append(
                error(
                    "lang-param",
                    f"instance '{inst_name}': params names no device "
                    f"'{dev_label}' of shield '{shield.name}'{context}\n"
                    f"devices of '{shield.name}': "
                    f"{', '.join(sorted(devices_by_label)) or 'none'}",
                    (props_v.src,),
                )
            )
            continue
        for prop_name, val_v in props_v.value.items():
            if prop_name not in dev.declared_params:
                diags.append(
                    error(
                        "lang-param",
                        f"instance '{inst_name}': device '{dev_label}' of "
                        f"shield '{shield.name}' declares no parameter "
                        f"'{prop_name}' (shield,params)\n"
                        f"declared parameters of '{dev_label}': "
                        f"{', '.join(dev.declared_params) or 'none'}",
                        (val_v.src,),
                    )
                )
                continue
            raw = str(val_v.value)
            params.setdefault(dev_label, {})[prop_name] = raw
            param_refs.setdefault(dev_label, {})[prop_name] = val_v.src
            if not is_int_literal(raw):
                tag = f"{tag_prefix}_{dev_label}_{prop_name}"
                d, tdeps = check_param_token(
                    raw,
                    dev.declared_param_includes,
                    workdir,
                    tag,
                    inst_name,
                    dev_label,
                    shield.name,
                    prop_name,
                    val_v.src,
                    include_dirs,
                )
                diags += d
                deps = union(deps, tdeps)
    return params, param_refs, diags, deps


def apply_config_block(
    config_v: Val | None,
    inst_name: str,
    shield: Shield,
) -> tuple[
    dict[str, int], dict[str, SourceRef], dict[str, object], dict[str, SourceRef], list[Diagnostic]
]:
    """config: {config-element-LABEL: value} -- shared by the base parse
    and a delta's instances: patch (which resets straps/jumpers first, so
    this always starts from empty when called from a patch). PURE:
    returns fresh dicts, never mutates an Instance.

    Resolution is by DTS LABEL only (`Shield.config_element`) -- the
    node name is refused, and there is no underscore/hyphen
    normalization: a label can never contain a hyphen, so trying one
    could only mis-resolve. The returned dicts stay keyed by the
    element's own NODE NAME regardless (`elem.name`): that is the
    internal identity `apply_delta`/the analyzer already key
    `Instance.straps`/`.jumpers` by, unaffected by which string a rig
    author used to name the element.

    Returns (straps, strap_refs, jumpers, jumper_refs, diagnostics), all
    fresh values the caller owns."""
    straps: dict[str, int] = {}
    strap_refs: dict[str, SourceRef] = {}
    jumpers: dict[str, object] = {}
    jumper_refs: dict[str, SourceRef] = {}
    diags: list[Diagnostic] = []
    if config_v is None:
        return straps, strap_refs, jumpers, jumper_refs, diags
    for cfg_label, val_v in config_v.value.items():
        # resolution rule: config keys name a config element (strap OR
        # routing jumper) of the named shield, BY LABEL
        elem = shield.config_element(cfg_label)
        if elem is None:
            labels = sorted(
                [s.label for s in shield.straps.values()]
                + [j.label for j in shield.jumpers.values()]
            )
            diags.append(
                error(
                    "lang-config",
                    f"instance '{inst_name}': config names no config element "
                    f"'{cfg_label}' of shield '{shield.name}'\n"
                    f"config elements of '{shield.name}': "
                    f"{', '.join(labels) or 'none'}",
                    (val_v.src,),
                )
            )
            continue
        if isinstance(elem, Strap):
            straps[elem.name] = val_v.value
            strap_refs[elem.name] = val_v.src
        else:  # Jumper: position value
            jumpers[elem.name] = val_v.value
            jumper_refs[elem.name] = val_v.src
    return straps, strap_refs, jumpers, jumper_refs, diags


def check_restate(
    params_v: Val, prior_params: dict[str, dict[str, str]], inst_name: str
) -> list[Diagnostic]:
    """The restate rule: if a delta supplies params for an instance whose
    shield it does NOT change, it must RESTATE every property the effective
    topology had already assigned; omitting one is an error naming it --
    otherwise wholesale replace means a silent revert to the shield
    default. Called with the PRIOR params (before the wholesale replace
    clears them).

    Returns one error per property omitted from the restatement;
    prior_params is read-only."""
    restated = {
        (dev_label, prop_name)
        for dev_label, props_v in params_v.value.items()
        for prop_name in props_v.value
    }
    diags: list[Diagnostic] = []
    for dev_label, props in prior_params.items():
        for prop_name in props:
            if (dev_label, prop_name) not in restated:
                diags.append(
                    error(
                        "lang-param",
                        f"instance '{inst_name}': this delta supplies params "
                        f"for device '{dev_label}' without restating "
                        f"'{prop_name}', which the effective topology already "
                        "assigns -- wholesale replace means omitting it "
                        "silently reverts to the shield default; restate it "
                        "explicitly or remove it deliberately",
                        (params_v.src,),
                    )
                )
    return diags
