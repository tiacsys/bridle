# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: shields -- plug identity and the shield-template model's
placement rules: which children of a template (or of a plug) may
declare a bus group vs. a plain device group, at both plug counts (one
vs. many), plus the plural-shield-only restrictions (no routing jumper
across plugs; a plug node declares no cell counts of its own).

Split out of the former test_shields.py (test_shields_devices.py holds
device attribution/addressing and position refs; test_shields_exposed.py
holds exposed sockets; test_shields_elements.py holds pads/straps/
jumpers and the shared label requirement) -- see
tests/unit/loader/conftest.py for the synthetic connector-type/DT
fixtures every module here shares.
"""

from __future__ import annotations

from textwrap import dedent

from rigc.dtsio import get_dtlib
from rigc.loader.shields import parse_shields

from .conftest import _PLURAL_TYPES, _TYPES, _dt, _one_shield

# ---------------------------------------------------------------- parse_shields


def test_no_shield_templates_root_yields_nothing(tmp_path) -> None:
    path = tmp_path / "empty.dts"
    path.write_text(
        dedent("""\
        /dts-v1/;
        / { };
        """)
    )
    dt = get_dtlib().DT(str(path))
    shields, diags = parse_shields(dt, _TYPES)
    assert shields == {}
    assert diags == []


def test_basic_identity(tmp_path) -> None:
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    assert set(shields) == {"fx"}
    shield = shields["fx"]
    assert shield.name == "fx"
    assert shield.label == "fx"
    assert shield.plugs == {"plug": "fixture-type"}


def test_unknown_connector_type_is_rejected(tmp_path) -> None:
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "no-such-type";
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-shield-type"
    assert "no-such-type" in diags[0].message


def test_missing_plug_node_is_rejected(tmp_path) -> None:
    """A template with no plug node at all: the plug is the position
    reference frame, and it is where a shield names its connector type."""
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-shield-plug"
    assert "shield,plug" in diags[0].message
    assert shields["fx"].plugs == {}


def test_template_level_shield_plugs_is_retired(tmp_path) -> None:
    """The retired single form -- `shield,plugs` on the TEMPLATE node --
    is refused, and the message says where the property moved: onto a
    plug node. It must FAIL rather than read as a device group named
    `plug`, which would silently drop every nested group."""
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tshield,plugs = "fixture-type";
\t\t\tplug: plug { };
\t\t\ti2c {
\t\t\t\tdev1: dev@50 { compatible = "vnd,thing"; reg = <0x50>; };
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-shield-plug"
    assert "retired" in diags[0].message
    assert shields["fx"].plugs == {}
    assert shields["fx"].devices == []


# ---------------------------------------------------------------- plural plugs


def test_single_form_device_plug_defaults_to_the_default_slot(tmp_path) -> None:
    """Single form normalizes to one slot, literally named 'plug' -- every
    device (bus or plain) records it, not just bus devices, since there
    is only one plug to belong to."""
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
\t\t\tgpio {
\t\t\t\tbtn: button { gpios = <&plug 0 1>; };
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    shield = shields["fx"]
    assert shield.plugs == {"plug": "fixture-type"}
    bus_dev = next(d for d in shield.devices if d.name == "dev")
    plain_dev = next(d for d in shield.devices if d.name == "button")
    assert bus_dev.plug == "plug"
    assert plain_dev.plug == "plug"
    assert plain_dev.function_refs[0].plug == "plug"


def test_plural_shield_two_plugs_and_bus_membership(tmp_path) -> None:
    """The can_span_click shape: two plugs of the SAME connector type,
    each with its own bus group nested under it -- the plug node NAME is
    the slot, and each bus device records its OWN plug's slot."""
    dt = _dt(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tleft_plug: left {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t\ti2c {
\t\t\t\t\tdev_l: devl@10 { compatible = "vnd,thing"; reg = <0x10>; };
\t\t\t\t};
\t\t\t};
\t\t\tright_plug: right {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t\ti2c {
\t\t\t\t\tdev_r: devr@20 { compatible = "vnd,thing"; reg = <0x20>; };
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    shields, diags = parse_shields(dt, _PLURAL_TYPES)
    assert diags == []
    shield = shields["fx"]
    assert shield.plugs == {"left": "fixture-type", "right": "fixture-type"}
    dev_l = next(d for d in shield.devices if d.name == "devl")
    dev_r = next(d for d in shield.devices if d.name == "devr")
    assert dev_l.plug == "left"
    assert dev_r.plug == "right"


def test_plural_shield_cross_plug_gpio_ref_records_the_named_plug(tmp_path) -> None:
    """A device on the LEFT plug's bus may still carry a gpio ref naming
    the RIGHT plug -- the phandle may name "one of this shield's plugs",
    not just "this device's own plug", and FunctionRef.plug records
    which one, independent of the device's own bus slot."""
    dt = _dt(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tleft_plug: left {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t\tspi {
\t\t\t\t\tdevl: devl { compatible = "vnd,thing";
\t\t\t\t\t\tint-gpios = <&right_plug 0 1>;
\t\t\t\t\t};
\t\t\t\t};
\t\t\t};
\t\t\tright_plug: right {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t};
""",
    )
    shields, diags = parse_shields(dt, _PLURAL_TYPES)
    assert diags == []
    dev = shields["fx"].devices[0]
    assert dev.plug == "left"  # the device's OWN bus slot
    ref = dev.function_refs[0]
    assert ref.plug == "right"  # the CROSS-PLUG reference's own slot
    assert ref.position == 0


def test_plural_shield_two_different_connector_types(tmp_path) -> None:
    """The acq_bridge shape: two plugs of DIFFERENT connector types."""
    dt = _dt(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tard: ard {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tmb: mb {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type-2";
\t\t\t};
\t\t};
""",
    )
    shields, diags = parse_shields(dt, _PLURAL_TYPES)
    assert diags == []
    assert shields["fx"].plugs == {"ard": "fixture-type", "mb": "fixture-type-2"}


def test_plural_shield_unknown_connector_type_on_one_plug(tmp_path) -> None:
    dt = _dt(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tleft_plug: left {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "no-such-type";
\t\t\t};
\t\t\tright_plug: right {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t};
""",
    )
    _shields, diags = parse_shields(dt, _PLURAL_TYPES)
    assert len(diags) == 1
    assert diags[0].code == "lang-shield-type"
    assert "left" in diags[0].message
    assert "no-such-type" in diags[0].message


def test_plain_group_device_is_plug_agnostic_in_the_plural_form(tmp_path) -> None:
    """A plain (non-bus) device group stays
    template-level in a plural shield, and its device is plug-AGNOSTIC
    (plug is None) -- its own refs each carry their own plug instead."""
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
\t\t\tgpio {
\t\t\t\tbtn: button { gpios = <&left_plug 0 1>; };
\t\t\t};
\t\t};
""",
    )
    shields, diags = parse_shields(dt, _PLURAL_TYPES)
    assert diags == []
    dev = shields["fx"].devices[0]
    assert dev.bus is None
    assert dev.plug is None
    assert dev.group == "gpio"
    assert dev.function_refs[0].plug == "left"


def test_one_plug_is_the_same_form_as_many(tmp_path) -> None:
    """There is ONE authored form: a shield with a single plug declares it
    exactly as a shield with two does, and its slot name is that node's
    own name. This is the shape every corpus shield has."""
    dt = _dt(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tleft_plug: left {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type-2";
\t\t\t};
\t\t\tgpio {
\t\t\t\tbtn: button { gpios = <&left_plug 0 1>; };
\t\t\t};
\t\t};
""",
    )
    shields, diags = parse_shields(dt, _PLURAL_TYPES)
    assert diags == []
    assert shields["fx"].plugs == {"left": "fixture-type-2"}
    # a plain-group device is attributed to the ONE plug by its own slot
    # name -- never to the literal "plug" the retired form hardcoded
    assert shields["fx"].devices[0].plug == "left"


def test_a_plug_node_may_be_named_plug_beside_another(tmp_path) -> None:
    """`plug` is an ordinary slot NAME -- conventional for a shield with
    one, reserved for nothing."""
    dt = _dt(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tright_plug: right {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t};
""",
    )
    shields, diags = parse_shields(dt, _PLURAL_TYPES)
    assert diags == []
    assert shields["fx"].plugs == {"plug": "fixture-type", "right": "fixture-type"}


def test_plural_shield_template_level_bus_group_is_rejected(tmp_path) -> None:
    """A plural shield's bus groups must nest under
    their owning plug -- a bus-shaped group at TEMPLATE level is a loud
    lang-shield-proxy error naming the candidate plugs."""
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
\t\t\ti2c {
\t\t\t\tdev1: dev@50 { compatible = "vnd,thing"; reg = <0x50>; };
\t\t\t};
\t\t};
""",
    )
    _shields, diags = parse_shields(dt, _PLURAL_TYPES)
    assert len(diags) == 1
    assert diags[0].code == "lang-shield-proxy"
    assert "template level" in diags[0].message
    assert "left" in diags[0].message and "right" in diags[0].message


def test_plural_shield_plain_group_nested_under_a_plug_is_rejected(tmp_path) -> None:
    """The reverse of the template-level case above: a plain (non-bus,
    not even bus-kind-named) group nested UNDER a plug is not a bus this
    plug's ctype could ever allow, so it is rejected -- accepting it
    would record Device.plug = slot and contradict the invariant that a
    plain-group device is plug-agnostic (plug is None)."""
    dt = _dt(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tleft_plug: left {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t\tgpio {
\t\t\t\t\tbtn: button { gpios = <&left_plug 0 1>; };
\t\t\t\t};
\t\t\t};
\t\t\tright_plug: right {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t};
""",
    )
    shields, diags = parse_shields(dt, _PLURAL_TYPES)
    assert len(diags) == 1
    assert diags[0].code == "lang-shield-proxy"
    assert (
        "plug 'left' has a 'gpio' group nested under it -- plain "
        "device groups belong at template level" in diags[0].message
    )
    assert shields["fx"].devices[0].plug is None


# ------------------------------------------- the placement rule at ONE plug
# The same three laws as above, at a plug count of one: a bus group must
# nest under its plug, never sit as a sibling of it, or a nested group
# would be silently dropped instead of parsed.


def test_one_plug_template_level_bus_group_is_rejected(tmp_path) -> None:
    """A bus group beside the plug rather than under it is refused. The
    message names the plug it should have nested under."""
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\ti2c {
\t\t\t\tdev1: dev@50 { compatible = "vnd,thing"; reg = <0x50>; };
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-shield-proxy"
    assert "template level" in diags[0].message
    assert "candidate plugs: plug" in diags[0].message


def test_one_plug_nested_plain_group_is_rejected(tmp_path) -> None:
    """And the reverse, at one plug: a plain group stays at template
    level whatever the count, so nesting one is refused rather than
    silently attributed to the plug."""
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t\tgpio {
\t\t\t\t\tbtn: button { gpios = <&plug 0 1>; };
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    assert len(diags) == 1
    assert diags[0].code == "lang-shield-proxy"
    assert "belong at template level" in diags[0].message


def test_one_plug_nested_bus_group_parses_its_devices(tmp_path) -> None:
    """The positive half: the nested spelling PARSES at one plug, and
    the plug node's children are visited like any other."""
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t\ti2c {
\t\t\t\t\tdev1: dev@50 { compatible = "vnd,thing"; reg = <0x50>;
\t\t\t\t\t\tint-gpios = <&plug 0 1>; };
\t\t\t\t};
\t\t\t};
\t\t\tgpio {
\t\t\t\tbtn: button { gpios = <&plug 1 0>; };
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    devs = {d.name: d for d in shields["fx"].devices}
    assert set(devs) == {"dev", "button"}
    assert devs["dev"].bus == "i2c"
    assert devs["dev"].plug == "plug"
    assert [(r.prop, r.position) for r in devs["dev"].function_refs] == [("int-gpios", 0)]
    # the plain-group device is attributed to the ONLY plug's own name,
    # never to the literal string "plug"
    assert devs["button"].bus is None
    assert devs["button"].group == "gpio"
    assert devs["button"].plug == "plug"


# ------------------------------------------------------ cells on a plug node


def test_cells_on_a_plug_node_are_rejected(tmp_path) -> None:
    """A plug declares no cell counts: the plug node is never emitted so
    nothing validates a `#gpio-cells`/`#pwm-cells`/`#io-channel-cells`
    value declared there, and a wrong value would silently change a
    reference's arity. One diagnostic per property, each naming the
    property."""
    _shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t\t#gpio-cells = <2>;
\t\t\t\t#pwm-cells = <3>;
\t\t\t\t#io-channel-cells = <1>;
\t\t\t};
\t\t};
""",
    )
    assert [d.code for d in diags] == ["lang-shield-plug-cells"] * 3
    assert {"#gpio-cells", "#pwm-cells", "#io-channel-cells"} == {
        w for d in diags for w in d.message.split() if w.startswith("#")
    }


def test_a_reference_through_a_plug_uses_the_generic_cell_count(tmp_path) -> None:
    """The counterpart: with no declaration to read, a claim through the
    plug carries the generic count for its function -- 2 for gpio."""
    shields, diags = _one_shield(
        tmp_path,
        """
\t\tfx: fx {
\t\t\tplug: plug {
\t\t\t\tcompatible = "shield,plug";
\t\t\t\tshield,plugs = "fixture-type";
\t\t\t};
\t\t\tgpio {
\t\t\t\tbtn: button { gpios = <&plug 0 1>, <&plug 1 0>; };
\t\t\t};
\t\t};
""",
    )
    assert diags == []
    refs = shields["fx"].devices[0].function_refs
    assert [(r.position, r.flags) for r in refs] == [(0, 1), (1, 0)]


def test_plural_shield_routing_jumper_is_rejected(tmp_path) -> None:
    """Routing jumpers have no plug axis, so a plural shield declaring
    one is refused outright."""
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
\t\t\tconfig {
\t\t\t\tirq_jmp: irq-jmp {
\t\t\t\t\t#gpio-cells = <1>;
\t\t\t\t\tshield,position-domain = <0 0>, <1 1>;
\t\t\t\t};
\t\t\t};
\t\t};
""",
    )
    shields, diags = parse_shields(dt, _PLURAL_TYPES)
    assert len(diags) == 1
    assert diags[0].code == "lang-shield-plurality"
    assert "jumper" in diags[0].message
    assert shields["fx"].jumpers == {}
