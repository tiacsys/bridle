# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Shared synthetic fixtures for the shields unit-test split
(test_shields_plugs / _devices / _exposed / _elements).

Every DT below is built with dtlib.DT() DIRECTLY from hand-written,
already-preprocessed text -- no cpp, no subprocess (the cpp/unit-test
seam) -- and every connector type is a PURPOSE-BUILT synthetic value,
never a real corpus one.
"""

from __future__ import annotations

from rigc.dtsio import get_dtlib
from rigc.loader.shields import parse_shields
from rigc.model import ConnectorType, Position

_PLUG_TYPE = ConnectorType(
    name="fixture-type",
    positions={
        "P0": Position(name="P0", index=0, function="gpio"),
        "P1": Position(name="P1", index=1, function="gpio"),
        # BUS_COPPER (index 2) is deliberately ABSENT here -- it exists
        # on index2name (the header's full index) but is not a claimable
        # plug,positions entry.
    },
    index2name={0: "P0", 1: "P1", 2: "BUS_COPPER"},
    bus_proxies=["i2c", "spi"],
    stackable=True,
    cs_pool={},
)
# BUS_COPPER (index 2) is NOT in .positions -- it exists on the header
# (index2name) but is bus copper, not a claimable position (mirrors real
# connector types' D11-D13-doubles-as-SPI shape).
_TYPES = {"fixture-type": _PLUG_TYPE}


def _dt(tmp_path, body: str):
    path = tmp_path / "fixture.dts"
    path.write_text(f"/dts-v1/;\n/ {{\n\tshield-templates {{\n{body}\n\t}};\n}};\n")
    return get_dtlib().DT(str(path))


def _one_shield(tmp_path, body: str):
    dt = _dt(tmp_path, body)
    shields, diags = parse_shields(dt, _TYPES)
    return shields, diags


# A second connector type distinct from _PLUG_TYPE, so a two-slot shield
# naming one of each proves per-slot resolution against genuinely
# different types, never accidentally sharing one ConnectorType object.
_PLUG_TYPE_2 = ConnectorType(
    name="fixture-type-2",
    positions={"Q0": Position(name="Q0", index=0, function="gpio")},
    index2name={0: "Q0"},
    bus_proxies=["i2c"],
    stackable=True,
    cs_pool={},
)
_PLURAL_TYPES = {"fixture-type": _PLUG_TYPE, "fixture-type-2": _PLUG_TYPE_2}
