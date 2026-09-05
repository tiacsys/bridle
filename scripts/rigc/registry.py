# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Connector-type registry. A type IS two artifacts: the unified
socket+plug binding (board side, edtlib's job in the real build; shield
side, consumed HERE by the loader) and the index header (position single
source of truth). The registry is a PREREQUISITE, not a nicety --
loader/shields.py checks every shield's plug against it (lang-shield-type), so
an empty or stubbed registry would emit errors on perfectly valid
fixture/corpus shields and corrupt every golden's bytes.

Data source: ONE file per type, dts/bindings/connectors/<type>.yaml -- the
real socket binding plus the shield-side plug contract folded in as
`plug,*` top-level extension keys (namespaced by the SIDE they describe,
never the project) -- legal since edtlib treats any top-level binding key
containing a comma as an opaque vendor-namespaced extension. Read HERE with
a plain `yaml.safe_load` rather than edtlib.Binding: the plug,* keys are
declared inline in every unified binding, so the raw YAML dict already has
them.

Resolved ONCE at CLI entry and threaded down as a value -- the
hardcoded BINDINGS default below is a DEV/TEST convenience only, never
the production path: a real build always threads --connector-dir
explicitly (cmake/modules/dts.cmake mirrors DTS_ROOT/dts/bindings/connectors for
every DTS_ROOT, the same rule this module's own default encodes), because
the connector-type registry is a DIFFERENT consumer from edtlib's own
bindings scan and cannot ride inside a threaded --bindings-dir. BINDINGS
being wrong or absent is therefore only ever a standalone-invocation or
workspace-layout problem, never a real build's -- see load_types' own
docstring for what happens when it is."""

from __future__ import annotations

import glob
import os

import yaml

from .buskind import CS_POOL_PROP_RE as _CS_POOL_PROP_RE
from .deps import Deps, touch, union
from .diag import LoadError, error
from .dtsio import MODULE_ROOT, parse_header_indices
from .model import ConnectorType, Position

#: The DEV/TEST fallback connector-type root (load_types' own default when
#: connector_dirs is None) -- MODULE_ROOT-relative, i.e. wherever rigc's
#: OWN source happens to live, which is this repo today but stops being
#: true the day the transpiler moves and the real connector types do not
#: move with it. Not the production path: cmake/modules/dts.cmake always threads
#: --connector-dir explicitly, so a real build never reaches this
#: fallback at all. Direct API / test use only.
BINDINGS = os.path.join(MODULE_ROOT, "dts", "bindings", "connectors")

#: socket,<kind>-<role>-cs-pool -- a named bus's own CS pool default,
#: keyed the qualified way. This module reads the raw binding dict,
#: board/project.py reads an already-built edtlib.EDT -- two different
#: inputs to the same fact; see buskind.py for the regex itself and why
#: it lives there rather than as a third verbatim copy.


def _socket_facts(binding: dict) -> tuple[bool, dict[str, list[int]]]:
    """(stackable, cs_pool) -- the socket-side type facts, read off the
    unified binding's own schema: mating multiplicity = presence of
    socket,stackable in the schema; default CS candidate lists, keyed by
    qualified bus name -- the legacy, role-less socket,cs-pool default
    always means the bare "spi" bus (CS only ever applies to SPI), and
    socket,<kind>-<role>-cs-pool is a named bus's own."""
    sprops = binding.get("properties", {})
    stackable = "socket,stackable" in sprops
    cs_pool: dict[str, list[int]] = {}
    legacy = sprops.get("socket,cs-pool")
    if legacy is not None:
        cs_pool["spi"] = list(legacy.get("default", []))
    for prop_name, meta in sprops.items():
        m = _CS_POOL_PROP_RE.match(prop_name)
        if m is None:
            continue
        cs_pool[m.group(1)] = list((meta or {}).get("default", []))
    return bool(stackable), cs_pool


def load_types(
    connector_dirs: list[str] | None = None,
    header_dirs: list[str] | None = None,
) -> tuple[dict[str, ConnectorType], Deps]:
    """Assemble every connector type found under connector_dirs (default:
    [BINDINGS]). header_dirs is the search list parse_header_indices
    resolves each type's <type>.h against (deliberately the SAME list a
    caller threads as --include-dir for cpp).

    connector_dirs=None (the default) falls back to [BINDINGS] -- a
    dev/test convenience, not the production path (see BINDINGS' own
    comment): a real build always threads --connector-dir explicitly. If
    that fallback is taken AND BINDINGS itself does not exist, this
    raises LoadError (lang-connector-root, unanchored, matching this
    module's other infra-level failure -- lang-cpp in dtsio.py) naming
    that directly, rather than silently returning an empty registry:
    with no types at all, the FIRST symptom a caller would otherwise see
    is loader/shields.py's own "unknown connector type" (lang-shield-type)
    on the first shield it checks -- correct as far as it goes, but far
    from the actual cause, and equally confusing whether zero shields or
    every shield in the corpus trips it. An EXPLICITLY passed
    connector_dirs that happens to not exist is NOT this case (see
    test_load_types_empty_directory_yields_no_types) -- an empty registry
    is exactly what a caller asking for zero roots means.

    Returns (types, deps) -- deps is every real file this call opened
    (dependency data is a returned value, never a mutable accumulator
    passed in and written to)."""
    used_default = connector_dirs is None
    if used_default and not os.path.isdir(BINDINGS):
        raise LoadError(
            error(
                "lang-connector-root",
                "no --connector-dir was given and the built-in fallback "
                f"({BINDINGS}) does not exist -- that fallback is a dev/test "
                "convenience, not the production path (a real build always "
                "threads --connector-dir explicitly, see cmake/modules/dts.cmake); "
                "either pass --connector-dir explicitly, or this is being run "
                "from a workspace where rigc's own source no longer sits "
                "alongside the real connector-type bindings it needs",
            )
        )
    dirs = connector_dirs if connector_dirs is not None else [BINDINGS]
    types: dict[str, ConnectorType] = {}
    deps: Deps = frozenset()
    for directory in dirs:
        for path in sorted(glob.glob(os.path.join(directory, "*.yaml"))):
            deps = union(deps, touch(path))
            with open(path) as f:
                binding = yaml.safe_load(f)
            name = os.path.splitext(os.path.basename(path))[0]

            stackable, cs_pool = _socket_facts(binding)

            indices, hdeps = parse_header_indices(name, header_dirs)
            deps = union(deps, hdeps)
            positions = {}
            for pname, meta in binding.get("plug,positions", {}).items():
                if pname not in indices:
                    raise KeyError(
                        f"unified binding for '{name}' names position "
                        f"'{pname}' which is not in "
                        f"dt-bindings/connector/{name}.h"
                    )
                positions[pname] = Position(
                    name=pname,
                    index=indices[pname],
                    function=meta.get("function", "gpio"),
                    optional=bool(meta.get("optional", False)),
                )

            types[name] = ConnectorType(
                name=name,
                positions=positions,
                index2name={v: k for k, v in indices.items()},
                bus_proxies=list(binding.get("plug,bus-proxies", [])),
                stackable=stackable,
                cs_pool=cs_pool,
            )
    return types, deps
