/*
 * Sensortek Technology STK8BA58 3-axis accelerometer driver
 *
 * Copyright (c) 2025 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief Driver Interface for an STK8BA58 I2C-based 3-axis accelerometer
 */

#ifndef ZEPHYR_DRIVERS_SENSOR_SENSORTEK_STK8BA58_H_
#define ZEPHYR_DRIVERS_SENSOR_SENSORTEK_STK8BA58_H_

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @ingroup io_sensors_imu_stk8ba58
 * @{
 */

#include <zephyr/types.h>
#include <zephyr/drivers/sensor.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/i2c.h>

#include <zephyr/dt-bindings/sensor/stk8ba58.h>
#include "stk8ba58_reg.h"

struct stk8ba58_config {
	const struct i2c_dt_spec i2c;
	uint8_t range;
	uint8_t odr;
	uint8_t pm;
#ifdef CONFIG_STK8BA58_TRIGGER
	struct gpio_dt_spec gpio_int;
#endif
};

/* Return ODR value based on data rate set in Hz. */
static inline uint8_t stk8ba58_hz_to_odr(const struct sensor_value *val)
{
	if (val->val1 >= 2000U) {
		return STK8BA58_DT_ODR_2000Hz;
	} else if (val->val1 >= 1000U) {
		return STK8BA58_DT_ODR_1000Hz;
	} else if (val->val1 >= 500U) {
		return STK8BA58_DT_ODR_500Hz;
	} else if (val->val1 >= 250U) {
		return STK8BA58_DT_ODR_250Hz;
	} else if (val->val1 >= 125U) {
		return STK8BA58_DT_ODR_125Hz;
	} else if (val->val1 >= 62U) {
		return STK8BA58_DT_ODR_62Hz5;
	} else if (val->val1 >= 31U) {
		return STK8BA58_DT_ODR_31Hz25;
	} else if (val->val1 >= 15U) {
		return STK8BA58_DT_ODR_15Hz63;
	} else {
		return STK8BA58_DT_ODR_OFF;
	}
}

static inline void stk8ba58_odr_to_hz(uint8_t odr, struct sensor_value *val)
{
	val->val1 = 0U;
	val->val2 = 0U;
	switch (odr) {
	case STK8BA58_DT_ODR_2000Hz:
		val->val1 = 2000U;
		break;
	case STK8BA58_DT_ODR_1000Hz:
		val->val1 = 1000U;
		break;
	case STK8BA58_DT_ODR_500Hz:
		val->val1 = 500U;
		break;
	case STK8BA58_DT_ODR_250Hz:
		val->val1 = 250U;
		break;
	case STK8BA58_DT_ODR_125Hz:
		val->val1 = 125U;
		break;
	case STK8BA58_DT_ODR_62Hz5:
		sensor_value_from_milli(val, 62500U);
		break;
	case STK8BA58_DT_ODR_31Hz25:
		sensor_value_from_milli(val, 31250U);
		break;
	case STK8BA58_DT_ODR_15Hz63:
		sensor_value_from_milli(val, 15630U);
		break;
	case STK8BA58_DT_ODR_OFF:
		break;
	}
}

/* Return power mode value based on sleep set in ms. */
static inline uint8_t stk8ba58_sleep_to_pm(const struct sensor_value *val)
{
	if (val->val1 >= 1000U) {
		return STK8BA58_DT_LOW_POWER_1000ms;
	} else if (val->val1 >= 500U) {
		return STK8BA58_DT_LOW_POWER_500ms;
	} else if (val->val1 >= 100U) {
		return STK8BA58_DT_LOW_POWER_100ms;
	} else if (val->val1 >= 50U) {
		return STK8BA58_DT_LOW_POWER_50ms;
	} else if (val->val1 >= 25U) {
		return STK8BA58_DT_LOW_POWER_25ms;
	} else if (val->val1 >= 10U) {
		return STK8BA58_DT_LOW_POWER_10ms;
	} else if (val->val1 >= 6U) {
		return STK8BA58_DT_LOW_POWER_6ms;
	} else if (val->val1 >= 4U) {
		return STK8BA58_DT_LOW_POWER_4ms;
	} else if (val->val1 >= 2U) {
		return STK8BA58_DT_LOW_POWER_2ms;
	} else if (val->val1 >= 1U) {
		return STK8BA58_DT_LOW_POWER_1ms;
	} else if ((val->val1 == 0U) && (val->val2 >= 0U)) {
		return STK8BA58_DT_LOW_POWER_0ms5;
	} else {
		return STK8BA58_DT_POWER_NORMAL;
	}
}

static inline void stk8ba58_pm_to_sleep(uint8_t odr, struct sensor_value *val)
{
	val->val1 = 0U;
	val->val2 = 0U;
	switch (odr) {
	case STK8BA58_DT_LOW_POWER_1000ms:
		val->val1 = 1000U;
		break;
	case STK8BA58_DT_LOW_POWER_500ms:
		val->val1 = 500U;
		break;
	case STK8BA58_DT_LOW_POWER_100ms:
		val->val1 = 100U;
		break;
	case STK8BA58_DT_LOW_POWER_50ms:
		val->val1 = 50U;
		break;
	case STK8BA58_DT_LOW_POWER_25ms:
		val->val1 = 25U;
		break;
	case STK8BA58_DT_LOW_POWER_10ms:
		val->val1 = 10U;
		break;
	case STK8BA58_DT_LOW_POWER_6ms:
		val->val1 = 6U;
		break;
	case STK8BA58_DT_LOW_POWER_4ms:
		val->val1 = 4U;
		break;
	case STK8BA58_DT_LOW_POWER_2ms:
		val->val1 = 2U;
		break;
	case STK8BA58_DT_LOW_POWER_1ms:
		val->val1 = 1U;
		break;
	case STK8BA58_DT_LOW_POWER_0ms5:
		sensor_value_from_milli(val, 500U);
		break;
	case STK8BA58_DT_POWER_NORMAL:
		break;
	}
}

struct stk8ba58_data {
	int sample_x;
	int sample_y;
	int sample_z;
	float gain;

#ifdef CONFIG_STK8BA58_TRIGGER
	struct gpio_callback gpio_cb;

	const struct sensor_trigger *data_ready_trigger;
	sensor_trigger_handler_t data_ready_handler;
	const struct device *dev;

#if defined(CONFIG_STK8BA58_TRIGGER_OWN_THREAD)
	K_KERNEL_STACK_MEMBER(thread_stack, CONFIG_STK8BA58_THREAD_STACK_SIZE);
	struct k_thread thread;
	struct k_sem trig_sem;
#elif defined(CONFIG_STK8BA58_TRIGGER_GLOBAL_THREAD)
	struct k_work work;
#endif

#endif /* CONFIG_STK8BA58_TRIGGER */
};

#ifdef CONFIG_STK8BA58_TRIGGER
int stk8ba58_trigger_set(const struct device *dev,
			 const struct sensor_trigger *trig,
			 sensor_trigger_handler_t handler);

int stk8ba58_trigger_init(const struct device *dev);
#endif

/** @} */

#ifdef __cplusplus
}
#endif

#endif /* ZEPHYR_DRIVERS_SENSOR_SENSORTEK_STK8BA58_H_ */
