/* Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */
/* Position indices for this fixture tree's own synthetic connector type
 * (socket,fixture-nexus). Not a copy of any real connector header under
 * include/dt-bindings/connector -- no real board or shield ever references
 * these names, so there is nothing for this numbering to stay consistent
 * with beyond this fixture tree itself.
 *
 * FIXTURE_POS0/FIXTURE_POS1 are consumed directly by
 * fixtures/boards/fixture_board.dts, which claims raw gpio-map/pwm-map
 * indices and never goes through the connector-type registry at all.
 * FIXTURE_D0/FIXTURE_D1/FIXTURE_CS are the registry-complete type's own
 * claimable positions (fixture-nexus.yaml's plug,positions), consumed by
 * fixtures/reference-shields. The common prefix ctypes_registry.py strips
 * to derive a position's short name is computed over EVERY define in this
 * file at once, so the two groups coexist: "FIXTURE_" is the shared prefix,
 * leaving "POS0"/"POS1" (unclaimable -- absent from plug,positions, so
 * shields.py rejects any attempt to claim them) alongside "D0"/"D1"/"CS"
 * (the claimable set).
 */
#ifndef DT_BINDINGS_CONNECTOR_FIXTURE_NEXUS_H_
#define DT_BINDINGS_CONNECTOR_FIXTURE_NEXUS_H_

#define FIXTURE_POS0 0
#define FIXTURE_POS1 1
#define FIXTURE_D0   2
#define FIXTURE_D1   3
#define FIXTURE_CS   4

#endif
