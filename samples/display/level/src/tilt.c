/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <math.h>

#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/sensor.h>
#include <zephyr/logging/log.h>
#include <zephyr/sys/util.h>

#include "tilt.h"

LOG_MODULE_DECLARE(level, CONFIG_LEVEL_LOG_LEVEL);

#if !DT_NODE_EXISTS(DT_ALIAS(accel0))
#error "This sample needs an inertial sensor assigned to the accel0 alias"
#endif

#define IMU_NODE DT_ALIAS(accel0)

/* Below this the acceleration vector is too short to define an attitude,
 * as in free fall. A board at rest reads about ten times this.
 */
#define ACCEL_MIN_MAGNITUDE 1.0f

/**
 * @brief Weight to give each new sample in the low pass filter.
 *
 * Kconfig sets a time constant rather than a raw weight, because a
 * weight only means something in combination with the sampling rate:
 * converting here keeps the smoothing the same if the frame interval
 * is ever changed.
 *
 * For a first order low pass sampled every @c dt, the weight that gives
 * a time constant of @c tau is 1 - e^(-dt/tau).
 */
static float filter_alpha(void)
{
	if (CONFIG_LEVEL_FILTER_TIME_CONSTANT <= 0) {
		/* Filtering disabled: pass every sample through
		 * unchanged.
		 */
		return 1.0f;
	}

	return 1.0f -
	       expf(-(float)CONFIG_LEVEL_FRAME_INTERVAL / (float)CONFIG_LEVEL_FILTER_TIME_CONSTANT);
}

int tilt_init(struct tilt_source *src)
{
	src->dev = DEVICE_DT_GET(IMU_NODE);
	src->alpha = filter_alpha();
	src->primed = false;

	for (size_t i = 0U; i < ARRAY_SIZE(src->filtered); i++) {
		src->filtered[i] = 0.0f;
	}

	if (!device_is_ready(src->dev)) {
		LOG_ERR("Sensor device %s is not ready", src->dev->name);
		return -ENODEV;
	}

	return 0;
}

int tilt_read(struct tilt_source *src, struct tilt *out)
{
	struct sensor_value accel[3];
	float x;
	float y;
	int ret;

	ret = sensor_sample_fetch(src->dev);
	if (ret < 0) {
		LOG_ERR("Failed to fetch a sample from %s (%d)", src->dev->name, ret);
		return ret;
	}

	ret = sensor_channel_get(src->dev, SENSOR_CHAN_ACCEL_XYZ, accel);
	if (ret < 0) {
		LOG_ERR("Failed to read acceleration from %s (%d)", src->dev->name, ret);
		return ret;
	}

	for (size_t i = 0U; i < ARRAY_SIZE(out->accel); i++) {
		const float sample = sensor_value_to_float(&accel[i]);

		if (src->primed) {
			/* Filter the acceleration vector, before
			 * normalisation, so the smoothing behaves the
			 * same at any tilt.
			 */
			src->filtered[i] += src->alpha * (sample - src->filtered[i]);
		} else {
			/* Seed from the first reading, so the bubble starts
			 * where the board is instead of at panel centre.
			 */
			src->filtered[i] = sample;
		}

		out->accel[i] = src->filtered[i];
	}

	src->primed = true;

	out->accel_magnitude =
		sqrtf((out->accel[0] * out->accel[0]) + (out->accel[1] * out->accel[1]) +
		      (out->accel[2] * out->accel[2]));

	/* Map the sensor frame onto the panel frame. The eight combinations
	 * of these three switches cover every way a sensor can be mounted
	 * relative to the display; the right one is measured per board and
	 * defaulted in Kconfig.
	 */
	if (IS_ENABLED(CONFIG_LEVEL_AXIS_SWAP_XY)) {
		x = out->accel[1];
		y = out->accel[0];
	} else {
		x = out->accel[0];
		y = out->accel[1];
	}

	if (IS_ENABLED(CONFIG_LEVEL_AXIS_INVERT_X)) {
		x = -x;
	}

	if (IS_ENABLED(CONFIG_LEVEL_AXIS_INVERT_Y)) {
		y = -y;
	}

	if (out->accel_magnitude < ACCEL_MIN_MAGNITUDE) {
		out->x = 0.0f;
		out->y = 0.0f;
		out->magnitude = 0.0f;
		out->valid = false;

		return 0;
	}

	/* Normalising by the measured vector length, rather than by a fixed
	 * 1 g, turns the components into plain sines of the tilt angle:
	 * bounded to [-1, 1], and valid even while the board is moving.
	 */
	out->x = x / out->accel_magnitude;
	out->y = y / out->accel_magnitude;
	out->magnitude = sqrtf((out->x * out->x) + (out->y * out->y));
	out->valid = true;

	return 0;
}
