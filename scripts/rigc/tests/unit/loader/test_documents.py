# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: loader.documents -- the document model.

Two contracts live here: content/fragment filename CONSTRUCTION
(construct-don't-parse: filenames derive from the rig's own declared
name: and a selected axis value, NEVER from the folder the rig happens
to live in), and require()'s missing-key structure (a stable contract --
code, severity, anchor -- even though the wording itself is a
no-golden diagnostic, hand-differentialed separately, not duplicated
here). A content document has no metadata/content key split to enforce:
board:/sockets: are not rig.yml metadata, so nothing about a content
document needs to reject them specially.

The anchor-line contract rides along: an anchor carries the VALUE node's
start line (a scalar value sits on its key's line; a nested mapping
starts on the first entry's line, one below its key).
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from rigc.diag import Diagnostic, SourceRef
from rigc.loader.documents import Val, content_file_name, parse_marked, require


def _ref(d: Diagnostic, i: int = 0) -> SourceRef:
    """First anchor of a diagnostic, mypy-narrowed (refs entries may be
    None by type; these tests assert presence)."""
    ref = d.refs[i]
    assert ref is not None
    return ref


def _doc(tmp_path: Path, text: str, name: str = "content.yml") -> Val:
    path = tmp_path / name
    path.write_text(dedent(text))
    return parse_marked(str(path))


# --------------------------------------------------- filename construction


def test_content_file_is_name_dot_yml() -> None:
    assert content_file_name("nucleo_datalogger") == "nucleo_datalogger.yml"


def test_construction_uses_the_name_value_alone() -> None:
    """No hidden inputs: same name, same result -- there is no folder
    parameter to parse a name out of. (Fragment-stem construction lives
    in axes.py -- the hwmv2 seam -- and is tested in test_axes.py.)"""
    assert content_file_name("other") == "other.yml"


# ------------------------------------------------------------- require()


def test_require_present_key_returns_it_with_no_diagnostics(tmp_path: Path) -> None:
    doc = _doc(tmp_path, "name: x\n")
    val, diags = require(doc, "name", "rig")
    assert val is not None and val.value == "x"
    assert diags == []


def test_require_missing_key_is_a_lang_schema_error_anchored_at_container(tmp_path: Path) -> None:
    doc = _doc(tmp_path, "other: 1\n")
    val, diags = require(doc, "name", "rig")
    assert val is None
    assert len(diags) == 1
    d = diags[0]
    assert d.severity == "error"
    assert d.code == "lang-schema"
    assert d.refs == (doc.src,)  # anchored at the CONTAINER, not a key
