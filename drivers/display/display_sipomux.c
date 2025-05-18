/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief Driver of the SIPO/MUX Display controller
 */

#define DT_DRV_COMPAT sipo_mux_display

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/pm/device.h>

#include <zephyr/drivers/display.h>

#include <zephyr/drivers/mfd/sipomuxgp.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(display_sipomux, CONFIG_DISPLAY_LOG_LEVEL);

/**
 * @brief    Generic latched SIPO/MUX Display controller
 * @defgroup io_display_sipomux SIPO/MUX Display
 * @ingroup  io_display
 * @since    3.6
 * @version  1.0.0
 *
 * The generic latched SIPO/MUX display controller based on the MFD interface
 * to the generic latched SIPO/MUX General Purpose (GP) matrix controller.
 *
 * @par SIPO/MUX:
 * Serial Input Parallel Output / Multiplexing hardware
 *
 * @{
 */

typedef struct display_sipomux_cfg {
	const uint16_t height;
	const uint16_t width;
	const uint16_t gap_front;
	const uint16_t gap_top;
	const bool inversion_on;
	const struct device *mfd;
} display_sipomux_cfg_t;

typedef struct display_sipomux_data {
	enum display_pixel_format current_pixel_format;
} display_sipomux_data_t;

static inline int display_sipomux_set(const struct device *dev, unsigned int set,
				      const size_t x, const size_t y)
{
	const display_sipomux_cfg_t * const config = dev->config;
	size_t xpos = config->gap_front + x;
	size_t ypos = config->gap_top + y;

	set = config->inversion_on ? ~set : set;

	if (set) {
		return mfd_sipomuxgp_xy_on(config->mfd, xpos, ypos);
	} else {
		return mfd_sipomuxgp_xy_off(config->mfd, xpos, ypos);
	}
}

static int display_sipomux_write(const struct device *dev,
				 const uint16_t x, const uint16_t y,
				 const struct display_buffer_descriptor *desc,
				 const void *buf)
{
	const display_sipomux_cfg_t * const config = dev->config;
	uint8_t *byte = (uint8_t *)buf;
	size_t bit = 0;
	int ret = 0;

	__ASSERT(desc->width <= desc->pitch, "Pitch is smaller then width");
	__ASSERT(desc->pitch <= config->width,
		"Pitch in descriptor is larger than screen size");
	__ASSERT(desc->height <= config->height,
		"Height in descriptor is larger than screen size");
	__ASSERT(x + desc->pitch <= config->width,
		 "Writing outside screen boundaries in horizontal direction");
	__ASSERT(y + desc->height <= config->height,
		 "Writing outside screen boundaries in vertical direction");

	if (desc->width > desc->pitch ||
	    x + desc->pitch > config->width ||
	    y + desc->height > config->height) {
		LOG_ERR("%s: writing outside screen boundaries", dev->name);
		return -EINVAL;
	}

	if (desc->height * desc->width > desc->buf_size * NUM_BITS(uint8_t)) {
		LOG_ERR("%s: not enough data, buffer too small", dev->name);
		return -EINVAL;
	}

	for (size_t ypos = y; ypos < (y + desc->height); ypos++) {
		for (size_t xpos = x; xpos < (x + desc->width); xpos++) {

			if (*byte & BIT(NUM_BITS(uint8_t) - bit - 1)) {
				ret = display_sipomux_set(dev, ~0, xpos, ypos);
			} else {
				ret = display_sipomux_set(dev, 0, xpos, ypos);
			}

			if (ret != 0U) {
				return ret;
			}

			if (!(++bit % NUM_BITS(uint8_t))) {
				bit = 0;
				byte++;
			}
		}
	}

	return 0;
}

static int display_sipomux_read(const struct device *dev,
				const uint16_t x, const uint16_t y,
				const struct display_buffer_descriptor *desc,
				void *buf)
{
	LOG_DBG("%s: READ not supported", dev->name);
	return -ENOTSUP;
}

static void *display_sipomux_get_framebuffer(const struct device *dev)
{
	LOG_DBG("%s: DIRECT FB ADDR not supported", dev->name);
	return NULL;
}

static int display_sipomux_blanking_off(const struct device *dev)
{
	const display_sipomux_cfg_t * const config = dev->config;

	return mfd_sipomuxgp_output_ratio(config->mfd, 100);
}

static int display_sipomux_blanking_on(const struct device *dev)
{
	const display_sipomux_cfg_t * const config = dev->config;

	return mfd_sipomuxgp_output_ratio(config->mfd, 0);
}

static int display_sipomux_set_brightness(const struct device *dev,
					  const uint8_t brightness)
{
	const display_sipomux_cfg_t * const config = dev->config;

	return mfd_sipomuxgp_output_ratio(config->mfd, brightness);
}

static int display_sipomux_set_contrast(const struct device *dev,
					const uint8_t contrast)
{
	LOG_DBG("%s: CONTRAST not supported", dev->name);
	return 0;
}

static void display_sipomux_get_capabilities(const struct device *dev,
		struct display_capabilities *capabilities)
{
	const display_sipomux_cfg_t * const config = dev->config;
	display_sipomux_data_t * const data = dev->data;

	memset(capabilities, 0, sizeof(struct display_capabilities));
	capabilities->x_resolution = config->width;
	capabilities->y_resolution = config->height;
	capabilities->supported_pixel_formats = PIXEL_FORMAT_MONO01;
	capabilities->current_pixel_format = data->current_pixel_format;
	capabilities->screen_info = SCREEN_INFO_MONO_VTILED |
				    SCREEN_INFO_MONO_MSB_FIRST;
}

static int display_sipomux_set_pixel_format(const struct device *dev,
		const enum display_pixel_format pixel_format)
{
	display_sipomux_data_t * const data = dev->data;

	if (pixel_format != PIXEL_FORMAT_MONO01) {
		LOG_ERR("%s: unsupported pixel format", dev->name);
		return -EINVAL;
	}

	data->current_pixel_format = pixel_format;

	return 0;
}

static const struct display_driver_api display_sipomux_api = {
	.blanking_on = display_sipomux_blanking_on,
	.blanking_off = display_sipomux_blanking_off,
	.write = display_sipomux_write,
	.read = display_sipomux_read,
	.get_framebuffer = display_sipomux_get_framebuffer,
	.set_brightness = display_sipomux_set_brightness,
	.set_contrast = display_sipomux_set_contrast,
	.get_capabilities = display_sipomux_get_capabilities,
	.set_pixel_format = display_sipomux_set_pixel_format,
};

static int display_sipomux_init(const struct device *dev)
{
	const display_sipomux_cfg_t * const config = dev->config;
	display_sipomux_data_t * const data = dev->data;
	uint16_t av_pixel, rq_pixel;

	if (!device_is_ready(config->mfd)) {
		return -ENODEV;
	}

	rq_pixel = (config->gap_front + config->width)
		 * (config->gap_top + config->height);
	av_pixel = mfd_sipomuxgp_num_bits(config->mfd);

	if (rq_pixel > av_pixel) {
		LOG_ERR("%s: invalid number of requested pixel: %u > %u",
			dev->name, rq_pixel, av_pixel);
		return -EINVAL;
	}

	data->current_pixel_format = PIXEL_FORMAT_MONO01;

	LOG_DBG("%s: ready for %u x %u (+%u:+%u) with MFD backend over %s!",
		dev->name, config->width, config->height, config->gap_front,
		config->gap_top, config->mfd->name);
	return 0;
}

#ifdef CONFIG_PM_DEVICE
static int display_sipomux_pm_device_pm_action(const struct device *dev,
					       enum pm_device_action action)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(action);

	return 0;
}
#endif

#if CONFIG_DISPLAY_SIPOMUX_INIT_PRIORITY <= CONFIG_MFD_SIPOMUXGP_INIT_PRIORITY
#error DISPLAY_SIPOMUX_INIT_PRIORITY must be greater than MFD_SIPOMUXGP_INIT_PRIORITY
#endif

#define DISPLAY_SIPOMUX_DEFINE(n)                                       \
	static const display_sipomux_cfg_t display_sipomux_cfg_##n = {  \
		.height = DT_INST_PROP(n, height),                      \
		.width = DT_INST_PROP(n, width),                        \
		.gap_front = DT_INST_PROP_BY_IDX(n, offset, 0),         \
		.gap_top = DT_INST_PROP_BY_IDX(n, offset, 1),           \
		.inversion_on = DT_INST_PROP(n, inversion_on),          \
		.mfd = DEVICE_DT_GET(DT_INST_PARENT(n)),                \
	};                                                              \
                                                                        \
	static display_sipomux_data_t display_sipomux_data_##n;         \
                                                                        \
	PM_DEVICE_DT_INST_DEFINE(n, display_sipomux_pm_device_pm_action);\
                                                                        \
	DEVICE_DT_INST_DEFINE(n, display_sipomux_init, NULL,            \
			      &display_sipomux_data_##n,                \
			      &display_sipomux_cfg_##n,                 \
			      POST_KERNEL,                              \
			      CONFIG_DISPLAY_SIPOMUX_INIT_PRIORITY,     \
			      &display_sipomux_api);

DT_INST_FOREACH_STATUS_OKAY(DISPLAY_SIPOMUX_DEFINE)

/** @} */
