/*
 * Sensortek Technology STK8BA58 3-axis accelerometer driver
 *
 * Copyright (c) 2025 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 *
 */

/**
 * @file
 * @brief I2C-Bus Access Interface for an STK8BA58
 */

#ifndef STK8BA58_REGS_H
#define STK8BA58_REGS_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stddef.h>
#include <math.h>

#include <zephyr/drivers/i2c.h>

/**
 * @addtogroup STK8BA58
 *
 * The values for the defines below as well as the register definitions
 * were taken from the datasheet revision 1.0, which can be found at:
 * https://datasheet4u.com/pdf-down/S/T/K/STK8BA58-Sensortek.pdf
 *
 * @{
 *
 */

/**
 * @defgroup  STK8BA58_BO Endianness definitions
 * @{
 *
 * The endianness of the STK8BA58 registers depends on the definition
 * selected by the chosen architecture:
 *
 * - @c CONFIG_LITTLE_ENDIAN
 * - @c CONFIG_BIG_ENDIAN
 *
 * @cond INTERNAL_HIDDEN
 */

#ifndef STK8BA58_BYTE_ORDER

#define STK8BA58_LITTLE_ENDIAN	1234
#define STK8BA58_BIG_ENDIAN	4321

#if defined(CONFIG_LITTLE_ENDIAN) && (CONFIG_LITTLE_ENDIAN)
#define STK8BA58_BYTE_ORDER	STK8BA58_LITTLE_ENDIAN

#elif defined(CONFIG_BIG_ENDIAN) && (CONFIG_BIG_ENDIAN)
#define STK8BA58_BYTE_ORDER	STK8BA58_BIG_ENDIAN

#else
#error unsupported chosen endianness by architecture
#endif

#endif /* STK8BA58_BYTE_ORDER */

/** @endcond */

/**
 * @}
 *
 */

/**
 * @defgroup STK8BA58_INF Infos
 * @brief    This section provide a set of default and identification values.
 * @{
 *
 */

/** Default for device identification (CHIP ID). **/
#define STK8BA58_ID		0x87U

/** Default for x-axis acceleration data (LSB) and the new data flag. */
#define STK8BA58_XOUT1_DFL	0x00U

/** Default for x-axis acceleration data (MSB). */
#define STK8BA58_XOUT2_DFL	0x00U

/** Default for y-axis acceleration data (LSB) and the new data flag. */
#define STK8BA58_YOUT1_DFL	0x00U

/** Default for y-axis acceleration data (MSB). */
#define STK8BA58_YOUT2_DFL	0x00U

/** Default for z-axis acceleration data (LSB) and the new data flag. */
#define STK8BA58_ZOUT1_DFL	0x00U

/** Default for z-axis acceleration data (MSB). */
#define STK8BA58_ZOUT2_DFL	0x00U

/** Default for motion detection interrupts status. */
#define STK8BA58_INTSTS1_DFL	0x00U

/** Default for new data interrupt status. */
#define STK8BA58_INTSTS2_DFL	0x00U

/** Default for any-motion (slope) detection information. */
#define STK8BA58_EVENTINFO1_DFL	0x00U

/** Default for acceleration sensing range. */
#define STK8BA58_RANGESEL_DFL	0x00U

/** Default for output data bandwidth selection. */
#define STK8BA58_BWSEL_DFL	0x1FU

/** Default for power mode selection and the sleep time duration setting. */
#define STK8BA58_POWMODE_DFL	0x00U

/** Default for output data filter and protection function. */
#define STK8BA58_DATASETUP_DFL	0x00U

/** Default for device software reset. */
#define STK8BA58_SWRST_DFL	0x00U

/** Command for device software reset to register defaults (SWRST). **/
#define STK8BA58_RST		0xB6U

/** Default for motion detection interrupts enable. */
#define STK8BA58_INTEN1_DFL	0x00U

/** Default for new data interrupt enable. */
#define STK8BA58_INTEN2_DFL	0x00U

/** Default for motion detection interrupts mapping to INT1 pin. */
#define STK8BA58_INTMAP1_DFL	0x00U

/** Default for new data interrupt mapping to INT1 pin. */
#define STK8BA58_INTMAP2_DFL	0x00U

/** Default for INT1 pin output type and active level. */
#define STK8BA58_INTCFG1_DFL	0x01U

/** Default for INT1 pin mode and latched hold-time. */
#define STK8BA58_INTCFG2_DFL	0x00U

/** Default for number of samples in the slope detection. */
#define STK8BA58_SLOPEDLY_DFL	0x00U

/** Default for threshold value of the slope detection. */
#define STK8BA58_SLOPETHD_DFL	0x14U

/** Default for skip time (LSB) of the significant motion. */
#define STK8BA58_SIGMOT1_DFL	0x96U

/** Default for skip time (MSB) of the significant motion, interrupt enable. */
#define STK8BA58_SIGMOT2_DFL	0x02U

/** Default for proof time of the significant motion. */
#define STK8BA58_SIGMOT3_DFL	0x32U

/** Default for digital interface parameters of the I2C interface. */
#define STK8BA58_INTFCFG_DFL	0x00U

/** Default for settings of the offset compensation. */
#define STK8BA58_OFSTCOMP1_DFL	0x00U

/** Default for x-axis offset compensation value. */
#define STK8BA58_OFSTX_DFL	0x00U

/** Default for y-axis offset compensation value. */
#define STK8BA58_OFSTY_DFL	0x00U

/** Default for z-axis offset compensation value. */
#define STK8BA58_OFSTZ_DFL	0x00U

/**
 * @}
 *
 */

/** Address for device identification (CHIP ID). **/
#define STK8BA58_CHIP_ID	0x00U

/** Address for x-axis acceleration data (LSB) and the new data flag. */
#define STK8BA58_XOUT1		0x02U

/** Address for y-axis acceleration data (LSB) and the new data flag. */
#define STK8BA58_YOUT1		0x04U

/** Address for z-axis acceleration data (LSB) and the new data flag. */
#define STK8BA58_ZOUT1		0x06U

/** Data for any-axis acceleration data (LSB) and the new data flag. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t new		: 1;
	uint8_t not_used_01	: 3;
	uint8_t out		: 4;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t out		: 4;
	uint8_t not_used_01	: 3;
	uint8_t new		: 1;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_out1_t;

/** Address for x-axis acceleration data (MSB). */
#define STK8BA58_XOUT2		0x03U

/** Address for y-axis acceleration data (MSB). */
#define STK8BA58_YOUT2		0x05U

/** Address for z-axis acceleration data (MSB). */
#define STK8BA58_ZOUT2		0x07U

/** Data struct for any-axis acceleration data (MSB). */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t out		: 8;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t out		: 8;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_out2_t;

/** Address for motion detection interrupts status. */
#define STK8BA58_INTSTS1	0x09U

/** Data for motion detection interrupts status. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t sig_mot_sts	: 1;
	uint8_t not_used_01	: 1;
	uint8_t any_mot_sts	: 1;
	uint8_t not_used_02	: 5;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t not_used_02	: 5;
	uint8_t any_mot_sts	: 1;
	uint8_t not_used_01	: 1;
	uint8_t sig_mot_sts	: 1;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_intsts1_t;

/** Address for new data interrupt status. */
#define STK8BA58_INTSTS2	0x0AU

/** Data for new data interrupt status. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t not_used_01	: 7;
	uint8_t data_sts	: 1;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t data_sts	: 1;
	uint8_t not_used_01	: 7;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_intsts2_t;

/** Address for any-motion (slope) detection information. */
#define STK8BA58_EVENTINFO1	0x0BU

/** Data for any-motion (slope) detection information. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t slp_1st_x	: 1;
	uint8_t slp_1st_y	: 1;
	uint8_t slp_1st_z	: 1;
	uint8_t not_used_01	: 1;
	uint8_t slpsign_x	: 1;
	uint8_t slpsign_y	: 1;
	uint8_t slpsign_z	: 1;
	uint8_t not_used_02	: 1;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t not_used_02	: 1;
	uint8_t slpsign_z	: 1;
	uint8_t slpsign_y	: 1;
	uint8_t slpsign_x	: 1;
	uint8_t not_used_01	: 1;
	uint8_t slp_1st_z	: 1;
	uint8_t slp_1st_y	: 1;
	uint8_t slp_1st_x	: 1;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_eventinfo1_t;

/** Address for acceleration sensing range. */
#define STK8BA58_RANGESEL	0x0FU

/** Data for acceleration sensing range. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t range		: 4;
	uint8_t not_used_01	: 4;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t not_used_01	: 4;
	uint8_t range		: 4;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_rangesel_t;

/** Address for output data bandwidth selection. */
#define STK8BA58_BWSEL		0x10U

/** Data for output data bandwidth selection. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t bw		: 5;
	uint8_t not_used_01	: 3;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t not_used_01	: 3;
	uint8_t bw		: 5;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_bwsel_t;

/** Address for power mode selection and the sleep time duration setting. */
#define STK8BA58_POWMODE	0x11U

/** Data for power mode selection and the sleep time duration setting. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t not_used_01	: 1;
	uint8_t sleep_dur	: 4;
	uint8_t not_used_02	: 1;
	uint8_t lowpower	: 1;
	uint8_t suspend		: 1;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t suspend		: 1;
	uint8_t lowpower	: 1;
	uint8_t not_used_02	: 1;
	uint8_t sleep_dur	: 4;
	uint8_t not_used_01	: 1;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_powmode_t;

/** Address for output data filter and protection function. */
#define STK8BA58_DATASETUP	0x13U

/** Data for output data filter and protection function. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t not_used_01	: 6;
	uint8_t protect_dis	: 1;
	uint8_t data_sel	: 1;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t data_sel	: 1;
	uint8_t protect_dis	: 1;
	uint8_t not_used_01	: 6;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_datasetup_t;

/** Address for device software reset. */
#define STK8BA58_SWRST		0x14U

/** Address for motion detection interrupts enable. */
#define STK8BA58_INTEN1		0x16U

/** Data for motion detection interrupts enable. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t slp_en_x	: 1;
	uint8_t slp_en_y	: 1;
	uint8_t slp_en_z	: 1;
	uint8_t not_used_01	: 5;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t not_used_01	: 5;
	uint8_t slp_en_z	: 1;
	uint8_t slp_en_y	: 1;
	uint8_t slp_en_x	: 1;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_inten1_t;

/** Address for new data interrupt enable. */
#define STK8BA58_INTEN2		0x17U

/** Data for new data interrupt enable. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t not_used_01	: 4;
	uint8_t data_en		: 1;
	uint8_t not_used_02	: 3;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t not_used_02	: 3;
	uint8_t data_en		: 1;
	uint8_t not_used_01	: 4;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_inten2_t;

/** Address for motion detection interrupts mapping to INT1 pin. */
#define STK8BA58_INTMAP1	0x19U

/** Data for motion detection interrupts mapping to INT1 pin. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t sigmot2int1	: 1;
	uint8_t not_used_01	: 1;
	uint8_t anymot2int1	: 1;
	uint8_t not_used_02	: 5;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t not_used_02	: 5;
	uint8_t anymot2int1	: 1;
	uint8_t not_used_01	: 1;
	uint8_t sigmot2int1	: 1;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_intmap1_t;

/** Address for new data interrupt mapping to INT1 pin. */
#define STK8BA58_INTMAP2	0x1AU

/** Data for new data interrupt mapping to INT1 pin. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t data2int1	: 1;
	uint8_t not_used_01	: 7;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t not_used_01	: 7;
	uint8_t data2int1	: 1;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_intmap2_t;

/** Address for INT1 pin output type and active level. */
#define STK8BA58_INTCFG1	0x20U

/** Data for INT1 pin output type and active level. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t int1_lv		: 1;
	uint8_t int1_od		: 1;
	uint8_t not_used_01	: 6;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t not_used_01	: 6;
	uint8_t int1_od		: 1;
	uint8_t int1_lv		: 1;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_intcfg1_t;

/** Address for INT1 pin mode and latched hold-time. */
#define STK8BA58_INTCFG2	0x21U

/** Data for INT1 pin mode and latched hold-time. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t int_latch	: 4;
	uint8_t not_used_01	: 3;
	uint8_t int_rst		: 1;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t int_rst		: 1;
	uint8_t not_used_01	: 3;
	uint8_t int_latch	: 4;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_intcfg2_t;

/** Address for number of samples in the slope detection. */
#define STK8BA58_SLOPEDLY	0x27U

/** Data for number of samples in the slope detection. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t slp_dur		: 2;
	uint8_t not_used_01	: 6;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t not_used_01	: 6;
	uint8_t slp_dur		: 2;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_slopedly_t;

/** Address for threshold value of the slope detection. */
#define STK8BA58_SLOPETHD	0x28U

/** Address for skip time (LSB) of the significant motion. */
#define STK8BA58_SIGMOT1	0x29U

/** Data for skip time (LSB) of the significant motion. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t skip_time	: 8;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t skip_time	: 8;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_sigmot1_t;

/** Address for skip time (MSB) of the significant motion, interrupt enable. */
#define STK8BA58_SIGMOT2	0x2AU

/** Data for skip time (MSB) of the significant motion, interrupt enable. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t skip_time	: 1;
	uint8_t sig_mot_en	: 1;
	uint8_t any_mot_en	: 1;
	uint8_t not_used_01	: 5;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t not_used_01	: 5;
	uint8_t any_mot_en	: 1;
	uint8_t sig_mot_en	: 1;
	uint8_t skip_time	: 1;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_sigmot2_t;

/** Address for proof time of the significant motion. */
#define STK8BA58_SIGMOT3	0x2BU

/** Data for proof time of the significant motion. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t proof_time	: 7;
	uint8_t not_used_01	: 1;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t not_used_01	: 1;
	uint8_t proof_time	: 7;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_sigmot3_t;

/** Address for digital interface parameters of the I2C interface. */
#define STK8BA58_INTFCFG	0x34U

/** Data for digital interface parameters of the I2C interface. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t not_used_01	: 1;
	uint8_t i2c_wdt_sel	: 1;
	uint8_t i2c_wdt_en	: 1;
	uint8_t not_used_02	: 5;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t not_used_02	: 5;
	uint8_t i2c_wdt_en	: 1;
	uint8_t i2c_wdt_sel	: 1;
	uint8_t not_used_01	: 1;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_intfcfg_t;

/** Address for settings of the offset compensation. */
#define STK8BA58_OFSTCOMP1	0x36U

/** Data for settings of the offset compensation. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t not_used_01	: 7;
	uint8_t ofst_rst	: 1;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t ofst_rst	: 1;
	uint8_t not_used_01	: 7;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_ofstcomp1_t;

/** Address for x-axis offset compensation value. */
#define STK8BA58_OFSTX		0x38U

/** Address for y-axis offset compensation value. */
#define STK8BA58_OFSTY		0x39U

/** Address for z-axis offset compensation value. */
#define STK8BA58_OFSTZ		0x3AU

/** Data struct for any-axis offset compensation value. */
typedef struct {
#if STK8BA58_BYTE_ORDER == STK8BA58_LITTLE_ENDIAN
	uint8_t comp		: 8;
#elif STK8BA58_BYTE_ORDER == STK8BA58_BIG_ENDIAN
	uint8_t comp		: 8;
#endif /* STK8BA58_BYTE_ORDER */
} stk8ba58_ofst_t;

/*
 * These are the basic platform dependent I/O routines to read
 * and write device registers connected on a standard I2C bus.
 */

int32_t stk8ba58_read_reg(const struct i2c_dt_spec *i2c, uint8_t reg,
			  uint8_t *data, uint16_t len);
int32_t stk8ba58_write_reg(const struct i2c_dt_spec *i2c, uint8_t reg,
			   uint8_t *data,  uint16_t len);

/**
 * The size of the buffer pushed on the stack used to copy
 * the data to be written along with the register address.
 */
#define STK8BA58_I2C_WRITE_BUFFER_SIZE (16U)

float_t stk8ba58_from_fs2g_to_mg(int16_t lsb);
float_t stk8ba58_from_fs4g_to_mg(int16_t lsb);
float_t stk8ba58_from_fs8g_to_mg(int16_t lsb);

/** Data for motion detection and data interrupts status. */
typedef struct {
	stk8ba58_intsts1_t	intsts1;
	stk8ba58_intsts2_t	intsts2;
	stk8ba58_eventinfo1_t	eventinfo1;
} stk8ba58_all_sources_t;

int32_t stk8ba58_all_sources_get(const struct i2c_dt_spec *i2c,
				 stk8ba58_all_sources_t *val);

/** Values for acceleration sensing range. */
typedef enum {
	STK8BA58_2g		= 0b0011,
	STK8BA58_4g		= 0b0101,
	STK8BA58_8g		= 0b1000,
} stk8ba58_range_t;

int32_t stk8ba58_xl_range_set(const struct i2c_dt_spec *i2c,
			      stk8ba58_range_t val);
int32_t stk8ba58_xl_range_get(const struct i2c_dt_spec *i2c,
			      stk8ba58_range_t *val);

/** Values for output data bandwidth selection. */
typedef enum {
	STK8BA58_XL_BW_7Hz81	= 0b01000,
	STK8BA58_XL_BW_15Hz63	= 0b01001,
	STK8BA58_XL_BW_31Hz25	= 0b01010,
	STK8BA58_XL_BW_62Hz5	= 0b01011,
	STK8BA58_XL_BW_125Hz	= 0b01100,
	STK8BA58_XL_BW_250Hz	= 0b01101,
	STK8BA58_XL_BW_500Hz	= 0b01110,
	STK8BA58_XL_BW_1000Hz	= 0b01111,
	STK8BA58_XL_BW_PWRUP	= 0b11111,
} stk8ba58_bw_t;

typedef enum {
	STK8BA58_XL_DS_FILTERED   = 0,
	STK8BA58_XL_DS_UNFILTERED = 1,
} stk8ba58_ds_t;

int32_t stk8ba58_xl_bandwidth_set(const struct i2c_dt_spec *i2c,
				  stk8ba58_bw_t val, stk8ba58_ds_t sel);
int32_t stk8ba58_xl_bandwidth_get(const struct i2c_dt_spec *i2c,
				  stk8ba58_bw_t *val, stk8ba58_ds_t *sel);

/** Values for power mode selection and the sleep time duration setting. */
typedef enum {
	STK8BA58_XL_LP_0ms5	= 0b0101,
	STK8BA58_XL_LP_1ms	= 0b0110,
	STK8BA58_XL_LP_2ms	= 0b0111,
	STK8BA58_XL_LP_4ms	= 0b1000,
	STK8BA58_XL_LP_6ms	= 0b1001,
	STK8BA58_XL_LP_10ms	= 0b1010,
	STK8BA58_XL_LP_25ms	= 0b1011,
	STK8BA58_XL_LP_50ms	= 0b1100,
	STK8BA58_XL_LP_100ms	= 0b1101,
	STK8BA58_XL_LP_500ms	= 0b1110,
	STK8BA58_XL_LP_1000ms	= 0b1111,
} stk8ba58_sleepdur_t;

/** Values for output data filter and protection function. */
typedef enum {
	STK8BA58_XL_PM_NORMAL	= 0,
	STK8BA58_XL_PM_LOWPOWER	= 1,
	STK8BA58_XL_PM_SUSPEND	= 2,
} stk8ba58_pm_t;

int32_t stk8ba58_xl_power_mode_set(const struct i2c_dt_spec *i2c,
				   stk8ba58_sleepdur_t val, stk8ba58_pm_t sel);
int32_t stk8ba58_xl_power_mode_get(const struct i2c_dt_spec *i2c,
				   stk8ba58_sleepdur_t *val, stk8ba58_pm_t *sel);

int32_t stk8ba58_acceleration_raw_get(const struct i2c_dt_spec *i2c,
				      int16_t *buff);

int32_t stk8ba58_device_id_get(const struct i2c_dt_spec *i2c, uint8_t *buff);

int32_t stk8ba58_reset_set(const struct i2c_dt_spec *i2c, uint8_t val);

/** Values for INT1 pin output type. */
typedef enum {
	STK8BA58_PUSH_PULL		= 0,
	STK8BA58_OPEN_DRAIN		= 1,
} stk8ba58_pp_od_t;

int32_t stk8ba58_pin_int1_mode_set(const struct i2c_dt_spec *i2c,
				   stk8ba58_pp_od_t val);
int32_t stk8ba58_pin_int1_mode_get(const struct i2c_dt_spec *i2c,
				   stk8ba58_pp_od_t *val);

/** Values for INT1 pin output active level. */
typedef enum {
	STK8BA58_ACTIVE_LOW	= 0,
	STK8BA58_ACTIVE_HIGH	= 1,
} stk8ba58_hl_active_t;

int32_t stk8ba58_pin_int1_polarity_set(const struct i2c_dt_spec *i2c,
				       stk8ba58_hl_active_t val);
int32_t stk8ba58_pin_int1_polarity_get(const struct i2c_dt_spec *i2c,
				       stk8ba58_hl_active_t *val);

/** Values for INT1 pin mode and latched hold-time. */
typedef enum {
	STK8BA58_INT_PULSED	= 0b0000,
	STK8BA58_INT_250ms	= 0b0001,
	STK8BA58_INT_500ms	= 0b0010,
	STK8BA58_INT_1000ms	= 0b0011,
	STK8BA58_INT_2000ms	= 0b0100,
	STK8BA58_INT_4000ms	= 0b0101,
	STK8BA58_INT_8000ms	= 0b0110,
	STK8BA58_INT_LATCHEDALT	= 0b0111,
	STK8BA58_INT_PULSEDALT	= 0b1000,
	STK8BA58_INT_0ms250	= 0b1001,
	STK8BA58_INT_0ms500	= 0b1010,
	STK8BA58_INT_1ms	= 0b1011,
	STK8BA58_INT_12ms5	= 0b1100,
	STK8BA58_INT_25ms	= 0b1101,
	STK8BA58_INT_50ms	= 0b1110,
	STK8BA58_INT_LATCHED	= 0b1111,
} stk8ba58_intlatch_t;

int32_t stk8ba58_int_notification_set(const struct i2c_dt_spec *i2c,
				      stk8ba58_intlatch_t val);
int32_t stk8ba58_int_notification_get(const struct i2c_dt_spec *i2c,
				      stk8ba58_intlatch_t *val);

/** Data for motion detection and data interrupts mapping to INT1 pin. */
typedef struct {
	uint8_t sigmot2int1	: 1;
	uint8_t anymot2int1	: 1;
	uint8_t data2int1	: 1;
} stk8ba58_pin_int1_route_t;

int32_t stk8ba58_pin_int1_route_set(const struct i2c_dt_spec *i2c,
				    stk8ba58_pin_int1_route_t val);
int32_t stk8ba58_pin_int1_route_get(const struct i2c_dt_spec *i2c,
				    stk8ba58_pin_int1_route_t *val);

/** Data for motion detection and data interrupts enable. */
typedef struct {
	uint8_t slp_en_x	: 1;
	uint8_t slp_en_y	: 1;
	uint8_t slp_en_z	: 1;
	uint8_t data_en		: 1;
} stk8ba58_int_enable_t;

int32_t stk8ba58_int_enable_set(const struct i2c_dt_spec *i2c,
				stk8ba58_int_enable_t val);
int32_t stk8ba58_int_enable_get(const struct i2c_dt_spec *i2c,
				stk8ba58_int_enable_t *val);

/**
 * @}
 *
 */

#ifdef __cplusplus
}
#endif

#endif /* STK8BA58_REGS_H */
