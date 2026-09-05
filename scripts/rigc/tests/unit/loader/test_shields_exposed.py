# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: shields -- exposed-socket parsing: gpio/pwm/adc channel maps,
bus/channel resolution (scope vs. plug-slot markers), cs-pool overrides,
and the plural-shield variants of each (a gpio-map row or socket,<bus>
resolving through one of several plugs, recorded per marker).

Split out of the former test_shields.py -- see
tests/unit/loader/conftest.py for the synthetic connector-type/DT
fixtures every module here shares.
"""

from __future__ import annotations

from rigc.loader.shields import parse_shields

from .conftest import _PLURAL_TYPES, _dt, _one_shield

# ---------------------------------------------------------------- exposed sockets


def test_exposed_socket_pass_through(tmp_path) -> None:
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tmb1: mb1 {
\t\t\t\tcompatible = "socket,mikrobus";
\t\t\t\t#gpio-cells = <2>;
\t\t\t\tgpio-map = <0 0 &plug 1 0>;
\t\t\t\tsocket,i2c = <&plug>;
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    exp = shields["fx"].exposes["mb1"]
    assert exp.type_name == "mikrobus"
    assert exp.gpio_map == {0: ("plug", 1, 0)}
    assert exp.buses["i2c"] == ("plug", "plug")


def test_exposed_socket_cs_pool_qualified_and_bare_both_parse(tmp_path) -> None:
    """A bare socket,cs-pool override lands in the "spi" entry; a
    qualified socket,<kind>-<role>-cs-pool lands under its OWN
    qualified key -- mirrors board/project.py's/registry.py's own
    _CS_POOL_PROP_RE."""
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tmb1: mb1 {
\t\t\t\tcompatible = "socket,fixture-multibus";
\t\t\t\t#gpio-cells = <2>;
\t\t\t\tsocket,cs-pool = <3 4>;
\t\t\t\tsocket,spi-sensors-cs-pool = <5 6>;
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    exp = shields["fx"].exposes["mb1"]
    assert exp.cs_pool == {"spi": [3, 4], "spi-sensors": [5, 6]}


def test_exposed_socket_new_scope_on_a_device(tmp_path) -> None:
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";

\t\t\t\ti2c {
\t\t\t\t\tmux: mux@70 { compatible = "vnd,mux"; reg = <0x70>; };
\t\t\t\t};
\t\t\t};
\t\t\tch0: ch0 {
\t\t\t\tcompatible = "socket,i2c-port";
\t\t\t\tsocket,i2c = <&mux>;
\t\t\t\tshield,channel = <0>;
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    exp = shields["fx"].exposes["ch0"]
    assert exp.buses["i2c"] == ("scope", "mux")
    assert exp.channel == 0


def test_exposed_socket_bus_prop_must_be_plug_or_device(tmp_path) -> None:
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tpads {
\t\t\t\tsq: sq { };
\t\t\t};
\t\t\tch0: ch0 {
\t\t\t\tcompatible = "socket,i2c-port";
\t\t\t\tsocket,i2c = <&sq>;
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-exposed"


# --------------------------------------- exposed sockets: pwm/adc pass-through


def test_exposed_socket_pwm_and_adc_pass_through(tmp_path) -> None:
    """pwm-map/io-channel-map parse the SAME way gpio-map already does --
    slot-widened (parent SLOT, parent plug position, filler) -- and each
    map's own declared cell count is captured for compose_socket's own
    require-and-check: a map with no matching cells declaration (or the
    reverse) is a parse-time rejection."""
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tao: ao {
\t\t\t\tcompatible = "socket,grove";
\t\t\t\t#gpio-cells = <2>;
\t\t\t\tgpio-map = <0 0 &plug 0 0>;
\t\t\t\t#pwm-cells = <2>;
\t\t\t\tpwm-map = <0 0 &plug 0 0 0>;
\t\t\t\t#io-channel-cells = <1>;
\t\t\t\tio-channel-map = <0 &plug 0>;
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    exp = shields["fx"].exposes["ao"]
    assert exp.pwm_cells == 2
    assert exp.pwm_map == {0: ("plug", 0, 0)}
    assert exp.adc_cells == 1
    assert exp.adc_map == {0: ("plug", 0, 0)}


def test_exposed_socket_pwm_map_two_rows(tmp_path) -> None:
    """Multi-row stride derivation: TWO pwm-map rows parse to two entries,
    proving the derived (not hardcoded) stride advances `i` correctly."""
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tao: ao {
\t\t\t\tcompatible = "socket,grove";
\t\t\t\t#gpio-cells = <2>;
\t\t\t\tgpio-map = <0 0 &plug 0 0>, <1 0 &plug 1 0>;
\t\t\t\t#pwm-cells = <2>;
\t\t\t\tpwm-map = <0 0 &plug 0 0 0>, <1 0 &plug 1 0 0>;
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    exp = shields["fx"].exposes["ao"]
    assert exp.pwm_map == {0: ("plug", 0, 0), 1: ("plug", 1, 0)}


def test_exposed_socket_pwm_map_without_pwm_cells_is_rejected(tmp_path) -> None:
    """A pwm-map with no #pwm-cells alongside it
    is a parse-time lang-exposed error, not a guess at the stride."""
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tao: ao {
\t\t\t\tcompatible = "socket,grove";
\t\t\t\t#gpio-cells = <2>;
\t\t\t\tgpio-map = <0 0 &plug 0 0>;
\t\t\t\tpwm-map = <0 0 &plug 0 0>;
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-exposed"
    assert "#pwm-cells" in diags[0].message
    exp = shields["fx"].exposes["ao"]
    assert exp.pwm_map == {}
    assert exp.pwm_cells is None


def test_exposed_socket_pwm_cells_without_pwm_map_is_rejected(tmp_path) -> None:
    """The reverse pairing -- #pwm-cells with no pwm-map -- is equally a
    parse-time lang-exposed error."""
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tao: ao {
\t\t\t\tcompatible = "socket,grove";
\t\t\t\t#gpio-cells = <2>;
\t\t\t\tgpio-map = <0 0 &plug 0 0>;
\t\t\t\t#pwm-cells = <2>;
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-exposed"
    assert "pwm-map" in diags[0].message


def test_exposed_socket_io_channel_map_without_cells_is_rejected(tmp_path) -> None:
    """Same require-and-check, ADC side (#io-channel-cells / io-channel-map)."""
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tao: ao {
\t\t\t\tcompatible = "socket,grove";
\t\t\t\t#gpio-cells = <2>;
\t\t\t\tgpio-map = <0 0 &plug 0 0>;
\t\t\t\tio-channel-map = <0 &plug 0>;
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-exposed"
    assert "#io-channel-cells" in diags[0].message
    exp = shields["fx"].exposes["ao"]
    assert exp.adc_map == {}
    assert exp.adc_cells is None


def test_exposed_socket_pwm_map_parent_must_be_a_plug(tmp_path) -> None:
    """Mirrors gpio-map's own parent-must-be-a-plug check (lang-exposed) --
    a pwm-map row pointing at anything else (here, a pad, which declares
    no #pwm-cells of its own -- so the row's parent side is read at the
    3-cell generic Zephyr default, _FUNCTION_DEFAULT_CELLS) is rejected
    the same way."""
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tpads {
\t\t\t\tsq: sq { };
\t\t\t};
\t\t\tao: ao {
\t\t\t\tcompatible = "socket,grove";
\t\t\t\t#gpio-cells = <2>;
\t\t\t\tgpio-map = <0 0 &plug 0 0>;
\t\t\t\t#pwm-cells = <2>;
\t\t\t\tpwm-map = <0 0 &sq 0 0 0>;
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-exposed"
    assert "pwm-map parent must be" in diags[0].message


def test_exposed_socket_pwm_map_stride_from_a_three_cell_plug(tmp_path) -> None:
    """The plug's OWN declared #pwm-cells drives the PARENT half of the
    stride (mirroring _parse_pos_ref's own _ncells(target, function)
    lookup) -- a 3-cell plug makes each row 6 words (2 child + phandle +
    3 parent), never the 5 a 2-cell plug needs, so this must still parse
    (not truncate) when the plug declares 3."""
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tao: ao {
\t\t\t\tcompatible = "socket,grove";
\t\t\t\t#gpio-cells = <2>;
\t\t\t\tgpio-map = <0 0 &plug 0 0>;
\t\t\t\t#pwm-cells = <2>;
\t\t\t\tpwm-map = <0 0 &plug 0 0 0>;
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    exp = shields["fx"].exposes["ao"]
    assert exp.pwm_map == {0: ("plug", 0, 0)}
    assert exp.pwm_cells == 2


def test_plural_shield_exposed_socket_mixed_parents(tmp_path) -> None:
    """A plural shield MAY declare an exposed socket -- each gpio-map
    row and each socket,<bus> resolves through ONE of the carrier's
    plugs, and the marker/tuple RECORDS which one, exactly like the
    single-plug form's own "plug" slot does."""
    dt = _dt(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tleft_plug: left {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tright_plug: right {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tcombined: combined {
\t\t\t\tcompatible = "socket,mikrobus";
\t\t\t\t#gpio-cells = <2>;
\t\t\t\tgpio-map = <0 0 &left_plug 0 0>,
\t\t\t\t\t   <1 0 &right_plug 1 0>;
\t\t\t\tsocket,i2c = <&right_plug>;
\t\t\t};
\t\t};
""",
    )
    shields, diags = parse_shields(dt, _PLURAL_TYPES)
    assert diags == []
    exp = shields["fx"].exposes["combined"]
    assert exp.gpio_map == {0: ("left", 0, 0), 1: ("right", 1, 0)}
    assert exp.buses["i2c"] == ("plug", "right")


def test_plural_shield_exposed_socket_gpio_map_parent_must_be_a_plug(tmp_path) -> None:
    """A gpio-map row's phandle must name one of the carrier's OWN plugs
    -- naming any other node of the shield is rejected, worded to list
    the carrier's plugs (plural) rather than the singular single-plug
    wording."""
    dt = _dt(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tleft_plug: left {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tright_plug: right {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tpads {
\t\t\t\tsq: sq { };
\t\t\t};
\t\t\tcombined: combined {
\t\t\t\tcompatible = "socket,mikrobus";
\t\t\t\t#gpio-cells = <2>;
\t\t\t\tgpio-map = <0 0 &sq 0 0>;
\t\t\t};
\t\t};
""",
    )
    shields, diags = parse_shields(dt, _PLURAL_TYPES)
    assert len(diags) == 1
    assert diags[0].code == "lang-exposed"
    assert "one of the carrier's plugs" in diags[0].message
    assert shields["fx"].exposes["combined"].gpio_map == {}


def test_exposed_socket_qualified_bus_name_the_type_does_not_declare_is_rejected(tmp_path) -> None:
    """The child-side qualified bus name is validated exact-match
    against the exposed type's OWN declared bus_proxies, no fallback --
    "spi" is not among fixture-type-2's own vocabulary (i2c only)."""
    dt = _dt(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tch0: ch0 {
\t\t\t\tcompatible = "socket,fixture-type-2";
\t\t\t\t#gpio-cells = <2>;
\t\t\t\tsocket,spi = <&plug>;
\t\t\t};
\t\t};
""",
    )
    shields, diags = parse_shields(dt, _PLURAL_TYPES)
    assert len(diags) == 1
    assert diags[0].code == "lang-exposed"
    assert "does not declare" in diags[0].message
    assert shields["fx"].exposes["ch0"].buses == {}
