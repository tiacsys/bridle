# unified-connectors

Byte-identical copies of the four production connector-type bindings under
`dts/bindings/connectors/` (`arduino-r3.yaml`, `grove.yaml`, `i2c-port.yaml`,
`mikrobus.yaml`), used by `test_connector_bindings.py`
(`scripts/rigc/tests/integration/`).

## Why a copy exists at all

`scripts/rigc/tests/integration/` is the half of this suite that migrates
out to bridle along with the transpiler (`scripts/rigc/`) and `doc/`; the
connector vocabulary under `dts/bindings/connectors/` stays behind with the
rest of the hardware definitions (`boards/rigs/`, `boards/shields/`,
`boards/extend/`) — that migration boundary is not up for revisiting here.
`test_connector_bindings.py` validates that vocabulary (it is the only test
that ever edtlib-loads these four files at all — see that module's own
docstring for why nothing else would notice a schema break), so for it to
travel with the transpiler it needs its own copy to validate instead of
reaching back across the boundary into content that will no longer be in
the same repository.

## Keeping this copy honest

Nothing here should ever earn a deliberate edit of its own: these files
carry NO provenance comments (unlike some other fixture directories under
`tests/fixtures/dts/`) precisely so they stay byte-comparable against
production without a diff-suppression rule. The provenance note lives here,
in this README, instead.

`scripts/rigc/tests/integration_stay/test_vendored_connector_drift.py`
holds the drift guard: it asserts every file here (and the matching header
in `tests/fixtures/include/dt-bindings/connector/`) is still byte-identical
to its production original, and that the two sets have the same four-name
membership — so adding a fifth connector type to `dts/bindings/connectors/`
without vendoring it here fails loudly instead of leaving
`test_connector_bindings.py` silently validating three-quarters of the
vocabulary. Run that guard (and refresh these copies from production)
whenever it reds.

This is a DIFFERENT arrangement from
`tests/fixtures/dts/singleton-law-connectors/`, an older fixture copy of
these same four types that has since drifted from production on three of
four (see that directory's own comments) and carries no drift guard at
all — it predates this mechanism and is out of scope for it; see
`test_singleton_identity_law.py`'s own comments for that copy's actual,
current state.
