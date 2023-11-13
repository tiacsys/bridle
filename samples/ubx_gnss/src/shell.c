/*
 * Copyright (c) 2023 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/shell/shell.h>

#include <main.h>

static int cmd_gnss_single(const struct shell *sh, size_t argc, char **argv, void *data) {
	
	if (gnss_device_handle == NULL) {
		shell_print(sh, "Error: GNSS device is not ready");
		return -1;
	}

	int32_t latitudeX1e7 = 0;
	int32_t longitudeX1e7 = 0;
	int32_t altitude_millimeters = 0;
	int32_t radius_millimeters = 0;
	int32_t speed_millimeters_per_second = 0;
	int32_t space_vehicles_used = 0;
	int64_t time_utc = 0;

	int64_t start_time_ms = k_uptime_get();

	int ret = uGnssPosGet(gnss_device_handle, &latitudeX1e7, &longitudeX1e7,
						  &altitude_millimeters, &radius_millimeters, &speed_millimeters_per_second,
						  &space_vehicles_used, &time_utc, NULL);

	int64_t stop_time_ms = k_uptime_get();
	float time_to_fix_seconds = (stop_time_ms - start_time_ms) / 1000.0;

	if (ret != 0) {
		shell_print(sh, "Error during uGnssPosGet: %d", ret);
		return -1;
	}

	float latitude = latitudeX1e7 / 1.e7;
	float longitude = longitudeX1e7 / 1.e7;
	float altitude_meters = altitude_millimeters / 1000.0;
	float radius_meters = radius_millimeters / 1000.0;

	shell_print(sh, "Found position estimate after %.1fs: (lat, lon): (%f, %f), alt: %.2fm, radius: %.2fm (%d SV used)",
		time_to_fix_seconds, latitude, longitude, altitude_meters, radius_meters, space_vehicles_used);

	return 0;
}

SHELL_STATIC_SUBCMD_SET_CREATE(gnss_sub,
	SHELL_CMD(single, NULL, "Get a one-shot position estimate", cmd_gnss_single),
	SHELL_SUBCMD_SET_END
);
SHELL_CMD_REGISTER(gnss, &gnss_sub, "GNSS related commands", NULL);
