/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <math.h>
#include <string.h>

#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/display.h>
#include <zephyr/logging/log.h>

#include "matrix.h"

LOG_MODULE_DECLARE(level, CONFIG_LEVEL_LOG_LEVEL);

#if !DT_HAS_CHOSEN(zephyr_display)
#error "This sample needs an RGB matrix assigned to the chosen zephyr,display node"
#endif

#define MATRIX_NODE   DT_CHOSEN(zephyr_display)
#define MATRIX_WIDTH  DT_PROP(MATRIX_NODE, width)
#define MATRIX_HEIGHT DT_PROP(MATRIX_NODE, height)

/* The frame buffer is sized at build time for the worst supported case,
 * ARGB_8888 at four bytes per pixel. The format in use is queried at
 * run time and may be narrower.
 */
#define MATRIX_MAX_BPP 4U
#define FRAME_BUF_SIZE ((size_t)MATRIX_WIDTH * MATRIX_HEIGHT * MATRIX_MAX_BPP)

static uint8_t frame_buf[FRAME_BUF_SIZE];

/** @brief Bytes per pixel, or 0 if the format is not supported. */
static size_t bytes_per_pixel(enum display_pixel_format format)
{
	switch (format) {
	case PIXEL_FORMAT_ARGB_8888:
		return 4U;
	case PIXEL_FORMAT_RGB_888:
		return 3U;
	default:
		return 0U;
	}
}

/** @brief Write one colour to the frame buffer at @p dst. */
static void put_pixel(uint8_t *dst, enum display_pixel_format format, struct matrix_rgb color)
{
	if (format == PIXEL_FORMAT_ARGB_8888) {
		uint32_t argb = 0xFF000000U | ((uint32_t)color.r << 16) | ((uint32_t)color.g << 8) |
				(uint32_t)color.b;

		/* Unaligned native store, matching how the LED strip matrix
		 * driver reads the pixel back.
		 */
		memcpy(dst, &argb, sizeof(argb));
	} else {
		dst[0] = color.r;
		dst[1] = color.g;
		dst[2] = color.b;
	}
}

int matrix_init(struct matrix *matrix)
{
	const struct device *const dev = DEVICE_DT_GET(MATRIX_NODE);
	struct display_capabilities caps;
	int ret;

	if (!device_is_ready(dev)) {
		LOG_ERR("Display device %s is not ready", dev->name);
		return -ENODEV;
	}

	display_get_capabilities(dev, &caps);

	matrix->dev = dev;
	matrix->width = caps.x_resolution;
	matrix->height = caps.y_resolution;
	matrix->format = caps.current_pixel_format;
	matrix->bpp = bytes_per_pixel(matrix->format);
	matrix->buf = frame_buf;

	if (matrix->bpp == 0U) {
		LOG_ERR("Pixel format %d is not supported, need RGB_888 or ARGB_8888",
			matrix->format);
		return -ENOTSUP;
	}

	if ((matrix->width > MATRIX_WIDTH) || (matrix->height > MATRIX_HEIGHT)) {
		LOG_ERR("Display is %ux%u, but the frame buffer only holds %ux%u", matrix->width,
			matrix->height, (unsigned int)MATRIX_WIDTH, (unsigned int)MATRIX_HEIGHT);
		return -ENOMEM;
	}

	/* Not every display driver implements blanking; the LED strip
	 * matrix is one of those, so -ENOSYS is not an error here.
	 */
	ret = display_blanking_off(dev);
	if ((ret < 0) && (ret != -ENOSYS)) {
		LOG_ERR("Failed to switch off display blanking (%d)", ret);
		return ret;
	}

	matrix->desc.width = matrix->width;
	matrix->desc.height = matrix->height;
	matrix->desc.pitch = matrix->width;
	matrix->desc.buf_size = (uint32_t)matrix->width * matrix->height * matrix->bpp;
	matrix->desc.frame_incomplete = false;

	matrix_clear(matrix);

	return 0;
}

/** @brief Read one colour from the frame buffer at @p src. */
static void get_pixel(const uint8_t *src, enum display_pixel_format format, struct matrix_rgb *out)
{
	if (format == PIXEL_FORMAT_ARGB_8888) {
		uint32_t argb;

		memcpy(&argb, src, sizeof(argb));

		out->r = (uint8_t)((argb >> 16) & 0xFFU);
		out->g = (uint8_t)((argb >> 8) & 0xFFU);
		out->b = (uint8_t)(argb & 0xFFU);
	} else {
		out->r = src[0];
		out->g = src[1];
		out->b = src[2];
	}
}

/** @brief Address of one pixel in the frame buffer, or NULL if off panel. */
static uint8_t *pixel_at(struct matrix *matrix, int x, int y)
{
	if ((x < 0) || (y < 0) || (x >= (int)matrix->width) || (y >= (int)matrix->height)) {
		return NULL;
	}

	return &matrix->buf[(((size_t)y * matrix->width) + (size_t)x) * matrix->bpp];
}

/** @brief Sum two channel levels, stopping at full drive. */
static uint8_t add_saturating(uint8_t a, uint8_t b)
{
	uint16_t sum = (uint16_t)a + (uint16_t)b;

	return (sum > 255U) ? 255U : (uint8_t)sum;
}

/** @brief Dim a colour to @p weight of its full strength. */
static struct matrix_rgb scale_color(struct matrix_rgb color, float weight)
{
	struct matrix_rgb out;

	out.r = (uint8_t)lroundf((float)color.r * weight);
	out.g = (uint8_t)lroundf((float)color.g * weight);
	out.b = (uint8_t)lroundf((float)color.b * weight);

	return out;
}

void matrix_set_pixel(struct matrix *matrix, int x, int y, struct matrix_rgb color)
{
	uint8_t *dst = pixel_at(matrix, x, y);

	if (dst == NULL) {
		return;
	}

	put_pixel(dst, matrix->format, color);
}

void matrix_add_pixel(struct matrix *matrix, int x, int y, struct matrix_rgb color)
{
	uint8_t *dst = pixel_at(matrix, x, y);
	struct matrix_rgb current;

	if (dst == NULL) {
		return;
	}

	get_pixel(dst, matrix->format, &current);

	current.r = add_saturating(current.r, color.r);
	current.g = add_saturating(current.g, color.g);
	current.b = add_saturating(current.b, color.b);

	put_pixel(dst, matrix->format, current);
}

void matrix_splat(struct matrix *matrix, float x, float y, struct matrix_rgb color)
{
	/* The pixel the point falls into, and how far into it the point sits
	 * along each axis. A fraction of zero means the point is dead centre
	 * on that pixel and its neighbour gets nothing.
	 */
	const int x0 = (int)floorf(x);
	const int y0 = (int)floorf(y);
	const float fx = x - floorf(x);
	const float fy = y - floorf(y);

	/* Bilinear coverage of the four pixels the point straddles. These
	 * sum to one, which is what keeps the panel equally bright wherever
	 * the point happens to sit.
	 */
	matrix_add_pixel(matrix, x0, y0, scale_color(color, (1.0f - fx) * (1.0f - fy)));
	matrix_add_pixel(matrix, x0 + 1, y0, scale_color(color, fx * (1.0f - fy)));
	matrix_add_pixel(matrix, x0, y0 + 1, scale_color(color, (1.0f - fx) * fy));
	matrix_add_pixel(matrix, x0 + 1, y0 + 1, scale_color(color, fx * fy));
}

void matrix_fill(struct matrix *matrix, struct matrix_rgb color)
{
	uint8_t *dst = matrix->buf;

	for (size_t i = 0U; i < ((size_t)matrix->width * matrix->height); i++) {
		put_pixel(dst, matrix->format, color);
		dst += matrix->bpp;
	}
}

void matrix_clear(struct matrix *matrix)
{
	matrix_fill(matrix, MATRIX_BLACK);
}

int matrix_flush(struct matrix *matrix)
{
	int ret;

	ret = display_write(matrix->dev, 0, 0, &matrix->desc, matrix->buf);
	if (ret < 0) {
		LOG_ERR("Failed to write a frame to the display (%d)", ret);
	}

	return ret;
}
