# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""rigc's own test tree. Layers are DIRECTORIES, not markers:
tests/unit/ (subprocess-free, value-shaped contracts) and
tests/integration/ (rigc's end-to-end coverage, driven through the CLI
and cmake entry points). Package-shaped (__init__.py) so pytest and
mypy both derive unique, collision-free module names."""
