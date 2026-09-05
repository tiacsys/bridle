# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""The emitter: a Solved rig plus its Rig/ConnectorType inputs projected
into concrete artifacts, split by visibility:

  MCU-visible-static   -> .overlay        (joins the unchanged Zephyr build)
  human-realized       -> config sheet    (markdown)
  runtime-discoverable -> expectations    (YAML stub)

Pure rendering under a strong contract: never decides anything, never
fails on an analyzer-accepted rig. Deterministic: all output is sorted
by stable keys, independent of rig-file declaration order.

Split into `overlay.py` (nexus synthesis, I2C/SPI scopes, collections,
plain groups, controllers, the device-node renderer), `sheet.py`
(config-sheet.md, including the params table's token resolution),
`expectations.py`, and this module (composing `emit()` and the ONE
writer). `context.py` renders context.cmake as its own value function,
kept out of `emit()` so rig artifacts and build glue stay separate
concerns; cli.py calls it alongside, never inside, `emit()`.

**Artifacts are `{filename: bytes}`, explicit UTF-8**: `config-sheet.md`
carries non-ASCII punctuation (arrows, em dashes), so the encoding is a
real decision, not a formality. The sub-renderers return `str` (readable
in unit tests); this module is the one place that encodes them into the
bytes-valued mapping cli.py hands to `write()`.

**Reads `solved.wires`, never `rig.wires`**: the loader's `rig.wires`
carries the RAW `via <name>` route string; the analyzer's wire check
returns NEW Wire values with the route resolved to a connector-type
position INDEX, held only on `Solved.wires`. Every renderer below takes
`solved` and never reaches back through `rig.wires`.
"""

from __future__ import annotations

import logging
import os

from ..analyzer import Solved
from ..dtsio import is_int_literal
from ..model import ConnectorType, Rig
from .banner import GEN
from .expectations import render_expectations
from .overlay import render_overlay
from .sheet import render_sheet

log = logging.getLogger(__name__)

__all__ = ["emit", "write_artifacts"]


def emit(
    rig: Rig,
    solved: Solved,
    types: dict[str, ConnectorType],
    workdir: str,
    include_dirs: list[str] | None = None,
) -> dict[str, bytes]:
    """Compute the rig artifacts (never context.cmake -- that is
    `context.render`, a build-glue concern kept out of this function by
    design) as a `{filename: bytes}` mapping. `include_dirs` is the cpp
    -I search list threaded into the config sheet's own token resolution
    (`dtsio.resolve_token`, via `sheet._params_table`) -- the same list a
    caller threads as --include-dir everywhere else; None reproduces the
    ZEPHYR_INC/MODULE_INC-only search, unchanged.

    Returns a fresh mapping the caller owns; `rig`/`solved`/`types` are
    read-only. `rig-gen-includes.dtsi` appears if and only if `_needed_param_includes`
    is non-empty (the common corpus case gets no extra artifact and no
    include line, zero churn); `rig-gen.conf` never appears (no
    corpus/fixture rig produces per-instance Kconfig fragments yet);
    `expectations.yml` always appears, though nothing gates its content
    (test_emitted_corpus.py's own docstring)."""
    log.info("emit(): rig '%s'", rig.name)
    needed_includes = _needed_param_includes(rig)
    outputs = {
        "rig-gen.overlay": render_overlay(rig, solved, types, needed_includes).encode("utf-8"),
        "config-sheet.md": render_sheet(rig, solved, types, workdir, include_dirs).encode("utf-8"),
        "expectations.yml": render_expectations(rig, solved).encode("utf-8"),
    }
    if needed_includes:
        outputs["rig-gen-includes.dtsi"] = _render_includes_dtsi(needed_includes).encode("utf-8")
    for fname, content in outputs.items():
        log.debug("emit(): rendered %s (%d bytes)", fname, len(content))
    return outputs


def _needed_param_includes(rig: Rig) -> list[str]:
    """Every header this rig's own per-instance parameter assignments
    actually need cpp to see: the union, across every instance (sorted by
    name) and every device label it assigns params to (sorted), of the
    owning device's own `declared_param_includes` -- but only for a
    device that has at least one assigned property whose value is NOT a
    bare integer literal (`dtsio.is_int_literal`), mirroring
    `loader.params.apply_params_block`'s own short-circuit: a literal
    never needs a header at all, in ANY code path.

    This is the SOLVED-side answer to the same question
    `loader.params.check_param_token` independently answers on the LOADER
    side (which headers a device's own non-literal assignments need cpp
    to preprocess): the two coincide today only because the loader passes
    a device's WHOLE `declared_param_includes` list to `check_param_token`
    rather than some filtered subset of it. A change to either that stops
    doing that must update the other, or `rig-gen-includes.dtsi` and the
    set of headers the loader actually validated will silently diverge.

    Deduplicated but never REORDERED -- rig-gen-includes.dtsi's own
    #include order can matter to cpp (a later header may rely on a macro
    an earlier one defines), and `compare_includes_dtsi`'s own contract
    treats it as a list, never a set. Traversal is by SORTED instance
    name and device label, never rig-file declaration order, so the
    result is deterministic regardless of authoring order.

    rig is read-only; returns a fresh list the caller owns."""
    headers: list[str] = []
    for inst in sorted(rig.instances, key=lambda i: i.name):
        devices_by_label = {d.label: d for d in inst.shield.devices}
        for dev_label, props in sorted(inst.params.items()):
            dev = devices_by_label.get(dev_label)
            if dev is None or not any(not is_int_literal(v) for v in props.values()):
                continue
            for header in dev.declared_param_includes:
                if header not in headers:
                    headers.append(header)
    return headers


def _render_includes_dtsi(headers: list[str]) -> str:
    """The fourth generated artifact: nothing but the needed #include
    lines (`_needed_param_includes`). rig-gen.overlay pulls this in via a
    QUOTED include at the top of the file -- quoted-include resolution
    against the including file's own directory means both files can
    simply sit side-by-side in <build>/rig/ with no -I plumbing, no
    EXTRA_DTC_OVERLAY_FILE entry, no ordering constraint in cmake, and no
    build_info key: the dependency is visible in the file that has it."""
    out = [f"/* {GEN} */", ""]
    out += [f"#include <{header}>" for header in headers]
    out.append("")
    return "\n".join(out)


def write_artifacts(out_dir: str, artifacts: dict[str, bytes]) -> None:
    """The ONE shell that performs every artifact write, binary mode --
    the IO-at-the-edges boundary: every renderer above and
    `context.render` computes bytes as a pure value, and this is the
    only place any of them touch a filesystem. Creates out_dir if needed
    (a caller passing a fresh --out-dir is the common case, not an
    error).

    artifacts is read-only; writes each mapping entry as out_dir/<name>,
    returns nothing."""
    log.info("write_artifacts(): writing %d file(s) to %s", len(artifacts), out_dir)
    os.makedirs(out_dir, exist_ok=True)
    for fname, content in artifacts.items():
        path = os.path.join(out_dir, fname)
        with open(path, "wb") as f:
            f.write(content)
        log.info("write_artifacts(): wrote %s (%d bytes)", path, len(content))
