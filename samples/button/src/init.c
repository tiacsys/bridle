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
	gpio_pin_configure_dt(&btn, GPIO_INPUT);
	gpio_pin_configure_dt(&led, GPIO_OUTPUT);

	return 0;
}

/* Register our init function  */
SYS_INIT(init, APPLICATION, APPLICATION_IO_INIT_PRIORITY);

/* Empty main */
int main(void) { return 0; }
