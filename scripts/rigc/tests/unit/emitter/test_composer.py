# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit: emitter (the package's own `__init__.py`) -- `emit()`'s artifact
SET as a function of input, and the ONE writer. This module's subject is
the ASSEMBLY, not any one artifact's content (those are covered where
they are named: test_overlay.py, test_sheet.py, test_expectations.py,
test_context.py).

`_needed_param_includes` (private) is tested directly here, the same
precedent test_loader.py already sets for `_build_topology` -- it is
PURE (no cpp), so poking it directly keeps these tests hermetic while
still pinning the derivation `emit()`'s own rig-gen-includes.dtsi
decision rests on; going through `emit()` itself would also render
config-sheet.md, which for a symbolic param value reaches cpp
(dtsio.resolve_token) -- exactly what this module's other tests avoid.
"""

from __future__ import annotations

from pathlib import Path

from rigc.analyzer import Solved
from rigc.emitter import GEN, _needed_param_includes, _render_includes_dtsi, emit, write_artifacts
from rigc.model import BoardSocket, ConnectorType, Device, Instance, Rig, Shield


def _device_declaring(header_list: list) -> Device:
    return Device(
        name="d",
        label="d",
        compatible=None,
        bus=None,
        group=None,
        reg=None,
        addr_from=None,
        cs_position=None,
        declared_params=["zephyr,code"],
        declared_param_includes=list(header_list),
    )


def test_needed_param_includes_is_empty_when_every_assigned_value_is_a_literal() -> None:
    dev = _device_declaring(["dt-bindings/input/input-event-codes.h"])
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
    inst = Instance(
        name="i1", shield=shield, sockets={"plug": "sock"}, params={"d": {"zephyr,code": "5"}}
    )
    rig = Rig(name="r", board="b", instances=[inst])

    assert _needed_param_includes(rig) == []


def test_needed_param_includes_collects_headers_for_a_symbolic_value() -> None:
    dev = _device_declaring(["dt-bindings/input/input-event-codes.h"])
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
    inst = Instance(
        name="i1",
        shield=shield,
        sockets={"plug": "sock"},
        params={"d": {"zephyr,code": "INPUT_KEY_0"}},
    )
    rig = Rig(name="r", board="b", instances=[inst])

    assert _needed_param_includes(rig) == ["dt-bindings/input/input-event-codes.h"]


def test_needed_param_includes_keeps_the_devices_own_declaration_order() -> None:
    """The PRODUCER side of the ordered-header contract. A device's own
    shield,param-includes order is the shield author's, and cpp include
    order can matter, so this derivation must not sort or otherwise
    reorder. Three headers whose declared order differs from BOTH
    ascending and descending sort order, so any reordering this function
    might introduce changes the result -- two names alone are not enough:
    a pair can coincide with one sort direction and make the assertion
    vacuous."""
    dev = _device_declaring(["mmm/mid.h", "aaa/first.h", "zzz/last.h"])
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
    inst = Instance(
        name="i1",
        shield=shield,
        sockets={"plug": "sock"},
        params={"d": {"zephyr,code": "INPUT_KEY_0"}},
    )
    rig = Rig(name="r", board="b", instances=[inst])

    assert _needed_param_includes(rig) == ["mmm/mid.h", "aaa/first.h", "zzz/last.h"]


def test_render_includes_dtsi_preserves_declaration_order() -> None:
    """The RENDERER side of the ordered-header contract
    (test_needed_param_includes_keeps_the_devices_own_declaration_order
    above pins the PRODUCER side): decoded text lists the given headers in
    the exact order handed in -- neither ascending nor descending sort
    order, so any reordering this function might introduce changes the
    result. Pure (no cpp), so this is unit-tested directly rather than
    only observed through emit()."""
    text = _render_includes_dtsi(["mmm/mid.h", "aaa/first.h", "zzz/last.h"])
    assert text == (
        f"/* {GEN} */\n\n#include <mmm/mid.h>\n#include <aaa/first.h>\n#include <zzz/last.h>\n"
    )


def test_rig_gen_includes_dtsi_is_absent_when_every_param_value_is_a_literal() -> None:
    """emit()-level companion to test_needed_param_includes_is_empty_when_
    every_assigned_value_is_a_literal above: a literal param value never
    reaches cpp at all (workdir is a path that does not exist, so a
    cpp/build attempt would fail loudly), and the artifact this device's
    own declared_param_includes would otherwise justify simply does not
    appear."""
    dev = _device_declaring(["dt-bindings/input/input-event-codes.h"])
    shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
    inst = Instance(
        name="i1", shield=shield, sockets={"plug": "sock"}, params={"d": {"zephyr,code": "5"}}
    )
    rig = Rig(name="r", board="b", instances=[inst])

    out = emit(rig, Solved(), {}, workdir="/does-not-matter")

    assert "rig-gen-includes.dtsi" not in out


def test_rig_gen_conf_is_never_emitted() -> None:
    rig = Rig(name="r", board="b", instances=[])
    out = emit(rig, Solved(), {}, workdir="/does-not-matter")
    assert "rig-gen.conf" not in out


def test_expectations_yml_is_always_emitted() -> None:
    rig = Rig(name="r", board="b", instances=[])
    out = emit(rig, Solved(), {}, workdir="/does-not-matter")
    assert "expectations.yml" in out


def test_every_artifact_is_utf8_encoded_bytes() -> None:
    """config-sheet.md's own banner carries an em dash -- a real
    multi-byte UTF-8 decision, not a formality. Every emitted artifact is
    exactly a {filename: bytes} pair, never str."""
    rig = Rig(name="r", board="b", instances=[])
    out = emit(rig, Solved(), {}, workdir="/does-not-matter")

    for name, content in out.items():
        assert isinstance(content, bytes), name
    assert "—".encode() in out["config-sheet.md"]


def test_emit_is_deterministic_under_a_shuffled_instance_order() -> None:
    ctype = ConnectorType(
        name="t", positions={}, index2name={}, bus_proxies=[], stackable=False, cs_pool={}
    )

    def make(order: list[str]) -> dict:
        insts = []
        sockets = {}
        for name in order:
            dev = Device(
                name="d",
                label="d",
                compatible=None,
                bus=None,
                group=None,
                reg=None,
                addr_from=None,
                cs_position=None,
            )
            shield = Shield(name="sh", label="sh", plugs={"plug": "t"}, devices=[dev])
            insts.append(Instance(name=name, shield=shield, sockets={"plug": "sock"}))
            sockets[name] = {
                "plug": BoardSocket(label="sock", path="/s", type_name="t", gpio_map={}, buses={})
            }
        rig = Rig(name="r", board="b", instances=insts)
        s = Solved(sockets=sockets)
        return emit(rig, s, {"t": ctype}, workdir="/does-not-matter")

    assert make(["alpha", "bravo"]) == make(["bravo", "alpha"])


def test_write_artifacts_writes_every_entry_in_binary_mode(tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    write_artifacts(str(out_dir), {"a.txt": b"hello", "b.bin": b"\x00\x01\xff"})

    assert (out_dir / "a.txt").read_bytes() == b"hello"
    assert (out_dir / "b.bin").read_bytes() == b"\x00\x01\xff"


def test_write_artifacts_creates_out_dir_if_missing(tmp_path: Path) -> None:
    out_dir = tmp_path / "nested" / "out"
    write_artifacts(str(out_dir), {"f": b"x"})
    assert out_dir.is_dir()
    assert (out_dir / "f").read_bytes() == b"x"
