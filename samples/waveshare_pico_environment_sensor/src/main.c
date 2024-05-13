/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/sensor.h>

#include <zephyr/drivers/sensor/sgp40.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(wspes_sample, LOG_LEVEL_INF);

#if !DT_HAS_COMPAT_STATUS_OKAY(invensense_icm20948) && \
	!DT_HAS_COMPAT_STATUS_OKAY(invensense_mpu9250)
#error "No invensense,icm20948/mpu9250 compatible node found in the device tree"
#endif

#if defined(CONFIG_ICM20948_TRIGGER) || defined(CONFIG_MPU6050_TRIGGER)
#error "Trigger mode for invensense,icm20948/mpu9250 not supported by hardware"
#endif

/*
 * Get a device structure from a devicetree node with compatible
 * "invensense,icm20948" or "invensense,mpu9250".
 * (If there are multiple, just pick one.)
 */
static const struct device *get_icm20948_device(void)
{
	const struct device *dev = DEVICE_DT_GET_ANY(invensense_icm20948);

	if (dev == NULL) {
		dev = DEVICE_DT_GET_ANY(invensense_mpu9250);
		if (dev == NULL) {
		/* No such node, or the node does not have status "okay". */
			LOG_ERR("ICM20948: no device found.");
			return NULL;
		}
	}

	if (!device_is_ready(dev)) {
		LOG_ERR("ICM20948: Device \"%s\" is not ready; "
			"check the driver initialization logs for errors.",
			dev->name);
		return NULL;
	}

	LOG_INF("ICM20948: Found device \"%s\", getting sensor data",
		dev->name);
	return dev;
}

#if !DT_HAS_COMPAT_STATUS_OKAY(bosch_bme280)
#error "No bosch,bme280 compatible node found in the device tree"
#endif

/*
 * Get a device structure from a devicetree node with compatible
 * "bosch,bme280". (If there are multiple, just pick one.)
 */
static const struct device *get_bme280_device(void)
{
	const struct device *const dev = DEVICE_DT_GET_ANY(bosch_bme280);

	if (dev == NULL) {
		/* No such node, or the node does not have status "okay". */
		LOG_ERR("BME280: no device found.");
		return NULL;
	}

	if (!device_is_ready(dev)) {
		LOG_ERR("BME280: Device \"%s\" is not ready; "
			"check the driver initialization logs for errors.",
			dev->name);
		return NULL;
	}

	LOG_INF("BME280: Found device \"%s\", getting sensor data",
		dev->name);
	return dev;
}

#if !DT_HAS_COMPAT_STATUS_OKAY(sensirion_sgp40)
#error "No sensirion,sgp40 compatible node found in the device tree"
#endif

/*
 * Get a device structure from a devicetree node with compatible
 * "sensirion,sgp40". (If there are multiple, just pick one.)
 */
static const struct device *get_sgp40_device(void)
{
	const struct device *const dev = DEVICE_DT_GET_ANY(sensirion_sgp40);

	if (dev == NULL) {
		/* No such node, or the node does not have status "okay". */
		LOG_ERR("SGP40: no device found.");
		return NULL;
	}

	if (!device_is_ready(dev)) {
		LOG_ERR("SGP40: Device \"%s\" is not ready; "
			"check the driver initialization logs for errors.",
			dev->name);
		return NULL;
	}

	LOG_INF("SGP40: Found device \"%s\", getting sensor data",
		dev->name);
	return dev;
}

int main(void)
{
	const struct device *const dof = get_icm20948_device();
	const struct device *const thp = get_bme280_device();
	const struct device *const voc = get_sgp40_device();
	static struct sensor_value dof_accel[3], dof_gyro[3], dof_magn[3],
				   dof_temp, thp_airpr, thp_temp, thp_rh,
				   voc_gas;

	if ((dof == NULL) | (thp == NULL) | (voc == NULL)) {
		return 0;
	}

	while (true) {

		/* wait first to respect sensors startup time too */
		k_sleep(K_SECONDS(2));

		if (sensor_sample_fetch(dof)) {
			LOG_ERR("%s: Failed to fetch sample from DOF device.",
				dof->name);
			break;
		}

		sensor_channel_get(dof, SENSOR_CHAN_ACCEL_XYZ, dof_accel);
		sensor_channel_get(dof, SENSOR_CHAN_GYRO_XYZ, dof_gyro);
		sensor_channel_get(dof, SENSOR_CHAN_MAGN_XYZ, dof_magn);
		sensor_channel_get(dof, SENSOR_CHAN_DIE_TEMP, &dof_temp);

		if (sensor_sample_fetch(thp)) {
			LOG_ERR("%s: Failed to fetch sample from THP device.",
				thp->name);
			break;
		}

		sensor_channel_get(thp, SENSOR_CHAN_PRESS, &thp_airpr);
		sensor_channel_get(thp, SENSOR_CHAN_AMBIENT_TEMP, &thp_temp);
		sensor_channel_get(thp, SENSOR_CHAN_HUMIDITY, &thp_rh);

#if CONFIG_APP_USE_COMPENSATION
		sensor_attr_set(voc, SENSOR_CHAN_GAS_RES,
				SENSOR_ATTR_SGP40_TEMPERATURE, &thp_temp);
		sensor_attr_set(voc, SENSOR_CHAN_GAS_RES,
				SENSOR_ATTR_SGP40_HUMIDITY, &thp_rh);
#endif

		if (sensor_sample_fetch(voc)) {
			LOG_ERR("%s: Failed to fetch sample from VOC device.",
				voc->name);
			break;
		}

		sensor_channel_get(voc, SENSOR_CHAN_GAS_RES, &voc_gas);

		LOG_INF("DOF: %f %f %f XYZ-Accel. [m/s/s]",
			sensor_value_to_double(&dof_accel[0]),
			sensor_value_to_double(&dof_accel[1]),
			sensor_value_to_double(&dof_accel[2]));
		LOG_INF("DOF: %f %f %f XYZ-Gyro. [rad/s]",
			sensor_value_to_double(&dof_gyro[0]),
			sensor_value_to_double(&dof_gyro[1]),
			sensor_value_to_double(&dof_gyro[2]));
		LOG_INF("DOF: %f %f %f XYZ-Magn. [uG]",
			sensor_value_to_double(&dof_magn[0]),
			sensor_value_to_double(&dof_magn[1]),
			sensor_value_to_double(&dof_magn[2]));
		LOG_INF("DOF: %.2f Temp. [C]",
			sensor_value_to_double(&dof_temp));

		LOG_INF("THP: %.2f AirPr. [hPa]",
			sensor_value_to_double(&thp_airpr));
		LOG_INF("THP: %.2f Temp. [C]",
			sensor_value_to_double(&thp_temp));
		LOG_INF("THP: %.3f RH [%%]",
			sensor_value_to_double(&thp_rh));

		LOG_INF("VOC: %d Gas [a.u.]", voc_gas.val1);

	}

	return 0;
}
