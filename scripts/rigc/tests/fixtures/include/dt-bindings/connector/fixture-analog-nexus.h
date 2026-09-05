/* Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */
/* Position indices for the carrier PWM/ADC pass-through feature's own
 * synthetic connector type (socket,fixture-analog-nexus,
 * carrier-analog-passthrough-brief.md Sec 6). Not a copy of any real
 * connector header under include/dt-bindings/connector -- no real board
 * or shield ever references these names. Every fixture in this tree
 * claims raw literal indices directly (0/1) rather than these macros, so
 * this header exists only because ctypes_registry.load_types
 * unconditionally opens dt-bindings/connector/<type>.h for every
 * registered type -- the same reason fixture-mp-spi.h exists with no
 * claimable positions at all.
 *
 * FIXTURE_ANALOG_UNUSED is a deliberately unclaimable third define
 * (absent from fixture-analog-nexus.yaml's own plug,positions) that
 * exists ONLY to bound dtsio.py's own common-prefix computation
 * (parse_header_indices: os.path.commonprefix) at "FIXTURE_ANALOG_" --
 * with just SIG0/SIG1 present, the two names' own shared prefix runs
 * all the way to "FIXTURE_ANALOG_SIG", stripping to "0"/"1" instead of
 * "SIG0"/"SIG1". fixture-nexus.h's own POS0/POS1-alongside-D0/D1/CS
 * split is the identical idiom, applied here at the smallest scale that
 * still needs it.
 */
#ifndef DT_BINDINGS_CONNECTOR_FIXTURE_ANALOG_NEXUS_H_
#define DT_BINDINGS_CONNECTOR_FIXTURE_ANALOG_NEXUS_H_

#define FIXTURE_ANALOG_SIG0   0
#define FIXTURE_ANALOG_SIG1   1
#define FIXTURE_ANALOG_UNUSED 99

#endif
