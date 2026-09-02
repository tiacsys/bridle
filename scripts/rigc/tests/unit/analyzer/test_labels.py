# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Emission feasibility of generated labels: the deterministic
`<instance>_<shield label>` scheme must be collision-free -- checked over
minimal constructed Rig/Instance/Device values."""

from __future__ import annotations

from rigc.analyzer.labels import check_labels
from rigc.model import Device, Instance, Rig, Shield


def _dev(name: str, label: str) -> Device:
    return Device(
        name=name,
        label=label,
        compatible=None,
        bus=None,
        group=None,
        reg=None,
        addr_from=None,
        cs_position=None,
    )


def _inst(name: str, *devices: Device) -> Instance:
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=list(devices))
    return Instance(name=name, shield=shield, sockets={"plug": "sock"})


def test_distinct_instance_names_never_collide() -> None:
    rig = Rig(
        name="r",
        instances=[
            _inst("logger_1", _dev("rtc", "rtc")),
            _inst("logger_2", _dev("rtc", "rtc")),
        ],
    )
    assert check_labels(rig) == []


def test_two_devices_of_one_instance_generate_distinct_labels() -> None:
    rig = Rig(
        name="r",
        instances=[
            _inst("i1", _dev("a", "a_lbl"), _dev("b", "b_lbl")),
        ],
    )
    assert check_labels(rig) == []


def test_a_generated_label_collision_is_phys_label() -> None:
    """Two devices whose SHIELD-LOCAL labels are identical, on the same
    instance, generate the identical <instance>_<label> pair -- the
    deterministic naming scheme cannot disambiguate them."""
    rig = Rig(
        name="r",
        instances=[
            _inst("i1", _dev("a", "same"), _dev("b", "same")),
        ],
    )
    diags = check_labels(rig)
    assert len(diags) == 1
    assert diags[0].code == "phys-label"


def test_check_labels_runs_regardless_of_socket_resolution() -> None:
    """Unlike every other pass, label collision is a property of instance
    NAME + device LABEL alone -- it needs no resolved socket, so it never
    skips an instance the way sockets.get(inst.name) would."""
    rig = Rig(
        name="r",
        instances=[
            _inst("i1", _dev("a", "same"), _dev("b", "same")),
        ],
    )
    # No sockets dict is even passed to check_labels -- its signature
    # takes only `rig`, proving the point structurally.
    diags = check_labels(rig)
    assert len(diags) == 1
