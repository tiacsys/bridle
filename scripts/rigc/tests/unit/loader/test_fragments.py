# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: loader.fragments -- the fragment-presence contributes-nothing
check.

The stable contract: a selected NON-DEFAULT axis value must contribute
something (an existing delta doc, or a cmake-collected overlay/
defconfig); the declared DEFAULT is always exempt. The rule is PURE:
which files exist arrives as a FragmentPresence VALUE (the IO phase
probes), so nothing here touches a filesystem -- no tmp_path, no
fixture files.

A variant's only avenue of contribution is the same fragment-file
avenue a revision has: rig.yml's grammar carries no board/socket
metadata for a variant to differ on.
"""

from __future__ import annotations

from rigc.diag import SourceRef
from rigc.loader.fragments import (
    FragmentPresence,
    check_fragment_presence,
    revision_contribution_names,
    variant_contribution_names,
)
from rigc.model import AxisDecl, Rig

_SRC = SourceRef("synthetic", 1, "rig")


def _rig(
    variant: str | None = None,
    revision: str | None = None,
    variants: AxisDecl | None = None,
    revisions: AxisDecl | None = None,
) -> Rig:
    return Rig(name="r", variant=variant, revision=revision, variants=variants, revisions=revisions)


# --------------------------------------------------------- check_fragment_presence


def test_default_variant_and_revision_are_exempt() -> None:
    variants = AxisDecl(values=["a"], default="a")
    revisions = AxisDecl(values=["1"], default="1")
    rig = _rig(variant="a", revision="1", variants=variants, revisions=revisions)
    diags = check_fragment_presence(rig, _SRC, FragmentPresence())
    assert diags == []


def test_nondefault_variant_with_a_loaded_delta_is_exempt() -> None:
    variants = AxisDecl(values=["a", "b"], default="a")
    rig = _rig(variant="b", variants=variants)
    diags = check_fragment_presence(rig, _SRC, FragmentPresence(variant_delta=True))
    assert diags == []


def test_nondefault_variant_contributing_nothing_is_rejected() -> None:
    variants = AxisDecl(values=["a", "b"], default="a")
    rig = _rig(variant="b", variants=variants)
    diags = check_fragment_presence(rig, _SRC, FragmentPresence())
    assert len(diags) == 1
    assert diags[0].code == "lang-variant"
    assert "r_b.overlay" in diags[0].message
    assert "r_b_defconfig" in diags[0].message
    assert "r_b.yml" in diags[0].message


def test_nondefault_revision_contributing_nothing_is_rejected() -> None:
    revisions = AxisDecl(values=["1", "2"], default="1")
    rig = _rig(revision="2", revisions=revisions)
    diags = check_fragment_presence(rig, _SRC, FragmentPresence())
    assert len(diags) == 1
    assert diags[0].code == "lang-rev"
    assert "r_2_defconfig" in diags[0].message
    assert "r_2.yml" in diags[0].message


def test_dotted_revision_names_the_normalized_filename() -> None:
    revisions = AxisDecl(values=["1", "1.5"], default="1")
    rig = _rig(revision="1.5", revisions=revisions)
    diags = check_fragment_presence(rig, _SRC, FragmentPresence())
    assert "r_1_5_defconfig" in diags[0].message
    assert "r_1.5_defconfig" not in diags[0].message


def test_an_existing_overlay_or_defconfig_counts_as_contribution() -> None:
    """The two cmake-collected artifact kinds satisfy the
    contributes-nothing check exactly like a loaded delta does -- the
    presence FACT arrives as a value."""
    variants = AxisDecl(values=["a", "b"], default="a")
    rig = _rig(variant="b", variants=variants)
    assert check_fragment_presence(rig, _SRC, FragmentPresence(variant_overlay=True)) == []
    assert check_fragment_presence(rig, _SRC, FragmentPresence(variant_defconfig=True)) == []
    revisions = AxisDecl(values=["1", "2"], default="1")
    rig = _rig(revision="2", revisions=revisions)
    assert check_fragment_presence(rig, _SRC, FragmentPresence(revision_defconfig=True)) == []


def test_contribution_names_are_the_single_stem_source() -> None:
    """The probes (IO phase) and the message text share these
    constructors -- variant stems stay RAW, revision stems normalize."""
    assert variant_contribution_names("r", "b.1") == (
        "r_b.1.overlay",
        "r_b.1_defconfig",
        "r_b.1.yml",
    )
    assert revision_contribution_names("r", "1.5") == ("r_1_5_defconfig", "r_1_5.yml")
