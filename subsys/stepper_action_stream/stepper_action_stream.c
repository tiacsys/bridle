/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <string.h>
#include <zephyr/drivers/stepper.h>
#include <zephyr/kernel.h>
#include <zephyr/subsys/stepper_action_stream.h>
#include <zephyr/sys/slist.h>

#include "zephyr/sys/util.h"

/**
 * @brief Gets the next pending action from a stream. Free's the heap-allocated
 * stream node.
 *
 * @param list Action stream to query.
 * @param[out] action The next pending action.
 *
 * @retval true  If an action is pending.
 * @retval false If no action is pending.
 */
static bool stepper_action_stream_item_get(sys_slist_t *list, struct stepper_action *action)
{
	sys_snode_t *node = sys_slist_get(list);
	if (node == NULL) {
		return false;
	}

	struct stepper_action_stream_item *item =
		CONTAINER_OF(node, struct stepper_action_stream_item, node);
	memcpy(action, &item->action, sizeof item->action);
	k_free(item);
	return true;
}

static void stepper_action_stream_handler_thread_fn(void *stream_raw, void *arg2, void *arg3)
{
	ARG_UNUSED(arg2);
	ARG_UNUSED(arg3);

	struct stepper_action_stream *stream = (struct stepper_action_stream *)stream_raw;

	struct stepper_action action = {0};
	bool pending = false;

	while (true) {
		do {
			/* If we're paused, wait until we're unpaused */
			k_mutex_lock(&stream->lock, K_FOREVER);
			bool running = stream->running;
			k_mutex_unlock(&stream->lock);

			if (!running) {
				k_msleep(10);
				continue;
			}

			/* Check for pending actions */
			k_mutex_lock(&stream->lock, K_FOREVER);
			pending = stepper_action_stream_item_get(&stream->actions, &action);
			k_mutex_unlock(&stream->lock);

			/* If an action is pending, perform it */
			if (pending) {
				stepper_move(stream->driver, stream->motor, &action);
			}
		} while (pending);

		k_msleep(10);
	}
}

int stepper_action_stream_init(struct stepper_action_stream *stream, const struct device *driver,
			       uint8_t motor)
{
	/* Initialize basic members */
	stream->driver = driver;
	stream->motor = motor;
	sys_slist_init(&stream->actions);
	stream->running = false;
	k_mutex_init(&stream->lock);

	/* Allocate thread stack */
	stream->thread_stack =
		k_thread_stack_alloc(CONFIG_STEPPER_ACTION_STREAM_THREAD_STACK_SIZE, 0);
	if (stream->thread_stack == NULL) {
		return -ENOMEM;
	}

	/* Create and launch associated thread */
	stream->thread_tid =
		k_thread_create(&stream->thread_data, stream->thread_stack,
				CONFIG_STEPPER_ACTION_STREAM_THREAD_STACK_SIZE,
				stepper_action_stream_handler_thread_fn, (void *)stream, NULL, NULL,
				CONFIG_STEPPER_ACTION_STREAM_THREAD_PRIO, 0, K_NO_WAIT);

	return 0;
}

int stepper_action_stream_start(struct stepper_action_stream *stream)
{
	k_mutex_lock(&stream->lock, K_FOREVER);
	stream->running = true;
	k_mutex_unlock(&stream->lock);

	return 0;
}

int stepper_action_stream_stop(struct stepper_action_stream *stream)
{
	k_mutex_lock(&stream->lock, K_FOREVER);
	stream->running = false;
	k_mutex_unlock(&stream->lock);

	return 0;
}

int stepper_action_stream_submit(struct stepper_action_stream *stream,
				 struct stepper_action *action)
{
	/* Make a copy of the given action */
	struct stepper_action_stream_item *item =
		k_calloc(1, sizeof(struct stepper_action_stream_item));
	if (item == NULL) {
		return -ENOMEM;
	}
	memcpy(&item->action, action, sizeof item->action);

	/* Append the item to the list */
	k_mutex_lock(&stream->lock, K_FOREVER);
	sys_slist_append(&stream->actions, &item->node);
	k_mutex_unlock(&stream->lock);

	return 0;
}

int stepper_action_stream_purge(struct stepper_action_stream *stream)
{
	k_mutex_lock(&stream->lock, K_FOREVER);
	sys_snode_t *node = NULL;
	while ((node = sys_slist_get(&stream->actions)) != NULL) {
		struct stepper_action_stream_item *item =
			CONTAINER_OF(node, struct stepper_action_stream_item, node);
		k_free(item);
	}
	k_mutex_unlock(&stream->lock);

	return 0;
}

int stepper_action_stream_abort(struct stepper_action_stream *stream)
{
	/* Holding this lock prevents the handler thread from fetching new
	 * actions to start */
	k_mutex_lock(&stream->lock, K_FOREVER);

	/* Perform a stop action directly, bypassing the stream */
	const struct stepper_action stop = STEPPER_ACTION_STOP;
	stepper_move(stream->driver, stream->motor, &stop);
	stream->running = false;

	/* The pause signal is set, so we can drop the lock safely */
	k_mutex_unlock(&stream->lock);

	/* Finally, purge the remaining items */
	return stepper_action_stream_purge(stream);
}
