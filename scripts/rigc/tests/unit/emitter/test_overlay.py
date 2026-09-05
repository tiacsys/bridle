# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: emitter/overlay -- the device-node renderer. Stable contracts
pinned here: gpio/pwm/adc idioms, the `inst.invert` flag flip,
per-instance params substitution (replace vs add), the sdmmc child
node, the PWM-flags AssertionError, and determinism under a shuffled
instance order -- the frozen suite's own goldens already cover this
end to end; this module aims at contracts that would survive a
rewrite, not coverage.
"""

from __future__ import annotations

import pytest

from rigc.analyzer import ChannelResolution, Solved
from rigc.diag import SourceRef
from rigc.emitter.overlay import render_overlay
from rigc.model import (
    BoardSocket,
    BusRef,
    ConnectorType,
    Device,
    FunctionRef,
    Instance,
    Rig,
    Shield,
)

_SRC = SourceRef("f.yml", 1, "k")


def _ctype() -> ConnectorType:
    return ConnectorType(
        name="t", positions={}, index2name={}, bus_proxies=[], stackable=False, cs_pool={}
    )


def _socket(pwm_cells: int | None = None) -> BoardSocket:
    return BoardSocket(
        label="sock", path="/s", type_name="t", gpio_map={}, buses={}, pwm_cells=pwm_cells
    )


def _plain_dev(**kwargs: object) -> Device:
    """A plain (non-bus, non-collected) device -- the shortest path to
    `_device_node` via render_overlay's per-instance container section."""
    defaults: dict = dict(
        name="d",
        label="d",
        compatible=None,
        bus=None,
        group=None,
        reg=None,
        addr_from=None,
        cs_position=None,
    )
    defaults.update(kwargs)
    return Device(**defaults)


def test_gpio_ref_flips_the_active_level_when_the_instance_inverts() -> None:
    ref = FunctionRef(prop="int-gpios", position=5, flags=0x1, src=_SRC, function="gpio")
    dev = _plain_dev(function_refs=[ref])
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
    inst = Instance(name="i1", shield=shield, sockets={"plug": "sock"}, invert=True)
    rig = Rig(name="r", instances=[inst])
    s = Solved(sockets={"i1": {"plug": _socket()}})

    text = render_overlay(rig, s, {"t": _ctype()})

    assert "int-gpios = <&sock 5 0x0>;" in text  # 0x1 ^ 0x1 (invert) = 0x0


def test_gpio_ref_keeps_flags_unchanged_when_not_inverted() -> None:
    ref = FunctionRef(prop="int-gpios", position=5, flags=0x1, src=_SRC, function="gpio")
    dev = _plain_dev(function_refs=[ref])
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
    inst = Instance(name="i1", shield=shield, sockets={"plug": "sock"})
    rig = Rig(name="r", instances=[inst])
    s = Solved(sockets={"i1": {"plug": _socket()}})

    text = render_overlay(rig, s, {"t": _ctype()})

    assert "int-gpios = <&sock 5 0x1>;" in text


def test_pwm_ref_omits_flags_and_renders_position_and_period() -> None:
    """2-cell socket: flags omitted, exactly as lotus's own
    atmel,sam0-tcc-pwm shape requires."""
    ref = FunctionRef(prop="pwms", position=2, flags=0, src=_SRC, function="pwm", period=1000)
    dev = _plain_dev(name="dev", label="dev", function_refs=[ref])
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
    inst = Instance(name="i1", shield=shield, sockets={"plug": "sock"})
    rig = Rig(name="r", instances=[inst])
    s = Solved(
        sockets={"i1": {"plug": _socket(pwm_cells=2)}},
        channels={("i1", "dev", "pwms"): ChannelResolution("pwm", "pwm0", 0, 1000, 0, 2)},
    )

    text = render_overlay(rig, s, {"t": _ctype()})

    assert "pwms = <&sock 2 1000>;" in text


def test_pwm_ref_on_a_3cell_socket_renders_the_flags_word_too() -> None:
    """The 3-cell twin: the SAME (position, period) plus a real flags
    word -- the common upstream shape (st,stm32-pwm/nxp,ftm-pwm)."""
    ref = FunctionRef(prop="pwms", position=2, flags=0x1, src=_SRC, function="pwm", period=1000)
    dev = _plain_dev(name="dev", label="dev", function_refs=[ref])
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
    inst = Instance(name="i1", shield=shield, sockets={"plug": "sock"})
    rig = Rig(name="r", instances=[inst])
    s = Solved(
        sockets={"i1": {"plug": _socket(pwm_cells=3)}},
        channels={("i1", "dev", "pwms"): ChannelResolution("pwm", "pwm0", 0, 1000, 0x1, 2)},
    )

    text = render_overlay(rig, s, {"t": _ctype()})

    assert "pwms = <&sock 2 1000 0x1>;" in text


def test_nonzero_pwm_flags_raise_assertionerror_never_silently_emitted() -> None:
    """The analyzer's phys-function rejection is what makes this
    unreachable on an accepted rig (analyzer/gpio.py); this documents the
    invariant rather than re-deriving the diagnostic -- a RAISE, not a
    bare `assert`, so it survives `python -O`.
    2-cell socket only: a 3-cell one has a real cell for flags, so this
    is unreachable there BY CONSTRUCTION, not merely by the analyzer's
    own gate -- see the 3-cell test above."""
    ref = FunctionRef(prop="pwms", position=2, flags=0, src=_SRC, function="pwm", period=1000)
    dev = _plain_dev(name="dev", label="dev", function_refs=[ref])
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
    inst = Instance(name="i1", shield=shield, sockets={"plug": "sock"})
    rig = Rig(name="r", instances=[inst])
    s = Solved(
        sockets={"i1": {"plug": _socket(pwm_cells=2)}},
        channels={("i1", "dev", "pwms"): ChannelResolution("pwm", "pwm0", 0, 1000, 0x1, 2)},
    )

    with pytest.raises(AssertionError, match="nonzero PWM flags"):
        render_overlay(rig, s, {"t": _ctype()})


def test_adc_ref_renders_position_only_no_flags_no_period() -> None:
    ref = FunctionRef(prop="io-channels", position=3, flags=0, src=_SRC, function="adc")
    dev = _plain_dev(name="dev", label="dev", function_refs=[ref])
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
    inst = Instance(name="i1", shield=shield, sockets={"plug": "sock"})
    rig = Rig(name="r", instances=[inst])
    s = Solved(
        sockets={"i1": {"plug": _socket()}},
        channels={("i1", "dev", "io-channels"): ChannelResolution("adc", "adc0", 0, None, 0, 3)},
    )

    text = render_overlay(rig, s, {"t": _ctype()})

    assert "io-channels = <&sock 3>;" in text


def test_pwm_collection_entry_renders_the_resolved_period_not_the_flags_cell() -> None:
    """A pwm-leds collection entry must render the resolved PERIOD from
    `s.channels` in the second cell, never the claim's flags/polarity
    bit -- those are gpio-shaped, not pwm-shaped. period=1234 here is
    chosen to differ sharply from flags=0, so a value-swap regression
    (period and flags rendered in each other's place) is visible rather
    than accidentally passing because both happen to be small."""
    ref = FunctionRef(prop="pwms", position=5, flags=0, src=_SRC, function="pwm", period=1234)
    dev = _plain_dev(name="led", label="led", collect="pwm-leds", function_refs=[ref])
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
    inst = Instance(name="i1", shield=shield, sockets={"plug": "sock"})
    rig = Rig(name="r", instances=[inst])
    s = Solved(
        sockets={"i1": {"plug": _socket(pwm_cells=2)}},
        channels={("i1", "led", "pwms"): ChannelResolution("pwm", "pwm0", 0, 1234, 0, 5)},
    )

    text = render_overlay(rig, s, {"t": _ctype()})

    assert 'compatible = "pwm-leds";' in text
    assert "pwms = <&sock 5 1234>;" in text
    assert "pwms = <&sock 5 0x0>;" not in text  # not the gpio-shaped flags cell


def test_invert_does_not_touch_a_pwm_collection_entry() -> None:
    """invert: is a gpio-flags concept. Even on a COLLECTED entry whose
    instance sets invert: true, the pwm branch never consults
    inst.invert -- accepted, silently without effect on the emitted line."""
    ref = FunctionRef(prop="pwms", position=5, flags=0, src=_SRC, function="pwm", period=1234)
    dev = _plain_dev(name="led", label="led", collect="pwm-leds", function_refs=[ref])
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
    inst = Instance(name="i1", shield=shield, sockets={"plug": "sock"}, invert=True)
    rig = Rig(name="r", instances=[inst])
    s = Solved(
        sockets={"i1": {"plug": _socket(pwm_cells=2)}},
        channels={("i1", "led", "pwms"): ChannelResolution("pwm", "pwm0", 0, 1234, 0, 5)},
    )

    text = render_overlay(rig, s, {"t": _ctype()})

    assert "pwms = <&sock 5 1234>;" in text
    assert "inverted" not in text


def test_adc_collection_entry_renders_one_cell_no_flags_no_period() -> None:
    """The same shared renderer's adc branch, reached through the collect
    path -- a genuine cell-count difference from the gpio-shaped render
    (#io-channel-cells is 1, not 2), not merely a wrong value like the pwm
    case above. No collected ADC device exists in the corpus today; this
    pins the shared helper's behavior ahead of one landing."""
    ref = FunctionRef(prop="io-channels", position=3, flags=0, src=_SRC, function="adc")
    dev = _plain_dev(
        name="sensor", label="sensor", collect="some-adc-collection", function_refs=[ref]
    )
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
    inst = Instance(name="i1", shield=shield, sockets={"plug": "sock"})
    rig = Rig(name="r", instances=[inst])
    s = Solved(
        sockets={"i1": {"plug": _socket()}},
        channels={("i1", "sensor", "io-channels"): ChannelResolution("adc", "adc0", 0, None, 0, 3)},
    )

    text = render_overlay(rig, s, {"t": _ctype()})

    assert 'compatible = "some-adc-collection";' in text
    assert "io-channels = <&sock 3>;" in text


def test_instance_params_replace_an_existing_prop_and_add_a_new_one() -> None:
    dev = _plain_dev(
        label="dev",
        extra_props=[("zephyr,code", "zephyr,code = <INPUT_KEY_0>;"), ("label", 'label = "btn";')],
    )
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
    inst = Instance(
        name="i1",
        shield=shield,
        sockets={"plug": "sock"},
        params={"dev": {"zephyr,code": "INPUT_KEY_9", "debounce-interval-ms": "30"}},
    )
    rig = Rig(name="r", instances=[inst])
    s = Solved(sockets={"i1": {"plug": _socket()}})

    text = render_overlay(rig, s, {"t": _ctype()})

    assert "zephyr,code = <INPUT_KEY_9>;" in text  # REPLACED
    assert "zephyr,code = <INPUT_KEY_0>;" not in text  # the old rendering is gone
    assert 'label = "btn";' in text  # untouched (not assigned)
    assert "debounce-interval-ms = <30>;" in text  # ADDED (no prior default)


def test_sdhc_spi_slot_device_gets_a_sdmmc_child_node() -> None:
    dev = _plain_dev(name="sd", label="sd", compatible="zephyr,sdhc-spi-slot")
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
    inst = Instance(name="i1", shield=shield, sockets={"plug": "sock"})
    rig = Rig(name="r", instances=[inst])
    s = Solved(sockets={"i1": {"plug": _socket()}})

    text = render_overlay(rig, s, {"t": _ctype()})

    assert 'compatible = "zephyr,sdmmc-disk";' in text
    assert 'disk-name = "SD";' in text


def test_devices_without_the_sdmmc_compatible_get_no_extra_child() -> None:
    dev = _plain_dev(name="sd", label="sd", compatible="something-else")
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
    inst = Instance(name="i1", shield=shield, sockets={"plug": "sock"})
    rig = Rig(name="r", instances=[inst])
    s = Solved(sockets={"i1": {"plug": _socket()}})

    text = render_overlay(rig, s, {"t": _ctype()})

    assert "sdmmc" not in text


def test_render_overlay_is_deterministic_under_a_shuffled_instance_order() -> None:
    """Output is sorted by stable keys, never rig-file declaration
    order -- two instance lists differing only in ORDER must render
    byte-identical text."""

    def make(order: list[str]) -> str:
        insts = []
        sockets = {}
        for name in order:
            dev = _plain_dev(name="d", label="d")
            shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
            insts.append(Instance(name=name, shield=shield, sockets={"plug": "sock"}))
            sockets[name] = {"plug": _socket()}
        rig = Rig(name="r", instances=insts)
        s = Solved(sockets=sockets)
        return render_overlay(rig, s, {"t": _ctype()})

    assert make(["alpha", "bravo"]) == make(["bravo", "alpha"])


def _mux_rig_and_solved(channel_order: list[int]) -> tuple[Rig, Solved]:
    """One I2C mux instance whose scopes: entries are inserted in
    channel_order -- the mux-channel counterpart of the shuffled instance
    list above (each channel is a NEW address scope)."""
    dev = _plain_dev(
        name="mux",
        label="mux",
        bus="i2c",
        extra_props=[("compatible", 'compatible = "ti,tca9548a";')],
    )
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
    inst = Instance(name="i1", shield=shield, sockets={"plug": "sock"})
    socket = BoardSocket(
        label="sock",
        path="/s",
        type_name="t",
        gpio_map={},
        buses={"i2c": BusRef(label="i2c1", path="/i2c1")},
    )
    scopes: dict[str, tuple[str, int]] = {
        f"/i2c1/ch{channel}": ("i1_mux", channel) for channel in channel_order
    }
    return (
        Rig(name="r", instances=[inst]),
        Solved(
            sockets={"i1": {"plug": socket}},
            addr={("i1", "mux"): 0x70},
            bus_label={"/i2c1": "i2c1"},
            scopes=scopes,
        ),
    )


def test_render_overlay_is_deterministic_under_a_shuffled_scope_order() -> None:
    """The same sorted-output guarantee for `Solved.scopes`, whose
    iteration builds the mux-channel lists: two dicts differing only in
    INSERTION order must render byte-identical channel nodes."""
    forward_rig, forward = _mux_rig_and_solved([0, 1, 2])
    reverse_rig, reverse = _mux_rig_and_solved([2, 1, 0])

    text = render_overlay(forward_rig, forward, {"t": _ctype()})

    assert text == render_overlay(reverse_rig, reverse, {"t": _ctype()})
    assert text.index("channel@0") < text.index("channel@1") < text.index("channel@2")


def test_resolved_controllers_are_enabled_under_the_pinctrl_note() -> None:
    """The PWM/ADC controller section, verbatim. Its three comment lines are
    frozen output text, not prose: the em dash in the second one is a
    literal byte of every overlay a PWM/ADC rig emits, and writing it as
    `--` renders a golden mismatch that only one corpus rig (lotus_pwm)
    can catch. Asserted character-for-character here so a fast unit run
    catches it instead of a 200-second differential."""
    rig = Rig(name="r", instances=[])
    s = Solved(controllers={"tcc0": "pwm", "adc0": "adc"})

    text = render_overlay(rig, s, {"t": _ctype()})

    assert (
        "/* PWM/ADC: enable the resolved controllers; the pin-mux (pinctrl)\n"
        " * for each muxed pin is board-provided and must be applied —\n"
        " * stubbed here, see the config sheet. */\n"
        '&adc0 { status = "okay"; };\n'  # sorted, not insertion order
        '&tcc0 { status = "okay"; };'
    ) in text


def test_no_controllers_means_no_controller_section_at_all() -> None:
    rig = Rig(name="r", instances=[])

    text = render_overlay(rig, Solved(), {"t": _ctype()})

    assert "PWM/ADC" not in text


def test_carrier_exported_socket_synthesizes_a_chained_gpio_nexus() -> None:
    """A socket with no DT node of its own gets a synthesized gpio-nexus
    chaining to its parent's, and a carrier stacked on a carrier
    synthesizes BOTH (the recursive parent visit). The four fixed property
    lines and the multi-row gpio-map join are frozen output text."""
    parent = BoardSocket(
        label="carrier",
        path="/c",
        type_name="t",
        gpio_map={},
        buses={},
        nexus_label="carrier_nexus",
        nexus_rows=[(0, "nucleo_ard", 7)],
    )
    child = BoardSocket(
        label="click",
        path="/c/k",
        type_name="t",
        gpio_map={},
        buses={},
        nexus_label="click_nexus",
        nexus_rows=[(0, "carrier_nexus", 3), (1, "carrier_nexus", 4)],
        parents={"plug": parent},
    )
    rig = Rig(name="r", instances=[])
    s = Solved(sockets={"i1": {"plug": child}})

    text = render_overlay(rig, s, {"t": _ctype()})

    assert "/* carrier-exported sockets, synthesized as gpio-nexus nodes */" in text
    assert (
        "\tclick_nexus: click_nexus {\n"
        "\t\t#gpio-cells = <2>;\n"
        "\t\tgpio-map-mask = <0xffffffff 0xffffffc0>;\n"
        "\t\tgpio-map-pass-thru = <0 0x3f>;\n"
        "\t\tgpio-map = <0 0 &carrier_nexus 3 0>,\n"
        "\t\t\t   <1 0 &carrier_nexus 4 0>;\n"
        "\t};"
    ) in text
    # the parent is reached through child.parents, never through s.sockets
    assert "\tcarrier_nexus: carrier_nexus {" in text


def test_carrier_exported_socket_analog_only_is_not_skipped() -> None:
    """A socket with adc/pwm rows but NO gpio rows (nexus_rows == []) must
    still be visited and rendered: analog-only exported sockets are not
    skipped. This carrier-exported socket authors ONLY an
    io-channel-map, no gpio-map at all."""
    child = BoardSocket(
        label="a0",
        path="/c/a0",
        type_name="t",
        gpio_map={},
        buses={},
        nexus_label="carrier_a0",
        nexus_rows=[],
        adc_map={5: ("adc0", 1)},
        adc_cells=1,
        adc_nexus_rows=[(5, "board_ard", 1)],
    )
    rig = Rig(name="r", instances=[])
    s = Solved(sockets={"i1": {"plug": child}})

    text = render_overlay(rig, s, {"t": _ctype()})

    assert "carrier_a0: carrier_a0 {" in text
    assert "#gpio-cells" not in text
    assert "gpio-map" not in text
    assert "#io-channel-cells = <1>;" in text
    assert "io-channel-map = <5 &board_ard 1>;" in text


def test_carrier_exported_socket_synthesizes_a_chained_pwm_nexus() -> None:
    """The PWM twin of the gpio nexus test above: #pwm-cells and the
    mask/pass-thru pair mirror the REAL board idiom (grove_sockets.dtsi)
    -- position matched, period passed through -- generated here for a
    SYNTHESIZED carrier node instead of a hand-authored real one."""
    child = BoardSocket(
        label="a0",
        path="/c/a0",
        type_name="t",
        gpio_map={},
        buses={},
        nexus_label="carrier_a0",
        nexus_rows=[(5, "board_ard", 3)],
        pwm_map={5: ("tcc0", 0)},
        pwm_cells=2,
        pwm_nexus_rows=[(5, "board_ard", 0)],
    )
    rig = Rig(name="r", instances=[])
    s = Solved(sockets={"i1": {"plug": child}})

    text = render_overlay(rig, s, {"t": _ctype()})

    assert (
        "\t\t#pwm-cells = <2>;\n"
        "\t\tpwm-map-mask = <0xffffffff 0x00000000>;\n"
        "\t\tpwm-map-pass-thru = <0x00000000 0xffffffff>;\n"
        "\t\tpwm-map = <5 0 &board_ard 0 0>;"
    ) in text


def test_carrier_exported_socket_mixed_gpio_pwm_adc_is_one_node_both_maps() -> None:
    """An exposed socket carrying gpio AND pwm AND adc rows emits ONE
    synthesized node with all three maps -- never two nodes, never one
    map silently winning over another."""
    child = BoardSocket(
        label="a0",
        path="/c/a0",
        type_name="t",
        gpio_map={0: ("gpiod", 2, 0)},
        buses={},
        nexus_label="carrier_a0",
        nexus_rows=[(0, "board_ard", 2)],
        pwm_map={0: ("tcc0", 0)},
        pwm_cells=2,
        pwm_nexus_rows=[(0, "board_ard", 0)],
        adc_map={1: ("adc0", 3)},
        adc_cells=1,
        adc_nexus_rows=[(1, "board_ard", 3)],
    )
    rig = Rig(name="r", instances=[])
    s = Solved(sockets={"i1": {"plug": child}})

    text = render_overlay(rig, s, {"t": _ctype()})

    # ONE node -- both "carrier_a0: carrier_a0 {" and its closing "};"
    # appear exactly once, with every map's lines between them.
    assert text.count("carrier_a0: carrier_a0 {") == 1
    node = text.split("carrier_a0: carrier_a0 {")[1].split("\n\t};")[0]
    assert "#gpio-cells = <2>;" in node
    assert "gpio-map = <0 0 &board_ard 2 0>;" in node
    assert "#pwm-cells = <2>;" in node
    assert "pwm-map = <0 0 &board_ard 0 0>;" in node
    assert "#io-channel-cells = <1>;" in node
    assert "io-channel-map = <1 &board_ard 3>;" in node


def test_pwm_nexus_cells_come_from_the_socket_not_hardcoded() -> None:
    """The synthesized nexus carries the PARENT's cell count, never a
    hardcoded one. A (synthetic, not a real supported
    shape) 3-cell value proves the emitter reads sock.pwm_cells rather
    than assuming 2 -- mutation check: hardcoding #pwm-cells=<2> here
    must fail THIS test on the cell count itself."""
    child = BoardSocket(
        label="a0",
        path="/c/a0",
        type_name="t",
        gpio_map={},
        buses={},
        nexus_label="carrier_a0",
        nexus_rows=[(5, "board_ard", 3)],
        pwm_map={5: ("tcc0", 0)},
        pwm_cells=3,
        pwm_nexus_rows=[(5, "board_ard", 0)],
    )
    rig = Rig(name="r", instances=[])
    s = Solved(sockets={"i1": {"plug": child}})

    text = render_overlay(rig, s, {"t": _ctype()})

    assert "#pwm-cells = <3>;" in text
    assert "pwm-map-mask = <0xffffffff 0x00000000 0x00000000>;" in text
    assert "pwm-map-pass-thru = <0x00000000 0xffffffff 0xffffffff>;" in text
    assert "pwm-map = <5 0 0 &board_ard 0 0 0>;" in text


def test_board_sockets_synthesize_no_nexus_node() -> None:
    """nexus_rows is None for a real board socket -- there is nothing to
    route, and emitting one would shadow the board's own node."""
    rig = Rig(name="r", instances=[])

    text = render_overlay(rig, Solved(sockets={"i1": {"plug": _socket()}}), {"t": _ctype()})

    assert "gpio-map" not in text
