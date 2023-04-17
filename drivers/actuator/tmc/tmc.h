/*
 * Copyright (c) 2023 TiaC Systems
 * Copyright (c) 2022 Stefano Cottafavi
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef BRIDLE_DRIVERS_ACTUATOR_TMC_TMC_H_
#define BRIDLE_DRIVERS_ACTUATOR_TMC_TMC_H_

#include <stdint.h>
#include <zephyr/drivers/spi.h>
#include <bridle/drivers/actuator.h>

struct tmc_data {
	uint16_t r_sens;
	uint16_t i_run;
	uint16_t i_hold;
};

struct tmc_config {
	// TODO: int (*bus_init)(const struct device *dev);
#if DT_ANY_INST_ON_BUS_STATUS_OKAY(spi)
	const struct spi_dt_spec spi;
#endif
};

#endif /* BRIDLE_DRIVERS_ACTUATOR_TMC_TMC_H_ */
