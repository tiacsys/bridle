/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief MFD Driver for an SC18IM604 bridge
 */

#define DT_DRV_COMPAT nxp_sc18is604

#include <string.h>

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/pm/device.h>

#include <zephyr/drivers/spi.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/gpio/gpio_utils.h>

#include <zephyr/drivers/mfd/sc18is604.h>

#include "mfd_sc18is604.h"

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(mfd_sc18is604, CONFIG_MFD_LOG_LEVEL);

#if defined(CONFIG_MFD_SC18IS604_ASYNC) \
	&& (!CONFIG_DYNAMIC_THREAD_POOL_SIZE && !defined(CONFIG_DYNAMIC_THREAD_ALLOC))
#error "SC18IS604 MFD driver requires either CONFIG_DYNAMIC_THREAD_POOL_SIZE>0" \
	"or CONFIG_DYNAMIC_THREAD_ALLOC"
#endif

int mfd_sc18is604_add_callback(const struct device *dev,
			       struct gpio_callback *callback)
{
	struct mfd_sc18is604_data * const data = dev->data;

	return gpio_manage_callback(&data->child_callbacks, callback, true);
}

int mfd_sc18is604_remove_callback(const struct device *dev,
				  struct gpio_callback *callback)
{
	struct mfd_sc18is604_data * const data = dev->data;

	return gpio_manage_callback(&data->child_callbacks, callback, false);
}

int mfd_sc18is604_claim(const struct device *dev, k_timeout_t timeout)
{
	struct mfd_sc18is604_data * const data = dev->data;

	return k_sem_take(&data->lock, timeout);
}

void mfd_sc18is604_release(const struct device *dev)
{
	struct mfd_sc18is604_data * const data = dev->data;

	k_sem_give(&data->lock);
}

/**
 * @brief Request device version string. The string will be placed in the
 *        internal buffer. The device interrupt is set once the string is
 *        ready to be read from the buffer.
 *
 * @param dev An SC18IS604 MFD device.
 *
 * @return A value from mfd_sc18is604_transfer().
 */
static int mfd_sc18is604_request_version_string(const struct device *dev)
{
	uint8_t cmd[] = {SC18IS604_CMD_VERSION_STRING};

	return mfd_sc18is604_transfer(dev, cmd, ARRAY_SIZE(cmd),
				      NULL, 0, NULL, 0);
}

/**
 * @brief Set up GPIO pin.
 *
 * @param dev An SC18IS604 MFD device.
 * @param gpio The GPIO specification from devicetree.
 * @param flags Additional GPIO flags.
 *
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
static int mfd_sc18is604_configure_gpio_pin(const struct device *dev,
					    const struct gpio_dt_spec *gpio,
					    const gpio_flags_t flags)
{
	int ret = 0;

	if (gpio->port != NULL) {
		LOG_DBG("%s: configure GPIO port %s, pin %d",
			dev->name, gpio->port->name, gpio->pin);

		if (!gpio_is_ready_dt(gpio)) {
			LOG_ERR("%s: GPIO port %s not ready",
				dev->name, gpio->port->name);
			return -ENODEV;
		}

		ret = gpio_pin_configure_dt(gpio, flags);
		if (ret != 0) {
			LOG_ERR("%s: couldn't configure GPIO pin %d",
				dev->name, gpio->pin);
			return ret;
		}
	} else {
		return -EINVAL;
	}

	return 0;
}

/**
 * @brief Reset device.
 *
 * @param dev An SC18IS604 MFD device.
 *
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
static int mfd_sc18is604_chip_reset(const struct device *dev)
{
	const struct mfd_sc18is604_config * const config = dev->config;
	int ret = 0;

	LOG_DBG("%s: resetting device", dev->name);
	if (config->reset.port != NULL) {
		ret = gpio_pin_set_dt(&config->reset, 1);
		if (ret != 0)
			goto end;

		/* Should suffice to pull for reset acceptance time. */
		k_busy_wait(MFD_SC18IS604_RESET_SETUP_USEC);

		ret = gpio_pin_set_dt(&config->reset, 0);
		if (ret != 0)
			goto end;

		/*
		 * Device needs some time before becoming
		 * responsive again after reset.
		 */
		k_busy_wait(MFD_SC18IS604_RESET_TIME_USEC);
	}

end:
	return ret;
}

/**
 * @brief Apply register default values.
 *
 * @param dev An SC18IS604 MFD device.
 *
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
static int mfd_sc18is604_reset_state_apply(const struct device *dev)
{
	static const uint8_t reset_state[][2] = {
		{SC18IS604_REG_IO_CONFIG, 0},
		{SC18IS604_REG_IO_STATE, 0},
		{SC18IS604_REG_I2C_CLOCK, 0x19},
		{SC18IS604_REG_I2C_TIMEOUT, 0},
		{SC18IS604_REG_I2C_ADDRESS, 0},
	};
	int ret = 0;

	LOG_WRN("%s: apply register reset state", dev->name);
	for (int i = 0; i < ARRAY_SIZE(reset_state); ++i) {
		ret = mfd_sc18is604_write_register(dev, reset_state[i][0],
							reset_state[i][1]);
		if (ret != 0) {
			LOG_ERR("%s: failed to reset register %02x: %d",
				dev->name, reset_state[i][0], ret);
			goto end;
		}
	}

end:
	return ret;
}

static int mfd_sc18is604_clear_interrupt_source(const struct device *dev)
{
	uint8_t buf = 0;

	/* Reset interrupt by reading from I2CStat register. */
	int ret = READ_SC18IS604_REG(dev, I2C_STATUS, &buf);

	return ret;
}

static void mfd_sc18is604_interrupt_callback(const struct device *dev,
					     struct gpio_callback *cb,
					     gpio_port_pins_t pins)
{
	struct mfd_sc18is604_data * const data = CONTAINER_OF(cb,
			struct mfd_sc18is604_data, interrupt_cb);

	/* Raise internal signal */
	k_sem_give(&data->interrupt_signal);

	/* Fire registered callbacks */
	gpio_fire_callbacks(&data->child_callbacks, dev, pins);
}

static int mfd_sc18is604_check_chipid(const struct device *dev,
				      k_timeout_t timeout)
{
	struct mfd_sc18is604_data * const data = dev->data;
	int ret = 0;

	/* Lock device */
	ret = mfd_sc18is604_claim(dev, timeout);
	if (ret != 0) {
		return -ETIMEDOUT;
	}

	/* Prepare signal for interrupt signaling */
	k_sem_reset(&data->interrupt_signal);

	/* Send command to place ID string in device buffer */
	ret = mfd_sc18is604_request_version_string(dev);
	if (ret != 0) {
		ret = -EIO;
		goto release_and_return;
	}

	/* Await interrupt signaling completion */
	ret = k_sem_take(&data->interrupt_signal, timeout);
	if (ret != 0) {
		ret = -ETIMEDOUT;
		goto release_and_return;
	}

	/*
	 * Clear hardware interrupt signal, because the simple
	 * data transfer by mfd_sc18is604_request_version_string()
	 * causes at least one interrupt that can not handled
	 * by the central MFD callback (missing interrupt source
	 * identification inside the chip, only I2C events are
	 * identifiable by the interrupt callback).
	 */
	mfd_sc18is604_clear_interrupt_source(dev);

	/* Read generated string from device buffer */
	char id[SC18IS604_VERSION_STRING_SIZE] = {0};

	ret = mfd_sc18is604_read_buffer(dev, (uint8_t *) id,
					SC18IS604_VERSION_STRING_SIZE);
	if (ret != 0) {
		ret = -EIO;
		goto release_and_return;
	}

	/* Compare with expected value */
	if (strncmp(MFD_SC18IS604_VERSION_CHIP, id,
			strlen(MFD_SC18IS604_VERSION_CHIP)) != 0) {
		LOG_ERR("%s: chip mismatch: expected %s, got %s",
			dev->name, MFD_SC18IS604_VERSION_CHIP, id);
		ret = -ENODEV;
		goto release_and_return;
	}

	LOG_INF("%s: found \"%s\"", dev->name, id);

release_and_return:
	mfd_sc18is604_release(dev);
	return ret;
}

/**
 * @brief Set up interrupt handling.
 *
 * @param dev An SC18IS604 MFD device.
 * @param gpio The GPIO specification from devicetree.
 * @param flags Additional GPIO flags.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
static int mfd_sc18is604_bind_interrupt(const struct device *dev,
					const struct gpio_dt_spec *gpio,
					const gpio_flags_t flags)
{
	struct mfd_sc18is604_data * const data = dev->data;
	int ret = 0;

	if (gpio->port == NULL) {
		return -EINVAL;
	}

	LOG_DBG("%s: bind GPIO port %s, pin %d to interrupt handling",
		dev->name, gpio->port->name, gpio->pin);

	ret = gpio_pin_interrupt_configure_dt(gpio, flags);
	if (ret != 0) {
		LOG_ERR("%s: couldn't enable interrupt on GPIO pin %d",
			dev->name, gpio->pin);
		return ret;
	}

	gpio_init_callback(&data->interrupt_cb,
			   mfd_sc18is604_interrupt_callback,
			   BIT(gpio->pin));

	ret = gpio_add_callback_dt(gpio, &data->interrupt_cb);
	if (ret != 0) {
		LOG_ERR("%s: couldn't register callback on GPIO port %s",
			dev->name, gpio->port->name);
		return ret;
	}

	return 0;
}

static int mfd_sc18is604_init(const struct device *dev)
{
	const struct mfd_sc18is604_config * const config = dev->config;
	struct mfd_sc18is604_data * const data = dev->data;
	int ret = 0;

	/* Check parent bus readiness for bridge. */
	if (!spi_is_ready_dt(&config->spi)) {
		LOG_ERR("%s: SPI device %s not ready",
			dev->name, config->spi.bus->name);
		return -ENODEV;
	}

	/* Set driver instance back reference */
	data->dev = dev;

	/* Initialize bus lock (initially open) */
	k_sem_init(&data->lock, 1, 1);

	/* Initialize interrupt signal (initially closed) */
	k_sem_init(&data->interrupt_signal, 0, 1);

#ifdef CONFIG_MFD_SC18IS604_ASYNC
	/* Initialize private work queue. */
	size_t work_queue_stack_size = CONFIG_MFD_SC18IS604_WORKQUEUE_STACK_SIZE;

	k_work_queue_init(&data->work_queue);
	data->work_queue_stack = k_thread_stack_alloc(work_queue_stack_size, 0);
	k_work_queue_start(&data->work_queue, data->work_queue_stack,
			   work_queue_stack_size, K_HIGHEST_THREAD_PRIO, NULL);
#endif /* CONFIG_MFD_SC18IS604_ASYNC */

	/* Configure interrupt input pin. */
	ret = mfd_sc18is604_configure_gpio_pin(dev, &config->interrupt,
						    GPIO_INPUT);
	if (ret != 0) {
		LOG_ERR("%s: interrupt GPIO pin configuration failed: %d",
			dev->name, ret);
		goto end;
	}

	/* Set up interrupt handling */
	ret = mfd_sc18is604_bind_interrupt(dev, &config->interrupt,
						GPIO_INT_EDGE_TO_ACTIVE);
	if (ret != 0) {
		LOG_ERR("%s: interrupt callback binding failed: %d",
			dev->name, ret);
		goto end;
	}

	/* Configure reset output pin. */
	ret = mfd_sc18is604_configure_gpio_pin(dev, &config->reset,
						    GPIO_OUTPUT_INACTIVE);
	if (ret != 0) {
		LOG_WRN("%s: reset GPIO pin configuration failed "
			"(work w/o chip reset)", dev->name);

		/* Reset device by applying register reset states. */
		ret = mfd_sc18is604_reset_state_apply(dev);
		if (ret != 0) {
			LOG_ERR("%s: couldn't apply reset states: %d",
				dev->name, ret);
			goto end;
		}

		/* Clear hardware interrupt signal (like real reset do) */
		mfd_sc18is604_clear_interrupt_source(dev);

	} else {

		/* Reset device. */
		ret = mfd_sc18is604_chip_reset(dev);
		if (ret != 0) {
			LOG_ERR("%s: couldn't reset device: %d",
				dev->name, ret);
			goto end;
		}
	}

	/* Check Chip ID */
	ret = mfd_sc18is604_check_chipid(dev, K_SECONDS(5));
	if (ret != 0) {
		LOG_ERR("%s: couldn't read chip ID: %d", dev->name, ret);
		return ret;
	}

end:
	return ret;
}

#ifdef CONFIG_PM_DEVICE
static int mfd_sc18is604_pm_device_pm_action(const struct device *dev,
					     enum pm_device_action action)
{
	ARG_UNUSED(dev);
	ARG_UNUSED(action);

	return 0;
}
#endif

#define MFD_SC18IS604_DEFINE(inst)                                           \
                                                                             \
	static const                                                         \
	struct mfd_sc18is604_config mfd_sc18is604_config_##inst =            \
	{                                                                    \
		.spi = SPI_DT_SPEC_INST_GET(inst, SPI_OP_MODE_MASTER |       \
						  SPI_TRANSFER_MSB |         \
						  SPI_HOLD_ON_CS |           \
						  SPI_LOCK_ON |              \
						  SPI_MODE_CPOL |            \
						  SPI_MODE_CPHA |            \
						  SPI_WORD_SET(8), 0),       \
		.interrupt = GPIO_DT_SPEC_INST_GET(inst, interrupt_gpios),   \
		.reset = GPIO_DT_SPEC_INST_GET_OR(inst, reset_gpios, { 0 }), \
	};                                                                   \
	BUILD_ASSERT(DT_INST_PROP(inst, spi_max_frequency)                   \
					>= MFD_SC18IS604_SPI_HZ_MIN,         \
			 "SPI bus clock too low");                           \
	BUILD_ASSERT(DT_INST_PROP(inst, spi_max_frequency)                   \
					<= MFD_SC18IS604_SPI_HZ_MAX,         \
			 "SPI bus clock too high");                          \
                                                                             \
	static struct mfd_sc18is604_data mfd_sc18is604_data_##inst = { 0 };  \
                                                                             \
	PM_DEVICE_DT_INST_DEFINE(inst, mfd_sc18is604_pm_device_pm_action);   \
                                                                             \
	DEVICE_DT_INST_DEFINE(inst, mfd_sc18is604_init,                      \
			      PM_DEVICE_DT_INST_GET(inst),                   \
			      &mfd_sc18is604_data_##inst,                    \
			      &mfd_sc18is604_config_##inst, POST_KERNEL,     \
			      CONFIG_MFD_SC18IS604_INIT_PRIORITY, NULL);

DT_INST_FOREACH_STATUS_OKAY(MFD_SC18IS604_DEFINE);
