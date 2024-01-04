/*
 * Copyright (c) 2023 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */
#ifndef ZEPHYR_INCLUDE_DRIVERS_MFD_DS3231_H_
#define ZEPHYR_INCLUDE_DRIVERS_MFD_DS3231_H_

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @defgroup mdf_interface_ds3231 MFD DS3231 Interface
 * @ingroup mfd_interfaces
 * @{
 */

#include <stddef.h>
#include <stdint.h>

#include <zephyr/device.h>

/* @todo Move DS3231 register definitions to MFD private area. */

#include <zephyr/sys/util.h>	/* for GENMASK() */

/* DS3231 registers */
#define DS3231_SECONDS		0x00
#define DS3231_SECONDS_BITS	GENMASK(6, 0)

#define DS3231_MINUTES		0x01
#define DS3231_MINUTES_BITS	GENMASK(6, 0)

#define DS3231_HOURS		0x02
#define DS3231_HOURS_BITS	GENMASK(5, 0)
#define DS3231_VALIDATE_24HR	BIT(6)

#define DS3231_DAY		0x03
#define DS3231_DAY_BITS		GENMASK(2, 0)

#define DS3231_DATE		0x04
#define DS3231_DATE_BITS	GENMASK(5, 0)

#define DS3231_MONTH		0x05
#define DS3231_MONTHS_BITS	GENMASK(4, 0)
#define DS3231_VALIDATE_CENTURY	BIT(7)

#define DS3231_YEAR		0x06
#define DS3231_YEAR_BITS	GENMASK(7, 0)

#define DS3231_CAL_NUM_REGS	(DS3231_YEAR - DS3231_SECONDS + 1)

/* @todo Define registers for alarm 1, 0x07 - 0x0A. */

/* @todo Define registers for alarm 2, 0x0B - 0x0D. */

#define DS3231_CTRL		0x0E
#define DS3231_CTRL_EOSC	BIT(7)
#define DS3231_CTRL_BBSQW	BIT(6)
#define DS3231_CTRL_CONV	BIT(5)
#define DS3231_CTRL_RS2		BIT(4)
#define DS3231_CTRL_RS1		BIT(3)
#define DS3231_CTRL_INTCN	BIT(2)
#define DS3231_CTRL_A2IE	BIT(1)
#define DS3231_CTRL_A1IE	BIT(0)

#define DS3231_CTRL_STAT	0x0F
#define DS3231_STAT_OSF		BIT(7)
#define DS3231_STAT_EN32KHZ	BIT(3)
#define DS3231_STAT_BSY		BIT(2)
#define DS3231_STAT_A2F		BIT(1)
#define DS3231_STAT_A1F		BIT(0)

#define DS3231_AGE_OFFS		0x10
#define DS3231_AGE_OFFS_BITS	GENMASK(7, 0)

#define DS3231_TEMP_MSB		0x11
#define DS3231_TEMP_MSB_BITS	GENMASK(7, 0)

#define DS3231_TEMP_LSB		0x12
#define DS3231_TEMP_LSB_BITS	GENMASK(7, 6)

#define DS3231_TEMP_NUM_REGS	(DS3231_TEMP_LSB - DS3231_TEMP_MSB + 1)
#define DS3231_TEMP_MSB_IDX	(DS3231_TEMP_MSB - DS3231_TEMP_MSB)
#define DS3231_TEMP_LSB_IDX	(DS3231_TEMP_LSB - DS3231_TEMP_MSB)

/**
 * @brief Read single register from DS3231
 *
 * @param dev ds3231 mfd device
 * @param reg Register address
 * @param val Pointer to buffer for received data
 * @retval 0 If successful
 * @retval -errno In case of any bus error (see i2c_reg_read_byte_dt())
 */
int mfd_ds3231_reg_read(const struct device *dev, const uint8_t reg,
			uint8_t *val);

/**
 * @brief Read multiple registers from DS3231
 *
 * @param dev ds3231 mfd device
 * @param reg Register address
 * @param buf Pointer to buffer for received data
 * @param len Number of bytes to read
 * @retval 0 If successful
 * @retval -errno In case of any bus error (see i2c_burst_write_dt())
 */
int mfd_ds3231_reg_read_burst(const struct device *dev, const uint8_t reg,
			      uint8_t *buf, const size_t len);

/**
 * @brief Write single register to DS3231
 *
 * @param dev ds3231 mfd device
 * @param reg Register address
 * @param val Data to be sent
 * @retval 0 If successful
 * @retval -errno In case of any bus error (see i2c_reg_write_byte_dt())
 */
int mfd_ds3231_reg_write(const struct device *dev, const uint8_t reg,
			 const uint8_t val);

/**
 * @brief Write multiple registers to DS3231
 *
 * @param dev ds3231 mfd device
 * @param reg Register address
 * @param buf Pointer to buffer with data to be sent
 * @param len Number of bytes to write
 * @retval 0 If successful
 * @retval -errno In case of any bus error (see i2c_burst_read_dt())
 */
int mfd_ds3231_reg_write_burst(const struct device *dev, const uint8_t reg,
			       const uint8_t *buf, const size_t len);

/** @} */

#ifdef __cplusplus
}
#endif

#endif /* ZEPHYR_INCLUDE_DRIVERS_MFD_DS3231_H_ */
