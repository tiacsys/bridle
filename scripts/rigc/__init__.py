# Copyright (c) 2026 TiaC Systems
# SPDX-License-Identifier: Apache-2.0
"""rigc -- the rig compiler: reads a rig's metadata and shield library,
reads the board's real devicetree, decides whether the assembly is
physically possible, and emits the devicetree overlay plus build glue.

Five stages, in order: the CLI front door (cli.py) sequences the run;
the loader (loader/, registry.py) reads the rig files and the shield
library into the rig model (model.py); the board reader (board/) reads
the board's real devicetree; the analyzer (analyzer/) decides whether
the assembly is physically possible; the emitter (emitter/) renders the
overlay, the config sheet, the expectations and the build glue. diag.py
is the diagnostics core all five report through.

`unimplemented.py`'s loud refusal (`rigc: not implemented: <what>`, exit
3) is the channel for a path this tool does not handle -- see that
module's own docstring for what still reaches it.

**Logging**: every module gets its own `logging.getLogger(__name__)`;
this package's ROOT logger gets a `NullHandler` here, the library
convention -- without it, an unconfigured logging tree falls through to
Python's own `lastResort` handler, which would print any WARNING-or-
louder record straight to stderr and corrupt a golden comparison.
`cli.main()` is the ONE place that ever attaches a REAL handler, and
only when asked to: `-v`/`-vv` on the command line (INFO/DEBUG) or,
absent either flag, the environment naming a level (`RIGC_LOG=<level>`)
-- see `_configure_logging`'s own docstring for the stderr-purity
tradeoff either knob makes deliberately."""

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
