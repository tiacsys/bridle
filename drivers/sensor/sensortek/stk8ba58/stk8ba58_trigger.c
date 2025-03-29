/*
 * Sensortek Technology STK8BA58 3-axis accelerometer driver
 *
 * Copyright (c) 2025 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT sensortek_stk8ba58

#include "stk8ba58.h"

#include <zephyr/logging/log.h>
LOG_MODULE_DECLARE(STK8BA58, CONFIG_SENSOR_LOG_LEVEL);

static void stk8ba58_gpio_callback(const struct device *dev,
				   struct gpio_callback *cb, uint32_t pins)
{
	struct stk8ba58_data *data =
		CONTAINER_OF(cb, struct stk8ba58_data, gpio_cb);
	const struct stk8ba58_config *cfg = data->dev->config;
	int ret;

	ARG_UNUSED(pins);

	ret = gpio_pin_interrupt_configure_dt(&cfg->gpio_int, GPIO_INT_DISABLE);
	if (ret < 0) {
		LOG_ERR("%s: Not able to configure pin_int", dev->name);
	}

#if defined(CONFIG_STK8BA58_TRIGGER_OWN_THREAD)
	k_sem_give(&data->trig_sem);
#elif defined(CONFIG_STK8BA58_TRIGGER_GLOBAL_THREAD)
	k_work_submit(&data->work);
#endif
}

static void stk8ba58_handle_drdy_int(const struct device *dev)
{
	struct stk8ba58_data *data = dev->data;

	if (data->data_ready_handler != NULL) {
		data->data_ready_handler(dev, data->data_ready_trigger);
	}
}

static void stk8ba58_handle_int(const struct device *dev)
{
	const struct stk8ba58_config *cfg = dev->config;
	const struct i2c_dt_spec *i2c = (struct i2c_dt_spec *)&cfg->i2c;
	stk8ba58_all_sources_t sources;
	int ret;

	stk8ba58_all_sources_get(i2c, &sources);

	if (sources.intsts2.data_sts) {
		stk8ba58_handle_drdy_int(dev);
	}

	ret = gpio_pin_interrupt_configure_dt(&cfg->gpio_int,
					      GPIO_INT_EDGE_TO_ACTIVE);
	if (ret < 0) {
		LOG_ERR("%s: Not able to configure pin_int", dev->name);
	}
}

#ifdef CONFIG_STK8BA58_TRIGGER_OWN_THREAD
static void stk8ba58_thread(void *p1, void *p2, void *p3)
{
	ARG_UNUSED(p2);
	ARG_UNUSED(p3);

	struct stk8ba58_data *data = p1;

	while (1) {
		k_sem_take(&data->trig_sem, K_FOREVER);
		stk8ba58_handle_int(data->dev);
	}
}
#endif

#ifdef CONFIG_STK8BA58_TRIGGER_GLOBAL_THREAD
static void stk8ba58_work_cb(struct k_work *work)
{
	struct stk8ba58_data *data =
		CONTAINER_OF(work, struct stk8ba58_data, work);

	stk8ba58_handle_int(data->dev);
}
#endif

static int stk8ba58_init_interrupt(const struct device *dev)
{
	const struct stk8ba58_config *cfg = dev->config;
	const struct i2c_dt_spec *i2c = (struct i2c_dt_spec *)&cfg->i2c;
	const struct gpio_dt_spec *int1 = (struct gpio_dt_spec *)&cfg->gpio_int;
	stk8ba58_pin_int1_route_t route;
	stk8ba58_int_enable_t enable;
	int err;

	/* Enable pulsed mode */
	err = stk8ba58_int_notification_set(i2c, STK8BA58_INT_PULSED);
	if (err < 0) {
		return err;
	}

	if (int1->dt_flags & GPIO_PULL_UP) {
		/* Enable open-drain mode */

		LOG_DBG("%s: int1: enable open-drain mode", dev->name);

		err = stk8ba58_pin_int1_mode_set(i2c, STK8BA58_OPEN_DRAIN);
		if (err < 0) {
			return err;
		}

	} else {

		/* Enable push-pull mode */
		LOG_DBG("%s: int1: enable push-pull mode", dev->name);

		err = stk8ba58_pin_int1_mode_set(i2c, STK8BA58_PUSH_PULL);
		if (err < 0) {
			return err;
		}
	}

	if (int1->dt_flags & GPIO_ACTIVE_LOW) {

		/* Enable active-low polarity */
		LOG_DBG("%s: int1: enable active-low polarity", dev->name);

		err = stk8ba58_pin_int1_polarity_set(i2c, STK8BA58_ACTIVE_LOW);
		if (err < 0) {
			return err;
		}

	} else {

		/* Enable active-high polarity */
		LOG_DBG("%s: int1: enable active-high polarity", dev->name);

		err = stk8ba58_pin_int1_polarity_set(i2c, STK8BA58_ACTIVE_HIGH);
		if (err < 0) {
			return err;
		}
	}

	/* route data-ready interrupt on int1 */
	err = stk8ba58_pin_int1_route_get(i2c, &route);
	if (err < 0) {
		return err;
	}

	route.data2int1 = 1;

	err = stk8ba58_pin_int1_route_set(i2c, route);
	if (err < 0) {
		return err;
	}

	/* enable data-ready interrupt source */
	err = stk8ba58_int_enable_get(i2c, &enable);
	if (err < 0) {
		return err;
	}

	enable.data_en = 1;

	err = stk8ba58_int_enable_set(i2c, enable);
	if (err < 0) {
		return err;
	}

	return 0;
}

int stk8ba58_trigger_init(const struct device *dev)
{
	struct stk8ba58_data *data = dev->data;
	const struct stk8ba58_config *cfg = dev->config;
	int ret;

	/* setup data ready gpio interrupt (INT1) */
	if (!gpio_is_ready_dt(&cfg->gpio_int)) {
		if (cfg->gpio_int.port) {
			LOG_ERR("%s: device %s is not ready", dev->name,
						cfg->gpio_int.port->name);
			return -ENODEV;
		}

		LOG_DBG("%s: gpio_int not defined in DT", dev->name);
		return 0;
	}

	data->dev = dev;

	ret = gpio_pin_configure_dt(&cfg->gpio_int, GPIO_INPUT);
	if (ret < 0) {
		LOG_ERR("Could not configure gpio");
		return ret;
	}

	LOG_DBG("%s: int on %s.%02u", dev->name, cfg->gpio_int.port->name,
				      cfg->gpio_int.pin);

	gpio_init_callback(&data->gpio_cb,
			   stk8ba58_gpio_callback,
			   BIT(cfg->gpio_int.pin));

	ret = gpio_add_callback(cfg->gpio_int.port, &data->gpio_cb);
	if (ret < 0) {
		LOG_ERR("Could not set gpio callback");
		return ret;
	}

#if defined(CONFIG_STK8BA58_TRIGGER_OWN_THREAD)
	k_sem_init(&data->trig_sem, 0, K_SEM_MAX_LIMIT);

	k_thread_create(&data->thread, data->thread_stack,
			CONFIG_STK8BA58_THREAD_STACK_SIZE,
			stk8ba58_thread,
			data, NULL, NULL,
			K_PRIO_COOP(CONFIG_STK8BA58_THREAD_PRIORITY),
			0, K_NO_WAIT);
	k_thread_name_set(&data->thread, dev->name);
#elif defined(CONFIG_STK8BA58_TRIGGER_GLOBAL_THREAD)
	data->work.handler = stk8ba58_work_cb;
#endif

	return gpio_pin_interrupt_configure_dt(&cfg->gpio_int,
					       GPIO_INT_EDGE_TO_ACTIVE);
}

int stk8ba58_trigger_set(const struct device *dev,
			 const struct sensor_trigger *trig,
			 sensor_trigger_handler_t handler)
{
	struct stk8ba58_data *data = dev->data;
	const struct stk8ba58_config *cfg = dev->config;
	const struct i2c_dt_spec *i2c = (struct i2c_dt_spec *)&cfg->i2c;
	int16_t raw[3];
	int ret;

	__ASSERT_NO_MSG(trig->type == SENSOR_TRIG_DATA_READY);

	if (cfg->gpio_int.port == NULL) {
		LOG_ERR("trigger_set is not supported");
		return -ENOTSUP;
	}

	ret = gpio_pin_interrupt_configure_dt(&cfg->gpio_int, GPIO_INT_DISABLE);
	if (ret < 0) {
		LOG_ERR("%s: Not able to configure pin_int", dev->name);
		return ret;
	}

	data->data_ready_handler = handler;
	if (handler == NULL) {
		LOG_WRN("stk8ba58: no handler");
		return 0;
	}

	/* re-trigger lost interrupt */
	stk8ba58_acceleration_raw_get(i2c, raw);

	data->data_ready_trigger = trig;

	stk8ba58_init_interrupt(dev);
	return gpio_pin_interrupt_configure_dt(&cfg->gpio_int,
					       GPIO_INT_EDGE_TO_ACTIVE);
}
