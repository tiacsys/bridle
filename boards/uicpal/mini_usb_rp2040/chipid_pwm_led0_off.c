/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/drivers/pwm.h>
#include <zephyr/logging/log.h>

LOG_MODULE_DECLARE(board_control);

#define LED0_PWM_SPEC	PWM_DT_SPEC_GET(DT_NODELABEL(pwm_led0))

int chipid_pwm_led0_off(void)
{
	int ret;
	static struct pwm_dt_spec led0_pwm = LED0_PWM_SPEC;

	if (!pwm_is_ready_dt(&led0_pwm)) {
		LOG_ERR("Chip-LED: PWM device was not found!\n");
		return -ENODEV;
	}

	ret = pwm_set_pulse_dt(&led0_pwm, 0);
	if (ret < 0) {
		LOG_ERR("Chip-LED: Set PWM channel inactive failed!\n");
		return ret;
	}

	LOG_INF("Chip-LED configured.");
	return 0;
}

/* needs to be done after PWM driver init */
SYS_INIT_NAMED(board_control, chipid_pwm_led0_off, POST_KERNEL,
	       CONFIG_BOARD_MINI_USB_RP2040_INIT_PRIORITY);
