# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Board DT reader, edtlib-based -- the production reader resolve.load_board
delegates to. It projects a real board's own devicetree, read via a
standalone edtlib.EDT (see edt_build.py), onto model.Board /
model.BoardSocket: the analyzer reads the board DT to find socket nodes
by compatible. model.py's dataclasses are populated here, never
redefined.

pwm_map / adc_map project the socket node's standard pwm-map /
io-channel-map nexuses -- read the same way gpio-map already is, via
edtlib.Node.maps() -- onto a position -> (controller label, channel) shape
(see boards/extend/seeed/seeeduino_lotus/grove_sockets.dtsi). Not every
socket carries these maps (only PWM/ADC-capable ones do); node.maps simply
omits the key for a ``*-map`` property the node doesn't author, so the loops
below are no-ops for sockets without one.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

# $ZEPHYR_BASE is what locates the devicetree package, so requiring it at
# IMPORT time would make merely importing this module -- which pytest does
# to every test module, to discover its markers, before any -m selection
# can deselect one -- fail without a Zephyr tree. Deferred to first use
# instead, the same shape edt_build uses: annotations are lazy under
# `from __future__ import annotations`, so only the single runtime
# reference below (an isinstance check in _project_socket) needs the real
# module.
from .edt_build import BuildRecipe, build_edt, ensure_devicetree_on_path

if TYPE_CHECKING:
    from devicetree import edtlib

from ..buskind import BUS_PROP_RE as _BUS_PROP_RE
from ..buskind import CS_POOL_PROP_RE as _CS_POOL_PROP_RE
from ..diag import LoadError, SourceRef, error
from ..model import Board, BoardSocket, BusRef

#: socket,<kind> or socket,<kind>-<role> -- a connector type names an
#: additional bus of a kind by suffixing the kind with a role (multi-bus-
#: socket schema, Sec 2); the QUALIFIED name (kind, or kind-role) is the
#: key BoardSocket.buses/ConnectorType.cs_pool use throughout. loader/shields.py
#: and registry.py read the identical two patterns off their own inputs
#: -- see buskind.py for the regexes themselves and why they live there.


def load_board(name: str, dts_path: str, recipe: BuildRecipe, workdir: str) -> Board:
    """Build a standalone edtlib.EDT over the board's OWN .dts (dts_path,
    no rig overlay, no shield/app context) and project every socket,* node
    into a model.Board -- the edtlib-side counterpart of
    resolve.load_board.

    Returns the projected Board; the caller owns it."""
    edt = build_edt(dts_path, recipe, workdir)
    return project_edt(edt, name)


def project_edt(edt: edtlib.EDT, name: str) -> Board:
    """Project an ALREADY-BUILT edtlib.EDT (fresh, or unpickled from a real
    build's edt.pickle) into a model.Board. Split out from load_board so
    both a fresh read and a real build's own edt.pickle can share this
    exact projection.

    Returns a fresh Board holding one BoardSocket per socket,*-compatible
    node, keyed by its defining label (node.labels[0]); every OTHER label
    the node declares projects into Board.aliases instead of a second
    sockets entry -- DT allows several labels per node, and a board
    rig-extension may add its
    connector type's conventional label (e.g. "arduino_r3") alongside the
    board-prefixed one it already had ("nucleo_ard") without renaming
    anything. The EDT is read-only."""
    sockets: dict[str, BoardSocket] = {}
    aliases: dict[str, str] = {}
    for node in edt.nodes:
        compat = node.matching_compat
        if compat is None or not compat.startswith("socket,"):
            continue
        socket = _project_socket(node, compat)
        sockets[socket.label] = socket
        for alias in node.labels[1:]:
            aliases[alias] = socket.label
    return Board(name=name, sockets=sockets, aliases=aliases)


def _project_socket(node: edtlib.Node, compat: str) -> BoardSocket:
    if not node.labels:
        raise ValueError(
            f"socket node {node.path} has no label -- rig socket: references sockets by label"
        )
    label = node.labels[0]
    type_name = compat.split(",", 1)[1]

    gpio_map: dict[int, tuple[str, int, int]] = {}
    for entry in node.maps.get("gpio", []):
        pos, _pos_flags = entry.child_specifiers
        pin, flags = entry.parent_specifiers
        ctrl = entry.parent
        if not ctrl.labels:
            raise ValueError(f"gpio controller {ctrl.path} has no label")
        gpio_map[pos] = (ctrl.labels[0], pin, flags)

    # Per-bus cs_pool, keyed the same qualified way as buses below: the
    # legacy role-less "socket,cs-pool" (every real connector type's own
    # spelling) always means the bare "spi" bus, since CS only ever
    # applies to SPI; "socket,<kind>-<role>-cs-pool" is a named bus's own.
    # Built before buses so each BusRef below can carry its own value at
    # construction time.
    cs_pools: dict[str, list[int]] = {}
    legacy_cs_prop = node.props.get("socket,cs-pool")
    if legacy_cs_prop is not None:
        assert isinstance(legacy_cs_prop.val, list)
        cs_pools["spi"] = cast(list[int], legacy_cs_prop.val)
    for prop_name, prop in node.props.items():
        m = _CS_POOL_PROP_RE.match(prop_name)
        if m is None:
            continue
        assert isinstance(prop.val, list)
        cs_pools[m.group(1)] = cast(list[int], prop.val)

    # edtlib back-fills the binding default here when the socket doesn't
    # author its own cs-pool property, provided the type's binding
    # declares it with a default (arduino-r3.yaml, mikrobus.yaml both do
    # for the bare "spi" bus). For those types this value is already the
    # EFFECTIVE one, same as the analyzer's own merge would compute
    # (analyzer/cs.py's effective_cs_pool: bus.cs_pool if not None else
    # ctype.cs_pool[qualified_key]) -- so for a real board socket of such
    # a type, this bus's cs_pool is never None and that merge's
    # ctype-fallback branch is inert.
    #
    # That merge is not dead code in general, though: this function is not
    # the only source of a BoardSocket. grove.yaml declares no
    # socket,cs-pool property at all (Grove never exposes SPI/CS), so a
    # grove socket's spi bus never even exists here -- harmlessly, since CS
    # allocation never reaches a socket with no "spi" bus. More
    # significantly, the analyzer's carrier/mux composition
    # (analyzer/sockets.py's compose_socket) builds each pass-through
    # bus's cs_pool from model.ExposedSocket.cs_pool -- the CARRIER'S OWN
    # authored override on its exposed socket node, parsed by loader/shields.py
    # with no binding-default backfill at all, and never the PARENT
    # socket's own (possibly edtlib-backfilled) BusRef.cs_pool. A carrier
    # that never authors socket,cs-pool on its exposed socket node
    # (arduino_uno_click, i2c_mux) therefore yields no per-bus cs_pool
    # there regardless of the connector type's binding default OR of
    # what the parent socket's own bus happens to carry, so the
    # analyzer's ctype-fallback branch is very much alive for that path.
    buses: dict[str, BusRef] = {}
    for prop_name, prop in node.props.items():
        m = _BUS_PROP_RE.match(prop_name)
        if m is None:
            continue
        bus_node = prop.val
        # The one runtime reference to edtlib in this module; anything
        # holding an EDT to project already has devicetree importable,
        # since it could not have been built or unpickled otherwise.
        ensure_devicetree_on_path()
        from devicetree import edtlib

        assert isinstance(bus_node, edtlib.Node)
        if not bus_node.labels:
            raise ValueError(f"bus controller {bus_node.path} has no label")
        qualified = prop_name[len("socket,") :]
        buses[qualified] = BusRef(
            label=bus_node.labels[0], path=bus_node.path, cs_pool=cs_pools.get(qualified)
        )

    pwm_map, pwm_cells = _project_channel_map(node, label, "pwm", "pwm")
    adc_map, adc_cells = _project_channel_map(node, label, "io-channel", "adc")

    return BoardSocket(
        label=label,
        path=node.path,
        type_name=type_name,
        gpio_map=gpio_map,
        buses=buses,
        pwm_map=pwm_map,
        pwm_cells=pwm_cells,
        adc_map=adc_map,
        adc_cells=adc_cells,
        src=SourceRef(node.filename, node.lineno, label),
    )


#: pwm/adc's shared checked-read table: the SET of parent (controller)
#: cell counts rigc supports per function today, plus the
#: wording an unsupported-count diagnostic needs. NOT a guess at what
#: MIGHT show up -- a survey of upstream Zephyr's own PWM bindings found 55 of 75
#: declare THREE cells (channel, period, flags) and only 7 declare two
#: (lotus's own atmel,sam0-tcc-pwm among them), so BOTH shapes are real
#: and neither is a rare guard; io-channel is close to uniform (107 of
#: 108 bindings are 1-cell) and stays a strict singleton, checked the
#: same way regardless, for the identical reason (a checked read, not a
#: guess). Widening this set to add a shape means widening
#: `supported_desc`/`unsupported_note` alongside it -- both describe
#: EVERY member of `supported`, not just the smallest.
_CHANNEL_FN: dict[str, dict[str, object]] = {
    "pwm": {
        "cells_prop": "#pwm-cells",
        "supported": frozenset({2, 3}),
        "supported_desc": "2-cell (channel, period) or 3-cell (channel, period, flags)",
        "unsupported_note": (
            "only 2-cell (channel, period) and 3-cell (channel, period, "
            "flags) PWM parents (covering both lotus's atmel,sam0-tcc-pwm "
            "and upstream's common st,stm32-pwm/nxp,ftm-pwm shape) are "
            "supported today"
        ),
    },
    "adc": {
        "cells_prop": "#io-channel-cells",
        "supported": frozenset({1}),
        "supported_desc": "1-cell (channel)",
        "unsupported_note": "multi-cell ADC controllers are not supported yet",
    },
}


def _project_channel_map(
    node: edtlib.Node, label: str, specifier_space: str, fn: str
) -> tuple[dict[int, tuple[str, int]], int | None]:
    """pwm_map / adc_map's shared checked read: replaces a bare
    `pos, _pos_period = entry.child_specifiers` /
    `channel, _channel_period = entry.parent_specifiers` destructuring --
    which raises an unhandled ValueError the instant a real controller's
    own declared cell count differs from what rigc hardcodes (a
    traceback, not a diagnostic) -- with a checked
    length read that raises LoadError (phys-board), naming the socket,
    the controller, and BOTH cell counts, whenever EITHER side's own
    declared count falls outside `_CHANNEL_FN`'s supported SET, or the
    two sides disagree with EACH OTHER even though both are
    individually supported: a nexus's mask/pass-thru idiom requires the
    child and parent specifier widths equal, and rigc does not translate
    between specifier widths. `resolve.load_board` is the
    catch boundary that turns this into the caller's normal
    (board, diagnostics, deps) return shape, exactly as dtsio.py's own
    LoadError raises already do for a fatal cpp/parse failure.

    Returns (position -> (controller label, channel), the cell count
    actually used); a socket authoring no map for this specifier space
    yields `({}, None)` (declared by absence, never a placeholder count)."""
    spec = _CHANNEL_FN[fn]
    supported = cast(frozenset[int], spec["supported"])
    result: dict[int, tuple[str, int]] = {}
    cells: int | None = None
    for entry in node.maps.get(specifier_space, []):
        ctrl = entry.parent
        ctrl_label = ctrl.labels[0] if ctrl.labels else ctrl.path
        child_n = len(entry.child_specifiers)
        parent_n = len(entry.parent_specifiers)
        if child_n not in supported:
            raise LoadError(
                error(
                    "phys-board",
                    f"socket '{label}': its own {spec['cells_prop']} declares "
                    f"<{child_n}>, but rigc supports only a "
                    f"{spec['supported_desc']} {fn.upper()} socket nexus today",
                    (SourceRef(node.filename, node.lineno, label),),
                )
            )
        if parent_n not in supported:
            raise LoadError(
                error(
                    "phys-board",
                    f"socket '{label}': {fn.upper()} controller '{ctrl_label}' "
                    f"declares {spec['cells_prop']} = <{parent_n}>, "
                    f"but rigc supports only a "
                    f"{spec['supported_desc']} {fn.upper()} parent today -- "
                    f"{spec['unsupported_note']}",
                    (SourceRef(node.filename, node.lineno, label),),
                )
            )
        if child_n != parent_n:
            raise LoadError(
                error(
                    "phys-board",
                    f"socket '{label}': its own {spec['cells_prop']} declares "
                    f"<{child_n}>, but {fn.upper()} controller '{ctrl_label}' "
                    f"declares {spec['cells_prop']} = <{parent_n}> -- a "
                    "socket's own declared cell count must equal its parent "
                    "controller's (rigc does not translate between "
                    "specifier widths)",
                    (SourceRef(node.filename, node.lineno, label),),
                )
            )
        pos = entry.child_specifiers[0]
        channel = entry.parent_specifiers[0]
        result[pos] = (_controller_label(entry.parent), channel)
        cells = child_n
    return result, cells


def _controller_label(node: edtlib.Node) -> str:
    """The controller's DEFINING label for a *-map target: node.labels[0],
    the label the node's own declaring dtsi gives it (dtlib's label list is
    append-only and never reordered, so index 0 is permanently the
    first-attached label no matter what else later aliases onto the same
    node). This is the only choice stable against module composition --
    a socket file or an unrelated board extension may attach further
    aliases to a shared controller (e.g. a legacy per-pin label), and doing
    so must never change what this function reports. Consistent with the
    labels[0] already used for gpio-map targets and bus refs in this
    module: *-map controllers get the identical treatment.

    Constraint the code cannot show: this label is emitted verbatim into
    overlay text (&<label> { ... }), so emitted golden text is the only
    guard on it -- resolved (dts_equiv) resolves labels away and cannot
    catch a regression here."""
    if not node.labels:
        raise ValueError(f"controller node {node.path} has no label")
    return node.labels[0]
