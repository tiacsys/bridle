/*
 * Copyright (c) 2024 TiaC Systems
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT nxp_sc16is75x_uart

#include <bridle/drivers/mfd/sc16is75x.h>

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/uart.h>
#include <zephyr/drivers/gpio.h>

#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(sc16is75x_uart, CONFIG_UART_LOG_LEVEL);

struct sc16is75x_uart_data {
    struct uart_config uart_config;
#ifdef CONFIG_UART_INTERRUPT_DRIVEN
    const struct device *self;
    struct gpio_callback interrupt_callback;
    struct k_work interrupt_work;
    uart_irq_callback_user_data_t uart_irq_callback;
    void *irq_user_data;
#endif // CONFIG_UART_INTERRUPT_DRIVEN
};

struct sc16is75x_uart_config {
    const struct device *bus;
    uint8_t channel;
    uint32_t clock_frequency;
    struct gpio_dt_spec interrupt;
};

static int sc16is75x_uart_read_register(const struct device *dev, uint8_t reg, uint8_t *value)
{
    const struct sc16is75x_uart_config *const config = dev->config;
    return sc16is75x_read_register(config->bus, config->channel, reg, value);
}

static int sc16is75x_uart_write_register(const struct device *dev, uint8_t reg, uint8_t value)
{
    const struct sc16is75x_uart_config *const config = dev->config;
    return sc16is75x_write_register(config->bus, config->channel, reg, value);
}

static int sc16is75x_uart_set_register_bit(const struct device *dev, uint8_t reg, uint8_t bit, bool value)
{
    int ret = 0;

    /* Read out current value */
    uint8_t reg_val = 0;
    ret = sc16is75x_uart_read_register(dev, reg, &reg_val);
    if (ret != 0) {
        return ret;
    }

    /* Set selected bit */
    WRITE_BIT(reg_val, bit, value);

    /* Write back modified value */
    ret = sc16is75x_uart_write_register(dev, reg, reg_val);
    if (ret != 0) {
        return ret;
    }

    return 0;
}

static void sc16is75x_uart_interrupt_work_fn(struct k_work *work)
{
    struct sc16is75x_uart_data *data = CONTAINER_OF(work, struct sc16is75x_uart_data, interrupt_work);
    const struct device *dev = data->self;

    /* Call registered UART IRQ callback, if there is one */
    if (data->uart_irq_callback) {
        data->uart_irq_callback(dev, data->irq_user_data);
    }
}

static void sc16is75x_uart_interrupt_callback(const struct device *dev, struct gpio_callback *cb, gpio_port_pins_t pins)
{
    /* Handling interrupts requires bus operations, which we can't do from an
       ISR. Schedule a work item to do it instead. */
    struct sc16is75x_uart_data *data = CONTAINER_OF(cb, struct sc16is75x_uart_data, interrupt_callback);
    k_work_submit(&data->interrupt_work);
}

static bool sc16is75x_uart_rx_available(const struct device *dev)
{
    int ret = 0;

    /* Line Status Register */
    uint8_t lsr = 0;
    ret = sc16is75x_uart_read_register(dev, SC16IS75X_REG_LSR, &lsr);
    if (ret != 0) {
        return false;
    }

    return (lsr & 0b1);
}

static int sc16is75x_uart_set_loopback(const struct device *dev, bool enable)
{
    /* Internal loopback is enabled by setting MCR[4] to 1 */
    return sc16is75x_uart_set_register_bit(dev, SC16IS75X_REG_MCR, 4, enable);
}

static int sc16is75x_uart_enable_fifo(const struct device *dev, bool enable)
{
    /* FIFO is enabled by setting FCR[0] to 1 */
    return sc16is75x_uart_set_register_bit(dev, SC16IS75X_REG_FCR, 0, enable);
}

static int sc16is75x_uart_reset_fifos(const struct device *dev)
{
    /* FIFO reset is controlled by FCR[1] (RX) and FCR[2] (TX) */
    uint8_t fcr = (BIT(1) | BIT(2));
    return sc16is75x_uart_write_register(dev, SC16IS75X_REG_FCR, fcr);    
}

static int sc16is75x_uart_poll_in(const struct device *dev, unsigned char *p_char)
{
    if (!sc16is75x_uart_rx_available(dev)) {
        return -1;
    }

    return sc16is75x_uart_read_register(dev, SC16IS75X_REG_RHR, p_char);
}

static void sc16is75x_uart_poll_out(const struct device *dev, unsigned char out_char)
{
    sc16is75x_uart_write_register(dev, SC16IS75X_REG_THR, out_char);
}

static int sc16is75x_uart_err_check(const struct device *dev)
{
    int ret = 0;

    /* Check Line Status Register for errors in the FIFO. */
    uint8_t lsr = 0;
    ret = sc16is75x_uart_read_register(dev, SC16IS75X_REG_LSR, &lsr);
    if (ret != 0) {
        return ret;
    }

    /* LSR[7] is 1 if there is at least one error present. */
    if (!(lsr & BIT(7))) {
        return 0;
    }

    /* Assemble error flags */
    int errors = 0;

    // LSR[1] ^= Overrun error
    if (lsr & BIT(1)) {
        errors |= UART_ERROR_OVERRUN;
    }

    // LSR[2] ^= Parity error
    if (lsr & BIT(2)) {
        errors |= UART_ERROR_PARITY;
    }

    // LSR[3] ^= Framing error
    if (lsr & BIT(3)) {
        errors |= UART_ERROR_FRAMING;
    }

    // LSR[4] ^= Break interrupt
    if (lsr & BIT(4)) {
        errors |= UART_BREAK;
    }

    return errors;
}

static int sc16is75x_uart_set_baudrate(const struct device *dev, uint32_t baudrate)
{
    const struct sc16is75x_uart_config *const config = dev->config;
    struct sc16is75x_uart_data *data = dev->data;
    int ret = 0;

    /* Set LCR[7] to 1 to enable access to DLL and DLH registers */
    ret = sc16is75x_uart_set_register_bit(dev, SC16IS75X_REG_LCR, 7, 1);
    if (ret != 0) {
        return ret;
    }

    /* Compute divisor value  */
    uint16_t divisor = config->clock_frequency / (baudrate * 16);
    uint8_t divisor_lsb = divisor;
    uint8_t divisor_msb = divisor >> 8;

    /* Write values to device. */
    ret = sc16is75x_uart_write_register(dev, SC16IS75X_REG_DLL, divisor_lsb);
    if (ret != 0) {
        return ret;
    }
    ret = sc16is75x_uart_write_register(dev, SC16IS75X_REG_DLH, divisor_msb);
    if (ret != 0) {
        return ret;
    }

    /* Update cached setting */
    data->uart_config.baudrate = baudrate;

    /* Unset LCR[7] to access normal registers again */
    ret = sc16is75x_uart_set_register_bit(dev, SC16IS75X_REG_LCR, 7, 0);
    if (ret != 0) {
        return ret;
    }

    return 0;
}

static int sc16is75x_uart_set_hw_flow_ctrl(const struct device *dev, bool enable)
{
    int ret = 0;

    /* To access enhanced register set, LCR must be set to 0xbf. Save current
      value to restore later. */
    uint8_t lcr = 0;
    ret = sc16is75x_uart_read_register(dev, SC16IS75X_REG_LCR, &lcr);
    if (ret != 0) {
        return ret;
    }
    ret = sc16is75x_uart_write_register(dev, SC16IS75X_REG_LCR, 0xbf);
    if (ret != 0) {
        return ret;
    }

    /* Get value of EFR register */
    uint8_t efr = 0;
    ret = sc16is75x_uart_read_register(dev, SC16IS75X_REG_EFR, &efr);
    if (ret != 0) {
        return ret;
    }

    /* Set Auto-RTS and Auto-CTS */
    WRITE_BIT(efr, 6, enable); // Auto-RTS
    WRITE_BIT(efr, 7, enable); // Auto-CTS

    /* Write back modified value */
    ret = sc16is75x_uart_write_register(dev, SC16IS75X_REG_EFR, efr);
    if (ret != 0) {
        return ret;
    }

    /* Restore LCR to previous value */
    ret = sc16is75x_uart_write_register(dev, SC16IS75X_REG_LCR, lcr);
    if (ret != 0) {
        return ret;
    }

    return 0;
}

static int sc16is75x_uart_set_rs485_flow_ctrl(const struct device *dev, bool enable)
{
    /* EFCR[0] controls RS-485 mode */
    return sc16is75x_uart_set_register_bit(dev, SC16IS75X_REG_EFCR, 0, enable);
}

static int sc16is75x_uart_use_modem_pins(const struct device *dev, bool enable)
{
    const struct sc16is75x_uart_config *const config = dev->config;

    /* IOControl[1] enables extra modem pins for channel 0 (A), IOControl[2] for
       channel 1 (B) */
    uint8_t bit = 0;
    if (config->channel == 0) {
        bit = 1;
    } else if (config->channel == 1) {
        bit = 2;
    } else {
        return -EINVAL;
    }
    
    return sc16is75x_uart_set_register_bit(dev, SC16IS75X_REG_IOCONTROL, bit, enable);
}

static int sc16is75x_uart_configure(const struct device *dev, const struct uart_config *cfg)
{
    struct sc16is75x_uart_data *data = dev->data;
    int ret = 0;

    /* Set parity, stop bits and data bits */

    uint8_t lcr = 0;
    ret = sc16is75x_uart_read_register(dev, SC16IS75X_REG_LCR, &lcr);
    if (ret != 0) {
        return ret;
    }

    // Parity
    uint8_t parity = 0;
    switch (cfg->parity) {
        case UART_CFG_PARITY_NONE:
            parity = SC16IS75X_PARITY_NONE;
            break;
        case UART_CFG_PARITY_ODD:
            parity = SC16IS75X_PARITY_ODD;
            break;
        case UART_CFG_PARITY_EVEN:
            parity = SC16IS75X_PARITY_EVEN;
            break;
        case UART_CFG_PARITY_MARK:
            parity = SC16IS75X_PARITY_MARK;
            break;
        case UART_CFG_PARITY_SPACE:
            parity = SC16IS75X_PARITY_SPACE;
            break;
        default:
            return -EINVAL;
    }

    // Stop bits
    uint8_t stop_bits = 0;
    if (cfg->stop_bits == UART_CFG_STOP_BITS_1) {
        stop_bits = 0;
    } else if ((cfg->stop_bits == UART_CFG_STOP_BITS_1_5) && (cfg->data_bits == UART_CFG_DATA_BITS_5)) {
        stop_bits = 1;
    } else if ((cfg->stop_bits == UART_CFG_STOP_BITS_2)
        && ((cfg->data_bits == UART_CFG_DATA_BITS_6)
            || (cfg->data_bits == UART_CFG_DATA_BITS_7)
            || (cfg->data_bits == UART_CFG_DATA_BITS_8))) {
        stop_bits = 1;
    } else {
        return -ENOTSUP;
    }

    // Data bits
    uint8_t data_bits = 0;
    switch (cfg->data_bits)
    {
    case UART_CFG_DATA_BITS_5:
        data_bits = SC16IS75X_WORD_LEN_5;
        break;
    case UART_CFG_DATA_BITS_6:
        data_bits = SC16IS75X_WORD_LEN_6;
        break;
    case UART_CFG_DATA_BITS_7:
        data_bits = SC16IS75X_WORD_LEN_7;
        break;
    case UART_CFG_DATA_BITS_8:
        data_bits = SC16IS75X_WORD_LEN_8;
        break;
    default:
        return -EINVAL;
    }

    // Clear relevant register values (lowest 5 bits)
    lcr &= 0b11000000;

    // Insert new values
    lcr |= (parity << 3) | (stop_bits << 2) | (data_bits);

    // Write back updated register value
    ret = sc16is75x_uart_write_register(dev, SC16IS75X_REG_LCR, lcr);
    if (ret != 0) {
        return ret;
    }

    data->uart_config.parity = cfg->parity;
    data->uart_config.stop_bits = cfg->stop_bits;
    data->uart_config.data_bits = cfg->data_bits;

    /* Set baud rate */
    ret = sc16is75x_uart_set_baudrate(dev, cfg->baudrate);
    if (ret != 0) {
        return ret;
    }

    /* Set flow control */
    switch (cfg->flow_ctrl) {
        case UART_CFG_FLOW_CTRL_NONE:
            ret = sc16is75x_uart_set_hw_flow_ctrl(dev, false);
            if (ret != 0) {
               return ret;
            }
            ret = sc16is75x_uart_set_rs485_flow_ctrl(dev, false);
            if (ret != 0) {
                return ret;
            }
            ret = sc16is75x_uart_use_modem_pins(dev, true);
            if (ret != 0) {
                return ret;
            }
            break;

        case UART_CFG_FLOW_CTRL_RTS_CTS:
            ret = sc16is75x_uart_set_rs485_flow_ctrl(dev, false);
            if (ret != 0) {
                return ret;
            }
            ret = sc16is75x_uart_use_modem_pins(dev, false);
            if (ret != 0) {
                return ret;
            }
            ret = sc16is75x_uart_set_hw_flow_ctrl(dev, true);
            if (ret != 0) {
               return ret;
            }
            break;

        case UART_CFG_FLOW_CTRL_DTR_DSR:
            return -ENOTSUP;

        case UART_CFG_FLOW_CTRL_RS485:
            ret = sc16is75x_uart_set_hw_flow_ctrl(dev, false);
            if (ret != 0) {
               return ret;
            }
            ret = sc16is75x_uart_use_modem_pins(dev, false);
            if (ret != 0) {
                return ret;
            }
            ret = sc16is75x_uart_set_rs485_flow_ctrl(dev, true);
            if (ret != 0) {
                return ret;
            }
            break;
        default:
            return -EINVAL;
    }

    return 0;
}

#ifdef CONFIG_UART_USE_RUNTIME_CONFIGURE

static int sc16is75x_uart_config_get(const struct device *dev, struct uart_config *cfg)
{
    struct sc16is75x_uart_data *data = dev->data;
    *cfg = data->uart_config;
    return 0;
}

#endif // CONFIG_UART_USE_RUNTIME_CONFIGURE

#ifdef CONFIG_UART_INTERRUPT_DRIVEN

static int sc16is75x_uart_fifo_fill(const struct device *dev, const uint8_t *tx_data, int size)
{
    const struct sc16is75x_uart_config *const config = dev->config;
    int ret = 0;

    /* Check current FIFO fill level (number of bytes available) */
    uint8_t txlvl = 0;
    ret = sc16is75x_uart_read_register(dev, SC16IS75X_REG_TXLVL, &txlvl);
    if (ret != 0) {
        return ret;
    }

    /* Calculate how many bytes to write */
    uint8_t bytes_free = txlvl;
    
    if (size > bytes_free) {
        size = bytes_free;
    }

    /* Copy data to respect pointer const-ness */
    uint8_t data_mut[SC16IS75X_FIFO_CAPACITY] = {0};
    memcpy(data_mut, tx_data, size);

    /* Write that many bytes to FIFO */
    ret = sc16is75x_write_fifo(config->bus, config->channel, data_mut, size);
    if (ret != 0) {
        return ret;
    }

    return size;
}

static int sc16is75x_uart_fifo_read(const struct device *dev, uint8_t *rx_data, const int size)
{
    const struct sc16is75x_uart_config *const config = dev->config;
    int ret = 0;

    /* Check FIFO fill level */
    uint8_t rxlvl = 0;
    ret = sc16is75x_uart_read_register(dev, SC16IS75X_REG_RXLVL, &rxlvl);
    if (ret != 0) {
        return ret;
    }

    /* Calculate how many bytes we can read */
    int bytes_to_read = rxlvl;
    if (bytes_to_read > size) {
        bytes_to_read = size;
    }

    if (bytes_to_read == 0) {
        return 0;
    }

    /* Read that many bytes from FIFO */
    ret = sc16is75x_read_fifo(config->bus, config->channel, rx_data, bytes_to_read);
    if (ret != 0) {
        return ret;
    }

    return bytes_to_read;
}

static void sc16is75x_uart_irq_tx_set(const struct device *dev, bool enable)
{
    /* IER[1] enables THR interrupt */
    sc16is75x_uart_set_register_bit(dev, SC16IS75X_REG_IER, 1, enable);
}

static void sc16is75x_uart_irq_tx_enable(const struct device *dev)
{
    sc16is75x_uart_irq_tx_set(dev, true);
}

static void sc16is75x_uart_irq_tx_disable(const struct device *dev)
{
    sc16is75x_uart_irq_tx_set(dev, false);
}

static int sc16is75x_uart_irq_tx_ready(const struct device *dev)
{
    int ret = 0;

    /* TXLVL register holds number of bytes free in TX FIFO */
    uint8_t txlvl = 0;
    ret = sc16is75x_uart_read_register(dev, SC16IS75X_REG_TXLVL, &txlvl);
    if (ret != 0) {
        return 0;
    }

    return (txlvl > 0);
}

static int sc16is75x_uart_irq_tx_complete(const struct device *dev)
{
    int ret = 0;

    /* LSR[5] holds THR status (0: not empty, 1: empty) */
    uint8_t lsr = 0;
    ret = sc16is75x_uart_read_register(dev, SC16IS75X_REG_LSR, &lsr);
    if (ret != 0) {
        return 0;
    }
    return (lsr & BIT(5)) == BIT(5);
}

static void sc16is75x_uart_irq_rx_set(const struct device *dev, bool enable)
{
    /* IER[0] enables RHR interrupt */
    sc16is75x_uart_set_register_bit(dev, SC16IS75X_REG_IER, 0, enable);
}

static void sc16is75x_uart_irq_rx_enable(const struct device *dev)
{
    sc16is75x_uart_irq_rx_set(dev, true);
}

static void sc16is75x_uart_irq_rx_disable(const struct device *dev)
{
    sc16is75x_uart_irq_rx_set(dev, false);
}

static int sc16is75x_uart_irq_rx_ready(const struct device *dev)
{
    return sc16is75x_uart_rx_available(dev);
}

static void sc16is75x_uart_irq_err_enable(const struct device *dev)
{
    LOG_INF("Implement sc16is75x_uart_irq_err_enable!");
}

static void sc16is75x_uart_irq_err_disable(const struct device *dev)
{
    LOG_INF("Implement sc16is75x_uart_irq_err_disable!");
}

static int sc16is75x_uart_irq_is_pending(const struct device *dev)
{
    int ret = 0;

    /* Read out IIR */
    uint8_t iir = 0;
    ret = sc16is75x_uart_read_register(dev, SC16IS75X_REG_IIR, &iir);
    if (ret != 0) {
        return 0;
    }

    /* IIR[0] holds interrupt status (0: pending, 1: not pending) */
    return !((iir & BIT(0)) == BIT(0));
}

static int sc16is75x_uart_irq_update(const struct device *dev)
{
    return 1;
}

static void sc16is75x_uart_irq_callback_set(const struct device *dev, uart_irq_callback_user_data_t cb, void *user_data)
{
    struct sc16is75x_uart_data *data = dev->data;

    data->uart_irq_callback = cb;
    data->irq_user_data = user_data;
}

#endif // CONFIG_UART_INTERRUPT_DRIVEN

#ifdef CONFIG_UART_LINE_CTRL

static int sc16is75x_uart_line_ctrl_set(const struct device *dev, uint32_t ctrl, uint32_t val)
{
    int ret = 0;

    if (ctrl == UART_LINE_CTRL_BAUD_RATE) {
        return sc16is75x_uart_set_baudrate(dev, val);
    }

    uint8_t reg = 0;
    uint8_t bit = 0;
    switch (ctrl) {
        case UART_LINE_CTRL_RTS:
            /* RTS is in MCR[1] */
            reg = SC16IS75X_REG_MCR;
            bit = 1;
            break;
        
        case UART_LINE_CTRL_DTR:
            /* DTR in in MCR[0] */
            reg = SC16IS75X_REG_MCR;
            bit = 0;
            break;

        case UART_LINE_CTRL_DCD:
            /* CD is read-only */
            return -EINVAL;

        case UART_LINE_CTRL_DSR:
            /* DSR is read-only */
            return -EINVAL;

        default:
            return -EINVAL;
    }
    
    uint8_t reg_value = 0;
    ret = sc16is75x_uart_read_register(dev, reg, &reg_value);
    if (ret != 0) {
        return ret;
    }

    WRITE_BIT(reg_value, bit, val);
    
    ret = sc16is75x_uart_write_register(dev, reg, reg_value);
    if (ret != 0) {
        return ret;
    }
    
    return 0;
}

static int sc16is75x_uart_line_ctrl_get(const struct device *dev, uint32_t ctrl, uint32_t *val)
{
    struct sc16is75x_uart_data *data = dev->data;
    int ret = 0;

    if (ctrl == UART_LINE_CTRL_BAUD_RATE) {
        *val = data->uart_config.baudrate;
        return 0;
    }

    uint8_t reg = 0;
    uint8_t bit = 0;
    switch (ctrl) {
        case UART_LINE_CTRL_RTS:
            /* RTS is in MCR[1] */
            reg = SC16IS75X_REG_MCR;
            bit = 1;
            break;
        
        case UART_LINE_CTRL_DTR:
            /* DTR in in MCR[0] */
            reg = SC16IS75X_REG_MCR;
            bit = 0;
            break;

        case UART_LINE_CTRL_DCD:
            /* CD is in MSR[7] */
            reg = SC16IS75X_REG_MSR;
            bit = 7;
            break;

        case UART_LINE_CTRL_DSR:
            /* DSR is in MSR[5] */
            reg = SC16IS75X_REG_MSR;
            bit = 5;
            break;

        default:
            return -EINVAL;
    }
    
    uint8_t reg_value = 0;
    ret = sc16is75x_uart_read_register(dev, reg, &reg_value);
    if (ret != 0) {
        return ret;
    }

    *val = ((reg_value & BIT(bit)) == BIT(bit));
    
    return 0;
}

#endif // CONFIG_UART_LINE_CTRL

#ifdef CONFIG_UART_DRV_CMD

static int sc16is75x_uart_drv_cmd(const struct device *dev, uint32_t cmd, uint32_t p) {
    return -ENOTSUP;
}

#endif // CONFIG_UART_DRV_CMD


static const struct uart_driver_api sc16is75x_uart_driver_api = {
#ifdef CONFIG_UART_ASYNC_API
    .callback_set = NULL,
    .tx = NULL,
    .tx_abort = NULL,
    .rx_enable = NULL,
    .rx_buf_rsp = NULL,
    .rx_disable = NULL,
#ifdef CONFIG_UART_WIDE_DATA
    .tx_u16 = NULL,
    .rx_enable_u16 = NULL,
    .rx_buf_rsp_u16 = NULL,
#endif // CONFIG_UART_WIDE_DATA
#endif // CONFIG_UART_ASYNC_API

    .poll_in = sc16is75x_uart_poll_in,
    .poll_out = sc16is75x_uart_poll_out,

#ifdef CONFIG_UART_WIDE_DATA
    .poll_in_u16 = NULL,
    .poll_out_u16 = NULL,
#endif // CONFIG_UART_WIDE_DATA

    .err_check = sc16is75x_uart_err_check,

#ifdef CONFIG_UART_USE_RUNTIME_CONFIGURE
    .configure = sc16is75x_uart_configure,
    .config_get = sc16is75x_uart_config_get,
#endif // CONFIG_UART_USE_RUNTIME_CONFIGURE

#ifdef CONFIG_UART_INTERRUPT_DRIVEN
    .fifo_fill = sc16is75x_uart_fifo_fill,
    .fifo_read = sc16is75x_uart_fifo_read,
#ifdef CONFIG_UART_WIDE_DATA
    .fifo_fill_u16 = NULL,
    .fifo_read_u16 = NULL,
#endif // CONFIG_UART_WIDE_DATA
    .irq_tx_enable = sc16is75x_uart_irq_tx_enable,
    .irq_tx_disable = sc16is75x_uart_irq_tx_disable,
    .irq_tx_ready = sc16is75x_uart_irq_tx_ready,
    .irq_tx_complete = sc16is75x_uart_irq_tx_complete,
    .irq_rx_enable = sc16is75x_uart_irq_rx_enable,
    .irq_rx_disable = sc16is75x_uart_irq_rx_disable,
    .irq_rx_ready = sc16is75x_uart_irq_rx_ready,
    .irq_err_enable = sc16is75x_uart_irq_err_enable,
    .irq_err_disable = sc16is75x_uart_irq_err_disable,
    .irq_is_pending = sc16is75x_uart_irq_is_pending,
    .irq_update = sc16is75x_uart_irq_update,
    .irq_callback_set = sc16is75x_uart_irq_callback_set,
#endif // CONFIG_UART_INTERRUPT_DRIVEN

#ifdef CONFIG_UART_LINE_CTRL
    .line_ctrl_set = sc16is75x_uart_line_ctrl_set,
    .line_ctrl_get = sc16is75x_uart_line_ctrl_get,
#endif // CONFIG_UART_LINE_CTRL

#ifdef CONFIG_UART_DRV_CMD
    .sc16is75x_uart_drv_cmd = sc16is75x_uart_drv_cmd,
#endif // CONFIG_UART_DRV_CMD

};

static int sc16is75x_uart_init(const struct device *dev)
{
    const struct sc16is75x_uart_config *const config = dev->config;
    struct sc16is75x_uart_data *data = dev->data;
    int ret = 0;

    /* Confirm bus readiness */
    if (!sc16is75x_is_ready(config->bus)) {
        LOG_ERR("SC16IS50x bridge device not ready");
        return -ENODEV;
    }

    /* Apply initial config */
    ret = sc16is75x_uart_configure(dev, &data->uart_config);
    if (ret != 0) {
        LOG_ERR("Failed to configure device");
        return ret;
    }

    /* Enable internal FIFO */
    ret = sc16is75x_uart_reset_fifos(dev);
    if (ret != 0) {
        LOG_ERR("Failed to reset FIFO");
        return ret;
    }
    ret = sc16is75x_uart_enable_fifo(dev, true);
    if (ret != 0) {
        LOG_ERR("Failed to enable FIFO");
        return ret;
    }

    /* Set up and register interrupt callback */
    gpio_init_callback(&data->interrupt_callback, sc16is75x_uart_interrupt_callback, BIT(config->interrupt.pin));
    k_work_init(&data->interrupt_work, sc16is75x_uart_interrupt_work_fn);
    data->self = dev;
    ret = gpio_add_callback_dt(&config->interrupt, &data->interrupt_callback);
    if (ret != 0) {
        LOG_ERR("Failed to register interrupt callback: %d", ret);
        return ret;
    }

    /* DEBUG: Enable internal loopback */
    ret = sc16is75x_uart_set_loopback(dev, true);
    if (ret != 0) {
        LOG_ERR("Failed to set internal loopback");
        return ret;
    }

    LOG_INF("Hello world!");
    return 0;
}

#define SC16IS75X_UART_DEFINE(inst) \
    static struct sc16is75x_uart_data sc16is75x_uart_data_##inst = { \
        .uart_config = { \
            .baudrate = DT_INST_PROP_OR(inst, current_speed, 9600), \
            .parity = DT_INST_ENUM_IDX_OR(inst, parity, UART_CFG_PARITY_EVEN), \
            .stop_bits = DT_INST_ENUM_IDX_OR(inst, stop_bits, UART_CFG_STOP_BITS_2), \
            .data_bits = DT_INST_ENUM_IDX_OR(inst, data_bits, UART_CFG_DATA_BITS_6), \
            .flow_ctrl = COND_CODE_1(DT_INST_PROP_OR(inst, hw_flow_control, false), \
                (UART_CFG_FLOW_CTRL_RTS_CTS), \
                (UART_CFG_FLOW_CTRL_NONE)), \
        }, \
    }; \
    static struct sc16is75x_uart_config sc16is75x_uart_config_##inst = { \
        .bus = DEVICE_DT_GET(DT_INST_BUS(inst)), \
        .channel = DT_INST_REG_ADDR(inst), \
        .clock_frequency = DT_PROP_BY_PHANDLE(DT_INST_PARENT(inst), clock, clock_frequency), \
        .interrupt = GPIO_DT_SPEC_GET(DT_INST_BUS(inst), interrupt_gpios), \
    }; \
    DEVICE_DT_INST_DEFINE(inst, \
        sc16is75x_uart_init, \
        NULL, /* PM */ \
        &sc16is75x_uart_data_##inst, \
        &sc16is75x_uart_config_##inst, \
        POST_KERNEL, \
        CONFIG_UART_SC16IS75X_INIT_PRIORITY, \
        &sc16is75x_uart_driver_api /* driver API */ \
    );

DT_INST_FOREACH_STATUS_OKAY(SC16IS75X_UART_DEFINE);
