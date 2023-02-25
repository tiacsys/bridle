/* bridle version support */

/*
 * Copyright (c) 2021-2023 TiaC Systems
 * Copyright (c) 2015 Wind River Systems, Inc.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef BRIDLE_INCLUDE_BRIDLE_VERSION_H_
#define BRIDLE_INCLUDE_BRIDLE_VERSION_H_

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @defgroup version_apis Version APIs
 * @ingroup bridle_apis
 * @{
 *
 * The bridle version has been converted from a string to a four-byte
 * quantity that is divided into two parts.
 *
 * Part 1: The three most significant bytes represent the bridle's
 * numeric version, x.y.z. These fields denote:
 *       x -- major release
 *       y -- minor release
 *       z -- patchlevel release
 * Each of these elements must therefore be in the range 0 to 255, inclusive.
 *
 * Part 2: The least significant byte is reserved for tweak mark use.
 */
#define SYS_BRIDLE_VER_MAJOR(ver) (((ver) >> 24) & 0xFF)
#define SYS_BRIDLE_VER_MINOR(ver) (((ver) >> 16) & 0xFF)
#define SYS_BRIDLE_VER_PATCHLEVEL(ver) (((ver) >> 8) & 0xFF)
#define SYS_BRIDLE_VERSION_TWEAK(ver) ((ver) & 0xFF)

/* bridle version routines */

/**
 * @brief Return the bridle version of the present build
 *
 * The bridle version is a four-byte value, whose format is described in the
 * file "bridle_version.h".
 *
 * @return bridle version
 */
extern uint32_t sys_bridle_version_get(void);

/**
 * @}
 */

#ifdef __cplusplus
}
#endif

#endif /* BRIDLE_INCLUDE_BRIDLE_VERSION_H_ */
