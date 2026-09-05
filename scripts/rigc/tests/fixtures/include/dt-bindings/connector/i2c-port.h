/* Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */
/* Connector type "i2c-port": a bare downstream I2C port (an I2C-mux channel,
 * or any board I2C header). No claimable gpio positions — just the bus, so
 * no position #defines. Kept for the connector-type registry's uniform
 * parse_header_indices() call across all four types; this compatible is
 * shield-synthesized only and never appears in a real board devicetree
 * (see dts/bindings/connectors/i2c-port.yaml), so nothing outside rigc
 * ever needs to #include this file.
 */
#ifndef DT_BINDINGS_CONNECTOR_I2C_PORT_H_
#define DT_BINDINGS_CONNECTOR_I2C_PORT_H_
#endif
