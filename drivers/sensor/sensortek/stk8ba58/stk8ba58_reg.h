/*
 * Sensortek Technology STK8BA58 3-axis accelerometer driver
 *
 * Copyright (c) 2025 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 *
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

/** @addtogroup STK8BA58
  *
  * The values for the defines below as well as the register definitions
  * were taken from the datasheet revision 1.0, which can be found at:
  * https://datasheet4u.com/pdf-down/S/T/K/STK8BA58-Sensortek.pdf
  *
  * @{
  *
  */

/** @defgroup  STK8BA58_BO Endianness definitions
  * @{
  *
  */

#ifndef DRV_BYTE_ORDER
#ifndef __BYTE_ORDER__

#define DRV_LITTLE_ENDIAN	1234
#define DRV_BIG_ENDIAN		4321

/** if _BYTE_ORDER is not defined, choose the endianness of your architecture
  * by uncommenting the define which fits your platform endianness
  */
#define DRV_BYTE_ORDER		DRV_LITTLE_ENDIAN
/* #define DRV_BYTE_ORDER	DRV_BIG_ENDIAN */

#else /* defined __BYTE_ORDER__ */

#define DRV_LITTLE_ENDIAN	__ORDER_LITTLE_ENDIAN__
#define DRV_BIG_ENDIAN		__ORDER_BIG_ENDIAN__
#define DRV_BYTE_ORDER		__BYTE_ORDER__

#endif /* __BYTE_ORDER__*/
#endif /* DRV_BYTE_ORDER */

/**
  * @}
  *
  */

/** @defgroup STK8BA58_INF Infos
  * @{
  *
  */

/** Device Identification (CHIP ID) **/
#define STK8BA58_ID		0x87U

/** Device Reset to register defaults (SWRST) **/
#define STK8BA58_RST		0xB6U

/**
  * @}
  *
  */

#define STK8BA58_CHIP_ID	0x00U

#define STK8BA58_XOUT1		0x02U
#define STK8BA58_YOUT1		0x04U
#define STK8BA58_ZOUT1		0x06U
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t new		: 1;
	uint8_t not_used_01	: 3;
	uint8_t out		: 4;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t out		: 4;
	uint8_t not_used_01	: 3;
	uint8_t new		: 1;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_out1_t;

#define STK8BA58_XOUT2		0x03U
#define STK8BA58_YOUT2		0x05U
#define STK8BA58_ZOUT2		0x07U
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t out		: 8;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t out		: 8;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_out2_t;

#define STK8BA58_INTSTS1	0x09U
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t sig_mot_sts	: 1;
	uint8_t not_used_01	: 1;
	uint8_t any_mot_sts	: 1;
	uint8_t not_used_02	: 5;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t not_used_02	: 5;
	uint8_t any_mot_sts	: 1;
	uint8_t not_used_01	: 1;
	uint8_t sig_mot_sts	: 1;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_intsts1_t;

#define STK8BA58_INTSTS2	0x0AU
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t not_used_01	: 7;
	uint8_t data_sts	: 1;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t data_sts	: 1;
	uint8_t not_used_01	: 7;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_intsts2_t;

#define STK8BA58_EVENTINFO1	0x0BU
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t slp_1st_x	: 1;
	uint8_t slp_1st_y	: 1;
	uint8_t slp_1st_z	: 1;
	uint8_t not_used_01	: 1;
	uint8_t slpsign_x	: 1;
	uint8_t slpsign_y	: 1;
	uint8_t slpsign_z	: 1;
	uint8_t not_used_02	: 1;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t not_used_02	: 1;
	uint8_t slpsign_z	: 1;
	uint8_t slpsign_y	: 1;
	uint8_t slpsign_x	: 1;
	uint8_t not_used_01	: 1;
	uint8_t slp_1st_z	: 1;
	uint8_t slp_1st_y	: 1;
	uint8_t slp_1st_x	: 1;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_eventinfo1_t;

#define STK8BA58_RANGESEL	0x0FU
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t range		: 4;
	uint8_t not_used_01	: 4;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t not_used_01	: 4;
	uint8_t range		: 4;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_rangesel_t;

#define STK8BA58_BWSEL		0x10U
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t bw		: 5;
	uint8_t not_used_01	: 3;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t not_used_01	: 3;
	uint8_t bw		: 5;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_bwsel_t;

#define STK8BA58_POWMODE	0x11U
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t not_used_01	: 1;
	uint8_t sleep_dur	: 4;
	uint8_t not_used_02	: 1;
	uint8_t lowpower	: 1;
	uint8_t suspend		: 1;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t suspend		: 1;
	uint8_t lowpower	: 1;
	uint8_t not_used_02	: 1;
	uint8_t sleep_dur	: 4;
	uint8_t not_used_01	: 1;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_powmode_t;

#define STK8BA58_DATASETUP	0x13U
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t not_used_01	: 6;
	uint8_t protect_dis	: 1;
	uint8_t data_sel	: 1;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t data_sel	: 1;
	uint8_t protect_dis	: 1;
	uint8_t not_used_01	: 6;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_datasetup_t;

#define STK8BA58_SWRST		0x14U

#define STK8BA58_INTEN1		0x16U
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t slp_en_x	: 1;
	uint8_t slp_en_y	: 1;
	uint8_t slp_en_z	: 1;
	uint8_t not_used_01	: 5;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t not_used_01	: 5;
	uint8_t slp_en_z	: 1;
	uint8_t slp_en_y	: 1;
	uint8_t slp_en_x	: 1;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_inten1_t;

#define STK8BA58_INTEN2		0x17U
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t not_used_01	: 4;
	uint8_t data_en		: 1;
	uint8_t not_used_02	: 3;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t not_used_02	: 3;
	uint8_t data_en		: 1;
	uint8_t not_used_01	: 4;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_inten2_t;

#define STK8BA58_INTMAP1	0x19U
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t sigmot2int1	: 1;
	uint8_t not_used_01	: 1;
	uint8_t anymot2int1	: 1;
	uint8_t not_used_02	: 5;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t not_used_02	: 5;
	uint8_t anymot2int1	: 1;
	uint8_t not_used_01	: 1;
	uint8_t sigmot2int1	: 1;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_intmap1_t;

#define STK8BA58_INTMAP2	0x1AU
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t data2int1	: 1;
	uint8_t not_used_01	: 7;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t not_used_01	: 7;
	uint8_t data2int1	: 1;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_intmap2_t;

#define STK8BA58_INTCFG1	0x20U
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t int1_lv		: 1;
	uint8_t int1_od		: 1;
	uint8_t not_used_01	: 6;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t not_used_01	: 6;
	uint8_t int1_od		: 1;
	uint8_t int1_lv		: 1;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_intcfg1_t;

#define STK8BA58_INTCFG2	0x21U
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t int_latch	: 4;
	uint8_t not_used_01	: 3;
	uint8_t int_rst		: 1;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t int_rst		: 1;
	uint8_t not_used_01	: 3;
	uint8_t int_latch	: 4;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_intcfg2_t;

#define STK8BA58_SLOPEDLY	0x27U
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t slp_dur		: 2;
	uint8_t not_used_01	: 6;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t not_used_01	: 6;
	uint8_t slp_dur		: 2;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_slopedly_t;

#define STK8BA58_SLOPETHD	0x28U

#define STK8BA58_SIGMOT1	0x29U
#define STK8BA58_SIGMOT2	0x2AU
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t skip_time	: 1;
	uint8_t sig_mot_en	: 1;
	uint8_t any_mot_en	: 1;
	uint8_t not_used_01	: 5;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t not_used_01	: 5;
	uint8_t any_mot_en	: 1;
	uint8_t sig_mot_en	: 1;
	uint8_t skip_time	: 1;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_sigmot2_t;

#define STK8BA58_SIGMOT3	0x2BU
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t proof_time	: 7;
	uint8_t not_used_01	: 1;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t not_used_01	: 1;
	uint8_t proof_time	: 7;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_sigmot3_t;

#define STK8BA58_INTFCFG	0x34U
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t not_used_01	: 1;
	uint8_t i2c_wdt_sel	: 1;
	uint8_t i2c_wdt_en	: 1;
	uint8_t not_used_02	: 5;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t not_used_02	: 5;
	uint8_t i2c_wdt_en	: 1;
	uint8_t i2c_wdt_sel	: 1;
	uint8_t not_used_01	: 1;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_intfcfg_t;

#define STK8BA58_OFSTCOMP1	0x36U
typedef struct
{
#if DRV_BYTE_ORDER == DRV_LITTLE_ENDIAN
	uint8_t not_used_01	: 7;
	uint8_t ofst_rst	: 1;
#elif DRV_BYTE_ORDER == DRV_BIG_ENDIAN
	uint8_t ofst_rst	: 1;
	uint8_t not_used_01	: 7;
#endif /* DRV_BYTE_ORDER */
} stk8ba58_ofstcomp1_t;

#define STK8BA58_OFSTX		0x38U
#define STK8BA58_OFSTY		0x39U
#define STK8BA58_OFSTZ		0x3AU

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

typedef struct
{
	stk8ba58_intsts1_t	intsts1;
	stk8ba58_intsts2_t	intsts2;
	stk8ba58_eventinfo1_t	eventinfo1;
} stk8ba58_all_sources_t;
int32_t stk8ba58_all_sources_get(const struct i2c_dt_spec *i2c,
				 stk8ba58_all_sources_t *val);

typedef enum
{
	STK8BA58_2g		= 0b0011,
	STK8BA58_4g		= 0b0101,
	STK8BA58_8g		= 0b1000,
} stk8ba58_range_t;
int32_t stk8ba58_xl_range_set(const struct i2c_dt_spec *i2c,
			      stk8ba58_range_t val);
int32_t stk8ba58_xl_range_get(const struct i2c_dt_spec *i2c,
			      stk8ba58_range_t *val);

typedef enum
{
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
typedef enum
{
	STK8BA58_XL_DS_FILTERED   = 0,
	STK8BA58_XL_DS_UNFILTERED = 1,
} stk8ba58_ds_t;
int32_t stk8ba58_xl_bandwidth_set(const struct i2c_dt_spec *i2c,
				  stk8ba58_bw_t val, stk8ba58_ds_t sel);
int32_t stk8ba58_xl_bandwidth_get(const struct i2c_dt_spec *i2c,
				  stk8ba58_bw_t *val, stk8ba58_ds_t *sel);

typedef enum
{
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
typedef enum
{
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

typedef enum
{
  STK8BA58_PUSH_PULL		= 0,
  STK8BA58_OPEN_DRAIN		= 1,
} stk8ba58_pp_od_t;
int32_t stk8ba58_pin_int1_mode_set(const struct i2c_dt_spec *i2c,
				   stk8ba58_pp_od_t val);
int32_t stk8ba58_pin_int1_mode_get(const struct i2c_dt_spec *i2c,
				   stk8ba58_pp_od_t *val);

typedef enum
{
	STK8BA58_ACTIVE_LOW	= 0,
	STK8BA58_ACTIVE_HIGH	= 1,
} stk8ba58_hl_active_t;
int32_t stk8ba58_pin_int1_polarity_set(const struct i2c_dt_spec *i2c,
				       stk8ba58_hl_active_t val);
int32_t stk8ba58_pin_int1_polarity_get(const struct i2c_dt_spec *i2c,
				       stk8ba58_hl_active_t *val);

typedef enum
{
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

typedef struct
{
	uint8_t sigmot2int1	: 1;
	uint8_t anymot2int1	: 1;
	uint8_t data2int1	: 1;
} stk8ba58_pin_int1_route_t;
int32_t stk8ba58_pin_int1_route_set(const struct i2c_dt_spec *i2c,
				    stk8ba58_pin_int1_route_t val);
int32_t stk8ba58_pin_int1_route_get(const struct i2c_dt_spec *i2c,
				    stk8ba58_pin_int1_route_t *val);

typedef struct
{
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
