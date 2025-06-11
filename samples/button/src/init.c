/*
 * Copyright (c) 2021-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include "init.h"

/* Setup for a button  */
#define BTN_NODE DT_ALIAS(sw0)
#if !DT_NODE_HAS_STATUS(BTN_NODE, okay)
#error "Unsupported board: sw0 devicetree alias is not defined"
#endif

const struct gpio_dt_spec btn = GPIO_DT_SPEC_GET(BTN_NODE, gpios);

/* Setup for an led */
#define LED_NODE DT_ALIAS(led0)
#if !DT_NODE_HAS_STATUS(LED_NODE, okay)
#error "Unsupported board: led0 devicetree alias is not defined"
#endif

const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED_NODE, gpios);

/* Init function for configuring button and led gpio pins */
static int init(void)
{
	int ret;

	if (!gpio_is_ready_dt(&btn)) {
		printk("Error: button device %s is not ready\n", btn.port->name);
		return -ENODEV;
	}

	ret = gpio_pin_configure_dt(&btn, GPIO_INPUT);
	if (ret != 0) {
		printk("Error %d: failed to configure %s pin %d\n", ret, btn.port->name, btn.pin);
		return ret;
	}

	if (!gpio_is_ready_dt(&led)) {
		printk("Error: LED device %s is not ready\n", led.port->name);
		return -ENODEV;
	}

	ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT);
	if (ret != 0) {
		printk("Error %d: failed to configure %s pin %d\n", ret, led.port->name, led.pin);
		return ret;
	}

	printk("Set up button at %s pin %d\n", btn.port->name, btn.pin);
	printk("Set up LED at %s pin %d\n", led.port->name, led.pin);
	return 0;
}

/* Register our init function  */
SYS_INIT(init, APPLICATION, APPLICATION_IO_INIT_PRIORITY);

/* Empty main */
int main(void) { return 0; }
