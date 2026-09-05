# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: dtsio -- the pure, cpp-free half of the DTS plumbing.

`run_cpp`/`parse_dts`/`parse_tu`/`check_include`/`resolve_token` invoke a
REAL subprocess (gcc) and get their coverage through the frozen suite's
front door, integration-only by construction -- nothing here calls them.
What IS unit-testable: `is_int_literal` (pure string classification),
and `words`/`render_prop`/`src_of`, which operate on a `dtlib.DT` --
hermetic and cpp-free as long as the `.dts` text handed to `dtlib.DT()`
is ALREADY in preprocessed form (no #include, no macros): a hand-written
synthetic file, never a real board/shield's own content (enforced by
assert_fixture_local).

`get_dtlib()` is exercised only INDIRECTLY here, by building a real
`dtlib.DT` from synthetic text -- this needs $ZEPHYR_BASE to locate the
devicetree PACKAGE (pure Python, no Zephyr DATA): "no Zephyr DATA" is
not "no $ZEPHYR_BASE".
"""

from __future__ import annotations

import os
from textwrap import dedent

from rigc.dtsio import get_dtlib, is_int_literal, linemarker_files, render_prop, src_of, words

# ---------------------------------------------------------------- is_int_literal


def test_is_int_literal_accepts_decimal() -> None:
    assert is_int_literal("42")


def test_is_int_literal_accepts_negative_decimal() -> None:
    assert is_int_literal("-1")


def test_is_int_literal_accepts_hex() -> None:
    assert is_int_literal("0x2A")


def test_is_int_literal_rejects_a_symbolic_token() -> None:
    assert not is_int_literal("INPUT_KEY_0")


def test_is_int_literal_rejects_empty_string() -> None:
    assert not is_int_literal("")


def test_is_int_literal_rejects_a_hex_looking_symbol_without_prefix() -> None:
    assert not is_int_literal("DEAD")


# ---------------------------------------------------------------- dtlib helpers


def _dt(tmp_path, text: str):
    """A dtlib.DT parsed DIRECTLY from already-preprocessed synthetic
    text -- no cpp, no subprocess, no real repo content."""
    path = tmp_path / "synthetic.dts"
    path.write_text(text)
    dtlib = get_dtlib()
    return dtlib.DT(str(path))


def test_words_reads_raw_32bit_cells(tmp_path) -> None:
    dt = _dt(
        tmp_path,
        """/dts-v1/;
/ {
    p { v = <1 2 3>; };
};
""",
    )
    prop = dt.get_node("/p").props["v"]
    assert words(prop) == [1, 2, 3]


def test_render_prop_num(tmp_path) -> None:
    dt = _dt(
        tmp_path,
        """/dts-v1/;
/ {
    p { v = <8000000>; };
};
""",
    )
    prop = dt.get_node("/p").props["v"]
    assert render_prop(prop) == "v = <8000000>;"


def test_render_prop_nums(tmp_path) -> None:
    dt = _dt(
        tmp_path,
        """/dts-v1/;
/ {
    p { v = <1 2 3>; };
};
""",
    )
    prop = dt.get_node("/p").props["v"]
    assert render_prop(prop) == "v = <1 2 3>;"


def test_render_prop_string(tmp_path) -> None:
    dt = _dt(
        tmp_path,
        """/dts-v1/;
/ {
    p { compatible = "vnd,thing"; };
};
""",
    )
    prop = dt.get_node("/p").props["compatible"]
    assert render_prop(prop) == 'compatible = "vnd,thing";'


def test_render_prop_bytes(tmp_path) -> None:
    dt = _dt(
        tmp_path,
        """/dts-v1/;
/ {
    p { v = [c8 40 15]; };
};
""",
    )
    prop = dt.get_node("/p").props["v"]
    assert render_prop(prop) == "v = [c8 40 15];"


def test_render_prop_empty(tmp_path) -> None:
    dt = _dt(
        tmp_path,
        """/dts-v1/;
/ {
    p { empty-flag; };
};
""",
    )
    prop = dt.get_node("/p").props["empty-flag"]
    assert render_prop(prop) == "empty-flag;"


def test_render_prop_phandle_returns_none(tmp_path) -> None:
    """The None-for-phandles branch is load-bearing (dtsio.py's own
    docstring): a phandle-typed value the model didn't interpret is
    dropped, never rendered via its DTS label."""
    dt = _dt(
        tmp_path,
        """/dts-v1/;
/ {
    plug: plug { #gpio-cells = <2>; };
    p { some-ref = <&plug 1 2>; };
};
""",
    )
    prop = dt.get_node("/p").props["some-ref"]
    assert render_prop(prop) is None


def test_src_of_node_uses_the_label(tmp_path) -> None:
    dt = _dt(
        tmp_path,
        """/dts-v1/;
/ {
    p: p { v = <1>; };
};
""",
    )
    node = dt.get_node("/p")
    ref = src_of(node)
    assert ref.file == str(tmp_path / "synthetic.dts")
    assert ref.key == "p"


def test_src_of_node_falls_back_to_path_with_no_label(tmp_path) -> None:
    dt = _dt(
        tmp_path,
        """/dts-v1/;
/ {
    p { v = <1>; };
};
""",
    )
    node = dt.get_node("/p")
    assert src_of(node).key == "/p"


def test_src_of_property_names_node_path_and_prop_name(tmp_path) -> None:
    dt = _dt(
        tmp_path,
        """/dts-v1/;
/ {
    p { v = <1>; };
};
""",
    )
    prop = dt.get_node("/p").props["v"]
    ref = src_of(prop)
    assert ref.key == "/p: v"


def test_module_root_is_the_repo_root() -> None:
    from rigc.dtsio import MODULE_ROOT

    assert os.path.isdir(os.path.join(MODULE_ROOT, "scripts", "rigc"))
    assert os.path.isdir(os.path.join(MODULE_ROOT, "boards", "shields"))


# ---------------------------------------------------------------- linemarker_files


def test_linemarker_files_recovers_a_real_included_header(tmp_path) -> None:
    """A single #include's own linemarker is recovered as a real file --
    source_files' sibling for a caller with no parsed dtlib.DT at all."""
    header = tmp_path / "header.h"
    pre_text = dedent(f"""\
        # 0 "{tmp_path}/workdir/tu.dts"
        # 0 "<built-in>"
        # 0 "<command-line>"
        # 1 "{tmp_path}/workdir/tu.dts"
        # 1 "{header}" 1
        # 3 "{tmp_path}/workdir/tu.dts" 2
        """)
    assert linemarker_files(pre_text, str(tmp_path / "workdir")) == [str(header)]


def test_linemarker_files_excludes_synthetic_cpp_markers(tmp_path) -> None:
    """<built-in> and <command-line> are cpp's own invented names, never
    real files -- they must never surface as dependency data, even
    alongside a real included header that DOES belong in the result."""
    header = tmp_path / "header.h"
    pre_text = dedent(f"""\
        # 0 "{tmp_path}/workdir/tu.dts"
        # 0 "<built-in>"
        # 0 "<command-line>"
        # 1 "{header}" 1
        """)
    assert linemarker_files(pre_text, str(tmp_path / "workdir")) == [str(header)]


def test_linemarker_files_excludes_the_workdir(tmp_path) -> None:
    """The workdir-exclusion rule, proven with a real negative control: a
    helper that forgot to exclude exclude_dir would put the generated TU
    itself into the result -- this asserts the TU is genuinely absent,
    not merely that some other file is present."""
    workdir = tmp_path / "workdir"
    tu = workdir / "tu.dts"
    pre_text = dedent(f"""\
        # 1 "{tu}"
        """)
    assert linemarker_files(pre_text, str(workdir)) == []


def test_linemarker_files_excludes_a_file_nested_under_the_workdir(tmp_path) -> None:
    """Not just the workdir's own TU: anything living UNDER exclude_dir is
    excluded too, matching source_files' own exclusion rule."""
    workdir = tmp_path / "workdir"
    nested = workdir / "nested" / "generated.dts"
    pre_text = dedent(f"""\
        # 1 "{nested}"
        """)
    assert linemarker_files(pre_text, str(workdir)) == []


def test_linemarker_files_recovers_a_nested_include(tmp_path) -> None:
    """A header that itself #includes another header leaves a linemarker
    for BOTH -- cpp linemarkers name every file actually opened, nested
    includes included, which is the whole point of reading them back
    instead of predicting a search path in Python."""
    outer = tmp_path / "outer.h"
    inner = tmp_path / "inner.h"
    pre_text = dedent(f"""\
        # 1 "{tmp_path}/workdir/tu.dts"
        # 1 "{outer}" 1
        # 1 "{inner}" 1
        # 3 "{inner}" 2
        # 2 "{outer}" 2
        """)
    assert linemarker_files(pre_text, str(tmp_path / "workdir")) == sorted([str(outer), str(inner)])


def test_linemarker_files_deduplicates_repeated_markers(tmp_path) -> None:
    """cpp emits a fresh linemarker every time it RETURNS to a file too
    (not only when it opens one) -- the same file appears more than once
    in real output, and must surface exactly once here."""
    header = tmp_path / "header.h"
    pre_text = dedent(f"""\
        # 1 "{header}" 1
        # 5 "{header}"
        # 6 "{header}"
        """)
    assert linemarker_files(pre_text, str(tmp_path / "workdir")) == [str(header)]
