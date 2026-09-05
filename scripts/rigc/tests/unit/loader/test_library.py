# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: loader.library -- the shield library's VALUE-shaped contracts:
`_pick_shield`'s declared-name-vs-node-name
decision (a pure function over already-parsed Shield values), `resolve()`'s
three failure shapes plus lazy-parse memoization for BOTH axis-less base
templates and revisions (exercised against a synthetic library VALUE,
never a filesystem scan), shield.yml's own entries (`_shield_yml_entries`,
file-based but cpp-free -- one per `shield:` or N per `shields:`, each
carrying its own `template:` flag and `revisions:` Val), and
`load_shield_library`'s discovery breadth -- every discovered RIG TEMPLATE,
axis-less or not, lands in `pending`, none of it parsed.

**The cpp/unit-test seam**: every template parse, axis-less base or
revision alike, funnels through the ONE module-level helper
`_parse_shield_template`, which calls `dtsio.parse_tu` (cpp, a real
subprocess) -- integration-only by construction, covered through the
frozen suite's front door. Tests here keep resolve()'s CONTROL FLOW
(when the helper is called, how its result is memoized, what deps compose
around it) unit-testable by either constructing a `ShieldLibrary` value
directly (never scanning a filesystem) and arranging for `resolve()` to
return before ever reaching the helper (a cache hit, or one of the
three failure shapes), or by monkeypatching `_parse_shield_template`
itself to a canned stub -- the same seam-substitution idiom
`test_board_resolve.py` uses for `project.load_board`. `load_shield_library`'s
DISCOVERY is exercised directly against real folders (garbage `.shield`
content included, deliberately, since discovery never reads it):
neither axis-less nor revisioned shields are ever eagerly parsed, so
scanning stays subprocess-free unconditionally.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from rigc.deps import Deps
from rigc.diag import Diagnostic, SourceRef, error
from rigc.loader.axes import parse_legacy_revision_decl
from rigc.loader.library import (
    ShieldLibrary,
    _Pending,
    _pick_shield,
    _shield_yml_entries,
    load_shield_library,
)
from rigc.model import AxisDecl, ConnectorType, Shield

_SRC = SourceRef("synthetic", 1, "instance 'x'")


def _shield(name: str) -> Shield:
    return Shield(
        name=name, label=name, plugs={"plug": "fixture-type"}, src=SourceRef("synthetic", 1)
    )


# ---------------------------------------------------------------- _pick_shield


def test_pick_shield_matches_by_folder_name() -> None:
    parsed = {"other": _shield("other"), "wanted": _shield("wanted")}
    shield, diags = _pick_shield(parsed, "wanted", "/some/wanted/wanted.shield")
    assert diags == []
    assert shield is parsed["wanted"]


def test_pick_shield_mismatch_is_rejected() -> None:
    parsed = {"other_name": _shield("other_name")}
    shield, diags = _pick_shield(parsed, "misnamed", "/x/misnamed/misnamed.shield")
    assert shield is None
    assert len(diags) == 1
    assert diags[0].code == "lang-shield-name"
    assert "other_name" in diags[0].message
    assert "misnamed.shield" in diags[0].message


def test_pick_shield_reports_none_when_the_template_defines_nothing() -> None:
    shield, diags = _pick_shield({}, "empty", "/x/empty/empty.shield")
    assert shield is None
    assert "nodes defined here: none" in diags[0].message


def test_pick_shield_mismatch_names_shield_yml_as_the_source_when_given_one() -> None:
    """A mismatch on a name that came FROM shield.yml (yml_path given)
    must say so, never claim the folder as the source -- the wording
    the yml-less case above keeps is only true when there is no
    shield.yml to have named it."""
    parsed = {"other_name": _shield("other_name")}
    shield, diags = _pick_shield(
        parsed, "declared", "/x/folder/declared.shield", yml_path="/x/folder/shield.yml"
    )
    assert shield is None
    assert "shield.yml itself declares" in diags[0].message
    assert "the folder it lives in" not in diags[0].message
    assert "other_name" in diags[0].message


# ------------------------------------------------------- _shield_yml_entries


def test_shield_yml_entries_absent_file_yields_nothing(tmp_path: Path) -> None:
    yml_path, entries, diags = _shield_yml_entries(str(tmp_path))
    assert yml_path is None
    assert entries == []
    assert diags == []


def test_shield_yml_entries_singular_shield_key(tmp_path: Path) -> None:
    (tmp_path / "shield.yml").write_text(
        dedent("""\
        shield:
          name: fx
        """)
    )
    yml_path, entries, diags = _shield_yml_entries(str(tmp_path))
    assert yml_path == str(tmp_path / "shield.yml")
    assert diags == []
    assert [(name, promotable) for name, _v, promotable in entries] == [("fx", False)]


def test_shield_yml_entries_plural_shields_key_yields_one_per_entry(tmp_path: Path) -> None:
    (tmp_path / "shield.yml").write_text(
        dedent("""\
        shields:
          - name: alpha
            template: true
          - name: beta
        """)
    )
    _yml_path, entries, diags = _shield_yml_entries(str(tmp_path))
    assert diags == []
    assert [(name, promotable) for name, _v, promotable in entries] == [
        ("alpha", True),
        ("beta", False),
    ]


def test_shield_yml_entries_a_shields_block_that_is_not_a_list_is_reported(tmp_path: Path) -> None:
    """The one-dash-short typo. It must not be a SILENT drop: the folder
    loses every name it meant to declare, and nothing downstream can
    attribute that loss to this file (an instance referencing the shield
    would blame itself instead)."""
    (tmp_path / "shield.yml").write_text(
        dedent("""\
        shields:
          name: alpha
          template: true
        """)
    )
    _yml_path, entries, diags = _shield_yml_entries(str(tmp_path))
    assert entries == []
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"
    assert "'shields' must be a list" in diags[0].message


def test_shield_yml_entries_a_shields_entry_missing_name_is_dropped(tmp_path: Path) -> None:
    (tmp_path / "shield.yml").write_text(
        dedent("""\
        shields:
          - template: true
          - name: beta
        """)
    )
    _yml_path, entries, diags = _shield_yml_entries(str(tmp_path))
    assert [name for name, _v, _p in entries] == ["beta"]
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"
    assert "required key 'name' is missing" in diags[0].message


def test_shield_yml_entries_a_repeated_name_in_one_list_is_dropped(tmp_path: Path) -> None:
    (tmp_path / "shield.yml").write_text(
        dedent("""\
        shields:
          - name: alpha
          - name: alpha
            template: true
        """)
    )
    _yml_path, entries, diags = _shield_yml_entries(str(tmp_path))
    assert [(name, promotable) for name, _v, promotable in entries] == [("alpha", False)]
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"
    assert "'alpha' is declared more than once" in diags[0].message


# ------------------------------------------ per-entry revisions:, owner-named
#
# `load_shield_library`'s scan calls parse_legacy_revision_decl directly on
# each promotable entry's own Val, owner=f"shield '{name}'" -- correct
# even when the folder basename and the declared name differ. These
# prove the ENTRY-level Val
# `_shield_yml_entries` hands back carries what that call needs, with a
# folder name distinct from the declared name so a regression back to
# `os.path.basename(shield_dir)` would fail here even though it kept the
# pre-plurality fixtures (folder name == declared name) green.


def test_entry_revisions_bad_default_is_blamed_on_the_declared_name(tmp_path: Path) -> None:
    shield_dir = tmp_path / "folder_name"
    shield_dir.mkdir()
    (shield_dir / "shield.yml").write_text(
        dedent("""\
        shield:
          name: declared_name
          template: true
          revisions:
            default: "3"
            list: ["1", "2"]
        """)
    )
    _yml_path, entries, entry_diags = _shield_yml_entries(str(shield_dir))
    assert entry_diags == []
    [(name, entry_v, _promotable)] = entries
    decl, diags = parse_legacy_revision_decl(entry_v, "revisions", owner=f"shield '{name}'")
    assert decl is None
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"
    assert "shield 'declared_name' revisions:" in diags[0].message
    assert "folder_name" not in diags[0].message


def test_entry_revisions_parses_from_a_plural_list_entry(tmp_path: Path) -> None:
    shield_dir = tmp_path / "plural_folder"
    shield_dir.mkdir()
    (shield_dir / "shield.yml").write_text(
        dedent("""\
        shields:
          - name: alpha
            template: true
            revisions:
              default: "1"
              list: ["1", "2"]
          - name: beta
            template: true
        """)
    )
    _yml_path, entries, entry_diags = _shield_yml_entries(str(shield_dir))
    assert entry_diags == []
    by_name = {name: entry_v for name, entry_v, _p in entries}
    decl_alpha, diags_alpha = parse_legacy_revision_decl(
        by_name["alpha"], "revisions", owner="shield 'alpha'"
    )
    assert diags_alpha == []
    assert decl_alpha == AxisDecl(values=["1", "2"], default="1")
    decl_beta, diags_beta = parse_legacy_revision_decl(
        by_name["beta"], "revisions", owner="shield 'beta'"
    )
    assert diags_beta == []
    assert decl_beta is None


# ------------------------------------------------------- resolve(): failure shapes


def test_resolve_unknown_shield_is_lang_instance_shield() -> None:
    lib = ShieldLibrary(shields={}, axes={}, pending={}, ymls={}, types={}, workdir="/nonexistent")
    shield, diags, deps = lib.resolve("ghost", "instance 'x'", _SRC)
    assert shield is None
    assert len(diags) == 1
    assert diags[0].code == "lang-instance-shield"
    assert deps == frozenset()


def test_resolve_a_declared_default_axis_shield_returns_the_cached_value() -> None:
    """The general (non-@rev, already-cached) path never needs
    `_resolve_revision`/parse_tu at all."""
    sh = _shield("plain")
    lib = ShieldLibrary(
        shields={"plain": sh},
        axes={"plain": None},
        pending={},
        ymls={},
        types={},
        workdir="/nonexistent",
    )
    shield, diags, _deps = lib.resolve("plain", "instance 'x'", _SRC)
    assert shield is sh
    assert diags == []


def test_resolve_bare_name_with_no_declared_axis_and_a_memoized_failure_returns_none() -> None:
    """A shield with NO declared axis whose base parse already failed on
    an earlier reference (recorded in `failed`) resolves quietly on a
    later one -- no re-parse (`pending` is deliberately left EMPTY
    here, so a re-parse attempt would KeyError), no re-echo."""
    lib = ShieldLibrary(
        shields={},
        axes={"plain": None},
        pending={},
        ymls={},
        types={},
        workdir="/nonexistent",
        failed={"plain"},
    )
    shield, diags, _deps = lib.resolve("plain", "instance 'x'", _SRC)
    assert shield is None
    assert diags == []


def test_resolve_at_rev_against_undeclared_axis() -> None:
    lib = ShieldLibrary(
        shields={}, axes={"fx": None}, pending={}, ymls={}, types={}, workdir="/nonexistent"
    )
    shield, diags, _deps = lib.resolve("fx@1", "instance 'x'", _SRC)
    assert shield is None
    assert diags[0].code == "lang-rev"
    assert "declares no revisions: at all" in diags[0].message


def test_resolve_at_rev_not_a_declared_member() -> None:
    """A shield's own revision axis has NO format (its declaration keeps
    the pre-hwmv2 shape permanently, see parse_legacy_revision_decl), so
    resolve_axis_selection runs no hwmv2 machinery here: '99' is rejected
    outright, never nearest-lower-matched down to '2'."""
    decl = AxisDecl(values=["1", "2"], default="1")
    lib = ShieldLibrary(
        shields={}, axes={"fx": decl}, pending={}, ymls={}, types={}, workdir="/nonexistent"
    )
    shield, diags, _deps = lib.resolve("fx@99", "instance 'x'", _SRC)
    assert shield is None
    assert diags[0].code == "lang-rev"
    # Full text, same reasoning as the no-default case below: the owner
    # wording is a parameter this call site passes to the shared decision.
    assert diags[0].message == (
        "shield 'fx': revision '99' is not declared -- known revisions: 1, 2"
    )


def test_resolve_at_rev_nearest_lower_match_is_owner_agnostic_in_the_shared_function() -> None:
    """A shield's revisions: block cannot carry format: today: the
    pinned zephyr tree's own schema restricts it to
    {default:, list: []} -- Zephyr's own list_shields.py enforces it on
    every configure, whether or not the shield is used
    (parse_legacy_revision_decl's own docstring has the measured
    detail).

    resolve_axis_selection itself is unaffected -- it reads decl.format,
    never owner_kind, so if a shield decl EVER carried one, this exact
    '99' -> '2' nearest-lower resolution would already work, reached
    through ShieldLibrary.resolve exactly as shown here. This proves the
    mechanism is ready; it does not claim shields exercise it today."""
    decl = AxisDecl(values=["1", "2"], default="1", format="number")
    cached = _shield("fx")
    lib = ShieldLibrary(
        shields={"fx@2": cached},
        axes={"fx": decl},
        pending={},
        ymls={},
        types={},
        workdir="/nonexistent",
    )
    shield, diags, _deps = lib.resolve("fx@99", "instance 'x'", _SRC)
    assert shield is cached
    assert diags == []


def test_resolve_bare_name_with_a_declared_axis_but_no_default() -> None:
    """Asserts the FULL message, not a substring, because this shape is
    the one with no reject golden behind it: the other two shield shapes
    are frozen by shield-undeclared-revision/ and
    shield-no-revisions-declared/, so a wording regression there fails
    the frozen suite, but a regression HERE would reach nothing else.

    Naming the owner ("shield 'fx'", "this shield") is the load-bearing
    part: resolution is `loader.axes.resolve_axis_selection`'s shared
    decision now, and the owner wording is a PARAMETER this call site
    passes. A substring like "no default revision" survives that
    parameter being wrong -- it appears verbatim in the rig phrasing
    too -- so it would pass while this call site emitted a diagnostic
    calling the shield a rig."""
    decl = AxisDecl(values=["1", "2"], default=None)
    lib = ShieldLibrary(
        shields={}, axes={"fx": decl}, pending={}, ymls={}, types={}, workdir="/nonexistent"
    )
    shield, diags, _deps = lib.resolve("fx", "instance 'x'", _SRC)
    assert shield is None
    assert diags[0].code == "lang-rev"
    assert diags[0].message == (
        "shield 'fx': no revision selected, and this shield declares no "
        "default revision -- choose one of: 1, 2"
    )


def test_resolve_memoizes_a_cached_revision_without_reparsing() -> None:
    """Lazy-parse memoization: a revision already resolved once (present
    in `shields` under its "<name>@<rev>" key) is returned AS-IS on a
    second call -- the cache-hit branch inside `_resolve_revision`, which
    never touches parse_tu/cpp."""
    decl = AxisDecl(values=["1", "2"], default="1")
    cached = _shield("fx")
    lib = ShieldLibrary(
        shields={"fx@2": cached},
        axes={"fx": decl},
        pending={},
        ymls={},
        types={},
        workdir="/nonexistent",
    )
    shield, diags, deps = lib.resolve("fx@2", "instance 'x'", _SRC)
    assert shield is cached
    assert diags == []
    assert deps == frozenset()


def test_resolve_records_the_shield_yml_dependency_when_referenced() -> None:
    """A shield's own shield.yml becomes load-bearing (dependency data)
    only once something actually NAMES it -- recorded at resolve() time,
    never at scan time."""
    cached = _shield("fx")
    lib = ShieldLibrary(
        shields={"fx": cached},
        axes={"fx": None},
        pending={},
        ymls={"fx": "/some/fx/shield.yml"},
        types={},
        workdir="/nonexistent",
    )
    shield, _diags, deps = lib.resolve("fx", "instance 'x'", _SRC)
    assert shield is cached
    assert deps == frozenset({"/some/fx/shield.yml"})


def test_resolve_no_dependency_when_the_shield_has_no_yml() -> None:
    cached = _shield("fx")
    lib = ShieldLibrary(
        shields={"fx": cached},
        axes={"fx": None},
        pending={},
        ymls={},
        types={},
        workdir="/nonexistent",
    )
    _, _, deps = lib.resolve("fx", "instance 'x'", _SRC)
    assert deps == frozenset()


# ---------------------------------------------- resolve(): axis-less lazy parse
#
# `_parse_shield_template` is the ONE seam that reaches cpp (dtsio.parse_tu);
# every test below monkeypatches it to a canned stub so resolve()'s CONTROL
# FLOW around it -- when it is called, how its result is memoized, what deps
# compose around it -- stays verifiable without a subprocess, the same
# seam-substitution idiom test_board_resolve.py uses for project.load_board.


def _fake_parse_template(
    shield: Shield | None,
    diags: list[Diagnostic],
    deps: Deps,
    calls: list[str],
):
    """A stand-in for `_parse_shield_template`: records every name it was
    called with (`calls`) and returns a fixed (shield, diags, deps)
    regardless of arguments -- enough to prove resolve() calls it AT MOST
    ONCE per name, never enough to need a real translation unit."""

    def _fake(
        name: str,
        template: str,
        includes: list[str],
        dts_name: str,
        workdir: str,
        include_dirs: list[str] | None,
        types: dict[str, ConnectorType],
        yml_path: str | None,
    ) -> tuple[Shield | None, list[Diagnostic], Deps]:
        calls.append(name)
        return shield, diags, deps

    return _fake


def test_axis_less_shield_parses_on_first_reference_and_caches_after(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The axis-less lazy-parse path, generalised from `_resolve_revision`'s
    own `self.shields[name]` memoization: resolve() must call the shared
    parse helper on the FIRST reference and reuse the cached Shield on a
    second, never reparsing. Negative control: an unmemoized
    implementation would call the helper (and therefore parse_tu/cpp) a
    second time too, doubling the call count this asserts is 1."""
    calls: list[str] = []
    parsed = _shield("fx")
    monkeypatch.setattr(
        "rigc.loader.library._parse_shield_template",
        _fake_parse_template(parsed, [], frozenset({"/some/fx/fx.shield"}), calls),
    )
    pending = _Pending("/some/fx", "/some/fx/fx.shield", None)
    lib = ShieldLibrary(
        shields={},
        axes={"fx": None},
        pending={"fx": pending},
        ymls={},
        types={},
        workdir="/nonexistent",
    )

    shield1, diags1, deps1 = lib.resolve("fx", "instance 'a'", _SRC)
    shield2, diags2, deps2 = lib.resolve("fx", "instance 'b'", _SRC)

    assert shield1 is parsed and shield2 is parsed
    assert diags1 == [] and diags2 == []
    assert calls == ["fx"]
    assert deps1 == frozenset({"/some/fx/fx.shield"})
    assert deps2 == frozenset()  # cache hit: no parse, no dep recomputed


def test_axis_less_shield_base_parse_failure_is_memoized_and_reports_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Naive laziness would re-run the parse (and
    re-emit the same diagnostic) on every reference to a broken template;
    this memoizes the failure the first time and answers silently after.
    Negative control: an implementation that memoizes only SUCCESSFUL
    parses (mirroring `_resolve_revision`'s own cache, which has nothing
    for a failure) calls the helper -- and reports -- twice."""
    calls: list[str] = []
    failure = [error("lang-shield-name", "boom", (SourceRef("/some/fx/fx.shield", 1),))]
    monkeypatch.setattr(
        "rigc.loader.library._parse_shield_template",
        _fake_parse_template(None, failure, frozenset(), calls),
    )
    pending = _Pending("/some/fx", "/some/fx/fx.shield", None)
    lib = ShieldLibrary(
        shields={},
        axes={"fx": None},
        pending={"fx": pending},
        ymls={},
        types={},
        workdir="/nonexistent",
    )

    shield1, diags1, _ = lib.resolve("fx", "instance 'a'", _SRC)
    shield2, diags2, _ = lib.resolve("fx", "instance 'b'", _SRC)

    assert shield1 is None and shield2 is None
    assert len(diags1) == 1 and diags1[0].code == "lang-shield-name"
    assert diags2 == []
    assert calls == ["fx"]
    assert lib.failed == {"fx"}


def test_resolved_axis_less_shield_deps_include_its_own_base_file(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The base template becomes a dependency once resolve()
    actually parses it -- touched explicitly by resolve(), not left to
    cpp-linemarker recovery (`source_files`) alone, because a template
    that defines no node at all would otherwise vanish from RIG_DEPENDS.
    Negative control: relying only on the parse helper's own returned
    deps would miss this -- the fake helper below returns none of its
    own, exactly the shape a node-less template's real parse would too."""
    monkeypatch.setattr(
        "rigc.loader.library._parse_shield_template",
        _fake_parse_template(_shield("fx"), [], frozenset(), []),
    )
    pending = _Pending("/some/fx", "/some/fx/fx.shield", None)
    lib = ShieldLibrary(
        shields={},
        axes={"fx": None},
        pending={"fx": pending},
        ymls={},
        types={},
        workdir="/nonexistent",
    )
    _, _, deps = lib.resolve("fx", "instance 'a'", _SRC)
    assert deps == frozenset({"/some/fx/fx.shield"})


# ------------------------------- resolve(): hwmv2 mechanism, owner-agnostic
#
# A real shield.yml can never carry format: today (the pinned zephyr
# tree's own carried schema forbids it, see parse_legacy_revision_decl's
# docstring) -- so the two tests below construct a hwmv2-shaped AxisDecl
# by hand and seed it directly into a synthetic ShieldLibrary, bypassing
# _load_shield_revisions entirely. They prove `_resolve_revision` and its
# stem/memoization-key construction have NO owner-kind branching of their
# own: whatever resolve_axis_selection resolves to is what gets used,
# rig or shield alike. The MACHINERY already supports shields getting
# hwmv2 semantics too, pending only the zephyr-side schema change that
# would let a real shield.yml reach it.


def test_resolve_shield_side_nearest_lower_stem_follows_the_resolved_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The RESOLVED value (not the requested one) constructs a shield
    revision's own template dts
    name, .shield/.conf lookups and memoization key -- a nearest-lower
    match must never look for the REQUESTED id's own fragment files. A
    requested '1.5' zero-appends to '1.5.0' (major.minor.patch's own
    loose typing) and, undeclared, resolves DOWN to '1.0.0' -- only a
    'fx_1_0_0...'-shaped lookup is ever attempted, never 'fx_1_5...'."""
    decl = AxisDecl(values=["1.0.0", "2.0.0"], default="1.0.0", format="major.minor.patch")
    calls: list[str] = []

    def _fake(
        name: str,
        template: str,
        includes: list[str],
        dts_name: str,
        workdir: str,
        include_dirs: list[str] | None,
        types: dict[str, ConnectorType],
        yml_path: str | None,
    ) -> tuple[Shield | None, list[Diagnostic], Deps]:
        calls.append(dts_name)
        return _shield(name), [], frozenset()

    monkeypatch.setattr("rigc.loader.library._parse_shield_template", _fake)
    pending = _Pending("/some/fx", "/some/fx/fx.shield", decl)
    lib = ShieldLibrary(
        shields={},
        axes={"fx": decl},
        pending={"fx": pending},
        ymls={},
        types={},
        workdir="/nonexistent",
    )

    shield, diags, _deps = lib.resolve("fx@1.5", "instance 'x'", _SRC)

    assert diags == []
    assert shield is not None
    assert shield.revision == "1.0.0"
    assert shield.revision_requested == "1.5"
    assert calls == ["shield-fx-1_0_0.dts"]
    assert "fx@1.0.0" in lib.shields
    assert "fx@1.5" not in lib.shields


def test_resolve_nearest_lower_memoizes_under_the_resolved_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """'@1.5' and '@1' both resolve to the SAME declared revision here
    -- they must parse the template only ONCE, memoized under the
    RESOLVED key, or a naive requested-keyed cache would parse it
    (and re-run cpp) twice."""
    decl = AxisDecl(values=["1.0.0", "2.0.0"], default="1.0.0", format="major.minor.patch")
    calls: list[str] = []

    def _fake(
        name: str,
        template: str,
        includes: list[str],
        dts_name: str,
        workdir: str,
        include_dirs: list[str] | None,
        types: dict[str, ConnectorType],
        yml_path: str | None,
    ) -> tuple[Shield | None, list[Diagnostic], Deps]:
        calls.append(dts_name)
        return _shield(name), [], frozenset()

    monkeypatch.setattr("rigc.loader.library._parse_shield_template", _fake)
    pending = _Pending("/some/fx", "/some/fx/fx.shield", decl)
    lib = ShieldLibrary(
        shields={},
        axes={"fx": decl},
        pending={"fx": pending},
        ymls={},
        types={},
        workdir="/nonexistent",
    )

    shield1, diags1, _ = lib.resolve("fx@1.5", "instance 'a'", _SRC)
    shield2, diags2, _ = lib.resolve("fx@1", "instance 'b'", _SRC)

    assert diags1 == [] and diags2 == []
    assert shield1 is shield2
    assert calls == ["shield-fx-1_0_0.dts"]


# ------------------------------------------------------- load_shield_library scan


def _declared_shield_folder(root: Path, name: str, revisions: str = "1") -> None:
    """A `template: true` shield folder carrying a shield.yml -- scanned
    but deferred to `pending`, so `load_shield_library` never calls
    parse_tu/cpp for it (keeps this whole test subprocess-free). Its own
    `revision:` block is deliberately the WRONG key (singular, no such
    axis exists on a shield) -- these tests exercise discovery BREADTH,
    never a real revisions: axis, so `parse_legacy_revision_decl` reads
    no axis here regardless (`decl is None` for every folder this
    builds), same as before plurality."""
    d = root / name
    d.mkdir(parents=True)
    (d / f"{name}.shield").write_text(f"/* fixture: {name} */\n")
    (d / "shield.yml").write_text(
        f"shield:\n  name: {name}\n  template: true\n  revision:\n"
        f"    format: number\n    default: \"{revisions}\"\n"
        f"    revisions:\n      - name: \"{revisions}\"\n"
    )


def test_scan_discovers_exactly_basename_dot_shield(tmp_path: Path) -> None:
    root = tmp_path / "shields"
    _declared_shield_folder(root, "fx_a")
    _declared_shield_folder(root, "fx_b")
    # A legacy Kconfig.shield fragment -- must NOT be mis-globbed as a
    # shield template (it ends in the literal substring ".shield").
    (root / "fx_a" / "Kconfig.shield").write_text(
        dedent("""\
        # not a shield template
        """)
    )
    lib, diags, _deps = load_shield_library(
        str(tmp_path / "work"), shield_dirs=[str(root)], types={}
    )
    assert diags == []
    assert set(lib.pending) == {"fx_a", "fx_b"}
    assert lib.shields == {}  # both deferred (declared axis), never eager-parsed


def test_scan_skips_a_folder_with_no_matching_dot_shield_file(tmp_path: Path) -> None:
    root = tmp_path / "shields"
    root.mkdir()
    stray = root / "not_a_shield"
    stray.mkdir()
    (stray / "Kconfig.shield").write_text(
        dedent("""\
        # no not_a_shield.shield beside it
        """)
    )
    lib, diags, _deps = load_shield_library(
        str(tmp_path / "work"), shield_dirs=[str(root)], types={}
    )
    assert diags == []
    assert lib.pending == {}
    assert lib.shields == {}


def test_scan_unions_multiple_shield_dirs(tmp_path: Path) -> None:
    root_a = tmp_path / "a"
    root_b = tmp_path / "b"
    _declared_shield_folder(root_a, "from_a")
    _declared_shield_folder(root_b, "from_b")
    lib, _diags, _deps = load_shield_library(
        str(tmp_path / "work"), shield_dirs=[str(root_a), str(root_b)], types={}
    )
    assert set(lib.pending) == {"from_a", "from_b"}


def _axisless_shield_folder(root: Path, name: str) -> None:
    """An axis-less shield folder (no shield.yml at all) -- deliberately
    GARBAGE, non-DTS `.shield` content. Discovery never reads the
    template at all, only probes its presence, so a folder built with
    this helper proves that by construction -- any test using it that
    doesn't raise is already evidence the scan stayed lazy."""
    d = root / name
    d.mkdir(parents=True)
    (d / f"{name}.shield").write_text("not a valid .dts document at all\n")


def test_scan_is_eager_and_complete_for_axis_less_shields_too(tmp_path: Path) -> None:
    """Discovery breadth: every discovered shield,
    axis-less or revisioned, lands in BOTH `axes` (the known-shields
    census) and `pending` -- none of it parsed. Negative control: a
    lazy-discovery implementation (the folder walk itself deferred to
    first reference) would leave `axes`/`pending` empty or partial here,
    since nothing in this scan ever references any of the three shields."""
    root = tmp_path / "shields"
    _axisless_shield_folder(root, "fx_a")
    _axisless_shield_folder(root, "fx_b")
    _declared_shield_folder(root, "fx_c")
    lib, diags, _deps = load_shield_library(
        str(tmp_path / "work"), shield_dirs=[str(root)], types={}
    )
    assert diags == []
    assert set(lib.axes) == {"fx_a", "fx_b", "fx_c"}
    assert lib.axes["fx_a"] is None and lib.axes["fx_b"] is None
    assert set(lib.pending) == {"fx_a", "fx_b", "fx_c"}
    assert lib.shields == {}


def test_scan_parses_nothing_at_all(tmp_path: Path) -> None:
    """NOTHING reaches cpp at scan time, axis-less or not -- proven here
    by asserting no translation unit was ever written into workdir.
    Negative control: an eager implementation that calls parse_tu for
    every axis-less shield would both create workdir and write a TU
    into it -- and, given this fixture's garbage content, raise
    LoadError before this assertion even runs."""
    root = tmp_path / "shields"
    _axisless_shield_folder(root, "fx_a")
    workdir = tmp_path / "work"
    load_shield_library(str(workdir), shield_dirs=[str(root)], types={})
    assert not workdir.exists()


def test_unreferenced_broken_axis_less_template_is_silent(tmp_path: Path) -> None:
    """An axis-less shield whose template cannot even parse never
    poisons the scan and produces no diagnostic at all, as long as
    nothing references it -- discovery reads shield.yml (absent here),
    never the template. Negative control: an implementation that calls
    parse_tu unconditionally for every axis-less shield would raise
    LoadError out of load_shield_library for this fixture's garbage
    content."""
    root = tmp_path / "shields"
    _axisless_shield_folder(root, "broken")
    lib, diags, _deps = load_shield_library(
        str(tmp_path / "work"), shield_dirs=[str(root)], types={}
    )
    assert diags == []
    assert lib.shields == {}


def test_discovery_deps_exclude_shield_templates(tmp_path: Path) -> None:
    """A discovered `.shield` template is not a dependency by
    itself -- shield.yml is the only file discovery reads, and even that
    is not recorded as a dep until resolve() is reached
    (test_resolve_records_the_shield_yml_dependency_when_referenced,
    above). Negative control: a discovery-time `touch(base_file)` would
    put this folder's own `fx_a.shield` path into `deps` regardless of
    whether anything ever references it."""
    root = tmp_path / "shields"
    _axisless_shield_folder(root, "fx_a")
    _, _, deps = load_shield_library(str(tmp_path / "work"), shield_dirs=[str(root)], types={})
    assert deps == frozenset()


def test_unknown_shield_reference_still_lists_every_discovered_shield(tmp_path: Path) -> None:
    """The known-shields census a
    `lang-instance-shield` diagnostic prints must name every DISCOVERED
    shield regardless of whether any of them has been parsed, resolved,
    or has a memoized failure -- `axes` is the census, never
    `shields`/`pending`/`failed`. Negative control: an implementation
    that derived the census from resolved/parsed shields instead of
    discovery's own `axes` would print an empty (or partial) list here,
    since none of these three shields has ever been referenced -- and
    would print a PARTIAL one even after the states below are seeded."""
    root = tmp_path / "shields"
    _axisless_shield_folder(root, "fx_a")
    _axisless_shield_folder(root, "fx_b")
    _declared_shield_folder(root, "fx_c")
    lib, _, _ = load_shield_library(str(tmp_path / "work"), shield_dirs=[str(root)], types={})
    # Seed the three post-discovery states the census must survive, so the
    # claim above is exercised rather than merely asserted: one parsed, one
    # with a memoized parse failure, one still untouched.
    lib.shields["fx_a"] = _shield("fx_a")
    lib.failed.add("fx_b")

    _, diags, _ = lib.resolve("ghost", "instance 'x'", _SRC)

    assert diags[0].code == "lang-instance-shield"
    assert "fx_a, fx_b, fx_c" in diags[0].message


# NOTE: a malformed shield.yml revisions: block (parse_legacy_revision_decl
# returning decl=None from a BAD declaration, tested directly above via
# _shield_yml_entries's own entry Val) makes `load_shield_library`'s scan
# treat the shield as axis-less -- exactly
# the golden fixture `shield-bad-revisions-block`'s own shape -- and now,
# same as any other axis-less shield, defers its base template's parse to
# `resolve()`'s first reference rather than eagerly parsing it during the
# scan. That parse calls dtsio.parse_tu (cpp, a real subprocess), so the
# scenario stays integration-only (covered already, through the frozen
# suite's front door) rather than getting a second unit test here that
# would need a real `.shield` DTS body and a real cpp call to reach.
