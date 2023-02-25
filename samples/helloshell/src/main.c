/*
 * Copyright (c) 2021 TiaC Systems
 * Copyright (c) 2019-2021 Li-Pro.Net
 * Copyright (c) 2012-2014 Wind River Systems, Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>

void main(void)
{
	printk("Hello World! I'm THE SHELL from %s\n", CONFIG_BOARD);
}
