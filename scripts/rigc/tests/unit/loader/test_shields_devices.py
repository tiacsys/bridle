# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: shields -- device attribution (bus membership, group placement,
declared_params/param-includes) and address-authority/unit-address
validation, plus position-ref resolution (gpio/pwm/adc claims onto the
plug or a jumper).

Split out of the former test_shields.py (test_shields_plugs.py holds
plug identity and placement rules; test_shields_exposed.py holds exposed
sockets; test_shields_elements.py holds pads/straps/jumpers and the
shared label requirement) -- see tests/unit/loader/conftest.py for the
synthetic connector-type/DT fixtures every module here shares.
"""

from __future__ import annotations

from rigc.loader.shields import parse_shields
from rigc.model import ConnectorType

from .conftest import _dt, _one_shield

# ---------------------------------------------------------------- devices


def test_device_bus_membership_by_parentage(tmp_path) -> None:
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";

\t\t\t\ti2c {
\t\t\t\t\tdev1: dev@50 { compatible = "vnd,thing"; reg = <0x50>; };
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    dev = shields["fx"].devices[0]
    assert dev.name == "dev"
    assert dev.label == "dev1"
    assert dev.bus == "i2c"
    assert dev.group is None
    assert dev.reg == 0x50
    assert dev.compatible == "vnd,thing"


def test_device_bus_membership_by_a_qualified_named_bus_proxy(tmp_path) -> None:
    """A multi-bus connector type names an additional bus of a kind by
    suffixing the kind with a role (bus_proxies, an open string list, is
    already wide enough for this -- shields.py needs no code change to
    recognize one: a device group node literally named "spi-motors"
    matches it exactly as "spi"/"i2c" match today)."""
    named_type = ConnectorType(
        name="fixture-multibus",
        positions={},
        index2name={},
        bus_proxies=["spi-sensors", "spi-motors"],
        stackable=False,
        cs_pool={},
    )
    dt = _dt(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-multibus";

\t\t\t\tspi-motors {
\t\t\t\t\tdrv: drv8825@0 { compatible = "vnd,motor-driver"; };
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    shields, diags = parse_shields(dt, {"fixture-multibus": named_type})

    assert diags == []
    dev = shields["fx"].devices[0]
    assert dev.bus == "spi-motors"
    assert dev.group is None


def test_device_in_a_non_bus_group_gets_the_group_name(tmp_path) -> None:
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tgpio {
\t\t\t\tbtn: button {
\t\t\t\t\tgpios = <&plug 0 1>;
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    dev = shields["fx"].devices[0]
    assert dev.bus is None
    assert dev.group == "gpio"


def test_unrecognized_bus_proxy_group_is_rejected(tmp_path) -> None:
    """A group named like a bus (i2c/spi/uart) that the plug binding does
    NOT allow as a proxy -- lang-shield-proxy, a hand-differential rule
    with no frozen golden behind it."""
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";

\t\t\t\tuart {
\t\t\t\t\tdev1: dev@1 { compatible = "vnd,thing"; };
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-shield-proxy"


def test_unrecognized_qualified_bus_proxy_group_is_rejected(tmp_path) -> None:
    """A ROLE-QUALIFIED group name ("spi-nonexistent-role") that still
    names a recognized kind (spi) but is NOT in this connector type's own
    bus_proxies vocabulary must raise lang-shield-proxy exactly like an
    unqualified name does -- the kind-prefix check that recognizes
    "spi-nonexistent-role" as bus-shaped at all must not stop at the
    three bare kind names."""
    named_type = ConnectorType(
        name="fixture-multibus",
        positions={},
        index2name={},
        bus_proxies=["spi-sensors", "spi-motors"],
        stackable=False,
        cs_pool={},
    )
    dt = _dt(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-multibus";

\t\t\t\tspi-nonexistent-role {
\t\t\t\t\tdev1: dev@0 { compatible = "vnd,thing"; };
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    shields, diags = parse_shields(dt, {"fixture-multibus": named_type})

    assert len(diags) == 1
    assert diags[0].code == "lang-shield-proxy"
    dev = shields["fx"].devices[0]
    assert dev.bus is None
    assert dev.group == "spi-nonexistent-role"


def test_declared_params_from_shield_params(tmp_path) -> None:
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";

\t\t\t\ti2c {
\t\t\t\t\tdev1: dev@50 {
\t\t\t\t\t\tcompatible = "vnd,thing";
\t\t\t\t\t\treg = <0x50>;
\t\t\t\t\t\tshield,params = "vnd,threshold";
\t\t\t\t\t};
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    dev = shields["fx"].devices[0]
    assert dev.declared_params == ["vnd,threshold"]
    assert dev.extra_props == [("compatible", 'compatible = "vnd,thing";')]


def test_declared_param_includes_from_shield_param_includes(tmp_path) -> None:
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";

\t\t\t\ti2c {
\t\t\t\t\tdev1: dev@50 {
\t\t\t\t\t\tcompatible = "vnd,thing";
\t\t\t\t\t\treg = <0x50>;
\t\t\t\t\t\tshield,params = "vnd,threshold";
\t\t\t\t\t\tshield,param-includes = "vnd/threshold.h";
\t\t\t\t\t};
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    dev = shields["fx"].devices[0]
    assert dev.declared_param_includes == ["vnd/threshold.h"]
    # excluded from the passthrough allowlist -- it is a rigc-only
    # vocabulary declaration, never a real DTS property to render.
    assert dev.extra_props == [("compatible", 'compatible = "vnd,thing";')]


def test_authored_default_shows_up_in_extra_props(tmp_path) -> None:
    """A declared param WITH an authored default is OPTIONAL: its name
    appears among extra_props too -- the invariant check's own "may be
    omitted" signal."""
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";

\t\t\t\ti2c {
\t\t\t\t\tdev1: dev@50 {
\t\t\t\t\t\tcompatible = "vnd,thing";
\t\t\t\t\t\treg = <0x50>;
\t\t\t\t\t\tshield,params = "vnd,threshold";
\t\t\t\t\t\tvnd,threshold = <10>;
\t\t\t\t\t};
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    dev = shields["fx"].devices[0]
    names = [n for n, _ in dev.extra_props]
    assert "vnd,threshold" in names


def test_addr_authority_rejects_both_reg_and_addr_from(tmp_path) -> None:
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";

\t\t\t\ti2c {
\t\t\t\t\tdev1: dev@50 {
\t\t\t\t\t\tcompatible = "vnd,thing";
\t\t\t\t\t\treg = <0x50>;
\t\t\t\t\t\tshield,addr-from = <&addr_strap>;
\t\t\t\t\t};
\t\t\t\t};
\t\t\t};
\t\t\tconfig {
\t\t\t\taddr_strap: addr-strap {
\t\t\t\t\tshield,domain = <0x48 0>, <0x49 1>;
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-addr-authority"
    assert "both" in diags[0].message


def test_addr_authority_rejects_neither_reg_nor_addr_from(tmp_path) -> None:
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";

\t\t\t\ti2c {
\t\t\t\t\tdev1: dev@50 { compatible = "vnd,thing"; };
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-addr-authority"
    assert "neither" in diags[0].message


def test_addr_authority_rule_applies_to_a_qualified_named_i2c_bus(tmp_path) -> None:
    """The address-authority rule (exactly one of reg / shield,addr-from)
    is a fact of the I2C KIND, not of the bare string "i2c" -- a device
    on a role-suffixed i2c bus a multi-bus connector type offers
    ("i2c-sensors") must be checked exactly like a device on bare "i2c",
    never silently skipped because the literal string differs."""
    named_type = ConnectorType(
        name="fixture-multibus",
        positions={},
        index2name={},
        bus_proxies=["i2c-sensors"],
        stackable=False,
        cs_pool={},
    )
    dt = _dt(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-multibus";

\t\t\t\ti2c-sensors {
\t\t\t\t\tdev1: dev@50 { compatible = "vnd,thing"; };
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    shields, diags = parse_shields(dt, {"fixture-multibus": named_type})

    assert len(diags) == 1
    assert diags[0].code == "lang-addr-authority"
    assert "neither" in diags[0].message
    assert shields["fx"].devices[0].bus == "i2c-sensors"


def test_addr_from_must_point_at_a_strap(tmp_path) -> None:
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";

\t\t\t\ti2c {
\t\t\t\t\tdev1: dev@50 {
\t\t\t\t\t\tcompatible = "vnd,thing";
\t\t\t\t\t\tshield,addr-from = <&plug>;
\t\t\t\t\t};
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    assert diags[0].code == "lang-addr-from"


def test_unit_address_must_match_authored_reg(tmp_path) -> None:
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";

\t\t\t\ti2c {
\t\t\t\t\tdev1: dev@51 { compatible = "vnd,thing"; reg = <0x50>; };
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-unit-addr"
    assert "!=" in diags[0].message


def test_symbolic_unit_address_with_authored_reg_is_rejected(tmp_path) -> None:
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";

\t\t\t\ti2c {
\t\t\t\t\tdev1: dev@symbolic { compatible = "vnd,thing"; reg = <0x50>; };
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-unit-addr"
    assert "symbolic markers are for deferred" in diags[0].message


# ---------------------------------------------------------------- position refs


def test_gpio_position_ref_on_the_plug(tmp_path) -> None:
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tgpio {
\t\t\t\tbtn: button { gpios = <&plug 0 3>; };
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    dev = shields["fx"].devices[0]
    ref = dev.function_refs[0]
    assert ref.position == 0
    assert ref.flags == 3
    assert ref.function == "gpio"
    assert ref.jumper is None


def test_gpio_position_ref_deferred_to_a_jumper(tmp_path) -> None:
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tconfig {
\t\t\t\tirq_jmp: irq-jmp {
\t\t\t\t\t#gpio-cells = <1>;
\t\t\t\t\tshield,position-domain = <0 0>, <1 1>;
\t\t\t\t};
\t\t\t};
\t\t\tgpio {
\t\t\t\tbtn: button { gpios = <&irq_jmp 1>; };
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    ref = shields["fx"].devices[0].function_refs[0]
    assert ref.position is None
    assert ref.jumper == "irq-jmp"
    assert ref.flags == 1


def test_position_ref_must_target_the_plug_or_a_jumper(tmp_path) -> None:
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";

\t\t\t\ti2c {
\t\t\t\t\tother: other@50 { compatible = "vnd,thing"; reg = <0x50>; };
\t\t\t\t};
\t\t\t};
\t\t\tgpio {
\t\t\t\tbtn: button { gpios = <&other 0 1>; };
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-pos-ref"
    assert "must reference THIS shield's plug node" in diags[0].message


def test_position_index_must_exist_on_the_connector_type(tmp_path) -> None:
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tgpio {
\t\t\t\tbtn: button { gpios = <&plug 99 1>; };
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-position"
    assert "does not exist" in diags[0].message


def test_position_must_be_claimable_not_bus_copper(tmp_path) -> None:
    """index 2 (BUS_COPPER) exists on the header but is not a claimable
    plug,positions entry -- electrical realization is not modeled."""
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tgpio {
\t\t\t\tbtn: button { gpios = <&plug 2 1>; };
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-position"
    assert "bus copper" in diags[0].message
