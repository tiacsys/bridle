/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief MFD Driver for an SC16IS75X bridge
 */

#include <zephyr/kernel.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/gpio/gpio_utils.h>

#include <zephyr/drivers/mfd/sc16is75x.h>

#include "mfd_sc16is75x.h"

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(mfd_sc16is75x, CONFIG_MFD_LOG_LEVEL);

#if defined(CONFIG_MFD_SC16IS75X_ASWQ) &&                                                          \
	(!CONFIG_DYNAMIC_THREAD_POOL_SIZE && !defined(CONFIG_DYNAMIC_THREAD_ALLOC))
#error "SC16IS75x MFD driver requires either CONFIG_DYNAMIC_THREAD_POOL_SIZE>0" \
	"or CONFIG_DYNAMIC_THREAD_ALLOC"
#endif

#define SC16IS75X_SA_RD true
#define SC16IS75X_SA_WR false

static inline int mfd_sc16is75x_sub_address(const bool read, const uint8_t reg,
					    const uint8_t channel, uint8_t *sub_address)
{
	/*
	 * Subaddress scheme: [ R/W, A3, A2, A1, A0, CH1, Ch0, X]
	 * R/W: 1: Read, 0: Write (SPI only)
	 * A[3:0]: Register address
	 * CH1, CH0: Select serial channel
	 * X: Unused
	 */

	if ((reg & BIT_MASK(4)) > BIT_MASK(4)) {
		return -EINVAL;
	}

	if ((channel & BIT_MASK(2)) > BIT_MASK(2)) {
		return -EINVAL;
	}

	*sub_address = 0;
	*sub_address |= (channel & BIT_MASK(2)) << 1;
	*sub_address |= (reg & BIT_MASK(4)) << 3;
	WRITE_BIT(*sub_address, 7, read ? 1 : 0);

	return 0;
}

static int mfd_sc16is75x_read(const struct device *dev, const uint8_t channel, const uint8_t reg,
			      uint8_t *buf, const size_t len)
{
	struct mfd_sc16is75x_data *const data = dev->data;
	uint8_t sub_address = 0;
	int ret = 0;

	ret = mfd_sc16is75x_sub_address(SC16IS75X_SA_RD, reg, channel, &sub_address);
	if (ret != 0) {
		return ret;
	}

	return data->transfer_function->read_raw(dev, sub_address, buf, len);
}

#define READ_SC16IS75X_CHANNEL(dev, ch, reg, buf, len)                                             \
	mfd_sc16is75x_read((dev), (ch), SC16IS75X_REG_##reg, (buf), (len));

static int mfd_sc16is75x_write(const struct device *dev, const uint8_t channel, const uint8_t reg,
			       const uint8_t *buf, const size_t len)
{
	struct mfd_sc16is75x_data *const data = dev->data;
	uint8_t sub_address = 0;
	int ret = 0;

	ret = mfd_sc16is75x_sub_address(SC16IS75X_SA_WR, reg, channel, &sub_address);
	if (ret != 0) {
		return ret;
	}

	return data->transfer_function->write_raw(dev, sub_address, buf, len);
}

#define WRITE_SC16IS75X_CHANNEL(dev, ch, reg, buf, len)                                            \
	mfd_sc16is75x_write((dev), (ch), SC16IS75X_REG_##reg, (buf), (len));

int mfd_sc16is75x_read_register(const struct device *dev, const uint8_t channel, const uint8_t reg,
				uint8_t *value)
{
	return mfd_sc16is75x_read(dev, channel, reg, value, 1);
}

int mfd_sc16is75x_write_register(const struct device *dev, const uint8_t channel, const uint8_t reg,
				 const uint8_t value)
{
	return mfd_sc16is75x_write(dev, channel, reg, &value, 1);
}

int mfd_sc16is75x_set_register_bit(const struct device *dev, const uint8_t channel,
				   const uint8_t reg, const uint8_t bit, const bool value)
{
	struct mfd_sc16is75x_data *const data = dev->data;
	uint8_t reg_val = 0;
	int ret = 0;

	/* Lock device before multi-transfer transaction */
	k_mutex_lock(&data->transaction_lock, K_FOREVER);

	/* Read out current value */
	ret = mfd_sc16is75x_read(dev, channel, reg, &reg_val, 1);
	if (ret != 0) {
		goto end;
	}

	/* Set selected bit */
	WRITE_BIT(reg_val, bit, value);

	/* Write back modified value */
	ret = mfd_sc16is75x_write(dev, channel, reg, &reg_val, 1);
	if (ret != 0) {
		goto end;
	}

end:
	k_mutex_unlock(&data->transaction_lock);
	return ret;
}

int mfd_sc16is75x_read_fifo(const struct device *dev, const uint8_t channel, uint8_t *buf,
			    const size_t len)
{
	return READ_SC16IS75X_CHANNEL(dev, channel, RHR, buf, len);
}

int mfd_sc16is75x_write_fifo(const struct device *dev, const uint8_t channel, const uint8_t *buf,
			     const size_t len)
{
	return WRITE_SC16IS75X_CHANNEL(dev, channel, THR, buf, len);
}

#ifdef CONFIG_MFD_SC16IS75X_ASYNC

static int mfd_sc16is75x_read_signal(const struct device *dev, const uint8_t channel,
				     const uint8_t reg, uint8_t *buf, const size_t len,
				     struct k_poll_signal *signal)
{
	struct mfd_sc16is75x_data *const data = dev->data;
	uint8_t sub_address = 0;
	int ret = 0;

	ret = mfd_sc16is75x_sub_address(SC16IS75X_SA_RD, reg, channel, &sub_address);
	if (ret != 0) {
		return ret;
	}

	return data->transfer_function->read_raw_signal(dev, sub_address, buf, len, signal);
}

int mfd_sc16is75x_read_register_signal(const struct device *dev, const uint8_t channel,
				       const uint8_t reg, uint8_t *value,
				       struct k_poll_signal *signal)
{
	return mfd_sc16is75x_read_signal(dev, channel, reg, value, 1, signal);
}

#endif /* CONFIG_MFD_SC16IS75X_ASYNC */

#ifdef CONFIG_MFD_SC16IS75X_INTERRUPTS

int mfd_sc16is75x_add_callback(const struct device *dev, struct gpio_callback *callback)
{
	struct mfd_sc16is75x_data *const data = dev->data;

	return gpio_manage_callback(&data->callbacks, callback, true);
}

int mfd_sc16is75x_remove_callback(const struct device *dev, struct gpio_callback *callback)
{
	struct mfd_sc16is75x_data *const data = dev->data;

	return gpio_manage_callback(&data->callbacks, callback, false);
}

static void mfd_sc16is75x_interrupt_work_fn_init(struct k_work *work)
{
	struct mfd_sc16is75x_data *const data =
		CONTAINER_OF(work, struct mfd_sc16is75x_data, interrupt_work_init);
	const struct device *const dev = data->self;
	const struct mfd_sc16is75x_config *const config = dev->config;
	int ret = 0;

	/*
	 * Attempt to get interrupt handling lock. If it's taken, that means
	 * a handling transaction is already active. In that case, reschedule
	 * self.
	 */
	ret = k_sem_take(&data->interrupt_lock, K_NO_WAIT);
	if (ret != 0) {
		k_work_submit(work);
		return;
	}

	/* Initiate reading from IIRs */
	for (int i = 0; i < config->n_channels; i++) {
		data->interrupt_data.iir[i] = BIT(SC16IS75X_BIT_IIR_PENDING);
		k_poll_signal_init(&data->interrupt_data.signals[i]);
		uint8_t ch = config->channels[i];

		ret = READ_SC16IS75X_CHREG_SIGNAL(dev, ch, IIR, &data->interrupt_data.iir[i],
						  &data->interrupt_data.signals[i]);
		if (ret != 0) {
			/*
			 * Propagate a failure to start the transfer the same
			 * as a failure to complete it: Have the finalizing
			 * work item retry the whole handling process. To do
			 * this, raise the signal ourselves with a generic
			 * error.
			 */
			k_poll_signal_raise(&data->interrupt_data.signals[i], -1);
		}
	}

	/* Schedule finalizing work item. */
	ret = k_work_schedule(&data->interrupt_work_final, K_USEC(100));
	if (ret != 0 && ret != 1) {
		/*
		 * Result ret == 0 shouldn't happen, but is permissible: at
		 * least we know the item will run. Other return values mean we
		 * can't rely on the item to run, so we must release the lock
		 * here to prevent a deadlock on the next interrupt.
		 */
		k_sem_give(&data->interrupt_lock);
	}
}

static void mfd_sc16is75x_interrupt_work_fn_final(struct k_work *work)
{
	struct k_work_delayable *work_delayable = (struct k_work_delayable *)work;
	struct mfd_sc16is75x_data *const data =
		CONTAINER_OF(work_delayable, struct mfd_sc16is75x_data, interrupt_work_final);
	const struct device *const dev = data->self;
	const struct mfd_sc16is75x_config *const config = dev->config;
	enum mfd_sc16is75x_event event;
	bool retry = false;

	struct k_poll_event poll_events[config->n_channels];
	int results[config->n_channels];

	/* Check for completion of running transfers */
	for (int i = 0; i < config->n_channels; i++) {
		poll_events[i] = (struct k_poll_event)K_POLL_EVENT_INITIALIZER(
			K_POLL_TYPE_SIGNAL, K_POLL_MODE_NOTIFY_ONLY,
			&data->interrupt_data.signals[i]);
	}

	k_poll(poll_events, config->n_channels, K_NO_WAIT);
	for (int i = 0; i < config->n_channels; i++) {
		int signaled = 0;

		k_poll_signal_check(&data->interrupt_data.signals[i], &signaled, &results[i]);
		if (!signaled) {
			/*
			 * At least one transfer isn't done yet,
			 * continue spinning.
			 */
			k_work_schedule(work_delayable, K_USEC(100));
			return;
		}
	}

	/*
	 * Once all transfers are complete, check return values. If any
	 * transfers failed, retry the interrupt handling precedure.
	 */
	for (int i = 0; i < config->n_channels; i++) {
		if (results[i] != 0) {
			retry = true;
			break;
		}
	}

	/* Sorting out and triggering callbacks for the various types */
	for (int i = 0; i < config->n_channels; i++) {
		uint8_t type = GET_FIELD(data->interrupt_data.iir[i], SC16IS75X_BIT_IIR_TYPE);

		/* Transfer for this channel failed, no data to check */
		if (results[i] != 0) {
			continue;
		}

		/* channel has not fired (0: pending, 1: not pending) */
		if (IS_BIT_SET(data->interrupt_data.iir[i], SC16IS75X_BIT_IIR_PENDING)) {
			continue;
		};

		uint8_t ch = config->channels[i];

		/* reset event number for each channel iterration */
		event = SC16IS75X_EVENT_MAX;

		if (type == SC16IS75X_INT_RXLSE) { /* priority 1 */
			retry = true;
			event = (ch == 0)   ? SC16IS75X_EVENT_UART0_RXLSE
				: (ch == 1) ? SC16IS75X_EVENT_UART1_RXLSE
					    : SC16IS75X_EVENT_MAX;
		} else if (type == SC16IS75X_INT_RXTO) { /* priority 2 */
			retry = true;
			event = (ch == 0)   ? SC16IS75X_EVENT_UART0_RXTO
				: (ch == 1) ? SC16IS75X_EVENT_UART1_RXTO
					    : SC16IS75X_EVENT_MAX;
		} else if (type == SC16IS75X_INT_RHRI) { /* priority 2 */
			retry = true;
			event = (ch == 0)   ? SC16IS75X_EVENT_UART0_RHRI
				: (ch == 1) ? SC16IS75X_EVENT_UART1_RHRI
					    : SC16IS75X_EVENT_MAX;
		} else if (type == SC16IS75X_INT_THRI) { /* priority 3 */
			retry = true;
			event = (ch == 0)   ? SC16IS75X_EVENT_UART0_THRI
				: (ch == 1) ? SC16IS75X_EVENT_UART1_THRI
					    : SC16IS75X_EVENT_MAX;
		} else if (type == SC16IS75X_INT_MSI) { /* priority 4 */
			retry = true;
			event = (ch == 0)   ? SC16IS75X_EVENT_UART0_MSI
				: (ch == 1) ? SC16IS75X_EVENT_UART1_MSI
					    : SC16IS75X_EVENT_MAX;
		} else if (type == SC16IS75X_INT_IO) { /* priority 5 */
			retry = true;
			event = (ch == 0)   ? SC16IS75X_EVENT_IO0_STATE
				: (ch == 1) ? SC16IS75X_EVENT_IO1_STATE
					    : SC16IS75X_EVENT_MAX;
		} else if (type == SC16IS75X_INT_XOFF) { /* priority 6 */
			retry = true;
			event = (ch == 0)   ? SC16IS75X_EVENT_UART0_XOFF
				: (ch == 1) ? SC16IS75X_EVENT_UART1_XOFF
					    : SC16IS75X_EVENT_MAX;
		} else if (type == SC16IS75X_INT_HWFL) { /* priority 7 */
			retry = true;
			event = (ch == 0)   ? SC16IS75X_EVENT_UART0_HWFL
				: (ch == 1) ? SC16IS75X_EVENT_UART1_HWFL
					    : SC16IS75X_EVENT_MAX;
		}

		if (event < SC16IS75X_EVENT_MAX) {
			gpio_fire_callbacks(&data->callbacks, data->self, BIT(event));
		}
	}

	/*
	 * Resubmit handler to queue to look for further pending interrupts,
	 * or if interrupt pin is still active.
	 */
	if (retry || gpio_pin_get_dt(&config->interrupt) != 0) {
		k_work_submit(&data->interrupt_work_init);
	};

	/* Release lock */
	k_sem_give(&data->interrupt_lock);
}

static void mfd_sc16is75x_interrupt_callback(const struct device *dev, struct gpio_callback *cb,
					     gpio_port_pins_t pins)
{
	/*
	 * Handling interrupts requires bus operations, which we can't
	 * do from an ISR. Schedule a work item to do it instead.
	 */
	struct mfd_sc16is75x_data *const data =
		CONTAINER_OF(cb, struct mfd_sc16is75x_data, interrupt_cb);

	k_work_submit(&data->interrupt_work_init);
}

/**
 * @brief Set up interrupt handling.
 *
 * @param dev An SC16IS75X MFD device.
 * @param gpio The GPIO specification from devicetree.
 * @param flags Additional GPIO flags.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
static int mfd_sc16is75x_bind_interrupt(const struct device *dev, const struct gpio_dt_spec *gpio,
					const gpio_flags_t flags)
{
	struct mfd_sc16is75x_data *const data = dev->data;
	int ret = 0;

	if (gpio->port == NULL) {
		return -EINVAL;
	}

	LOG_DBG("%s: bind GPIO port %s, pin %d to interrupt handling", dev->name, gpio->port->name,
		gpio->pin);

	ret = gpio_pin_interrupt_configure_dt(gpio, flags);
	if (ret != 0) {
		LOG_ERR("%s: couldn't enable interrupt on GPIO pin %d", dev->name, gpio->pin);
		return ret;
	}

	gpio_init_callback(&data->interrupt_cb, mfd_sc16is75x_interrupt_callback, BIT(gpio->pin));

	ret = gpio_add_callback_dt(gpio, &data->interrupt_cb);
	if (ret != 0) {
		LOG_ERR("%s: couldn't register callback on GPIO port %s", dev->name,
			gpio->port->name);
		return ret;
	}

	return 0;
}

#endif /* CONFIG_MFD_SC16IS75X_INTERRUPTS */

/**
 * @brief Reset device.
 *
 * @param dev An SC16IS75X MFD device.
 *
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
static int mfd_sc16is75x_chip_reset(const struct device *dev)
{
	const struct mfd_sc16is75x_config *const config = dev->config;
	int ret = 0;

	LOG_DBG("%s: resetting device", dev->name);
	if (config->reset.port != NULL) {
		ret = gpio_pin_set_dt(&config->reset, 1);
		if (ret != 0) {
			goto end;
		}

		/* Pull reset for a few µs. */
		k_usleep(5);

		ret = gpio_pin_set_dt(&config->reset, 0);
		if (ret != 0) {
			goto end;
		}

		/* Then wait another few µs for device startup. */
		k_usleep(5);
	}

end:
	return ret;
}

/**
 * @brief Set up GPIO pin.
 *
 * @param dev An SC16IS75X MFD device.
 * @param gpio The GPIO specification from devicetree.
 * @param flags Additional GPIO flags.
 *
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
static int mfd_sc16is75x_configure_gpio_pin(const struct device *dev,
					    const struct gpio_dt_spec *gpio,
					    const gpio_flags_t flags)
{
	int ret = 0;

	if (gpio->port != NULL) {
		LOG_DBG("%s: configure GPIO port %s, pin %d", dev->name, gpio->port->name,
			gpio->pin);

		if (!gpio_is_ready_dt(gpio)) {
			LOG_ERR("%s: GPIO port %s not ready", dev->name, gpio->port->name);
			return -ENODEV;
		}

		ret = gpio_pin_configure_dt(gpio, flags);
		if (ret != 0) {
			LOG_ERR("%s: couldn't configure GPIO pin %d", dev->name, gpio->pin);
			return ret;
		}
	} else {
		return -EINVAL;
	}

	return 0;
}

static int mfd_sc16is75x_init(const struct device *dev)
{
	const struct mfd_sc16is75x_config *const config = dev->config;
	struct mfd_sc16is75x_data *const data = dev->data;
	int ret = 0;

	/* Create back-reference for interrupt handling */
	data->self = dev;

	/* Initialize transaction lock */
	k_mutex_init(&data->transaction_lock);

	/* Configure bus specific transfer functions (SPI or I2C) */
	ret = config->bus_init(dev);
	if (ret != 0) {
		LOG_ERR("%s: bus initialization failed: %d", dev->name, ret);
		goto end;
	}

	/* Configure reset output pin. */
	ret = mfd_sc16is75x_configure_gpio_pin(dev, &config->reset, GPIO_OUTPUT);
	if (ret != 0) {
		LOG_ERR("%s: reset GPIO pin configuration failed: %d", dev->name, ret);
		goto end;
	}

	/* Reset device. */
	ret = mfd_sc16is75x_chip_reset(dev);
	if (ret != 0) {
		LOG_ERR("%s: couldn't reset device: %d", dev->name, ret);
		goto end;
	}

#ifdef CONFIG_MFD_SC16IS75X_ASWQ
	/* Initialize private work queue. */
	size_t work_queue_stack_size = CONFIG_MFD_SC16IS75X_WORKQUEUE_STACK_SIZE;

	k_work_queue_init(&data->work_queue);
	data->work_queue_stack = k_thread_stack_alloc(work_queue_stack_size, 0);
	k_work_queue_start(&data->work_queue, data->work_queue_stack, work_queue_stack_size,
			   K_HIGHEST_THREAD_PRIO, NULL);
#endif /* CONFIG_MFD_SC16IS75X_ASWQ */

#ifdef CONFIG_MFD_SC16IS75X_INTERRUPTS

	/* Initialize interrupt handling lock as open */
	k_sem_init(&data->interrupt_lock, 1, 1);

	/* Configure interrupt output pin. */
	ret = mfd_sc16is75x_configure_gpio_pin(dev, &config->reset, GPIO_INPUT);
	if (ret != 0) {
		LOG_ERR("%s: interrupt GPIO pin configuration failed: %d", dev->name, ret);
		goto end;
	}

	/* Set up interrupt handling */
	k_work_init(&data->interrupt_work_init, mfd_sc16is75x_interrupt_work_fn_init);
	k_work_init_delayable(&data->interrupt_work_final, mfd_sc16is75x_interrupt_work_fn_final);

	/* Set up interrupt handling */
	ret = mfd_sc16is75x_bind_interrupt(dev, &config->interrupt, GPIO_INT_EDGE_TO_ACTIVE);
	if (ret != 0) {
		LOG_ERR("%s: interrupt callback binding failed: %d", dev->name, ret);
		goto end;
	}

#endif /* CONFIG_MFD_SC16IS75X_INTERRUPTS */

end:
	return ret;
}

#ifdef CONFIG_PM_DEVICE
static int mfd_sc16is75x_pm_device_pm_action(const struct device *dev, enum pm_device_action action)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(action);

	return 0;
}
#endif

/**
 * @brief For a given child node, if it's a UART controller: return the
 *        channel id (`reg` property), with a comma. If the child is not
 *        a UART controller, return nothing.
 *
 * Note that since the property is technically an array, we take the 0th entry
 * to avoid extra braces.
 */
#define MFD_SC16IS75X_CHILD_CHANNEL(child)                                                         \
	COND_CODE_1(DT_NODE_HAS_COMPAT(child, nxp_sc16is75x_uart),                                 \
		    (DT_PROP_BY_IDX(child, reg, 0), ), ())

/**
 * @brief Construct a bracketed list of all child UART controllers' channel id
 *        (== `reg` property)
 */
#define MFD_SC16IS75X_UART_CHANNELS(inst)                                                          \
	{DT_INST_FOREACH_CHILD_STATUS_OKAY(inst, MFD_SC16IS75X_CHILD_CHANNEL)}

/**
 * @brief Construct struct initializer entries for an SPI bus configuration.
 */
#define MFD_SC16IS75X_DEFINE_SPI_BUS(inst)                                                         \
	.spi = SPI_DT_SPEC_INST_GET(inst, SPI_OP_MODE_MASTER | SPI_WORD_SET(8), 0),                \
	.bus_init = mfd_sc16is75x_spi_init

/**
 * @brief Construct struct initializer entries for an I2C bus configuration.
 */
#define MFD_SC16IS75X_DEFINE_I2C_BUS(inst)                                                         \
	.i2c = I2C_DT_SPEC_INST_GET(inst), .bus_init = mfd_sc16is75x_i2c_init

/**
 * @brief Return one of the two bus initializer lists above, selecting the
 *        correct bus based on the devicetree.
 */
#define MFD_SC16IS75X_DEFINE_BUS(inst)                                                             \
	COND_CODE_1(DT_INST_ON_BUS(inst, spi), (MFD_SC16IS75X_DEFINE_SPI_BUS(inst)),               \
		    (MFD_SC16IS75X_DEFINE_I2C_BUS(inst)))

/**
 * @brief Initializer macro for a device driver instance.
 *
 * In order to count the number of channels, we create an instance of the
 * channels list. Unfortunately, GCC doesn't like us using this same instance
 * for initialization, so we have to invoke the list construction macro again to
 * get a naked initializer list later.
 */
#define MFD_SC16IS75X_DEFINE(inst)                                                                 \
                                                                                                   \
	static uint8_t mfd_sc16is75x_uart_channels_##inst[] = MFD_SC16IS75X_UART_CHANNELS(inst);   \
                                                                                                   \
	static struct mfd_sc16is75x_config mfd_sc16is75x_config_##inst = {                         \
		MFD_SC16IS75X_DEFINE_BUS(inst), .reset = GPIO_DT_SPEC_INST_GET(inst, reset_gpios), \
		.n_channels = ARRAY_SIZE(mfd_sc16is75x_uart_channels_##inst),                      \
		.channels = MFD_SC16IS75X_UART_CHANNELS(inst),                                     \
		COND_CODE_1(CONFIG_MFD_SC16IS75X_INTERRUPTS,                                       \
			    (.interrupt = GPIO_DT_SPEC_INST_GET(inst, interrupt_gpios), ), ())};        \
                                                                                                   \
	static struct mfd_sc16is75x_data mfd_sc16is75x_data_##inst;                                \
                                                                                                   \
	PM_DEVICE_DT_INST_DEFINE(inst, mfd_sc16is75x_pm_device_pm_action);                         \
                                                                                                   \
	DEVICE_DT_INST_DEFINE(inst, mfd_sc16is75x_init, PM_DEVICE_DT_INST_GET(inst),               \
			      &mfd_sc16is75x_data_##inst, &mfd_sc16is75x_config_##inst,            \
			      POST_KERNEL, CONFIG_MFD_SC16IS75X_INIT_PRIORITY, NULL);

DT_INST_FOREACH_STATUS_OKAY(MFD_SC16IS75X_DEFINE);
