/* Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */
/* Position indices for the 3-cell PWM feature's own synthetic connector
 * type (socket,three-cell-pwm-nexus, three-cell-pwm-brief.md Sec 5/6).
 * Not a copy of any real connector header under
 * include/dt-bindings/connector -- no real board or shield ever
 * references these names. Every fixture in this tree claims raw literal
 * indices directly (0/1) rather than these macros, so this header
 * exists only because ctypes_registry.load_types unconditionally opens
 * dt-bindings/connector/<type>.h for every registered type -- the same
 * reason fixture-analog-nexus.h exists.
 *
 * THREE_CELL_PWM_UNUSED is a deliberately unclaimable third define
 * (absent from three-cell-pwm-nexus.yaml's own plug,positions) that
 * exists ONLY to bound dtsio.py's own common-prefix computation
 * (parse_header_indices: os.path.commonprefix) at "THREE_CELL_PWM_" --
 * with just SIG0/SIG1 present, the two names' own shared prefix runs
 * all the way to "THREE_CELL_PWM_SIG", stripping to "0"/"1" instead of
 * "SIG0"/"SIG1". fixture-analog-nexus.h's identical idiom is the direct
 * precedent.
 */
#ifndef DT_BINDINGS_CONNECTOR_THREE_CELL_PWM_NEXUS_H_
#define DT_BINDINGS_CONNECTOR_THREE_CELL_PWM_NEXUS_H_

#define THREE_CELL_PWM_SIG0   0
#define THREE_CELL_PWM_SIG1   1
#define THREE_CELL_PWM_UNUSED 99

#endif
