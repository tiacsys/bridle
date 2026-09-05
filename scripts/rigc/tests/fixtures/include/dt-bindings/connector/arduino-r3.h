/* Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */
/* Arduino Uno (R3) position indices, as consumed by shield `.shield`
 * templates (`#include <dt-bindings/connector/arduino-r3.h>`) and by
 * `rigc.registry` (the same header, single source of truth for
 * both consumers).
 *
 * The real board socket node (e.g.
 * boards/extend/st/nucleo_f401re/arduino_r3_socket.dtsi) instead includes
 * upstream's own <zephyr/dt-bindings/gpio/arduino-header-r3.h> directly —
 * values are IDENTICAL (checked at promotion time), so this is not a second
 * source of truth for the *values*, just the path shields and rigc
 * already depend on.
 */
#ifndef DT_BINDINGS_CONNECTOR_ARDUINO_R3_H_
#define DT_BINDINGS_CONNECTOR_ARDUINO_R3_H_

#define ARDUINO_HEADER_R3_A0  0
#define ARDUINO_HEADER_R3_A1  1
#define ARDUINO_HEADER_R3_A2  2
#define ARDUINO_HEADER_R3_A3  3
#define ARDUINO_HEADER_R3_A4  4
#define ARDUINO_HEADER_R3_A5  5
#define ARDUINO_HEADER_R3_D0  6
#define ARDUINO_HEADER_R3_D1  7
#define ARDUINO_HEADER_R3_D2  8
#define ARDUINO_HEADER_R3_D3  9
#define ARDUINO_HEADER_R3_D4  10
#define ARDUINO_HEADER_R3_D5  11
#define ARDUINO_HEADER_R3_D6  12
#define ARDUINO_HEADER_R3_D7  13
#define ARDUINO_HEADER_R3_D8  14
#define ARDUINO_HEADER_R3_D9  15
#define ARDUINO_HEADER_R3_D10 16
#define ARDUINO_HEADER_R3_D11 17
#define ARDUINO_HEADER_R3_D12 18
#define ARDUINO_HEADER_R3_D13 19
#define ARDUINO_HEADER_R3_D14 20
#define ARDUINO_HEADER_R3_D15 21

#endif
