# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""The document model: mark-aware YAML parsing shared by rig.yml (the
METADATA document) and every content/delta document -- the base
<rigname>.yml and every <rigname>_<variant|rev>.yml fragment all use
the SAME flat top-level shape, with no `rig:` wrapper in either case,
so the same parser serves both.

Line-accurate anchors ride on YAML composer marks: a scalar value's own
start line, a nested mapping's FIRST ENTRY line (one below the key that
introduces it), a sequence item's own line -- proven byte-exact against
the frozen goldens, which this module's diagnostics depend on staying
that way.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import yaml

from ..diag import Diagnostic, SourceRef, error
from ..unimplemented import Unimplemented


@dataclass(frozen=True)
class Val:
    """A YAML scalar/collection plus its source position. Mappings hold
    {key: Val}, sequences hold [Val]; src carries the VALUE node's own
    start line and the dotted/bracketed key path as the human label."""

    value: Any
    src: SourceRef


def _scalar(node: Any) -> Any:
    v = node.value
    if node.tag.endswith(":int"):
        return int(v.replace("_", ""), 0)
    if node.tag.endswith(":bool"):
        return v.lower() in ("true", "yes", "on")
    if node.tag.endswith(":null"):
        return None
    return v


def _walk(node: Any, path: str, fname: str) -> Val:
    src = SourceRef(fname, node.start_mark.line + 1, path)
    if isinstance(node, yaml.MappingNode):
        m = {}
        for k, v in node.value:
            key = k.value
            m[key] = _walk(v, f"{path}.{key}" if path else key, fname)
        return Val(m, src)
    if isinstance(node, yaml.SequenceNode):
        return Val([_walk(v, f"{path}[{i}]", fname) for i, v in enumerate(node.value)], src)
    return Val(_scalar(node), src)


def parse_marked(path: str) -> Val:
    """Parse one YAML file into a Val tree with line-accurate marks.

    No frozen golden exercises a YAML parse failure, so `Unimplemented`
    is used here rather than inventing unverified diagnostic wording.

    Returns the file's Val tree; raises Unimplemented on an unreadable
    file or malformed YAML."""
    try:
        with open(path) as f:
            try:
                root = yaml.compose(f, yaml.SafeLoader)
            except yaml.YAMLError as exc:
                raise Unimplemented(f"YAML parse failure in {path}") from exc
    except OSError as exc:
        raise Unimplemented(f"cannot read {path}") from exc
    if root is None:
        raise Unimplemented(f"empty YAML document {path}")
    return _walk(root, "", path)


def as_mapping(v: Val, what: str) -> dict[str, Val]:
    """The Val's own value as a mapping, or a loud (Unimplemented)
    refusal if it is not one -- a document shape no frozen golden
    exercises, so there is no verified wording to give it instead."""
    if not isinstance(v.value, dict):
        raise Unimplemented(f"{what} that is not a mapping")
    return v.value


def require(mapping: Val, key: str, ctx: str) -> tuple[Val | None, list[Diagnostic]]:
    """A required key's Val, or a lang-schema diagnostic naming what is
    missing. Diagnostics are always returned rather than raised, so a
    caller can keep collecting further findings after a missing key.

    Returns (value, diagnostics): the key's Val, or None beside the
    single missing-key error."""
    m = as_mapping(mapping, ctx)
    if key not in m:
        return None, [
            error("lang-schema", f"{ctx}: required key '{key}' is missing", (mapping.src,))
        ]
    return m[key], []


def content_file_name(rig_name: str) -> str:
    """<rigname>.yml -- CONSTRUCTED from the rig's own name:, never
    parsed from the folder it happens to live in."""
    return f"{rig_name}.yml"
