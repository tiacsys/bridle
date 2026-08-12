/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 *
 * Based on Zephyr upstream display driver sample:
 * Copyright (c) 2019 Jan Van Winkel <jan.van_winkel@dxplore.eu>
 * Copyright (c) 2025 NXP
 */

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(sample, LOG_LEVEL_INF);

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/display.h>
#include <zephyr/pm/device_runtime.h>
#include <zephyr/sys/byteorder.h>

#ifdef CONFIG_ARCH_POSIX
#include "posix_board_if.h"
#endif

#include "colorful.h"

typedef void (*fill_buffer)(uint8_t red_lumina, uint8_t green, uint8_t blue, uint8_t *buf,
			    size_t buf_size, enum display_pixel_format fmt);

static inline uint8_t fast_rgb2y(uint8_t red, uint8_t green, uint8_t blue)
{
	/* Digital ITU BT.601 Luminance (relative):
	 *
	 *    Y = 0.299 * R + 0.587 * G + 0.114 * B
	 *
	 * Details on and fast approximation from:
	 *    - https://www.scantips.com/lumin.html
	 *    - https://www.songho.ca/dsp/luminance/luminance.html#fast
	 */
	uint16_t lumina = (2 * (uint16_t)red + 5 * (uint16_t)green + 1 * (uint16_t)blue) >> 3;

	return (uint8_t)(lumina & 0xFFu);
}

static void fill_buffer_argb8888(uint8_t r, uint8_t g, uint8_t b, uint8_t *buf, size_t buf_size,
				 enum display_pixel_format fmt)
{
	uint8_t a = 0xFFu;
	uint32_t color;

	switch (fmt) {
	case PIXEL_FORMAT_ABGR_8888:
		color = (uint32_t)a << 24 | (uint32_t)b << 16 | (uint32_t)g << 8 | r;
		break;
	case PIXEL_FORMAT_RGBA_8888:
		color = (uint32_t)r << 24 | (uint32_t)g << 16 | (uint32_t)b << 8 | a;
		break;
	case PIXEL_FORMAT_BGRA_8888:
		color = (uint32_t)b << 24 | (uint32_t)g << 16 | (uint32_t)r << 8 | a;
		break;
	default: /* PIXEL_FORMAT_ARGB_8888 / PIXEL_FORMAT_XRGB_8888 */
		color = (uint32_t)a << 24 | (uint32_t)r << 16 | (uint32_t)g << 8 | b;
		break;
	}

	for (size_t idx = 0; idx < buf_size; idx += 4) {
		*((uint32_t *)(buf + idx)) = sys_cpu_to_le32(color);
	}
}

static void fill_buffer_rgb888(uint8_t r, uint8_t g, uint8_t b, uint8_t *buf, size_t buf_size,
			       enum display_pixel_format fmt)
{
	uint8_t byte0, byte1, byte2;

	if (fmt == PIXEL_FORMAT_BGR_888) {
		byte0 = r;
		byte1 = g;
		byte2 = b;
	} else { /* PIXEL_FORMAT_RGB_888 */
		byte0 = b;
		byte1 = g;
		byte2 = r;
	}

	for (size_t idx = 0; idx < buf_size; idx += 3) {
		*(buf + idx + 0) = byte0;
		*(buf + idx + 1) = byte1;
		*(buf + idx + 2) = byte2;
	}
}

static void fill_buffer_rgb565(uint8_t r, uint8_t g, uint8_t b, uint8_t *buf, size_t buf_size,
			       enum display_pixel_format fmt)
{
	/* shift the green an extra bit, it has 6 bits */
	uint16_t color = ((uint16_t)r & 0x1Fu) << 11 | ((uint16_t)g & 0x1Fu) << (5 + 1) |
			 ((uint16_t)b & 0x1Fu);

	if (fmt == PIXEL_FORMAT_RGB_565) {
		for (size_t idx = 0; idx < buf_size; idx += 2) {
			*(uint16_t *)(buf + idx) = color;
		}
	} else { /* PIXEL_FORMAT_RGB_565X */
		for (size_t idx = 0; idx < buf_size; idx += 2) {
			*(buf + idx + 0) = (color >> 8) & 0xFFu;
			*(buf + idx + 1) = (color >> 0) & 0xFFu;
		}
	}
}

static void fill_buffer_al_88(uint8_t r, uint8_t g, uint8_t b, uint8_t *buf, size_t buf_size,
			      enum display_pixel_format fmt)
{
	uint16_t word = 0xFF00u | fast_rgb2y(r, g, b);

	for (size_t idx = 0; idx < buf_size; idx += 2) {
		*((uint16_t *)(buf + idx)) = sys_cpu_to_le16(word);
	}
}

static void fill_buffer_l_8(uint8_t r, uint8_t g, uint8_t b, uint8_t *buf, size_t buf_size,
			    enum display_pixel_format fmt)
{
	uint8_t byte = 0x00u | fast_rgb2y(r, g, b);

	for (size_t idx = 0; idx < buf_size; idx += 1) {
		*(uint8_t *)(buf + idx) = byte;
	}
}

static void fill_buffer_l_4(uint8_t r, uint8_t g, uint8_t b, uint8_t *buf, size_t buf_size,
			    enum display_pixel_format fmt)
{
	uint8_t nibble = 0x0Fu & fast_rgb2y(r, g, b);
	uint8_t byte = (nibble << 4) | nibble;

	for (size_t idx = 0; idx < buf_size; idx += 1) {
		*(uint8_t *)(buf + idx) = byte;
	}
}

static void fill_buffer_mono(uint8_t r, uint8_t g, uint8_t b, uint8_t *buf, size_t buf_size,
			     enum display_pixel_format fmt)
{
	uint8_t lumina = fast_rgb2y(r, g, b);
	uint8_t byte;

	if (fmt == PIXEL_FORMAT_MONO01) {
		byte = (lumina & 0x01u) ? 0xFFu : 0x00u;
	} else { /* PIXEL_FORMAT_MONO10 */
		byte = (lumina & 0x01u) ? 0x00u : 0xFFu;
	}

	memset(buf, byte, buf_size);
}

static int write_lines_to_display(const struct device * const display, uint16_t lines,
				  struct display_buffer_descriptor *buf_desc, const uint8_t *buf)
{
	int ret = 0;

	/* This allows double-buffered displays to hold the pixels back
	 * until the first image is complete.
	 */
	buf_desc->frame_incomplete = true;

	for (int y = 0; y <= lines; ++y) {
		ret = display_write(display, 0, y, buf_desc, buf);
		if (ret < 0) {
			break;
		}

		/* With next (last) write the full frame is ready for output,
		 * so turn this off. Double-buffered displays will then
		 * present the new image to the user.
		 */
		if (y == lines) {
			buf_desc->frame_incomplete = false;
		}
	}

	return ret;
}

int sample_colorful_draw(void)
{
	const struct device *display;
	struct display_capabilities capabilities;
	struct display_buffer_descriptor buf_desc;
	uint8_t bg_ival;	/* background initial value */
	uint8_t cg_mval;	/* color/gray maximum value */
	uint16_t hlc_max;	/* height line count maximum */
	size_t buf_size = 0;
	uint8_t *buf;
	fill_buffer fill_buffer_fnc = NULL;
	int32_t gradient_sleep;
	size_t gradient_count = 0;
	int ret = 0;

	display = DEVICE_DT_GET(DT_CHOSEN(zephyr_display));
	if (!device_is_ready(display)) {
		LOG_ERR("Device %s not found. Aborting sample.", display->name);
		ret = -ENODEV;
		goto end;
	}

	/* Hold a runtime PM reference so the display stays active for the
	 * duration of the sample. No-op when runtime PM is not enabled on
	 * the device.
	 */
	(void)pm_device_runtime_get(display);

	display_get_capabilities(display, &capabilities);
	LOG_INF("Colorful sample for %s", display->name);
	LOG_INF("%s: %ux%u, pixel format: %u", display->name, capabilities.x_resolution,
		capabilities.y_resolution, capabilities.current_pixel_format);

	/* Screen is an Electrophoretic Display (ePaper). */
	if (capabilities.screen_info & SCREEN_INFO_EPD) {
		gradient_sleep = 10000;
	} else {
		gradient_sleep = 100;
	}

	switch (capabilities.current_pixel_format) {
	case PIXEL_FORMAT_XRGB_8888:
	case PIXEL_FORMAT_ARGB_8888:
	case PIXEL_FORMAT_ABGR_8888:
	case PIXEL_FORMAT_RGBA_8888:
	case PIXEL_FORMAT_BGRA_8888:
		/* True color space with alpha channel */
		bg_ival = (uint8_t)(CONFIG_SAMPLE_INIT_INTENSITY);
		cg_mval = (uint8_t)(CONFIG_SAMPLE_MAX_INTENSITY);
		fill_buffer_fnc = fill_buffer_argb8888;
		break;
	case PIXEL_FORMAT_RGB_888:
	case PIXEL_FORMAT_BGR_888:
		/* True color space w/o alpha channel */
		bg_ival = (uint8_t)(CONFIG_SAMPLE_INIT_INTENSITY);
		cg_mval = (uint8_t)(CONFIG_SAMPLE_MAX_INTENSITY);
		fill_buffer_fnc = fill_buffer_rgb888;
		break;
	case PIXEL_FORMAT_RGB_565:
	case PIXEL_FORMAT_RGB_565X:
		/* 64k color space (only 32k used with 5bit for green) */
		bg_ival = (uint8_t)(CONFIG_SAMPLE_INIT_INTENSITY);
		cg_mval = (uint8_t)(CONFIG_SAMPLE_MAX_INTENSITY & 0x1Fu);
		fill_buffer_fnc = fill_buffer_rgb565;
		break;
	case PIXEL_FORMAT_AL_88:
		/* 256 grayscale with alpha cahnnel */
		bg_ival = (uint8_t)(CONFIG_SAMPLE_INIT_INTENSITY);
		cg_mval = (uint8_t)(CONFIG_SAMPLE_MAX_INTENSITY);
		fill_buffer_fnc = fill_buffer_al_88;
		break;
	case PIXEL_FORMAT_L_8:
		/* 256 grayscale w/o alpha cahnnel */
		bg_ival = (uint8_t)(CONFIG_SAMPLE_INIT_INTENSITY);
		cg_mval = (uint8_t)(CONFIG_SAMPLE_MAX_INTENSITY);
		fill_buffer_fnc = fill_buffer_l_8;
		break;
	case PIXEL_FORMAT_L_4:
		/* 16 grayscale w/o alpha cahnnel */
		bg_ival = (uint8_t)(CONFIG_SAMPLE_INIT_INTENSITY);
		cg_mval = (uint8_t)(CONFIG_SAMPLE_MAX_INTENSITY & 0x0Fu);
		fill_buffer_fnc = fill_buffer_l_4;
		break;
	case PIXEL_FORMAT_MONO01:
		/* 1 bpp black/white with 0: black, 1: white */
		bg_ival = (uint8_t)(CONFIG_SAMPLE_INIT_INTENSITY);
		cg_mval = (uint8_t)(CONFIG_SAMPLE_MAX_INTENSITY);
		fill_buffer_fnc = fill_buffer_mono;
		break;
	case PIXEL_FORMAT_MONO10:
		/* 1 bpp black/white with 1: black, 0: white */
		bg_ival = (uint8_t)(~(CONFIG_SAMPLE_INIT_INTENSITY));
		cg_mval = (uint8_t)(CONFIG_SAMPLE_MAX_INTENSITY);
		fill_buffer_fnc = fill_buffer_mono;
		break;
	default:
		LOG_ERR("Unsupported pixel format. Aborting sample.");
		ret = -ENOTSUP;
		goto end;
	}

	/* hold only one single line at once in application buffer on heap */
	buf_size = capabilities.x_resolution;

	/* Amount of bytes necessary depends on format - ensure to round up, necessary for
	 * MONO formats
	 */
	buf_size *= DISPLAY_BITS_PER_PIXEL(capabilities.current_pixel_format);
	buf_size = DIV_ROUND_UP(DIV_ROUND_UP(buf_size, NUM_BITS(uint8_t)), sizeof(uint8_t));

	buf = k_aligned_alloc(CONFIG_SAMPLE_BUFFER_ADDR_ALIGN, buf_size);

	if (buf == NULL) {
		LOG_ERR("Could not allocate memory (%zu byte). Aborting sample.", buf_size);
		ret = -ENOMEM;
		goto end;
	}

	LOG_INF("%s: allocated memory: %zu", display->name, buf_size);
	(void)memset(buf, bg_ival, buf_size);

	buf_desc.buf_size = buf_size;
	buf_desc.pitch = capabilities.x_resolution;
	buf_desc.width = capabilities.x_resolution;
	buf_desc.height = 1;
	hlc_max = capabilities.y_resolution - buf_desc.height;

	ret = write_lines_to_display(display, hlc_max, &buf_desc, buf);
	if (ret < 0) {
		LOG_ERR("Failed to write to display (error %d)", ret);
		goto end;
	}

	ret = display_blanking_off(display);
	if (ret < 0 && ret != -ENOSYS) {
		LOG_ERR("Failed to turn blanking off (error %d)", ret);
		goto end;
	}

	LOG_INF("Colorful starts");
	while (1) {
		/* Red -> Green Gradient */
		for (int i = 0; i <= cg_mval; ++i) {
			uint8_t r = cg_mval - i;
			uint8_t g = i;
			uint8_t b = 0;

			fill_buffer_fnc(r, g, b, buf, buf_size, capabilities.current_pixel_format);
			ret = write_lines_to_display(display, hlc_max, &buf_desc, buf);
			if (ret < 0) {
				LOG_ERR("Failed to write to display (error %d)", ret);
				goto end;
			}

			k_msleep(gradient_sleep);
		}

		/* Green -> Blue Gradient */
		for (int i = 0; i <= cg_mval; ++i) {
			uint8_t g = cg_mval - i;
			uint8_t b = i;
			uint8_t r = 0;

			fill_buffer_fnc(r, g, b, buf, buf_size, capabilities.current_pixel_format);
			ret = write_lines_to_display(display, hlc_max, &buf_desc, buf);
			if (ret < 0) {
				LOG_ERR("Failed to write to display (error %d)", ret);
				goto end;
			}

			k_msleep(gradient_sleep);
		}

		/* Blue -> Red Gradient */
		for (int i = 0; i <= cg_mval; ++i) {
			uint8_t b = cg_mval - i;
			uint8_t r = i;
			uint8_t g = 0;

			fill_buffer_fnc(r, g, b, buf, buf_size, capabilities.current_pixel_format);
			ret = write_lines_to_display(display, hlc_max, &buf_desc, buf);
			if (ret < 0) {
				LOG_ERR("Failed to write to display (error %d)", ret);
				goto end;
			}

			k_msleep(gradient_sleep);
		}

		++gradient_count;
#if CONFIG_TEST
		if (gradient_count >= 3) {
			LOG_INF("Colorful sample test mode done %s", display->name);
			break;
		}
#endif
	}

end:
#if CONFIG_TEST
	if (ret == 0) {
		LOG_INF("PROJECT EXECUTION SUCCESSFUL");
	} else {
		LOG_INF("PROJECT EXECUTION FAILED");
	}
#endif
#ifdef CONFIG_ARCH_POSIX
	posix_exit(ret == 0 ? 0 : 1);
#endif
	return 0;
}
