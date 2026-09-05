# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""DTS plumbing for the SHIELD-template side, and for shield-declared
per-instance-parameter token vocabularies (shield,param-includes:). This
module never touches the board DT (that is an analyzer-slice concern);
what's here is cpp + stock dtlib parsing of `.shield` translation units
(shield templates are pre-instantiation text with no binding/schema of
their own, so there is nothing for edtlib to attach type info to),
``dt-bindings/connector/*.h`` position-index header parsing, and
resolve_token/check_include, the per-instance-parameter mechanism's own
synthetic-TU resolution.

**The cpp/unit-test seam**: cpp is a subprocess, so nothing that invokes
it is unit-testable. `run_cpp`/`parse_dts`/`parse_tu`/`check_include`/
`resolve_token` are integration-only by construction; `is_int_literal`,
`words`, `render_prop`, `src_of` are pure and get unit tests directly.

**No module-scope $ZEPHYR_BASE lookup**: `devicetree.dtlib` is located
via `get_dtlib()`, called only from inside a function -- pytest imports
every module in a directory before a marker expression (e.g. `-m "not
build"`) deselects any one item, so a module-scope lookup would break
collection for selections that never run it."""

from __future__ import annotations

import logging
import os
import re
import shlex
import subprocess
import sys

from .deps import Deps, touch
from .diag import LoadError, SourceRef, error

log = logging.getLogger(__name__)

#: This module's own file, two levels up from scripts/rigc/dtsio.py ->
#: the repo root, computed from __file__ alone (no environment lookup,
#: so this constant is safe at module scope).
MODULE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODULE_INC = os.path.join(MODULE_ROOT, "include")


def _zephyr_base() -> str:
    """$ZEPHYR_BASE, read at CALL time -- never at module scope (the
    collection trap this module designs out)."""
    zb = os.environ.get("ZEPHYR_BASE")
    if not zb:
        raise RuntimeError(
            "rigc: $ZEPHYR_BASE is not set -- it is required to locate "
            "zephyr's devicetree library and includes. The build "
            "(dts.cmake) passes it automatically; for standalone use, "
            "export ZEPHYR_BASE=<zephyr tree>."
        )
    return zb


def zephyr_inc() -> str:
    return os.path.join(_zephyr_base(), "include")


def get_dtlib():
    """Import and return the `devicetree.dtlib` module, locating it via
    $ZEPHYR_BASE at CALL time. Safe to call repeatedly (sys.path.insert
    is a no-op once the entry is already present; the module import
    itself is cached by Python regardless)."""
    zephyr_dt_src = os.path.join(_zephyr_base(), "scripts", "dts", "python-devicetree", "src")
    if zephyr_dt_src not in sys.path:
        sys.path.insert(0, zephyr_dt_src)
    from devicetree import dtlib

    return dtlib


def src_of(obj) -> SourceRef:
    """SourceRef from a dtlib Node or Property (both carry filename/lineno).
    Duck-typed on shape rather than `isinstance(obj, dtlib.Node)`, so this
    function needs no dtlib import of its own -- callers already have one
    live by the time they call this (they are holding a Node/Property)."""
    if hasattr(obj, "props"):  # Node: has child props/nodes
        label = obj.labels[0] if obj.labels else obj.path
        return SourceRef(obj.filename, obj.lineno, label)
    label = f"{obj.node.path}: {obj.name}"  # Property
    return SourceRef(obj.filename, obj.lineno, label)


def run_cpp(dts_path: str, out_path: str, include_dirs: list[str] | None = None) -> None:
    """include_dirs is searched FIRST, in order, exactly as gcc searches a
    -I list; ZEPHYR_INC/MODULE_INC are always appended last, so a caller
    passing none sees exactly the two-directory search path.

    Writes cpp's stdout to out_path OURSELVES (never gcc's own -o, which
    writes nothing at all on a failing run) -- even a preprocess that
    fails partway (a missing NESTED #include, a macro error) has already
    emitted linemarkers for every file it opened up to that point, and
    that partial text is what a caller recovering dependency data on the
    failure path needs (see linemarker_files). Captured and written as
    BYTES, never text: a preprocessed tree is whatever bytes its sources
    hold, and decoding it through the ambient locale would make this
    file's contents depend on the environment rather than on its inputs.
    Byte-for-byte identical to what gcc's own -o produces. Returns None
    on success; raises LoadError (lang-cpp) when the preprocessor
    fails."""
    cmd = ["gcc", "-E", "-x", "assembler-with-cpp", "-nostdinc"]
    for d in include_dirs or []:
        cmd += ["-I", d]
    cmd += [
        "-I",
        zephyr_inc(),
        "-I",
        MODULE_INC,
        "-undef",
        "-D__DTS__",
        dts_path,
    ]
    log.debug("cpp argv: %s", shlex.join(cmd))
    res = subprocess.run(cmd, capture_output=True)
    with open(out_path, "wb") as f:
        f.write(res.stdout)
    if res.returncode != 0:
        raise LoadError(
            error(
                "lang-cpp",
                "preprocessing failed\n" + res.stderr.decode("utf-8", "replace").strip(),
                (SourceRef(dts_path, 0),),
            )
        )


def parse_dts(dts_path: str, workdir: str, include_dirs: list[str] | None = None):
    """CPP + stock dtlib. dtlib reads the CPP linemarkers, so node/prop
    source references point at the ORIGINAL .shield files, not the
    generated translation unit -- free provenance for diagnostics.

    Returns the parsed dtlib.DT; raises LoadError (lang-parse) on a
    dtlib error."""
    os.makedirs(workdir, exist_ok=True)
    pre = os.path.join(workdir, os.path.basename(dts_path) + ".pre")
    run_cpp(dts_path, pre, include_dirs)
    dtlib = get_dtlib()
    try:
        return dtlib.DT(pre)
    except dtlib.DTError as e:
        raise LoadError(error("lang-parse", str(e))) from e


def parse_tu(includes: list[str], workdir: str, name: str, include_dirs: list[str] | None = None):
    """Build + parse a one-off translation unit that includes the given
    files -- the shield-TU entry point (one base `.shield` plus an
    optional resolved revision fragment, cpp-included into ONE unit
    rather than merged as YAML).

    Returns the parsed dtlib.DT of the synthesized unit (parse_dts's
    failure shapes apply)."""
    os.makedirs(workdir, exist_ok=True)
    tu = os.path.join(workdir, name)
    with open(tu, "w") as f:
        f.write("/dts-v1/;\n")
        for inc in includes:
            f.write(f'#include "{inc}"\n')
    log.info("wrote %s", tu)
    log.info("shield TU: %s", name)
    log.debug("TU: %s (includes %s)", tu, includes)
    return parse_dts(tu, workdir, include_dirs)


_DEFINE_RE = re.compile(r"^\s*#define\s+(\w+)\s+(\d+|0x[0-9a-fA-F]+)\s*$", re.M)


def parse_header_indices(
    type_name: str,
    header_dirs: list[str] | None = None,
) -> tuple[dict, Deps]:
    """dt-bindings/connector/<type>.h -- the position-index single source
    of truth for connector type_name. Returns ({short position name:
    index}, Deps) with the common macro prefix stripped
    (ARDUINO_HEADER_R3_D7 -> D7).

    header_dirs is searched in order, first match wins, exactly as cpp
    resolves #include <dt-bindings/connector/x.h> against a -I list --
    MODULE_INC is always tried last."""
    dirs = list(header_dirs) if header_dirs else []
    dirs.append(MODULE_INC)
    rel = os.path.join("dt-bindings", "connector", f"{type_name}.h")
    path = next(
        (os.path.join(d, rel) for d in dirs if os.path.isfile(os.path.join(d, rel))),
        os.path.join(dirs[-1], rel),
    )
    with open(path) as f:
        defines = {m[1]: int(m[2], 0) for m in _DEFINE_RE.finditer(f.read())}
    prefix = os.path.commonprefix(list(defines))
    indices = {name[len(prefix) :]: val for name, val in defines.items()}
    return indices, touch(path)


def source_files(dt, exclude_dir: str) -> list[str]:
    """Every REAL source-tree file dt was parsed from, recovered from cpp
    linemarkers via each Node/Property's own .filename. EXCLUDES
    exclude_dir (and anything under it): the synthesized translation unit
    parse_tu builds there is a generated artifact, not a real source
    file -- only its real #included files belong in dependency data."""
    exclude = os.path.realpath(exclude_dir)
    names = set()
    for node in dt.node_iter():
        names.add(node.filename)
        for prop in node.props.values():
            names.add(prop.filename)
    return sorted(
        name
        for name in names
        if name
        and os.path.realpath(name) != exclude
        and not os.path.realpath(name).startswith(exclude + os.sep)
    )


#: GNU cpp's own file-change record: `# <line> "<file>" [flags...]`,
#: emitted whenever cpp opens or returns from a file (nested #includes
#: included). Anchored at line start -- this is cpp's own line-oriented
#: output convention, never indented.
_LINEMARKER_RE = re.compile(r'^# \d+ "([^"]*)"', re.M)


def linemarker_files(pre_text: str, exclude_dir: str) -> list[str]:
    """source_files' sibling for callers that never get a parsed dtlib.DT
    at all -- a preprocess that fails partway (dtlib itself rejects the
    result, or a NESTED #include inside the named file is what actually
    fails) still leaves linemarkers in pre_text for every file cpp opened
    before the failure, and that is the dependency data such a caller
    needs (a header that fails to preprocess is still a file the rig
    depends on).

    Synthetic names cpp invents for itself (`<built-in>`,
    `<command-line>`, ...) are not real files and are skipped. EXCLUDES
    exclude_dir (and anything under it), the same rule source_files
    applies to the synthesized translation unit.

    pre_text is the preprocessed output's own text -- reading it from
    disk is the CALLER's concern (this function touches no filesystem);
    returns the files sorted and deduplicated. The caller owns the
    result."""
    exclude = os.path.realpath(exclude_dir)
    names = {
        m.group(1) for m in _LINEMARKER_RE.finditer(pre_text) if not m.group(1).startswith("<")
    }
    return sorted(
        name
        for name in names
        if os.path.realpath(name) != exclude
        and not os.path.realpath(name).startswith(exclude + os.sep)
    )


def words(prop) -> list[int]:
    """Raw 32-bit cells of a property value. Only for
    Type.PHANDLES_AND_NUMS -- dtlib has no typed accessor for that shape;
    every other cell shape goes through to_num/to_nums directly."""
    v = prop.value
    return [int.from_bytes(v[i : i + 4], "big") for i in range(0, len(v) - len(v) % 4, 4)]


def render_prop(prop) -> str | None:
    """Generic passthrough rendering for props the rig model doesn't
    interpret (compatible, spi-max-frequency, jedec-id, ...). Returns a
    complete "name = value;" string, or None if the type can't
    passthrough. Renders via dtlib's typed accessors with its OWN stable
    formatting, never str(prop): str(prop) can leak an authored numeric
    radix or a phandle's label rather than the value dtlib resolved,
    which this passthrough must not do."""
    dtlib = get_dtlib()
    T = dtlib.Type
    t = prop.type
    if t is T.EMPTY:
        return f"{prop.name};"
    if t is T.NUM:
        return f"{prop.name} = <{prop.to_num()}>;"
    if t is T.NUMS:
        return f"{prop.name} = <{' '.join(str(n) for n in prop.to_nums())}>;"
    if t is T.STRING or t is T.STRINGS:
        vals = ", ".join(f'"{s}"' for s in prop.to_strings())
        return f"{prop.name} = {vals};"
    if t is T.BYTES:
        return f"{prop.name} = [{prop.value.hex(' ')}];"
    return None


# ------------------------------------------------ per-instance-parameter vocabulary

_INT_LITERAL_RE = re.compile(r"^-?(0[xX][0-9a-fA-F]+|\d+)$")


def is_int_literal(text: str) -> bool:
    """Whether text is already a bare DTS integer literal (decimal or 0x
    hex, optionally negative) needing no header resolution at all."""
    return bool(_INT_LITERAL_RE.match(text))


def check_include(
    header: str,
    workdir: str,
    tag: str,
    include_dirs: list[str] | None = None,
) -> tuple[str | None, list[str]]:
    """Confirm one declared header (a shield device's own
    shield,param-includes entry) is real and preprocesses cleanly on its
    own (the "lang-dt-include" diagnostic).

    Returns (detail, files): detail is an error detail string on failure,
    else None; files is every real file this preprocess opened
    (linemarker_files over the synthesized TU's own preprocessed output),
    recovered WHETHER OR NOT this check passes -- a header that fails to
    preprocess (its own nested #include is what actually failed) is still
    a file the rig depends on, and is exactly the file an author is about
    to edit. files is empty only when nothing beyond the synthesized TU
    itself was ever opened (the named header could not be found at all).
    The caller owns the returned list."""
    tu = os.path.join(workdir, f"rig-dt-include-{tag}.dts")
    with open(tu, "w") as f:
        f.write(f'/dts-v1/;\n#include "{header}"\n/ {{ }};\n')
    log.info("wrote %s", tu)
    pre = os.path.join(workdir, os.path.basename(tu) + ".pre")
    detail = None
    try:
        parse_dts(tu, workdir, include_dirs)
    except LoadError as e:
        detail = e.diags[-1].message
    files: list[str] = []
    if os.path.isfile(pre):
        # Only the linemarkers are wanted, and those are ASCII paths --
        # decode leniently rather than let an undecodable byte somewhere
        # in a preprocessed tree turn dependency recovery into a crash.
        with open(pre, encoding="utf-8", errors="replace") as f:
            files = linemarker_files(f.read(), workdir)
    return detail, files


def resolve_token(
    token: str, headers: list[str], workdir: str, tag: str, include_dirs: list[str] | None = None
) -> int | None:
    """cpp+dtlib-resolve one assigned parameter TOKEN against a synthetic
    TU that includes exactly headers -- the owning shield device's own
    declared_param_includes vocabulary, in order. Returns None if cpp
    leaves the token unexpanded (an unresolved bareword identifier is not
    valid syntax inside a DTS cell list, so the embedding dtlib.DT parse
    fails -- the same failure shape whether the token is a typo or the
    defining header was never declared)."""
    tu = os.path.join(workdir, f"rig-param-{tag}.dts")
    with open(tu, "w") as f:
        f.write("/dts-v1/;\n")
        for header in headers:
            f.write(f'#include "{header}"\n')
        f.write(f"/ {{ p {{ v = <{token}>; }}; }};\n")
    log.info("wrote %s", tu)
    try:
        dt = parse_dts(tu, workdir, include_dirs)
    except LoadError:
        return None
    return dt.get_node("/p").props["v"].to_num()
