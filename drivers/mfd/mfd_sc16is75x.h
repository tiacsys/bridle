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
#include <zephyr/drivers/mfd/sc16is75x.h>

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
	/** Number of UART channels provided by this device. */
	uint8_t n_channels;
	/** UART channel numbers. */
	uint8_t channels[SC16IS75X_UART_CHANNELS_MAX];
#ifdef CONFIG_MFD_SC16IS75X_INTERRUPTS
	/** GPIO pin for interrupt requests */
	struct gpio_dt_spec interrupt;
#endif /* CONFIG_MFD_SC16IS75X_INTERRUPTS */
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
#ifdef CONFIG_MFD_SC16IS75X_ASYNC
	int (*read_raw_signal)(const struct device *dev, const uint8_t sub_address,
			       uint8_t *buf, const size_t len,
			       struct k_poll_signal *signal);
#endif /* CONFIG_MFD_SC16IS75X_ASYNC */
};

#ifdef CONFIG_MFD_SC16IS75X_ASWQ

/**
 * @brief Bus agnostic asynchronous read function.
 */
int mfd_sc16is75x_read_raw_signal(const struct device *dev,
				  const uint8_t sub_address,
				  uint8_t *buf, const size_t len,
				  struct k_poll_signal *signal);

#endif /* CONFIG_MFD_SC16IS75X_ASWQ */

#ifdef CONFIG_MFD_SC16IS75X_INTERRUPTS

/**
 * @brief SC16IS75X MFD data for asynchronous interrupt handling
 */
struct sc16is75x_interrupt_data {
	/** IIR value per channels */
	uint8_t iir[SC16IS75X_UART_CHANNELS_MAX];
	/** asynchronous notification signal per channel */
	struct k_poll_signal signals[SC16IS75X_UART_CHANNELS_MAX];
};

#endif /* CONFIG_MFD_SC16IS75X_INTERRUPTS */

/**
 * @brief SC16IS75X MFD data
 *
 * This structure contains data structures used by a SC16IS75X MFD.
 *
 * Combined register access sequences, either multiple read, multiple write
 * or mixed read and write, are synchronized using @a k_mutex.
 */
struct mfd_sc16is75x_data {
	/** Back refernce to driver instance */
	const struct device *self;
	/** bus specific transfer functions (SPI or I2C) */
	const struct mfd_sc16is75x_transfer_function *transfer_function;
	/** Mutex to allow locking across multiple transactions */
	struct k_mutex transaction_lock;
#ifdef CONFIG_MFD_SC16IS75X_ASWQ
	/** Private work queue for offloading blocking work. */
	struct k_work_q work_queue;
	/** Stack area used by this driver instance's work queue. */
	k_thread_stack_t *work_queue_stack;
#endif /* CONFIG_MFD_SC16IS75X_ASWQ */
#ifdef CONFIG_MFD_SC16IS75X_INTERRUPTS
	/** Lock for interrupt handling */
	struct k_sem interrupt_lock;
	/** GPIO port interrupt callback */
	struct gpio_callback interrupt_cb;
	/** GPIO port interrupt worker */
	struct k_work interrupt_work_init;
	struct k_work_delayable interrupt_work_final;
	/** Struct for passing data between interrupt handling work items */
	struct sc16is75x_interrupt_data interrupt_data;
	/** Child callbacks for interrupt handling */
	sys_slist_t callbacks;
#endif /* CONFIG_MFD_SC16IS75X_INTERRUPTS */
};

int mfd_sc16is75x_spi_init(const struct device *dev);
int mfd_sc16is75x_i2c_init(const struct device *dev);

#ifdef __cplusplus
}
#endif

#endif /* ZEPHYR_DRIVERS_MFD_SC16IS75X_H_*/
