/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "polar.h"

/*
 * First octant arctangent, shared by both branches of polar_atan2_deg.
 *
 * Approximates atan(r) for a ratio @p r already scaled into [0, 1024] and
 * returns the angle in 1/1024 of a degree, using the rational form
 *
 *   atan(r) ~= r * (45 + 15.65 * (1 - r))        (degrees, 0 <= r <= 1)
 *
 * with a worst case error of 0.21 degrees. The coefficient is carried as
 * 15.65 * 1024 = 16026 to keep the evaluation in 32 bit integer
 * arithmetic, cheap enough for a per pixel inner loop without an FPU. The
 * error is far below the angular resolution of a discrete matrix, where
 * one pixel step near the centre spans several degrees.
 */
#define ATAN_K0 (45 * 1024)
#define ATAN_K1 16026

static int32_t atan_first_octant(int32_t r)
{
	return (r * (ATAN_K0 + ATAN_K1 - ((ATAN_K1 * r) >> 10))) >> 10;
}

uint16_t polar_atan2_deg(int32_t y, int32_t x)
{
	const int32_t ax = (x >= 0) ? x : -x;
	const int32_t ay = (y >= 0) ? y : -y;
	int32_t angle;

	if ((ax == 0) && (ay == 0)) {
		return 0U;
	}

	/* Fold the vector into the first octant, evaluate the arctangent of
	 * the slope, then re-apply the signs to unfold the reflections
	 * into the correct quadrant.
	 */
	if (ax >= ay) {
		angle = atan_first_octant((ay << 10) / ax) >> 10;
	} else {
		angle = 90 - (atan_first_octant((ax << 10) / ay) >> 10);
	}

	if (y < 0) {
		angle = -angle;
	}
	if (x < 0) {
		angle = 180 - angle;
	}

	return (uint16_t)(((angle % 360) + 360) % 360);
}

uint32_t polar_isqrt(uint32_t v)
{
	uint32_t r = 0U;
	uint32_t bit = 1UL << 30;

	while (bit > v) {
		bit >>= 2;
	}

	while (bit != 0U) {
		if (v >= r + bit) {
			v -= r + bit;
			r = (r >> 1) + bit;
		} else {
			r >>= 1;
		}
		bit >>= 2;
	}

	return r;
}
