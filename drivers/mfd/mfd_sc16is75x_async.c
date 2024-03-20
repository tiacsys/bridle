/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/device.h>

#include "mfd_sc16is75x.h"

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(mfd_sc16is75x_async, CONFIG_MFD_LOG_LEVEL);

struct mfd_sc16is75x_transfer_work {
	/** The work item performing the transfer. */
	struct k_work work;
	/** The device on which the transfer is performed. */
	const struct device *dev;
	/** The subaddress being read from. */
	uint8_t sub_address;
	/** Buffer for receiving data from the device. */
	uint8_t *rx_data;
	/** Length of rx_data */
	size_t rx_len;
	/** Signal to be raised once the transfer is complete (or has failed). */
	struct k_poll_signal *signal;
};

/*
 * Work item that performs the actual transfers on the underlying SPI bus.
 * Must be submitted to the work queue owned by the driver instance .
 */
static void mfd_sc16is75x_transfer_work_fn(struct k_work *work)
{
	/* Access bundled data */
	struct mfd_sc16is75x_transfer_work *transfer_work = CONTAINER_OF(work,
		struct mfd_sc16is75x_transfer_work, work);
	const struct device *dev = transfer_work->dev;
	struct mfd_sc16is75x_data * const data = dev->data;
	int ret = 0;

	/* Call blocking transfer */
	ret = data->transfer_function->read_raw(dev,
						transfer_work->sub_address,
						transfer_work->rx_data,
						transfer_work->rx_len);

	/* Report result through signal */
	k_poll_signal_raise(transfer_work->signal, ret);

	/* Clean up this work item */
	k_free(transfer_work);
}


int mfd_sc16is75x_read_raw_signal(const struct device *dev,
					 const uint8_t sub_address,
					 uint8_t *buf, const size_t len,
					 struct k_poll_signal *signal)
{
	struct mfd_sc16is75x_data * const data = dev->data;
	int ret = 0;

	/* Create work item to manage transfers */
	struct mfd_sc16is75x_transfer_work *transfer_work = k_malloc(
		sizeof(struct mfd_sc16is75x_transfer_work));
	if (transfer_work == NULL) {
		return -ENOMEM;
	}

	*transfer_work = (struct mfd_sc16is75x_transfer_work) {
		.dev = dev,
		.sub_address = sub_address,
		.rx_data = buf,
		.rx_len = len,
		.signal = signal,
	};
	k_work_init(&transfer_work->work, mfd_sc16is75x_transfer_work_fn);

	/* Submit work item to driver owned queue */
	ret = k_work_submit_to_queue(&data->work_queue, &transfer_work->work);
	if (ret != 1) {
		k_free(transfer_work);
		return -EAGAIN;
	}

	return 0;
}
