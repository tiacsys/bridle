# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Board projection over a SYNTHETIC, cpp-free board DT:
project.project_edt is called directly against an edtlib.EDT built from
`tests/fixtures/boards/fixture_board.dts` -- purpose-built fixture data in
rigc's own tree. No cpp at all: the fixture .dts has no `#include`/macros,
so `edtlib.EDT()` is built straight off it here -- `project.load_board`/
`edt_build.build_edt` (which DO invoke cpp) are integration-only by
construction, the same seam that makes shield-side parsing
integration-only, so this module never calls them.

Everything that must resolve out of ONE socket,fixture-nexus node is
covered by construction: gpio-map (two positions), pwm-map (whose
controller carries a SECOND, later-attached label -- the controller-label
determinism invariant, mirroring upstream python-devicetree's
test_controller_label.py coverage), io-channel-map, an i2c bus phandle,
an spi bus phandle, and an authored cs-pool (per-bus, on BusRef -- the
i2c bus of the same socket carries none, pinning that a cs-pool value
attaches to the ONE bus that authors it, never every bus of the socket).

A named, multi-bus connector type (socket,spi-sensors/socket,spi-motors,
project.py's own widened pattern match) is a SEPARATE, hermetic
edtlib.EDT this file builds inline rather than through fixture_board.dts
-- it needs its own binding (the shared socket-fixture-nexus.yaml schema
declares no such properties), and keeping it out of the shared fixture
avoids widening that schema/DTS for every other test in this file.

fixture_socket_bare additionally carries a SECOND label of its own
(fixture_bare_alias) -- the alias-index fixture proving project_edt must
index every label a socket node declares for RESOLUTION (Board.resolve),
while Board.sockets itself stays keyed by the defining label alone, one
entry per physical socket.

The module-level census below (test_every_board_rig_extension_socket_...)
is a SEPARATE concern from the rest of this file: it scans the REAL
boards/extend/ tree's .dtsi text (regex, not edtlib -- several of those
fragments, e.g. lotus's `adc0: &adc {};`, reference a node their own file
never defines, so they are not standalone-parseable outside a real board
build) for the per-connector-type conventional label every board rig
extension is expected to declare. It is a census-style test: falsified
by mutating the WORLD it observes (dropping a label from a real board
file), never by editing its own assertion.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from rigc.board import project
from rigc.board.census import scan_socket_nodes
from rigc.board.edt_build import ensure_devicetree_on_path
from rigc.diag import LoadError
from rigc.dtsio import MODULE_ROOT
from rigc.tests.conftest import FIXTURES_DIR, assert_fixture_local

_BOARD_DTS = FIXTURES_DIR / "boards" / "fixture_board.dts"
_BINDINGS_DIR = FIXTURES_DIR / "dts" / "bindings"


def _edt():
    """Build the fixture's edtlib.EDT directly -- no cpp, no BuildRecipe,
    no workdir: the fixture .dts is already valid, preprocessed-shape DTS
    text."""
    assert_fixture_local([_BOARD_DTS, _BINDINGS_DIR])
    ensure_devicetree_on_path()
    from devicetree import edtlib

    return edtlib.EDT(str(_BOARD_DTS), [str(_BINDINGS_DIR)], default_prop_types=True)


def _socket():
    board = project.project_edt(_edt(), "fixture-board")
    return board.sockets["fixture_socket"]


def _bare_socket():
    board = project.project_edt(_edt(), "fixture-board")
    return board.sockets["fixture_socket_bare"]


# ---------------------------------------------------------------- project_edt


def test_project_edt_finds_every_socket_by_label() -> None:
    board = project.project_edt(_edt(), "fixture-board")
    assert board.name == "fixture-board"
    assert set(board.sockets) == {"fixture_socket", "fixture_socket_bare"}


def test_project_edt_ignores_non_socket_compatibles() -> None:
    """Only compatible = "socket,*" nodes project -- the gpio/pwm/adc/i2c
    controller nodes in the fixture must never appear as sockets of their
    own (only the two socket,fixture-nexus nodes do)."""
    board = project.project_edt(_edt(), "fixture-board")
    assert len(board.sockets) == 2


# ------------------------------------------------------- alias-aware lookup
#
# fixture_socket_bare's second label (fixture_bare_alias) is the fixture
# proving a socket node may declare more than one label, and every one of
# them must resolve -- without the defining-label dict growing a second
# entry per socket.


def test_project_edt_indexes_every_additional_label_as_an_alias() -> None:
    board = project.project_edt(_edt(), "fixture-board")
    assert board.aliases == {"fixture_bare_alias": "fixture_socket_bare"}


def test_resolve_finds_a_socket_by_its_defining_label() -> None:
    board = project.project_edt(_edt(), "fixture-board")
    assert board.resolve("fixture_socket_bare") is board.sockets["fixture_socket_bare"]


def test_resolve_finds_the_same_socket_by_its_alias() -> None:
    """The additive-conformance claim itself: BOTH labels of one node
    resolve to the identical BoardSocket."""
    board = project.project_edt(_edt(), "fixture-board")
    assert board.resolve("fixture_bare_alias") is board.resolve("fixture_socket_bare")


def test_resolve_of_an_unknown_ref_is_none() -> None:
    board = project.project_edt(_edt(), "fixture-board")
    assert board.resolve("no_such_socket") is None


def test_an_alias_does_not_double_key_the_sockets_census() -> None:
    """The critical constraint: board.sockets stays ONE entry per
    physical socket. analyzer/sockets.py's phys-socket diagnostic
    iterates board.sockets.values() to render "sockets of <board>: ..."
    (wording frozen by the unmapped-socket golden) -- a second key per
    socket would list it twice and churn that census."""
    board = project.project_edt(_edt(), "fixture-board")
    assert len(board.sockets) == 2
    assert "fixture_bare_alias" not in board.sockets


def test_a_bare_dict_get_does_not_find_the_alias() -> None:
    """Negative control: this is what a bare board.sockets.get(ref)
    does with an alias -- nothing, since the second label is
    inert without going through resolve(). Proves resolve() is doing
    real work, not just tolerating an already-working lookup."""
    board = project.project_edt(_edt(), "fixture-board")
    assert board.sockets.get("fixture_bare_alias") is None


def test_gpio_map_resolves_position_to_controller_pin_flags() -> None:
    socket = _socket()
    assert socket.type_name == "fixture-nexus"
    assert socket.gpio_map[0] == ("gpio_ctrl0", 5, 0)
    assert socket.gpio_map[1] == ("gpio_ctrl0", 6, 1)


def test_bus_ref_projects_label_and_path() -> None:
    socket = _socket()
    assert "i2c" in socket.buses
    assert socket.buses["i2c"].label == "i2c0"
    assert socket.buses["i2c"].path == "/i2c_ctrl@30"
    assert socket.buses["spi"].label == "spi_ctrl0"
    assert socket.buses["spi"].path == "/spi_ctrl@40"
    # subset exposure: a socket declaring no socket,uart at all simply
    # has no entry for it -- never a placeholder.
    assert "uart" not in socket.buses


def test_authored_cs_pool_is_read_verbatim_onto_its_own_bus() -> None:
    """cs_pool lives on BusRef, not on BoardSocket -- authored
    verbatim onto the ONE bus (spi) that carries a cs-pool property."""
    assert _socket().buses["spi"].cs_pool == [2, 3]


def test_a_bus_without_its_own_cs_pool_stays_none() -> None:
    """The SAME socket's i2c bus authors no cs-pool of its own -- stays
    None, never inheriting the sibling spi bus's value or an invented
    empty list. The ctype-fallback merge (analyzer/cs.py's
    effective_cs_pool) exists specifically for this case."""
    assert _socket().buses["i2c"].cs_pool is None


def test_bare_socket_has_no_bus_pwm_or_adc_entries() -> None:
    """Subset exposure and multi-function maps alike are declared by
    ABSENCE: a socket authoring none of socket,i2c/pwm-map/io-channel-map
    projects empty dicts, never placeholders."""
    socket = _bare_socket()
    assert socket.buses == {}
    assert socket.pwm_map == {}
    assert socket.adc_map == {}


# ------------------------------------------------- multi-bus socket widening
#
# A connector type naming more than one bus of a kind suffixes it with a
# role ("spi-sensors"/"spi-motors") -- project.py's pattern match against
# EVERY socket,* property name, not the fixed 3-entry table the rest of
# this file's fixture predates. A dedicated, hermetic edtlib.EDT (its own
# binding, its own DTS text) rather than fixture_board.dts/socket-fixture-
# nexus.yaml: no other test in this file needs these properties, and
# widening the shared fixture just for this would be pure churn on it.


def _multibus_edt(tmp_path: Path):
    binding_dir = tmp_path / "bindings"
    binding_dir.mkdir()
    (binding_dir / "socket-fixture-multibus.yaml").write_text(
        textwrap.dedent("""\
        description: purpose-built fixture binding for the multi-bus widening tests
        compatible: "socket,fixture-multibus"
        properties:
          "#gpio-cells":
            type: int
            required: true
          gpio-map:
            type: compound
            required: true
          gpio-map-mask:
            type: array
          gpio-map-pass-thru:
            type: array
          socket,spi-sensors:
            type: phandle
          socket,spi-motors:
            type: phandle
          socket,spi-sensors-cs-pool:
            type: array
          socket,spi-motors-cs-pool:
            type: array
        """)
    )
    dts_path = tmp_path / "multibus.dts"
    dts_path.write_text(
        textwrap.dedent("""\
        /dts-v1/;
        / {
            #address-cells = <1>;
            #size-cells = <1>;

            spi_a: spi_ctrl@0 {
                compatible = "fixturetest,spi-ctrl";
                reg = <0x0 0x4>;
            };
            spi_b: spi_ctrl@10 {
                compatible = "fixturetest,spi-ctrl";
                reg = <0x10 0x4>;
            };
            gpio0: gpio_ctrl@20 {
                compatible = "fixturetest,gpio-ctrl";
                reg = <0x20 0x4>;
                gpio-controller;
                #gpio-cells = <2>;
            };

            multibus_socket: connector_multibus {
                compatible = "socket,fixture-multibus";
                #gpio-cells = <2>;
                gpio-map-mask = <0xffffffff 0xffffffff>;
                gpio-map-pass-thru = <0 0>;
                gpio-map = <10 0 &gpio0 0 0>,
                          <11 0 &gpio0 1 0>;
                socket,spi-sensors = <&spi_a>;
                socket,spi-motors = <&spi_b>;
                socket,spi-sensors-cs-pool = <10>;
                socket,spi-motors-cs-pool = <11>;
            };
        };
        """)
    )
    ensure_devicetree_on_path()
    from devicetree import edtlib

    return edtlib.EDT(str(dts_path), [str(binding_dir)], default_prop_types=True)


def test_project_edt_widens_named_bus_properties_to_qualified_keys(tmp_path: Path) -> None:
    board = project.project_edt(_multibus_edt(tmp_path), "multibus-board")
    socket = board.sockets["multibus_socket"]
    assert set(socket.buses) == {"spi-sensors", "spi-motors"}
    assert socket.buses["spi-sensors"].label == "spi_a"
    assert socket.buses["spi-motors"].label == "spi_b"


def test_project_edt_widens_cs_pool_per_named_bus(tmp_path: Path) -> None:
    board = project.project_edt(_multibus_edt(tmp_path), "multibus-board")
    socket = board.sockets["multibus_socket"]
    assert socket.buses["spi-sensors"].cs_pool == [10]
    assert socket.buses["spi-motors"].cs_pool == [11]


def test_pwm_map_resolves_position_to_controller_and_channel() -> None:
    assert _socket().pwm_map[0] == ("defining_ctrl", 0)


def test_adc_map_resolves_position_to_controller_and_channel() -> None:
    assert _socket().adc_map[2] == ("adc_ctrl0", 1)


# ------------------------------------------ multi-parent io-channel-map
#
# frdm_k64f's own real io-channel-map splits across &adc0/&adc1, so a
# socket's io-channel-map ENTRIES can name two DIFFERENT ADC controllers
# -- confirmed here directly against `_project_channel_map` (project.py's
# shared checked read), which reads `entry.parent` PER ROW, never once
# for the whole map. A dedicated,
# hermetic edtlib.EDT (own binding, own DTS text), same reasoning as
# `_multibus_edt` above: no other test in this file needs a second ADC
# controller, so widening the shared fixture_board.dts just for this
# would be pure churn on every OTHER test that fixture already serves.


def _multi_adc_edt(tmp_path: Path):
    binding_dir = tmp_path / "bindings"
    binding_dir.mkdir()
    (binding_dir / "socket-fixture-multiadc.yaml").write_text(
        textwrap.dedent("""\
        description: purpose-built fixture binding for the multi-parent ADC test
        compatible: "socket,fixture-multiadc"
        properties:
          "#io-channel-cells":
            type: int
            required: true
          io-channel-map:
            type: compound
            required: true
          io-channel-map-mask:
            type: array
          io-channel-map-pass-thru:
            type: array
        """)
    )
    dts_path = tmp_path / "multiadc.dts"
    dts_path.write_text(
        textwrap.dedent("""\
        /dts-v1/;
        / {
            #address-cells = <1>;
            #size-cells = <1>;

            adc_a: adc_ctrl@0 {
                compatible = "fixturetest,adc-ctrl";
                reg = <0x0 0x4>;
                #io-channel-cells = <1>;
            };
            adc_b: adc_ctrl@10 {
                compatible = "fixturetest,adc-ctrl";
                reg = <0x10 0x4>;
                #io-channel-cells = <1>;
            };

            multiadc_socket: connector_multiadc {
                compatible = "socket,fixture-multiadc";
                #io-channel-cells = <1>;
                io-channel-map-mask = <0xffffffff>;
                io-channel-map-pass-thru = <0x00000000>;
                io-channel-map = <0 &adc_a 12>,
                                 <1 &adc_a 13>,
                                 <2 &adc_b 14>,
                                 <3 &adc_b 15>;
            };
        };
        """)
    )
    ensure_devicetree_on_path()
    from devicetree import edtlib

    return edtlib.EDT(str(dts_path), [str(binding_dir)], default_prop_types=True)


def test_adc_map_resolves_each_position_against_its_own_row_parent(tmp_path: Path) -> None:
    """Confirms rigc handles a multi-parent io-channel-map: positions 0/1
    resolve through adc_a, positions 2/3 through
    adc_b -- ALL FOUR from the ONE socket's ONE io-channel-map, never one
    controller silently winning."""
    board = project.project_edt(_multi_adc_edt(tmp_path), "multiadc-board")
    socket = board.sockets["multiadc_socket"]
    assert socket.adc_map[0] == ("adc_a", 12)
    assert socket.adc_map[1] == ("adc_a", 13)
    assert socket.adc_map[2] == ("adc_b", 14)
    assert socket.adc_map[3] == ("adc_b", 15)


def test_adc_map_multi_parent_channel_count_is_the_single_row_read(tmp_path: Path) -> None:
    """adc_cells stays the ONE declared count (1) regardless of how many
    DISTINCT controllers the map's rows name -- _project_channel_map reads
    cells per row but this socket's rows all agree, so the returned count
    is unambiguous."""
    board = project.project_edt(_multi_adc_edt(tmp_path), "multiadc-board")
    socket = board.sockets["multiadc_socket"]
    assert socket.adc_cells == 1
    assert len(socket.adc_map) == 4


# ------------------------------------------ multi-parent pwm-map
#
# Confirms the multi-parent result holds for PWM too, not only ADC: real
# sockets with a pwm-map are themselves multi-parent (nucleo_f401re:
# &pwm1/2/3/4; frdm_k64f: &ftm0/&ftm3), so this is ALSO proven
# structurally by the real corpus goldens regardless of this fixture --
# but a dedicated, hermetic
# unit test (own binding, own DTS text, three-cell #pwm-cells this time
# rather than ADC's one-cell #io-channel-cells) is the same
# belt-and-suspenders precedent `_multi_adc_edt` above already set, and
# is cheaper to read than a full board golden for exactly this property.


def _multi_pwm_edt(tmp_path: Path):
    binding_dir = tmp_path / "bindings"
    binding_dir.mkdir()
    (binding_dir / "socket-fixture-multipwm.yaml").write_text(
        textwrap.dedent("""\
        description: purpose-built fixture binding for the multi-parent PWM test
        compatible: "socket,fixture-multipwm"
        properties:
          "#pwm-cells":
            type: int
            required: true
          pwm-map:
            type: compound
            required: true
          pwm-map-mask:
            type: array
          pwm-map-pass-thru:
            type: array
        """)
    )
    dts_path = tmp_path / "multipwm.dts"
    dts_path.write_text(
        textwrap.dedent("""\
        /dts-v1/;
        / {
            #address-cells = <1>;
            #size-cells = <1>;

            tim_a: pwm_ctrl@0 {
                compatible = "fixturetest,pwm-ctrl";
                reg = <0x0 0x4>;
                #pwm-cells = <3>;
            };
            tim_b: pwm_ctrl@10 {
                compatible = "fixturetest,pwm-ctrl";
                reg = <0x10 0x4>;
                #pwm-cells = <3>;
            };

            multipwm_socket: connector_multipwm {
                compatible = "socket,fixture-multipwm";
                #pwm-cells = <3>;
                pwm-map-mask = <0xffffffff 0x00000000 0x00000000>;
                pwm-map-pass-thru = <0x00000000 0xffffffff 0xffffffff>;
                pwm-map = <0 0 0 &tim_a 1 0 0>,
                          <1 0 0 &tim_a 2 0 0>,
                          <2 0 0 &tim_b 0 0 0>,
                          <3 0 0 &tim_b 3 0 0>;
            };
        };
        """)
    )
    ensure_devicetree_on_path()
    from devicetree import edtlib

    return edtlib.EDT(str(dts_path), [str(binding_dir)], default_prop_types=True)


def test_pwm_map_resolves_each_position_against_its_own_row_parent(tmp_path: Path) -> None:
    """Confirms rigc handles a multi-parent pwm-map, the 3-cell
    (channel, period, flags) shape rather than ADC's
    1-cell one: positions 0/1 resolve through tim_a, positions 2/3
    through tim_b -- ALL FOUR from the ONE socket's ONE pwm-map, never
    one controller silently winning."""
    board = project.project_edt(_multi_pwm_edt(tmp_path), "multipwm-board")
    socket = board.sockets["multipwm_socket"]
    assert socket.pwm_map[0] == ("tim_a", 1)
    assert socket.pwm_map[1] == ("tim_a", 2)
    assert socket.pwm_map[2] == ("tim_b", 0)
    assert socket.pwm_map[3] == ("tim_b", 3)


def test_pwm_map_multi_parent_channel_count_is_the_single_row_read(tmp_path: Path) -> None:
    """pwm_cells stays the ONE declared count (3) regardless of how many
    DISTINCT controllers the map's rows name."""
    board = project.project_edt(_multi_pwm_edt(tmp_path), "multipwm-board")
    socket = board.sockets["multipwm_socket"]
    assert socket.pwm_cells == 3
    assert len(socket.pwm_map) == 4


# ------------------------------------------------- pwm_cells / adc_cells
#
# A carrier does not get to choose its own cell count -- BoardSocket must
# carry the count a real
# socket's own pwm-map/io-channel-map actually declares, not just the
# resolved (ctrl, channel) pair, so a carrier passing it through can be
# checked against it later (analyzer/sockets.py's compose_socket).


def test_pwm_cells_carries_the_socket_own_declared_count() -> None:
    assert _socket().pwm_cells == 2


def test_adc_cells_carries_the_socket_own_declared_count() -> None:
    assert _socket().adc_cells == 1


def test_bare_socket_has_no_pwm_or_adc_cells() -> None:
    """Declared by absence, matching pwm_map/adc_map's own empty-dict
    convention: a socket with no pwm-map/io-channel-map at all carries
    None, never a guessed count."""
    assert _bare_socket().pwm_cells is None
    assert _bare_socket().adc_cells is None


# --------------------------------------- a 3-cell PWM parent
#
# Zephyr's generic PWM consumer form is THREE cells (channel, period,
# flags) -- the norm upstream (55 of 75 surveyed bindings), not the rare
# case; lotus's own atmel,sam0-tcc-pwm 2-cell override is the outlier.
# A malformed or unsupported PWM parent shape must raise a named
# LoadError (phys-board), never an unhandled ValueError -- caught at
# resolve.load_board's own boundary (test_board_resolve.py owns THAT
# half; this file owns project.py's own raise).
#
# Both 2-cell and 3-cell PWM parents are individually supported. The
# fixture below (2-cell SOCKET, 3-cell PARENT) is the CHILD/PARENT
# MISMATCH witness: the two must agree, rigc does not translate between
# specifier widths -- both counts are individually supported, but they
# disagree with each other, which is a DIFFERENT diagnostic than
# "unsupported count" (see test_four_cell_pwm_parent_is_still_unsupported
# below for that one).


def _three_cell_pwm_edt(tmp_path: Path):
    binding_dir = tmp_path / "bindings"
    binding_dir.mkdir()
    (binding_dir / "socket-fixture-3cell.yaml").write_text(
        textwrap.dedent("""\
        description: purpose-built fixture binding for the 3-cell-PWM-parent diagnostic test
        compatible: "socket,fixture-3cell"
        properties:
          "#gpio-cells":
            type: int
            required: true
          gpio-map:
            type: compound
            required: true
          gpio-map-mask:
            type: array
          gpio-map-pass-thru:
            type: array
          "#pwm-cells":
            type: int
          pwm-map:
            type: compound
          pwm-map-mask:
            type: array
          pwm-map-pass-thru:
            type: array
        """)
    )
    dts_path = tmp_path / "three_cell_pwm.dts"
    dts_path.write_text(
        textwrap.dedent("""\
        /dts-v1/;
        / {
            #address-cells = <1>;
            #size-cells = <1>;

            gpio0: gpio_ctrl@0 {
                compatible = "fixturetest,gpio-ctrl";
                reg = <0x0 0x4>;
                gpio-controller;
                #gpio-cells = <2>;
            };
            pwm3: three_cell_pwm_ctrl@10 {
                compatible = "fixturetest,pwm-ctrl";
                reg = <0x10 0x4>;
                #pwm-cells = <3>;
            };

            three_cell_socket: connector_three_cell {
                compatible = "socket,fixture-3cell";
                #gpio-cells = <2>;
                gpio-map-mask = <0xffffffff 0xffffffff>;
                gpio-map-pass-thru = <0 0>;
                gpio-map = <0 0 &gpio0 0 0>;

                #pwm-cells = <2>;
                pwm-map-mask = <0xffffffff 0x00000000>;
                pwm-map-pass-thru = <0x00000000 0xffffffff>;
                pwm-map = <0 0 &pwm3 0 0 0>;
            };
        };
        """)
    )
    ensure_devicetree_on_path()
    from devicetree import edtlib

    return edtlib.EDT(str(dts_path), [str(binding_dir)], default_prop_types=True)


def test_three_cell_pwm_parent_raises_loaderror_not_valueerror(tmp_path: Path) -> None:
    """A 2-cell socket wired to a 3-cell parent controller: BOTH counts
    are individually supported, but they disagree with each other -- still a
    LoadError (phys-board), not a ValueError, naming the socket, the
    controller's defining label, and BOTH counts."""
    with pytest.raises(LoadError) as excinfo:
        project.project_edt(_three_cell_pwm_edt(tmp_path), "three-cell-board")
    (diag,) = excinfo.value.diags
    assert diag.code == "phys-board"
    assert "three_cell_socket" in diag.message
    assert "pwm3" in diag.message  # the controller's DEFINING label
    assert "<2>" in diag.message and "<3>" in diag.message
    assert "must equal" in diag.message


def test_three_cell_pwm_parent_names_both_cell_counts_and_the_controller(tmp_path: Path) -> None:
    """A 3-cell PWM parent is the COMMON case upstream (both twister
    boards' own st,stm32-pwm/nxp,ftm-pwm are 3-cell), so this mismatch
    diagnostic is user-facing, not a rare-guard afterthought -- it must
    name the controller by its own defining label, not just the
    socket."""
    with pytest.raises(LoadError) as excinfo:
        project.project_edt(_three_cell_pwm_edt(tmp_path), "three-cell-board")
    (diag,) = excinfo.value.diags
    assert "#pwm-cells" in diag.message
    assert "PWM" in diag.message.upper() or "pwm" in diag.message


def _self_consistent_pwm_edt(tmp_path: Path, cells: int):
    """A socket AND its parent controller both declaring the SAME
    #pwm-cells count -- the self-consistent case at whatever `cells` is,
    used both to prove a 3-cell parent resolves cleanly (accept) and
    that a genuinely unsupported count (e.g. 4) is still refused with the
    "not supported yet" wording; only {2, 3} are accepted."""
    binding_dir = tmp_path / "bindings"
    binding_dir.mkdir()
    (binding_dir / "socket-fixture-ncell.yaml").write_text(
        textwrap.dedent("""\
        description: purpose-built fixture binding for the self-consistent N-cell PWM test
        compatible: "socket,fixture-ncell"
        properties:
          "#gpio-cells":
            type: int
            required: true
          gpio-map:
            type: compound
            required: true
          "#pwm-cells":
            type: int
          pwm-map:
            type: compound
        """)
    )
    dts_path = tmp_path / "ncell_pwm.dts"
    child_words = " ".join(["0"] * cells)
    parent_words = " ".join(["0"] * cells)
    dts_path.write_text(
        textwrap.dedent(f"""\
        /dts-v1/;
        / {{
            #address-cells = <1>;
            #size-cells = <1>;

            gpio0: gpio_ctrl@0 {{
                compatible = "fixturetest,gpio-ctrl";
                reg = <0x0 0x4>;
                gpio-controller;
                #gpio-cells = <2>;
            }};
            pwmn: ncell_pwm_ctrl@10 {{
                compatible = "fixturetest,pwm-ctrl";
                reg = <0x10 0x4>;
                #pwm-cells = <{cells}>;
            }};

            ncell_socket: connector_ncell {{
                compatible = "socket,fixture-ncell";
                #gpio-cells = <2>;
                gpio-map = <0 0 &gpio0 0 0>;

                #pwm-cells = <{cells}>;
                pwm-map = <{child_words} &pwmn {parent_words}>;
            }};
        }};
        """)
    )
    ensure_devicetree_on_path()
    from devicetree import edtlib

    return edtlib.EDT(str(dts_path), [str(binding_dir)], default_prop_types=True)


def test_three_cell_pwm_self_consistent_is_accepted(tmp_path: Path) -> None:
    """A socket and its parent BOTH declaring #pwm-cells = <3> resolves
    cleanly -- no LoadError, pwm_cells carries the real count 3."""
    board = project.project_edt(_self_consistent_pwm_edt(tmp_path, 3), "ncell-board")
    socket = board.sockets["ncell_socket"]
    assert socket.pwm_cells == 3
    assert socket.pwm_map[0] == ("pwmn", 0)


def test_four_cell_pwm_parent_is_still_unsupported(tmp_path: Path) -> None:
    """A count outside the supported set {2, 3} -- both sides SELF-
    CONSISTENT at 4 -- must still be refused, with the "not supported
    yet" LoadError/phys-board wording. Distinct from the
    mismatch tests above, which disagree with EACH OTHER while both
    individually stay inside the supported set."""
    with pytest.raises(LoadError) as excinfo:
        project.project_edt(_self_consistent_pwm_edt(tmp_path, 4), "ncell-board")
    (diag,) = excinfo.value.diags
    assert diag.code == "phys-board"
    assert "ncell_socket" in diag.message
    assert "<4>" in diag.message
    assert "supports only" in diag.message
    assert "2-cell" in diag.message and "3-cell" in diag.message


def _self_consistent_adc_edt(tmp_path: Path, cells: int):
    """ADC's own twin of `_self_consistent_pwm_edt` above -- a socket and
    its parent io-channel controller both declaring the SAME
    #io-channel-cells count. Used to pin ADC's supported set at the
    STRICT singleton {1}: its checked read stays strict at exactly one
    cell, unlike PWM's wider {2, 3}."""
    binding_dir = tmp_path / "bindings"
    binding_dir.mkdir()
    (binding_dir / "socket-fixture-adc-ncell.yaml").write_text(
        textwrap.dedent("""\
        description: purpose-built fixture binding for the ADC cell-count test
        compatible: "socket,fixture-adc-ncell"
        properties:
          "#gpio-cells":
            type: int
            required: true
          gpio-map:
            type: compound
            required: true
          "#io-channel-cells":
            type: int
          io-channel-map:
            type: compound
        """)
    )
    dts_path = tmp_path / "ncell_adc.dts"
    child_words = " ".join(["0"] * (cells - 1))
    parent_words = " ".join(["0"] * (cells - 1))
    # Pre-joined so the io-channel-map template line stays inside the
    # line limit; a 1-cell socket contributes no extra words at all.
    child_cells = f" {child_words}" if child_words else ""
    parent_cells = f" {parent_words}" if parent_words else ""
    dts_path.write_text(
        textwrap.dedent(f"""\
        /dts-v1/;
        / {{
            #address-cells = <1>;
            #size-cells = <1>;

            gpio0: gpio_ctrl@0 {{
                compatible = "fixturetest,gpio-ctrl";
                reg = <0x0 0x4>;
                gpio-controller;
                #gpio-cells = <2>;
            }};
            adcn: ncell_adc_ctrl@10 {{
                compatible = "fixturetest,adc-ctrl";
                reg = <0x10 0x4>;
                #io-channel-cells = <{cells}>;
            }};

            ncell_adc_socket: connector_ncell_adc {{
                compatible = "socket,fixture-adc-ncell";
                #gpio-cells = <2>;
                gpio-map = <0 0 &gpio0 0 0>;

                #io-channel-cells = <{cells}>;
                io-channel-map = <0{child_cells} &adcn 0{parent_cells}>;
            }};
        }};
        """)
    )
    ensure_devicetree_on_path()
    from devicetree import edtlib

    return edtlib.EDT(str(dts_path), [str(binding_dir)], default_prop_types=True)


def test_adc_one_cell_self_consistent_is_still_accepted(tmp_path: Path) -> None:
    """ADC's own accept case, unchanged by this slice: a 1-cell socket
    and parent resolve cleanly."""
    board = project.project_edt(_self_consistent_adc_edt(tmp_path, 1), "ncell-adc-board")
    socket = board.sockets["ncell_adc_socket"]
    assert socket.adc_cells == 1
    assert socket.adc_map[0] == ("adcn", 0)


def test_adc_two_cell_self_consistent_is_still_refused(tmp_path: Path) -> None:
    """ADC is NOT widened alongside PWM -- a 2-cell ADC socket/parent,
    even self-consistent with each other, must still be refused. This
    is the mutation-check target: widening ADC's own supported set
    (e.g. to accept 2 cells) must make THIS test fail."""
    with pytest.raises(LoadError) as excinfo:
        project.project_edt(_self_consistent_adc_edt(tmp_path, 2), "ncell-adc-board")
    (diag,) = excinfo.value.diags
    assert diag.code == "phys-board"
    assert "ncell_adc_socket" in diag.message
    assert "<2>" in diag.message
    assert "supports only" in diag.message
    assert "1-cell" in diag.message


# ------------------------------------------------- controller-label determinism
#
# Mirrors upstream python-devicetree's test_controller_label.py coverage:
# the *-map target's identity must be node.labels[0] -- the DEFINING label --
# stable no matter what else composes onto the same node afterward.


def test_controller_label_is_the_defining_label() -> None:
    label, _channel = _socket().pwm_map[0]
    assert label == "defining_ctrl"


def test_controller_label_ignores_a_later_attached_alias() -> None:
    label, _channel = _socket().pwm_map[0]
    assert label != "legacy_alias"


def test_gpio_map_controller_label_is_the_defining_label() -> None:
    """The gpio side of the same invariant. project resolves the
    controller label INLINE for gpio-map and through _controller_label for
    pwm/adc -- two separate implementations, so pinning only the pwm side
    leaves a label regression on the gpio path undetectable. Position 2
    targets the dual-labelled node for exactly this."""
    ctrl_label, _pin, _flags = _socket().gpio_map[2]
    assert ctrl_label == "defining_ctrl"
    assert ctrl_label != "legacy_alias"


# ------------------------------------------------- conventional-label census
#
# Every socket,* node a board rig-extension declares must carry its
# connector type's conventional label -- "<type>" for a singleton,
# "<type>_<silkscreen>" for a family -- ALONGSIDE whatever board-prefixed
# label it already had. That is the fact Board.resolve() depends on: an
# alias only resolves if project actually saw it declared in the board's
# own devicetree.
#
# The node scan itself is board/census.py's scan_socket_nodes -- production
# code, shared rather than restated here. It reports type_name DASHED,
# exactly as compatible =
# "socket,<type>" spells it (the census's own mating-facing value); the
# label convention below compares against a LABEL, which uses
# underscores, so the underscoring happens HERE, once, for this one
# comparison only -- never inside the shared scanner.


def _conventional_label_offenders(text: str) -> list[str]:
    """The defining label of every socket,* node in text whose label set
    carries NO label matching its type's convention -- "<type>" or
    "<type>_<anything>". Empty when every node conforms."""
    offenders = []
    for node in scan_socket_nodes("<test>", text):
        type_name = node.type_name.replace("-", "_")
        if not any(
            label == type_name or label.startswith(type_name + "_") for label in node.labels
        ):
            offenders.append(node.labels[0] if node.labels else "<unlabeled>")
    return offenders


def test_conventional_label_offenders_detects_a_missing_alias() -> None:
    """Mechanism check for the checker itself, on synthetic text -- BEFORE
    trusting it to census the real tree. A node with no conventional
    label is flagged; the identical node WITH one is not."""
    missing = textwrap.dedent("""\
        / {
            board_ard: connector_arduino_r3 {
                compatible = "socket,arduino-r3";
            };
        };
        """)
    assert _conventional_label_offenders(missing) == ["board_ard"]

    present = textwrap.dedent("""\
        / {
            board_ard: arduino_r3: connector_arduino_r3 {
                compatible = "socket,arduino-r3";
            };
        };
        """)
    assert _conventional_label_offenders(present) == []


def test_every_board_rig_extension_socket_carries_its_type_convention_label() -> None:
    """The census over the REAL tree. Falsified by mutating the WORLD it
    observes -- drop a label from a real boards/extend/*.dtsi and this
    fails -- never by editing this assertion."""
    root = Path(MODULE_ROOT) / "boards" / "extend"
    offenders = []
    for path in sorted(root.rglob("*.dtsi")):
        for offender in _conventional_label_offenders(path.read_text()):
            offenders.append(f"{path.relative_to(MODULE_ROOT)}: {offender}")
    assert not offenders, (
        "socket,* node(s) with no label matching their connector type's "
        "naming convention ('<type>' singleton or '<type>_<silkscreen>' "
        f"family): {offenders}"
    )
