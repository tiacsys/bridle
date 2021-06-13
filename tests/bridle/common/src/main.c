/*
 * Copyright (c) 2021 TiaC Systems
 * Copyright (c) 2016 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */


#include <ztest.h>
#include <bridle_version.h>
#include "version.h"

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
static void test_version(void)
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

void test_main(void)
{
	ztest_test_suite(common,
			 ztest_unit_test(test_version)
			 );

	ztest_run_test_suite(common);
}
