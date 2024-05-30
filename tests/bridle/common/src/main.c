/*
 * Copyright (c) 2021-2023 TiaC Systems
 * Copyright (c) 2016 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */


#include <zephyr/ztest.h>
#include <bridle/core_version.h>
#include "bridle/version.h"

/**
 * @defgroup bridle_common_tests Common Tests
 * @ingroup all_tests
 * @{
 * @}
 *
 */

/**
 * @brief Test sys_bridle_version_get() functionality
 *
 * @ingroup bridle_common_tests
 *
 * @see sys_bridle_version_get()
 */
ZTEST(common, test_version)
{
	uint32_t version = sys_bridle_version_get();

	zassert_true(version == BRIDLEVERSION, "version mismatch");

	zassert_true(SYS_BRIDLE_VER_MAJOR(version) == BRIDLE_VERSION_MAJOR,
		     "major version mismatch");
	zassert_true(SYS_BRIDLE_VER_MINOR(version) == BRIDLE_VERSION_MINOR,
		     "minor version mismatch");
	zassert_true(SYS_BRIDLE_VER_PATCHLEVEL(version) == BRIDLE_PATCHLEVEL,
		     "patchlevel version match");

}

ZTEST_SUITE(common, NULL, NULL, NULL, NULL, NULL);
