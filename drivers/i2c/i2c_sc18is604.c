/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef CONFIG_MFD_SC18IS604_ASYNC
#error "CONFIG_MFD_SC18IS604_ASYNC must be enabled for I2C controller to function."
#endif /* CONFIG_MFD_SC18IS604_ASYNC */

#define DT_DRV_COMPAT nxp_sc18is604_i2c

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/pm/device.h>

#include <zephyr/drivers/i2c.h>

#include <zephyr/drivers/mfd/sc18is604.h>

#include "i2c_sc18is604.h"

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(sc18is604_i2c, CONFIG_I2C_LOG_LEVEL);

int await_signal(struct k_poll_signal *signal, int *result, k_timeout_t timeout)
{
	struct k_poll_event events[1] = {
		K_POLL_EVENT_INITIALIZER(K_POLL_TYPE_SIGNAL,
					 K_POLL_MODE_NOTIFY_ONLY,
					 signal),
	};

	k_poll(events, 1, timeout);

	int signaled = 0;

	k_poll_signal_check(signal, &signaled, result);

	return signaled;
}

/* Initialize reading out the interrupt source. */
static void i2c_sc18is604_interrupt_work_fn_initial(struct k_work *work)
{
	struct i2c_sc18is604_data * const data = CONTAINER_OF(work,
			struct i2c_sc18is604_data, interrupt_work_initial);
	const struct device *dev = data->dev;
	const struct i2c_sc18is604_config * const config = dev->config;
	int ret = 0;

	/* Soft spinning on interrupt handling lock */
	ret = k_sem_take(&data->interrupt_lock, K_NO_WAIT);
	if (ret != 0) {
		k_work_submit(work);
		return;
	}

	/*
	 * Begin asynchronous readout of i2c status register (this resets the
	 * hardware interrupt signal).
	 */
	k_poll_signal_reset(&data->interrupt_handling_data.signal);
	ret = READ_SC18IS604_REG_SIGNAL(config->parent_dev, I2C_STATUS,
					&data->interrupt_handling_data.i2cstat,
					&data->interrupt_handling_data.signal);
	if (ret != 0) {
		/* Failed to read out I2C status, retry */
		k_work_submit(work);
		k_sem_give(&data->interrupt_lock);
		return;
	}

	/* Submit work item for awaiting result */
	ret = k_work_schedule(&data->interrupt_work_final, K_NO_WAIT);
	if (ret != 0 && ret != 1) {
		/*
		 * ret == 0 shouldn't happen, but is permissible: at least we
		 * know the item will run. Other return values mean we can't
		 * rely on the item to run, so we must release the lock here to
		 * prevent a deadlock on the next interrupt.
		 */
		k_sem_give(&data->interrupt_lock);
	}
}

/* Await the result of reading out the interrupt source and act on it. */
static void i2c_sc18is604_interrupt_work_fn_final(struct k_work *work)
{
	struct k_work_delayable *work_delayable = CONTAINER_OF(work,
					struct k_work_delayable, work);
	struct i2c_sc18is604_data * const data = CONTAINER_OF(work_delayable,
			struct i2c_sc18is604_data, interrupt_work_final);

	/* Check result of i2c status readout */
	int result = 0;
	int signaled = await_signal(&data->interrupt_handling_data.signal,
				    &result, K_NO_WAIT);

	if (!signaled) {
		/* Transfer not complete, keep spinning */
		k_work_schedule(work_delayable, K_MSEC(1));
		return;
	}

	/* If bus transfer failed, try again */
	if (result != 0) {
		k_work_submit(&data->interrupt_work_initial);
		goto end;
	}

	/* Otherwise, propagate the received status via signal */
	k_poll_signal_raise(&data->interrupt_signal,
			    data->interrupt_handling_data.i2cstat);

end:
	/* Release interrupt handling lock */
	k_sem_give(&data->interrupt_lock);
}

/*
 * Interrupt callback that is registered with the parent MFD which runs in ISR
 * context.
 */
static void i2c_sc18is604_interrupt_callback(const struct device *dev,
					     struct gpio_callback *cb,
					     gpio_port_pins_t pins)
{
	struct i2c_sc18is604_data * const data = CONTAINER_OF(cb,
			struct i2c_sc18is604_data, interrupt_cb);

	/*
	 * Reading out the interrupt source requires bus communication, so we do
	 * it via work queue items
	 */
	k_work_submit(&data->interrupt_work_initial);
}

static inline int i2c_sc18is604_set_clock_speed(const struct device *dev,
						uint32_t speed)
{
	const struct i2c_sc18is604_config * const config = dev->config;
	uint8_t value;

	switch (speed) {
	case I2C_SPEED_STANDARD:
		value = SC18IS604_I2C_CLOCK_99KHZ;
		break;
	case I2C_SPEED_FAST:
		value = SC18IS604_I2C_CLOCK_375KHZ;
		break;
	default:
		return -EINVAL;
	}

	return WRITE_SC18IS604_REG(config->parent_dev, I2C_CLOCK, value);
}

static int i2c_sc18is604_write_message(const struct device *dev,
				       uint8_t *data, size_t len,
				       uint16_t addr)
{
	const struct i2c_sc18is604_config * const config = dev->config;
	struct i2c_sc18is604_data * const drv_data = dev->data;
	int ret;

	uint8_t cmd[] = {
		SC18IS604_CMD_WRITE_I2C,
		len, (uint8_t) addr
	};

	/* Reset interrupt signal */
	k_poll_signal_reset(&drv_data->interrupt_signal);

	/* Send 'I2C WRITE' command with data attached */
	ret = mfd_sc18is604_transfer(config->parent_dev, cmd, ARRAY_SIZE(cmd),
							 data, len, NULL, 0);
	if (ret != 0) {
		return ret;
	}
	/* Await interrupt signal */
	int result = 0;
	int signaled = await_signal(&drv_data->interrupt_signal,
				    &result, K_FOREVER);

	if (!signaled) {
		return -EIO;
	}

	if (result != SC18IS604_I2C_STATUS_SUCCESS) {
		return -EIO;
	}

	return 0;
}

static int i2c_sc18is604_read_message(const struct device *dev,
				      uint8_t *data, size_t len,
				      uint16_t addr)
{
	const struct i2c_sc18is604_config * const config = dev->config;
	struct i2c_sc18is604_data * const drv_data = dev->data;
	int ret = 0;

	uint8_t cmd[] = {
		SC18IS604_CMD_READ_I2C,
		len, (uint8_t) addr
	};

	/* Claim lock on MFD */
	mfd_sc18is604_claim(config->parent_dev, K_FOREVER);

	/* Reset interrupt signal */
	k_poll_signal_reset(&drv_data->interrupt_signal);

	/* Send 'I2C READ' command */
	ret = mfd_sc18is604_transfer(config->parent_dev, cmd, ARRAY_SIZE(cmd),
							 NULL, 0, NULL, 0);
	if (ret != 0) {
		goto release_and_return;
	}

	/* Await interrupt signal */
	int result = 0;
	int signaled = await_signal(&drv_data->interrupt_signal,
				    &result, K_FOREVER);

	if (!signaled) {
		ret = -EIO;
		goto release_and_return;
	}

	if (result != SC18IS604_I2C_STATUS_SUCCESS) {
		ret = -EIO;
		goto release_and_return;
	}

	/* Read out the received data */
	ret =  mfd_sc18is604_read_buffer(config->parent_dev, data, len);
	if (ret != 0) {
		ret = -EIO;
		goto release_and_return;
	}

release_and_return:
	mfd_sc18is604_release(config->parent_dev);
	return ret;
}

static int i2c_sc18is604_configure(const struct device *dev, uint32_t config)
{
	struct i2c_sc18is604_data * const data = dev->data;

	/* Device can only act as controller */
	if ((config & I2C_MODE_CONTROLLER) != I2C_MODE_CONTROLLER) {
		return -EINVAL;
	}

	/* Controller doesn't support 10bit addressing */
	if ((config & I2C_ADDR_10_BITS) == I2C_ADDR_10_BITS) {
		return -EINVAL;
	}

	/* Adjust bus speed if necessary */
	uint32_t speed = I2C_SPEED_GET(config);

	if (speed != I2C_SPEED_GET(data->i2c_config)) {

		/*
		 * Controller only supports 'standard' (100kHz) and 'fast'
		 * (400kHz) speeds.
		 */
		if ((speed == I2C_SPEED_STANDARD) ||
			(speed == I2C_SPEED_FAST)) {

			int ret = i2c_sc18is604_set_clock_speed(dev, speed);

			if (ret != 0) {
				return ret;
			}

		} else {
			return -EINVAL;
		}
	}

	/* Store new config */
	data->i2c_config = config;

	return 0;
}

static int i2c_sc18is604_get_config(const struct device *dev, uint32_t *config)
{
	const struct i2c_sc18is604_data * const data = dev->data;
	*config = data->i2c_config;
	return 0;
}

static int i2c_sc18is604_transfer_msg(const struct device *dev,
				      struct i2c_msg *msg, uint16_t addr)
{
	/* Device doesn't support 10bit addressing */
	if ((msg->flags & I2C_MSG_ADDR_10_BITS) == I2C_MSG_ADDR_10_BITS) {
		return -EINVAL;
	}

	/* Add RW bit to address */
	addr <<= 1;
	addr |= (msg->flags & I2C_MSG_RW_MASK);

	if ((msg->flags & I2C_MSG_READ) == I2C_MSG_READ) {
		return i2c_sc18is604_read_message(dev, msg->buf,
						  msg->len, addr);
	} else {
		return i2c_sc18is604_write_message(dev, msg->buf,
						   msg->len, addr);
	}

	/* Should be unreachable */
	return -EINVAL;
}

static int i2c_sc18is604_transfer(const struct device *dev,
				  struct i2c_msg *msgs,
				  uint8_t num_msgs,
				  uint16_t addr)
{
	struct i2c_sc18is604_data * const data = dev->data;
	int ret;

	if (num_msgs == 0) {
		return 0;
	}

	/* Lock driver instance before multi-transfer transaction */
	k_sem_take(&data->lock, K_FOREVER);

	/* Handle messages one-by-one */
	for (int i = 0; i < num_msgs; i++) {
		ret = i2c_sc18is604_transfer_msg(dev, &msgs[i], addr);
		if (ret != 0) {
			break;
		}
	}

	/* Release lock */
	k_sem_give(&data->lock);

	return ret;
}

static const struct i2c_driver_api i2c_sc18is604_api = {
	.configure = i2c_sc18is604_configure,
	.get_config = i2c_sc18is604_get_config,
	.transfer = i2c_sc18is604_transfer,
#ifdef CONFIG_I2C_CALLBACK
	.transfer_cb = i2c_sc18is604_transfer_cb,
#endif /* CONFIG_I2C_CALLBACK */
};

static int i2c_sc18is604_init(const struct device *dev)
{
	const struct i2c_sc18is604_config * const config = dev->config;
	struct i2c_sc18is604_data * const data = dev->data;
	int ret = 0;

	/* Check parent bus readiness */
	if (!device_is_ready(config->parent_dev)) {
		LOG_ERR("%s: bridge device %s not ready",
			dev->name, config->parent_dev->name);
		return -ENODEV;
	}

	/* Set back-reference */
	data->dev = dev;

	/* Initialize locks (both initially open) */
	k_sem_init(&data->lock, 1, 1);
	k_sem_init(&data->interrupt_lock, 1, 1);

	/* Initialize interrupt signal */
	k_poll_signal_init(&data->interrupt_signal);

	/* Register interrupt callback with parent MFD */
	gpio_init_callback(&data->interrupt_cb,
			   i2c_sc18is604_interrupt_callback, 0xffffffff);
	ret = mfd_sc18is604_add_callback(config->parent_dev, &data->interrupt_cb);
	if (ret != 0) {
		LOG_ERR("%s: failed to register interrupt callback on %s: %d",
			dev->name, config->parent_dev->name, ret);
		return ret;
	}

	/* Set up work items for interrupt handling */
	k_work_init(&data->interrupt_work_initial,
		    i2c_sc18is604_interrupt_work_fn_initial);
	k_work_init_delayable(&data->interrupt_work_final,
			      i2c_sc18is604_interrupt_work_fn_final);

	/* Initialize data used by interrupt handling work items */
	k_poll_signal_init(&data->interrupt_handling_data.signal);

	LOG_DBG("%s: ready over %s!", dev->name,
		config->parent_dev->name);
	return 0;
}

#ifdef CONFIG_PM_DEVICE
static int i2c_sc18is604_pm_device_pm_action(const struct device *dev,
					     enum pm_device_action action)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(action);

	return 0;
}
#endif

#define I2C_SC18IS604_DEFINE(inst)                                            \
                                                                              \
	static const                                                          \
	struct i2c_sc18is604_config i2c_sc18is604_config_##inst =             \
	{                                                                     \
		.parent_dev = DEVICE_DT_GET(DT_INST_BUS(inst)),               \
	};                                                                    \
                                                                              \
	static struct i2c_sc18is604_data i2c_sc18is604_data_##inst = { };     \
                                                                              \
	PM_DEVICE_DT_INST_DEFINE(inst, i2c_sc18is604_pm_device_pm_action);    \
                                                                              \
	DEVICE_DT_INST_DEFINE(inst, i2c_sc18is604_init,                       \
			      PM_DEVICE_DT_INST_GET(inst),                    \
			      &i2c_sc18is604_data_##inst,                     \
			      &i2c_sc18is604_config_##inst, POST_KERNEL,      \
			      CONFIG_I2C_SC18IS604_INIT_PRIORITY,             \
			      &i2c_sc18is604_api);

DT_INST_FOREACH_STATUS_OKAY(I2C_SC18IS604_DEFINE);
