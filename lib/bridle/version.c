/*
 * Copyright (c) 2021 TiaC Systems
 * Copyright (c) 1997-2010, 2012-2014 Wind River Systems, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief Bridle Version API implementation.
 */

#include <zephyr/types.h>
#include "bridle/version.h" /* generated at compile time */

/** @cond INTERNAL_HIDDEN */

/**
 * @brief Return the Bridle version of the present build
 *
 * The Bridle version is a four-byte value, whose format is described in the
 * file "bridle_version.h".
 *
 * @return Bridle version
 */
uint32_t sys_bridle_version_get(void)
{
	return BRIDLEVERSION;
}

/** @endcond */
