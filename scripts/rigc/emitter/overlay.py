# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""rig-gen.overlay and rig-gen-includes.dtsi's payload: the device-tree
projection of a Solved rig -- nexus synthesis, I2C scopes + mux nesting,
SPI/cs-gpios, collections, plain groups, controllers, the device-node
renderer.

Label policy: generated label = <instance>_<shield-local label>, e.g.
logger_a_dl_rtc.

Per-instance parameters: a rig-assigned params: value is emitted
VERBATIM -- the raw token text, never resolved here -- so
rig-gen.overlay stays readable (zephyr,code = <INPUT_KEY_1>;, not a bare
number). Resolving those tokens is sheet.py's concern (the config
sheet's human-facing display value), not this module's.
"""

from __future__ import annotations

from collections.abc import Iterator

from ..analyzer import ChannelResolution, Solved
from ..analyzer.socketmap import for_bus_device, for_ref, slots_of
from ..buskind import is_bus_kind
from ..model import BoardSocket, ConnectorType, Device, FunctionRef, Instance, Rig
from .banner import GEN


def _nexus(socket: BoardSocket) -> str:
    """The DT label a socket is referenced through. Board sockets are real
    nodes (their own label); carrier-exported sockets are referenced through
    the nexus the emitter synthesizes for them."""
    return socket.nexus_label or socket.label


def _instance_extra_props(inst: Instance, dev: Device) -> list[tuple[str, str]]:
    """dev.extra_props, with this INSTANCE's rig-assigned params:
    substituted in: a property the rig assigns REPLACES the shield's own
    rendering of it (a default being overridden) or is simply ADDED (the
    shield declared it required, so there is no default to replace) --
    emitted verbatim, never resolved. Every device-node rendering path
    (plain, collected, mux-nested) goes through this instead of
    dev.extra_props directly, so a parameter assignment on any of them is
    honored the same way."""
    assigned = inst.params.get(dev.label, {})
    if not assigned:
        return dev.extra_props
    kept = [(name, rendered) for name, rendered in dev.extra_props if name not in assigned]
    added = [(name, f"{name} = <{value}>;") for name, value in sorted(assigned.items())]
    return kept + added


def _i2c_scopes(rig: Rig, s: Solved, types: dict[str, ConnectorType]) -> list[str]:
    """The I2C scopes block: one `&bus {...};` per physical I2C bus in use,
    each device node emitted directly or, for a mux interposer, nested
    under its own synthesized channel scopes. rig/s/types are read-only;
    returns fresh lines the caller owns, one bus scope's lines appended
    after another in `s.bus_label` order."""
    out: list[str] = []
    # I2C scopes -- rigc is the sole author of reg + unit-address, always
    # as a matching pair (address authority rule). A mux's channels are NEW
    # scopes emitted nested inside their mux device, not at the top level.
    mux_channels: dict[str, list[tuple[int, str]]] = {}
    for path, (root, channel) in s.scopes.items():
        mux_channels.setdefault(root, []).append((channel, path))
    for bus_path in sorted(s.bus_label):
        if bus_path in s.scopes:  # a mux channel -- emitted nested
            continue
        devs = list(_bus_devices(rig, s, "i2c", bus_path))
        if not devs:
            continue
        out.append(f"&{s.bus_label[bus_path]} {{")
        for inst, dev, _socket in sorted(devs, key=lambda m: s.addr[(m[0].name, m[1].name)]):
            addr = s.addr[(inst.name, dev.name)]
            label = f"{inst.name}_{dev.label}"
            if label in mux_channels:  # scope-creating interposer
                out += _mux_node(rig, s, types, inst, dev, addr, mux_channels[label])
            else:
                out += _device_node(s, types, inst, dev, unit=f"{addr:x}", reg=f"<{addr:#04x}>")
        out.append("};")
        out.append("")
    return out


def _spi_scopes(rig: Rig, s: Solved, types: dict[str, ConnectorType]) -> list[str]:
    """The SPI scopes block: one `&bus {...};` per physical SPI bus with
    chip-selects, its cs-gpios array and each child device's reg written
    together. rig/s/types are read-only; returns fresh lines the caller
    owns, one bus scope's lines appended after another in `s.cs_gpios`
    order."""
    out: list[str] = []
    # SPI scopes -- cs-gpios array and child reg written together
    for bus_path, entries in sorted(s.cs_gpios.items()):
        devs = list(_bus_devices(rig, s, "spi", bus_path))
        if not devs:
            continue
        out.append(f"&{s.bus_label[bus_path]} {{")
        cs = ", ".join(f"<&{_nexus(sock)} {pos} 1 /* ACTIVE_LOW */>" for sock, pos in entries)
        out.append(f"\tcs-gpios = {cs};")
        for inst, dev, _socket in sorted(devs, key=lambda m: s.cs[(m[0].name, m[1].name)][0]):
            index, _pos = s.cs[(inst.name, dev.name)]
            out += _device_node(s, types, inst, dev, unit=str(index), reg=f"<{index}>")
        out.append("};")
        out.append("")
    return out


def _plain_groups(rig: Rig, s: Solved, types: dict[str, ConnectorType]) -> list[str]:
    """The plain non-bus device groups block: one `/ { <instance> {...}; };`
    container per instance that has neither a bus nor a collected device.
    rig/s/types are read-only; returns fresh lines the caller owns, empty
    when no instance has a plain device."""
    root_nodes: list[str] = []
    for inst in sorted(rig.instances, key=lambda i: i.name):
        plain_devs = [d for d in inst.shield.devices if d.bus is None and d.collect is None]
        if not plain_devs or not slots_of(s.sockets, inst):
            continue
        root_nodes.append(f"\t{inst.name} {{")
        for plain_dev in sorted(plain_devs, key=lambda d: d.name):
            root_nodes += ["\t" + line for line in _device_node(s, types, inst, plain_dev)]
        root_nodes.append("\t};")
    if not root_nodes:
        return []
    return ["/ {", *root_nodes, "};", ""]


def render_overlay(
    rig: Rig, s: Solved, types: dict[str, ConnectorType], needed_includes: list[str] | None = None
) -> str:
    """rig-gen.overlay's full text. rig/s/types are read-only; returns a
    fresh string the caller owns. `needed_includes`
    (`emitter._needed_param_includes`) is the caller's own decision about
    which headers this rig's params actually need -- this function only
    gates the quoted #include line on whether the list is non-empty; it
    never derives the list itself."""
    out = []
    if needed_includes:
        # Opens the file: the needed parameter vocabulary reaches cpp
        # before anything that might use it, via a quoted include
        # resolved against this file's own directory (<build>/rig/, where
        # the emitter also writes rig-gen-includes.dtsi).
        out.append('#include "rig-gen-includes.dtsi"')
    out += [f"/* {GEN}", f" * rig: {rig.name}  board: {rig.board}", " */", ""]

    out += _synth_nexus_nodes(s)
    out += _i2c_scopes(rig, s, types)
    out += _spi_scopes(rig, s, types)

    # collection bindings (gpio-keys/gpio-leds, ...): entries from every
    # instance aggregate under ONE node per compatible
    out += _collections(rig, s, types)

    out += _plain_groups(rig, s, types)

    out += _controllers(s)
    return "\n".join(out)


def _controllers(s: Solved) -> list[str]:
    """Enable the timer/adc controllers a PWM/ADC claim resolved to, and NOTE
    the board-provided pin-mux each needs (rigc names the pinctrl
    requirement; applying the SoC-specific fragment is the board's job,
    stubbed here)."""
    if not s.controllers:
        return []
    out = [
        "/* PWM/ADC: enable the resolved controllers; the pin-mux (pinctrl)",
        " * for each muxed pin is board-provided and must be applied —",
        " * stubbed here, see the config sheet. */",
    ]
    for ctrl in sorted(s.controllers):
        out.append(f"&{ctrl} {{ status = \"okay\"; }};")
    out.append("")
    return out


def _sanitize(compat: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in compat)


def _collections(rig: Rig, s: Solved, types: dict[str, ConnectorType]) -> list[str]:
    """Aggregate collected entries (shield,collect) by their collection
    compatible into one node each -- the idiomatic gpio-keys/gpio-leds shape,
    where the compatible sits on the parent and each module is a child entry.
    (Merging into a board-provided collection of the same compatible: parked.)"""
    groups: dict[str, list[tuple[Instance, Device]]] = {}
    for inst in rig.instances:
        if not slots_of(s.sockets, inst):
            continue
        for dev in inst.shield.devices:
            if dev.collect is not None:
                groups.setdefault(dev.collect, []).append((inst, dev))
    if not groups:
        return []

    out = ["/ {"]
    for compat in sorted(groups):
        node = _sanitize(compat)
        out += [f"\t{node}: {node} {{", f'\t\tcompatible = "{compat}";']
        for inst, dev in sorted(groups[compat], key=lambda m: m[0].name):
            out += ["\t" + line for line in _collection_entry(s, types, inst, dev)]
        out.append("\t};")
    out += ["};", ""]
    return out


def _collection_entry(
    s: Solved, types: dict[str, ConnectorType], inst: Instance, dev: Device
) -> list[str]:
    """One child of a collection node: the module's function ref(s) (gpio,
    pwm, or adc). Node name and label are the composed <instance>_<shield
    label> -- unique per (instance, device), so an instance may contribute
    several entries (a shield with two LEDs), each keeping its own
    identity rather than collapsing into one."""
    lbl = f"{inst.name}_{dev.label}"
    lines = [f"\t{lbl}: {lbl} {{", f'\t\tlabel = "{lbl}";']
    # Carry through the device's passthrough properties -- a collected child
    # is still a real device node and its driver may require them (e.g. the
    # gpio-keys driver mandates zephyr,code). Same emission as _device_node;
    # aggregation only composes the label/gpio, it must not drop the rest.
    for _pname, rendered in _instance_extra_props(inst, dev):
        lines.append(f"\t\t{rendered}")
    for ref in dev.function_refs:
        lines.append(_render_ref(s, types, inst, dev, ref))
    lines.append("\t};")
    return lines


def _bus_devices(
    rig: Rig,
    s: Solved,
    kind: str,
    bus_path: str,
) -> Iterator[tuple[Instance, Device, BoardSocket]]:
    """Every (instance, device, socket) of `kind` ("i2c" or "spi") whose
    device sits on the physical bus `bus_path` identifies -- matched
    through the device's OWN qualified Device.bus name against its
    socket's buses dict, never a literal kind-as-name comparison (a named
    bus spells "spi-sensors", never bare "spi"). `kind` itself IS still
    needed despite bus_path being a real per-controller identity: the
    caller's own bus_label mixes i2c AND spi paths in one dict, so a
    kind-blind match would let an SPI device leak into the I2C-address-
    keyed rendering path whenever it walks a bus_path that happens to be
    this device's own (a real SPI bus, just not the one this call is
    rendering). A device whose own socket does not even offer the bus it
    names simply yields nothing (the loader/analyzer already rejected
    that shield, phys-subset)."""
    for inst in rig.instances:
        for dev in inst.shield.devices:
            if dev.bus is None or not is_bus_kind(dev.bus, kind):
                continue
            socket = for_bus_device(s.sockets, inst, dev)
            if socket is None:
                continue
            bus_ref = socket.buses.get(dev.bus)
            if bus_ref is None or bus_ref.path != bus_path:
                continue
            yield inst, dev, socket


def _ref_socket(s: Solved, inst: Instance, ref: FunctionRef) -> BoardSocket:
    """`ref`'s own resolved socket -- a cross-plug reference's slot may
    differ from its device's own bus slot, so every gpio/pwm/adc ref
    renderer resolves through THIS, never the device's bus socket. An
    accepted rig has every ref's slot resolved by construction; a None
    here would mean that guarantee broke, the same invariant
    `_device_node`'s own position assert already documents."""
    socket = for_ref(s.sockets, inst, ref)
    assert socket is not None
    return socket


def _render_ref(
    s: Solved, types: dict[str, ConnectorType], inst: Instance, dev: Device, ref: FunctionRef
) -> str:
    """One rendered property line for a single device reference (gpio, pwm,
    or adc) -- the per-ref half of a device node's body, shared by every
    caller that renders a device node's refs (`_device_node`, `_mux_node`'s
    nested devices, and `_collection_entry`) so the branch on `ref.function`
    is written exactly once: a collected entry and a plain device node can
    never render the same ref differently.

    `s`/`types`/`inst`/`dev`/`ref` are all read-only to this call; returns
    a single line, already prefixed at two tabs ("\\t\\t") to match a
    device node's own body indentation, that the caller owns."""
    socket = _ref_socket(s, inst, ref)
    ctype = types[socket.type_name]
    pos = s.positions.get((inst.name, dev.name, ref.prop), ref.position)
    # The analyzer resolves every ref's position (fixed or jumper-routed)
    # before an accepted rig ever reaches the emitter; None here would
    # mean that guarantee broke, not a rig-author mistake -- narrows the
    # type for posname() below rather than silently rendering "None".
    assert pos is not None
    if ref.function == "gpio":
        # Rewrite &plug (or the routing jumper) to the socket's nexus --
        # a real board node, or a synthesized carrier nexus. dtc chases
        # the (multi-level) gpio-map to the pin.
        # invert is a GPIO-only concept: it flips the active-level flag
        # bit a gpio ref alone carries. PWM_POLARITY is a different
        # property, authored by the shield in its own pwms= ref (a
        # 3-cell socket carries a real flags cell) -- coupling the two
        # would make one rig key mean two unrelated things depending on
        # the device's function. invert is never consulted for a pwm/adc
        # ref (adc has no flags cell at all), even on a collected entry
        # whose instance sets invert: true.
        flags = ref.flags ^ 0x1 if inst.invert else ref.flags
        return (
            f"\t\t{ref.prop} = <&{_nexus(socket)} {pos} {flags:#x}>;"
            f"\t/* {ctype.posname(pos)}{' inverted' if inst.invert else ''} */"
        )
    # pwm/adc: socket-relative, unified with the gpio idiom above -- dtc
    # chases the socket's real pwm-map/io-channel-map nexus to the
    # controller and channel; rigc does not resolve the channel
    # itself.
    res: ChannelResolution = s.channels[(inst.name, dev.name, ref.prop)]
    if ref.function == "pwm":
        # PWM cells: the SOCKET's own #pwm-cells decides the word count --
        # a real board socket's checked-read count or a carrier's
        # inherited one, never a hardcoded constant. A 2-cell socket
        # matches upstream atmel,sam0-tcc-pwm's flags-less convention
        # (channel, period); its pwm-map-pass-thru <0x0 0xffffffff>
        # carries exactly ONE cell through, so a 3rd cell here would not
        # be absorbed by the map at all -- dtlib would parse it as the
        # start of a BOGUS trailing phandle-array element (silently a
        # spurious null entry when it happens to be 0, a hard EDTError
        # otherwise). A 3-cell socket (the common upstream shape --
        # st,stm32-pwm, nxp,ftm-pwm) has a real THIRD cell for flags, and
        # its own pass-thru carries it exactly like period.
        assert socket.pwm_cells is not None
        if socket.pwm_cells == 2:
            if res.flags:  # not assert -- must survive python -O
                # Nonzero PWM flags on a 2-cell socket are rejected
                # upstream, by the analyzer (analyzer/gpio.py, category
                # phys-function, conditional on socket.pwm_cells == 2) --
                # a device with such a ref never earns a solved.channels
                # entry, so cli.py exits on diags.errors before
                # emitter.emit() is ever called (its "cannot fail"
                # contract would otherwise be violated by a raised
                # ValueError here). This documents the invariant rather
                # than re-deriving the diagnostic; tripping it means the
                # analyzer's guarantee broke, not that a rig author did
                # something wrong.
                raise AssertionError(
                    f"{inst.name}/{dev.name}: {ref.prop} reached the "
                    f"emitter with nonzero PWM flags {res.flags:#x} on a "
                    "2-cell socket — the analyzer should have rejected "
                    "this (phys-function) before emission"
                )
            return (
                f"\t\t{ref.prop} = <&{_nexus(socket)} {pos} {res.period}>;"
                f"\t/* {ctype.posname(pos)} */"
            )
        # socket.pwm_cells == 3 (the only other supported count,
        # board/project.py's _CHANNEL_FN) -- the shield's own plug always
        # declares #pwm-cells = <3> today (grove_servo, grove_pwm_led,
        # every corpus consumer), so ref.flags is always a real value
        # here, never a placeholder.
        return (
            f"\t\t{ref.prop} = <&{_nexus(socket)} {pos} {res.period} "
            f"{res.flags:#x}>;\t/* {ctype.posname(pos)} */"
        )
    # adc: #io-channel-cells is 1 (channel only) -- one cell, no flags, no
    # period; emitting the gpio-shaped two cells here would be a hard
    # EDTError against a 1-cell map, not merely a wrong value.
    return f"\t\t{ref.prop} = <&{_nexus(socket)} {pos}>;\t/* {ctype.posname(pos)} */"


def _mux_node(
    rig: Rig,
    s: Solved,
    types: dict[str, ConnectorType],
    inst: Instance,
    dev: Device,
    addr: int,
    channels: list[tuple[int, str]],
) -> list[str]:
    """A scope-creating interposer device (an I2C mux): the device node on
    the parent bus, with one child channel bus per scope, each hosting that
    scope's modules. Per-scope address uniqueness means 0x48 can recur
    across channels."""
    label = f"{inst.name}_{dev.label}"
    lines = [f"\t{label}: {dev.name}@{addr:x} {{"]
    for _pname, rendered in _instance_extra_props(inst, dev):  # compatible, ...
        lines.append(f"\t\t{rendered}")
    lines += [f"\t\treg = <{addr:#04x}>;", "\t\t#address-cells = <1>;", "\t\t#size-cells = <0>;"]
    for channel, scope_path in sorted(channels):
        lines += [
            f"\t\tchannel@{channel} {{",
            f"\t\t\treg = <{channel}>;",
            "\t\t\t#address-cells = <1>;",
            "\t\t\t#size-cells = <0>;",
        ]
        members = sorted(
            _bus_devices(rig, s, "i2c", scope_path), key=lambda m: s.addr[(m[0].name, m[1].name)]
        )
        for si, sd, _ss in members:
            sa = s.addr[(si.name, sd.name)]
            lines += [
                "\t\t" + ln
                for ln in _device_node(s, types, si, sd, unit=f"{sa:x}", reg=f"<{sa:#04x}>")
            ]
        lines.append("\t\t};")
    lines.append("\t};")
    return lines


def _device_node(
    s: Solved,
    types: dict[str, ConnectorType],
    inst: Instance,
    dev: Device,
    unit: str | None = None,
    reg: str | None = None,
) -> list[str]:
    label = f"{inst.name}_{dev.label}"
    name = f"{dev.name}@{unit}" if unit is not None else dev.name
    lines = [f"\t{label}: {name} {{"]
    for _pname, rendered in _instance_extra_props(inst, dev):
        lines.append(f"\t\t{rendered}")
    if reg is not None:
        lines.append(f"\t\treg = {reg};")
    for ref in dev.function_refs:
        # PER-REFERENCE resolution: a cross-plug ref's own slot may
        # differ from this device's own bus slot, so each ref looks up
        # ITS OWN socket rather than sharing one across the whole device
        # -- handled inside _render_ref, shared verbatim with
        # _collection_entry so the gpio/pwm/adc branch is written exactly
        # once.
        lines.append(_render_ref(s, types, inst, dev, ref))
    # Every device the analyzer accepted is, by definition, installed
    # hardware -- match the legacy shield convention of an explicit
    # status = "okay" on each instantiated device (not just its parent bus,
    # which the board DT already enables unconditionally).
    lines.append('\t\tstatus = "okay";')
    # An SD card on SPI needs its zephyr,sdmmc-disk child node (the legacy
    # adafruit_data_logger.overlay nests this under every sdhc-spi-slot
    # device) -- fixed, generic shape, no rig-specific data, so rigc
    # is the natural place to author it rather than duplicating
    # it in every shield that carries an SD slot.
    if dev.compatible == "zephyr,sdhc-spi-slot":
        lines += [
            "\t\tsdmmc {",
            '\t\t\tcompatible = "zephyr,sdmmc-disk";',
            '\t\t\tdisk-name = "SD";',
            '\t\t\tstatus = "okay";',
            "\t\t};",
        ]
    lines.append("\t};")
    return lines


def _synth_nexus_nodes(s: Solved) -> list[str]:
    """Emit a gpio-nexus node for each carrier-exported socket in use,
    chaining to its parent's nexus. Matches hand-written nested overlays:
    a click's <&carrier_nexus pos> resolves through the carrier to the
    host board pin, keeping the routing visible in the artifact."""
    synth: dict[str, BoardSocket] = {}

    def visit(sock: BoardSocket | None) -> None:
        # skip board sockets (no rows of ANY kind -- nexus_label is None)
        # and sockets with nothing to route at all. An analog-only exposed
        # socket (adc/pwm rows, no gpio -- e.g. a carrier's grove_a* with
        # no digital pass-through) must NOT be skipped here: checking
        # nexus_rows alone would drop it, since gpio is not the only kind
        # of row a nexus can carry.
        if (
            sock is None
            or not (sock.nexus_rows or sock.pwm_nexus_rows or sock.adc_nexus_rows)
            or sock.nexus_label in synth
        ):
            return
        assert sock.nexus_label is not None
        synth[sock.nexus_label] = sock
        for parent in sock.parents.values():  # a carrier stacked on carrier(s)
            visit(parent)

    for per_inst in s.sockets.values():
        for sock in per_inst.values():
            visit(sock)
    if not synth:
        return []

    out = ["/* carrier-exported sockets, synthesized as gpio-nexus nodes */", "/ {"]
    for label in sorted(synth):
        sock = synth[label]
        out += [f"\t{label}: {label} {{"]
        if sock.nexus_rows:
            rows = ",\n\t\t\t   ".join(
                f"<{child} 0 &{parent} {ppos} 0>" for child, parent, ppos in sock.nexus_rows
            )
            out += [
                "\t\t#gpio-cells = <2>;",
                # Match on the position cell only; mask the GPIO flag bits
                # out of matching and pass them through to the parent --
                # the same nexus idiom the board's own typed socket uses.
                # Without this edtlib demands an exact specifier match, so
                # a consumer's <&nexus pos GPIO_ACTIVE_LOW> would fail
                # against the stored <pos 0> row.
                "\t\tgpio-map-mask = <0xffffffff 0xffffffc0>;",
                "\t\tgpio-map-pass-thru = <0 0x3f>;",
                f"\t\tgpio-map = {rows};",
            ]
        if sock.pwm_nexus_rows:
            assert sock.pwm_cells is not None
            out += _channel_nexus_block("pwm", "pwm-map", sock.pwm_cells, sock.pwm_nexus_rows)
        if sock.adc_nexus_rows:
            assert sock.adc_cells is not None
            out += _channel_nexus_block(
                "io-channel", "io-channel-map", sock.adc_cells, sock.adc_nexus_rows
            )
        out.append("\t};")
    out += ["};", ""]
    return out


def _channel_nexus_block(
    cells_prop_base: str, map_prop: str, cells: int, rows: list[tuple[int, str, int]]
) -> list[str]:
    """The pwm-map / io-channel-map lines of a synthesized nexus node: the
    same mask/pass-thru idiom `boards/extend/seeed/seeeduino_lotus/
    grove_sockets.dtsi` authors by hand on a real board socket, generated
    here for a synthesized carrier one. Cell 0 (position) is always
    matched in full; every cell after it (pwm's own period cell; none
    for adc's single-cell form) is passed through UNTOUCHED to the
    parent -- it belongs to whatever the consuming shield's own ref
    supplies, chased through by dtc, not decided by rigc.
    `cells` is the PARENT's own declared count (a carrier inherits it,
    never chooses its own), so the node this function renders always
    presents the SAME cell count its own parent does, chaining correctly
    however many carriers deep the composition goes."""
    mask = " ".join(["0xffffffff"] + ["0x00000000"] * (cells - 1))
    pass_thru = " ".join(["0x00000000"] + ["0xffffffff"] * (cells - 1))
    row_words = " ".join(["0"] * (cells - 1))
    map_rows = ",\n\t\t\t   ".join(
        f"<{child}{(' ' + row_words) if row_words else ''} &{parent} {ppos}"
        f"{(' ' + row_words) if row_words else ''}>"
        for child, parent, ppos in rows
    )
    return [
        f"\t\t#{cells_prop_base}-cells = <{cells}>;",
        f"\t\t{map_prop}-mask = <{mask}>;",
        f"\t\t{map_prop}-pass-thru = <{pass_thru}>;",
        f"\t\t{map_prop} = {map_rows};",
    ]
