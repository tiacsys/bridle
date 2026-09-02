# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""`python -m rigc ...` entry point -- delegates to cli.main(). The exit
vocabulary is cli.py's: 0 accept, 1 rejected input, 2 usage error,
3 not implemented."""

from __future__ import annotations

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
