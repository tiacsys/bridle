/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef COLORWHEEL_POLAR_H_
#define COLORWHEEL_POLAR_H_

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/** Fixed point shift for pixel-centred coordinates, units of 1/8 pixel. */
#define COLORWHEEL_COORD_SHIFT 3U
/** One pixel step in the fixed point coordinates. */
#define COLORWHEEL_COORD_ONE   (1U << COLORWHEEL_COORD_SHIFT)

/**
 * @brief Four quadrant arctangent in degrees.
 *
 * Computes the angle of the vector (@p y, @p x) counter-clockwise from the
 * positive x axis, mapped into [0, 360). Integer only, cheap enough to
 * evaluate per pixel and per frame on a core without an FPU, and accurate
 * to within a single step of the color wheel.
 *
 * @param y Y coordinate of the vector, in any fixed point unit.
 * @param x X coordinate of the vector, in the same unit as @p y.
 * @return Angle in degrees, from 0 up to but not including 360.
 */
uint16_t polar_atan2_deg(int32_t y, int32_t x);

/**
 * @brief Integer square root via the bit by bit method.
 *
 * @param v Input value.
 * @return The largest integer @p r with @p r * @p r <= @p v.
 */
uint32_t polar_isqrt(uint32_t v);

#ifdef __cplusplus
}
#endif

#endif /* COLORWHEEL_POLAR_H_ */
