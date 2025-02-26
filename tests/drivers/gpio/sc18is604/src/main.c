/*
 * Copyright (c) 2025 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/ztest.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/emul.h>
#include <zephyr/drivers/mfd/sc18is604_emul.h>

static const struct emul *get_sc18is604(void)
{
	const struct emul *sc18is604 = EMUL_DT_GET(DT_NODELABEL(sc18is604));

	zassert_true(device_is_ready(sc18is604->dev), "SC18IS604 device not ready");

	return sc18is604;
}

static const struct device *get_sc18is604_gpio(void)
{
	const struct device *sc18is604_gpio = DEVICE_DT_GET(DT_NODELABEL(sc18is604_gpio));

	zassert_true(device_is_ready(sc18is604_gpio), "SC18IS604 GPIO device not ready");

	return sc18is604_gpio;
}

ZTEST_SUITE(sc18is604_gpio_emul, NULL, NULL, NULL, NULL, NULL);

ZTEST(sc18is604_gpio_emul, test_pin_set)
{
	const struct device *gpio = get_sc18is604_gpio();
	const struct emul *mfd_emul = get_sc18is604();

	/* Check all (output capable) pins */
	for (int i = 0; i < 4; i++) {
		uint8_t value = 0;

		/* Configure the pin as output */
		zassert_ok(gpio_pin_configure(gpio, i, GPIO_OUTPUT), "Failed to configure pin %d",
			   i);

		/* Set the pin to active */
		zassert_ok(gpio_pin_set(gpio, i, 1), "Failed to set pin %d", i);
		zassert_ok(mfd_sc18is604_emul_gpio_get_output(mfd_emul, i, &value),
			   "Failed to get value of pin %d from emulator backend", i);
		zassert_equal(value, 1, "Pin %d value mismatch", i);

		/* Set the pin to inactive */
		zassert_ok(gpio_pin_set(gpio, i, 0), "Failed to clear pin %d", i);
		zassert_ok(mfd_sc18is604_emul_gpio_get_output(mfd_emul, i, &value),
			   "Failed to get value of pin %d from emulator backend", i);
		zassert_equal(value, 0, "Pin %d value mismatch", i);
	}
}

ZTEST(sc18is604_gpio_emul, test_pin_get)
{
	const struct device *gpio = get_sc18is604_gpio();
	const struct emul *mfd_emul = get_sc18is604();

	/* Check all pins */
	for (int i = 0; i < 5; i++) {
		/* Configure the pin as input */
		zassert_ok(gpio_pin_configure(gpio, i, GPIO_INPUT), "Failed to configure pin %d",
			   i);

		/* Set the pin value via emulator backend */
		zassert_ok(mfd_sc18is604_emul_gpio_set_input(mfd_emul, i, 1),
			   "Failed to set pin %d via emulator backend", i);
		/* Check the pin value reported by driver */
		zassert_equal(gpio_pin_get(gpio, i), 1, "Pin %d value mismatch", i);

		/* Clear the pin value via emulator backend */
		zassert_ok(mfd_sc18is604_emul_gpio_set_input(mfd_emul, i, 0),
			   "Failed to clear pin %d via emulator backend", i);
		/* Check the pin value reported by driver */
		zassert_equal(gpio_pin_get(gpio, i), 0, "Pin %d value mismatch", i);
	}
}

ZTEST(sc18is604_gpio_emul, test_port_get)
{
	const struct device *gpio = get_sc18is604_gpio();
	const struct emul *mfd_emul = get_sc18is604();

	/* Configure all pins as input */
	for (int i = 0; i < 5; i++) {
		zassert_ok(gpio_pin_configure(gpio, i, GPIO_INPUT));
	}

	/* Set an input pattern */
	zassert_ok(mfd_sc18is604_emul_gpio_set_input(mfd_emul, 0, 1),
		   "Failed to set pin 0 via emulator backend");
	zassert_ok(mfd_sc18is604_emul_gpio_set_input(mfd_emul, 1, 0),
		   "Failed to set pin 1 via emulator backend");
	zassert_ok(mfd_sc18is604_emul_gpio_set_input(mfd_emul, 2, 1),
		   "Failed to set pin 2 via emulator backend");
	zassert_ok(mfd_sc18is604_emul_gpio_set_input(mfd_emul, 3, 0),
		   "Failed to set pin 3 via emulator backend");
	zassert_ok(mfd_sc18is604_emul_gpio_set_input(mfd_emul, 4, 1),
		   "Failed to set pin 4 via emulator backend");

	/* Check the port */
	gpio_port_value_t port_value = 0;

	zassert_ok(gpio_port_get(gpio, &port_value), "Failed to get port value");
	zassert_equal(port_value, 0b10101, "Port value mismatch");
}

ZTEST(sc18is604_gpio_emul, test_port_set_masked)
{
	const struct device *gpio = get_sc18is604_gpio();
	const struct emul *mfd_emul = get_sc18is604();

	/* Configure all pins as output */
	for (int i = 0; i < 4; i++) {
		zassert_ok(gpio_pin_configure(gpio, i, GPIO_OUTPUT), "Failed to configure pin %d",
			   i);
	}

	/* Clear all pins */
	zassert_ok(gpio_port_clear_bits(gpio, 0b1111), "Failed to clear port");

	/* Confirm the port is cleared */
	uint8_t value = 0;

	for (int i = 0; i < 4; i++) {
		zassert_ok(mfd_sc18is604_emul_gpio_get_output(mfd_emul, i, &value),
			   "Failed to get value of pin %d from emulator backend", i);
		zassert_equal(value, 0, "Pin %d value mismatch", i);
	}

	/* Set an output pattern (partially masked) */
	zassert_ok(gpio_port_set_masked(gpio, 0b1110, 0b1011), "Failed to set port values");

	/* Confirm the port is set according to pattern and mask */
	zassert_ok(mfd_sc18is604_emul_gpio_get_output(mfd_emul, 0, &value),
		   "Failed to get value of pin 0 from emulator backend");
	zassert_equal(value, 0, "Pin 0 value mismatch");
	zassert_ok(mfd_sc18is604_emul_gpio_get_output(mfd_emul, 1, &value),
		   "Failed to get value of pin 1 from emulator backend");
	zassert_equal(value, 1, "Pin 1 value mismatch");
	zassert_ok(mfd_sc18is604_emul_gpio_get_output(mfd_emul, 2, &value),
		   "Failed to get value of pin 2 from emulator backend");
	zassert_equal(value, 0, "Pin 2 value mismatch");
	zassert_ok(mfd_sc18is604_emul_gpio_get_output(mfd_emul, 3, &value),
		   "Failed to get value of pin 3 from emulator backend");
	zassert_equal(value, 1, "Pin 3 value mismatch");
}
