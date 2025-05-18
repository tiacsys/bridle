/*
 * Sensortek Technology STK8BA58 3-axis accelerometer driver
 *
 * Copyright (c) 2025 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 *
 */

/**
 * @file
 * @brief I2C-Bus Access for an STK8BA58
 */

#include "stk8ba58_reg.h"

/**
 * @brief     This file provides a set of functions needed to drive the
 *            STK8BA58 simplified inertial module.
 * @defgroup  STK8BA58 STK8BA58 Register Access
 * @ingroup   io_sensors_imu_stk8ba58
 * @since     4.1
 * @version   1.0.0
 *
 * I2C chip register access for the Sensortek Technology STK8BA58 3-axis
 * accelerometer. Data sheet can be found here:
 * https://datasheet4u.com/pdf-down/S/T/K/STK8BA58-Sensortek.pdf
 *
 * @{
 *
 */

/**
 * @defgroup  STK8BA58_IF Interfaces Functions
 * @brief     This section provide a set of functions used to read and
 *            write a generic register of the device.
 *            MANDATORY: return 0 -> no Error.
 * @{
 *
 */

/**
 * @brief  Read generic device register
 *
 * @param  i2c   Read / write interface definitions.(ptr)
 * @param  reg   Register to read.
 * @param  data  Pointer to buffer that store the data read.(ptr)
 * @param  len   Number of consecutive register to read.
 * @retval       Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_read_reg(const struct i2c_dt_spec *i2c, uint8_t reg,
			  uint8_t *data, uint16_t len)
{
	int32_t ret;

	if (i2c == NULL) {
		return -EINVAL;
	}

	ret = i2c_burst_read_dt(i2c, reg, data, len);

	return ret;
}

/**
 * @brief  Write generic device register
 *
 * @param  i2c   Read / write interface definitions.(ptr)
 * @param  reg   Register to write.
 * @param  data  Pointer to data to write in register reg.(ptr)
 * @param  len   Number of consecutive register to write.
 * @retval       Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_write_reg(const struct i2c_dt_spec *i2c, uint8_t reg,
			   uint8_t *data, uint16_t len)
{
	int32_t ret;
	uint8_t buf[STK8BA58_I2C_WRITE_BUFFER_SIZE];

	__ASSERT_NO_MSG(len <= sizeof(buf) - 1);

	if (i2c == NULL) {
		return -EINVAL;
	}

	buf[0] = reg;
	memcpy(&buf[1], data, len);

	ret = i2c_write_dt(i2c, buf, len + 1);

	return ret;
}

/**
 * @}
 *
 */

/**
 * @defgroup    STK8BA58_SENS Sensitivity
 * @brief       These functions convert raw-data into engineering units.
 * @{
 *
 */

float_t stk8ba58_from_fs2g_to_mg(int16_t lsb)
{
	return ((float_t)lsb * 0.98f);
}

float_t stk8ba58_from_fs4g_to_mg(int16_t lsb)
{
	return ((float_t)lsb * 1.95f);
}

float_t stk8ba58_from_fs8g_to_mg(int16_t lsb)
{
	return ((float_t)lsb * 3.91f);
}

/**
 * @}
 *
 */

/**
 * @defgroup  STK8BA58_DATGEN Data generation
 * @brief     This section groups all the functions concerning
 *            data generation.
 * @{
 *
 */

/**
 * @brief  Read all the interrupt/status flag of the device.[get]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Get INTSTS1, INTSTS2, EVENTINFO1.(ptr)
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_all_sources_get(const struct i2c_dt_spec *i2c,
				 stk8ba58_all_sources_t *val)
{
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_INTSTS1,
				     (uint8_t *)&(val->intsts1), 1);

	if (ret == 0) {
		ret = stk8ba58_read_reg(i2c, STK8BA58_INTSTS2,
					     (uint8_t *)&(val->intsts2), 1);
	}

	if (ret == 0) {
		ret = stk8ba58_read_reg(i2c, STK8BA58_EVENTINFO1,
					     (uint8_t *)&(val->eventinfo1), 1);
	}

	return ret;
}

/**
 * @brief  Accelerometer range selection.[set]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Change the values of range in reg RANGESEL.
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_xl_range_set(const struct i2c_dt_spec *i2c,
			      stk8ba58_range_t val)
{
	stk8ba58_rangesel_t rangesel;
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_RANGESEL,
				     (uint8_t *)&rangesel, 1);

	if (ret == 0) {
		rangesel.range = (uint8_t)val;
		ret = stk8ba58_write_reg(i2c, STK8BA58_RANGESEL,
					      (uint8_t *)&rangesel, 1);
	}

	return ret;
}

/**
 * @brief  Accelerometer range selection.[get]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Get the values of range in reg RANGESEL.(ptr)
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_xl_range_get(const struct i2c_dt_spec *i2c,
			      stk8ba58_range_t *val)
{
	stk8ba58_rangesel_t rangesel = { 0 };
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_RANGESEL,
				     (uint8_t *)&rangesel, 1);

	switch (rangesel.range) {
	default:
	case STK8BA58_2g:
		*val = STK8BA58_2g;
		break;

	case STK8BA58_4g:
		*val = STK8BA58_4g;
		break;

	case STK8BA58_8g:
		*val = STK8BA58_8g;
		break;
	}

	return ret;
}

/**
 * @brief  Accelerometer bandwidth selection.[set]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Change the values of bw in reg BWSEL.
 * @param  sel    Change the values of data-sel in reg DATASETUP.
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_xl_bandwidth_set(const struct i2c_dt_spec *i2c,
				  stk8ba58_bw_t val, stk8ba58_ds_t sel)
{
	stk8ba58_datasetup_t datasetup;
	stk8ba58_bwsel_t bwsel;
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_BWSEL, (uint8_t *)&bwsel, 1);

	if (ret == 0) {
		bwsel.bw = (uint8_t)val & 0x1FU;
		ret = stk8ba58_write_reg(i2c, STK8BA58_BWSEL,
					      (uint8_t *)&bwsel, 1);
	}

	if (ret == 0) {
		ret = stk8ba58_read_reg(i2c, STK8BA58_DATASETUP,
					     (uint8_t *)&datasetup, 1);
	}

	if (ret == 0) {
		datasetup.data_sel = (uint8_t)sel & 0x1U;
		ret = stk8ba58_write_reg(i2c, STK8BA58_DATASETUP,
					      (uint8_t *)&datasetup, 1);
	}

	return ret;
}

/**
 * @brief  Accelerometer bandwidth selection.[get]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Get the values of bw in reg BWSEL.(ptr)
 * @param  sel    Get the values of data-sel in reg DATASETUP.(ptr)
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_xl_bandwidth_get(const struct i2c_dt_spec *i2c,
				  stk8ba58_bw_t *val, stk8ba58_ds_t *sel)
{
	stk8ba58_datasetup_t datasetup = { 0 };
	stk8ba58_bwsel_t bwsel = { 0 };
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_BWSEL, (uint8_t *)&bwsel, 1);

	if (ret == 0) {
		ret = stk8ba58_read_reg(i2c, STK8BA58_DATASETUP,
					     (uint8_t *)&datasetup, 1);
	}

	switch (bwsel.bw) {
	case STK8BA58_XL_BW_7Hz81:
		*val = STK8BA58_XL_BW_7Hz81;
		break;

	case STK8BA58_XL_BW_15Hz63:
		*val = STK8BA58_XL_BW_15Hz63;
		break;

	case STK8BA58_XL_BW_31Hz25:
		*val = STK8BA58_XL_BW_31Hz25;
		break;

	case STK8BA58_XL_BW_62Hz5:
		*val = STK8BA58_XL_BW_62Hz5;
		break;

	case STK8BA58_XL_BW_125Hz:
		*val = STK8BA58_XL_BW_125Hz;
		break;

	case STK8BA58_XL_BW_250Hz:
		*val = STK8BA58_XL_BW_250Hz;
		break;

	case STK8BA58_XL_BW_500Hz:
		*val = STK8BA58_XL_BW_500Hz;
		break;

	case STK8BA58_XL_BW_1000Hz:
		*val = STK8BA58_XL_BW_1000Hz;
		break;

	default:
	case STK8BA58_XL_BW_PWRUP:
		*val = STK8BA58_XL_BW_PWRUP;
		break;
	}

	switch (datasetup.data_sel) {
	default:
	case STK8BA58_XL_DS_FILTERED:
		*sel = STK8BA58_XL_DS_FILTERED;
		break;

	case STK8BA58_XL_DS_UNFILTERED:
		*sel = STK8BA58_XL_DS_UNFILTERED;
		break;
	}

	return ret;
}

/**
 * @brief  Accelerometer power mode selection.[set]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Change the values of sleep-dur in reg POWMODE.
 * @param  sel    Change the values of lowpower / suspend in reg POWMODE.
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_xl_power_mode_set(const struct i2c_dt_spec *i2c,
				   stk8ba58_sleepdur_t val, stk8ba58_pm_t sel)
{
	stk8ba58_powmode_t powmode;
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_POWMODE, (uint8_t *)&powmode, 1);

	if (ret == 0) {
		switch (sel) {
		default:
		case STK8BA58_XL_PM_NORMAL:
			powmode.sleep_dur = 0;
			powmode.lowpower = 0;
			powmode.suspend = 0;
			break;

		case STK8BA58_XL_PM_LOWPOWER:
			powmode.sleep_dur = (uint8_t)val & 0x0FU;
			powmode.lowpower = 1;
			powmode.suspend = 0;
			break;

		case STK8BA58_XL_PM_SUSPEND:
			powmode.sleep_dur = 0;
			powmode.lowpower = 0;
			powmode.suspend = 1;
			break;
		}

		ret = stk8ba58_write_reg(i2c, STK8BA58_POWMODE,
					      (uint8_t *)&powmode, 1);
	}

	return ret;
}

/**
 * @brief  Accelerometer bandwidth selection.[get]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Get the values of sleep-dur in reg POWMODE.(ptr)
 * @param  sel    Get the values of lowpower / suspend in reg POWMODE.(ptr)
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_xl_power_mode_get(const struct i2c_dt_spec *i2c,
				   stk8ba58_sleepdur_t *val, stk8ba58_pm_t *sel)
{
	stk8ba58_powmode_t powmode = { 0 };
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_POWMODE, (uint8_t *)&powmode, 1);

	if (powmode.suspend == 1) {
		*sel = STK8BA58_XL_PM_SUSPEND;
		*val = 0;
	}

	else if (powmode.lowpower == 1) {

		*sel = STK8BA58_XL_PM_LOWPOWER;

		switch (powmode.sleep_dur) {
		case STK8BA58_XL_LP_0ms5:
			*val = STK8BA58_XL_LP_0ms5;
			break;

		case STK8BA58_XL_LP_1ms:
			*val = STK8BA58_XL_LP_1ms;
			break;

		case STK8BA58_XL_LP_2ms:
			*val = STK8BA58_XL_LP_2ms;
			break;

		case STK8BA58_XL_LP_4ms:
			*val = STK8BA58_XL_LP_4ms;
			break;

		case STK8BA58_XL_LP_6ms:
			*val = STK8BA58_XL_LP_6ms;
			break;

		case STK8BA58_XL_LP_10ms:
			*val = STK8BA58_XL_LP_10ms;
			break;

		case STK8BA58_XL_LP_25ms:
			*val = STK8BA58_XL_LP_25ms;
			break;

		case STK8BA58_XL_LP_50ms:
			*val = STK8BA58_XL_LP_50ms;
			break;

		case STK8BA58_XL_LP_100ms:
			*val = STK8BA58_XL_LP_100ms;
			break;

		case STK8BA58_XL_LP_500ms:
			*val = STK8BA58_XL_LP_500ms;
			break;

		case STK8BA58_XL_LP_1000ms:
			*val = STK8BA58_XL_LP_1000ms;
			break;

		default:
			*val = 0;
			break;
		}
	}

	else {
		*sel = STK8BA58_XL_PM_NORMAL;
		*val = 0;
	}

	return ret;
}

/**
 * @}
 *
 */

/**
 * @defgroup  STK8BA58_DATOUT Data output
 * @brief     This section groups all the data output functions.
 * @{
 *
 */

/**
 * @brief  Linear acceleration output register. The value is expressed as a
 *         16-bit word in two’s complement.[get]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  buff   Buffer that stores data read.(ptr)
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_acceleration_raw_get(const struct i2c_dt_spec *i2c,
				      int16_t *buff)
{
	int32_t ret;
	uint8_t raw[6];
	uint16_t raw16;
	const stk8ba58_out1_t *xout1 = (const stk8ba58_out1_t *)&raw[0];
	const stk8ba58_out2_t *xout2 = (const stk8ba58_out2_t *)&raw[1];
	const stk8ba58_out1_t *yout1 = (const stk8ba58_out1_t *)&raw[2];
	const stk8ba58_out2_t *yout2 = (const stk8ba58_out2_t *)&raw[3];
	const stk8ba58_out1_t *zout1 = (const stk8ba58_out1_t *)&raw[4];
	const stk8ba58_out2_t *zout2 = (const stk8ba58_out2_t *)&raw[5];

	if (buff == NULL) {
		return -EINVAL;
	}

	ret = stk8ba58_read_reg(i2c, STK8BA58_XOUT1, raw, 6);

	raw16 = (uint16_t)(xout2->out << 4) + (uint16_t)(xout1->out);
	buff[0] = (int16_t)(raw16 << 4) / 16;

	raw16 = (uint16_t)(yout2->out << 4) + (uint16_t)(yout1->out);
	buff[1] = (int16_t)(raw16 << 4) / 16;

	raw16 = (uint16_t)(zout2->out << 4) + (uint16_t)(zout1->out);
	buff[2] = (int16_t)(raw16 << 4) / 16;

	return ret;
}

/**
 * @}
 *
 */

/**
 * @defgroup  STK8BA58_COM Common Functions
 * @brief     This section groups common useful functions.
 * @{
 *
 */

/**
 * @brief  DeviceChipID.[get]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  buff   Buffer that stores data read.(ptr)
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_device_id_get(const struct i2c_dt_spec *i2c, uint8_t *buff)
{
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_CHIP_ID, buff, 1);

	return ret;
}

/**
 * @brief  Software reset. Restore the default values in
 *         user registers.[set]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Change the value with soft-reset in reg SWRST.
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_reset_set(const struct i2c_dt_spec *i2c, uint8_t val)
{
	int32_t ret;
	uint8_t swrst;

	ret = stk8ba58_read_reg(i2c, STK8BA58_SWRST, &swrst, 1);

	if (ret == 0) {
		if (swrst == 0) {
			swrst = val;
			ret = stk8ba58_write_reg(i2c, STK8BA58_SWRST,
						      &swrst, 1);
		} else {
			ret = -EBUSY;
		}
	}

	return ret;
}

/**
 * @}
 *
 */

/**
 * @defgroup   STK8BA58_SIF Serial Interface
 * @brief      This section groups all the functions concerning main serial
 *             interface management (not auxiliary)
 * @{
 *
 */

/**
 * @brief  Push-pull/open-drain selection on interrupt pad.[set]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Change the values of int1_od in reg INTCFG1.
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_pin_int1_mode_set(const struct i2c_dt_spec *i2c,
				   stk8ba58_pp_od_t val)
{
	stk8ba58_intcfg1_t intcfg1;
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_INTCFG1, (uint8_t *)&intcfg1, 1);

	if (ret == 0) {
		intcfg1.int1_od = (uint8_t)val;
		ret = stk8ba58_write_reg(i2c, STK8BA58_INTCFG1,
					      (uint8_t *)&intcfg1, 1);
	}

	return ret;
}

/**
 * @brief  Push-pull/open-drain selection on interrupt pad.[get]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Get the values of int1_od in reg INTCFG1.(ptr)
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_pin_int1_mode_get(const struct i2c_dt_spec *i2c,
				   stk8ba58_pp_od_t *val)
{
	stk8ba58_intcfg1_t intcfg1;
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_INTCFG1, (uint8_t *)&intcfg1, 1);

	switch (intcfg1.int1_od) {
	default:
	case STK8BA58_PUSH_PULL:
		*val = STK8BA58_PUSH_PULL;
		break;

	case STK8BA58_OPEN_DRAIN:
		*val = STK8BA58_OPEN_DRAIN;
		break;
	}

	return ret;
}

/**
 * @brief  Polarity active-high/-low selection on interrupt pad.[set]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Change the values of int1_lv in reg INTCFG1.
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_pin_int1_polarity_set(const struct i2c_dt_spec *i2c,
				       stk8ba58_hl_active_t val)
{
	stk8ba58_intcfg1_t intcfg1;
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_INTCFG1, (uint8_t *)&intcfg1, 1);

	if (ret == 0) {
		intcfg1.int1_lv = (uint8_t)val;
		ret = stk8ba58_write_reg(i2c, STK8BA58_INTCFG1,
					      (uint8_t *)&intcfg1, 1);
	}

	return ret;
}

/**
 * @brief  Polarity active-high/-low selection on interrupt pad.[get]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Get the values of int1_lv in reg INTCFG1.(ptr)
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_pin_int1_polarity_get(const struct i2c_dt_spec *i2c,
				       stk8ba58_hl_active_t *val)
{
	stk8ba58_intcfg1_t intcfg1;
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_INTCFG1, (uint8_t *)&intcfg1, 1);

	switch (intcfg1.int1_lv) {
	case STK8BA58_ACTIVE_LOW:
		*val = STK8BA58_ACTIVE_LOW;
		break;

	default:
	case STK8BA58_ACTIVE_HIGH:
		*val = STK8BA58_ACTIVE_HIGH;
		break;
	}

	return ret;
}

/**
 * @brief  Latched/pulsed interrupt.[set]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Change the values of int-latch in reg INTCFG2.
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_int_notification_set(const struct i2c_dt_spec *i2c,
				      stk8ba58_intlatch_t val)
{
	stk8ba58_intcfg2_t intcfg2;
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_INTCFG2, (uint8_t *)&intcfg2, 1);

	if (ret == 0) {
		intcfg2.int_rst = 1;
		intcfg2.int_latch = (uint8_t)val;
		ret = stk8ba58_write_reg(i2c, STK8BA58_INTCFG2,
					      (uint8_t *)&intcfg2, 1);
	}

	return ret;
}

/**
 * @brief  Latched/pulsed interrupt.[get]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Get the values of int-latch in reg INTCFG2.(ptr)
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_int_notification_get(const struct i2c_dt_spec *i2c,
				      stk8ba58_intlatch_t *val)
{
	stk8ba58_intcfg2_t intcfg2;
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_INTCFG2, (uint8_t *)&intcfg2, 1);

	switch (intcfg2.int_latch) {
	default:
	case STK8BA58_INT_PULSED:
		*val = STK8BA58_INT_PULSED;
		break;

	case STK8BA58_INT_250ms:
		*val = STK8BA58_INT_250ms;
		break;

	case STK8BA58_INT_500ms:
		*val = STK8BA58_INT_500ms;
		break;

	case STK8BA58_INT_1000ms:
		*val = STK8BA58_INT_1000ms;
		break;

	case STK8BA58_INT_2000ms:
		*val = STK8BA58_INT_2000ms;
		break;

	case STK8BA58_INT_4000ms:
		*val = STK8BA58_INT_4000ms;
		break;

	case STK8BA58_INT_8000ms:
		*val = STK8BA58_INT_8000ms;
		break;

	case STK8BA58_INT_LATCHEDALT:
		*val = STK8BA58_INT_LATCHEDALT;
		break;

	case STK8BA58_INT_PULSEDALT:
		*val = STK8BA58_INT_PULSEDALT;
		break;

	case STK8BA58_INT_0ms250:
		*val = STK8BA58_INT_0ms250;
		break;

	case STK8BA58_INT_0ms500:
		*val = STK8BA58_INT_0ms500;
		break;

	case STK8BA58_INT_1ms:
		*val = STK8BA58_INT_1ms;
		break;

	case STK8BA58_INT_12ms5:
		*val = STK8BA58_INT_12ms5;
		break;

	case STK8BA58_INT_25ms:
		*val = STK8BA58_INT_25ms;
		break;

	case STK8BA58_INT_50ms:
		*val = STK8BA58_INT_50ms;
		break;

	case STK8BA58_INT_LATCHED:
		*val = STK8BA58_INT_LATCHED;
		break;
	}

	return ret;
}

/**
 * @brief  Select the signal that need to route on int1 pad.[set]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Change union of registers from INTMAP1 to INTMAP2.
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_pin_int1_route_set(const struct i2c_dt_spec *i2c,
				    stk8ba58_pin_int1_route_t val)
{
	stk8ba58_intmap1_t intmap1;
	stk8ba58_intmap2_t intmap2;
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_INTMAP1, (uint8_t *)&intmap1, 1);

	if (ret == 0) {
		ret = stk8ba58_read_reg(i2c, STK8BA58_INTMAP2,
					     (uint8_t *)&intmap2, 1);
	}

	intmap1.sigmot2int1 = (uint8_t)val.sigmot2int1;
	intmap1.anymot2int1 = (uint8_t)val.anymot2int1;
	intmap2.data2int1   = (uint8_t)val.data2int1;

	if (ret == 0) {
		ret = stk8ba58_write_reg(i2c, STK8BA58_INTMAP1,
					      (uint8_t *)&intmap1, 1);
	}

	if (ret == 0) {
		ret = stk8ba58_write_reg(i2c, STK8BA58_INTMAP2,
					      (uint8_t *)&intmap2, 1);
	}

	return ret;
}

/**
 * @brief  Select the signal that need to route on int1 pad.[get]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Get union of registers from INTMAP1 to INTMAP2.(ptr)
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_pin_int1_route_get(const struct i2c_dt_spec *i2c,
				    stk8ba58_pin_int1_route_t *val)
{
	stk8ba58_intmap1_t intmap1 = { 0 };
	stk8ba58_intmap2_t intmap2 = { 0 };
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_INTMAP1, (uint8_t *)&intmap1, 1);

	if (ret == 0) {
		ret = stk8ba58_read_reg(i2c, STK8BA58_INTMAP2,
					     (uint8_t *)&intmap2, 1);
	}

	val->sigmot2int1 = intmap1.sigmot2int1;
	val->anymot2int1 = intmap1.anymot2int1;
	val->data2int1   = intmap2.data2int1;

	return ret;
}

/**
 * @brief  Enable the source that need to trigger interrupt.[get]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Change union of registers from INTEN1 to INTEN2.
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_int_enable_set(const struct i2c_dt_spec *i2c,
				stk8ba58_int_enable_t val)
{
	stk8ba58_inten1_t inten1;
	stk8ba58_inten2_t inten2;
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_INTEN1, (uint8_t *)&inten1, 1);

	if (ret == 0) {
		ret = stk8ba58_read_reg(i2c, STK8BA58_INTEN2,
					     (uint8_t *)&inten2, 1);
	}

	inten1.slp_en_x = (uint8_t)val.slp_en_x;
	inten1.slp_en_y = (uint8_t)val.slp_en_y;
	inten1.slp_en_z = (uint8_t)val.slp_en_z;
	inten2.data_en  = (uint8_t)val.data_en;

	if (ret == 0) {
		ret = stk8ba58_write_reg(i2c, STK8BA58_INTEN1,
					      (uint8_t *)&inten1, 1);
	}

	if (ret == 0) {
		ret = stk8ba58_write_reg(i2c, STK8BA58_INTEN2,
					      (uint8_t *)&inten2, 1);
	}

	return ret;
}

/**
 * @brief  Enable the source that need to trigger interrupt.[get]
 *
 * @param  i2c    Read / write interface definitions.(ptr)
 * @param  val    Get union of registers from INTEN1 to INTEN2.(ptr)
 * @retval        Interface status (MANDATORY: return 0 -> no Error).
 *
 */
int32_t stk8ba58_int_enable_get(const struct i2c_dt_spec *i2c,
				stk8ba58_int_enable_t *val)
{
	stk8ba58_inten1_t inten1 = { 0 };
	stk8ba58_inten2_t inten2 = { 0 };
	int32_t ret;

	ret = stk8ba58_read_reg(i2c, STK8BA58_INTEN1, (uint8_t *)&inten1, 1);

	if (ret == 0) {
		ret = stk8ba58_read_reg(i2c, STK8BA58_INTEN2,
					     (uint8_t *)&inten2, 1);
	}

	val->slp_en_x = inten1.slp_en_x;
	val->slp_en_y = inten1.slp_en_y;
	val->slp_en_z = inten1.slp_en_z;
	val->data_en  = inten2.data_en;

	return ret;
}

/**
 * @}
 *
 */

/**
 * @}
 *
 */
