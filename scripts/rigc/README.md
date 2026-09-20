# rigc — the rig transpiler

A **rig** is a named topology: one board, plus the shields plugged into
its typed sockets, plus how they are configured. `rigc` compiles that
description into the devicetree overlay a Zephyr build consumes, and
refuses the ones that cannot physically work — a shield that needs SPI on
a socket exposing none, two devices claiming one chip-select, a required
parameter left unassigned.

**Full documentation lives at `doc/bridle/rigs4zephyr/`** — tutorials,
how-to guides, reference pages (commands, the board-socket and
shield-template vocabulary, diagnostics, the API) and the design
rationale, built as part of bridle's own Sphinx docs. This file is a
pointer plus what a reader browsing this directory on GitHub, with no
docs build in hand, needs to run the gate.

It is wired into the build: a rig is `-DRIG=<name>` on an ordinary `west
build` or bare `cmake` invocation (`doc/bridle/rigs4zephyr/reference/
commands.rst`), and `west rigs` lists, explains and censuses rigs without
building. Standalone operation (`python3 -m rigc expand ...`) still works
and is what the test suite drives directly, but it is the seam for
tooling, not the way to build a rig by hand.

## Running the tests

```console
$ ZEPHYR_BASE=<your zephyr tree> scripts/rigc/check.sh
```

mypy over the package, the unit suite under a coverage floor, then the
integration suite driving the real CLI as a subprocess (including the
documentation drift guards under `tests/integration/`, which fail the
gate if a reference page and the real code or docs tree disagree).
`CHECK_FAST=1` deselects tests marked `build`; this suite carries none
yet.

The suite is hermetic: it reads only the vendored fixtures under
`tests/fixtures/` and threads them explicitly on every call.
`tests/integration/harness.py`'s `assert_fixture_local` is the structural
proof of that, applied per test.

## Layout

| path | |
|---|---|
| `loader/` | rig files and shield templates in, a topology out |
| `board/` | reads the board's real devicetree (edtlib) for its sockets |
| `analyzer/` | resolves it against the board: sockets, addresses, chip-selects, GPIO nets, wires |
| `emitter/` | renders the artifacts; decides nothing |
| `cli.py` | the argv surface; `python -m rigc expand` |
| `tests/` | `unit/` in-process, `integration/` through the CLI front door |
| `check.sh` | the gate |
