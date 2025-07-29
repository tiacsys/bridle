/*
 * Copyright (c) 2025 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/logging/log.h>

LOG_MODULE_DECLARE(board_control);

#define CHIPLED_GPIO_SPEC GPIO_DT_SPEC_GET(DT_NODELABEL(gpio_chipled), gpios)

int chipled_gpio_chipled_off(void)
{
	int ret;
	static struct gpio_dt_spec chipled_gpio = CHIPLED_GPIO_SPEC;

	if (!gpio_is_ready_dt(&chipled_gpio)) {
		LOG_ERR("Chip-LED: GPIO device was not found!\n");
		return -ENODEV;
	}

	ret = gpio_pin_configure_dt(&chipled_gpio, GPIO_OUTPUT_INACTIVE);
	if (ret < 0) {
		LOG_ERR("Chip-LED: Set GPIO line inactive failed!\n");
		return ret;
	}

	LOG_INF("Chip-LED: GPIO configured.");
	return 0;
}

/* needs to be done after GPIO/LED driver init */
SYS_INIT_NAMED(board_control, chipled_gpio_chipled_off, POST_KERNEL,
	       CONFIG_BOARD_MINI_USB_RP2040_INIT_PRIORITY);
