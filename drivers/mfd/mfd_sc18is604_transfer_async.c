/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @file
 * @brief MFD Bus Transfer Driver Callbacks for an SC18IM604 bridge
 */

#include <zephyr/kernel.h>
#include <zephyr/device.h>

#include <zephyr/drivers/mfd/sc18is604.h>

#include "mfd_sc18is604.h"

/**
 * @brief Structure tracking an asynchronous transfer.
 */
struct mfd_sc18is604_transfer_work {
	/** The work item performing the transfer. */
	struct k_work work;
	/** The device on which the transfer is performed. */
	const struct device *dev;
	/** The command sequence to be sent. */
	uint8_t *cmd;
	/** Length of the command sequence. */
	size_t cmd_len;
	/** Data to be sent to the device. */
	uint8_t *tx_data;
	/** Length of tx_data. */
	size_t tx_len;
	/** Buffer for receiving data from the device. */
	uint8_t *rx_data;
	/** Length of rx_data */
	size_t rx_len;
	/** Signal to be raised once the transfer is complete (or has failed). */
	struct k_poll_signal *signal;
};

/*
 * Work item that performs the actual transfers on the underlying SPI bus. Must
 * be submitted to the work queue owned by the driver instance .
 */
static void mfd_sc18is604_transfer_work_fn(struct k_work *work)
{
	/* Access bundled data */
	struct mfd_sc18is604_transfer_work *transfer_work =
		CONTAINER_OF(work, struct mfd_sc18is604_transfer_work, work);
	const struct device *dev = transfer_work->dev;
	int ret = 0;

	/* Call blocking transfer */
	ret = mfd_sc18is604_transfer(dev, transfer_work->cmd, transfer_work->cmd_len,
				     transfer_work->tx_data, transfer_work->tx_len,
				     transfer_work->rx_data, transfer_work->rx_len);

	/* Report result through signal */
	k_poll_signal_raise(transfer_work->signal, ret);

	/* Clean up this work item */
	k_free(transfer_work->cmd);
	k_free(transfer_work);
}

int mfd_sc18is604_transfer_signal(const struct device *dev, uint8_t *cmd, size_t cmd_len,
				  uint8_t *tx_data, size_t tx_len, uint8_t *rx_data, size_t rx_len,
				  struct k_poll_signal *signal)
{
	struct mfd_sc18is604_data *const data = dev->data;
	int ret = 0;

	/* Create work item to manage transfers */
	struct mfd_sc18is604_transfer_work *transfer_work =
		k_malloc(sizeof(struct mfd_sc18is604_transfer_work));
	if (transfer_work == NULL) {
		return -ENOMEM;
	}

	*transfer_work = (struct mfd_sc18is604_transfer_work){
		.dev = dev,
		.cmd_len = cmd_len,
		.tx_data = tx_data,
		.tx_len = tx_len,
		.rx_data = rx_data,
		.rx_len = rx_len,
		.signal = signal,
	};
	k_work_init(&transfer_work->work, mfd_sc18is604_transfer_work_fn);

	/*
	 * We can expect the TX and RX buffer to stay live until
	 * transfer completion, but the command sequence was
	 * stack-allocated inbetween. To make sure it stays valid,
	 * we create an allocated copy attached to the transfer work.
	 */

	transfer_work->cmd = k_malloc(cmd_len);
	if (transfer_work->cmd == NULL) {
		k_free(transfer_work);
		return -ENOMEM;
	}
	memcpy(transfer_work->cmd, cmd, cmd_len);

	/* Submit work item to driver owned queue */
	ret = k_work_submit_to_queue(&data->work_queue, &transfer_work->work);
	if (ret != 1) {
		k_free(transfer_work->cmd);
		k_free(transfer_work);
		return -EAGAIN;
	}

	return 0;
}

int mfd_sc18is604_read_register_signal(const struct device *dev, uint8_t reg, uint8_t *val,
				       struct k_poll_signal *signal)
{
	uint8_t cmd[] = {SC18IS604_CMD_READ_REGISTER, reg};

	return mfd_sc18is604_transfer_signal(dev, cmd, ARRAY_SIZE(cmd), NULL, 0, val, 1, signal);
}

int mfd_sc18is604_read_buffer_signal(const struct device *dev, uint8_t *data, size_t len,
				     struct k_poll_signal *signal)
{
	uint8_t cmd[] = {SC18IS604_CMD_READ_BUFFER};

	return mfd_sc18is604_transfer_signal(dev, cmd, ARRAY_SIZE(cmd), NULL, 0, data, len, signal);
}
