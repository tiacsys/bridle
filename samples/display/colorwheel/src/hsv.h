/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef COLORWHEEL_HSV_H_
#define COLORWHEEL_HSV_H_

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/** @brief A color in the sRGB cube, one byte per channel. */
struct hsv_rgb {
	uint8_t r;
	uint8_t g;
	uint8_t b;
};

/**
 * @brief Convert an HSV color into its RGB representation.
 *
 * The conversion is done entirely in integer arithmetic, so it is cheap
 * enough to run per pixel and per frame even on a core without an FPU.
 *
 * @param hue Hue in degrees. Values outside [0, 360) are wrapped.
 * @param sat Saturation, from 0 (grey) to 255 (fully saturated).
 * @param val Value (brightness), from 0 (black) to 255 (full).
 * @param out Destination color, must not be @c NULL.
 */
void hsv_to_rgb(uint16_t hue, uint8_t sat, uint8_t val, struct hsv_rgb *out);

#ifdef __cplusplus
}
#endif

#endif /* COLORWHEEL_HSV_H_ */
