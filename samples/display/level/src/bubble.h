/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef LEVEL_BUBBLE_H_
#define LEVEL_BUBBLE_H_

#include <stdbool.h>

#include "matrix.h"
#include "tilt.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief The state of the level indicator.
 *
 * The position is a continuous coordinate in pixel centre space, so the
 * centre of an eight pixel wide panel is @c 3.5, between two pixels,
 * and that of a five pixel wide one is @c 2.0, on a pixel. Keeping the
 * fraction rather than rounding it away is what allows the bubble to be
 * rendered with sub-pixel accuracy.
 *
 * @note This is state, not a fresh result. bubble_update() carries the
 *       @c locked latch over from one call to the next, so the same
 *       struct has to be handed back in every frame, and it has to start
 *       out zeroed.
 */
struct bubble {
	/** Column, in pixel centre coordinates. */
	float x;
	/** Row, in pixel centre coordinates. */
	float y;
	/**
	 * @brief How close to level the board is, from 0 to 1.
	 *
	 * One at dead level, zero at CONFIG_LEVEL_COLOR_RANGE_TILT and
	 * beyond, interpolated in between. This drives the colour of the
	 * bubble, which exists because position alone cannot resolve near
	 * the middle: the last degree of tilt moves the bubble by a
	 * fraction of a pixel, too little to see.
	 *
	 * Pinned to one while @c locked, and zero whenever the attitude is
	 * not valid, so that a board in free fall is never reported as
	 * level.
	 */
	float proximity;
	/**
	 * @brief Whether the board currently counts as level.
	 *
	 * Latched with hysteresis: engages at CONFIG_LEVEL_LOCK_TILT and
	 * does not release until the board is tipped past that plus
	 * CONFIG_LEVEL_LOCK_HYSTERESIS. Carried over between calls, which
	 * is why this struct is state rather than a result.
	 */
	bool locked;
	/** Whether the tilt exceeded full scale and the position was clamped. */
	bool off_scale;
};

/**
 * @brief Bring the bubble up to date for a given attitude.
 *
 * The bubble travels away from the centre of the panel in proportion to
 * the tilt, reaching the rim at CONFIG_LEVEL_FULL_SCALE_TILT degrees.
 * Beyond full scale it is clamped radially, so it sweeps a disc like the
 * bubble in a real vial instead of reaching into the corners.
 *
 * Its colour is worked out over the much tighter
 * CONFIG_LEVEL_COLOR_RANGE_TILT, and latches once the board is level.
 *
 * @param matrix Initialised matrix, read for its geometry only.
 * @param tilt Attitude to place the bubble for.
 * @param bubble Bubble to update, must not be @c NULL, and must be the
 *               same one as on the previous call so that the latch is
 *               carried over.
 */
void bubble_update(const struct matrix *matrix, const struct tilt *tilt, struct bubble *bubble);

/**
 * @brief Paint the bubble into the frame buffer.
 *
 * Does not clear the frame buffer first, so the caller decides what else
 * shares the panel.
 *
 * @param matrix Initialised matrix.
 * @param bubble Position to paint at.
 */
void bubble_render(struct matrix *matrix, const struct bubble *bubble);

#ifdef __cplusplus
}
#endif

#endif /* LEVEL_BUBBLE_H_ */
