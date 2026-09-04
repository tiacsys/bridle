/*
 * Copyright (c) 2026 TiaC Systems
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#include <zephyr/device.h>
#include <zephyr/drivers/display.h>
#include <zephyr/drivers/sensor.h>
#include <zephyr/kernel.h>

static const struct device *const sensor = DEVICE_DT_GET(DT_ALIAS(accel0));

const struct device *display_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_display));

static struct display_capabilities capabilities;

static const enum sensor_channel channels[] = {
	SENSOR_CHAN_ACCEL_X,
	SENSOR_CHAN_ACCEL_Y,
};

static int print_dot(uint8_t rgb[3], uint16_t pos[2])
{
	static uint16_t pos_x = UINT16_MAX;
	static uint16_t pos_y = UINT16_MAX;

	struct display_buffer_descriptor buf_desc = {
		.width = 1, .pitch = 1, .height = 1, .buf_size = 4};
	uint8_t pixel[4] = {0};

	/* If position of dot has changed since last call, clear the last position. Do this
	 * manually, as not all displays support dislay_clear. */
	if (pos_x != pos[0] || pos_y != pos[1]) {
		display_write(display_dev, pos_x, pos_y, &buf_desc, pixel);

		pos_x = pos[0];
		pos_y = pos[1];
	}

	pixel[0] = rgb[0];
	pixel[1] = rgb[1];
	pixel[2] = rgb[2];
	pixel[3] = 0xff;

	display_write(display_dev, pos[0], pos[1], &buf_desc, pixel);

	return 0;
}

static int print_frame(const struct device *dev)
{
	int ret;
	struct sensor_value accel[2];

	/* Get and print accel sensor values*/
	ret = sensor_sample_fetch(dev);
	if (ret < 0) {
		printk("%s: sensor_sample_fetch() failed: %d\n", dev->name, ret);
		return ret;
	}

	for (size_t i = 0; i < ARRAY_SIZE(channels); i++) {
		ret = sensor_channel_get(dev, channels[i], &accel[i]);
		if (ret < 0) {
			printk("%s: sensor_channel_get(%c) failed: %d\n", dev->name, 'X' + i, ret);
			return ret;
		}
	}

	printk("%16s [m/s^2]:    (%12.6f, %12.6f,)\n", dev->name, sensor_value_to_double(&accel[0]),
	       sensor_value_to_double(&accel[1]));

	/* Normalize sensor values to range -1 - 1*/
	double x = MAX(-1.0, MIN(1.0, -sensor_value_to_double(&accel[1]) / 10.0));
	double y = MAX(-1.0, MIN(1.0, sensor_value_to_double(&accel[0]) / 10.0));

	/* Calculate dot color*/
	uint8_t brightness_red = ((x + 1.0) / 2.0) * CONFIG_SAMPLE_MAX_BRIGHTNESS;
	uint8_t brightness_green = ((y + 1.0) / 2.0) * CONFIG_SAMPLE_MAX_BRIGHTNESS;
	uint8_t brightness_blue = 0;

	/* Calculate dot position*/
	uint16_t pos_x =
		((capabilities.x_resolution / 2) - 1) + (capabilities.x_resolution / 2) * x;
	uint16_t pos_y =
		((capabilities.y_resolution / 2) - 1) + (capabilities.y_resolution / 2) * y;

	printk("### Brightness (r g b): (%u %u %u)\n", brightness_red, brightness_green,
	       brightness_blue);
	printk("### Position (x y): (%u %u)\n", pos_x, pos_y);

	/* Display dot on screen*/
	uint8_t bgr[] = {brightness_blue, brightness_green, brightness_red};
	uint16_t pos[] = {pos_x, pos_y};

	return print_dot(bgr, pos);
}

/* Taken from accel_polling Zephyr sample. */
static int set_sampling_freq(const struct device *dev)
{
	int ret;
	struct sensor_value odr;

	/* Get display capabilities and store them globally. */
	display_get_capabilities(display_dev, &capabilities);

	ret = sensor_attr_get(dev, SENSOR_CHAN_ACCEL_XYZ, SENSOR_ATTR_SAMPLING_FREQUENCY, &odr);

	/* If we don't get a frequency > 0, we set one */
	if (ret != 0 || (odr.val1 == 0 && odr.val2 == 0)) {
		odr.val1 = 100;
		odr.val2 = 0;

		ret = sensor_attr_set(dev, SENSOR_CHAN_ACCEL_XYZ, SENSOR_ATTR_SAMPLING_FREQUENCY,
				      &odr);

		if (ret != 0) {
			printk("%s : failed to set sampling frequency\n", dev->name);
		}
	}

	return 0;
}

int main(void)
{
	int ret;

	if (!device_is_ready(sensor)) {
		printk("sensor: device %s not ready.\n", sensor->name);
		return 0;
	}
	set_sampling_freq(sensor);

	while (1) {
		ret = print_frame(sensor);
		if (ret < 0) {
			return 0;
		}
		k_msleep(33);
	}
	return 0;
}
