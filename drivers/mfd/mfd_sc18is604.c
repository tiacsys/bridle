/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
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

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(mfd_sc18is604, CONFIG_MFD_LOG_LEVEL);

/*
 * Values in Hz, intentionally to be comparable with the spi-max-frequency
 * property from DT bindings in spi-device.yaml.
 */
#define MFD_SC18IS604_SPI_HZ_MIN		100000
#define MFD_SC18IS604_SPI_HZ_MAX		1200000

#define MFD_SC18IS604_SPI_DELAY_USEC		8 /* between two SPI bytes */
#define MFD_SC18IS604_RESET_SETUP_USEC		1 /* >= 125ns acceptance time */
#define MFD_SC18IS604_RESET_TIME_USEC		500

/* timeout for about two times a maximum command (three byte) at 100kHz */
#define MFD_SC18IS604_CMD_MAX_TOUT_USEC		200

/* expected chip in version string */
#define MFD_SC18IS604_VERSION_CHIP		"SC18IS604"
BUILD_ASSERT(
	ARRAY_SIZE(MFD_SC18IS604_VERSION_CHIP) <= SC18IS604_VERSION_STRING_SIZE,
	"Chip name too long"
);

/**
 * @brief SC18IM604 MFD configuration data
 *
 * @a interrupt must be set to a valid input pin with interrupt capability.
 * @a reset must be set to a valid output pin.
 *
 * This structure contains all of the state for a given SC18IM604 MFD
 * controller as well as the binding to related SPI device.
 */
typedef struct mfd_sc18is604_config {
	const struct spi_dt_spec spi;
	const struct gpio_dt_spec interrupt;
	const struct gpio_dt_spec reset;
} mfd_sc18is604_config_t;

/**
 * @brief SC18IM604 MFD data
 *
 * This structure contains data structures used by a SC18IM604 MFD.
 *
 * Interrupt propagation is handled by @a k_sem. Changes to
 * @ref mfd_sc18is604_data and @ref mfd_sc18is604_config are
 * synchronized using @a k_mutex.
 */
typedef struct mfd_sc18is604_data {
	const struct device *dev;
	uint8_t version[SC18IS604_VERSION_STRING_SIZE];
	struct k_mutex lock;
	struct k_sem interrupt_raised;
	struct gpio_callback interrupt_callback;
	struct k_work interrupt_work;
} mfd_sc18is604_data_t;

int mfd_sc18is604_claim(const struct device *dev)
{
	mfd_sc18is604_data_t * const data = dev->data;

	return k_mutex_lock(&data->lock, K_FOREVER);
}

int mfd_sc18is604_release(const struct device *dev)
{
	mfd_sc18is604_data_t * const data = dev->data;

	return k_mutex_unlock(&data->lock);
}

struct k_sem *mfd_sc18is604_interrupt_sem_get(const struct device *dev)
{
	mfd_sc18is604_data_t * const data = dev->data;

	return &data->interrupt_raised;
}

int mfd_sc18is604_transfer(const struct device *dev,
			   uint8_t *cmd, size_t cmd_len,
			   uint8_t *tx_data, size_t tx_len,
			   uint8_t *rx_data, size_t rx_len)
{
	/*
	 * The SC18IS604 requires significant delay between each byte
	 * sent via SPI. We achieve this by sending bytes in individual
	 * transactions, but keeping the CS line set, and the device
	 * locked, until we explicitly release it (see the flags
	 * SPI_HOLD_ON_CS and SPI_LOCK_ON set in device init).
	 */

	const mfd_sc18is604_config_t * const config = dev->config;
	int ret = 0;

	struct spi_buf buffer = {
		.buf = NULL,
		.len = 1,
	};

	const struct spi_buf_set buf_set = {
		.buffers = &buffer,
		.count = 1
	};

	/*
	 * Lock device. Putting this gate here ensures a calling thread
	 * can't "forget" to check for existing locks, but still allows
	 * a thread to pass through if it holds an "outer" lock. This
	 * way a caller can guarantee that a complex transaction is not
	 * interrupted.
	 */
	mfd_sc18is604_claim(dev);

	/* Write command sequence */
	if (cmd != NULL) {
		for (int i = 0; i < cmd_len; i++) {
			buffer.buf = &cmd[i];

			ret = spi_write_dt(&config->spi, &buf_set);
			if (ret != 0) {
				goto end;
			}

			k_busy_wait(MFD_SC18IS604_SPI_DELAY_USEC);
		}
	}

	/* Write data */
	if (tx_data != NULL) {
		for (int i = 0; i < tx_len; i++) {
			buffer.buf = &tx_data[i];

			ret = spi_write_dt(&config->spi, &buf_set);
			if (ret != 0) {
				goto end;
			}

			k_busy_wait(MFD_SC18IS604_SPI_DELAY_USEC);
		}
	}

	/* Read data */
	if (rx_data != NULL) {
		for (int i = 0; i < rx_len; i++) {
			buffer.buf = &rx_data[i];

			ret = spi_read_dt(&config->spi, &buf_set);
			if (ret != 0) {
				goto end;
			}

			k_busy_wait(MFD_SC18IS604_SPI_DELAY_USEC);
		}
	}

end:
	/*
	 * Releases the SPI bus itself, which we locked
	 * with our first spi_write_dt call.
	 */
	spi_release_dt(&config->spi);

	/*
	 * Release the lock on the bridge device.
	 * Potential "outer" locks will persist.
	 */
	mfd_sc18is604_release(dev);

	return ret;
}

int mfd_sc18is604_write_register(const struct device *dev,
				 uint8_t reg, uint8_t value)
{
	uint8_t cmd[] = {SC18IS604_CMD_WRITE_REGISTER, reg};

	return mfd_sc18is604_transfer(dev, cmd, ARRAY_SIZE(cmd),
					   &value, 1, NULL, 0);
}

int mfd_sc18is604_read_register(const struct device *dev,
				uint8_t reg, uint8_t *value)
{
	uint8_t cmd[] = {SC18IS604_CMD_READ_REGISTER, reg};

	return mfd_sc18is604_transfer(dev, cmd, ARRAY_SIZE(cmd),
					   NULL, 0, value, 1);
}

int mfd_sc18is604_read_buffer(const struct device *dev,
			      uint8_t *data, size_t len)
{
	uint8_t cmd[] = {SC18IS604_CMD_READ_BUFFER};

	return mfd_sc18is604_transfer(dev, cmd, ARRAY_SIZE(cmd),
					   NULL, 0, data, len);
}

/**
 * @brief Request device version string. The string will be placed in the
 *        internal buffer. The device interrupt is set once the string is
 *        ready to be read from the buffer.
 *
 * @param dev An SC18IS604 MFD device.
 * @return A value from mfd_sc18is604_transfer().
 */
static int mfd_sc18is604_request_version_string(const struct device *dev)
{
	uint8_t cmd[] = {SC18IS604_CMD_VERSION_STRING};

	return mfd_sc18is604_transfer(dev, cmd, ARRAY_SIZE(cmd),
					   NULL, 0, NULL, 0);
}

static int mfd_sc18is604_clear_interrupt_source(const struct device *dev)
{
	uint8_t buf = 0;
	/* Reset interrupt by reading from I2CStat register. */
	/* FIXME: provide macro */
	int ret = mfd_sc18is604_read_register(dev, SC18IS604_REG_I2C_STATUS, &buf);

	/* LOG_WRN("%s: I2C STATUS: 0x%02X", dev->name, buf); */
	return ret;
}

static void mfd_sc18is604_interrupt_work_fn(struct k_work *work)
{
	mfd_sc18is604_data_t * const data = CONTAINER_OF(work,
							 mfd_sc18is604_data_t,
							 interrupt_work);
	const struct device * const dev = data->dev;

	/* Clear hardware signal. */
	mfd_sc18is604_clear_interrupt_source(dev);

	/* Propagate software signal. */
	k_sem_give(&data->interrupt_raised);
}

static void mfd_sc18is604_interrupt_callback(const struct device *dev,
					     struct gpio_callback *cb,
					     gpio_port_pins_t pins)
{
	mfd_sc18is604_data_t * const data = CONTAINER_OF(cb,
							 mfd_sc18is604_data_t,
							 interrupt_callback);

	/*
	 * Resetting the interrupt involves SPI communication,
	 * so we can't do it from the ISR, trigger worker.
	 */
	k_work_submit(&data->interrupt_work);
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
	mfd_sc18is604_data_t * const data = dev->data;
	int ret = 0;

	if (gpio->port != NULL) {
		LOG_DBG("%s: bind GPIO port %s, pin %d to interrupt handling",
			dev->name, gpio->port->name, gpio->pin);

		mfd_sc18is604_claim(dev);

		ret = gpio_pin_interrupt_configure_dt(gpio, flags);
		if (ret != 0) {
			LOG_ERR("%s: couldn't enable interrupt on GPIO pin %d",
				dev->name, gpio->pin);
			goto end;
		}

		/* Set back-pointer to device for interrupt callback. */
		data->dev = dev;

		/* Initialize interrupt raising propagation. */
		k_sem_init(&data->interrupt_raised, 0, 1);
		k_work_init(&data->interrupt_work, mfd_sc18is604_interrupt_work_fn);

		gpio_init_callback(&data->interrupt_callback,
				   mfd_sc18is604_interrupt_callback,
				   BIT(gpio->pin));

		ret = gpio_add_callback_dt(gpio, &data->interrupt_callback);
		if (ret != 0) {
			LOG_ERR("%s: couldn't register callback on GPIO port %s",
				dev->name, gpio->port->name);
			goto end;
		}
	} else {
		return -EINVAL;
	}

end:
	mfd_sc18is604_release(dev);
	return ret;
}

/**
 * @brief Set up GPIO pin.
 *
 * @param dev An SC18IS604 MFD device.
 * @param gpio The GPIO specification from devicetree.
 * @param flags Additional GPIO flags.
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

		mfd_sc18is604_claim(dev);

		ret = gpio_pin_configure_dt(gpio, flags);
		if (ret != 0) {
			LOG_ERR("%s: couldn't configure GPIO pin %d",
				dev->name, gpio->pin);
			goto end;
		}
	} else {
		return -EINVAL;
	}

end:
	mfd_sc18is604_release(dev);
	return ret;
}

/**
 * @brief Reset device.
 *
 * @param dev An SC18IS604 MFD device.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
static int mfd_sc18is604_chip_reset(const struct device *dev)
{
	const mfd_sc18is604_config_t * const config = dev->config;
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
 * @brief Confirm version string.
 *
 * @param dev An SC18IS604 MFD device.
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
static int mfd_sc18is604_check_chipid(const struct device *dev)
{
	mfd_sc18is604_data_t * const data = dev->data;
	int ret = 0;

	LOG_DBG("%s: confirm device version", dev->name);
	ret = mfd_sc18is604_request_version_string(dev);
	if (ret != 0) {
		LOG_ERR("%s: version command failed: %d", dev->name, ret);
		goto end;
	}

	/* FIXME: make this better to avoid dead lock, when no device connected */
	ret = k_sem_take(&data->interrupt_raised,
			 K_USEC(MFD_SC18IS604_CMD_MAX_TOUT_USEC));
	if (ret != 0) {
		LOG_ERR("%s: interrupt timeout, check hardware wiring: %d",
			dev->name, ret);
		goto end;
	}

	ret = mfd_sc18is604_read_buffer(dev, data->version,
					     ARRAY_SIZE(data->version));
	if (strncmp(MFD_SC18IS604_VERSION_CHIP, data->version,
		    strlen(MFD_SC18IS604_VERSION_CHIP)) != 0) {
		LOG_ERR("%s: version mismatch, got %s",
			dev->name, data->version);
		return -ENODEV;
	}

end:
	return ret;
}

static int mfd_sc18is604_init(const struct device *dev)
{
	const mfd_sc18is604_config_t * const config = dev->config;
	mfd_sc18is604_data_t * const data = dev->data;
	int ret = 0;

	/* Check parent bus readiness for bridge. */
	if (!spi_is_ready_dt(&config->spi)) {
		LOG_ERR("%s: SPI device %s not ready",
			dev->name, config->spi.bus->name);
		return -ENODEV;
	}

	/* Initialize device lock. */
	k_mutex_init(&data->lock);

	/* Configure interrupt input pin. */
	ret = mfd_sc18is604_configure_gpio_pin(dev, &config->interrupt,
						    GPIO_INPUT);
	if (ret != 0) {
		LOG_ERR("%s: interrupt GPIO port not given", dev->name);
		return -EINVAL;
	}

	/* Set up interrupt handling */
	ret = mfd_sc18is604_bind_interrupt(dev, &config->interrupt,
						GPIO_INT_EDGE_TO_ACTIVE);
	if (ret != 0) {
		LOG_ERR("%s: interrupt callback binding failed", dev->name);
		goto end;
	}

	/* Configure reset output pin. */
	ret = mfd_sc18is604_configure_gpio_pin(dev, &config->reset,
						    GPIO_OUTPUT_INACTIVE);
	if (ret != 0) {
		LOG_WRN("%s: reset GPIO port not given (work w/o chip reset)",
			dev->name);
	}

	/* Reset device. */
	ret = mfd_sc18is604_chip_reset(dev);
	if (ret != 0) {
		LOG_ERR("%s: couldn't reset device", dev->name);
		goto end;
	}

#if 0
	ret = mfd_sc18is604_clear_interrupt_source(dev);
	if (ret != 0) {
		LOG_ERR("%s: couldn't clear interrupt source", dev->name);
	}
#endif

	/* Confirm version string */
	ret = mfd_sc18is604_check_chipid(dev);
	if (ret != 0) {
		LOG_ERR("%s: version string read out failed: %d",
			dev->name, ret);
		goto end;
	}

	LOG_DBG("%s: ready with %s over %s!",
		dev->name, data->version, config->spi.bus->name);

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
	static const mfd_sc18is604_config_t mfd_sc18is604_config_##inst =    \
	{                                                                    \
		.spi = SPI_DT_SPEC_INST_GET(inst, SPI_OP_MODE_MASTER |       \
						  SPI_TRANSFER_MSB |         \
						  SPI_HOLD_ON_CS |           \
						  SPI_LOCK_ON |              \
						  SPI_MODE_CPOL |            \
						  SPI_MODE_CPHA |            \
						  SPI_WORD_SET(8), 0),       \
		.interrupt = GPIO_DT_SPEC_INST_GET(inst, int_gpios),         \
		.reset = GPIO_DT_SPEC_INST_GET_OR(inst, reset_gpios, { 0 }), \
	};                                                                   \
	BUILD_ASSERT(DT_INST_PROP(inst, spi_max_frequency)                   \
					>= MFD_SC18IS604_SPI_HZ_MIN,         \
		     "SPI bus clock too low");                               \
	BUILD_ASSERT(DT_INST_PROP(inst, spi_max_frequency)                   \
					<= MFD_SC18IS604_SPI_HZ_MAX,         \
		     "SPI bus clock too high");                              \
                                                                             \
                                                                             \
	static mfd_sc18is604_data_t mfd_sc18is604_data_##inst = {            \
		.version = { 0 },                                            \
	};                                                                   \
                                                                             \
	PM_DEVICE_DT_INST_DEFINE(inst, mfd_sc18is604_pm_device_pm_action);   \
                                                                             \
	DEVICE_DT_INST_DEFINE(inst, mfd_sc18is604_init,                      \
			      PM_DEVICE_DT_INST_GET(inst),                   \
			      &mfd_sc18is604_data_##inst,                    \
			      &mfd_sc18is604_config_##inst, POST_KERNEL,     \
			      CONFIG_MFD_SC18IS604_INIT_PRIORITY, NULL);

DT_INST_FOREACH_STATUS_OKAY(MFD_SC18IS604_DEFINE);
