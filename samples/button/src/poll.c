/*
 * Copyright (c) 2021-2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/device.h>
#include "init.h"

/* Setup for creating the polling thread */
#define MY_STACK_SIZE 512
#define MY_PRIORITY 5

K_THREAD_STACK_DEFINE(polling_thread_stack_area, MY_STACK_SIZE);

/* Entry point function for the polling thread  */
static void polling_thread_entry_point(void *btn_void, void *led_void, void *)
{
	/* Unwrap the argument pointers */
	struct gpio_dt_spec *btn = (struct gpio_dt_spec *) btn_void;
	struct gpio_dt_spec *led = (struct gpio_dt_spec *) led_void;

	/* Infinite polling loop */
	while (1) {
		int val = gpio_pin_get_dt(btn);

		gpio_pin_set_dt(led, val);

		/* Sleep the thread for a little while */
		k_msleep(CONFIG_SLEEP_TIME_MS);
	}
}

/* Init function which spawns a dedicated polling thread  */
static int init(void)
{
	struct k_thread polling_thread;

	__unused k_tid_t tid = k_thread_create(&polling_thread,
					polling_thread_stack_area,
					K_THREAD_STACK_SIZEOF(polling_thread_stack_area),
					polling_thread_entry_point,
					(void *) &btn, (void *) &led, NULL,
					MY_PRIORITY, 0, K_NO_WAIT);

	return 0;
}

/* Register our init function */
SYS_INIT(init, APPLICATION, APPLICATION_CB_INIT_PRIORITY);
