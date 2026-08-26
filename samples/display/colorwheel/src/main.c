/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <string.h>

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/display.h>
#include <zephyr/logging/log.h>

#include "hsv.h"
#include "polar.h"

LOG_MODULE_REGISTER(colorwheel, CONFIG_COLORWHEEL_LOG_LEVEL);

#if !DT_HAS_CHOSEN(zephyr_display)
#error "This sample needs an RGB matrix assigned to the chosen zephyr,display node"
#endif

#define MATRIX_NODE   DT_CHOSEN(zephyr_display)
#define MATRIX_WIDTH  DT_PROP(MATRIX_NODE, width)
#define MATRIX_HEIGHT DT_PROP(MATRIX_NODE, height)

/* The frame buffer is sized at build time for the worst case, ARGB_8888
 * with four bytes per pixel. The actual pixel format is queried at run
 * time and may be narrower.
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

/** @brief Write one color to the frame buffer at @p dst. */
static void put_pixel(uint8_t *dst, enum display_pixel_format format, const struct hsv_rgb *color)
{
	if (format == PIXEL_FORMAT_ARGB_8888) {
		uint32_t argb = 0xFF000000U | ((uint32_t)color->r << 16) |
				((uint32_t)color->g << 8) | (uint32_t)color->b;

		/* An unaligned native store, matching how the LED strip
		 * matrix driver reads the pixel back.
		 */
		memcpy(dst, &argb, sizeof(argb));
	} else {
		dst[0] = color->r;
		dst[1] = color->g;
		dst[2] = color->b;
	}
}

/**
 * @brief Paint one full frame of the color wheel into @p buf.
 *
 * Each pixel is placed in polar coordinates centred on the panel. Hue
 * follows the polar angle, so a full rainbow wraps once around the
 * centre, while saturation rises with the radius: a bright white core
 * in the centre blooms into fully saturated color. The radius is
 * normalised against a fraction of the corner distance set by
 * CONFIG_COLORWHEEL_SAT_SCALE, so the ramp reaches full saturation
 * before the corners. The value is fixed at
 * CONFIG_COLORWHEEL_MAX_BRIGHTNESS, keeping the white core bright and
 * bounding the panel's current draw.
 *
 * Advancing @p phase between frames rotates the wheel.
 */
static void render_frame(uint8_t *buf, uint16_t width, uint16_t height,
			 enum display_pixel_format format, size_t bpp, uint16_t phase)
{
	/* Pixel-centred coordinates in units of 1/8 pixel, so the origin lands on the geometric
	 * centre of the panel even when a dimension is even and no pixel sits exactly on it.
	 */
	const uint32_t center_w = (uint32_t)width * COLORWHEEL_COORD_ONE - 1U;
	const uint32_t center_h = (uint32_t)height * COLORWHEEL_COORD_ONE - 1U;

	/* Reference radius: the panel corner, in the same units. The saturation ramp is scaled to
	 * reach full saturation at a fraction of this corner distance. The scale is a percentage,
	 * so the computation stays in integer arithmetic.
	 */
	const int32_t corner_x = (int32_t)(center_w / 2U);
	const int32_t corner_y = (int32_t)(center_h / 2U);
	const uint32_t corner = polar_isqrt((uint32_t)(corner_x * corner_x + corner_y * corner_y));
	const uint32_t radius_max = (corner * (uint32_t)CONFIG_COLORWHEEL_SAT_SCALE) / 100U;

	for (uint16_t y = 0U; y < height; y++) {
		for (uint16_t x = 0U; x < width; x++) {
			const int32_t fx = (int32_t)((uint32_t)x * COLORWHEEL_COORD_ONE) -
					   (int32_t)(center_w / 2U);
			const int32_t fy = (int32_t)((uint32_t)y * COLORWHEEL_COORD_ONE) -
					   (int32_t)(center_h / 2U);
			const uint32_t radius = polar_isqrt((uint32_t)(fx * fx + fy * fy));
			const uint16_t angle = polar_atan2_deg(fy, fx);
			struct hsv_rgb color;
			uint32_t saturation;

			/* Saturation is the radius normalised to [0, 255] against the scaled
			 * reference: a white core in the centre, fully saturated color at the
			 * reference radius, clamped beyond it. The value stays at the brightness
			 * ceiling, so the core stays bright and the panel draws a bounded current.
			 */
			saturation = (radius_max != 0U) ? ((radius * 255U) / radius_max) : 0U;
			if (saturation > 255U) {
				saturation = 255U;
			}

			hsv_to_rgb((uint16_t)(((uint32_t)angle + phase) % 360U),
				   (uint8_t)saturation, (uint8_t)CONFIG_COLORWHEEL_MAX_BRIGHTNESS,
				   &color);

			put_pixel(buf, format, &color);
			buf += bpp;
		}
	}
}

int main(void)
{
	const struct device *const display = DEVICE_DT_GET(MATRIX_NODE);
	struct display_buffer_descriptor desc;
	struct display_capabilities caps;
	enum display_pixel_format format;
	uint16_t phase = 0U;
	size_t bpp;
	int ret;

	if (!device_is_ready(display)) {
		LOG_ERR("Display device %s is not ready", display->name);
		return -ENODEV;
	}

	display_get_capabilities(display, &caps);
	format = caps.current_pixel_format;
	bpp = bytes_per_pixel(format);

	if (bpp == 0U) {
		LOG_ERR("Pixel format %d is not supported, need RGB_888 or ARGB_8888", format);
		return -ENOTSUP;
	}

	if ((caps.x_resolution > MATRIX_WIDTH) || (caps.y_resolution > MATRIX_HEIGHT)) {
		LOG_ERR("Display is %ux%u, but the frame buffer only holds %ux%u",
			caps.x_resolution, caps.y_resolution, (unsigned int)MATRIX_WIDTH,
			(unsigned int)MATRIX_HEIGHT);
		return -ENOMEM;
	}

	/* The LED strip matrix driver does not implement blanking,
	 * so -ENOSYS is not an error.
	 */
	ret = display_blanking_off(display);
	if ((ret < 0) && (ret != -ENOSYS)) {
		LOG_ERR("Failed to switch off display blanking (%d)", ret);
		return ret;
	}

	desc.width = caps.x_resolution;
	desc.height = caps.y_resolution;
	desc.pitch = caps.x_resolution;
	desc.buf_size = (uint32_t)caps.x_resolution * caps.y_resolution * bpp;
	desc.frame_incomplete = false;

	LOG_INF("Color wheel on a %ux%u RGB matrix, %u bytes per pixel, %u ms per frame",
		caps.x_resolution, caps.y_resolution, (unsigned int)bpp,
		(unsigned int)CONFIG_COLORWHEEL_FRAME_INTERVAL);

	while (true) {
		render_frame(frame_buf, caps.x_resolution, caps.y_resolution, format, bpp, phase);

		ret = display_write(display, 0, 0, &desc, frame_buf);
		if (ret < 0) {
			LOG_ERR("Failed to write a frame to the display (%d)", ret);
			return ret;
		}

		phase = (uint16_t)((phase + CONFIG_COLORWHEEL_HUE_STEP) % 360U);

		k_sleep(K_MSEC(CONFIG_COLORWHEEL_FRAME_INTERVAL));
	}
}
