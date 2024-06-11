/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/device.h>

#include <zephyr/drivers/mfd/sc18is604.h>

#include "i2c_sc18is604.h"

/*
 * Asynchronous message transfers are processed by a tracking structure
 * being passed between 3 separate work items: One for initiating transfers,
 * one for performing RX buffer readouts, and one for awaiting completion of
 * one message being processed.
 *
 * These work items can both re-schedule themselves to wait on data or locks
 * without blocking, and they schedule each other to progress message
 * processing.
 *
 * On completion, or if unrecoverable errors occur, each work item can call
 * out to a shared completion function, which propagates the final return
 * value to the user provided callback.
 *
 * A driver instance wide lock ensures that only one packet of messages given
 * to `i2c_transfer_cb` is processed at the same time. Multiple calls can still
 * be made in succession, but it is not guaranteed that they will be processed
 * in the order they are submitted.
 */

/** Data structure for tracking a asynchronous I2C transfer. */
typedef struct i2c_sc18is604_transfer_cb_work {
	/** Work items performing the transfer. */
	struct k_work work_init_msg;
	struct k_work work_buffer_readout;
	struct k_work work_finish_msg;
	/** Device performing this transfer. */
	const struct device *dev;
	/** Whether this transfer holds the transaction lock. */
	bool owns_lock;
	/** Signal used during processing to await individual message transfers. */
	struct k_poll_signal signal;
	/** Index of the message currently being processed. */
	uint8_t msg_index;
	/** Messages to be processed. */
	struct i2c_msg *msgs;
	/** Number of messages to be processed. */
	uint8_t num_msgs;
	/** I2C bus address the messages should be sent to. */
	uint16_t addr;
	/** User callback to be called once all messages are processed. */
	i2c_callback_t cb;
	/** User provided data for the callback. */
	void *userdata;
} transfer_work_t;

/*
 * Finish an asynchronous transfer with some result,
 * cleaning up locks and resources.
 */
static void i2c_sc18is604_transfer_cb_process_done(
					transfer_work_t *transfer_work,
					int result)
{
	const struct device *dev = transfer_work->dev;
	i2c_sc18is604_data_t * const data = dev->data;

	/* Release driver lock */
	k_sem_give(&data->lock);

	/* Free this work item */
	i2c_callback_t cb = transfer_work->cb;
	void *userdata = transfer_work->userdata;

	k_free(transfer_work);

	/* Fire user callback */
	cb(dev, result, userdata);
}

static void i2c_sc18is604_init_msg_read(transfer_work_t *transfer_work,
					uint16_t addr, struct i2c_msg *msg)
{
	const struct device *dev = transfer_work->dev;
	const i2c_sc18is604_config_t * const config = dev->config;
	int ret = 0;

	/* Call asynchronous transfer function with our internal signal. */
	uint8_t cmd[] = {SC18IS604_CMD_READ_I2C, msg->len, (uint8_t) addr};

	ret = mfd_sc18is604_transfer_signal(config->parent_dev,
					    cmd, ARRAY_SIZE(cmd),
					    NULL, 0, NULL, 0,
					    &transfer_work->signal);
	if (ret != 0) {
		mfd_sc18is604_release(config->parent_dev);
		i2c_sc18is604_transfer_cb_process_done(transfer_work, -EIO);
		return;
	}

	/* Schedule next work item to continue processing this message */
	ret = k_work_submit(&transfer_work->work_buffer_readout);
	if (ret != 1 && ret != 0) {
		mfd_sc18is604_release(config->parent_dev);
		i2c_sc18is604_transfer_cb_process_done(transfer_work, -EIO);
		return;
	}
}

static void i2c_sc18is604_init_msg_write(transfer_work_t *transfer_work,
					 uint16_t addr, struct i2c_msg *msg)
{
	const struct device *dev = transfer_work->dev;
	const i2c_sc18is604_config_t * const config = dev->config;
	int ret = 0;

	uint8_t cmd[] = {SC18IS604_CMD_WRITE_I2C, msg->len, (uint8_t) addr};

	/* Call asynchronous transfer function with our internal signal. */
	ret = mfd_sc18is604_transfer_signal(config->parent_dev,
					    cmd, ARRAY_SIZE(cmd),
					    msg->buf, msg->len,
					    NULL, 0,
					    &transfer_work->signal);
	if (ret != 0) {
		i2c_sc18is604_transfer_cb_process_done(transfer_work, -EIO);
		return;
	}

	/* Schedule final work item to finish processing this message */
	ret = k_work_submit(&transfer_work->work_finish_msg);
	if (ret != 1 && ret != 0) {
		i2c_sc18is604_transfer_cb_process_done(transfer_work, -EIO);
		return;
	}
}

static void i2c_sc18is604_init_msg_work_fn(struct k_work *work)
{
	transfer_work_t *transfer_work = CONTAINER_OF(work,
				transfer_work_t, work_init_msg);
	const struct device *dev = transfer_work->dev;
	i2c_sc18is604_data_t * const data = dev->data;
	int ret = 0;

	/* Get device lock, or reschedule to retry later */
	if (!transfer_work->owns_lock) {
		ret = k_sem_take(&data->lock, K_NO_WAIT);
		if (ret != 0) {
			ret = k_work_submit(work);
			if (ret != 1 && ret != 0) {
				i2c_sc18is604_transfer_cb_process_done(
						transfer_work, -EIO);
				return;
			}
			return;
		}
	}

	/* Make sure there is a message to transfer */
	uint8_t index = transfer_work->msg_index;

	if (index >= transfer_work->num_msgs) {
		i2c_sc18is604_transfer_cb_process_done(transfer_work, 0);
	}

	/*
	 * Reset signals
	 */

	/* Signals completion of communication *with* the device */
	k_poll_signal_reset(&transfer_work->signal);
	/* Signals comletion of the command *by* the device */
	k_poll_signal_reset(&data->interrupt_signal);

	/* Begin processing the i-th message */
	struct i2c_msg *msg = &transfer_work->msgs[index];

	/* Device doesn't support 10bit addressing */
	if ((msg->flags & I2C_MSG_ADDR_10_BITS) == I2C_MSG_ADDR_10_BITS) {
		i2c_sc18is604_transfer_cb_process_done(transfer_work, -EINVAL);
		return;
	}

	/* Add RW bit to address */
	uint16_t addr = transfer_work->addr;

	addr <<= 1;
	addr |= (msg->flags & I2C_MSG_RW_MASK);

	/* Process message depending on type */
	if ((msg->flags & I2C_MSG_READ) == I2C_MSG_READ) {
		i2c_sc18is604_init_msg_read(transfer_work, addr, msg);
		return;
	}

	/* If it's not a 'read' message, it must be a 'write' message */
	i2c_sc18is604_init_msg_write(transfer_work, addr, msg);
}

static void i2c_sc18is604_buffer_readout_work_fn(struct k_work *work)
{
	transfer_work_t *transfer_work = CONTAINER_OF(work,
				transfer_work_t, work_buffer_readout);
	const struct device *dev = transfer_work->dev;
	const i2c_sc18is604_config_t * const config = dev->config;
	i2c_sc18is604_data_t * const data = dev->data;
	int ret = 0;

	/* Await completion of the previous transfer */
	int result = 0;
	int signaled = await_signal(&transfer_work->signal, &result, K_NO_WAIT);

	if (!signaled) {
		ret = k_work_submit(work);
		if (ret != 1 && ret != 0) {
			i2c_sc18is604_transfer_cb_process_done(transfer_work, -EIO);
			return;
		}
		return;
	}

	if (result != 0) {
		i2c_sc18is604_transfer_cb_process_done(transfer_work, -EIO);
		return;
	}

	/* Await interrupt signal */
	signaled = await_signal(&data->interrupt_signal, &result, K_NO_WAIT);
	if (!signaled) {
		/*
		 * We didn't reset the transfer signal, so we'll fall through
		 * to awaiting the interrupt again next time.
		 */
		ret = k_work_submit(work);
		if (ret != 1 && ret != 0) {
			i2c_sc18is604_transfer_cb_process_done(transfer_work, -EIO);
			return;
		}
		return;
	}

	/*
	 * Check contents of I2C_STATUS register (propagated through
	 * interrupt signal)
	 */
	if (result != SC18IS604_I2C_STATUS_SUCCESS) {
		i2c_sc18is604_transfer_cb_process_done(transfer_work, -EIO);
		return;
	}

	/* Reset signal */
	k_poll_signal_reset(&transfer_work->signal);

	/* Begin readout of the received data from device buffer */
	uint8_t index = transfer_work->msg_index;
	struct i2c_msg *msg = &transfer_work->msgs[index];

	ret = mfd_sc18is604_read_buffer_signal(config->parent_dev,
					       msg->buf, msg->len,
					       &transfer_work->signal);
	if (ret != 0) {
		i2c_sc18is604_transfer_cb_process_done(transfer_work, -EIO);
		return;
	}

	/* Schedule final work item to finish processing this message */
	ret = k_work_submit(&transfer_work->work_finish_msg);
	if (ret != 1 && ret != 0) {
		i2c_sc18is604_transfer_cb_process_done(transfer_work, -EIO);
		return;
	}
}

static void i2c_sc18is604_finish_msg_work_fn(struct k_work *work)
{
	transfer_work_t *transfer_work = CONTAINER_OF(work,
				transfer_work_t, work_finish_msg);
	const struct device *dev = transfer_work->dev;
	i2c_sc18is604_data_t * const data = dev->data;
	int ret = 0;

	int result = 0;
	int signaled = await_signal(&transfer_work->signal, &result, K_NO_WAIT);

	if (!signaled) {
		ret = k_work_submit(work);
		if (ret != 1 && ret != 0) {
			i2c_sc18is604_transfer_cb_process_done(transfer_work, -EIO);
			return;
		}
		return;
	}

	/*
	 * For I2C_WRITE messages, we also need to await the interrupt signal.
	 * For I2C_READ messages, we're awaiting completion of an RX buffer
	 * readout, which doesn't require confirmation via interrupt.
	 */

	uint8_t index = transfer_work->msg_index;
	struct i2c_msg *msg = &transfer_work->msgs[index];

	if ((msg->flags & I2C_MSG_READ) != I2C_MSG_READ) {
		signaled = await_signal(&data->interrupt_signal, &result, K_NO_WAIT);
		if (!signaled) {
			ret = k_work_submit(work);
			if (ret != 1 && ret != 0) {
				i2c_sc18is604_transfer_cb_process_done(
							transfer_work, -EIO);
				return;
			}
			return;
		}

		/*
		 * Check status read from I2C_STATUS (returned through interrupt
		 * signal).
		 */
		if (result != SC18IS604_I2C_STATUS_SUCCESS) {
			i2c_sc18is604_transfer_cb_process_done(transfer_work, -EIO);
			return;
		}
	}

	/* We've finished processing this message. Check if there are more. */
	transfer_work->msg_index += 1;
	if (transfer_work->msg_index >= transfer_work->num_msgs) {
		/* We've successfully processed all messages */
		i2c_sc18is604_transfer_cb_process_done(transfer_work, 0);
		return;
	}

	/* Schedule work item to begin processing the next message */
	ret = k_work_submit(&transfer_work->work_init_msg);
	if (ret != 1 && ret != 0) {
		i2c_sc18is604_transfer_cb_process_done(transfer_work, -EIO);
		return;
	}
}

int i2c_sc18is604_transfer_cb(const struct device *dev,
			      struct i2c_msg *msgs, uint8_t num_msgs,
			      uint16_t addr,
			      i2c_callback_t cb, void *userdata)
{
	int ret = 0;

	/* Create work item for tracking this transfer */
	transfer_work_t *transfer_work = k_calloc(1, sizeof(transfer_work_t));

	if (transfer_work == NULL) {
		return -ENOMEM;
	}

	*transfer_work = (transfer_work_t) {
		.dev = dev,
		.owns_lock = false,
		.msg_index = 0,
		.msgs = msgs,
		.num_msgs = num_msgs,
		.addr = addr,
		.cb = cb,
		.userdata = userdata,
	};
	k_work_init(&transfer_work->work_init_msg,
		    i2c_sc18is604_init_msg_work_fn);
	k_work_init(&transfer_work->work_buffer_readout,
		    i2c_sc18is604_buffer_readout_work_fn);
	k_work_init(&transfer_work->work_finish_msg,
		    i2c_sc18is604_finish_msg_work_fn);
	k_poll_signal_init(&transfer_work->signal);

	ret = k_work_submit(&transfer_work->work_init_msg);
	if (ret != 1 && ret != 0) {
		return -EAGAIN;
	}

	return 0;
}
