# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""Unit-suite-local fixtures.

Every unit test observes the `rigc` logger tree at DEBUG through caplog,
regardless of RIGC_LOG/-v/-vv (which govern the REAL stderr handler
`_configure_logging` attaches, a separate concern -- see cli.py). Scoped
to tests/unit/ only: the frozen integration suite drives rigc as a
subprocess, where caplog cannot observe anything anyway.
"""

from __future__ import annotations

import logging

import pytest


@pytest.fixture(autouse=True)
def _debug_logging(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG, logger="rigc")
