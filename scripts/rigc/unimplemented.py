# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""The loud-refusal channel for functionality rigc does not have yet.

Such a path must fail DISTINCTLY: `rigc: not implemented: <what>` on
stderr and exit status 3 -- never exit 1 (the reject convention: "we
cannot do this yet" must never be mistakable for "your input is wrong"),
never a traceback, and never a silent accept. Exit 2 stays argparse's own
usage-error code, so the full exit vocabulary is 0 accept / 1 rejected
input / 2 usage error / 3 not implemented.

Nothing in the frozen corpus reaches it any more. What still does: an
unreadable, empty or non-mapping YAML document (loader/documents.py),
and cli.py's unreachable unknown-subcommand branch.

Raised anywhere inside the pipeline, caught ONCE in cli.main().
"""

from __future__ import annotations


class Unimplemented(Exception):
    """A path rigc has not implemented yet. `what` names the missing
    capability in one line; cli.main() renders it as
    `rigc: not implemented: <what>` and exits 3."""

    def __init__(self, what: str) -> None:
        self.what = what
        super().__init__(what)
