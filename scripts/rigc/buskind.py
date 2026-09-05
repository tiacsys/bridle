# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Bus-kind matching: whether a bus name (a `Device.bus` value, or a
shield group/proxy name authored in a `.shield` file) names a given
socket bus KIND -- bare ("spi"), or a named variant a multi-bus
connector type suffixes with a role ("spi-sensors"). One shared
implementation for every pass that gates behavior on which kind a
qualified bus name is, rather than each duplicating the same
kind-prefix match (or, worse, a literal three-name membership check
that silently stops covering a role-suffixed name).

Also the one home for the two `socket,*` PROPERTY-NAME regexes every
reader of a `socket,*` binding/node needs -- loader/shields.py (exposed-socket
parsing), board/project.py (board-side projection) and registry.py
(connector-type binding facts) each read the identical two patterns off
a different input (a dtlib node, an edtlib.EDT, a raw binding dict), so
the patterns themselves belong here rather than as separate verbatim
copies drifting apart one edit at a time."""

from __future__ import annotations

import re

#: Every socket bus kind the schema recognizes -- the vocabulary
#: `bus_kind_of` matches a qualified name against, in order.
BUS_KINDS = ("i2c", "spi", "uart")

#: socket,<kind> or socket,<kind>-<role> -- a connector type names an
#: additional bus of a kind by suffixing the kind with a role. Anchored
#: full-match so a "-cs-pool" property (matched separately below) never
#: also reads as a bus.
BUS_PROP_RE = re.compile(r"^socket,(i2c|spi|uart)(?:-\w+)?$")

#: socket,<kind>-<role>-cs-pool -- a named bus's own CS pool (default or
#: authored override), keyed the same qualified way. The legacy,
#: role-less "socket,cs-pool" (every real connector type's own spelling,
#: unchanged by this schema) is handled separately by each caller: it
#: carries no kind in its own name, so it is not this pattern's concern.
CS_POOL_PROP_RE = re.compile(r"^socket,((?:i2c|spi|uart)-\w+)-cs-pool$")


def is_bus_kind(bus: str | None, kind: str) -> bool:
    """Whether `bus` names `kind` -- bare, or `kind` suffixed with a role
    ("-sensors", "-motors", ...). `bus` may be absent (a device with no
    bus at all), which never matches any kind."""
    return bus is not None and (bus == kind or bus.startswith(f"{kind}-"))


def bus_kind_of(name: str | None) -> str | None:
    """Which of `BUS_KINDS` `name` names, bare or role-suffixed, else
    None -- the general form of `is_bus_kind` for a caller that must
    recognize ANY of the schema's kinds rather than one it already
    knows."""
    return next((k for k in BUS_KINDS if is_bus_kind(name, k)), None)
