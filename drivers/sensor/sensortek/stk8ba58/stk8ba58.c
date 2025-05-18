/*
 * Sensortek Technology STK8BA58 3-axis accelerometer driver
 *
 * Copyright (c) 2025 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief Driver for an STK8BA58 I2C-based 3-axis accelerometer
 */

#define DT_DRV_COMPAT sensortek_stk8ba58

#include <zephyr/drivers/sensor.h>
#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/init.h>
#include <string.h>
#include <zephyr/sys/__assert.h>

#include "stk8ba58.h"

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(STK8BA58, CONFIG_SENSOR_LOG_LEVEL);

/**
 * @brief    3-axis Accelerometer Sensor STK8BA58
 * @defgroup io_sensors_imu_stk8ba58 STK8BA58 3-Axis Accelerometer
 * @ingroup  io_sensors_imu
 * @since    4.1
 * @version  1.0.0
 *
 * The IMU sensor driver for an I2C-based STK8BA58 3-axis accelerometer.
 *
 * @{
 */

static int stk8ba58_get_range(const struct device *dev, uint8_t *range)
{
	const struct stk8ba58_config *cfg = dev->config;
	const struct i2c_dt_spec *i2c = (struct i2c_dt_spec *)&cfg->i2c;
	stk8ba58_range_t val;
	int ret;

	ret = stk8ba58_xl_range_get(i2c, &val);

	switch (val) {
	case STK8BA58_2g:
		*range = 2U;
		break;
	case STK8BA58_4g:
		*range = 4U;
		break;
	case STK8BA58_8g:
		*range = 8U;
		break;
	default:
		LOG_ERR("%s: bad range reg val %d", dev->name, val);
		return -ENOTSUP;
	}

	return ret;
}

static int stk8ba58_set_range(const struct device *dev, uint8_t range)
{
	struct stk8ba58_data *data = dev->data;
	const struct stk8ba58_config *cfg = dev->config;
	const struct i2c_dt_spec *i2c = (struct i2c_dt_spec *)&cfg->i2c;
	int ret;

	switch (range) {
	default:
		range = 2U;
	case 2U:
		ret = stk8ba58_xl_range_set(i2c, STK8BA58_2g);
		data->gain = stk8ba58_from_fs2g_to_mg(1);
		break;
	case 4U:
		ret = stk8ba58_xl_range_set(i2c, STK8BA58_4g);
		data->gain = stk8ba58_from_fs4g_to_mg(1);
		break;
	case 8U:
		ret = stk8ba58_xl_range_set(i2c, STK8BA58_8g);
		data->gain = stk8ba58_from_fs8g_to_mg(1);
		break;
	}

	LOG_DBG("%s: set range to %dg, gain to %0.2f mg/LSB",
		dev->name, range, (double)data->gain);

	return ret;
}

static int stk8ba58_get_odr(const struct device *dev, uint8_t *odr)
{
	const struct stk8ba58_config *cfg = dev->config;
	const struct i2c_dt_spec *i2c = (struct i2c_dt_spec *)&cfg->i2c;
	stk8ba58_bw_t val;
	stk8ba58_ds_t sel;
	int ret;

	ret = stk8ba58_xl_bandwidth_get(i2c, &val, &sel);

	if (sel == STK8BA58_XL_DS_UNFILTERED) {
		*odr = STK8BA58_DT_ODR_OFF;
	} else if (sel == STK8BA58_XL_DS_FILTERED) {
		switch (val) {
		case STK8BA58_XL_BW_7Hz81:
			*odr = STK8BA58_DT_ODR_15Hz63;
			break;
		case STK8BA58_XL_BW_15Hz63:
			*odr = STK8BA58_DT_ODR_31Hz25;
			break;
		case STK8BA58_XL_BW_31Hz25:
			*odr = STK8BA58_DT_ODR_62Hz5;
			break;
		case STK8BA58_XL_BW_62Hz5:
			*odr = STK8BA58_DT_ODR_125Hz;
			break;
		case STK8BA58_XL_BW_125Hz:
			*odr = STK8BA58_DT_ODR_250Hz;
			break;
		case STK8BA58_XL_BW_250Hz:
			*odr = STK8BA58_DT_ODR_500Hz;
			break;
		case STK8BA58_XL_BW_500Hz:
			*odr = STK8BA58_DT_ODR_1000Hz;
			break;
		case STK8BA58_XL_BW_1000Hz:
			*odr = STK8BA58_DT_ODR_2000Hz;
			break;
		default:
		case STK8BA58_XL_BW_PWRUP:
			*odr = STK8BA58_DT_ODR_OFF;
			break;
		}
	} else {
		LOG_ERR("%s: bad odr reg val:sel %d:%d", dev->name, val, sel);
		return -ENOTSUP;
	}

	return ret;
}

static int stk8ba58_set_odr(const struct device *dev, uint8_t odr)
{
	const struct stk8ba58_config *cfg = dev->config;
	const struct i2c_dt_spec *i2c = (struct i2c_dt_spec *)&cfg->i2c;
	stk8ba58_bw_t val;
	stk8ba58_ds_t sel;

	switch (odr) {
	case STK8BA58_DT_ODR_OFF:
		LOG_DBG("%s: set odr to 2 kHz, bw to 1 kHz (unfiltered)", dev->name);
		val = STK8BA58_XL_BW_PWRUP;
		sel = STK8BA58_XL_DS_UNFILTERED;
		break;
	case STK8BA58_DT_ODR_15Hz63:
		LOG_DBG("%s: set odr to 15.63 Hz, bw to 7.81 Hz", dev->name);
		val = STK8BA58_XL_BW_7Hz81;
		sel = STK8BA58_XL_DS_FILTERED;
		break;
	case STK8BA58_DT_ODR_31Hz25:
		LOG_DBG("%s: set odr to 31.25 Hz, bw to 15.63 Hz", dev->name);
		val = STK8BA58_XL_BW_15Hz63;
		sel = STK8BA58_XL_DS_FILTERED;
		break;
	case STK8BA58_DT_ODR_62Hz5:
		LOG_DBG("%s: set odr to 62.50 Hz, bw to 31.25 Hz", dev->name);
		val = STK8BA58_XL_BW_31Hz25;
		sel = STK8BA58_XL_DS_FILTERED;
		break;
	case STK8BA58_DT_ODR_125Hz:
		LOG_DBG("%s: set odr to 125 Hz, bw to 62.50 Hz", dev->name);
		val = STK8BA58_XL_BW_62Hz5;
		sel = STK8BA58_XL_DS_FILTERED;
		break;
	case STK8BA58_DT_ODR_250Hz:
		LOG_DBG("%s: set odr to 250 Hz, bw to 125 Hz", dev->name);
		val = STK8BA58_XL_BW_125Hz;
		sel = STK8BA58_XL_DS_FILTERED;
		break;
	case STK8BA58_DT_ODR_500Hz:
		LOG_DBG("%s: set odr to 500 Hz, bw to 250 Hz", dev->name);
		val = STK8BA58_XL_BW_250Hz;
		sel = STK8BA58_XL_DS_FILTERED;
		break;
	case STK8BA58_DT_ODR_1000Hz:
		LOG_DBG("%s: set odr to 1 kHz, bw to 500 Hz", dev->name);
		val = STK8BA58_XL_BW_500Hz;
		sel = STK8BA58_XL_DS_FILTERED;
		break;
	case STK8BA58_DT_ODR_2000Hz:
		LOG_DBG("%s: set odr to 2 kHz, bw to 1 kHz", dev->name);
		val = STK8BA58_XL_BW_1000Hz;
		sel = STK8BA58_XL_DS_FILTERED;
		break;
	default:
		LOG_ERR("%s: bad odr %d", dev->name, odr);
		return -ENOTSUP;
	}

	return stk8ba58_xl_bandwidth_set(i2c, val, sel);
}

static int stk8ba58_get_pm(const struct device *dev, uint8_t *pm)
{
	const struct stk8ba58_config *cfg = dev->config;
	const struct i2c_dt_spec *i2c = (struct i2c_dt_spec *)&cfg->i2c;
	stk8ba58_sleepdur_t val;
	stk8ba58_pm_t sel;
	int ret;

	ret = stk8ba58_xl_power_mode_get(i2c, &val, &sel);

	if (sel == STK8BA58_XL_PM_NORMAL) {
		*pm = STK8BA58_DT_POWER_NORMAL;
	} else if (sel == STK8BA58_XL_PM_LOWPOWER) {
		switch (val) {
		default:
			*pm = STK8BA58_DT_POWER_NORMAL;
			break;
		case STK8BA58_XL_LP_0ms5:
			*pm = STK8BA58_DT_LOW_POWER_0ms5;
			break;
		case STK8BA58_XL_LP_1ms:
			*pm = STK8BA58_DT_LOW_POWER_1ms;
			break;
		case STK8BA58_XL_LP_2ms:
			*pm = STK8BA58_DT_LOW_POWER_2ms;
			break;
		case STK8BA58_XL_LP_4ms:
			*pm = STK8BA58_DT_LOW_POWER_4ms;
			break;
		case STK8BA58_XL_LP_6ms:
			*pm = STK8BA58_DT_LOW_POWER_6ms;
			break;
		case STK8BA58_XL_LP_10ms:
			*pm = STK8BA58_DT_LOW_POWER_10ms;
			break;
		case STK8BA58_XL_LP_25ms:
			*pm = STK8BA58_DT_LOW_POWER_25ms;
			break;
		case STK8BA58_XL_LP_50ms:
			*pm = STK8BA58_DT_LOW_POWER_50ms;
			break;
		case STK8BA58_XL_LP_100ms:
			*pm = STK8BA58_DT_LOW_POWER_100ms;
			break;
		case STK8BA58_XL_LP_500ms:
			*pm = STK8BA58_DT_LOW_POWER_500ms;
			break;
		case STK8BA58_XL_LP_1000ms:
			*pm = STK8BA58_DT_LOW_POWER_1000ms;
			break;
		}
	} else {
		LOG_ERR("%s: bad odr reg val:sel %d:%d", dev->name, val, sel);
		return -ENOTSUP;
	}

	return ret;
}

static int stk8ba58_set_pm(const struct device *dev, uint8_t pm)
{
	const struct stk8ba58_config *cfg = dev->config;
	const struct i2c_dt_spec *i2c = (struct i2c_dt_spec *)&cfg->i2c;
	stk8ba58_sleepdur_t val;
	stk8ba58_pm_t sel;

	switch (pm) {
	case STK8BA58_DT_POWER_NORMAL:
		LOG_DBG("%s: set pm to normal, no sleep", dev->name);
		val = 0;
		sel = STK8BA58_XL_PM_NORMAL;
		break;
	case STK8BA58_DT_LOW_POWER_0ms5:
		LOG_DBG("%s: set pm to low-power, sleep 0.5ms", dev->name);
		val = STK8BA58_XL_LP_0ms5;
		sel = STK8BA58_XL_PM_LOWPOWER;
		break;
	case STK8BA58_DT_LOW_POWER_1ms:
		LOG_DBG("%s: set pm to low-power, sleep 1ms", dev->name);
		val = STK8BA58_XL_LP_1ms;
		sel = STK8BA58_XL_PM_LOWPOWER;
		break;
	case STK8BA58_DT_LOW_POWER_2ms:
		LOG_DBG("%s: set pm to low-power, sleep 2ms", dev->name);
		val = STK8BA58_XL_LP_2ms;
		sel = STK8BA58_XL_PM_LOWPOWER;
		break;
	case STK8BA58_DT_LOW_POWER_4ms:
		LOG_DBG("%s: set pm to low-power, sleep 4ms", dev->name);
		val = STK8BA58_XL_LP_4ms;
		sel = STK8BA58_XL_PM_LOWPOWER;
		break;
	case STK8BA58_DT_LOW_POWER_6ms:
		LOG_DBG("%s: set pm to low-power, sleep 6ms", dev->name);
		val = STK8BA58_XL_LP_6ms;
		sel = STK8BA58_XL_PM_LOWPOWER;
		break;
	case STK8BA58_DT_LOW_POWER_10ms:
		LOG_DBG("%s: set pm to low-power, sleep 10ms", dev->name);
		val = STK8BA58_XL_LP_10ms;
		sel = STK8BA58_XL_PM_LOWPOWER;
		break;
	case STK8BA58_DT_LOW_POWER_25ms:
		LOG_DBG("%s: set pm to low-power, sleep 25ms", dev->name);
		val = STK8BA58_XL_LP_25ms;
		sel = STK8BA58_XL_PM_LOWPOWER;
		break;
	case STK8BA58_DT_LOW_POWER_50ms:
		LOG_DBG("%s: set pm to low-power, sleep 50ms", dev->name);
		val = STK8BA58_XL_LP_50ms;
		sel = STK8BA58_XL_PM_LOWPOWER;
		break;
	case STK8BA58_DT_LOW_POWER_100ms:
		LOG_DBG("%s: set pm to low-power, sleep 100ms", dev->name);
		val = STK8BA58_XL_LP_100ms;
		sel = STK8BA58_XL_PM_LOWPOWER;
		break;
	case STK8BA58_DT_LOW_POWER_500ms:
		LOG_DBG("%s: set pm to low-power, sleep 500ms", dev->name);
		val = STK8BA58_XL_LP_500ms;
		sel = STK8BA58_XL_PM_LOWPOWER;
		break;
	case STK8BA58_DT_LOW_POWER_1000ms:
		LOG_DBG("%s: set pm to low-power, sleep 1000ms", dev->name);
		val = STK8BA58_XL_LP_1000ms;
		sel = STK8BA58_XL_PM_LOWPOWER;
		break;
	default:
		LOG_ERR("%s: bad pm %d", dev->name, pm);
		return -ENOTSUP;
	}

	return stk8ba58_xl_power_mode_set(i2c, val, sel);
}

static int stk8ba58_accel_getcfg(const struct device *dev,
				 enum sensor_channel chan,
				 enum sensor_attribute attr,
				 struct sensor_value *val)
{
	const struct stk8ba58_config *cfg = dev->config;
	uint8_t range = cfg->range;
	uint8_t odr = cfg->odr;
	uint8_t pm = cfg->pm;
	int ret;

	switch (attr) {
	case SENSOR_ATTR_SAMPLING_FREQUENCY:
		ret = stk8ba58_get_odr(dev, &odr);
		stk8ba58_odr_to_hz(odr, val);
		return ret;
	case SENSOR_ATTR_FULL_SCALE:
		ret = stk8ba58_get_range(dev, &range);
		sensor_g_to_ms2(range, val);
		return ret;
	case SENSOR_ATTR_CONFIGURATION:
		ret = stk8ba58_get_pm(dev, &pm);
		stk8ba58_pm_to_sleep(pm, val);
		return ret;
	default:
		LOG_DBG("Accel attribute not supported.");
		return -ENOTSUP;
	}

	return 0;
}

static int stk8ba58_attr_get(const struct device *dev,
			     enum sensor_channel chan,
			     enum sensor_attribute attr,
			     struct sensor_value *val)
{
	switch (chan) {
	case SENSOR_CHAN_ACCEL_XYZ:
		return stk8ba58_accel_getcfg(dev, chan, attr, val);
	default:
		LOG_WRN("attr_get() not supported on this channel.");
		return -ENOTSUP;
	}

	return 0;
}

static int stk8ba58_accel_setcfg(const struct device *dev,
				 enum sensor_channel chan,
				 enum sensor_attribute attr,
				 const struct sensor_value *val)
{
	switch (attr) {
	case SENSOR_ATTR_SAMPLING_FREQUENCY:
		return stk8ba58_set_odr(dev, stk8ba58_hz_to_odr(val));
	case SENSOR_ATTR_FULL_SCALE:
		return stk8ba58_set_range(dev, sensor_ms2_to_g(val));
	case SENSOR_ATTR_CONFIGURATION:
		return stk8ba58_set_pm(dev, stk8ba58_sleep_to_pm(val));
	default:
		LOG_DBG("Accel attribute not supported.");
		return -ENOTSUP;
	}

	return 0;
}

static int stk8ba58_attr_set(const struct device *dev,
			     enum sensor_channel chan,
			     enum sensor_attribute attr,
			     const struct sensor_value *val)
{
	switch (chan) {
	case SENSOR_CHAN_ACCEL_XYZ:
		return stk8ba58_accel_setcfg(dev, chan, attr, val);
	default:
		LOG_WRN("attr_set() not supported on this channel.");
		return -ENOTSUP;
	}

	return 0;
}

static int stk8ba58_sample_fetch_accel(const struct device *dev)
{
	struct stk8ba58_data *data = dev->data;
	const struct stk8ba58_config *cfg = dev->config;
	const struct i2c_dt_spec *i2c = (struct i2c_dt_spec *)&cfg->i2c;
	int16_t buf[3];

	/* fetch raw data sample */
	if (stk8ba58_acceleration_raw_get(i2c, buf) < 0) {
		LOG_ERR("Failed to fetch raw data sample");
		return -EIO;
	}

	data->sample_x = buf[0];
	data->sample_y = buf[1];
	data->sample_z = buf[2];

	return 0;
}

static int stk8ba58_sample_fetch(const struct device *dev,
				 enum sensor_channel chan)
{
	switch (chan) {
	case SENSOR_CHAN_ACCEL_XYZ:
		stk8ba58_sample_fetch_accel(dev);
		break;
	case SENSOR_CHAN_ALL:
		stk8ba58_sample_fetch_accel(dev);
		break;
	default:
		return -ENOTSUP;
	}

	return 0;
}

static inline void stk8ba58_convert(struct sensor_value *val, int raw_val,
				    float gain)
{
	int64_t dval;

	/* Gain is in mg/LSB */
	/* Convert to m/s^2 */
	dval = ((int64_t)raw_val * gain * SENSOR_G) / 1000;
	val->val1 = dval / 1000000LL;
	val->val2 = dval % 1000000LL;
}

static inline int stk8ba58_get_channel(enum sensor_channel chan,
				       struct sensor_value *val,
				       struct stk8ba58_data *data,
				       float gain)
{
	switch (chan) {
	case SENSOR_CHAN_ACCEL_X:
		stk8ba58_convert(val, data->sample_x, gain);
		break;
	case SENSOR_CHAN_ACCEL_Y:
		stk8ba58_convert(val, data->sample_y, gain);
		break;
	case SENSOR_CHAN_ACCEL_Z:
		stk8ba58_convert(val, data->sample_z, gain);
		break;
	case SENSOR_CHAN_ACCEL_XYZ:
		stk8ba58_convert(val, data->sample_x, gain);
		stk8ba58_convert(val + 1, data->sample_y, gain);
		stk8ba58_convert(val + 2, data->sample_z, gain);
		break;
	default:
		return -ENOTSUP;
	}

	return 0;
}

static int stk8ba58_channel_get(const struct device *dev,
				enum sensor_channel chan,
				struct sensor_value *val)
{
	struct stk8ba58_data *data = dev->data;

	return stk8ba58_get_channel(chan, val, data, data->gain);
}

static DEVICE_API(sensor, stk8ba58_driver_api) = {
	.attr_get = stk8ba58_attr_get,
	.attr_set = stk8ba58_attr_set,
#if defined(CONFIG_STK8BA58_TRIGGER)
	.trigger_set = stk8ba58_trigger_set,
#endif
	.sample_fetch = stk8ba58_sample_fetch,
	.channel_get = stk8ba58_channel_get,
};

static int stk8ba58_init(const struct device *dev)
{
	const struct stk8ba58_config * const cfg = dev->config;
	const struct i2c_dt_spec *i2c = (struct i2c_dt_spec *)&cfg->i2c;
	uint8_t chip_id;
	int ret;

	/* check chip ID */
	ret = stk8ba58_device_id_get(i2c, &chip_id);
	if (ret < 0) {
		LOG_ERR("%s: Not able to read dev id", dev->name);
		return ret;
	}

	if (chip_id != STK8BA58_ID) {
		LOG_ERR("%s: Invalid chip ID 0x%02x", dev->name, chip_id);
		return -EINVAL;
	}

	/* reset device */
	ret = stk8ba58_reset_set(i2c, STK8BA58_RST);
	if (ret < 0) {
		return ret;
	}

	k_busy_wait(100);

	LOG_DBG("%s: chip id 0x%x", dev->name, chip_id);

#ifdef CONFIG_STK8BA58_TRIGGER
	ret = stk8ba58_trigger_init(dev);
	if (ret < 0) {
		LOG_ERR("%s: Failed to initialize triggers", dev->name);
		return ret;
	}
#endif

	/* set sensor default pm and odr */
	LOG_DBG("%s: pm: %d, odr: %d", dev->name, cfg->pm, cfg->odr);
	ret = stk8ba58_set_pm(dev, cfg->pm);
	if (ret < 0) {
		LOG_ERR("%s: pm init error %d", dev->name, cfg->pm);
		return ret;
	}
	ret = stk8ba58_set_odr(dev, cfg->odr);
	if (ret < 0) {
		LOG_ERR("%s: odr init error %d", dev->name, cfg->odr);
		return ret;
	}

	/* set sensor default range */
	LOG_DBG("%s: range is %d", dev->name, cfg->range);
	ret = stk8ba58_set_range(dev, cfg->range);
	if (ret < 0) {
		LOG_ERR("%s: range init error %d", dev->name, cfg->range);
		return ret;
	}

	return 0;
};

#if DT_NUM_INST_STATUS_OKAY(DT_DRV_COMPAT) == 0
#warning "STK8BA58 driver enabled without any devices"
#endif

#define STK8BA58_DEFINE(inst)						\
	static struct stk8ba58_data stk8ba58_data_##inst;		\
	static const struct stk8ba58_config stk8ba58_config_##inst =	\
	{								\
		.i2c = I2C_DT_SPEC_INST_GET(inst),			\
		IF_ENABLED(CONFIG_STK8BA58_TRIGGER,			\
			(.gpio_int = GPIO_DT_SPEC_INST_GET_OR(inst,	\
					irq_gpios, { 0 }),		\
			)						\
		)							\
		.range = DT_INST_PROP(inst, range),			\
		.pm = DT_INST_PROP(inst, power_mode),			\
		.odr = DT_INST_PROP(inst, odr),				\
	};								\
	SENSOR_DEVICE_DT_INST_DEFINE(inst, stk8ba58_init, NULL,		\
			    &stk8ba58_data_##inst,			\
			    &stk8ba58_config_##inst,			\
			    POST_KERNEL, CONFIG_SENSOR_INIT_PRIORITY,	\
			    &stk8ba58_driver_api);

DT_INST_FOREACH_STATUS_OKAY(STK8BA58_DEFINE)

/** @} */
