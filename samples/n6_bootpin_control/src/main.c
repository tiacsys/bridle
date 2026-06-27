/*
 * Copyright (c) 2026 inovex GmbH
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/shell/shell.h>

/*
 * The boot-select control pin is taken from the "boot-ctrl-gpios" property of
 * the devicetree "/zephyr,user" node, for example:
 *
 *   / {
 *           zephyr,user {
 *                   boot-ctrl-gpios = <&gpio0 11 GPIO_ACTIVE_HIGH>;
 *           };
 *   };
 *
 * The pin polarity (i.e. whether "assert" drives the line high or low) is
 * controlled by the GPIO flags in the devicetree, so the active level can be
 * adapted per board without touching this source file.
 */
#if !DT_NODE_HAS_PROP(DT_PATH(zephyr_user), boot_ctrl_gpios)
#error "Unsupported board: boot-ctrl-gpios is not defined in /zephyr,user"
#endif

static const struct gpio_dt_spec boot_ctrl =
	GPIO_DT_SPEC_GET(DT_PATH(zephyr_user), boot_ctrl_gpios);

static int boot_ctrl_set(const struct shell *sh, int value)
{
	int ret;

	if (!gpio_is_ready_dt(&boot_ctrl)) {
		shell_error(sh, "boot-ctrl device %s is not ready",
			    boot_ctrl.port->name);
		return -ENODEV;
	}

	ret = gpio_pin_set_dt(&boot_ctrl, value);
	if (ret != 0) {
		shell_error(sh, "failed to %s boot-ctrl (err %d)",
			    value ? "assert" : "de-assert", ret);
		return ret;
	}

	shell_print(sh, "boot-ctrl %s (%s pin %u)",
		    value ? "asserted" : "de-asserted",
		    boot_ctrl.port->name, boot_ctrl.pin);
	return 0;
}

static int cmd_assert(const struct shell *sh, size_t argc, char **argv)
{
	ARG_UNUSED(argc);
	ARG_UNUSED(argv);

	return boot_ctrl_set(sh, 1);
}

static int cmd_deassert(const struct shell *sh, size_t argc, char **argv)
{
	ARG_UNUSED(argc);
	ARG_UNUSED(argv);

	return boot_ctrl_set(sh, 0);
}

SHELL_CMD_REGISTER(assert, NULL,
		   "Assert the boot-select control pin.", cmd_assert);
SHELL_CMD_REGISTER(deassert, NULL,
		   "De-assert the boot-select control pin.", cmd_deassert);

int main(void)
{
	int ret;

	if (!gpio_is_ready_dt(&boot_ctrl)) {
		printk("Error: boot-ctrl device %s is not ready\n",
		       boot_ctrl.port->name);
		return -ENODEV;
	}

	/* Start in the de-asserted (inactive) state. */
	ret = gpio_pin_configure_dt(&boot_ctrl, GPIO_OUTPUT_INACTIVE);
	if (ret != 0) {
		printk("Error %d: failed to configure boot-ctrl %s pin %u\n",
		       ret, boot_ctrl.port->name, boot_ctrl.pin);
		return ret;
	}

	printk("N6 boot selector ready: boot-ctrl on %s pin %u\n",
	       boot_ctrl.port->name, boot_ctrl.pin);
	printk("Use the 'assert' and 'deassert' shell commands.\n");
	return 0;
}
