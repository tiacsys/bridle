/*
 * Copyright (c) 2021-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/device.h>
#include "init.h"

/* Interrupt handler  */
static void button_pressed(const struct device *dev, struct gpio_callback *cb, uint32_t pins)
{
	/* Only trigger on the correct pin */
	if (pins & BIT(btn.pin)) {
		int val = gpio_pin_get(dev, btn.pin);

		gpio_pin_set_dt(&led, val);
	}
}


/* Init function which creates the interrupt callback  */
static int init(void)
{
	static struct gpio_callback button_cb_data;

	/* Configure btn to trigger interrupts on both press and release */
	gpio_pin_interrupt_configure_dt(&btn, GPIO_INT_EDGE_BOTH);

	/* Create and fill the callback struct */
	gpio_init_callback(&button_cb_data, button_pressed, BIT(btn.pin));

	/* Register the callback */
	gpio_add_callback(btn.port, &button_cb_data);

	return 0;
}

/* Register our init function */
SYS_INIT(init, APPLICATION, APPLICATION_CB_INIT_PRIORITY);
