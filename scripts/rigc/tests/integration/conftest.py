# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""pytest wants a conftest.py in this directory; the actual plumbing lives
in harness.py (generic, importable from tests/integration_stay/ too) and,
for the corpus-tethered half, in tests/integration_stay/corpus.py. No test
module in this directory should import from this file any more -- import
from harness directly (`from harness import ...`). This file exists purely
so the pytest rootdir/conftest mechanism has something to find here; it is
NOT the shared import surface (see harness.py's own docstring for why: two
sibling conftest.py files under a common sys.path, with no __init__.py
anywhere, would otherwise cross-wire under Python's plain `from conftest
import ...` idiom, since sys.modules["conftest"] is first-wins)."""

from __future__ import annotations

from harness import *  # noqa: F401,F403
