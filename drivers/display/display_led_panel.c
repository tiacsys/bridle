/*
 * Copyright (c) 2023 TOKITA Hiroshi
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT led_panel

#include <zephyr/drivers/led_strip.h>
#include <zephyr/drivers/display.h>
#include <zephyr/sys/util.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(display_led_panel, CONFIG_DISPLAY_LOG_LEVEL);


struct led_panel_config {
	const struct device *const dev;
	uint16_t height;
	uint16_t width;
	uint16_t module_width;
	uint16_t module_height;
};

struct led_panel_data {
	struct led_rgb *pixels;
};

size_t pixel_index(const struct led_panel_config *config, const uint16_t x, const uint16_t y)
{
	const size_t mod_col = x / config->module_width;
	const size_t mod_row = y / config->module_height;
	const size_t mod_x = x % config->module_width;
	const size_t mod_y = y % config->module_height;
	const size_t mod_pixs = config->module_width * config->module_height;
	const size_t mod_num_in_row = (config->width / config->module_width);
	const size_t offset = (mod_num_in_row * mod_row + mod_col) * mod_pixs;

	return offset + mod_y * config->module_width + mod_x;
}

static int led_panel_write(const struct device *dev, const uint16_t x, const uint16_t y,
			   const struct display_buffer_descriptor *desc, const void *buf)
{
	const struct led_panel_config *config = dev->config;
	struct led_panel_data *data = dev->data;
	const uint32_t *u32buf = buf;
	int rc;

	__ASSERT(desc->width <= desc->pitch, "Pitch is smaller then width");
	__ASSERT(desc->pitch <= config->width, "Pitch in descriptor is larger than screen size");
	__ASSERT(desc->height <= config->height, "Height in descriptor is larger than screen size");
	__ASSERT(x + desc->pitch <= config->width,
		 "Writing outside screen boundaries in horizontal direction");
	__ASSERT(y + desc->height <= config->height,
		 "Writing outside screen boundaries in vertical direction");

	if (desc->width > desc->pitch || x + desc->pitch > config->width ||
	    y + desc->height > config->height) {
		return -EINVAL;
	}

	for (size_t ypos = y; ypos < (y + desc->height); ypos++) {
		for (size_t xpos = x; xpos < (x + desc->width); xpos++) {
			uint32_t color = *u32buf++;
			size_t idx = pixel_index(config, xpos, ypos);
			struct led_rgb *pix = &data->pixels[idx];

			pix->r = ((color >> 16) & 0xFF);
			pix->g = ((color >> 8) & 0xFF);
			pix->b = ((color) & 0xFF);
		}
		u32buf += (desc->pitch - desc->width);
	}

	rc = led_strip_update_rgb(config->dev, data->pixels, config->width * config->height);
	if (rc) {
		LOG_ERR("couldn't update strip: %d", rc);
	}

	return rc;
}

static int led_panel_read(const struct device *dev, const uint16_t x, const uint16_t y,
			  const struct display_buffer_descriptor *desc, void *buf)
{
	return -ENOTSUP;
}

static void *led_panel_get_framebuffer(const struct device *dev)
{
	return NULL;
}

static int led_panel_blanking_off(const struct device *dev)
{
	return -ENOTSUP;
}

static int led_panel_blanking_on(const struct device *dev)
{
	return -ENOTSUP;
}

static int led_panel_set_brightness(const struct device *dev, const uint8_t brightness)
{
	return -ENOTSUP;
}

static int led_panel_set_contrast(const struct device *dev, const uint8_t contrast)
{
	return -ENOTSUP;
}

static void led_panel_get_capabilities(const struct device *dev,
				       struct display_capabilities *capabilities)
{
	const struct led_panel_config *config = dev->config;

	memset(capabilities, 0, sizeof(struct display_capabilities));
	capabilities->x_resolution = config->width;
	capabilities->y_resolution = config->height;
	capabilities->supported_pixel_formats = PIXEL_FORMAT_ARGB_8888;
	capabilities->current_pixel_format = PIXEL_FORMAT_ARGB_8888;
	capabilities->screen_info = 0;
}

static int led_panel_set_pixel_format(const struct device *dev,
				      const enum display_pixel_format pixel_format)
{
	return -ENOTSUP;
}

static const struct display_driver_api led_panel_api = {
	.blanking_on = led_panel_blanking_on,
	.blanking_off = led_panel_blanking_off,
	.write = led_panel_write,
	.read = led_panel_read,
	.get_framebuffer = led_panel_get_framebuffer,
	.set_brightness = led_panel_set_brightness,
	.set_contrast = led_panel_set_contrast,
	.get_capabilities = led_panel_get_capabilities,
	.set_pixel_format = led_panel_set_pixel_format,
};

static int led_panel_init(const struct device *dev)
{
	const struct led_panel_config *config = dev->config;

	if (!device_is_ready(config->dev)) {
		LOG_ERR("LED strip device %s is not ready", config->dev->name);
		return -EINVAL;
	}

	return 0;
}

#define LED_PANEL_DEFINE(n)                                                                        \
	static const struct led_panel_config dd_config_##n = {                                     \
		.dev = DEVICE_DT_GET(DT_INST_PHANDLE(n, led_strip)),                               \
		.height = DT_INST_PROP(n, height),                                                 \
		.width = DT_INST_PROP(n, width),                                                   \
		.module_width = DT_INST_PROP(n, module_width),                                     \
		.module_height = DT_INST_PROP(n, module_height),                                   \
	};                                                                                         \
	struct led_rgb pixels##n[DT_INST_PROP(n, height) * DT_INST_PROP(n, width)];                \
                                                                                                   \
	static struct led_panel_data dd_data_##n = {                                               \
		.pixels = pixels##n,                                                               \
	};                                                                                         \
	DEVICE_DT_INST_DEFINE(n, led_panel_init, NULL, &dd_data_##n, &dd_config_##n, POST_KERNEL,  \
			      CONFIG_DISPLAY_INIT_PRIORITY, &led_panel_api);

DT_INST_FOREACH_STATUS_OKAY(LED_PANEL_DEFINE)
