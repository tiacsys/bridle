/*
 * Copyright (c) 2024 Matthew Tran
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT wch_ch32_uart

#include <errno.h>
#include <zephyr/device.h>
#include <zephyr/drivers/uart.h>
#include <zephyr/irq.h>
#include <soc.h>

struct uart_ch32_config {
    USART_TypeDef *base;
    uint32_t clock_type, clock_mask;
    uint32_t pin_tx, pin_rx;
    uint32_t remap;
#ifdef CONFIG_UART_INTERRUPT_DRIVEN
    void (*irq_config_func)(void);
#endif
};

struct uart_ch32_data {
    struct uart_config uart_cfg;
#ifdef CONFIG_UART_INTERRUPT_DRIVEN
    uart_irq_callback_user_data_t cb;
    void *user_data;
#endif
};

static int uart_ch32_poll_in(const struct device *dev, unsigned char *c) {
    const struct uart_ch32_config *config = dev->config;
    if (USART_GetFlagStatus(config->base, USART_FLAG_RXNE) == SET) {
        *c = USART_ReceiveData(config->base);
        return 0;
    }
    return -1;
}

static void uart_ch32_poll_out(const struct device *dev, unsigned char c) {
    const struct uart_ch32_config *config = dev->config;
    while (USART_GetFlagStatus(config->base, USART_FLAG_TC) == RESET);
    USART_SendData(config->base, c);
}

static int uart_ch32_err_check(const struct device *dev) {
    const struct uart_ch32_config *config = dev->config;
    int err = 0;

    if (USART_GetITStatus(config->base, USART_IT_ORE_RX) == SET) {
        USART_ClearITPendingBit(config->base, USART_IT_ORE_RX);
        err |= UART_ERROR_OVERRUN;
    }

    if (USART_GetITStatus(config->base, USART_IT_PE) == SET) {
        USART_ClearITPendingBit(config->base, USART_IT_PE);
        err |= UART_ERROR_PARITY;
    }

    if (USART_GetITStatus(config->base, USART_IT_FE) == SET) {
        USART_ClearITPendingBit(config->base, USART_IT_FE);
        err |= UART_ERROR_FRAMING;
    }

    return err;
}

#ifdef CONFIG_UART_USE_RUNTIME_CONFIGURE

static int uart_ch32_configure(const struct device *dev, const struct uart_config *cfg) {
    const struct uart_ch32_config *config = dev->config;
    struct uart_ch32_data *data = dev->data;

    USART_InitTypeDef usart_cfg = {
        .USART_BaudRate = cfg->baudrate,
        .USART_Mode     = USART_Mode_Tx | USART_Mode_Rx,
    };

    switch (cfg->parity) {
        case UART_CFG_PARITY_NONE: usart_cfg.USART_Parity = USART_Parity_No;   break;
        case UART_CFG_PARITY_EVEN: usart_cfg.USART_Parity = USART_Parity_Even; break;
        case UART_CFG_PARITY_ODD:  usart_cfg.USART_Parity = USART_Parity_Odd;  break;
        default: return -ENOTSUP; break;
    }

    switch (cfg->stop_bits) {
        case UART_CFG_STOP_BITS_0_5: usart_cfg.USART_StopBits = USART_StopBits_0_5; break;
        case UART_CFG_STOP_BITS_1:   usart_cfg.USART_StopBits = USART_StopBits_1;   break;
        case UART_CFG_STOP_BITS_1_5: usart_cfg.USART_StopBits = USART_StopBits_1_5; break;
        case UART_CFG_STOP_BITS_2:   usart_cfg.USART_StopBits = USART_StopBits_2;   break;
        default: return -ENOTSUP; break;
    }

    switch (cfg->data_bits) {
        case UART_CFG_DATA_BITS_8: usart_cfg.USART_WordLength = USART_WordLength_8b; break;
        case UART_CFG_DATA_BITS_9: usart_cfg.USART_WordLength = USART_WordLength_9b; break;
        default: return -ENOTSUP; break;
    }

    switch (cfg->flow_ctrl) {
        case UART_CFG_FLOW_CTRL_NONE:    usart_cfg.USART_HardwareFlowControl = USART_HardwareFlowControl_None;    break;
        case UART_CFG_FLOW_CTRL_RTS_CTS: usart_cfg.USART_HardwareFlowControl = USART_HardwareFlowControl_RTS_CTS; break;
        default: return -ENOTSUP; break;
    }

    USART_Init(config->base, &usart_cfg); // note can silently fail
    USART_Cmd(config->base, ENABLE);

    data->uart_cfg = *cfg;
    return 0;
}

static int uart_ch32_config_get(const struct device *dev, struct uart_config *cfg) {
    struct uart_ch32_data *data = dev->data;
    *cfg = data->uart_cfg;
    return 0;
}

#endif // CONFIG_UART_USE_RUNTIME_CONFIGURE

#ifdef CONFIG_UART_INTERRUPT_DRIVEN

static int uart_ch32_fifo_fill(const struct device *dev, const uint8_t *tx_data, int len) {
    const struct uart_ch32_config *config = dev->config;
    int num_tx = 0;
    while ((len - num_tx > 0) && (USART_GetFlagStatus(config->base, USART_FLAG_TXE) == SET)) {
        USART_SendData(config->base, tx_data[num_tx++]);
    }
    return num_tx;
}

static int uart_ch32_fifo_read(const struct device *dev, uint8_t *rx_data, const int len) {
    const struct uart_ch32_config *config = dev->config;
    int num_rx = 0;
    while ((len - num_rx > 0) && (USART_GetFlagStatus(config->base, USART_FLAG_RXNE) == SET)) {
        rx_data[num_rx++] = USART_ReceiveData(config->base);
    }
    return num_rx;
}

static void uart_ch32_irq_tx_enable(const struct device *dev) {
    const struct uart_ch32_config *config = dev->config;
    USART_ITConfig(config->base, USART_IT_TXE, ENABLE);
}

static void uart_ch32_irq_tx_disable(const struct device *dev) {
    const struct uart_ch32_config *config = dev->config;
    USART_ITConfig(config->base, USART_IT_TXE, DISABLE);
}

static int uart_ch32_irq_tx_ready(const struct device *dev) {
    const struct uart_ch32_config *config = dev->config;
    return USART_GetITStatus(config->base, USART_IT_TXE) == SET;
}

static void uart_ch32_irq_rx_enable(const struct device *dev) {
    const struct uart_ch32_config *config = dev->config;
    USART_ITConfig(config->base, USART_IT_RXNE, ENABLE);
}

static void uart_ch32_irq_rx_disable(const struct device *dev) {
    const struct uart_ch32_config *config = dev->config;
    USART_ITConfig(config->base, USART_IT_RXNE, DISABLE);
}

static int uart_ch32_irq_tx_complete(const struct device *dev) {
    const struct uart_ch32_config *config = dev->config;
    return USART_GetFlagStatus(config->base, USART_FLAG_TC) == SET;
}

static int uart_ch32_irq_rx_ready(const struct device *dev) {
    const struct uart_ch32_config *config = dev->config;
    return USART_GetITStatus(config->base, USART_IT_RXNE) == SET;
}

static void uart_ch32_irq_err_enable(const struct device *dev) {
    const struct uart_ch32_config *config = dev->config;
    USART_ITConfig(config->base, USART_IT_ORE_RX, ENABLE);
    USART_ITConfig(config->base, USART_IT_PE,     ENABLE);
    USART_ITConfig(config->base, USART_IT_FE,     ENABLE);
}

static void uart_ch32_irq_err_disable(const struct device *dev) {
    const struct uart_ch32_config *config = dev->config;
    USART_ITConfig(config->base, USART_IT_ORE_RX, DISABLE);
    USART_ITConfig(config->base, USART_IT_PE,     DISABLE);
    USART_ITConfig(config->base, USART_IT_FE,     DISABLE);
}

static int uart_ch32_irq_is_pending(const struct device *dev) {
    return uart_ch32_irq_tx_ready(dev) || uart_ch32_irq_rx_ready(dev);
}

static int uart_ch32_irq_update(const struct device *dev) {
    return true; // does nothing
}

static void uart_ch32_irq_callback_set(const struct device *dev, uart_irq_callback_user_data_t cb, void *user_data) {
    struct uart_ch32_data *data = dev->data;
    data->cb = cb;
    data->user_data = user_data;
}

static void uart_ch32_isr(const struct device *dev) {
    struct uart_ch32_data *data = dev->data;
    if (data->cb) {
        data->cb(dev, data->user_data);
    }
}

#endif // CONFIG_UART_INTERRUPT_DRIVEN

static int uart_ch32_init(const struct device *dev) {
    const struct uart_ch32_config *config = dev->config;
    struct uart_ch32_data *data = dev->data;
    int err = 0;

    pinctrl_configure_pins(config->pin_tx, GPIO_Mode_AF_PP);
    pinctrl_configure_pins(config->pin_rx, GPIO_Mode_IN_FLOATING);
    pinctrl_apply_state(config->remap);
    clock_control_on(config->clock_type, config->clock_mask);

    err = uart_ch32_configure(dev, &data->uart_cfg);

#ifdef CONFIG_UART_INTERRUPT_DRIVEN
    config->irq_config_func();
#endif

    return err;
}

static const struct uart_driver_api uart_ch32_driver_api = {
    .poll_in          = uart_ch32_poll_in,
    .poll_out         = uart_ch32_poll_out,
    .err_check        = uart_ch32_err_check,
#ifdef CONFIG_UART_USE_RUNTIME_CONFIGURE
    .configure        = uart_ch32_configure,
    .config_get       = uart_ch32_config_get,
#endif
#ifdef CONFIG_UART_INTERRUPT_DRIVEN
    .fifo_fill        = uart_ch32_fifo_fill,
    .fifo_read        = uart_ch32_fifo_read,
    .irq_tx_enable    = uart_ch32_irq_tx_enable,
    .irq_tx_disable   = uart_ch32_irq_tx_disable,
    .irq_tx_ready     = uart_ch32_irq_tx_ready,
    .irq_rx_enable    = uart_ch32_irq_rx_enable,
    .irq_rx_disable   = uart_ch32_irq_rx_disable,
    .irq_tx_complete  = uart_ch32_irq_tx_complete,
    .irq_rx_ready     = uart_ch32_irq_rx_ready,
    .irq_err_enable   = uart_ch32_irq_err_enable,
    .irq_err_disable  = uart_ch32_irq_err_disable,
    .irq_is_pending   = uart_ch32_irq_is_pending,
    .irq_update       = uart_ch32_irq_update,
    .irq_callback_set = uart_ch32_irq_callback_set,
#endif
};

#ifdef CONFIG_UART_INTERRUPT_DRIVEN
#define CH32_UART_IRQ_CONFIG(n)                        \
    static void uart_ch32_##n##_irq_config(void) {     \
        IRQ_CONNECT(DT_INST_PROP_BY_IDX(n, irq, 0), 0, \
            uart_ch32_isr, DEVICE_DT_INST_GET(n), 0);  \
        irq_enable(DT_INST_PROP_BY_IDX(n, irq, 0));                   \
    }
#define CH32_UART_IRQ_INIT(n) .irq_config_func = uart_ch32_##n##_irq_config,
#else
#define CH32_UART_IRQ_CONFIG(n)
#define CH32_UART_IRQ_INIT(n)
#endif // CONFIG_UART_INTERRUPT_DRIVEN

#define CH32_UART_INIT(n)                                             \
    CH32_UART_IRQ_CONFIG(n)                                           \
                                                                      \
    static const struct uart_ch32_config uart_ch32_##n##_config = {   \
        .base       = (USART_TypeDef*) DT_INST_REG_ADDR(n),           \
        .clock_type = DT_INST_PROP_BY_IDX(n, clk, 0),                 \
        .clock_mask = DT_INST_PROP_BY_IDX(n, clk, 1),                 \
        .pin_tx     = DT_INST_PROP_BY_IDX(n, pinctrl, 0),             \
        .pin_rx     = DT_INST_PROP_BY_IDX(n, pinctrl, 1),             \
        .remap      = DT_INST_PROP_BY_IDX(n, remap, 0),               \
        CH32_UART_IRQ_INIT(n)                                         \
    };                                                                \
                                                                      \
    static struct uart_ch32_data uart_ch32_##n##_data = {             \
        .uart_cfg = {                                                 \
            .stop_bits = UART_CFG_STOP_BITS_1,                        \
            .data_bits = UART_CFG_DATA_BITS_8,                        \
            .baudrate  = DT_INST_PROP(n, current_speed),              \
            .parity    = UART_CFG_PARITY_NONE,                        \
            .flow_ctrl = DT_INST_PROP(n, hw_flow_control) ?           \
                UART_CFG_FLOW_CTRL_RTS_CTS : UART_CFG_FLOW_CTRL_NONE, \
        },                                                            \
    };                                                                \
                                                                      \
    DEVICE_DT_INST_DEFINE(n,                                          \
        &uart_ch32_init,                                              \
        NULL,                                                         \
        &uart_ch32_##n##_data,                                        \
        &uart_ch32_##n##_config,                                      \
        PRE_KERNEL_1,                                                 \
        CONFIG_SERIAL_INIT_PRIORITY,                                  \
        &uart_ch32_driver_api                                         \
    );

DT_INST_FOREACH_STATUS_OKAY(CH32_UART_INIT)
