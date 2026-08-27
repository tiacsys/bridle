/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef LEVEL_MATRIX_H_
#define LEVEL_MATRIX_H_

#include <stdint.h>

#include <zephyr/device.h>
#include <zephyr/drivers/display.h>

#ifdef __cplusplus
extern "C" {
#endif

/** @brief A colour in the sRGB cube, one byte per channel. */
struct matrix_rgb {
	uint8_t r;
	uint8_t g;
	uint8_t b;
};

/** @brief Compound literal for an opaque sRGB colour. */
#define MATRIX_RGB(_r, _g, _b) ((struct matrix_rgb){.r = (_r), .g = (_g), .b = (_b)})

/** @brief The colour of an unlit pixel. */
#define MATRIX_BLACK MATRIX_RGB(0U, 0U, 0U)

/**
 * @brief An RGB matrix driven through the display driver API.
 *
 * Everything in here is filled in by matrix_init() and should be treated
 * as read only afterwards. Drawing goes through matrix_set_pixel() and
 * friends, which paint into an off screen frame buffer, and reaches the
 * panel only once matrix_flush() is called.
 */
struct matrix {
	/** The underlying display device. */
	const struct device *dev;
	/** Panel geometry as reported by the driver, in pixels. */
	uint16_t width;
	uint16_t height;
	/** Pixel format the driver is currently configured for. */
	enum display_pixel_format format;
	/** Bytes one pixel occupies in the frame buffer. */
	size_t bpp;
	/** Descriptor handed to display_write(), prepared once. */
	struct display_buffer_descriptor desc;
	/** Off screen frame buffer, owned by the matrix module. */
	uint8_t *buf;
};

/**
 * @brief Bring up the chosen RGB matrix and its frame buffer.
 *
 * Fetches the panel geometry and pixel format from the driver, checks
 * that both fit what this sample can render, switches blanking off and
 * clears the frame buffer. The panel itself is left untouched until the
 * first matrix_flush().
 *
 * @param matrix Destination descriptor, must not be @c NULL.
 *
 * @retval 0 On success.
 * @retval -ENODEV If the display device is not ready.
 * @retval -ENOTSUP If the pixel format is neither RGB_888 nor ARGB_8888.
 * @retval -ENOMEM If the panel is larger than the compiled in frame buffer.
 * @retval -errno Otherwise, as reported by the display driver.
 */
int matrix_init(struct matrix *matrix);

/**
 * @brief Paint a single pixel into the frame buffer.
 *
 * Coordinates outside the panel are silently ignored, so callers may
 * clip lazily.
 *
 * @param matrix Initialised matrix descriptor.
 * @param x Column, counted from the left edge.
 * @param y Row, counted from the top edge.
 * @param color Colour to write.
 */
void matrix_set_pixel(struct matrix *matrix, int x, int y, struct matrix_rgb color);

/**
 * @brief Add light to a single pixel of the frame buffer.
 *
 * Like matrix_set_pixel(), but sums into whatever is already there and
 * saturates at full drive rather than overwriting, which lets several
 * things share a pixel.
 *
 * Coordinates outside the panel are silently ignored.
 *
 * @param matrix Initialised matrix descriptor.
 * @param x Column, counted from the left edge.
 * @param y Row, counted from the top edge.
 * @param color Colour to add.
 */
void matrix_add_pixel(struct matrix *matrix, int x, int y, struct matrix_rgb color);

/**
 * @brief Paint a point of light at a fractional position.
 *
 * Spreads @p color over the up to four pixels that the point at
 * (@p x, @p y) straddles, weighting each by how much of it the point
 * covers. The weights are bilinear and sum to one, so the panel stays
 * equally bright wherever the point sits, and the eye reads its
 * position from the balance between the lit pixels.
 *
 * This buys sub-pixel resolution on a panel with very few pixels but
 * plenty of brightness steps, and it needs no special case for an even
 * number of pixels: a point at (3.5, 3.5) simply lights the four middle
 * pixels equally, while on an odd-sided panel a point at (2.0, 2.0)
 * lights the single middle one.
 *
 * Contributions falling outside the panel are silently dropped.
 *
 * @param matrix Initialised matrix descriptor.
 * @param x Column, in pixel centre coordinates.
 * @param y Row, in pixel centre coordinates.
 * @param color Colour of the point at full weight.
 */
void matrix_splat(struct matrix *matrix, float x, float y, struct matrix_rgb color);

/**
 * @brief Paint every pixel of the frame buffer in one colour.
 *
 * @param matrix Initialised matrix descriptor.
 * @param color Colour to write.
 */
void matrix_fill(struct matrix *matrix, struct matrix_rgb color);

/**
 * @brief Paint every pixel of the frame buffer black.
 *
 * @param matrix Initialised matrix descriptor.
 */
void matrix_clear(struct matrix *matrix);

/**
 * @brief Push the frame buffer out to the panel.
 *
 * @param matrix Initialised matrix descriptor.
 *
 * @retval 0 On success.
 * @retval -errno Otherwise, as reported by the display driver.
 */
int matrix_flush(struct matrix *matrix);

#ifdef __cplusplus
}
#endif

#endif /* LEVEL_MATRIX_H_ */
