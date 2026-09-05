# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Shared helpers for rigc's own tests.

Only the hermeticity enforcement lives here: assert_fixture_local, so any
test can prove at the point of use that the paths it hands to the code
under test never escape its own fixture tree. Golden/corpus plumbing
lives in tests/integration/conftest.py instead -- this file must never
grow a second copy of it.
"""

from __future__ import annotations

import os
from collections.abc import Iterable
from pathlib import Path

#: rigc's own fixture tree. A value derived from this file's location --
#: no environment lookup at module scope anywhere in this package, which
#: would otherwise fire at collection time before any test gets to set it.
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


def assert_fixture_local(paths: Iterable[Path | str], fixtures_dir: Path = FIXTURES_DIR) -> None:
    """Structural proof of hermeticity: every path a test hands to the
    code under test resolves under fixtures_dir -- never a real Zephyr
    tree, never repo-production devicetree content. Hermetic means "no
    foreign DATA", proven from what the test actually references, not
    from the absence of an environment variable. fixtures_dir is a
    parameter (default: rigc's own tree) so the enforcement itself is
    unit-testable against synthetic roots."""
    root = fixtures_dir.resolve()
    for p in paths:
        resolved = Path(p).resolve()
        assert resolved == root or str(resolved).startswith(str(root) + os.sep), (
            f"{resolved} is outside {root} -- a test asserting hermeticity "
            "must reference only its own fixture-tree paths"
        )
