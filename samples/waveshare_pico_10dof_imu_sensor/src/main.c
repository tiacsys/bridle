/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/sensor.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(wsptdis_sample, LOG_LEVEL_INF);

static int process_mpu9250(const struct device *dev);
static int process_lps22hb(const struct device *dev);

#if !DT_HAS_COMPAT_STATUS_OKAY(invensense_mpu9250)
#error "No invensense,mpu9250 compatible node found in the device tree"
#endif

#ifdef CONFIG_MPU9250_TRIGGER
static struct sensor_trigger trigger_mpu9250;

static void handle_mpu9250_drdy(const struct device *dev,
				const struct sensor_trigger *trig)
{
	int ret = process_mpu9250(dev);

	if (ret != 0) {
		LOG_ERR("%s: Cancelling trigger due to failure: %d",
			dev->name, ret);
		(void)sensor_trigger_set(dev, trig, NULL);
		return;
	}
}
#endif /* CONFIG_MPU9250_TRIGGER */

/*
 * Get a device structure from a devicetree node with compatible
 * "invensense,mpu9250". (If there are multiple, just pick one.)
 */
static const struct device *get_mpu9250_device(void)
{
	const struct device *dev = DEVICE_DT_GET_ANY(invensense_mpu9250);

	if (dev == NULL) {
		dev = DEVICE_DT_GET_ANY(invensense_mpu9250);
		if (dev == NULL) {
		/* No such node, or the node does not have status "okay". */
			LOG_ERR("MPU9250: no device found.");
			return NULL;
		}
	}

	if (!device_is_ready(dev)) {
		LOG_ERR("MPU9250: Device \"%s\" is not ready; "
			"check the driver initialization logs for errors.",
			dev->name);
		return NULL;
	}

	LOG_INF("MPU9250: Found device \"%s\", getting sensor data",
		dev->name);

#ifdef CONFIG_MPU9250_TRIGGER
	trigger_mpu9250 = (struct sensor_trigger) {
		.type = SENSOR_TRIG_DATA_READY,
		.chan = SENSOR_CHAN_ALL,
	};

	if (sensor_trigger_set(dev, &trigger_mpu9250,
					handle_mpu9250_drdy) < 0) {
		LOG_ERR("MPU9250: Cannot configure trigger for device \"%s\".",
			dev->name);
		return 0;
	}

	LOG_INF("DOF: Configured for triggered sampling.");
#endif /* CONFIG_MPU9250_TRIGGER */

	return dev;
}

#if !DT_HAS_COMPAT_STATUS_OKAY(st_lps22hb_press)
#error "No st,lps22hb-press compatible node found in the device tree"
#endif

/*
 * Get a device structure from a devicetree node with compatible
 * "st,lps22hb-press". (If there are multiple, just pick one.)
 */
static const struct device *get_lps22hb_device(void)
{
	const struct device *const dev = DEVICE_DT_GET_ANY(st_lps22hb_press);

	if (dev == NULL) {
		/* No such node, or the node does not have status "okay". */
		LOG_ERR("LPS22HB: no device found.");
		return NULL;
	}

	if (!device_is_ready(dev)) {
		LOG_ERR("LPS22HB: Device \"%s\" is not ready; "
			"check the driver initialization logs for errors.",
			dev->name);
		return NULL;
	}

	LOG_INF("LPS22HB: Found device \"%s\", getting sensor data",
		dev->name);
	return dev;
}

/*
 * Processing on "invensense,mpu9250" compatible device: fetch, get, print.
 */
static int process_mpu9250(const struct device *dev)
{
	static struct sensor_value accel[3];
	static struct sensor_value gyro[3];
	static struct sensor_value magn[3];
	static struct sensor_value temp;
	int ret;

	ret = sensor_sample_fetch(dev);

	if (ret == 0) {
		ret = sensor_channel_get(dev, SENSOR_CHAN_ACCEL_XYZ, accel);
	}
	if (ret == 0) {
		ret = sensor_channel_get(dev, SENSOR_CHAN_GYRO_XYZ, gyro);
	}
	if (ret == 0) {
		ret = sensor_channel_get(dev, SENSOR_CHAN_MAGN_XYZ, magn);
	}
	if (ret == 0) {
		ret = sensor_channel_get(dev, SENSOR_CHAN_DIE_TEMP, &temp);
	}

	if (ret == 0) {

		LOG_INF("DOF: %f %f %f XYZ-Accel. [m/s/s]",
			sensor_value_to_double(&accel[0]),
			sensor_value_to_double(&accel[1]),
			sensor_value_to_double(&accel[2]));
		LOG_INF("DOF: %f %f %f XYZ-Gyro. [rad/s]",
			sensor_value_to_double(&gyro[0]),
			sensor_value_to_double(&gyro[1]),
			sensor_value_to_double(&gyro[2]));
		LOG_INF("DOF: %f %f %f XYZ-Magn. [uG]",
			sensor_value_to_double(&magn[0]),
			sensor_value_to_double(&magn[1]),
			sensor_value_to_double(&magn[2]));
		LOG_INF("DOF: %.2f Temp. [C]",
			sensor_value_to_double(&temp));

#ifdef CONFIG_MPU9250_TRIGGER
		/* slow down processing and wait too */
		k_sleep(K_SECONDS(2));
#endif

	} else {
		LOG_ERR("%s: Failed to fetch date from DOF device.", dev->name);
	}

	return ret;
}

/*
 * Processing on "st,lps22hb-press" compatible device: fetch, get, print.
 */
static int process_lps22hb(const struct device *dev)
{
	static struct sensor_value airpr;
	static struct sensor_value temp;
	int ret;

	ret = sensor_sample_fetch(dev);

	if (ret == 0) {
		ret = sensor_channel_get(dev, SENSOR_CHAN_PRESS, &airpr);
	}
	if (ret == 0) {
		ret = sensor_channel_get(dev, SENSOR_CHAN_AMBIENT_TEMP, &temp);
	}

	if (ret == 0) {

		LOG_INF("TP: %.2f AirPr. [hPa]",
			sensor_value_to_double(&airpr));
		LOG_INF("TP: %.2f Temp. [C]",
			sensor_value_to_double(&temp));

	} else {
		LOG_ERR("%s: Failed to fetch date from TP device.", dev->name);
	}

	return ret;
}

int main(void)
{
	const struct device *const dof = get_mpu9250_device();
	const struct device *const tp = get_lps22hb_device();

	if ((dof == NULL) | (tp == NULL)) {
		return 0;
	}

	while (true) {

		if (!IS_ENABLED(CONFIG_MPU9250_TRIGGER)) {
			if (process_mpu9250(dof)) {
				LOG_ERR("%s: Failed to process on DOF device.",
					dof->name);
				break;
			}
		}

		if (process_lps22hb(tp)) {
			LOG_ERR("%s: Failed to process on TP device.",
				tp->name);
			break;
		}

		/* slow down polling loop and wait */
		k_sleep(K_SECONDS(2));

	}

	return 0;
}
