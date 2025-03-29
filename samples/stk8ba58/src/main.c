/*
 * Copyright (c) 2025 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <stdio.h>
#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/sensor.h>

static void fetch_and_display(const struct device *sensor)
{
	static unsigned int count;
	struct sensor_value accel[3];
	const char *overrun = "";
	int rc = sensor_sample_fetch(sensor);

	++count;
	if (rc == -EBADMSG) {
		/* Sample overrun.  Ignore in polled mode. */
		if (IS_ENABLED(CONFIG_STK8BA58_TRIGGER)) {
			overrun = "[OVERRUN] ";
		}
		rc = 0;
	}
	if (rc == 0) {
		rc = sensor_channel_get(sensor,
					SENSOR_CHAN_ACCEL_XYZ,
					accel);
	}
	if (rc < 0) {
		printf("ERROR: Update failed: %d\n", rc);
	} else {
		printf("#%u @ %u ms: %sx %f , y %f , z %f\n",
		       count, k_uptime_get_32(), overrun,
		       sensor_value_to_double(&accel[0]),
		       sensor_value_to_double(&accel[1]),
		       sensor_value_to_double(&accel[2]));
	}
}

#ifdef CONFIG_STK8BA58_TRIGGER
static void trigger_handler(const struct device *dev,
			    const struct sensor_trigger *trig)
{
	fetch_and_display(dev);
}
#endif

int main(void)
{
	const struct device *const sensor = DEVICE_DT_GET_ANY(sensortek_stk8ba58);
	int rc;

	if (sensor == NULL) {
		printf("No device found\n");
		return 0;
	}
	if (!device_is_ready(sensor)) {
		printf("Device %s is not ready\n", sensor->name);
		return 0;
	}

	struct sensor_value attr_val = {
		.val1 = CONFIG_APPLICATION_RANGE,
		.val2 = 0,
	};

	rc = sensor_attr_set(sensor, SENSOR_CHAN_ACCEL_XYZ,
			     SENSOR_ATTR_FULL_SCALE, &attr_val);
	if (rc != 0) {
		printf("Failed to set range: %d\n", rc);
		return 0;
	}
	printf("Range at %u m/s^2\n", attr_val.val1);

#if CONFIG_STK8BA58_TRIGGER
	{
		struct sensor_trigger trig;

		trig.type = SENSOR_TRIG_DATA_READY;
		trig.chan = SENSOR_CHAN_ACCEL_XYZ;

		attr_val.val1 = CONFIG_APPLICATION_ODR;
		attr_val.val2 = 0;
		rc = sensor_attr_set(sensor, trig.chan,
				     SENSOR_ATTR_SAMPLING_FREQUENCY,
				     &attr_val);
		if (rc != 0) {
			printf("Failed to set odr: %d\n", rc);
			return 0;
		}
		printf("Sampling at %u Hz\n", attr_val.val1);

		sensor_value_from_milli(&attr_val, CONFIG_APPLICATION_LPSLEEP);
		rc = sensor_attr_set(sensor, trig.chan,
				     SENSOR_ATTR_CONFIGURATION,
				     &attr_val);
		if (rc != 0) {
			printf("Failed to set pm: %d\n", rc);
			return 0;
		}
		printf("LP Sleep at %u ms\n", attr_val.val1);

		rc = sensor_trigger_set(sensor, &trig, trigger_handler);
		if (rc != 0) {
			printf("Failed to set trigger: %d\n", rc);
			return 0;
		}

		printf("Waiting for triggers\n");
		while (true) {
			k_sleep(K_MSEC(2000));
		}
	}
#else /* CONFIG_STK8BA58_TRIGGER */
	printf("Polling at 0.5 Hz\n");
	while (true) {
		fetch_and_display(sensor);
		k_sleep(K_MSEC(2000));
	}
#endif /* CONFIG_STK8BA58_TRIGGER */
}
