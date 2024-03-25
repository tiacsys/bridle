/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/devicetree.h>
#include <zephyr/init.h>
#include <zephyr/drivers/uart.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(main, CONFIG_MAIN_LOG_LEVEL);

static const struct device *const uart = DEVICE_DT_GET(DT_ALIAS(test_uart));

#define UART_BUFFER_SIZE 128

struct serial_buffer {
    char buffer[UART_BUFFER_SIZE]; // The buffer itself
    size_t used; // Number of bytes actually used
    size_t position; // Current 'cursor' position in buffer
};

struct serial_buffers {
    struct serial_buffer tx;
    struct serial_buffer rx;
};

static struct serial_buffers serial_buffers;
static K_SEM_DEFINE(serial_tx_buffer_available, 1, 1);

/* Callback handling serial communication. */
static void uart_callback(const struct device *dev, void *user_data)
{

    /* Must be the first thing called in the ISR */
    if (!uart_irq_update(dev)) {
        return;
    }

    /* Check for TX data */
    if (uart_irq_tx_ready(dev)) {

        struct serial_buffer *buf = &serial_buffers.tx;

        /* Try to put as much data into the FIFO as we can */
        int bytes_copied = uart_fifo_fill(dev,
            (uint8_t*)&buf->buffer[buf->position], // Start reading here
            buf->used - buf->position); // This many bytes are left (may be 0)


        /* Advance cursor position in buffer */
        buf->position += bytes_copied; // May be 0

        /* Check if we're done */
        if (buf->position >= buf->used) { // '>=' check just in case
            // Disable interrupt
            uart_irq_tx_disable(dev);
            // Signal that the buffer is available again
            k_sem_give(&serial_tx_buffer_available);
        }
    }

    /* Check for RX data */
    if (uart_irq_rx_ready(dev)) {

        struct serial_buffer *buf = &serial_buffers.rx;

        /* Read out data from FIFO until it's empty, one byte at a time. */
        char c;
        while (uart_fifo_read(dev, &c, 1) == 1) {

            /* Consider null bytes delimiters between messages. Also stop
               reading if the RX buffer is full (the message will then be
               truncated, and remaining pieces read afterward). */
            if ((c == '\0') || (buf->position == (sizeof(buf->buffer) - 1))) {
                
                /* Add terminator */
                buf->buffer[buf->position++] = '\0';

                /* Write full message to logs */
                LOG_INF("Received message: %s", buf->buffer);

                /* Reset buffer position after copying out the message */
                buf->position = 0;
            } else {

                /* Append character to buffer */
                buf->buffer[buf->position++] = c;
            }
        }
    }
}

static int init(void)
{
    /* Set up callback for serial communication */
    uart_irq_callback_user_data_set(uart, uart_callback, NULL);
    uart_irq_rx_enable(uart);

    return 0;
}
SYS_INIT(init, APPLICATION, 90);

int uart_send(char* msg, size_t len) {

    /* Validate input */
    if (msg == NULL) {
        LOG_ERR("Invalid input to uart_send");
        return -EINVAL;
    }

    if (len > UART_BUFFER_SIZE) {
        LOG_WRN("Serial port message is too large for TX buffer. Message will be truncated.");
    }

    /* If another transfer is still in progress, wait until the buffer becomes
       available */
    int ret = k_sem_take(&serial_tx_buffer_available, K_SECONDS(1));
    if (ret != 0) {
        LOG_ERR("TX buffer blocked");
        return -1;
    }

    /* Copy message into buffer and set up length and position */
    strncpy(serial_buffers.tx.buffer, msg, sizeof(serial_buffers.tx.buffer));
    serial_buffers.tx.used = MIN(len, UART_BUFFER_SIZE);
    serial_buffers.tx.position = 0;

    /* Enable TX interrupt */
    uart_irq_tx_enable(uart);

    return 0;
}

int main(int argc, char *argv[])
{
    if (uart == NULL) {
        LOG_ERR("UART under test not ready");
        return 0;
    }

    LOG_INF("Testing UART %s", uart->name);

    LOG_INF("Hello world!");

    return 0;
}
