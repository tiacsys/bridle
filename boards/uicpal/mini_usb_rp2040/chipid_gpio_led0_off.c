/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/logging/log.h>

LOG_MODULE_DECLARE(board_control);

#define LED0_GPIO_SPEC	GPIO_DT_SPEC_GET(DT_NODELABEL(gpio_led0), gpios)

int chipid_gpio_led0_off(void)
{
	int ret;
	static struct gpio_dt_spec led0_gpio = LED0_GPIO_SPEC;

	if (!gpio_is_ready_dt(&led0_gpio)) {
		LOG_ERR("Chip-LED: GPIO device was not found!\n");
		return -ENODEV;
	}

	ret = gpio_pin_configure_dt(&led0_gpio, GPIO_OUTPUT_INACTIVE);
	if (ret < 0) {
		LOG_ERR("Chip-LED: Set GPIO line inactive failed!\n");
		return ret;
	}

	LOG_INF("Chip-LED configured.");
	return 0;
}

/* needs to be done after GPIO driver init */
SYS_INIT_NAMED(board_control, chipid_gpio_led0_off, POST_KERNEL,
	       CONFIG_BOARD_MINI_USB_RP2040_INIT_PRIORITY);
