/*
 * Copyright (c) 2023 TiaC Systems
 * Copyright (c) 2022 Golioth, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

#include "buzzer.h"

#include <zephyr/kernel.h>
#include <zephyr/init.h>

/* Logging */
#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(buzzersh, CONFIG_BUZZER_SHELL_LOG_LEVEL);

/* Setup for a buzzer  */
#define PWM_BUZZER_NODE DT_ALIAS(pwm_buzzer0)
#if !DT_NODE_HAS_STATUS(PWM_BUZZER_NODE, okay)
#error "Unsupported board: pwm-buzzer0 devicetree alias is not defined"
#endif

/* Buzzer instance structs */
static struct buzzer_instance buzzer =
{
	.dt_spec = PWM_DT_SPEC_GET(PWM_BUZZER_NODE),
	.song = beep // on startup
};

int main(void)
{
	int err;

	err = app_buzzer_init(&buzzer);
	if (err)
	{
		LOG_ERR("Unable to configure buzzer");
	}

	LOG_INF("Buzzer shell is ready!");
	return 0;
}
