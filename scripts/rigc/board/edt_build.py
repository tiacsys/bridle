# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: BSD-3-Clause
"""Standalone edtlib.EDT construction over a single real devicetree file.

This is a generic reader layer, under a BSD-3-Clause license (see SPDX
header above), deliberately decoupled from the Apache-2.0 product layer
-- it knows nothing about rigs, sockets, or any other rigc product
concept, only devicetree/edtlib mechanics plus the one piece of Zephyr
CMake convention (a build_info.yml's cmake.devicetree section) needed to
recover the include/bindings directories a real west build used. It is
the candidate for upstreaming into python-devicetree itself, so it must
never import a rigc product module (model / analyzer / diag / loader) --
only the standard library, PyYAML, and devicetree.edtlib.

Recipe (mirrors cmake/modules/dts.cmake + scripts/dts/gen_defines.py): cpp
the board .dts with -nostdinc plus one -isystem per include dir and
-D__DTS__ (no other defines -- linemarkers stay intact, so dtlib/edtlib
source references point at the ORIGINAL board files, not the preprocessed
temp file), then hand the preprocessed file plus the bindings dirs to
edtlib.EDT.

$ZEPHYR_BASE is needed only to locate the devicetree package itself
(scripts/dts/python-devicetree/src) -- this module carries no other tie to
a Zephyr checkout. That lookup is deferred to ensure_devicetree_on_path(),
called from build_edt() rather than at import time, so a caller that only
needs BuildRecipe / recipe_from_build_info / preprocess (none of which
touch devicetree.edtlib) can use this module with $ZEPHYR_BASE unset."""

from __future__ import annotations

import logging
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from devicetree import edtlib

#: stdlib logging only (no product import, SPDX header above): keeps
#: this reader-module's license boundary clean.
log = logging.getLogger(__name__)


def ensure_devicetree_on_path() -> None:
    """Put zephyr's python-devicetree source on sys.path, locating it via
    $ZEPHYR_BASE. Idempotent; safe to call from a caller (project.py)
    that needs devicetree.edtlib importable before build_edt() itself
    ever runs."""
    zephyr_base = os.environ.get("ZEPHYR_BASE")
    if not zephyr_base:
        raise RuntimeError(
            "edt_build: $ZEPHYR_BASE is not set -- it is required to locate "
            "zephyr's devicetree library (scripts/dts/python-devicetree/"
            "src). Export it (the zephyr-rigs tree) before building an EDT."
        )
    dt_src = os.path.join(zephyr_base, "scripts", "dts", "python-devicetree", "src")
    if dt_src not in sys.path:
        sys.path.insert(0, dt_src)


@dataclass(frozen=True)
class BuildRecipe:
    """The two directory lists a real Zephyr configure step feeds to the
    devicetree preprocessor and to edtlib.

    include_dirs:
      -isystem search directories for the C preprocessor pass.

    bindings_dirs:
      Directories edtlib recursively globs for .yaml binding files.
    """

    include_dirs: list[str]
    bindings_dirs: list[str]


def recipe_from_build_info(build_info_path: str) -> BuildRecipe:
    """Recover the recipe a real west build used from its
    <build-dir>/build_info.yml.

    dts.cmake's dts_build_info_output() records the exact directories
    passed to the board-DTS preprocessor and to edtlib under
    cmake.devicetree.include-dirs / cmake.devicetree.bindings-dirs -- this
    is a read of that record, not a re-derivation, so it stays correct
    across Zephyr versions without mirroring pre_dt.cmake.

    Also appends cmake.board.path (written by boards.cmake:
    build_info(board path PATH ${BOARD_DIRECTORIES}) -- every board
    directory the configure resolved, base board first, then any hwmv2
    board-EXTENSION directories registered against it). Plain boards get
    exactly one entry here (their own dir, already implied by
    include-dirs' subpaths); an extension variant's own dts lives in a
    DIFFERENT directory than the base board it #includes, so its base
    directory must be on the cpp search path too for that quoted include
    to resolve -- this is the standalone-read analog of cmake/modules/dts.cmake
    appending the same BOARD_DIRECTORIES list to rigc's
    --include-dir args for the in-build path.
    """
    with open(build_info_path) as f:
        doc = yaml.safe_load(f)
    devicetree = doc["cmake"]["devicetree"]
    board_paths = doc["cmake"].get("board", {}).get("path", [])
    if isinstance(board_paths, str):
        board_paths = [board_paths]
    return BuildRecipe(
        include_dirs=list(devicetree["include-dirs"]) + list(board_paths),
        bindings_dirs=list(devicetree["bindings-dirs"]),
    )


def preprocess(dts_path: str, include_dirs: list[str], out_path: str) -> None:
    """cpp dts_path, exactly as a real board-DTS preprocess does: no
    standard include path, one -isystem per include_dirs entry, and
    -D__DTS__ (the sole macro Zephyr's own board-DTS cpp step defines).

    Writes the preprocessed text to out_path and returns None."""
    cmd = ["gcc", "-E", "-x", "assembler-with-cpp", "-nostdinc"]
    for include_dir in include_dirs:
        cmd += ["-isystem", include_dir]
    cmd += ["-D__DTS__", dts_path, "-o", out_path]
    log.debug("cpp argv: %s", shlex.join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"cpp failed on {dts_path}:\n{result.stderr}")


def build_edt(dts_path: str, recipe: BuildRecipe, workdir: str) -> edtlib.EDT:
    """Build a standalone edtlib.EDT over one .dts file -- no app, no
    overlay: this pass reads only the board's own devicetree, never app or
    overlay context.

    infer_binding_for_paths covers the two paths a real build always
    carries without a dedicated binding (/zephyr,user, /cpus), matching
    what a normal Zephyr configure does for the same board.

    Returns a fresh edtlib.EDT over the preprocessed devicetree;
    workdir receives the intermediate file."""
    ensure_devicetree_on_path()
    from devicetree import edtlib

    os.makedirs(workdir, exist_ok=True)
    pre = os.path.join(workdir, os.path.basename(dts_path) + ".pre")
    log.debug("TU: %s (board dts %s)", pre, dts_path)
    preprocess(dts_path, recipe.include_dirs, pre)
    return edtlib.EDT(
        pre,
        recipe.bindings_dirs,
        default_prop_types=True,
        infer_binding_for_paths=["/zephyr,user", "/cpus"],
    )
