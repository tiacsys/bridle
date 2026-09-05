# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: loader.axes -- hwmv2-shaped qualifier axes for variant/revision
declarations.

Covers: variant declaration parsing (the mapping-entry shape only
`variants:` takes), revision declaration parsing (hwmv2's own
format:/default:/exact:/revisions: shape), axis resolution's three
failure shapes (undeclared axis / not-a-member / no-default) plus
hwmv2's own per-format id validation, zero-append and nearest-lower
match, revision normalization, and the widened fragment-stem collision
enumeration. Wording stays out of these tests where a frozen golden
already owns it (the goldens assert the target fixtures' exact message
text); here the SHAPE -- values, defaults, format/exact, which
diagnostic code fires -- is what must survive a rewrite. The
`resolve_axis_selection` section below is the one place that DOES assert
full message text (see its own header comment).
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from rigc.diag import SourceRef
from rigc.loader.axes import (
    check_axis_collision,
    normalize_revision,
    parse_revision_decl,
    parse_variant_decl,
    resolve_axis,
    resolve_axis_selection,
    revision_fragment_name,
    variant_fragment_name,
)
from rigc.loader.documents import Val, parse_marked
from rigc.model import AxisDecl

_SRC = SourceRef("synthetic", 1, "rig")


def _rig(tmp_path: Path, text: str) -> Val:
    path = tmp_path / "rig.yml"
    path.write_text(dedent(text))
    doc = parse_marked(str(path))
    return doc.value["rig"]


# -------------------------------------------------------- normalization


def test_normalize_revision_replaces_dots_with_underscores() -> None:
    assert normalize_revision("1.2") == "1_2"


def test_normalize_revision_is_a_no_op_without_dots() -> None:
    assert normalize_revision("2") == "2"


def test_fragment_stem_is_name_underscore_value() -> None:
    assert variant_fragment_name("pilot", "b") == "pilot_b.yml"
    assert revision_fragment_name("pilot", "2") == "pilot_2.yml"


def test_revision_fragment_stem_normalizes_dots() -> None:
    """hwmv2's own normalization: 1.2 -> 1_2 in the CONSTRUCTED filename
    -- callers pass the RESOLVED value here, never the raw requested
    one."""
    assert revision_fragment_name("pilot", "1.2") == "pilot_1_2.yml"


def test_variant_fragment_stem_is_never_normalized() -> None:
    """Normalization is a REVISION concept: a variant legally named with
    a dot keeps its raw stem -- normalizing it would make the loader look
    for a file that doesn't exist and the collision enumerator never
    construct."""
    assert variant_fragment_name("pilot", "b.1") == "pilot_b.1.yml"


# ------------------------------------------------------ variants: declaration


def test_absent_variants_key_declares_nothing(tmp_path: Path) -> None:
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
        """,
    )
    decl, diags = parse_variant_decl(rig_v, "variants")
    assert decl is None
    assert diags == []


def test_bare_scalar_variant_list_declares_values_with_no_metadata(tmp_path: Path) -> None:
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          variants:
            default: a
            list: [a, b]
        """,
    )
    decl, diags = parse_variant_decl(rig_v, "variants")
    assert diags == []
    assert decl == AxisDecl(values=["a", "b"], default="a")


def test_variant_no_default_leaves_default_none(tmp_path: Path) -> None:
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          variants:
            list: [a, b]
        """,
    )
    decl, diags = parse_variant_decl(rig_v, "variants")
    assert diags == []
    assert decl is not None
    assert decl.default is None
    assert decl.values == ["a", "b"]


def test_variant_default_not_a_member_is_rejected(tmp_path: Path) -> None:
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          variants:
            default: c
            list: [a, b]
        """,
    )
    decl, diags = parse_variant_decl(rig_v, "variants")
    assert decl is None
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"


def test_variant_mapping_entry_missing_name_is_rejected(tmp_path: Path) -> None:
    """The malformed entry is skipped, not silently accepted -- the
    well-formed remainder ('b') still constitutes a valid axis."""
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          variants:
            list:
              - board: b/s/rig
              - b
        """,
    )
    decl, diags = parse_variant_decl(rig_v, "variants")
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"
    assert decl is not None
    assert decl.values == ["b"]


def test_variant_empty_list_is_rejected(tmp_path: Path) -> None:
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          variants:
            list: []
        """,
    )
    decl, diags = parse_variant_decl(rig_v, "variants")
    assert decl is None
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"
    assert diags[0].message == "rig variants: 'list' must be a non-empty list"


def test_variant_mapping_entry_board_and_sockets_are_silently_ignored(tmp_path: Path) -> None:
    """rig.yml's grammar has no board:/sockets: keys -- a variant entry
    may still carry them (nothing rejects an unrecognized key here, same
    as anywhere else in this grammar), but only name: is read, and they
    reach nothing: AxisDecl has no field either one could land in. The
    assertion is therefore that the entry parses to its NAME alone, with
    no diagnostic -- ignored, neither rejected nor absorbed."""
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          variants:
            default: a
            list:
              - name: a
                board: b1/s/rig
                sockets: {ard: nucleo_ard}
              - b
        """,
    )
    decl, diags = parse_variant_decl(rig_v, "variants")
    assert diags == []
    assert decl is not None
    assert decl.values == ["a", "b"]


# ------------------------------------------------------ revision: declaration


def test_absent_revision_key_declares_nothing(tmp_path: Path) -> None:
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
        """,
    )
    decl, diags = parse_revision_decl(rig_v, "revision")
    assert decl is None
    assert diags == []


def test_revision_mapping_list_declares_values_and_format(tmp_path: Path) -> None:
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          revision:
            format: number
            default: "1"
            revisions:
              - name: "1"
              - name: "2"
        """,
    )
    decl, diags = parse_revision_decl(rig_v, "revision")
    assert diags == []
    assert decl == AxisDecl(values=["1", "2"], default="1", format="number")


def test_revision_no_default_leaves_default_none(tmp_path: Path) -> None:
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          revision:
            format: number
            revisions:
              - name: "1"
              - name: "2"
        """,
    )
    decl, diags = parse_revision_decl(rig_v, "revision")
    assert diags == []
    assert decl is not None
    assert decl.default is None
    assert decl.values == ["1", "2"]


def test_revision_format_is_required(tmp_path: Path) -> None:
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          revision:
            revisions:
              - name: "1"
        """,
    )
    decl, diags = parse_revision_decl(rig_v, "revision")
    assert decl is None
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"
    assert "'format' is required" in diags[0].message


def test_revision_unknown_format_is_rejected(tmp_path: Path) -> None:
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          revision:
            format: hex
            revisions:
              - name: "1"
        """,
    )
    decl, diags = parse_revision_decl(rig_v, "revision")
    assert decl is None
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"


def test_revision_custom_format_is_a_legal_declaration(tmp_path: Path) -> None:
    """format: custom is valid upstream YAML -- parse_revision_decl
    accepts it; only resolve_axis_selection rejects it (once the axis is
    actually used), see the resolution tests below."""
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          revision:
            format: custom
            revisions:
              - name: "anything"
        """,
    )
    decl, diags = parse_revision_decl(rig_v, "revision")
    assert diags == []
    assert decl is not None
    assert decl.format == "custom"


def test_revision_default_not_a_member_is_rejected(tmp_path: Path) -> None:
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          revision:
            format: number
            default: "3"
            revisions:
              - name: "1"
              - name: "2"
        """,
    )
    decl, diags = parse_revision_decl(rig_v, "revision")
    assert decl is None
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"


def test_revision_empty_list_is_rejected(tmp_path: Path) -> None:
    """Asserts the message text too, not just the code -- deliberately,
    against this module's own general policy above: a code-only
    assertion would let this wording drift unnoticed. The golden
    fixture empty-revisions-list pins the same message."""
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          revision:
            format: number
            revisions: []
        """,
    )
    decl, diags = parse_revision_decl(rig_v, "revision")
    assert decl is None
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"
    assert diags[0].message == "rig revision: 'revisions' must be a non-empty list"


def test_revision_bare_scalar_entry_is_rejected(tmp_path: Path) -> None:
    """Upstream's shape is mapping entries with name: -- a bare scalar
    entry is rejected, per entry, with the well-formed remainder still
    constituting a valid (partial) axis."""
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          revision:
            format: number
            revisions:
              - "1"
              - name: "2"
        """,
    )
    decl, diags = parse_revision_decl(rig_v, "revision")
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"
    assert decl is not None
    assert decl.values == ["2"]


def test_revision_mapping_entry_missing_name_is_rejected(tmp_path: Path) -> None:
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          revision:
            format: number
            revisions:
              - full_name: not a name key
              - name: "2"
        """,
    )
    decl, diags = parse_revision_decl(rig_v, "revision")
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"
    assert decl is not None
    assert decl.values == ["2"]


def test_revision_default_must_be_a_quoted_string(tmp_path: Path) -> None:
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          revision:
            format: number
            default: 1
            revisions:
              - name: "1"
        """,
    )
    decl, diags = parse_revision_decl(rig_v, "revision")
    assert decl is None
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"
    assert "'default' must be a quoted string" in diags[0].message


def test_revision_id_must_be_a_string(tmp_path: Path) -> None:
    """A non-string revision id is a lang-schema REJECTION, never a
    coercion -- upstream's own `name: {type: string}`."""
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          revision:
            format: number
            revisions:
              - name: 1
              - name: "2"
        """,
    )
    decl, diags = parse_revision_decl(rig_v, "revision")
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"
    assert decl is not None
    assert decl.values == ["2"]


def test_revision_declared_id_validated_against_its_own_format(tmp_path: Path) -> None:
    """board-schema.yaml's own conditional block validates declared
    names per format independently of any selection -- a declared name
    that does not match format: is a defect of the FILE (lang-schema),
    reported per entry."""
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          revision:
            format: number
            revisions:
              - name: "1"
              - name: "1.5"
        """,
    )
    decl, diags = parse_revision_decl(rig_v, "revision")
    assert len(diags) == 1
    assert diags[0].code == "lang-schema"
    assert decl is not None
    assert decl.values == ["1"]


def test_revision_exact_flag_defaults_false(tmp_path: Path) -> None:
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          revision:
            format: number
            revisions:
              - name: "1"
        """,
    )
    decl, diags = parse_revision_decl(rig_v, "revision")
    assert diags == []
    assert decl is not None
    assert decl.exact is False


def test_revision_exact_flag_parses_true(tmp_path: Path) -> None:
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          revision:
            format: number
            exact: true
            revisions:
              - name: "1"
        """,
    )
    decl, diags = parse_revision_decl(rig_v, "revision")
    assert diags == []
    assert decl is not None
    assert decl.exact is True


def test_revision_letter_format_accepts_declared_letters(tmp_path: Path) -> None:
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          revision:
            format: letter
            default: "A"
            revisions:
              - name: "A"
              - name: "B"
        """,
    )
    decl, diags = parse_revision_decl(rig_v, "revision")
    assert diags == []
    assert decl == AxisDecl(values=["A", "B"], default="A", format="letter")


def test_revision_major_minor_patch_format_accepts_declared_triples(tmp_path: Path) -> None:
    rig_v = _rig(
        tmp_path,
        """\
        rig:
          name: r
          revision:
            format: major.minor.patch
            default: "1.0.0"
            revisions:
              - name: "1.0.0"
              - name: "1.5.0"
        """,
    )
    decl, diags = parse_revision_decl(rig_v, "revision")
    assert diags == []
    assert decl == AxisDecl(values=["1.0.0", "1.5.0"], default="1.0.0", format="major.minor.patch")


# -------------------------------------------------------------- resolution
#
# resolve_axis wraps resolve_axis_selection for a rig's own axis
# (owner_kind="rig"); the SHAPE tests below exercise it directly. Every
# revision AxisDecl constructed here carries format="number" -- a real
# revision decl always does (parse_revision_decl requires it), and
# resolve_axis_selection checks it unconditionally for a revision axis.


def test_resolve_selected_member_of_declared_axis() -> None:
    decl = AxisDecl(values=["1", "2"], default="1", format="number")
    value, diags = resolve_axis("r", "revision", "revision", decl, "2", _SRC)
    assert value == "2"
    assert diags == []


def test_resolve_bare_target_takes_the_declared_default() -> None:
    decl = AxisDecl(values=["1", "2"], default="1", format="number")
    value, diags = resolve_axis("r", "revision", "revision", decl, None, _SRC)
    assert value == "1"
    assert diags == []


def test_resolve_selected_against_undeclared_axis() -> None:
    """Failure shape 1: a selection naming an axis the rig does not
    declare AT ALL -- distinct code path from "not a member"."""
    value, diags = resolve_axis("r", "variant", "variants", None, "x", _SRC)
    assert value is None
    assert len(diags) == 1
    assert diags[0].code == "lang-variant"


def test_resolve_selected_not_a_declared_member() -> None:
    """Failure shape 2: a selection against a declared axis, but not one
    of its values (a VARIANT axis: exact membership only, no
    nearest-lower)."""
    decl = AxisDecl(values=["a", "b"], default="a")
    value, diags = resolve_axis("r", "variant", "variants", decl, "c", _SRC)
    assert value is None
    assert len(diags) == 1
    assert diags[0].code == "lang-variant"


def test_resolve_bare_target_no_default_declared() -> None:
    """Failure shape 3: a bare target against a declared axis with no
    default."""
    decl = AxisDecl(values=["a", "b"])
    value, diags = resolve_axis("r", "variant", "variants", decl, None, _SRC)
    assert value is None
    assert len(diags) == 1
    assert diags[0].code == "lang-variant"


def test_resolve_bare_target_undeclared_axis_is_silent() -> None:
    """No selection + no declaration at all: nothing to resolve, nothing
    to report -- this is the ordinary axis-less rig."""
    value, diags = resolve_axis("r", "revision", "revision", None, None, _SRC)
    assert value is None
    assert diags == []


def test_revision_kind_uses_lang_rev_code() -> None:
    _, diags = resolve_axis("r", "revision", "revision", None, "9", _SRC)
    assert diags[0].code == "lang-rev"


# ---------------------------------------- hwmv2 semantics: per-format, nearest-lower


def test_number_format_rejects_a_malformed_requested_id() -> None:
    decl = AxisDecl(values=["1", "2"], default="1", format="number")
    value, diags = resolve_axis("r", "revision", "revision", decl, "1a", _SRC)
    assert value is None
    assert diags[0].code == "lang-rev"
    assert "does not match this axis's declared format" in diags[0].message


def test_letter_format_rejects_a_malformed_requested_id() -> None:
    decl = AxisDecl(values=["A", "B"], default="A", format="letter")
    value, diags = resolve_axis("r", "revision", "revision", decl, "AA", _SRC)
    assert value is None
    assert diags[0].code == "lang-rev"


def test_letter_format_accepts_a_declared_member() -> None:
    decl = AxisDecl(values=["A", "B"], default="A", format="letter")
    value, diags = resolve_axis("r", "revision", "revision", decl, "B", _SRC)
    assert value == "B"
    assert diags == []


def test_major_minor_patch_rejects_a_malformed_requested_id() -> None:
    decl = AxisDecl(values=["1.0.0"], default="1.0.0", format="major.minor.patch")
    value, diags = resolve_axis("r", "revision", "revision", decl, "1.a.0", _SRC)
    assert value is None
    assert diags[0].code == "lang-rev"


def test_major_minor_patch_zero_appends_before_matching() -> None:
    """hwmv2's own loose typing (extensions.cmake:1092-1103): a requested
    '1' resolves against a declared '1.0.0' -- the zero-append happens to
    the REQUESTED value only; declared names are never rewritten."""
    decl = AxisDecl(values=["1.0.0", "1.5.0"], default="1.0.0", format="major.minor.patch")
    value, diags = resolve_axis("r", "revision", "revision", decl, "1", _SRC)
    assert value == "1.0.0"
    assert diags == []
    value, diags = resolve_axis("r", "revision", "revision", decl, "1.5", _SRC)
    assert value == "1.5.0"
    assert diags == []


def test_nearest_lower_match_resolves_an_undeclared_revision_down() -> None:
    """hwmv2's own nearest-lower match: an undeclared '99' resolves DOWN
    to the highest declared revision <= it -- '2', not a rejection."""
    decl = AxisDecl(values=["1", "2"], default="1", format="number")
    value, diags = resolve_axis("r", "revision", "revision", decl, "99", _SRC)
    assert value == "2"
    assert diags == []


def test_nearest_lower_match_per_format_major_minor_patch() -> None:
    decl = AxisDecl(values=["1.0.0", "2.0.0"], default="1.0.0", format="major.minor.patch")
    value, diags = resolve_axis("r", "revision", "revision", decl, "1.9.9", _SRC)
    assert value == "1.0.0"
    assert diags == []


def test_nearest_lower_match_per_format_letter() -> None:
    decl = AxisDecl(values=["A", "C"], default="A", format="letter")
    value, diags = resolve_axis("r", "revision", "revision", decl, "B", _SRC)
    assert value == "A"
    assert diags == []


def test_nearest_lower_match_with_no_lower_bound_is_rejected() -> None:
    """A requested revision BELOW every declared value has nothing to
    fall back to -- still a genuine rejection, not silently the lowest
    declared value."""
    decl = AxisDecl(values=["1", "2"], default="1", format="number")
    value, diags = resolve_axis("r", "revision", "revision", decl, "0", _SRC)
    assert value is None
    assert diags[0].code == "lang-rev"
    assert "is not declared" in diags[0].message


def test_exact_true_disables_nearest_lower() -> None:
    """exact: true reproduces this axis's pre-hwmv2 behaviour bit for
    bit: an undeclared value is fatal even though nearest-lower would
    otherwise have resolved it."""
    decl = AxisDecl(values=["1", "2"], default="1", format="number", exact=True)
    value, diags = resolve_axis("r", "revision", "revision", decl, "99", _SRC)
    assert value is None
    assert diags[0].code == "lang-rev"
    assert diags[0].message == ("rig 'r': revision '99' is not declared -- known revisions: 1, 2")


def test_exact_true_still_accepts_a_declared_member() -> None:
    decl = AxisDecl(values=["1", "2"], default="1", format="number", exact=True)
    value, diags = resolve_axis("r", "revision", "revision", decl, "2", _SRC)
    assert value == "2"
    assert diags == []


def test_format_custom_is_rejected_loudly() -> None:
    """format: custom is valid YAML (parse_revision_decl accepts it) but
    unimplemented -- rejected the moment this axis is actually used, even
    a bare reference to its own default."""
    decl = AxisDecl(values=["1"], default="1", format="custom")
    value, diags = resolve_axis("r", "revision", "revision", decl, None, _SRC)
    assert value is None
    assert len(diags) == 1
    assert diags[0].code == "lang-rev"
    assert "format: custom is not implemented" in diags[0].message
    assert "letter" in diags[0].message
    assert "number" in diags[0].message
    assert "major.minor.patch" in diags[0].message


def test_format_custom_is_rejected_even_for_a_selected_value() -> None:
    decl = AxisDecl(values=["1"], default="1", format="custom")
    value, diags = resolve_axis("r", "revision", "revision", decl, "1", _SRC)
    assert value is None
    assert diags[0].code == "lang-rev"


# ---------------------------------- shared decision: resolve_axis_selection
#
# `resolve_axis`, above, and `ShieldLibrary.resolve` (loader/library.py) both
# delegate here. The SHAPE is already covered by the tests above (through
# resolve_axis) and by loader/library.py's own tests (through
# ShieldLibrary.resolve) -- what those tests do NOT prove is that the two
# callers get the wording each frozen stderr.txt golden actually pins.
# These assert full message TEXT, for both owner_kind values, so a caller
# that started passing the wrong owner_kind (or the wrong axis_kind/decl_key)
# would fail here even though the shape-only tests elsewhere would still
# pass.


def test_shared_decision_rig_selected_against_undeclared_axis_wording() -> None:
    value, diags = resolve_axis_selection("rig", "r", "revision", "revision", None, "9", _SRC)
    assert value is None
    assert len(diags) == 1
    assert diags[0].code == "lang-rev"
    assert diags[0].message == (
        "rig 'r' names a revision ('9'), but this rig declares no revision: at all"
    )


def test_shared_decision_rig_selected_not_a_member_wording() -> None:
    decl = AxisDecl(values=["1", "2"], default="1", format="number", exact=True)
    value, diags = resolve_axis_selection("rig", "r", "revision", "revision", decl, "9", _SRC)
    assert value is None
    assert diags[0].message == ("rig 'r': revision '9' is not declared -- known revisions: 1, 2")


def test_shared_decision_rig_no_default_wording() -> None:
    decl = AxisDecl(values=["1", "2"], format="number")
    value, diags = resolve_axis_selection("rig", "r", "revision", "revision", decl, None, _SRC)
    assert value is None
    assert diags[0].message == (
        "rig 'r': no revision selected, and this rig declares no default "
        "revision -- choose one of: 1, 2"
    )


def test_shared_decision_rig_variant_wording_pluralizes_variants() -> None:
    """The rig side exercises BOTH axis kinds through the same function --
    'variant'/'variants' must come out, not a 'revision' left over from
    the other caller's defaults."""
    value, diags = resolve_axis_selection("rig", "r", "variant", "variants", None, "x", _SRC)
    assert value is None
    assert diags[0].code == "lang-variant"
    assert diags[0].message == (
        "rig 'r' names a variant ('x'), but this rig declares no variants: at all"
    )


def test_shared_decision_rig_bare_target_takes_default() -> None:
    decl = AxisDecl(values=["1", "2"], default="1", format="number")
    value, diags = resolve_axis_selection("rig", "r", "revision", "revision", decl, None, _SRC)
    assert value == "1"
    assert diags == []


def test_shared_decision_rig_no_axis_no_selection_is_silent() -> None:
    value, diags = resolve_axis_selection("rig", "r", "revision", "revision", None, None, _SRC)
    assert value is None
    assert diags == []


def test_shared_decision_shield_selected_against_undeclared_axis_wording() -> None:
    """decl_key is "revisions" (plural) here, matching the actual YAML
    key ShieldLibrary.resolve passes -- a shield's own axis keeps ITS
    pre-hwmv2 shape permanently (parse_legacy_revision_decl's own
    docstring), unlike a rig's now-singular "revision"."""
    value, diags = resolve_axis_selection("shield", "fx", "revision", "revisions", None, "1", _SRC)
    assert value is None
    assert len(diags) == 1
    assert diags[0].code == "lang-rev"
    assert diags[0].message == (
        "shield 'fx' names a revision ('1'), but this shield declares no revisions: at all"
    )


def test_shared_decision_shield_selected_not_a_member_wording() -> None:
    """No format: a shield's own axis never carries one today, so this
    is the ordinary exact-membership rejection, not a nearest-lower
    near-miss."""
    decl = AxisDecl(values=["1", "2"], default="1")
    value, diags = resolve_axis_selection("shield", "fx", "revision", "revisions", decl, "99", _SRC)
    assert value is None
    assert diags[0].message == (
        "shield 'fx': revision '99' is not declared -- known revisions: 1, 2"
    )


def test_shared_decision_shield_no_default_wording() -> None:
    decl = AxisDecl(values=["1", "2"])
    value, diags = resolve_axis_selection("shield", "fx", "revision", "revisions", decl, None, _SRC)
    assert value is None
    assert diags[0].message == (
        "shield 'fx': no revision selected, and this shield declares no "
        "default revision -- choose one of: 1, 2"
    )


def test_shared_decision_shield_bare_target_takes_default() -> None:
    decl = AxisDecl(values=["1", "2"], default="1")
    value, diags = resolve_axis_selection("shield", "fx", "revision", "revisions", decl, None, _SRC)
    assert value == "1"
    assert diags == []


def test_shared_decision_shield_no_axis_no_selection_is_silent() -> None:
    value, diags = resolve_axis_selection("shield", "fx", "revision", "revisions", None, None, _SRC)
    assert value is None
    assert diags == []


def test_shared_decision_shield_nearest_lower_is_owner_agnostic_in_the_shared_function() -> None:
    """Not current shield.yml behaviour (a real one never carries
    format:, see parse_legacy_revision_decl's own docstring for the
    external constraint) -- this constructs a hypothetical hwmv2-shaped
    shield decl directly and proves resolve_axis_selection itself has no
    owner-kind branching: nearest-lower already works for ANY owner
    whose decl carries format:, rig or shield alike."""
    decl = AxisDecl(values=["1", "2"], default="1", format="number")
    value, diags = resolve_axis_selection("shield", "fx", "revision", "revisions", decl, "99", _SRC)
    assert value == "2"
    assert diags == []


# --------------------------------------------------- fragment-stem collision


def test_no_collision_when_axes_share_no_stem() -> None:
    variants = AxisDecl(values=["a"], default="a")
    revisions = AxisDecl(values=["1"], default="1", format="number")
    assert check_axis_collision("r", variants, revisions, _SRC) == []


def test_single_axis_collision_variant_equals_revision() -> None:
    variants = AxisDecl(values=["2"], default="2")
    revisions = AxisDecl(values=["2"], default="2", format="number")
    diags = check_axis_collision("r", variants, revisions, _SRC)
    assert len(diags) == 1
    assert diags[0].code == "lang-variant"
    assert "r_2" in diags[0].message


def test_combined_stem_collision_variant_plus_revision_vs_another_variant() -> None:
    """variant 'a_2' collides with variant 'a' + revision '2'."""
    variants = AxisDecl(values=["a", "a_2"], default="a")
    revisions = AxisDecl(values=["2"], default="2", format="number")
    diags = check_axis_collision("r", variants, revisions, _SRC)
    assert len(diags) == 1
    assert "r_a_2" in diags[0].message


def test_no_axes_declared_never_collides() -> None:
    assert check_axis_collision("r", None, None, _SRC) == []
