/*
 * Copyright (c) 2023 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef MAIN_H
#define MAIN_H

/* ubxlib specific includes */
#include <ubxlib.h>
#include <u_cfg_app_platform_specific.h>

extern uDeviceHandle_t gnss_device_handle;

void reset_gnss(void);

#endif /* MAIN_H */
