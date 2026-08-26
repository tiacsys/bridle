/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "hsv.h"

/** Scale @p a by the fraction @p b / 255, rounding towards zero. */
#define SCALE8(a, b) ((uint8_t)(((uint32_t)(a) * (uint32_t)(b)) / 255U))

void hsv_to_rgb(uint16_t hue, uint8_t sat, uint8_t val, struct hsv_rgb *out)
{
	uint8_t sector;
	uint8_t offset;
	uint8_t p, q, t;

	if (sat == 0U) {
		/* No saturation means a pure shade of grey. */
		out->r = val;
		out->g = val;
		out->b = val;
		return;
	}

	hue %= 360U;

	/* The six 60 degree sectors of the color wheel, plus the offset within
	 * the sector rescaled from [0, 60) to [0, 255].
	 */
	sector = (uint8_t)(hue / 60U);
	offset = (uint8_t)(((hue % 60U) * 255U) / 60U);

	/* The three secondary levels of the classic HSV conversion:
	 * p is the falling channel, q falls and t rises within the sector.
	 */
	p = SCALE8(val, 255U - sat);
	q = SCALE8(val, 255U - SCALE8(sat, offset));
	t = SCALE8(val, 255U - SCALE8(sat, 255U - offset));

	switch (sector) {
	case 0: /* red -> yellow */
		out->r = val;
		out->g = t;
		out->b = p;
		break;
	case 1: /* yellow -> green */
		out->r = q;
		out->g = val;
		out->b = p;
		break;
	case 2: /* green -> cyan */
		out->r = p;
		out->g = val;
		out->b = t;
		break;
	case 3: /* cyan -> blue */
		out->r = p;
		out->g = q;
		out->b = val;
		break;
	case 4: /* blue -> magenta */
		out->r = t;
		out->g = p;
		out->b = val;
		break;
	default: /* magenta -> red */
		out->r = val;
		out->g = p;
		out->b = q;
		break;
	}
}
