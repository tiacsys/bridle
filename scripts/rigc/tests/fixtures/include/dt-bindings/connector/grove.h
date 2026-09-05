/* Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 *
 * Grove position indices — THE single source of truth shared by: board
 * socket gpio-map/pwm-map/io-channel-map child pins, shield plug
 * references, binding docs. (Pattern: include/dt-bindings/connector/mikrobus.h;
 * no upstream dt-bindings header exists for Grove position indices either,
 * so btr-shields is the one true source for its own typed socket clones.
 * rigc reads this header directly, not a copy of its own.)
 *
 * A Grove connector is 4 pins: two signal + VCC + GND. The two signal pins
 * are the claimable positions (they double as SCL/SDA on an I2C Grove
 * socket, D(n)/D(n+1) on a digital one, or PWM/ADC on a dual-function one —
 * the dual-function copper is discovered at the board binding, not declared
 * here).
 */
#ifndef DT_BINDINGS_CONNECTOR_GROVE_H_
#define DT_BINDINGS_CONNECTOR_GROVE_H_

/* pin 1 (yellow) = SIG0, pin 2 (white) = SIG1, then VCC, GND */
#define GROVE_SIG0 0
#define GROVE_SIG1 1
#define GROVE_VCC  2
#define GROVE_GND  3

#endif
