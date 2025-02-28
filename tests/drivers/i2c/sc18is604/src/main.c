/*
 * Copyright (c) 2025 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/ztest.h>
#include <zephyr/drivers/emul.h>
#include <zephyr/drivers/mfd/sc18is604_emul.h>

static const struct emul *get_sc18is604(void)
{
	const struct emul *sc18is604 = EMUL_DT_GET(DT_NODELABEL(sc18is604));

	zassert_true(device_is_ready(sc18is604->dev), "SC18IS604 device not ready");

	return sc18is604;
}

static const struct device *get_sc18is604_i2c(void)
{
	const struct device *sc18is604_i2c = DEVICE_DT_GET(DT_NODELABEL(sc18is604_i2c));

	zassert_true(device_is_ready(sc18is604_i2c), "SC18IS604 I2C device not ready");

	return sc18is604_i2c;
}

ZTEST_SUITE(sc18is604_i2c_emul, NULL, NULL, NULL, NULL, NULL);

ZTEST(sc18is604_i2c_emul, test_write)
{
	const struct device *i2c = get_sc18is604_i2c();
	const struct emul *mfd_emul = get_sc18is604();

	/* Set up a message */
	uint8_t buf[4] = {0x01, 0x02, 0x03, 0x04};

	/* Perform the write */
	zassert_ok(i2c_write(i2c, buf, sizeof(buf), 0x42), "Failed to write");

	/* Check the transmission */
	struct mfd_sc18is604_emul_transmission tx = {0};

	zassert_ok(mfd_sc18is604_emul_i2c_get_last_tx(mfd_emul, &tx),
		   "Failed to get last transmission");

	zassert_equal(tx.addr, 0x42, "Address mismatch");
	zassert_equal(tx.len, sizeof(buf), "Length mismatch");
	zassert_mem_equal(tx.msg, buf, sizeof(buf), "Message mismatch");
}

ZTEST(sc18is604_i2c_emul, test_read)
{
	const struct device *i2c = get_sc18is604_i2c();
	const struct emul *mfd_emul = get_sc18is604();

	/* Set up a message */
	uint8_t buf[4] = {0};
	uint8_t msg[4] = {0x01, 0x02, 0x03, 0x04};

	/* Inject the message into the emulated device (function returns the number of bytes set) */
	zassert_equal(mfd_sc18is604_emul_i2c_set_rx(mfd_emul, msg, sizeof(buf)), 4,
		      "Failed to set RX buffer");

	/* Perform the read */
	zassert_ok(i2c_read(i2c, buf, sizeof(buf), 0x42), "Failed to read");

	/* Check the read buffer */
	zassert_mem_equal(buf, msg, sizeof(buf), "Message mismatch");
}

ZTEST(sc18is604_i2c_emul, test_write_read)
{
	const struct device *i2c = get_sc18is604_i2c();
	const struct emul *mfd_emul = get_sc18is604();

	/* Set up messages */
	uint8_t write_buf[4] = {0x01, 0x02, 0x03, 0x04};
	uint8_t read_buf[4] = {0};
	uint8_t read_msg[4] = {0x05, 0x06, 0x07, 0x08};

	/* Inject the message into the emulated device (function returns the number of bytes set) */
	zassert_equal(mfd_sc18is604_emul_i2c_set_rx(mfd_emul, read_msg, sizeof(read_buf)), 4,
		      "Failed to set RX buffer");

	/* Perform the write-read */
	zassert_ok(
		i2c_write_read(i2c, 0x42, write_buf, sizeof(write_buf), read_buf, sizeof(read_buf)),
		"Failed to write-read");

	/* Check the transmission */
	struct mfd_sc18is604_emul_transmission tx = {0};

	zassert_ok(mfd_sc18is604_emul_i2c_get_last_tx(mfd_emul, &tx),
		   "Failed to get last transmission");

	zassert_equal(tx.addr, 0x42, "Address mismatch");
	zassert_equal(tx.len, sizeof(write_buf), "Length mismatch");
	zassert_mem_equal(tx.msg, write_buf, sizeof(write_buf), "TX Message mismatch");

	/* Check the read buffer */
	zassert_mem_equal(read_buf, read_msg, sizeof(read_buf), "RX Message mismatch");
}
