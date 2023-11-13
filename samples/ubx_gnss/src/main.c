/*
 * Copyright (c) 2023 Sarah Renkhoff
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/init.h>

#include <main.h>

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
