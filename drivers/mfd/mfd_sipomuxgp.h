/*
 * Copyright (c) 2023-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief MFD Driver Interface for an SIPO/MUX GP matrix controller
 */

#ifndef DRIVERS_MFD_MFD_SIPOMUXGP_H_
#define DRIVERS_MFD_MFD_SIPOMUXGP_H_

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/pm/device.h>

#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/gpio/gpio_utils.h>

#include <zephyr/drivers/mfd/sipomuxgp.h>

#include <zephyr/sys/util.h>

typedef struct mfd_sipomuxgp_backend {
	const void *config;
	int (*init)(const struct device *dev);
	int (*cfg_oe)(const struct device *dev);
	int (*cfg_addr)(const struct device *dev);
	int (*set_oe)(const struct device *dev, const uint8_t value);
	int (*set_addr)(const struct device *dev, const uint8_t addr);
	int (*xfr_data)(const struct device *dev, const uint8_t addr,
			const uint8_t *tx_data, const size_t tx_count,
			const size_t padding_sz);
} mfd_sipomuxgp_backend_t;

typedef struct mfd_sipomuxgp_config {
	const mfd_sipomuxgp_backend_t backend;
	const struct gpio_dt_spec enable;
	const struct gpio_dt_spec *addr;
	const size_t num_addr;
	const size_t num_bits;
	const size_t columns;
	const size_t rows;
} mfd_sipomuxgp_config_t;

typedef struct mfd_sipomuxgp_data {
	const struct device *dev;
	struct k_spinlock lock;
	struct k_work refresh_worker;
	struct k_timer refresh_timer;
	uint32_t refresh_time_us;
	const size_t padding_sz;
	const size_t bitbuf_sz;
	uint8_t *bitbuf;
	size_t row_count;
	bool oe_noblank;
	bool oe_noratio;
	uint8_t oe_count;
} mfd_sipomuxgp_data_t;

#define __BITBUF_COL(bit, cols) ((bit) % (cols))
#define __BITBUF_ROW(bit, cols) ((bit) / (cols))
#define __BITBUF_BIT(bit, cols) (                                             \
		  (NUM_BITS(uint8_t) - 1)                                     \
		- (((bit) % (cols)) % NUM_BITS(uint8_t))                      \
	)
#define __BITBUF_IDX(bit, cols) (                                             \
		  (__BITBUF_COL((bit), (cols)) / NUM_BITS(uint8_t))           \
		+ (__BITBUF_ROW((bit), (cols)) * ((cols) / NUM_BITS(uint8_t)))\
	)

#define __TOTAL_BYTES(total_bits) (DIV_ROUND_UP(DIV_ROUND_UP(                 \
		total_bits, NUM_BITS(uint8_t)), sizeof(uint8_t))              \
	)

extern struct k_work_q mfd_sipomuxgp_xfr_workq;

#define MFD_SIPOMUXGP_NUM_INSTS (                                            \
		  DT_NUM_INST_STATUS_OKAY(sipo_mux_gp)                       \
		+ DT_NUM_INST_STATUS_OKAY(sipo_mux_gp_spi)                   \
	)

#endif /* DRIVERS_MFD_MFD_SIPOMUXGP_H_ */
