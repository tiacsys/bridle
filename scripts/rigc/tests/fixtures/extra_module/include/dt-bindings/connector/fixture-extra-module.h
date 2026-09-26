/* Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */
/*
 * Index header for the extra_module fixture's own connector type. It
 * declares no positions; it exists because the registry opens
 * dt-bindings/connector/<type>.h for every type, and it lives only in this
 * fixture module's include/ -- so resolving it proves that include root was
 * threaded.
 */
#ifndef DT_BINDINGS_CONNECTOR_FIXTURE_EXTRA_MODULE_H_
#define DT_BINDINGS_CONNECTOR_FIXTURE_EXTRA_MODULE_H_

#define FIXTURE_EXTRA_MODULE_ANCHOR 0

#endif
