/*
 * Copyright (c) 2023 Sarah Renkhoff
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/init.h>
#include <zephyr/shell/shell.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(main, CONFIG_MAIN_LOG_LEVEL);

#include <ubxlib.h>
#include <u_cfg_app_platform_specific.h>

static const uDeviceCfg_t device_config = {
	.deviceType = U_DEVICE_TYPE_GNSS,
	.deviceCfg = {
		.cfgGnss = {
			.moduleType = U_GNSS_MODULE_TYPE_M10,
			.pinEnablePower = -1,
			.pinDataReady = -1,
		},
	},
	.transportType = U_DEVICE_TRANSPORT_TYPE_UART,
	.transportCfg = {
		.cfgUart = {
			.uart = 0,
			.baudRate = U_GNSS_UART_BAUD_RATE,
			.pinTxd = -1,
			.pinRxd = -1,
			.pinCts = -1,
			.pinRts = -1,
		}
	},
};

uDeviceHandle_t gnss_device_handle = NULL;

static int init(void) {

	uPortInit();
	uDeviceInit();

	return 0;
}
SYS_INIT(init, APPLICATION, 90);

static int cmd_pos_single(const struct shell *sh, size_t argc, char **argv, void *data) {
	
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
	SHELL_CMD(single, NULL, "Get a one-shot position estimate", cmd_pos_single),
	SHELL_SUBCMD_SET_END
);
SHELL_CMD_REGISTER(gnss, &gnss_sub, "GNSS related commands", NULL);

int main(void) {

	int ret = uDeviceOpen(&device_config, &gnss_device_handle);

	if (ret != 0) {
		LOG_ERR("Error during uDeviceOpen: %d", ret);
		return 0;
	}

	LOG_INF("GNSS Device is ready!");

	while(true) {
		k_msleep(1000);
	}

	return 0;
}
