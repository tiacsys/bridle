/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <math.h>

#include <zephyr/logging/log.h>

#include "bubble.h"

LOG_MODULE_DECLARE(level, CONFIG_LEVEL_LOG_LEVEL);

/** @brief The channel level a fully lit primary colour is drawn at. */
#define LIT ((uint8_t)CONFIG_LEVEL_BRIGHTNESS)

/* The two ends of the colour scale, interpolated by tilt magnitude and
 * latched to the near end once the board is level. Changing the pairing,
 * say to something a red-green colour deficiency can still read, means
 * editing these two lines and nothing else.
 */
#define BUBBLE_COLOR_FAR  MATRIX_RGB(LIT, 0U, 0U)
#define BUBBLE_COLOR_NEAR MATRIX_RGB(0U, LIT, 0U)

#define PI_F             3.14159265358979f
#define DEG_TO_RAD(_deg) ((_deg) * PI_F / 180.0f)

/** @brief Interpolate from @p from to @p to by @p t. */
static uint8_t lerp_channel(uint8_t from, uint8_t to, float t)
{
	return (uint8_t)lroundf((float)from + (((float)to - (float)from) * t));
}

/** @brief Interpolate from @p from to @p to by @p t, per channel. */
static struct matrix_rgb lerp_color(struct matrix_rgb from, struct matrix_rgb to, float t)
{
	struct matrix_rgb out;

	out.r = lerp_channel(from.r, to.r, t);
	out.g = lerp_channel(from.g, to.g, t);
	out.b = lerp_channel(from.b, to.b, t);

	return out;
}

/**
 * @brief Decide whether the board counts as level, with hysteresis.
 *
 * The latch engages at one angle and releases at a wider one, so a
 * board balanced on the threshold stays stable instead of flickering
 * with every noisy sample.
 *
 * @param tilt Current attitude.
 * @param locked Whether the latch was engaged on the previous frame.
 *
 * @return Whether the latch is engaged now.
 */
static bool level_latched(const struct tilt *tilt, bool locked)
{
	/* Compared in sine space, like every other angle in this sample. */
	const float engage = sinf(DEG_TO_RAD((float)CONFIG_LEVEL_LOCK_TILT / 10.0f));
	const float release = sinf(
		DEG_TO_RAD((float)(CONFIG_LEVEL_LOCK_TILT + CONFIG_LEVEL_LOCK_HYSTERESIS) / 10.0f));

	if (!tilt->valid || (CONFIG_LEVEL_LOCK_TILT == 0)) {
		/* Free fall is never level; zero disables the latch. */
		return false;
	}

	return locked ? (tilt->magnitude <= release) : (tilt->magnitude <= engage);
}

void bubble_update(const struct matrix *matrix, const struct tilt *tilt, struct bubble *bubble)
{
	/* The panel centre the bubble returns to at level. It lands between
	 * pixels on an even panel and on a pixel on an odd one; both are
	 * fine as long as it stays fractional.
	 */
	const float centre_x = (float)(matrix->width - 1U) * 0.5f;
	const float centre_y = (float)(matrix->height - 1U) * 0.5f;

	/* Tilt is carried as a sine, so the full scale angle has to become
	 * one too before the two can be divided.
	 */
	const float full_scale = sinf(DEG_TO_RAD((float)CONFIG_LEVEL_FULL_SCALE_TILT));

	/* Colour responds over a much tighter angle than position: it covers
	 * the last degree or so, where the panel has no resolution left.
	 */
	const float color_range = sinf(DEG_TO_RAD((float)CONFIG_LEVEL_COLOR_RANGE_TILT / 10.0f));

	float travel_x = 0.0f;
	float travel_y = 0.0f;

	bubble->off_scale = false;
	bubble->proximity = 0.0f;

	/* Reads the previous latch and writes back the new one, which is
	 * why the same struct is passed in every frame.
	 */
	bubble->locked = level_latched(tilt, bubble->locked);

	if (tilt->valid) {
		float travel;

		travel_x = tilt->x / full_scale;
		travel_y = tilt->y / full_scale;

		travel = sqrtf((travel_x * travel_x) + (travel_y * travel_y));
		if (travel > 1.0f) {
			travel_x /= travel;
			travel_y /= travel;
			bubble->off_scale = true;
		}

		/* One at dead level, zero at the edge of the colour range.
		 * Stays zero for an invalid attitude, so free fall is never
		 * painted as level.
		 */
		if (tilt->magnitude < color_range) {
			bubble->proximity = 1.0f - (tilt->magnitude / color_range);
		}
	}

	if (bubble->locked) {
		/* When latched, snap to the near colour so the level state
		 * is visible rather than inferred.
		 */
		bubble->proximity = 1.0f;
	}

	bubble->x = centre_x + (travel_x * centre_x);
	bubble->y = centre_y + (travel_y * centre_y);
}

void bubble_render(struct matrix *matrix, const struct bubble *bubble)
{
	/* Colour conveys what position cannot: how close to level the board
	 * is once the bubble has stopped visibly moving.
	 */
	const struct matrix_rgb color =
		lerp_color(BUBBLE_COLOR_FAR, BUBBLE_COLOR_NEAR, bubble->proximity);

	/* The position is fractional, and the splat keeps it that way: it
	 * spreads the bubble over the pixels it straddles, weighted by
	 * coverage, so the eye reads its position from the balance between
	 * them rather than from which one is lit.
	 *
	 * This also centres the bubble on a panel that has no middle pixel:
	 * at (3.5, 3.5) the four central pixels come up equally bright, on
	 * an odd-sided panel the single central pixel comes up alone.
	 * Neither case is special to the code.
	 */
	matrix_splat(matrix, bubble->x, bubble->y, color);
}
