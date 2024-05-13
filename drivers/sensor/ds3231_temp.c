/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT maxim_ds3231_temp

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/pm/device.h>

#include <zephyr/drivers/sensor.h>

#include <zephyr/drivers/mfd/ds3231.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(ds3231_temp, CONFIG_SENSOR_LOG_LEVEL);

struct ds3231_temp_config {
	const struct device *mfd;
};

struct ds3231_temp_data {
	int16_t temp;	/* temperature in 0.01°C */
};

static inline int ds3231_temp_fetch(const struct ds3231_temp_config *config,
				    struct ds3231_temp_data *data)
{
	int ret;
	uint8_t regs[DS3231_TEMP_NUM_REGS];
	int16_t temp;

	ret = mfd_ds3231_reg_read_burst(config->mfd, DS3231_TEMP_MSB,
				regs, sizeof(regs));
	if (ret) {
		LOG_ERR("Could not fetch temperature [%d]", ret);
		return -EIO;
	}

	/*
	 * temp is in two's complement; bit 7 and 6
	 * in the LSB part corresponds to 0.25°C
	 */
	temp  = (regs[DS3231_TEMP_MSB_IDX] & DS3231_TEMP_MSB_BITS) << 8;
	temp |= (regs[DS3231_TEMP_LSB_IDX] & DS3231_TEMP_LSB_BITS);

	/*
	 * shift right by 6 to align data
	 * multiply by 100 to get 0.01
	 * and divide by 4 to get °C
	 */
	data->temp = (temp / 64) * 100 / 4;

	return 0;
}

static int ds3231_temp_sample_fetch(const struct device *dev,
				    enum sensor_channel chan)
{
	const struct ds3231_temp_config * const config = dev->config;
	struct ds3231_temp_data * const data = dev->data;
	int ret;

	switch (chan) {
	case SENSOR_CHAN_ALL:
	case SENSOR_CHAN_AMBIENT_TEMP:
		ret = ds3231_temp_fetch(config, data);
		break;
	default:
		ret = -ENOTSUP;
		break;
	}

	return ret;
}

static int ds3231_temp_channel_get(const struct device *dev,
				   enum sensor_channel chan,
				   struct sensor_value *val)
{
	struct ds3231_temp_data * const data = dev->data;

	switch (chan) {
	case SENSOR_CHAN_AMBIENT_TEMP:
		val->val1 = data->temp / 100;
		val->val2 = (data->temp % 100) * 10000U;
		return 0;
	default:
		return -ENOTSUP;
	}
}

static const struct sensor_driver_api ds3231_temp_driver_api = {
	.sample_fetch = ds3231_temp_sample_fetch,
	.channel_get = ds3231_temp_channel_get,
};

int ds3231_temp_init(const struct device *dev)
{
	const struct ds3231_temp_config * const config = dev->config;

	if (!device_is_ready(config->mfd)) {
		return -ENODEV;
	}

	LOG_DBG("%s: ready with MFD backend over %s!", dev->name,
		config->mfd->name);
	return 0;
}

#ifdef CONFIG_PM_DEVICE
static int ds3231_temp_pm_device_pm_action(const struct device *dev,
					   enum pm_device_action action)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(action);

	return 0;
}
#endif

#if CONFIG_DS3231_TEMP_INIT_PRIORITY <= CONFIG_MFD_DS3231_INIT_PRIORITY
#error DS3231_TEMP_INIT_PRIORITY must be greater than MFD_DS3231_INIT_PRIORITY
#endif

#define DS3231_TEMP_DEFINE(n)                                           \
                                                                        \
	static const struct ds3231_temp_config ds3231_temp_config_##n = { \
		.mfd = DEVICE_DT_GET(DT_INST_PARENT(n)),                \
	};                                                              \
                                                                        \
	static struct ds3231_temp_data ds3231_temp_data_##n;            \
                                                                        \
	PM_DEVICE_DT_INST_DEFINE(n, ds3231_temp_pm_device_pm_action);   \
                                                                        \
	SENSOR_DEVICE_DT_INST_DEFINE(n, ds3231_temp_init,               \
				     PM_DEVICE_DT_INST_GET(n),          \
				     &ds3231_temp_data_##n,             \
				     &ds3231_temp_config_##n,           \
				     POST_KERNEL,                       \
				     CONFIG_DS3231_TEMP_INIT_PRIORITY,  \
				     &ds3231_temp_driver_api);

DT_INST_FOREACH_STATUS_OKAY(DS3231_TEMP_DEFINE)
