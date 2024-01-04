/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT maxim_ds3231_mfd

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/pm/device.h>

#include <zephyr/drivers/i2c.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/gpio/gpio_utils.h>

#include <zephyr/drivers/mfd/ds3231.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(mfd_ds3231, CONFIG_MFD_LOG_LEVEL);

struct mfd_ds3231_config {
	const struct i2c_dt_spec bus;
	const struct gpio_dt_spec isw;
};

struct mfd_ds3231_data {
	const struct device *dev;
	struct k_sem lock;
};

/*
 * multi functional interface --- main entries
 */

int mfd_ds3231_reg_read(const struct device *dev, const uint8_t reg,
			uint8_t *val)
{
	const struct mfd_ds3231_config * const config = dev->config;
	struct mfd_ds3231_data * const data = dev->data;
	int ret = 0;

	k_sem_take(&data->lock, K_FOREVER);

	ret = i2c_reg_read_byte_dt(&config->bus, reg, val);

	k_sem_give(&data->lock);

	return ret;
}

int mfd_ds3231_reg_read_burst(const struct device *dev, const uint8_t reg,
			      uint8_t *buf, const size_t len)
{
	const struct mfd_ds3231_config * const config = dev->config;
	struct mfd_ds3231_data * const data = dev->data;
	int ret = 0;

	k_sem_take(&data->lock, K_FOREVER);

	ret = i2c_burst_read_dt(&config->bus, reg, buf, len);

	k_sem_give(&data->lock);

	return ret;
}

int mfd_ds3231_reg_write(const struct device *dev, const uint8_t reg,
			 const uint8_t val)
{
	const struct mfd_ds3231_config * const config = dev->config;
	struct mfd_ds3231_data * const data = dev->data;
	int ret = 0;

	k_sem_take(&data->lock, K_FOREVER);

	ret = i2c_reg_write_byte_dt(&config->bus, reg, val);

	k_sem_give(&data->lock);

	return ret;
}

int mfd_ds3231_reg_write_burst(const struct device *dev, const uint8_t reg,
			       const uint8_t *buf, const size_t len)
{
	const struct mfd_ds3231_config * const config = dev->config;
	struct mfd_ds3231_data * const data = dev->data;
	int ret = 0;

	k_sem_take(&data->lock, K_FOREVER);

	ret = i2c_burst_write_dt(&config->bus, reg, buf, len);

	k_sem_give(&data->lock);

	return ret;
}

/*
 * driver initialization --- configure and setup internal driver mechanic
 */

static int mfd_ds3231_init(const struct device *dev)
{
	const struct mfd_ds3231_config * const config = dev->config;
	struct mfd_ds3231_data * const data = dev->data;
	int ret = 0;

	/* Initialize and take the lock */
	k_sem_init(&data->lock, 0, 1);

	/* Save device instance */
	data->dev = dev;

	if (!i2c_is_ready_dt(&config->bus)) {
		LOG_ERR("%s: I2C device %s not ready", dev->name,
			config->bus.bus->name);
		ret = -ENODEV;
		goto out_locked;
	}

	/* Disable alarm interrupt requests and squarewave output */
	ret = i2c_reg_write_byte_dt(&config->bus, DS3231_CTRL, 0x00);
	if (ret < 0) {
		LOG_ERR("%s: can't disable nINT/SQW output", dev->name);
	}

	if (config->isw.port != NULL) {
		if (!gpio_is_ready_dt(&config->isw)) {
			LOG_ERR("%s: GPIO pin: %s not ready", dev->name,
				config->isw.port ? config->isw.port->name :
						   "null");
			ret = -ENODEV;
			goto out_locked;
		}

		ret = gpio_pin_configure_dt(&config->isw, GPIO_INPUT);
		if (ret < 0) {
			LOG_ERR("%s: can't configure nINT/SQW pin %d as input",
				dev->name, config->isw.pin);
			goto out_locked;
		}
	}

out_locked:
	k_sem_give(&data->lock);

	LOG_DBG("%s: ready!", dev->name);
	return ret;
}

#ifdef CONFIG_PM_DEVICE
static int mfd_ds3231_pm_device_pm_action(const struct device *dev,
					  enum pm_device_action action)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(action);

	return 0;
}
#endif

#if CONFIG_MFD_DS3231_INIT_PRIORITY <= CONFIG_I2C_INIT_PRIORITY
#error MFD_DS3231_INIT_PRIORITY must be greater than I2C_INIT_PRIORITY
#endif

#define MFD_DS3231_DEFINE(n)                                            \
                                                                        \
	static const struct mfd_ds3231_config mfd_ds3231_config_##n = { \
		.bus = I2C_DT_SPEC_INST_GET(n),                         \
		.isw = GPIO_DT_SPEC_INST_GET_OR(n, isw_gpios, {0}),     \
	};                                                              \
                                                                        \
	static struct mfd_ds3231_data mfd_ds3231_data_##n;              \
                                                                        \
	PM_DEVICE_DT_INST_DEFINE(n, mfd_ds3231_pm_device_pm_action);    \
                                                                        \
	DEVICE_DT_INST_DEFINE(n, mfd_ds3231_init,                       \
			      PM_DEVICE_DT_INST_GET(n),                 \
			      &mfd_ds3231_data_##n,                     \
			      &mfd_ds3231_config_##n, POST_KERNEL,      \
			      CONFIG_MFD_DS3231_INIT_PRIORITY, NULL);

DT_INST_FOREACH_STATUS_OKAY(MFD_DS3231_DEFINE)
