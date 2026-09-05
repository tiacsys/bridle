# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""The loader proper: rig.yml metadata (qualifier axes), the shield
library, the required content file, fragment discovery, and the delta
engine with params/config fully wired -- assembled here from the
loader's own submodules::

  documents.py  -- mark-aware YAML, content-filename construction
  axes.py       -- revisions:/variants: declaration + resolution (the
                   hwmv2 seam) -- reused unchanged for shield.yml's own
                   revisions: axis
  binding.py    -- the invocation's board -> rig.board, and the
                   SocketBinding seam
  fragments.py  -- the contributes-nothing check for a selected
                   non-default axis value
  library.py    -- the shield library: scan, axes, lazy revision
                   resolution
  params.py     -- params:/config: machinery; the per-instance-
                   parameter vocabulary is the owning DEVICE's own
                   declared_param_includes, never a rig.yml declaration
  delta.py      -- base topology + the delta engine, resolving
                   `shield:` against the REAL library

The shield library is scanned BEFORE rig.yml even opens, so
`shield-node-name-mismatch` and every other scan-time diagnostic
precedes every rig-side one.

`load()` returns (Rig | None, diagnostics) rather than raising on a
reject: a load that finds nothing wrong hands its Rig to cli.py, which
carries on into the board reader, the analyzer and the emitter.

**Three phases**: `load()` itself is just the library scan, three
phase calls, and the final Rig assembly -- `_resolve_metadata` (rig.yml's
shell: name, qualifier axes, the invocation's board -- entirely
cpp-free), `_gather_content` (the required content file, the two delta
fragments, the contributes-nothing check), `_build_topology` (stage 0
plus the two delta stages, the per-stage invariant). Each phase returns
its OWN small value -- never a shared mutable "context" written into
across phases. `load()` concatenates each phase's diagnostics onto its
own running list, in the phases' own call order -- reproducing today's
traversal order byte for byte, since that order is the frozen stderr
contract. A LoadError raised partway through must still carry every
diagnostic gathered before the raise, or a later caller renders only
the fatal finding and silently drops the rest; the boundary that
catches LoadError therefore sits at the TOP of `load()`, wrapping the
library scan and all three phases, and re-raises with its own
diagnostics-so-far prepended. `_build_topology` carries its OWN inner
instance of the same guard, because a shield revision resolved LAZILY,
mid-topology (`ShieldLibrary.resolve`), can still raise LoadError from
inside that one phase call, same as the library scan already does in
library.py."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field

from ..deps import Deps, touch, union
from ..diag import Diagnostic, LoadError, SourceRef, anchor_path, error
from ..model import ConnectorType, Rig
from . import axes, binding, fragments
from .axes import revision_fragment_name, variant_fragment_name
from .binding import SocketBinding
from .delta import Topology, apply_delta, parse_instance, parse_wire
from .documents import Val, as_mapping, content_file_name, parse_marked, require
from .library import ShieldLibrary, load_shield_library
from .params import check_param_invariant

__all__ = ["load"]

log = logging.getLogger(__name__)


def _missing_content_diag(rig_name: str, path: str, src: SourceRef) -> Diagnostic:
    # anchor_path so the expected location renders the same way every other
    # path in a diagnostic does. A real rig lives outside scripts/<module>/,
    # so its path stays absolute here -- which is what an author needs in
    # order to create the file.
    return error(
        "lang-content",
        f"rig '{rig_name}': no content file found -- expected {anchor_path(path)}",
        (src,),
    )


# ---------------------------------------------------------------- phase 1


@dataclass(frozen=True)
class MetadataResult:
    """Phase 1's own value: rig.yml's shell -- name, qualifier axes
    resolved, and the SocketBinding this rig's topology resolves socket:
    references through. `rig` is None only when rig.yml is malformed
    enough that nothing further can be attempted (no `rig:` block, or no
    `name:` inside it); every OTHER defect found here (an axis collision,
    an unresolved axis) still produces a Rig plus diagnostics naming
    what is wrong."""

    rig: Rig | None
    binding: SocketBinding = field(default_factory=SocketBinding)


def _resolve_metadata(
    doc: Val,
    revision: str | None,
    variant: str | None,
    board: str | None = None,
) -> tuple[MetadataResult, list[Diagnostic]]:
    """The rig shell and its qualifier axes (declaration, collision,
    resolution). Entirely cpp-free -- reads `doc`'s own parsed YAML tree
    alone, so a synthetic Val tree exercises every branch here with no
    shield library, no ZEPHYR_BASE, no file on disk; this is also where
    a future hwmv2 revision-semantics seam would land, entirely inside
    this one function.

    `board`, when given, is the invocation's injected board -- the only
    source of one, since rig.yml has no `board:`/`sockets:` grammar of
    its own; `rig.board` is "" when omitted, which is legal here (see
    binding.resolve_board) and becomes a diagnostic only where a real
    board devicetree is actually needed, downstream in cli.py."""
    diags: list[Diagnostic] = []
    rig_v, d = require(doc, "rig", "top level")
    diags += d
    if rig_v is None:
        return MetadataResult(rig=None), diags
    name_v, d = require(rig_v, "name", "rig")
    diags += d
    if name_v is None:
        return MetadataResult(rig=None), diags

    rig = Rig(name=name_v.value, src=rig_v.src)

    revisions, d = axes.parse_revision_decl(rig_v, "revision", owner="rig")
    diags += d
    variants, d = axes.parse_variant_decl(rig_v, "variants", owner="rig")
    diags += d
    rig.revisions, rig.variants = revisions, variants
    diags += axes.check_axis_collision(rig.name, variants, revisions, rig_v.src)

    rig.revision_requested = revision
    rig.revision, d = axes.resolve_axis(
        rig.name, "revision", "revision", revisions, revision, rig_v.src
    )
    diags += d
    rig.variant, d = axes.resolve_axis(
        rig.name, "variant", "variants", variants, variant, rig_v.src
    )
    diags += d
    log.debug("rig '%s': selected revision=%r variant=%r", rig.name, rig.revision, rig.variant)
    if (
        rig.revision is not None
        and rig.revision_requested is not None
        and rig.revision != rig.revision_requested
    ):
        log.info(
            "rig '%s': revision requested %r resolved to %r",
            rig.name,
            rig.revision_requested,
            rig.revision,
        )

    rig.board = binding.resolve_board(board)
    sock_binding = SocketBinding()
    log.debug("rig '%s': board=%r socket binding=%r", rig.name, rig.board, sock_binding)

    return MetadataResult(rig=rig, binding=sock_binding), diags


# ---------------------------------------------------------------- phase 2


@dataclass(frozen=True)
class Deltas:
    """The rig's two (parsed, not yet APPLIED) qualifier delta fragments,
    in their fixed variant-then-revision stage order, carried to phase 3
    as a value rather than two loose fields on `ContentResult`, since
    phase 3 applies them as a PAIR in that one fixed order."""

    variant_v: Val | None = None
    revision_v: Val | None = None


@dataclass(frozen=True)
class ContentResult:
    """Phase 2's own value: the rig's required content document and its
    two delta fragments (unapplied)."""

    content_v: Val
    deltas: Deltas


def _gather_content(
    rig: Rig,
    rig_dir: str,
) -> tuple[ContentResult | None, list[Diagnostic], Deps]:
    """The rig's REQUIRED content file, its two qualifier delta
    fragments (looked up by the constructed stems `loader.axes` builds,
    never `${RIG}` literally), and the contributes-nothing check (a
    selected non-default axis value that contributes nothing). Returns
    None only when the content file itself is missing -- every other
    finding here still returns a value, matching phase 1's own
    only-truly-fatal-stops-here shape.

    Entirely cpp-free (unlike phase 3, see `_build_topology`): a delta
    fragment is parsed the same mark-aware-YAML way the base content is,
    never cpp, and the per-instance-parameter vocabulary is the owning
    shield DEVICE's own concern (`loader.params`), not something this
    phase probes -- so it never raises LoadError and needs no matching
    inner try/except boundary of its own.

    Returns (result, diagnostics, deps): deps names the content file
    itself and whichever of the two qualifier delta fragments actually
    exist -- the RIG_DEPENDS handoff's own closure over this phase."""
    assert rig.src is not None  # phase 1 always sets it before returning a Rig
    diags: list[Diagnostic] = []
    deps: Deps = frozenset()
    content_path = os.path.join(rig_dir, content_file_name(rig.name))
    if not os.path.isfile(content_path):
        diags.append(_missing_content_diag(rig.name, content_path, rig.src))
        return None, diags, deps
    deps = union(deps, touch(content_path))
    content_v = parse_marked(content_path)

    variant_delta_v: Val | None = None
    if rig.variant is not None:
        p = os.path.join(rig_dir, variant_fragment_name(rig.name, rig.variant))
        if os.path.isfile(p):
            deps = union(deps, touch(p))
            variant_delta_v = parse_marked(p)

    revision_delta_v: Val | None = None
    if rig.revision is not None:
        p = os.path.join(rig_dir, revision_fragment_name(rig.name, rig.revision))
        if os.path.isfile(p):
            deps = union(deps, touch(p))
            revision_delta_v = parse_marked(p)

    if rig.revision is not None or rig.variant is not None:
        # The contributes-nothing check is a PURE decision (fragments.py);
        # this IO phase probes
        # which contribution artifacts exist and hands the facts in as a
        # value. Names come from fragments' own constructors -- the one
        # source both the probes and the message text share.
        variant_overlay = variant_defconfig = revision_defconfig = False
        if rig.variant is not None:
            overlay, defconfig, _ = fragments.variant_contribution_names(rig.name, rig.variant)
            variant_overlay = os.path.isfile(os.path.join(rig_dir, overlay))
            variant_defconfig = os.path.isfile(os.path.join(rig_dir, defconfig))
        if rig.revision is not None:
            defconfig, _ = fragments.revision_contribution_names(rig.name, rig.revision)
            revision_defconfig = os.path.isfile(os.path.join(rig_dir, defconfig))
        diags += fragments.check_fragment_presence(
            rig,
            rig.src,
            fragments.FragmentPresence(
                variant_delta=variant_delta_v is not None,
                variant_overlay=variant_overlay,
                variant_defconfig=variant_defconfig,
                revision_delta=revision_delta_v is not None,
                revision_defconfig=revision_defconfig,
            ),
        )

    return (
        ContentResult(
            content_v=content_v,
            deltas=Deltas(variant_v=variant_delta_v, revision_v=revision_delta_v),
        ),
        diags,
        deps,
    )


# ---------------------------------------------------------------- phase 3


def _build_topology(
    rig: Rig,
    sock_binding: SocketBinding,
    lib: ShieldLibrary,
    content: ContentResult,
    workdir: str,
    include_dirs: list[str] | None,
) -> tuple[Topology, list[Diagnostic], Deps]:
    """Stage 0 (the base content's instances:/wires:, order preserved,
    the per-stage invariant checked per instance as it is parsed), then
    the variant delta stage, then the revision delta stage -- each
    re-checking the invariant over the whole topology afterward.

    A shield revision resolved LAZILY here (`ShieldLibrary.resolve`,
    reached through `parse_instance`/`apply_delta`) can raise LoadError
    mid-loop -- this phase's OWN try/except carries this call's
    diagnostics-so-far into the exception, the same shape
    `load_shield_library` already applies to its own scan loop, so the
    outer boundary in `load()` renders every finding gathered before the
    raise, never just the fatal one.

    Returns (topology, diagnostics, deps): deps is the UNION of every
    shield resolution this phase made -- stage 0's own `parse_instance`
    calls AND both delta stages' `apply_delta` -- never derived from the
    final topology alone: a variant stage that SUBSTITUTES one
    instance's shield for another still leaves the base stage's own
    resolution (of the shield the variant replaced) in this union,
    because that resolution genuinely happened -- RIG_DEPENDS records
    resolution HISTORY, not final topology."""
    diags: list[Diagnostic] = []
    deps: Deps = frozenset()
    try:
        content_map = as_mapping(
            content.content_v, f"content document {content.content_v.src.file}"
        )

        topology = Topology()
        insts_v, d = require(content.content_v, "instances", "content")
        diags += d
        for item in insts_v.value if insts_v is not None else []:
            inst, d, idep = parse_instance(item, sock_binding, lib, rig.name, workdir, include_dirs)
            diags += d
            deps = union(deps, idep)
            if inst is not None:
                topology.effective[inst.name] = inst
                topology.order.append(inst.name)
                diags += check_param_invariant([inst])

        wires_v = content_map.get("wires")
        for item in wires_v.value if wires_v is not None else []:
            wire, d = parse_wire(item, topology.effective)
            diags += d
            if wire is not None:
                topology.wires.append(wire)

        # Stage 1: variant delta.
        if content.deltas.variant_v is not None:
            assert rig.variant is not None  # a delta only loads for a selected axis
            topology, d, idep = apply_delta(
                content.deltas.variant_v,
                "variant",
                rig.variant,
                topology,
                sock_binding,
                lib,
                rig.variant,
                rig.name,
                workdir,
                include_dirs,
            )
            diags += d
            deps = union(deps, idep)
            diags += check_param_invariant(topology.instances())

        # Stage 2: revision delta -- ONE family-wide stream, applied AFTER
        # the variant.
        if content.deltas.revision_v is not None:
            assert rig.revision is not None  # a delta only loads for a selected axis
            topology, d, idep = apply_delta(
                content.deltas.revision_v,
                "revision",
                rig.revision,
                topology,
                sock_binding,
                lib,
                rig.variant,
                rig.name,
                workdir,
                include_dirs,
            )
            diags += d
            deps = union(deps, idep)
            diags += check_param_invariant(topology.instances())

        return topology, diags, deps
    except LoadError as e:
        raise LoadError(*diags, *e.diags) from None


# ---------------------------------------------------------------- load()


def load(
    rig_path: str,
    workdir: str,
    shield_dirs: list[str] | None = None,
    revision: str | None = None,
    variant: str | None = None,
    board: str | None = None,
    types: dict[str, ConnectorType] | None = None,
    include_dirs: list[str] | None = None,
) -> tuple[Rig | None, list[Diagnostic], Deps]:
    """Load rig_path (absolute) as far as rigc's loader reaches, returning
    the built Rig (best-effort; None only when nothing further could be
    attempted at all) alongside every diagnostic found. Loading CONTINUES
    after most errors rather than stopping at the first diagnostic, so a
    later one is never dropped.

    `workdir` is where every `.shield` translation unit and per-instance-
    parameter resolution probe gets synthesized (cli.py's responsibility
    to create/clean up).

    `board`, when given, is the invocation's injected board (the cmake
    seam always supplies one) -- threaded straight to
    `_resolve_metadata`/`binding.resolve_board`, the ONLY source of
    `rig.board`, since rig.yml has no `board:` grammar of its own.
    Omitted (the standalone CLI's default, and `west rigs
    --boards-for`'s own census call), `rig.board` is simply "" -- legal
    here; nothing in this loader needs a real board to assemble a
    topology.

    Returns (rig, diagnostics, deps): deps is the UNION of every real
    source-tree file this load touched -- rig_path itself, the shield
    library scan (library.py's own eager-breadth deps, unchanged whether
    a rig ends up naming the shield or not), the content file plus
    whichever qualifier delta fragments exist (`_gather_content`), and
    every shield resolution the topology stages made (`_build_topology`,
    unioned rather than derived from the final instance list). This is
    the RIG_DEPENDS handoff's own value; cli.py composes it with the
    connector-registry and board deps and hands the result to
    `context.render`. The caller owns the Rig and the Deps alike."""
    # LoadError (a fatal parse/cpp failure, dtsio.py) can surface from
    # the library scan below or a lazy shield resolve mid-topology. With
    # diagnostics as return values rather than a shared accumulator, a
    # raise would otherwise drop every diagnostic gathered before it;
    # THIS boundary catches instead and returns everything gathered so
    # far plus what the exception carries, so no finding is lost.
    diags: list[Diagnostic] = []
    deps: Deps = frozenset()
    try:
        lib, diags, lib_deps = load_shield_library(
            workdir, shield_dirs, types=types, include_dirs=include_dirs
        )
        deps = union(deps, lib_deps)

        deps = union(deps, touch(rig_path))
        doc = parse_marked(rig_path)

        log.info("load(): resolving metadata")
        meta, d = _resolve_metadata(doc, revision, variant, board)
        diags += d
        if meta.rig is None:
            return None, diags, deps
        rig, sock_binding = meta.rig, meta.binding

        log.info("load(): gathering content")
        rig_dir = os.path.dirname(rig_path)
        content, d, cdeps = _gather_content(rig, rig_dir)
        diags += d
        deps = union(deps, cdeps)
        if content is None:
            return None, diags, deps

        log.info("load(): building topology")
        topology, d, tdeps = _build_topology(rig, sock_binding, lib, content, workdir, include_dirs)
        diags += d
        deps = union(deps, tdeps)

        rig.instances = topology.instances()
        rig.wires = topology.wires
        for inst in rig.instances:
            socket_desc = ", ".join(
                f"{slot}={ref if ref is not None else '(inferred)'}"
                for slot, ref in inst.sockets.items()
            )
            log.info(
                "rig '%s': instance '%s' requires shield '%s', mated to socket '%s'",
                rig.name,
                inst.name,
                inst.shield.name,
                socket_desc,
            )
        return rig, diags, deps
    except LoadError as e:
        return None, diags + list(e.diags), deps
