/*
 * Copyright (c) 2019 Linaro Limited
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <math.h>
#include <stdio.h>
#include <zephyr/kernel.h>

#include <zephyr/device.h>
#include <zephyr/drivers/counter.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/pinctrl.h>
#include <zephyr/drivers/pwm.h>
#include <zephyr/sys/printk.h>

#define DELAY 250000
#define TOP 2500
#define ALARM_CHANNEL_ID 0

struct counter_alarm_cfg alarm_cfg;

static const struct gpio_dt_spec pin_stepper =
    GPIO_DT_SPEC_GET(DT_PATH(zephyr_user), stepper_gpios);
static const struct gpio_dt_spec m0 =
    GPIO_DT_SPEC_GET(DT_PATH(drv8424), m0_gpios);
static const struct gpio_dt_spec m1 =
    GPIO_DT_SPEC_GET(DT_PATH(drv8424), m1_gpios);

// #if defined(CONFIG_BOARD_SAMD20_XPRO)
// #define TIMER DT_NODELABEL(tc4)
// #elif defined(CONFIG_SOC_FAMILY_ATMEL_SAM)
// #define TIMER DT_NODELABEL(tc0)
// #elif defined(CONFIG_COUNTER_MICROCHIP_MCP7940N)
// #define TIMER DT_NODELABEL(extrtc0)
// #elif defined(CONFIG_COUNTER_NRF_RTC)
// #define TIMER DT_NODELABEL(rtc0)
// #elif defined(CONFIG_COUNTER_TIMER_STM32)
// #define TIMER DT_INST(0, st_stm32_counter)
// #elif defined(CONFIG_COUNTER_RTC_STM32)
// #define TIMER DT_INST(0, st_stm32_rtc)
// #elif defined(CONFIG_COUNTER_SMARTBOND_TIMER)
// #define TIMER DT_NODELABEL(timer3)
// #elif defined(CONFIG_COUNTER_NATIVE_POSIX)
// #define TIMER DT_NODELABEL(counter0)
// #elif defined(CONFIG_COUNTER_XLNX_AXI_TIMER)
// #define TIMER DT_INST(0, xlnx_xps_timer_1_00_a)
// #elif defined(CONFIG_COUNTER_TMR_ESP32)
// #define TIMER DT_NODELABEL(timer0)
// #elif defined(CONFIG_COUNTER_MCUX_CTIMER)
// #define TIMER DT_NODELABEL(ctimer0)
// #elif defined(CONFIG_COUNTER_NXP_S32_SYS_TIMER)
// #define TIMER DT_NODELABEL(stm0)
// #elif defined(CONFIG_COUNTER_TIMER_GD32)
// #define TIMER DT_NODELABEL(timer0)
// #elif defined(CONFIG_COUNTER_GECKO_RTCC)
// #define TIMER DT_NODELABEL(rtcc0)
// #elif defined(CONFIG_COUNTER_GECKO_STIMER)
// #define TIMER DT_NODELABEL(stimer0)
// #elif defined(CONFIG_COUNTER_INFINEON_CAT1)
// #define TIMER DT_NODELABEL(counter0_0)
// #elif defined(CONFIG_COUNTER_AMBIQ)
// #define TIMER DT_NODELABEL(counter0)
// #elif defined(CONFIG_COUNTER_SNPS_DW)
// #define TIMER DT_NODELABEL(timer0)
// #elif defined(CONFIG_COUNTER_TIMER_RPI_PICO)
// #define TIMER DT_NODELABEL(timer)
// #else
// #error Unable to find a counter device node in devicetree
// #endif

#define TIMER DT_NODELABEL(counter2)
#define ACCURATE_STEPS 15

enum Ramp_State { RAMP_ACCELERATION, RAMP_CONST, RAMP_DECELERATION, RAMP_NONE };

struct callback_data {
	enum Ramp_State ramp_state;
	float current_time;
	float base_time;
	struct counter_top_cfg *top_cfg;
	uint32_t accel_steps;
	uint32_t const_steps;
	uint32_t decel_steps;
	uint32_t n;
	bool rising;
};

static void test_counter_top_fn(const struct device *dev, void *user_data) {
	struct callback_data *data;
	data = (struct callback_data *)user_data;

	float t_1;

	if (data->ramp_state == RAMP_ACCELERATION) {
		if (!data->rising) {
			data->n++;
			gpio_pin_set_dt(&pin_stepper, 0);
		} else {
			if (data->n >
			    ACCURATE_STEPS) { /* Use Approximation, once error
						 is small enough*/
				float t_n_1 = data->current_time;
				float adjust = 2 * t_n_1 / (4 * data->n + 1);
				t_1 = t_n_1 - adjust;
			} else {
				t_1 = data->base_time *
				      (sqrtf(data->n + 1) - sqrtf(data->n));
			}
			data->top_cfg->ticks =
			    counter_us_to_ticks(dev, (uint32_t)t_1 / 2);
			data->current_time = t_1;
			gpio_pin_set_dt(&pin_stepper, 1);
			counter_set_top_value(dev, data->top_cfg);
		}
	}
	if (data->ramp_state == RAMP_CONST) {
		if (!data->rising) {
			data->n++;
			gpio_pin_set_dt(&pin_stepper, 0);
		} else {
			gpio_pin_set_dt(&pin_stepper, 1);
		}
	}
	if (data->ramp_state == RAMP_DECELERATION) {
		if (!data->rising) {
			data->n--;
			gpio_pin_set_dt(&pin_stepper, 0);
		} else {
			if (data->n >
			    ACCURATE_STEPS) { /* Use Approximation, as long as
						 error is small enough*/
				float t_n = data->current_time;
				float adjust = 2 * t_n / (4 * data->n - 1);
				t_1 = t_n + adjust;
			} else {
				t_1 = data->base_time *
				      (sqrtf(data->n + 1) - sqrtf(data->n));
			}
			data->top_cfg->ticks =
			    counter_us_to_ticks(dev, (uint32_t)t_1 / 2);
			data->current_time = t_1;
			gpio_pin_set_dt(&pin_stepper, 1);
			counter_set_top_value(dev, data->top_cfg);
		}
	}
	data->rising = !data->rising;

	if (data->ramp_state == RAMP_ACCELERATION &&
	    data->n - 1 == data->accel_steps) {
		if (data->const_steps == 0) {
			data->ramp_state = RAMP_DECELERATION;
			data->n = data->decel_steps;
		} else {
			data->ramp_state = RAMP_CONST;
			data->n = 1;
		}
		printk("%u\n", (uint32_t)data->current_time);
	}
	if (data->ramp_state == RAMP_CONST &&
	    data->n - 1 == data->const_steps) {
		data->ramp_state = RAMP_DECELERATION;
		data->n = data->decel_steps;
	}
	if (data->ramp_state == RAMP_DECELERATION && data->n == 0) {
		data->ramp_state = RAMP_NONE;
		counter_stop(dev);
	}
}

static void trapeze_deceleration(const struct device *dev, void *user_data) {
	struct callback_data *data;
	data = (struct callback_data *)user_data;

	float t_1;

	if (!data->rising) {
		data->n--;
		gpio_pin_set_dt(&pin_stepper, 0);
	} else {
		if (data->n > ACCURATE_STEPS) { /* Use Approximation, as long as
						   error is small enough*/
			float t_n = data->current_time;
			float adjust = 2 * t_n / (4 * data->n - 1);
			t_1 = t_n + adjust;
		} else {
			t_1 = data->base_time *
			      (sqrtf(data->n + 1) - sqrtf(data->n));
		}
		data->top_cfg->ticks =
		    counter_us_to_ticks(dev, (uint32_t)t_1 / 2);
		data->current_time = t_1;
		gpio_pin_set_dt(&pin_stepper, 1);
		counter_set_top_value(dev, data->top_cfg);
	}
	data->rising = !data->rising;

	if (data->n == 0) {
		counter_stop(dev);
		printk("Finished\n");
	}
}

static void trapeze_constant(const struct device *dev, void *user_data) {
	struct callback_data *data;
	data = (struct callback_data *)user_data;

	if (!data->rising) {
		data->n++;
		gpio_pin_set_dt(&pin_stepper, 0);
	} else {
		gpio_pin_set_dt(&pin_stepper, 1);
	}
	data->rising = !data->rising;

	if (data->n - 1 == data->const_steps) {
		data->n = data->decel_steps;
		data->top_cfg->callback = trapeze_deceleration;
		counter_set_top_value(dev, data->top_cfg);
	}
}

static void trapeze_acceleration(const struct device *dev, void *user_data) {
	struct callback_data *data;
	data = (struct callback_data *)user_data;

	float t_1;

	if (!data->rising) {
		data->n++;
		gpio_pin_set_dt(&pin_stepper, 0);
	} else {
		if (data->n > ACCURATE_STEPS) { /* Use Approximation, once error
						   is small enough*/
			float t_n_1 = data->current_time;
			float adjust = 2 * t_n_1 / (4 * data->n + 1);
			t_1 = t_n_1 - adjust;
		} else {
			t_1 = data->base_time *
			      (sqrtf(data->n + 1) - sqrtf(data->n));
		}
		data->top_cfg->ticks =
		    counter_us_to_ticks(dev, (uint32_t)t_1 / 2);
		data->current_time = t_1;
		gpio_pin_set_dt(&pin_stepper, 1);
		counter_set_top_value(dev, data->top_cfg);
	}
	data->rising = !data->rising;

	if (data->n - 1 == data->accel_steps) {
		if (data->const_steps == 0) {
			data->n = data->decel_steps;
			data->top_cfg->callback = trapeze_deceleration;
			counter_set_top_value(dev, data->top_cfg);
		} else {
			data->n = 1;
			data->top_cfg->callback = trapeze_constant;
			counter_set_top_value(dev, data->top_cfg);
		}
		// printk("%u\n", (uint32_t)data->current_time);
	}
}

int main(void) {
	const struct device *const counter_dev = DEVICE_DT_GET(TIMER);
	gpio_pin_configure_dt(&pin_stepper, GPIO_OUTPUT_INACTIVE);
	gpio_pin_configure_dt(
	    &m0,
	    GPIO_OUTPUT_ACTIVE); /* Activating microstep mode, not required*/
	gpio_pin_configure_dt(
	    &m1,
	    GPIO_OUTPUT_ACTIVE); /* Activating microstep mode, not required*/

	printk("Counter alarm sample\n\n");

	if (!device_is_ready(counter_dev)) {
		printk("device not ready.\n");
		return 0;
	}

	/* Input Area*/
	float velocity = 6400;	       /* steps/s*/
	uint32_t steps = 12800 + 6400; /* steps*/
	float accel_time = 2.0;	       /* s*/

	uint32_t accel_steps = (velocity * accel_time) / 2; /* steps*/
	uint32_t decel_steps = accel_steps;		    /* steps*/
	uint32_t const_steps;				    /* steps*/

	if (2 * accel_steps > steps) { /* Max speed not achievable*/
		const_steps = 0;
		if ((2 * accel_steps - steps) % 2 == 0) {
			accel_steps =
			    accel_steps - (2 * accel_steps - steps) / 2;
			decel_steps = accel_steps;
		} else {
			accel_steps =
			    accel_steps - (2 * accel_steps - steps) / 2;
			decel_steps = accel_steps;
			accel_steps++; /* Compensate for uneven number of
					  steps*/
		}
	} else {
		const_steps = steps - 2 * accel_steps;
	}

	float acceleration =
	    (velocity * velocity) / (2 * accel_steps); /* steps/s² */
	float t_1 = sqrt(2.0 / acceleration) *
		    1000000U; /* micro s (via 1000000), 2.0 contains *1 step*/

	struct callback_data cb_data;
	cb_data.ramp_state = RAMP_ACCELERATION;
	cb_data.current_time = t_1;
	cb_data.base_time = t_1;
	cb_data.accel_steps = accel_steps;
	cb_data.const_steps = const_steps;
	cb_data.decel_steps = decel_steps;
	cb_data.n = 1;
	cb_data.rising = true;

	struct counter_top_cfg top_cfg;
	top_cfg.callback = trapeze_acceleration;
	top_cfg.ticks = counter_us_to_ticks(counter_dev, (uint32_t)t_1 / 2);
	top_cfg.user_data = &cb_data;
	top_cfg.flags = COUNTER_TOP_CFG_DONT_RESET;

	cb_data.top_cfg = &top_cfg;

	counter_set_top_value(counter_dev, &top_cfg);
	counter_start(counter_dev);

	while (1) {
		k_sleep(K_FOREVER);
	}
	return 0;
}
