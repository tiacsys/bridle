/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef ZEPHYR_DRIVERS_MFD_SC16IS75X_H_
#define ZEPHYR_DRIVERS_MFD_SC16IS75X_H_

#ifdef __cplusplus
extern "C" {
#endif

#define DT_DRV_COMPAT nxp_sc16is75x

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/pm/device.h>
#include <zephyr/drivers/gpio.h>

#if DT_ANY_INST_ON_BUS_STATUS_OKAY(spi)
#include <zephyr/drivers/spi.h>
#endif /* DT_ANY_INST_ON_BUS_STATUS_OKAY(spi) */

#if DT_ANY_INST_ON_BUS_STATUS_OKAY(i2c)
#include <zephyr/drivers/i2c.h>
#endif /* DT_ANY_INST_ON_BUS_STATUS_OKAY(i2c) */

/**
 * @brief SC16IS75X MFD configuration data
 *
 * @a interrupt must be set to a valid input pin with interrupt capability.
 * @a reset must be set to a valid output pin.
 *
 * This structure contains all of the state for a given SC16IS75X MFD
 * controller as well as the binding to related SPI or I2C device.
 */
struct mfd_sc16is75x_config {
#if DT_ANY_INST_ON_BUS_STATUS_OKAY(spi)
	struct spi_dt_spec spi;
#endif /* DT_ANY_INST_ON_BUS_STATUS_OKAY(spi) */
#if DT_ANY_INST_ON_BUS_STATUS_OKAY(i2c)
	struct i2c_dt_spec i2c;
#endif /* DT_ANY_INST_ON_BUS_STATUS_OKAY(i2c) */
	/** bus specific initialization function (SPI or I2C) */
	int (*bus_init)(const struct device *dev);
	/** GPIO pin for chip reset */
	struct gpio_dt_spec reset;
};

/**
 * @brief SC16IS75X MFD bus transfer functions
 *
 * The SC16IS75X supports either SPI or I2C bus communiation. Depending
 * on the device tree definitions, the driver automatically selects the
 * correct transfer functions for reading and writing raw data.
 */
struct mfd_sc16is75x_transfer_function {
	/** read raw data */
	int (*read_raw)(const struct device *dev, const uint8_t sub_address,
			uint8_t *buf, const size_t len);
	/** write raw data */
	int (*write_raw)(const struct device *dev, const uint8_t sub_address,
			 const uint8_t *buf, const size_t len);
};

/**
 * @brief SC16IS75X MFD data
 *
 * This structure contains data structures used by a SC16IS75X MFD.
 *
 * Combined register access sequences, either multiple read, multiple write or
 * mixed read and write, are synchronized using @a k_mutex.
 */
struct mfd_sc16is75x_data {
	/** Back refernce to driver instance */
	const struct device *self;
	/** bus specific transfer functions (SPI or I2C) */
	const struct mfd_sc16is75x_transfer_function *transfer_function;
	/** Mutex to allow locking across multiple transactions */
	struct k_mutex transaction_lock;
};

int mfd_sc16is75x_spi_init(const struct device *dev);
int mfd_sc16is75x_i2c_init(const struct device *dev);

#ifdef __cplusplus
}
#endif

#endif /* ZEPHYR_DRIVERS_MFD_SC16IS75X_H_*/
