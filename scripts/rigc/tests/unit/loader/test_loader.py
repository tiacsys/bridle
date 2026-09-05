# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: loader (loader/__init__.py) -- `load()`'s three-phase split:
`_resolve_metadata` (steps 2-5, the rig
shell), `_gather_content` (steps 6-9, the content file + delta
fragments + the contributes-nothing check), `_build_topology` (steps
10-11, stage 0 plus the two delta stages).

`_resolve_metadata` and `_gather_content` are entirely cpp-free --
every test below feeds them a synthetic, already-parsed rig.yml document
(via `documents.parse_marked` over a tmp file: still hermetic, no shield
library, no ZEPHYR_BASE, no subprocess) and asserts the values they
build. `_build_topology` gets lighter coverage of its own SHAPE (its
cpp-reaching branch -- a lazily-resolved shield revision -- is
integration-only by construction, same seam as `loader.library`'s own
eager-parse branch); every scenario here stays inside the cpp-free
subset on purpose, so the unit suite's hermeticity holds."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from rigc.diag import SourceRef
from rigc.loader import ContentResult, Deltas, _build_topology, _gather_content, _resolve_metadata
from rigc.loader.binding import SocketBinding
from rigc.loader.documents import Val, parse_marked
from rigc.loader.library import ShieldLibrary
from rigc.model import AxisDecl, Rig

_SRC = SourceRef("synthetic", 1, "rig")


def _write(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / name
    path.write_text(dedent(text))
    return path


def _parsed(tmp_path: Path, name: str, text: str) -> Val:
    return parse_marked(str(_write(tmp_path, name, text)))


def _rig(**kwargs: object) -> Rig:
    """A Rig as `_resolve_metadata` would hand one to phase 2/3 -- `src`
    set (phase 1 always does, from rig.yml's own `rig:` key), which
    `_gather_content` relies on for its own diagnostics' anchors."""
    kwargs.setdefault("src", _SRC)
    return Rig(name="r", **kwargs)  # type: ignore[arg-type]


def _empty_lib(workdir: str) -> ShieldLibrary:
    return ShieldLibrary(shields={}, axes={}, pending={}, ymls={}, types={}, workdir=workdir)


# ---------------------------------------------------------------- _resolve_metadata


def test_resolve_metadata_rejects_a_missing_rig_block(tmp_path: Path) -> None:
    doc = _parsed(tmp_path, "rig.yml", "not-rig: {}\n")
    meta, diags = _resolve_metadata(doc, None, None)
    assert meta.rig is None
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"


def test_resolve_metadata_rejects_a_missing_name(tmp_path: Path) -> None:
    doc = _parsed(tmp_path, "rig.yml", "rig: {}\n")
    meta, diags = _resolve_metadata(doc, None, None)
    assert meta.rig is None
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"


def test_resolve_metadata_happy_path_with_no_axes(tmp_path: Path) -> None:
    """board is never read off rig.yml -- `board="b/s/rig"` here is the
    INJECTED value, the only source of `meta.rig.board`."""
    doc = _parsed(tmp_path, "rig.yml", "rig:\n  name: r\n")
    meta, diags = _resolve_metadata(doc, None, None, board="b/s/rig")
    assert diags == []
    assert meta.rig is not None
    assert meta.rig.name == "r"
    assert meta.rig.board == "b/s/rig"
    assert meta.rig.revision is None
    assert meta.rig.variant is None
    assert isinstance(meta.binding, SocketBinding)
    assert meta.binding.get("x") == "x"  # lookup-else-identity


def test_resolve_metadata_board_absent_is_the_empty_string_with_no_diagnostic(
    tmp_path: Path,
) -> None:
    """The negative control: omitting `board` is legal, not an error --
    rig.yml has no grammar left to declare one from, and this loader
    phase never needed a real board to assemble a topology. A caller
    that DOES need one (cli.py, right before load_board) is
    where an empty board becomes a diagnostic, not here."""
    doc = _parsed(tmp_path, "rig.yml", "rig:\n  name: r\n")
    meta, diags = _resolve_metadata(doc, None, None)
    assert diags == []
    assert meta.rig is not None
    assert meta.rig.board == ""


def test_resolve_metadata_resolves_the_declared_default_revision(tmp_path: Path) -> None:
    doc = _parsed(
        tmp_path,
        "rig.yml",
        "rig:\n"
        "  name: r\n"
        "  revision:\n"
        "    format: number\n"
        "    default: '1'\n"
        "    revisions:\n"
        "      - name: '1'\n"
        "      - name: '2'\n",
    )
    meta, diags = _resolve_metadata(doc, None, None)
    assert diags == []
    assert meta.rig is not None
    assert meta.rig.revision == "1"
    assert meta.rig.revision_requested is None


def test_resolve_metadata_an_explicit_revision_selection_wins_over_the_default(
    tmp_path: Path,
) -> None:
    doc = _parsed(
        tmp_path,
        "rig.yml",
        "rig:\n"
        "  name: r\n"
        "  revision:\n"
        "    format: number\n"
        "    default: '1'\n"
        "    revisions:\n"
        "      - name: '1'\n"
        "      - name: '2'\n",
    )
    meta, diags = _resolve_metadata(doc, "2", None)
    assert diags == []
    assert meta.rig is not None
    assert meta.rig.revision == "2"
    assert meta.rig.revision_requested == "2"


def test_resolve_metadata_nearest_lower_match_keeps_requested_for_provenance(
    tmp_path: Path,
) -> None:
    """The requested/resolved split: a nearest-lower match resolves
    DOWN, but the RAW requested string survives on `revision_requested`
    -- what a caller (the configure-log "requested -> resolved" line)
    needs to tell the two apart."""
    doc = _parsed(
        tmp_path,
        "rig.yml",
        "rig:\n"
        "  name: r\n"
        "  revision:\n"
        "    format: number\n"
        "    default: '1'\n"
        "    revisions:\n"
        "      - name: '1'\n"
        "      - name: '2'\n",
    )
    meta, diags = _resolve_metadata(doc, "99", None)
    assert diags == []
    assert meta.rig is not None
    assert meta.rig.revision == "2"
    assert meta.rig.revision_requested == "99"


def test_resolve_metadata_reports_an_axis_collision(tmp_path: Path) -> None:
    """A variant name equal to a revision id constructs the same
    fragment stem -- still returns a Rig (not None), since the collision
    is a warning-shaped continuation, not a stop-here defect. '9' rather
    than a word: a variant name has no format constraint, but a revision
    id must match its own declared format (number here)."""
    doc = _parsed(
        tmp_path,
        "rig.yml",
        "rig:\n"
        "  name: r\n"
        "  variants:\n"
        "    default: '9'\n"
        "    list: ['9']\n"
        "  revision:\n"
        "    format: number\n"
        "    default: '9'\n"
        "    revisions:\n"
        "      - name: '9'\n",
    )
    meta, diags = _resolve_metadata(doc, None, None)
    assert meta.rig is not None
    assert any(d.code == "lang-variant" for d in diags)


# ---------------------------------------------------------------- _gather_content


def test_gather_content_rejects_a_missing_content_file(tmp_path: Path) -> None:
    rig = _rig()
    content, diags, deps = _gather_content(rig, str(tmp_path))
    assert content is None
    assert len(diags) == 1
    assert diags[0].code == "lang-content"
    assert deps == frozenset()


def test_gather_content_reads_an_empty_content_file(tmp_path: Path) -> None:
    content_path = _write(
        tmp_path,
        "r.yml",
        """\
        instances: []
        """,
    )
    rig = _rig()
    content, diags, deps = _gather_content(rig, str(tmp_path))
    assert diags == []
    assert content is not None
    assert content.deltas == Deltas(variant_v=None, revision_v=None)
    assert deps == frozenset((str(content_path),))


def test_gather_content_a_nondefault_variant_contributing_nothing_is_rejected(
    tmp_path: Path,
) -> None:
    _write(
        tmp_path,
        "r.yml",
        """\
        instances: []
        """,
    )
    rig = _rig(variant="b", variants=AxisDecl(values=["a", "b"], default="a"))
    _content, diags, _deps = _gather_content(rig, str(tmp_path))
    assert len(diags) == 1
    assert diags[0].code == "lang-variant"
    assert "contributes nothing" in diags[0].message


def test_gather_content_finds_and_carries_the_variant_delta_fragment(tmp_path: Path) -> None:
    content_path = _write(
        tmp_path,
        "r.yml",
        """\
        instances: []
        """,
    )
    fragment_path = _write(
        tmp_path,
        "r_b.yml",
        """\
        instances: []
        """,
    )
    rig = _rig(variant="b", variants=AxisDecl(values=["a", "b"], default="a"))
    content, diags, deps = _gather_content(rig, str(tmp_path))
    assert diags == []
    assert content is not None
    assert content.deltas.variant_v is not None
    assert content.deltas.revision_v is None
    assert deps == frozenset((str(content_path), str(fragment_path)))


def test_gather_content_finds_and_carries_the_revision_delta_fragment(tmp_path: Path) -> None:
    content_path = _write(
        tmp_path,
        "r.yml",
        """\
        instances: []
        """,
    )
    fragment_path = _write(
        tmp_path,
        "r_2.yml",
        """\
        instances: []
        """,
    )
    rig = _rig(revision="2", revisions=AxisDecl(values=["1", "2"], default="1"))
    content, diags, deps = _gather_content(rig, str(tmp_path))
    assert diags == []
    assert content is not None
    assert content.deltas.variant_v is None
    assert content.deltas.revision_v is not None
    assert deps == frozenset((str(content_path), str(fragment_path)))


# ---------------------------------------------------------------- _build_topology


def test_build_topology_resolves_an_instance_from_an_already_cached_shield(tmp_path: Path) -> None:
    """`ShieldLibrary.resolve` cache-hits on a shield already present in
    `.shields` (`.axes[name] is None` -- no declared revisions: axis)
    without ever calling `parse_tu` (cpp) -- so a real Instance parse,
    including a wire between two of its nodes, stays cpp-free here."""
    from rigc.model import Pad, Shield

    shield = Shield(
        name="sh",
        label="sh",
        plugs={"plug": "fixture-type"},
        pads={
            "a": Pad(name="a", label="a", role="driver", of=None),
            "b": Pad(name="b", label="b", role="listener", of=None),
        },
    )
    lib = ShieldLibrary(
        shields={"sh": shield},
        axes={"sh": None},
        pending={},
        ymls={},
        types={},
        workdir=str(tmp_path),
    )
    content_v = _parsed(
        tmp_path,
        "content.yml",
        "instances:\n"
        "  - {name: i1, shield: sh, socket: s1}\n"
        "wires:\n"
        "  - {from: i1.a, to: i1.b, route: adhoc}\n",
    )
    content = ContentResult(content_v=content_v, deltas=Deltas())
    rig = _rig()
    topology, diags, _deps = _build_topology(
        rig, SocketBinding(), lib, content, str(tmp_path), None
    )
    assert diags == []
    assert [i.name for i in topology.instances()] == ["i1"]
    assert len(topology.wires) == 1


def test_build_topology_unions_deps_across_variant_substitution(tmp_path: Path) -> None:
    """RIG_DEPENDS records RESOLUTION HISTORY, not final topology --
    a variant stage that substitutes one
    instance's shield away must still leave the base stage's own
    resolution (of the shield the variant replaced) in the union, never
    derived from the final instance list alone (which would silently
    drop it). Mirrors pilot_variants_variant_c, whose accept golden's
    RIG_DEPENDS still names adafruit_data_logger/shield.yml although
    RIG_SHIELDS lists only pilot_alt_button."""
    from rigc.model import Shield

    sh_a = Shield(name="sh_a", label="sh_a", plugs={"plug": "fixture-type"})
    sh_b = Shield(name="sh_b", label="sh_b", plugs={"plug": "fixture-type"})
    lib = ShieldLibrary(
        shields={"sh_a": sh_a, "sh_b": sh_b},
        axes={"sh_a": None, "sh_b": None},
        pending={},
        ymls={"sh_a": "/fake/sh_a/shield.yml", "sh_b": "/fake/sh_b/shield.yml"},
        types={},
        workdir=str(tmp_path),
    )
    content_v = _parsed(
        tmp_path, "content.yml", "instances:\n  - {name: i1, shield: sh_a, socket: s1}\n"
    )
    variant_v = _parsed(tmp_path, "variant.yml", "instances:\n  - {name: i1, shield: sh_b}\n")
    content = ContentResult(content_v=content_v, deltas=Deltas(variant_v=variant_v))
    rig = _rig(variant="v", variants=AxisDecl(values=["v"], default="v"))

    topology, diags, deps = _build_topology(rig, SocketBinding(), lib, content, str(tmp_path), None)

    assert diags == []
    assert [i.shield.name for i in topology.instances()] == ["sh_b"]
    assert deps == frozenset(("/fake/sh_a/shield.yml", "/fake/sh_b/shield.yml"))


def test_build_topology_of_an_empty_content_document(tmp_path: Path) -> None:
    content_v = _parsed(tmp_path, "content.yml", "instances: []\n")
    content = ContentResult(content_v=content_v, deltas=Deltas())
    rig = _rig()
    topology, diags, deps = _build_topology(
        rig, SocketBinding(), _empty_lib(str(tmp_path)), content, str(tmp_path), None
    )
    assert diags == []
    assert topology.instances() == []
    assert topology.wires == []
    assert deps == frozenset()


def test_build_topology_a_wire_naming_an_unknown_instance_is_rejected(tmp_path: Path) -> None:
    content_v = _parsed(
        tmp_path, "content.yml", "instances: []\nwires:\n  - {from: a.x, to: b.y, route: adhoc}\n"
    )
    content = ContentResult(content_v=content_v, deltas=Deltas())
    rig = _rig()
    topology, diags, _deps = _build_topology(
        rig, SocketBinding(), _empty_lib(str(tmp_path)), content, str(tmp_path), None
    )
    assert topology.wires == []
    # both endpoints name an instance the (empty) topology doesn't have
    assert len(diags) == 2
    assert all(d.code == "lang-wire-ref" for d in diags)
