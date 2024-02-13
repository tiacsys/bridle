/*
 * Copyright (c) 2023 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/shell/shell.h>
#include <stdlib.h>

#include <main.h>

static void gnss_stream_callback(uDeviceHandle_t device_handle,
				 int32_t error_code,
				 int32_t latitudeX1e7,
				 int32_t longitudeX1e7,
				 int32_t altitude_millimeters,
				 int32_t radius_millimeters,
				 int32_t speed_millimeters_per_second,
				 int32_t space_vehicles_used,
				 int64_t time_utc) {

	if (error_code != 0) {
		return;
	}

	float latitude = latitudeX1e7 / 1.e7;
	float longitude = longitudeX1e7 / 1.e7;
	float altitude_meters = altitude_millimeters / 1000.0;
	float radius_meters = radius_millimeters / 1000.0;

	printk("Found position estimate: (lat, lon): (%f, %f), alt: %.2fm, radius: %.2fm (%d SV used)\n",
		latitude, longitude, altitude_meters, radius_meters, space_vehicles_used);

}

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

	int ret = uGnssPosGet(gnss_device_handle, &latitudeX1e7, &longitudeX1e7, &altitude_millimeters,
						  &radius_millimeters, &speed_millimeters_per_second,
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

static int cmd_gnss_stream_start(const struct shell *sh, size_t argc, char **argv, void *data) {

	if (gnss_device_handle == NULL) {
		shell_print(sh, "Error: GNSS device is not ready");
		return -1;
	}

	uGnssPosGetStreamedStart(gnss_device_handle, 1000, gnss_stream_callback);

	return 0;
}

static int cmd_gnss_stream_stop(const struct shell *sh, size_t argc, char **argv, void *data) {

	if (gnss_device_handle == NULL) {
		shell_print(sh, "Error: GNSS device is not ready");
		return -1;
	}

	uGnssPosGetStreamedStop(gnss_device_handle);

	return 0;
}

static int cmd_gnss_reset(const struct shell *sh, size_t argc, char **argv, void *data) {

	if (gnss_device_handle == NULL) {
		shell_print(sh, "Error: GNSS device is not ready");
		return -1;
	}

	reset_gnss();
	return 0;
}

static int cmd_gnss_ttff(const struct shell *sh, size_t argc, char **argv, void *data) {

	if (gnss_device_handle == NULL) {
		shell_print(sh, "Error: GNSS device is not ready");
		return -1;
	}

	int n_tests = 1;
	if (argc > 1) {
		n_tests = atoi(argv[1]);
	}

	uint64_t durations_total_ms = 0;
	for (int i = 0; i < n_tests; i++) {
		
		reset_gnss();
		uint64_t start_time_ms = k_uptime_get();
		int ret = uGnssPosGet(gnss_device_handle, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
		if (ret != 0) {
			shell_print(sh, "Error during uGnssPosGet: %d", ret);
			return -1;
		}
		
		uint64_t stop_time_ms = k_uptime_get();
		uint64_t duration_ms = stop_time_ms - start_time_ms;
		shell_print(sh, "Run %d of %d: Acquired fix after %.2fs", i+1, n_tests, duration_ms / 1000.0);
		durations_total_ms += duration_ms;
	}

	float duration_avg_seconds = (durations_total_ms / 1000.0) / n_tests;
	shell_print(sh, "---------------");
	shell_print(sh, "Avg. TTFF: %.2f", duration_avg_seconds);

	return 0;
}

SHELL_STATIC_SUBCMD_SET_CREATE(gnss_stream_sub,
	SHELL_CMD(start, NULL, "Start streaming position estimates", cmd_gnss_stream_start),
	SHELL_CMD(stop, NULL, "Stop streaming position estimates", cmd_gnss_stream_stop),
	SHELL_SUBCMD_SET_END
);

SHELL_STATIC_SUBCMD_SET_CREATE(gnss_sub,
	SHELL_CMD(single, NULL, "Get a one-shot position estimate", cmd_gnss_single),
	SHELL_CMD(stream, &gnss_stream_sub, "Start or stop streaming of position estimates", NULL),
	SHELL_CMD(reset, NULL, "Reset GNSS module", cmd_gnss_reset),
	SHELL_CMD(ttff, NULL, "Measure TTFF", cmd_gnss_ttff),
	SHELL_SUBCMD_SET_END
);
SHELL_CMD_REGISTER(gnss, &gnss_sub, "GNSS related commands", NULL);
