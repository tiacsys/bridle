/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT maxim_ds3231_rtc

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/pm/device.h>

#include <zephyr/drivers/rtc.h>

#include <zephyr/drivers/mfd/ds3231.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(rtc_ds3231, CONFIG_RTC_LOG_LEVEL);

struct rtc_ds3231_config {
	const struct device *mfd;
};

struct rtc_ds3231_data {
	struct k_spinlock lock;
};

static int rtc_ds3231_set_time(const struct device *dev,
			       const struct rtc_time *tm)
{
	const struct rtc_ds3231_config * const config = dev->config;
	struct rtc_ds3231_data * const data = dev->data;
	k_spinlock_key_t key;
	uint8_t regs[DS3231_CAL_NUM_REGS];
	int ret;

	key = k_spin_lock(&data->lock);

	LOG_DBG("%s: set time: year = %d, mon = %d, mday = %d, wday = %d, "
		"hour = %d, min = %d, sec = %d", dev->name,
		tm->tm_year, tm->tm_mon, tm->tm_mday, tm->tm_wday,
		tm->tm_hour, tm->tm_min, tm->tm_sec);

	regs[DS3231_SECONDS] = bin2bcd(tm->tm_sec) & DS3231_SECONDS_BITS;
	regs[DS3231_MINUTES] = bin2bcd(tm->tm_min);
	regs[DS3231_HOURS] = bin2bcd(tm->tm_hour);
	regs[DS3231_DAY] = bin2bcd(tm->tm_wday);
	regs[DS3231_DATE] = bin2bcd(tm->tm_mday);
	regs[DS3231_MONTH] = bin2bcd(tm->tm_mon);
	regs[DS3231_YEAR] = bin2bcd((tm->tm_year % 100));

	ret = mfd_ds3231_reg_write_burst(config->mfd, DS3231_SECONDS,
					 regs, sizeof(regs));

	k_spin_unlock(&data->lock, key);

	return ret;
}

static int rtc_ds3231_get_time(const struct device *dev, struct rtc_time *tm)
{

	const struct rtc_ds3231_config * const config = dev->config;
	struct rtc_ds3231_data * const data = dev->data;
	k_spinlock_key_t key;
	uint8_t regs[DS3231_CAL_NUM_REGS];
	int ret;

	key = k_spin_lock(&data->lock);

	ret = mfd_ds3231_reg_read_burst(config->mfd, DS3231_SECONDS,
					regs, sizeof(regs));
	if (ret != 0) {
		goto unlock;
	}

	tm->tm_sec = bcd2bin(regs[DS3231_SECONDS] & DS3231_SECONDS_BITS);
	tm->tm_min = bcd2bin(regs[DS3231_MINUTES] & DS3231_MINUTES_BITS);
	tm->tm_hour = bcd2bin(regs[DS3231_HOURS] & DS3231_HOURS_BITS); /* 24hr mode */
	tm->tm_wday = bcd2bin(regs[DS3231_DAY] & DS3231_DAY_BITS);
	tm->tm_mday = bcd2bin(regs[DS3231_DATE] & DS3231_DATE_BITS);
	tm->tm_mon = bcd2bin(regs[DS3231_MONTH] & DS3231_MONTHS_BITS);
	tm->tm_year = bcd2bin(regs[DS3231_YEAR] & DS3231_YEAR_BITS);
	tm->tm_year = tm->tm_year + 100;

	/* Not used */
	tm->tm_nsec = 0;
	tm->tm_isdst = -1;
	tm->tm_yday = -1;

	/* Validate the chip in 24hr mode */
	if (regs[DS3231_HOURS] & DS3231_VALIDATE_24HR) {
		ret = -ENODATA;
		goto unlock;
	}

	LOG_DBG("%s: get time: year = %d, mon = %d, mday = %d, wday = %d, "
		"hour = %d, min = %d, sec = %d", dev->name,
		tm->tm_year, tm->tm_mon, tm->tm_mday, tm->tm_wday,
		tm->tm_hour, tm->tm_min, tm->tm_sec);

unlock:
	k_spin_unlock(&data->lock, key);

	return ret;
}

static const struct rtc_driver_api rtc_ds3231_driver_api = {
	.set_time = rtc_ds3231_set_time,
	.get_time = rtc_ds3231_get_time,
};

static int rtc_ds3231_init(const struct device *dev)
{
	const struct rtc_ds3231_config * const config = dev->config;

	if (!device_is_ready(config->mfd)) {
		return -ENODEV;
	}

	LOG_DBG("%s: ready with MFD backend over %s!", dev->name,
		config->mfd->name);
	return 0;
}

#ifdef CONFIG_PM_DEVICE
static int rtc_ds3231_pm_device_pm_action(const struct device *dev,
					  enum pm_device_action action)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(action);

	return 0;
}
#endif

#if CONFIG_RTC_DS3231_INIT_PRIORITY <= CONFIG_MFD_DS3231_INIT_PRIORITY
#error RTC_DS3231_INIT_PRIORITY must be greater than MFD_DS3231_INIT_PRIORITY
#endif

#define RTC_DS3231_DEFINE(n)                                            \
                                                                        \
	static const struct rtc_ds3231_config rtc_ds3231_config_##n = { \
		.mfd = DEVICE_DT_GET(DT_INST_PARENT(n)),                \
	};                                                              \
                                                                        \
	static struct rtc_ds3231_data rtc_ds3231_data_##n;              \
                                                                        \
	PM_DEVICE_DT_INST_DEFINE(n, rtc_ds3231_pm_device_pm_action);    \
                                                                        \
	DEVICE_DT_INST_DEFINE(n, rtc_ds3231_init,                       \
			      PM_DEVICE_DT_INST_GET(n),                 \
			      &rtc_ds3231_data_##n,                     \
			      &rtc_ds3231_config_##n, POST_KERNEL,      \
			      CONFIG_RTC_DS3231_INIT_PRIORITY,          \
			      &rtc_ds3231_driver_api);

DT_INST_FOREACH_STATUS_OKAY(RTC_DS3231_DEFINE)
