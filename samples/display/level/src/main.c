/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <math.h>
#include <stdbool.h>

#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>
#include <zephyr/sys/util.h>

#include "bubble.h"
#include "matrix.h"
#include "tilt.h"

LOG_MODULE_REGISTER(level, CONFIG_LEVEL_LOG_LEVEL);

/** @brief The channel level a fully lit primary colour is drawn at. */
#define LIT ((uint8_t)CONFIG_LEVEL_BRIGHTNESS)

#define RAD_TO_DEG(_rad) ((_rad) * 180.0f / 3.14159265358979f)

/** @brief Render a Kconfig switch as something readable in a log line. */
#define YESNO(_cfg) (IS_ENABLED(_cfg) ? "yes" : "no")

/**
 * @brief Show the corner test image for a moment.
 *
 * Lights the four corners in four colours to reveal where the origin
 * of the panel physically sits, which is needed to judge whether the
 * bubble runs the right way: red top left, green top right, blue
 * bottom right, white bottom left.
 */
static void show_test_image(struct matrix *matrix)
{
	const int right = (int)matrix->width - 1;
	const int bottom = (int)matrix->height - 1;

	if (CONFIG_LEVEL_TEST_IMAGE_MS == 0) {
		return;
	}

	matrix_clear(matrix);

	matrix_set_pixel(matrix, 0, 0, MATRIX_RGB(LIT, 0U, 0U));
	matrix_set_pixel(matrix, right, 0, MATRIX_RGB(0U, LIT, 0U));
	matrix_set_pixel(matrix, right, bottom, MATRIX_RGB(0U, 0U, LIT));
	matrix_set_pixel(matrix, 0, bottom, MATRIX_RGB(LIT, LIT, LIT));

	if (matrix_flush(matrix) == 0) {
		k_sleep(K_MSEC(CONFIG_LEVEL_TEST_IMAGE_MS));
	}
}

/**
 * @brief Report the current attitude and where it puts the bubble.
 *
 * Prints the raw sensor frame, the panel-aligned tilt derived from it,
 * and the pixel that tilt finally lights.
 */
static void log_state(const struct tilt *tilt, const struct bubble *bubble)
{
	/* Rounding can push the magnitude slightly past one, and asinf()
	 * of anything above one is NaN.
	 */
	const float angle = RAD_TO_DEG(asinf(MIN(tilt->magnitude, 1.0f)));

	LOG_INF("accel %7.3f %7.3f %7.3f m/s^2, |a| %6.3f", (double)tilt->accel[0],
		(double)tilt->accel[1], (double)tilt->accel[2], (double)tilt->accel_magnitude);
	LOG_INF("tilt  x %+6.3f y %+6.3f, angle %5.2f deg%s", (double)tilt->x, (double)tilt->y,
		(double)angle, tilt->valid ? "" : ", INVALID");
	LOG_INF("dot   %5.2f, %5.2f, proximity %4.2f%s%s", (double)bubble->x, (double)bubble->y,
		(double)bubble->proximity, bubble->off_scale ? ", off scale" : "",
		bubble->locked ? ", LEVEL" : "");
}

int main(void)
{
	struct tilt_source source;
	struct matrix matrix;
	/* Carries the level latch between frames, so it lives outside the
	 * loop and starts zeroed.
	 */
	struct bubble bubble = {0};
	int64_t next_log = 0;
	int ret;

	ret = matrix_init(&matrix);
	if (ret < 0) {
		return ret;
	}

	ret = tilt_init(&source);
	if (ret < 0) {
		return ret;
	}

	LOG_INF("Level on a %ux%u RGB matrix, %u bytes per pixel, %u ms per frame", matrix.width,
		matrix.height, (unsigned int)matrix.bpp, (unsigned int)CONFIG_LEVEL_FRAME_INTERVAL);
	LOG_INF("Inertial sensor is %s, full scale tilt is %u deg", source.dev->name,
		(unsigned int)CONFIG_LEVEL_FULL_SCALE_TILT);
	LOG_INF("Axis map: swap-xy %s, invert-x %s, invert-y %s", YESNO(CONFIG_LEVEL_AXIS_SWAP_XY),
		YESNO(CONFIG_LEVEL_AXIS_INVERT_X), YESNO(CONFIG_LEVEL_AXIS_INVERT_Y));
	LOG_INF("Filter time constant is %u ms, giving a weight of %.3f per sample",
		(unsigned int)CONFIG_LEVEL_FILTER_TIME_CONSTANT, (double)source.alpha);
	LOG_INF("Colour ramps below %u.%u deg, latches level below %u.%u deg, releases at %u.%u "
		"deg",
		CONFIG_LEVEL_COLOR_RANGE_TILT / 10U, CONFIG_LEVEL_COLOR_RANGE_TILT % 10U,
		CONFIG_LEVEL_LOCK_TILT / 10U, CONFIG_LEVEL_LOCK_TILT % 10U,
		(CONFIG_LEVEL_LOCK_TILT + CONFIG_LEVEL_LOCK_HYSTERESIS) / 10U,
		(CONFIG_LEVEL_LOCK_TILT + CONFIG_LEVEL_LOCK_HYSTERESIS) % 10U);

	show_test_image(&matrix);

	while (true) {
		struct tilt tilt;
		int64_t now;

		ret = tilt_read(&source, &tilt);
		if (ret < 0) {
			return ret;
		}

		bubble_update(&matrix, &tilt, &bubble);

		/* Throttle the log without slowing the sampling. */
		now = k_uptime_get();
		if (now >= next_log) {
			log_state(&tilt, &bubble);
			next_log = now + CONFIG_LEVEL_SENSOR_LOG_INTERVAL;
		}

		matrix_clear(&matrix);
		bubble_render(&matrix, &bubble);

		ret = matrix_flush(&matrix);
		if (ret < 0) {
			return ret;
		}

		k_sleep(K_MSEC(CONFIG_LEVEL_FRAME_INTERVAL));
	}
}
