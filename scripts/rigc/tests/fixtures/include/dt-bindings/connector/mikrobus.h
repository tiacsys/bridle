/* Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */
/* mikroBUS position indices — THE single source of truth shared by:
 * board socket gpio-map child pins, shield plug references, binding docs.
 * (Pattern: upstream include/zephyr/dt-bindings/gpio/arduino-header-r3.h;
 * no equivalent upstream header exists for mikroBUS, so btr-shields is the
 * one true source for its own typed socket clones.)
 */
#ifndef DT_BINDINGS_CONNECTOR_MIKROBUS_H_
#define DT_BINDINGS_CONNECTOR_MIKROBUS_H_

#define MIKROBUS_AN   0
#define MIKROBUS_RST  1
#define MIKROBUS_CS   2
#define MIKROBUS_SCK  3
#define MIKROBUS_MISO 4
#define MIKROBUS_MOSI 5
#define MIKROBUS_PWM  6
#define MIKROBUS_INT  7
#define MIKROBUS_RX   8
#define MIKROBUS_TX   9
#define MIKROBUS_SCL  10
#define MIKROBUS_SDA  11

#endif
