/*
 * Copyright (c) 2025 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */
#ifndef ZEPHYR_INCLUDE_DT_BINDINGS_SENSORTEK_STK8BA58_H_
#define ZEPHYR_INCLUDE_DT_BINDINGS_SENSORTEK_STK8BA58_H_

/* power-modes */
#define STK8BA58_DT_POWER_NORMAL	0
#define STK8BA58_DT_LOW_POWER_0ms5	1
#define STK8BA58_DT_LOW_POWER_1ms	2
#define STK8BA58_DT_LOW_POWER_2ms	3
#define STK8BA58_DT_LOW_POWER_4ms	4
#define STK8BA58_DT_LOW_POWER_6ms	5
#define STK8BA58_DT_LOW_POWER_10ms	6
#define STK8BA58_DT_LOW_POWER_25ms	7
#define STK8BA58_DT_LOW_POWER_50ms	8
#define STK8BA58_DT_LOW_POWER_100ms	9
#define STK8BA58_DT_LOW_POWER_500ms	10
#define STK8BA58_DT_LOW_POWER_1000ms	11

/* output data rate */
#define STK8BA58_DT_ODR_OFF		0
#define STK8BA58_DT_ODR_15Hz63		1
#define STK8BA58_DT_ODR_31Hz25		2
#define STK8BA58_DT_ODR_62Hz5		3
#define STK8BA58_DT_ODR_125Hz		4
#define STK8BA58_DT_ODR_250Hz		5
#define STK8BA58_DT_ODR_500Hz		6
#define STK8BA58_DT_ODR_1000Hz		7
#define STK8BA58_DT_ODR_2000Hz		8

#endif /* ZEPHYR_INCLUDE_DT_BINDINGS_SENSORTEK_STK8BA58_H_ */
