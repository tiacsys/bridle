/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio/gpio_utils.h>

#include <zephyr/drivers/mfd/sc16is75x.h>

#include "mfd_sc16is75x.h"

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(mfd_sc16is75x, CONFIG_MFD_LOG_LEVEL);

#define SC16IS75X_SA_RD	true
#define SC16IS75X_SA_WR	false

static inline int mfd_sc16is75x_sub_address(const bool read,
					    const uint8_t reg,
					    const uint8_t channel,
					    uint8_t *sub_address)
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

static int mfd_sc16is75x_read(const struct device *dev,
			      const uint8_t channel, const uint8_t reg,
			      uint8_t *buf, const size_t len)
{
	struct mfd_sc16is75x_data * const data = dev->data;
	uint8_t sub_address = 0;
	int ret = 0;

	ret = mfd_sc16is75x_sub_address(SC16IS75X_SA_RD, reg, channel,
					&sub_address);
	if (ret != 0) {
		return ret;
	}

	return data->transfer_function->read_raw(dev, sub_address, buf, len);
}

#define READ_SC16IS75X_CHANNEL(dev, ch, reg, buf, len)                       \
	mfd_sc16is75x_read((dev), (ch), SC16IS75X_REG_##reg, (buf), (len));

static int mfd_sc16is75x_write(const struct device *dev,
			       const uint8_t channel, const uint8_t reg,
			       const uint8_t *buf, const size_t len)
{
	struct mfd_sc16is75x_data * const data = dev->data;
	uint8_t sub_address = 0;
	int ret = 0;

	ret = mfd_sc16is75x_sub_address(SC16IS75X_SA_WR, reg, channel,
					&sub_address);
	if (ret != 0) {
		return ret;
	}

	return data->transfer_function->write_raw(dev, sub_address, buf, len);
}

#define WRITE_SC16IS75X_CHANNEL(dev, ch, reg, buf, len)                      \
	mfd_sc16is75x_write((dev), (ch), SC16IS75X_REG_##reg, (buf), (len));

int mfd_sc16is75x_read_register(const struct device *dev,
				const uint8_t channel,
				const uint8_t reg, uint8_t *value)
{
	return mfd_sc16is75x_read(dev, channel, reg, value, 1);
}

int mfd_sc16is75x_write_register(const struct device *dev,
				 const uint8_t channel,
				 const uint8_t reg, const uint8_t value)
{
	return mfd_sc16is75x_write(dev, channel, reg, &value, 1);
}

int mfd_sc16is75x_set_register_bit(const struct device *dev,
				   const uint8_t channel, const uint8_t reg,
				   const uint8_t bit, const bool value)
{
	struct mfd_sc16is75x_data * const data = dev->data;
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

int mfd_sc16is75x_read_fifo(const struct device *dev, const uint8_t channel,
			    uint8_t *buf, const size_t len)
{
	return READ_SC16IS75X_CHANNEL(dev, channel, RHR, buf, len);
}

int mfd_sc16is75x_write_fifo(const struct device *dev, const uint8_t channel,
			     const uint8_t *buf, const size_t len)
{
	return WRITE_SC16IS75X_CHANNEL(dev, channel, THR, buf, len);
}

int mfd_sc16is75x_add_callback(const struct device *dev,
			       struct gpio_callback *callback)
{
	struct mfd_sc16is75x_data * const data = dev->data;

	return gpio_manage_callback(&data->callbacks, callback, true);
}

int mfd_sc16is75x_remove_callback(const struct device *dev,
				  struct gpio_callback *callback)
{
	struct mfd_sc16is75x_data * const data = dev->data;

	return gpio_manage_callback(&data->callbacks, callback, false);
}

static void mfd_sc16is75x_interrupt_work_fn(struct k_work *work)
{
	struct mfd_sc16is75x_data * const data = CONTAINER_OF(work,
			struct mfd_sc16is75x_data, interrupt_work);
	const struct device * const dev = data->self;
	const struct mfd_sc16is75x_config * const config = dev->config;
	uint8_t iir[SC16IS75X_UART_CHANNELS_MAX] = {
		BIT(SC16IS75X_BIT_IIR_PENDING),
		BIT(SC16IS75X_BIT_IIR_PENDING)
	};
	enum mfd_sc16is75x_event event;
	bool retry = false; /* either IIR read error or until no pending */
	int ret = 0;

	/* Read all interrupt identification types in an atomic loop */
	k_mutex_lock(&data->transaction_lock, K_FOREVER);
	for (int ch = 0; ch < SC16IS75X_UART_CHANNELS_MAX; ch++) {
		ret = READ_SC16IS75X_CHREG(dev, ch, IIR, &iir[ch]);
		if (ret != 0) {
			LOG_WRN("%s: IIR[%d] read failed (lose IRQ reason): %d",
				dev->name, ch, ret);
			retry = true;
			break;
		}
	}
	k_mutex_unlock(&data->transaction_lock);

	if (retry) {
		LOG_WRN("%s: retry IRQ handling", dev->name);
		k_work_submit(&data->interrupt_work);
		return;
	};

	/* Sorting out and triggering callbacks for the various types */
	for (int ch = 0; ch < SC16IS75X_UART_CHANNELS_MAX; ch++) {
		uint8_t type = GET_FIELD(iir[ch], SC16IS75X_BIT_IIR_TYPE);

		/* channel has not fired (0: pending, 1: not pending) */
		if (IS_BIT_SET(iir[ch], SC16IS75X_BIT_IIR_PENDING)) {
			continue;
		};

		/* reset event number for each channel iterration */
		event = SC16IS75X_EVENT_MAX;

		if (type == SC16IS75X_INT_RXLSE) {          /* priority 1 */
			retry = true;
			event = ch ? SC16IS75X_EVENT_UART1_RXLSE
				   : SC16IS75X_EVENT_UART0_RXLSE;
		} else if (type == SC16IS75X_INT_RXTO) {    /* priority 2 */
			retry = true;
			event = ch ? SC16IS75X_EVENT_UART1_RXTO
				   : SC16IS75X_EVENT_UART0_RXTO;
		} else if (type == SC16IS75X_INT_RHRI) {    /* priority 2 */
			retry = true;
			event = ch ? SC16IS75X_EVENT_UART1_RHRI
				   : SC16IS75X_EVENT_UART0_RHRI;
		} else if (type == SC16IS75X_INT_THRI) {    /* priority 3 */
			retry = true;
			event = ch ? SC16IS75X_EVENT_UART1_THRI
				   : SC16IS75X_EVENT_UART0_THRI;
		} else if (type == SC16IS75X_INT_MSI) {     /* priority 4 */
			retry = true;
			event = ch ? SC16IS75X_EVENT_UART1_MSI
				   : SC16IS75X_EVENT_UART0_MSI;
		} else if (type == SC16IS75X_INT_IO) {      /* priority 5 */
			retry = true;
			event = ch ? SC16IS75X_EVENT_IO1_STATE
				   : SC16IS75X_EVENT_IO0_STATE;
		} else if (type == SC16IS75X_INT_XOFF) {    /* priority 6 */
			retry = true;
			event = ch ? SC16IS75X_EVENT_UART1_XOFF
				   : SC16IS75X_EVENT_UART0_XOFF;
		} else if (type == SC16IS75X_INT_HWFL) {    /* priority 7 */
			retry = true;
			event = ch ? SC16IS75X_EVENT_UART1_HWFL
				   : SC16IS75X_EVENT_UART0_HWFL;
		}

		if (event < SC16IS75X_EVENT_MAX) {
			gpio_fire_callbacks(&data->callbacks, data->self,
							      BIT(event));
		}
	}

	/* Resubmit handler to queue to look for further pending interrupts */
	if (retry) {
		k_work_submit(&data->interrupt_work);
		return;
	};

	/* Resubmit handler to queue if interrupt is still active */
	if (gpio_pin_get_dt(&config->interrupt) != 0) {
		k_work_submit(&data->interrupt_work);
		return;
	}
}

static void mfd_sc16is75x_interrupt_callback(const struct device *dev,
					     struct gpio_callback *cb,
					     gpio_port_pins_t pins)
{
	/*
	 * Handling interrupts requires bus operations, which we can't
	 * do from an ISR. Schedule a work item to do it instead.
	 */
	struct mfd_sc16is75x_data * const data = CONTAINER_OF(cb,
			struct mfd_sc16is75x_data, interrupt_cb);

	k_work_submit(&data->interrupt_work);
}

static int mfd_sc16is75x_init(const struct device *dev)
{
	const struct mfd_sc16is75x_config * const config = dev->config;
	struct mfd_sc16is75x_data * const data = dev->data;
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

	/* Configure reset GPIO pin, confirm device readiness first */
	if (gpio_is_ready_dt(&config->reset)) {
		ret = gpio_pin_configure_dt(&config->reset, GPIO_OUTPUT);
		if (ret != 0) {
			LOG_ERR("%s: configure reset pin failed: %d",
				dev->name, ret);
			goto end;
		}
	} else {
		LOG_ERR("%s: GPIO device %s with reset pin not ready",
			dev->name, config->reset.port->name);
		return -ENODEV;
	}

	/*
	 * Pull reset for a few µs, then wait another
	 * few µs for device startup.
	 */
	gpio_pin_set_dt(&config->reset, 1); /* assert */
	k_usleep(5);
	gpio_pin_set_dt(&config->reset, 0); /* deassert */
	k_usleep(5);

	/* Configure interrupt GPIO pin, confirm device readiness first */
	if (gpio_is_ready_dt(&config->interrupt)) {
		ret = gpio_pin_configure_dt(&config->interrupt, GPIO_INPUT);
		if (ret != 0) {
			LOG_ERR("%s: configure interrupt pin failed: %d",
				dev->name, ret);
			goto end;
		}
	} else {
		LOG_ERR("%s: GPIO device %s with interrupt pin not ready",
			dev->name, config->interrupt.port->name);
		return -ENODEV;
	}

	/* Set up interrupt handling */
	k_work_init(&data->interrupt_work, mfd_sc16is75x_interrupt_work_fn);

	gpio_init_callback(&data->interrupt_cb,
			   mfd_sc16is75x_interrupt_callback,
			   BIT(config->interrupt.pin));

	ret = gpio_add_callback_dt(&config->interrupt, &data->interrupt_cb);
	if (ret < 0) {
		goto end;
	}

	/* Enable interrupts */
	ret = gpio_pin_interrupt_configure_dt(&config->interrupt,
					      GPIO_INT_EDGE_TO_ACTIVE);
	if (ret != 0) {
		LOG_ERR("%s: enable interrupt on interrupt pin failed: %d",
			dev->name, ret);
		goto end;
	}

end:
	return ret;
}

#ifdef CONFIG_PM_DEVICE
static int mfd_sc16is75x_pm_device_pm_action(const struct device *dev,
					     enum pm_device_action action)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(action);

	return 0;
}
#endif

#define MFD_SC16IS75X_DEFINE_SPI_BUS(inst)                                   \
	.spi = SPI_DT_SPEC_INST_GET(inst, SPI_OP_MODE_MASTER |               \
					  SPI_WORD_SET(8), 0),               \
	.bus_init = mfd_sc16is75x_spi_init

#define MFD_SC16IS75X_DEFINE_I2C_BUS(inst)                                   \
	.i2c = I2C_DT_SPEC_INST_GET(inst),                                   \
	.bus_init = mfd_sc16is75x_i2c_init

#define MFD_SC16IS75X_DEFINE_BUS(inst)                                       \
	COND_CODE_1(DT_INST_ON_BUS(inst, spi),                               \
			(MFD_SC16IS75X_DEFINE_SPI_BUS(inst)),                \
			(MFD_SC16IS75X_DEFINE_I2C_BUS(inst)))

#define MFD_SC16IS75X_DEFINE(inst)                                           \
                                                                             \
	static struct mfd_sc16is75x_config mfd_sc16is75x_config_##inst =     \
	{                                                                    \
		MFD_SC16IS75X_DEFINE_BUS(inst),                              \
		.reset = GPIO_DT_SPEC_INST_GET(inst, reset_gpios),           \
		.interrupt = GPIO_DT_SPEC_INST_GET(inst, interrupt_gpios),   \
	};                                                                   \
                                                                             \
	static struct mfd_sc16is75x_data mfd_sc16is75x_data_##inst;          \
                                                                             \
	PM_DEVICE_DT_INST_DEFINE(inst, mfd_sc16is75x_pm_device_pm_action);   \
                                                                             \
	DEVICE_DT_INST_DEFINE(inst, mfd_sc16is75x_init,                      \
			      PM_DEVICE_DT_INST_GET(inst),                   \
			      &mfd_sc16is75x_data_##inst,                    \
			      &mfd_sc16is75x_config_##inst, POST_KERNEL,     \
			      CONFIG_MFD_SC16IS75X_INIT_PRIORITY, NULL);

DT_INST_FOREACH_STATUS_OKAY(MFD_SC16IS75X_DEFINE);
