/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef ZEPHYR_INCLUDE_STEPPER_ACTION_STREAM_H_
#define ZEPHYR_INCLUDE_STEPPER_ACTION_STREAM_H_

#include <zephyr/drivers/stepper.h>
#include <zephyr/kernel.h>

#include "zephyr/sys/slist.h"

/**
 * @brief A stream of stepper action to be performed successively.
 */
struct stepper_action_stream {
	/** Stepper motor driver device. */
	const struct device *driver;
	/** Motor output index. */
	uint8_t motor;
	/** List of pending actions. */
	sys_slist_t actions;
	/** Signaling flag for starting/pausing the stream */
	bool running;
	/** Stream lock. */
	struct k_mutex lock;
	/** Thread stack of the stream handling thread. */
	k_thread_stack_t *thread_stack;
	/** Thread data of the stream handling thread. */
	struct k_thread thread_data;
	/** TID of the thread handling thread */
	k_tid_t thread_tid;
};

struct stepper_action_stream_item {
	sys_snode_t node;
	struct stepper_action action;
};

/**
 * @brief Initialize an action stream for a stepper motor.
 *
 * @param[out] stream The action stream to initialize.
 * @param driver The stepper motor driver device controlling the motor.
 * @param motor Motor output index.
 *
 * @retval 0       On success.
 * @retval -ENOMEM On allocation failure.
 * @return Negative error code on failure.
 */
int stepper_action_stream_init(struct stepper_action_stream *stream, const struct device *driver,
			       uint8_t motor);

/**
 * @brief Initialize an action stream for a stepper motor based on devicetree
 * specification.
 *
 * @details Equivalent to
 * `stepper_action_stream_init(stream, spec->driver, spec->motor)`
 *
 * @param[out] stream The action stream to initialize.
 * @param spec Devicetree specification of the stepper motor.
 *
 * @return A value from @ref stepper_action_stream_init.
 */
static inline int stepper_action_stream_init_dt(struct stepper_action_stream *stream,
						const struct stepper_motor_dt_spec *spec)
{
	if (spec == NULL) {
		return -EINVAL;
	}

	return stepper_action_stream_init(stream, spec->driver, spec->motor);
}

/**
 * @brief Begin executing actions from the action stream.
 *
 * @param stream Action stream.
 *
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int stepper_action_stream_start(struct stepper_action_stream *stream);

/**
 * @brief Stop executing actions from the action stream (but let the current
 * action finish).
 *
 * @param stream Action stream.
 *
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int stepper_action_stream_stop(struct stepper_action_stream *stream);

/**
 * @brief Append an action to the action stream.
 *
 * @param stream Action stream.
 * @param action The action to append.
 *
 * @retval 0 On success.
 * @retval -ENOMEM On allocation failure.
 * @return Negative error code on other failure.
 */
int stepper_action_stream_submit(struct stepper_action_stream *stream,
				 struct stepper_action *action);

/**
 * @brief Remove all pending actions from the action stream.
 *
 * @param stream Action stream.
 *
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int stepper_action_stream_purge(struct stepper_action_stream *stream);

/**
 * @brief Stop executing actions from the action stream (and immediately stop
 * the current action).
 *
 * @param stream Action stream.
 *
 * @retval 0 On success.
 * @return Negative error code on failure.
 */
int stepper_action_stream_abort(struct stepper_action_stream *stream);

#endif /* ZEPHYR_INCLUDE_STEPPER_ACTION_STREAM_H_ */
