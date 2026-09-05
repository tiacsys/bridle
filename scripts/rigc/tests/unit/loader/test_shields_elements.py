# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: shields -- pads/straps/jumpers (config-block elements) and the
label requirement shared by every rig-facing reference surface (device,
pad, strap, jumper, exposed socket): each must resolve by DTS LABEL,
never by node name, and each is a loud lang-shield-label error with no
label at all.

Split out of the former test_shields.py -- see
tests/unit/loader/conftest.py for the synthetic connector-type/DT
fixtures every module here shares.
"""

from __future__ import annotations

from rigc.loader.shields import parse_shields
from rigc.model import Jumper, Pad, Strap

from .conftest import _PLURAL_TYPES, _dt, _one_shield

# ---------------------------------------------------------------- pads/straps/jumpers


def test_pads_straps_jumpers_and_lookup_helpers(tmp_path) -> None:
    """`config_element`/`by_name`/`names()` all resolve by DTS LABEL,
    never by node name -- exercised here via `addr_strap`/
    `addr-strap` and `irq_jmp`/`irq-jmp`, which deliberately differ (the
    real corpus's own naming convention), so a same-spelling coincidence
    can never hide a label-vs-name bug."""
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tpads {
\t\t\t\tsq: sq { shield,role = "driver"; };
\t\t\t};
\t\t\tconfig {
\t\t\t\taddr_strap: addr-strap {
\t\t\t\t\tshield,domain = <0x48 0>, <0x49 1>;
\t\t\t\t\tshield,sheet-label = "ADDR";
\t\t\t\t};
\t\t\t\tirq_jmp: irq-jmp {
\t\t\t\t\t#gpio-cells = <1>;
\t\t\t\t\tshield,position-domain = <0 0>, <1 1>;
\t\t\t\t\tshield,sheet-label = "IRQ";
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    shield = shields["fx"]
    assert isinstance(shield.pads["sq"], Pad)
    assert shield.pads["sq"].role == "driver"
    assert isinstance(shield.straps["addr-strap"], Strap)
    assert shield.straps["addr-strap"].label == "addr_strap"
    assert shield.straps["addr-strap"].domain == [(0x48, 0), (0x49, 1)]
    assert isinstance(shield.jumpers["irq-jmp"], Jumper)
    assert shield.jumpers["irq-jmp"].label == "irq_jmp"
    assert shield.jumpers["irq-jmp"].domain == [(0, 0), (1, 1)]
    assert shield.jumpers["irq-jmp"].positions() == [0, 1]
    assert shield.jumpers["irq-jmp"].state_of(1) == 1
    assert shield.jumpers["irq-jmp"].state_of(99) is None

    # by LABEL resolves; the node-name spelling is REJECTED outright,
    # never a fallback.
    assert shield.config_element("addr_strap") is shield.straps["addr-strap"]
    assert shield.config_element("addr-strap") is None
    assert shield.config_element("irq_jmp") is shield.jumpers["irq-jmp"]
    assert shield.config_element("irq-jmp") is None
    assert shield.config_element("no-such") is None

    assert shield.by_name("sq") == [shield.pads["sq"]]
    assert shield.by_name("addr_strap") == [shield.straps["addr-strap"]]
    assert shield.by_name("addr-strap") == []
    assert shield.by_name("no-such") == []
    assert shield.names() == sorted(["sq", "addr_strap"])


def test_unlabeled_device_is_a_loud_error(tmp_path) -> None:
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";

\t\t\t\ti2c {
\t\t\t\t\tdev@50 { compatible = "vnd,thing"; reg = <0x50>; };
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-shield-label"
    assert "device 'dev@50'" in diags[0].message
    assert "fx" in diags[0].message
    assert "no DTS label" in diags[0].message


def test_unlabeled_pad_is_a_loud_error(tmp_path) -> None:
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tpads {
\t\t\t\tsq { shield,role = "driver"; };
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-shield-label"
    assert "pad 'sq'" in diags[0].message
    assert "no DTS label" in diags[0].message


def test_unlabeled_strap_is_a_loud_error(tmp_path) -> None:
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tconfig {
\t\t\t\taddr-strap {
\t\t\t\t\tshield,domain = <0x48 0>;
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-shield-label"
    assert "strap 'addr-strap'" in diags[0].message
    assert "no DTS label" in diags[0].message


def test_unlabeled_jumper_is_a_loud_error(tmp_path) -> None:
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tconfig {
\t\t\t\tirq-jmp {
\t\t\t\t\t#gpio-cells = <1>;
\t\t\t\t\tshield,position-domain = <0 0>;
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-shield-label"
    assert "jumper 'irq-jmp'" in diags[0].message
    assert "no DTS label" in diags[0].message


def test_unlabeled_exposed_socket_is_a_loud_error(tmp_path) -> None:
    """The fourth (and last) rig-facing reference surface: an exposed
    socket with no DTS label goes through the same `_require_label`
    helper devices/pads/straps/jumpers do, rather than falling back to
    the node name silently."""
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tmb1 {
\t\t\t\tcompatible = "socket,mikrobus";
\t\t\t\t#gpio-cells = <2>;
\t\t\t\tsocket,i2c = <&plug>;
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-shield-label"
    assert "exposed socket 'mb1'" in diags[0].message
    assert "fx" in diags[0].message
    assert "no DTS label" in diags[0].message


def test_exposed_socket_label_is_the_naming_authority(tmp_path) -> None:
    """`Shield.exposed_socket` resolves by DTS LABEL, never by node name
    -- exercised with a label that DIFFERS from the node name (`span_ch0`
    labelling `ch0`), since the real corpus's own 8 exposed nodes all
    happen to share the two spellings and so cannot show which one
    actually resolves."""
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tspan_ch0: ch0 {
\t\t\t\tcompatible = "socket,mikrobus";
\t\t\t\t#gpio-cells = <2>;
\t\t\t\tsocket,i2c = <&plug>;
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    shield = shields["fx"]
    assert shield.exposes["ch0"].label == "span_ch0"
    assert shield.exposed_socket("span_ch0") is shield.exposes["ch0"]
    assert shield.exposed_socket("ch0") is None
    assert shield.exposed_socket("no-such") is None


def test_invalid_pad_role_is_rejected(tmp_path) -> None:
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tpads {
\t\t\t\tsq: sq { shield,role = "nonsense"; };
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-pad-role"


def test_plural_shield_straps_are_unaffected_template_level_facts(tmp_path) -> None:
    """Straps (address-domain, bus-scoped) are NOT refused on a plural
    shield -- only routing jumpers are."""
    dt = _dt(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tleft_plug: left {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t\ti2c {
\t\t\t\t\tdevl: devl@addr_strap {
\t\t\t\t\t\tcompatible = "vnd,thing";
\t\t\t\t\t\tshield,addr-from = <&addr_strap>;
\t\t\t\t\t};
\t\t\t\t};
\t\t\t};
\t\t\tright_plug: right {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tconfig {
\t\t\t\taddr_strap: addr-strap {
\t\t\t\t\tshield,domain = <0x48 0>, <0x49 1>;
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    shields, diags = parse_shields(dt, _PLURAL_TYPES)
    assert diags == []
    assert "addr-strap" in shields["fx"].straps
