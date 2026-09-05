# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: registry -- the connector-type registry, assembled from a
synthetic unified binding + a synthetic dt-bindings/connector/<type>.h
index header (fixtures are purpose-built, never a copy of a real
connector type). No cpp/subprocess anywhere in this path --
`load_types`/`parse_header_indices` are pure file I/O.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from rigc.model import ConnectorType
from rigc.registry import load_types


def _write_type(
    root: Path, name: str, *, positions: dict, bus_proxies=(), stackable=True, cs_pool=()
) -> None:
    yaml_dir = root / "connectors"
    yaml_dir.mkdir(parents=True, exist_ok=True)
    header_dir = root / "include" / "dt-bindings" / "connector"
    header_dir.mkdir(parents=True, exist_ok=True)

    properties: dict = {}
    if stackable:
        properties["socket,stackable"] = {"type": "boolean"}
    if cs_pool:
        properties["socket,cs-pool"] = {"type": "array", "default": list(cs_pool)}

    binding = {
        "compatible": f"socket,{name}",
        "properties": properties,
        "plug,bus-proxies": list(bus_proxies),
        "plug,positions": {pname: {"function": func} for pname, func in positions.items()},
    }
    (yaml_dir / f"{name}.yaml").write_text(yaml.safe_dump(binding))

    # parse_header_indices strips the COMMON prefix shared by every
    # #define in the header (os.path.commonprefix) -- a single macro
    # would have its ENTIRE name "stripped" (empty string left), so a
    # synthetic header always carries a second, prefix-anchoring define
    # (never itself a claimable position) alongside the real ones, the
    # same shape every real dt-bindings/connector/<type>.h has by having
    # more than one position.
    prefix = f"{name.upper()}_"
    defines = [f"#define {prefix}ANCHOR\t999"]
    defines += [f"#define {prefix}{pname}\t{i}" for i, pname in enumerate(positions)]
    (header_dir / f"{name}.h").write_text(
        f"#ifndef DT_BINDINGS_CONNECTOR_{name.upper()}_H_\n"
        f"#define DT_BINDINGS_CONNECTOR_{name.upper()}_H_\n" + "\n".join(defines) + "\n#endif\n"
    )


def test_load_types_assembles_one_synthetic_type(tmp_path: Path) -> None:
    _write_type(
        tmp_path,
        "fixture_type",
        positions={"SIG0": "gpio", "SIG1": "gpio"},
        bus_proxies=["i2c"],
        stackable=True,
        cs_pool=[0],
    )
    types, _deps = load_types(
        connector_dirs=[str(tmp_path / "connectors")], header_dirs=[str(tmp_path / "include")]
    )
    assert set(types) == {"fixture_type"}
    ctype = types["fixture_type"]
    assert isinstance(ctype, ConnectorType)
    assert ctype.name == "fixture_type"
    assert ctype.bus_proxies == ["i2c"]
    assert ctype.stackable is True
    assert ctype.cs_pool == {"spi": [0]}
    assert set(ctype.positions) == {"SIG0", "SIG1"}
    assert ctype.positions["SIG0"].index == 0
    assert ctype.positions["SIG0"].function == "gpio"
    assert ctype.index2name[0] == "SIG0"
    assert ctype.index2name[1] == "SIG1"


def test_load_types_records_every_file_it_opened_as_deps(tmp_path: Path) -> None:
    _write_type(tmp_path, "fixture_type", positions={"SIG0": "gpio"})
    _types, deps = load_types(
        connector_dirs=[str(tmp_path / "connectors")], header_dirs=[str(tmp_path / "include")]
    )
    yaml_path = str((tmp_path / "connectors" / "fixture_type.yaml").resolve())
    header_path = str(
        (tmp_path / "include" / "dt-bindings" / "connector" / "fixture_type.h").resolve()
    )
    assert yaml_path in deps
    assert header_path in deps


def test_load_types_empty_directory_yields_no_types(tmp_path: Path) -> None:
    types, deps = load_types(connector_dirs=[str(tmp_path / "nonexistent")])
    assert types == {}
    assert deps == frozenset()


def test_load_types_posname_falls_back_for_an_unknown_index(tmp_path: Path) -> None:
    _write_type(tmp_path, "fixture_type", positions={"SIG0": "gpio"})
    types, _ = load_types(
        connector_dirs=[str(tmp_path / "connectors")], header_dirs=[str(tmp_path / "include")]
    )
    ctype = types["fixture_type"]
    assert ctype.posname(0) == "SIG0"
    assert ctype.posname(99) == "position 99"


def test_load_types_stackable_false_when_key_absent(tmp_path: Path) -> None:
    _write_type(tmp_path, "fixture_type", positions={}, stackable=False)
    types, _ = load_types(
        connector_dirs=[str(tmp_path / "connectors")], header_dirs=[str(tmp_path / "include")]
    )
    assert types["fixture_type"].stackable is False


def test_load_types_widens_cs_pool_per_named_bus(tmp_path: Path) -> None:
    """A multi-bus connector type's cs_pool is keyed by the QUALIFIED bus
    name -- a named bus's own "socket,<kind>-<role>-cs-pool" default,
    alongside (in a different type) the legacy role-less "socket,cs-pool"
    default, which always means the bare "spi" bus."""
    yaml_dir = tmp_path / "connectors"
    yaml_dir.mkdir(parents=True)
    header_dir = tmp_path / "include" / "dt-bindings" / "connector"
    header_dir.mkdir(parents=True)
    binding = {
        "compatible": "socket,fixture_multibus",
        "properties": {
            "socket,spi-sensors-cs-pool": {"type": "array", "default": [10]},
            "socket,spi-motors-cs-pool": {"type": "array", "default": [11]},
        },
        "plug,bus-proxies": ["spi-sensors", "spi-motors"],
        "plug,positions": {},
    }
    (yaml_dir / "fixture_multibus.yaml").write_text(yaml.safe_dump(binding))
    (header_dir / "fixture_multibus.h").write_text(
        "#ifndef DT_BINDINGS_CONNECTOR_FIXTURE_MULTIBUS_H_\n"
        "#define DT_BINDINGS_CONNECTOR_FIXTURE_MULTIBUS_H_\n"
        "#endif\n"
    )

    types, _ = load_types(connector_dirs=[str(yaml_dir)], header_dirs=[str(tmp_path / "include")])

    assert types["fixture_multibus"].cs_pool == {"spi-sensors": [10], "spi-motors": [11]}
