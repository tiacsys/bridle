/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef LEVEL_TILT_H_
#define LEVEL_TILT_H_

#include <stdbool.h>

#include <zephyr/device.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief The attitude of the board, derived from one accelerometer reading.
 *
 * The in-plane components are the sine of the tilt angle projected onto
 * each panel axis, bounded to [-1, 1], and already mapped into the
 * coordinate system of the panel: @c x grows towards the right edge of
 * the display and @c y towards the bottom edge, however the sensor is
 * mounted.
 */
struct tilt {
	/** In-plane component along the panel X axis, as sin of the angle. */
	float x;
	/** In-plane component along the panel Y axis, as sin of the angle. */
	float y;
	/** Length of the in-plane component, equal to sin of the total tilt. */
	float magnitude;
	/**
	 * @brief Smoothed reading in the sensor frame, in m/s².
	 *
	 * This is the filtered vector the rest of the sample runs on, not
	 * the raw sample from the sensor. Set the filter time constant
	 * to zero for the raw reading.
	 */
	float accel[3];
	/** Length of the raw reading, in m/s². Around 9.81 when at rest. */
	float accel_magnitude;
	/**
	 * @brief Whether the in-plane components mean anything.
	 *
	 * Cleared when the acceleration vector is too short to define an
	 * attitude, as in free fall. The components then read zero, which
	 * parks the bubble in the centre.
	 */
	bool valid;
};

/**
 * @brief State of one accelerometer feeding the level.
 *
 * Allocated by the caller, filled in by tilt_init(), and then owned by
 * tilt_read(), which keeps the low pass filter state in here between
 * calls.
 */
struct tilt_source {
	/** The underlying sensor device. */
	const struct device *dev;
	/**
	 * @brief Weight given to each new sample by the low pass filter.
	 *
	 * Derived once from the configured time constant and the frame
	 * interval. A weight of one means no filtering.
	 */
	float alpha;
	/** Smoothed acceleration, in the sensor frame and in m/s². */
	float filtered[3];
	/** Whether @c filtered has been seeded with a first reading yet. */
	bool primed;
};

/**
 * @brief Bind to the accelerometer behind the @c accel0 alias.
 *
 * @param src Destination context, must not be @c NULL.
 *
 * @retval 0 On success.
 * @retval -ENODEV If the sensor device is not ready.
 */
int tilt_init(struct tilt_source *src);

/**
 * @brief Take one reading and reduce it to a panel aligned attitude.
 *
 * @param src Initialised context.
 * @param out Destination attitude, must not be @c NULL.
 *
 * @retval 0 On success, including the case where @p out is not valid.
 * @retval -errno Otherwise, as reported by the sensor driver.
 */
int tilt_read(struct tilt_source *src, struct tilt *out);

#ifdef __cplusplus
}
#endif

#endif /* LEVEL_TILT_H_ */
