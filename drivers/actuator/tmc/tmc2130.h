/*
 * Copyright (c) 2023 TiaC Systems
 * Copyright (c) 2022 Stefano Cottafavi
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef BRIDLE_DRIVERS_ACTUATOR_TMC_TMC2130_H_
#define BRIDLE_DRIVERS_ACTUATOR_TMC_TMC2130_H_

#include "tmc.h"
#include "TMC2130.h"

struct tmc2130_data {
	TMC2130TypeDef	api_type;
	ConfigurationTypeDef api_conf;
	struct tmc_data	tmc_data;
};

#endif /* BRIDLE_DRIVERS_ACTUATOR_TMC_TMC2130_H_ */
