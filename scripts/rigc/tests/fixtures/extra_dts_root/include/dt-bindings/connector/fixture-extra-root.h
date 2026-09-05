/* Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */
/*
 * Fixture connector-type index header for
 * test_cmake_alone_entry.py::test_cmake_alone_threads_connector_dir_per_dts_root.
 * Never read by that test directly -- it exists so registry.load_types can
 * fully resolve fixture-extra-root.yaml's own plug,positions (there are
 * none, so this header needs no real position #defines), the same way any
 * real connector type's header would be resolved, rather than leaving the
 * expand step to fail on a missing header for an otherwise-unused type.
 */
#ifndef DT_BINDINGS_CONNECTOR_FIXTURE_EXTRA_ROOT_H_
#define DT_BINDINGS_CONNECTOR_FIXTURE_EXTRA_ROOT_H_

#define FIXTURE_EXTRA_ROOT_ANCHOR 0

#endif
