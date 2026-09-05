# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""board/census.py: the text-only census over board rig-extension SOURCES
that `west rigs --boards-for` runs against, and `boards_for`'s own
conformance query over synthetic Rig/Board values.

No corpus rig omits `socket:` today (checked: all 41 instance socket
references are explicit), so the inference-path tests below are the ONLY
place that discrimination is exercised at all -- these tests carry the
slice, pure and millisecond-fast."""

from __future__ import annotations

import textwrap

from rigc.board.census import (
    BoardVerdict,
    CensusBoard,
    board_targets,
    boards_for,
    census_board,
    scan_socket_nodes,
)
from rigc.model import Board, BoardSocket, Device, Rig, Shield
from rigc.tests.unit.analyzer.test_sockets import _ctype, _inst, _parent, _shield

# ---------------------------------------------------------------- census_board fixtures

_BOARD_YML_ONE_VARIANT = textwrap.dedent("""\
    board:
      extend: nucleo_f401re
      variants:
        - name: rig
          qualifier: stm32f401xe
    """)

_BOARD_YML_TWO_VARIANTS = textwrap.dedent("""\
    board:
      extend: mikroe_quail
      variants:
        - name: rig
          qualifier: stm32f427xx
        - name: rig2
          qualifier: stm32f427yy
    """)

_BOARD_YML_NEITHER_SHAPE = textwrap.dedent("""\
    board:
      revision:
        default: "1.0.0"
        revisions:
          - name: "1.0.0"
    """)

_TWO_LABEL_FRAGMENT = textwrap.dedent("""\
    / {
        board_ard: arduino_r3: connector_arduino_r3 {
            compatible = "socket,arduino-r3";
            socket,i2c = <&i2c1>;
            socket,spi = <&spi1>;
        };
    };
    """)

_NO_BUS_FRAGMENT = textwrap.dedent("""\
    / {
        bare_socket: connector_bare {
            compatible = "socket,bare";
        };
    };
    """)

_FRAGMENT_A = textwrap.dedent("""\
    / {
        sock_a: connector_a {
            compatible = "socket,typea";
        };
    };
    """)

_FRAGMENT_B = textwrap.dedent("""\
    / {
        sock_b: connector_b {
            compatible = "socket,typeb";
        };
    };
    """)


def test_census_board_keys_sockets_by_the_defining_label_only() -> None:
    boards = census_board(_BOARD_YML_ONE_VARIANT, [("f.dtsi", _TWO_LABEL_FRAGMENT)])
    assert len(boards) == 1
    board = boards[0].board
    assert set(board.sockets) == {"board_ard"}
    assert board.aliases == {"arduino_r3": "board_ard"}


def test_census_board_type_name_stays_dashed() -> None:
    """compatible = "socket,arduino-r3" must project as "arduino-r3",
    never underscored -- the census's value
    feeds mating_ok against shield.plugs, which uses the identical dashed
    spelling."""
    boards = census_board(_BOARD_YML_ONE_VARIANT, [("f.dtsi", _TWO_LABEL_FRAGMENT)])
    socket = boards[0].board.sockets["board_ard"]
    assert socket.type_name == "arduino-r3"


def test_census_board_records_declared_bus_kinds() -> None:
    boards = census_board(_BOARD_YML_ONE_VARIANT, [("f.dtsi", _TWO_LABEL_FRAGMENT)])
    socket = boards[0].board.sockets["board_ard"]
    assert set(socket.buses) == {"i2c", "spi"}
    assert "uart" not in socket.buses


def test_census_board_socket_declaring_no_bus_props_has_empty_buses() -> None:
    boards = census_board(_BOARD_YML_ONE_VARIANT, [("f.dtsi", _NO_BUS_FRAGMENT)])
    socket = boards[0].board.sockets["bare_socket"]
    assert socket.buses == {}


def test_census_board_records_qualified_named_bus_kinds() -> None:
    """A connector type naming more than one bus of a kind suffixes it
    with a role -- the census's own bus-membership scan must recognize
    the QUALIFIED name as a distinct member, in lockstep with
    board/project.py's own regex, or --boards-for silently stops recognizing
    a shield that needs a named bus."""
    fragment = textwrap.dedent("""\
        / {
            multibus_sock: connector_multibus {
                compatible = "socket,fixture-multibus";
                socket,spi-sensors = <&spi_a>;
                socket,spi-motors = <&spi_b>;
            };
        };
        """)
    boards = census_board(_BOARD_YML_ONE_VARIANT, [("f.dtsi", fragment)])
    socket = boards[0].board.sockets["multibus_sock"]
    assert set(socket.buses) == {"spi-sensors", "spi-motors"}


def test_census_board_does_not_mistake_a_cs_pool_property_for_a_bus() -> None:
    """Negative control: a named bus's own "-cs-pool" property must never
    be counted as a SECOND bus of that name."""
    fragment = textwrap.dedent("""\
        / {
            multibus_sock: connector_multibus {
                compatible = "socket,fixture-multibus";
                socket,spi-sensors = <&spi_a>;
                socket,spi-sensors-cs-pool = <10>;
            };
        };
        """)
    boards = census_board(_BOARD_YML_ONE_VARIANT, [("f.dtsi", fragment)])
    socket = boards[0].board.sockets["multibus_sock"]
    assert set(socket.buses) == {"spi-sensors"}


def test_census_board_two_variants_yield_two_targets_over_one_socket_set() -> None:
    boards = census_board(_BOARD_YML_TWO_VARIANTS, [("f.dtsi", _TWO_LABEL_FRAGMENT)])
    assert {cb.target for cb in boards} == {
        "mikroe_quail/stm32f427xx/rig",
        "mikroe_quail/stm32f427yy/rig2",
    }
    assert len(boards) == 2
    assert set(boards[0].board.sockets) == set(boards[1].board.sockets) == {"board_ard"}


def test_census_board_skips_a_board_yml_with_neither_shape() -> None:
    assert census_board(_BOARD_YML_NEITHER_SHAPE, []) == []


def test_board_targets_skips_a_variant_entry_missing_its_qualifier() -> None:
    """The skip is per ENTRY, not per file: a board.yml whose variants
    mix a complete entry with an incomplete one yields the complete one
    alone. Pinning this separately from the whole-file skip above because
    census_boards now short-circuits on `board_targets(...)[1]` being
    empty -- an entry-level skip that silently emptied the list would
    make a real board invisible to the census rather than merely
    partial."""
    mixed = textwrap.dedent("""\
        board:
          extend: some_board
          variants:
            - name: rig
              qualifier: soc1
            - name: no_qualifier_here
            - not_even_a_mapping
        """)
    extend, targets = board_targets(mixed)
    assert extend == "some_board"
    assert targets == ["some_board/soc1/rig"]


def test_scan_socket_nodes_yields_only_socket_compatible_nodes() -> None:
    """Two distinct non-socket shapes a real board fragment mixes in with
    its sockets, both of which must be passed over rather than
    manufacturing a socket with an empty type:

      * a labelled node with some OTHER compatible (`leds`) -- this one
        DOES match the node pattern, and is rejected on its compatible;
      * a phandle-target reference to a node the fragment's own file never
        defines (lotus's `adc0: &adc {};`) -- the shape that makes a regex
        scan viable at all, since it is not standalone-parseable. Its `&`
        is not a word character, so the node pattern never matches it in
        the first place.

    Both are asserted because they fail for different reasons, and a test
    naming only the second would leave the compatible check itself
    unexercised."""
    text = textwrap.dedent("""\
        / {
            adc0: &adc {};
            board_leds: leds {
                compatible = "gpio-leds";
            };
            real_sock: connector_real {
                compatible = "socket,grove";
            };
        };
        """)
    assert [n.labels[0] for n in scan_socket_nodes("f.dtsi", text)] == ["real_sock"]


def test_census_board_collects_sockets_across_several_fragments() -> None:
    boards = census_board(
        _BOARD_YML_ONE_VARIANT, [("a.dtsi", _FRAGMENT_A), ("b.dtsi", _FRAGMENT_B)]
    )
    assert set(boards[0].board.sockets) == {"sock_a", "sock_b"}


# ---------------------------------------------------------------- boards_for


def _census(target: str, board: Board) -> CensusBoard:
    return CensusBoard(target=target, dir=None, board=board)


def _device_needing(bus: str) -> Device:
    return Device(
        name="d",
        label="d",
        compatible=None,
        bus=bus,
        group=None,
        reg=None,
        addr_from=None,
        cs_position=None,
    )


def test_boards_for_conforms_via_the_defining_label() -> None:
    board = Board(name="b", sockets={"ard": _parent(label="ard", path="/ard")})
    inst = _inst("i1", "ard", _shield())
    rig = Rig(name="r", instances=[inst])

    verdicts = boards_for(rig, {"arduino-r3": _ctype()}, [_census("t1", board)])

    assert verdicts == [BoardVerdict(target="t1", conforms=True, diags=[])]


def test_boards_for_conforms_via_the_conventional_alias() -> None:
    """The same rig naming the CONVENTIONAL alias (rather than the
    board-prefixed defining label) conforms against the identical
    board -- resolve_sockets goes through Board.resolve, not a bare
    dict lookup."""
    socket = _parent(label="nucleo_ard", path="/nucleo_ard")
    board = Board(name="b", sockets={"nucleo_ard": socket}, aliases={"arduino_r3": "nucleo_ard"})
    inst = _inst("i1", "arduino_r3", _shield())
    rig = Rig(name="r", instances=[inst])

    verdicts = boards_for(rig, {"arduino-r3": _ctype()}, [_census("t1", board)])

    assert verdicts[0].conforms is True


def test_boards_for_type_mismatch_does_not_conform() -> None:
    socket = BoardSocket(label="mb", path="/mb", type_name="mikrobus", gpio_map={}, buses={})
    board = Board(name="b", sockets={"mb": socket})
    inst = _inst("i1", "mb", _shield(plugs="arduino-r3"))
    rig = Rig(name="r", instances=[inst])

    verdicts = boards_for(rig, {"arduino-r3": _ctype()}, [_census("t1", board)])

    assert verdicts[0].conforms is False


def test_boards_for_bus_subset_gap_does_not_conform() -> None:
    """The real shield-uart-subset-frdm shape: a shield needing UART
    against a socket declaring no socket,uart does not conform."""
    socket = BoardSocket(label="ard", path="/ard", type_name="arduino-r3", gpio_map={}, buses={})
    board = Board(name="b", sockets={"ard": socket})
    shield = Shield(
        name="sh", label="sh", plugs={"plug": "arduino-r3"}, devices=[_device_needing("uart")]
    )
    inst = _inst("i1", "ard", shield)
    rig = Rig(name="r", instances=[inst])

    verdicts = boards_for(rig, {"arduino-r3": _ctype()}, [_census("t1", board)])

    assert verdicts[0].conforms is False


def test_boards_for_inference_one_candidate_conforms() -> None:
    board = Board(name="b", sockets={"ard": _parent(label="ard", path="/ard")})
    inst = _inst("i1", None, _shield())  # socket: omitted
    rig = Rig(name="r", instances=[inst])

    verdicts = boards_for(rig, {"arduino-r3": _ctype()}, [_census("t1", board)])

    assert verdicts[0].conforms is True


def test_boards_for_inference_two_candidates_does_not_conform() -> None:
    board = Board(
        name="b",
        sockets={
            "ard1": _parent(label="ard1", path="/ard1"),
            "ard2": _parent(label="ard2", path="/ard2"),
        },
    )
    inst = _inst("i1", None, _shield())
    rig = Rig(name="r", instances=[inst])

    verdicts = boards_for(rig, {"arduino-r3": _ctype()}, [_census("t1", board)])

    assert verdicts[0].conforms is False


def test_boards_for_inference_zero_candidates_does_not_conform() -> None:
    socket = BoardSocket(label="mb", path="/mb", type_name="mikrobus", gpio_map={}, buses={})
    board = Board(name="b", sockets={"mb": socket})
    inst = _inst("i1", None, _shield(plugs="arduino-r3"))  # no match at all
    rig = Rig(name="r", instances=[inst])

    verdicts = boards_for(
        rig, {"arduino-r3": _ctype(), "mikrobus": _ctype(name="mikrobus")}, [_census("t1", board)]
    )

    assert verdicts[0].conforms is False


def test_boards_for_two_instances_on_a_non_stackable_socket_does_not_conform() -> None:
    board = Board(name="b", sockets={"ard": _parent(label="ard", path="/ard")})
    shield = _shield()
    inst1 = _inst("i1", "ard", shield)
    inst2 = _inst("i2", "ard", shield)
    rig = Rig(name="r", instances=[inst1, inst2])

    verdicts = boards_for(rig, {"arduino-r3": _ctype(stackable=False)}, [_census("t1", board)])

    assert verdicts[0].conforms is False
