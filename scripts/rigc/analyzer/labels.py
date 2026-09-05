# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Emission feasibility of generated labels. Strong contract: the
emitter never fails, so the deterministic label scheme
`<instance>_<shield label>` must be collision-free HERE. Runs over every
declared instance regardless of whether its socket resolved: a label
collision is a property of two instance/device NAME pairs alone,
needing no board/socket information at all, so it is not one of the
passes skip-don't-abort applies to."""

from __future__ import annotations

from ..diag import Diagnostic, error
from ..model import Instance, Rig


def check_labels(rig: Rig) -> list[Diagnostic]:
    """Emission feasibility: composed output labels
    (<instance>_<shield-local-label>) must be unique across the rig.

    Returns the label findings (phys-label); rig is read-only."""
    diags: list[Diagnostic] = []
    seen: dict[str, Instance] = {}
    for inst in rig.instances:
        for dev in inst.shield.devices:
            label = f"{inst.name}_{dev.label}"
            if label in seen:
                diags.append(
                    error(
                        "phys-label",
                        f"generated label '{label}' collides (instances '{inst.name}' "
                        "twice in one rig?) — deterministic naming cannot "
                        "disambiguate",
                        (inst.src,) if inst.src else (),
                    )
                )
            seen[label] = inst
    return diags
