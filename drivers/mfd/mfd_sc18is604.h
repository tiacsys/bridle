/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief MFD Driver Interface for an SC18IM604 bridge
 */

#ifndef ZEPHYR_DRIVERS_MFD_SC18IS604_H_
#define ZEPHYR_DRIVERS_MFD_SC18IS604_H_

#ifdef __cplusplus
extern "C" {
#endif

#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/spi.h>

#include <zephyr/drivers/mfd/sc18is604.h>

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
struct mfd_sc18is604_config {
	/** Specs of the underlying SPI bus. */
	const struct spi_dt_spec spi;
	/** Specs of this device's interrupt pin. */
	const struct gpio_dt_spec interrupt;
	/** Specs of this device's reset pin. */
	const struct gpio_dt_spec reset;
};

/**
 * @brief SC18IM604 MFD data
 *
 * This structure contains data structures used by a SC18IM604 MFD.
 *
 * Interrupt propagation is handled by @a k_sem. Changes to
 * @ref mfd_sc18is604_data and @ref mfd_sc18is604_config are
 * synchronized using @a k_mutex.
 */
struct mfd_sc18is604_data {
	/** Backreference to driver instance. */
	const struct device *dev;
	/** Lock for ensuring uninterrupted access to the MFD bus. */
	struct k_sem lock;
	/** Interrupt callback of this driver instance. */
	struct gpio_callback interrupt_cb;
	/** Semaphore used for MFD-internal signaling of interrupts. */
	struct k_sem interrupt_signal;
	/** Interrupt callbacks registered by child devices. */
	sys_slist_t child_callbacks;
#ifdef CONFIG_MFD_SC18IS604_ASYNC
	/** Private work queue for offloading blocking work. */
	struct k_work_q work_queue;
	/** Stack area used by this driver instance's work queue. */
	k_thread_stack_t *work_queue_stack;
#endif /* CONFIG_MFD_SC18IS604_ASYNC */
};

#ifdef __cplusplus
}
#endif

#endif /* ZEPHYR_DRIVERS_MFD_SC18IS604_H_ */
