/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/pwm.h>
#include <zephyr/kernel.h>
#include <stdlib.h>
#include <string.h>

#include "zephyr/sys/slist.h"
#include "zephyr/sys/util.h"
#include "zephyr/sys_clock.h"

const struct gpio_dt_spec enable_pin =
    GPIO_DT_SPEC_GET(DT_PATH(zephyr_user), enable_gpios);
const struct gpio_dt_spec sleep_pin =
    GPIO_DT_SPEC_GET(DT_PATH(zephyr_user), sleep_gpios);
const struct gpio_dt_spec direction_pin =
    GPIO_DT_SPEC_GET(DT_PATH(zephyr_user), direction_gpios);
const struct pwm_dt_spec pwm = PWM_DT_SPEC_GET(DT_PATH(zephyr_user));

enum stepper_action_type {
	STEPPER_ACTION_POSIIONING,
	STEPPER_ACTION_VELOCITY,
	STEPPER_ACTION_ACCELERATION,
};

struct stepper_action {
	/** Type of this action. */
	enum stepper_action_type type;
	/** Additional flags, e.g. microstep resolution. */
	uint32_t flags;
	union {
		/** Step-precise movement with constant velocity. */
		struct positioning_action {
			/** Stepping velocity during this movement
			 * (milli-arcseconds/s). Sign encodes direction.
			 */
			int32_t velocity;
			/** Number of steps to take */
			uint32_t steps;
		} positioning;
		/** Coasting at constant velocity for specified time */
		struct velocity_action {
			/** Stepping velocity (milli-arcseconds/s) (sign encodes
			 * direction).
			 */
			int32_t velocity;
			/** Coasting time in microseconds. */
			uint32_t duration_us;
		} velocity;
		struct acceleration_action {
			/** Stepping velocity at the start of the action
			 * (milli-arcseconds/s). */
			int32_t start_velocity;
			/** Stepping velocity at the end of the action
			 * (milli-arcseconds(s). */
			int32_t end_velocity;
			/** Duration of the action in microseconds */
			uint32_t duration_us;
		} acceleration;
	} action;
};

struct stepper_action_stream_item {
	sys_snode_t node;
	struct stepper_action action;
};

typedef sys_slist_t stepper_action_stream_t;

void stepper_action_stream_init(stepper_action_stream_t *stream) {
	sys_slist_init(stream);
}

int stepper_action_stream_append(stepper_action_stream_t *stream, struct stepper_action *action) {
	struct stepper_action_stream_item *stream_item = k_calloc(1, sizeof(struct stepper_action_stream_item));
	memcpy(&stream_item->action, action, sizeof stream_item->action);
	sys_slist_append(stream, &stream_item->node);
	return 0;
}

int stepper_action_stream_get(stepper_action_stream_t *stream, struct stepper_action *action) {
	sys_snode_t *node = sys_slist_get(stream);
	if (node == NULL) {
		return -1;
	}
	struct stepper_action_stream_item *item = CONTAINER_OF(node, struct stepper_action_stream_item, node);
	memcpy(action, &item->action, sizeof item->action);
	k_free(item);
	return 0;
}

int set_direction(int32_t velocity) {
	int value = 0;
	if (velocity >= 0) {
		value = 1;
	} else {
		value = 0;
	}
	return gpio_pin_set_dt(&direction_pin, value);
}

int pwm_off(void) { return pwm_set_cycles(pwm.dev, pwm.channel, 1, 0, 0); }

int set_pwm_freq(uint32_t freq_hz) {
	if (freq_hz == 0) {
		return pwm_off();
	}
	uint32_t pulse_width_ns = NSEC_PER_SEC / freq_hz;
	return pwm_set_dt(&pwm, pulse_width_ns, pulse_width_ns / 2);
}

int do_action(const struct stepper_action *action) {
	if (action->type == STEPPER_ACTION_VELOCITY) {
		int32_t velocity = action->action.velocity.velocity;
		uint32_t time_us = action->action.velocity.duration_us;
		uint32_t freq = velocity;  // pretend v is steps/s
		set_direction(velocity);
		set_pwm_freq(freq);
		k_sleep(K_USEC(time_us));
		pwm_off();
	} else if (action->type == STEPPER_ACTION_ACCELERATION) {

		uint32_t duration_us = action->action.acceleration.duration_us;
		int32_t start_velocity = action->action.acceleration.start_velocity;
		int32_t end_velocity = action->action.acceleration.end_velocity;

		uint32_t dt_us = 1000; // 1 ms
		uint64_t start_time = k_uptime_get() * USEC_PER_MSEC;
		uint64_t finish_time = start_time + duration_us;

		uint64_t now = 0;
		while ((now = (k_uptime_get() * USEC_PER_MSEC)) < finish_time) {
			int32_t t_milliunit = ((1000 * (now - start_time)) / duration_us);
			int32_t velocity = ((1000 - t_milliunit) * start_velocity + t_milliunit * end_velocity) / 1000;
			set_direction(velocity);
			set_pwm_freq(abs(velocity)); // pretend unit is steps/s
			k_sleep(K_USEC(dt_us));
		}
		set_pwm_freq(end_velocity);

	} else {
		return -1;
	}

	return 0;
}

stepper_action_stream_t action_stream = SYS_SLIST_STATIC_INIT(&action_stream);

void stream_handler_thread_fn(void) {
	struct stepper_action action = {0};
	while (true) {

		if (stepper_action_stream_get(&action_stream, &action) == 0) {
			do_action(&action);
		} else {
			k_msleep(100);
		}
	}
}

K_THREAD_DEFINE(stepper_action_stream_handler, 4096, stream_handler_thread_fn, NULL, NULL, NULL, 10, 0, 0);

int main(void) {
	printk("Hello world!\n");

	printk("Initializing pins\n");
	gpio_pin_configure_dt(&enable_pin, GPIO_OUTPUT_ACTIVE);
	gpio_pin_configure_dt(&sleep_pin, GPIO_OUTPUT_INACTIVE);
	gpio_pin_configure_dt(&direction_pin, GPIO_OUTPUT_INACTIVE);

	printk("Trying some actions\n");

	struct stepper_action a1 = {
		.type = STEPPER_ACTION_ACCELERATION,
		.action.acceleration = {
			.duration_us = 2 * USEC_PER_SEC,
			.start_velocity = 10,
			.end_velocity = 500,
		},
	};
	struct stepper_action a2 = {
		.type = STEPPER_ACTION_VELOCITY,
		.action.velocity = {
			.duration_us = 10 * USEC_PER_SEC,
			.velocity = 500,
		},
	};
	struct stepper_action a3 = {
		.type = STEPPER_ACTION_ACCELERATION,
		.action.acceleration = {
			.duration_us = 3 * USEC_PER_SEC,
			.start_velocity = 500,
			.end_velocity = -200,
		},
	};
	struct stepper_action a4 = {
		.type = STEPPER_ACTION_VELOCITY,
		.action.velocity = {
			.duration_us = 10 * USEC_PER_SEC,
			.velocity = -200,
		},
	};
	struct stepper_action a5 = {
		.type = STEPPER_ACTION_ACCELERATION,
		.action.acceleration = {
			.duration_us = 1 * USEC_PER_SEC,
			.start_velocity = -200,
			.end_velocity = 0,
		},
	};

	stepper_action_stream_append(&action_stream, &a1);
	stepper_action_stream_append(&action_stream, &a2);
	stepper_action_stream_append(&action_stream, &a3);
	stepper_action_stream_append(&action_stream, &a4);
	stepper_action_stream_append(&action_stream, &a5);

	k_sleep(K_SECONDS(10));

	stepper_action_stream_append(&action_stream, &a1);
	stepper_action_stream_append(&action_stream, &a2);
	stepper_action_stream_append(&action_stream, &a3);
	stepper_action_stream_append(&action_stream, &a4);
	stepper_action_stream_append(&action_stream, &a5);


	printk("Done!\n");

	return 0;
}
