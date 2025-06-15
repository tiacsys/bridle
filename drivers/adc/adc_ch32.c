/*
 * Copyright (c) 2024 Matthew Tran
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT wch_ch32_adc

#include <errno.h>
#include <zephyr/device.h>
#include <zephyr/drivers/adc.h>
#include <zephyr/irq.h>
#include <zephyrboards/dt-bindings/adc/ch32x035-adc.h>
#include <soc.h>

#define ADC_CHANNEL_NUM  (16)
#define RULE_CHANNEL_NUM (16)

struct adc_ch32_config {
    ADC_TypeDef *base;
    uint32_t clock_type, clock_mask;
    uint32_t prescaler;
    DMA_Channel_TypeDef *dma;
    uint32_t dma_tc;
    void (*irq_config_func)(void);
};

struct adc_ch32_data {
    // state
    volatile bool done;
    int ret;
    bool scanning;
    uint16_t sample_idx;
    struct k_timer timer;
    uint16_t buffer[RULE_CHANNEL_NUM];
    struct {
        uint16_t *dst;
    } rules[RULE_CHANNEL_NUM];

    // options
    const struct device *dev;
    uint8_t num_chan, num_rule;
    uint16_t sample_total;
    uint32_t interval_us;
    struct k_poll_signal *async;
    const struct adc_sequence *sequence;
    ADC_InitTypeDef adc_cfg;
    DMA_InitTypeDef dma_cfg;
    struct {
        uint16_t num_conv;
        uint8_t sample_time;
    } channels[ADC_CHANNEL_NUM];
};

static int adc_ch32_channel_setup(const struct device *dev,
        const struct adc_channel_cfg *channel_cfg) {
    if ((channel_cfg->gain != ADC_GAIN_1) ||
        (channel_cfg->reference != ADC_REF_VDD_1 && channel_cfg->reference != ADC_REF_INTERNAL) ||
        (channel_cfg->channel_id >= ADC_CHANNEL_NUM) ||
        (channel_cfg->differential)) {
        return -EINVAL;
    }

    struct adc_ch32_data *data = dev->data;
    switch (channel_cfg->acquisition_time) {
        case ADC_ACQ_TIME_DEFAULT: // min time
            data->channels[channel_cfg->channel_id].num_conv    = 1;
            data->channels[channel_cfg->channel_id].sample_time = ADC_SAMPLE_TIME_4;
            break;

        case ADC_ACQ_TIME_MAX:
            data->channels[channel_cfg->channel_id].num_conv    = RULE_CHANNEL_NUM;
            data->channels[channel_cfg->channel_id].sample_time = ADC_SAMPLE_TIME_11;
            break;

        default:
            data->channels[channel_cfg->channel_id].num_conv    = ADC_ACQ_TIME_NUM_CONV(channel_cfg->acquisition_time);
            data->channels[channel_cfg->channel_id].sample_time = ADC_ACQ_TIME_SAMPLE_TIME(channel_cfg->acquisition_time);
            break;
    }
    return 0;
}

static int adc_ch32_read_async(const struct device *dev, const struct adc_sequence *sequence,
        struct k_poll_signal *async) {
    const struct adc_ch32_config *config = dev->config;
    struct adc_ch32_data *data = dev->data;        

    if (!data->done) {
        return -EAGAIN;
    }

    if ((sequence->channels & ~BIT_MASK(ADC_CHANNEL_NUM)) ||
        (sequence->channels == 0) ||
        (sequence->resolution != 12) ||
        (sequence->oversampling != 0)) {
        return -EINVAL;
    }

    uint16_t *buffer = (uint16_t*) sequence->buffer;
    data->num_chan = 0;
    data->num_rule = 0;
    for (uint8_t c = 0; c < ADC_CHANNEL_NUM; c++) {
        if (sequence->channels & BIT(c)) {
            uint8_t r = data->num_rule;
            data->num_rule += data->channels[c].num_conv;
            if (data->num_rule > RULE_CHANNEL_NUM) {
                return -ENOTSUP;
            }
            while (r < data->num_rule) { // use multiple rule channels to extend a single sample
                data->rules[r].dst = &buffer[data->num_chan];
                ADC_RegularChannelConfig(config->base, c, r + 1, data->channels[c].sample_time);
                r++;
            }
            data->num_chan++;
        }
    }

    data->interval_us = 0;
    data->sample_total = 1;
    data->sample_idx = 0;
    data->sequence = sequence;
    if (sequence->options) {
        data->interval_us = sequence->options->interval_us;
        data->sample_total += sequence->options->extra_samplings;
    }
    if ((data->num_chan * data->sample_total * sizeof(uint16_t)) > sequence->buffer_size) {
        return -ENOMEM;
    }

    data->adc_cfg.ADC_NbrOfChannel = data->num_rule;
    data->dma_cfg.DMA_BufferSize = data->num_rule;
    ADC_Init(config->base, &data->adc_cfg);
    DMA_Init(config->dma, &data->dma_cfg);
    DMA_Cmd(config->dma, ENABLE);

    data->ret = 0;
    data->done = false;
    data->scanning = true;
    data->async = async;
    ADC_SoftwareStartConvCmd(config->base, ENABLE);

    if (data->interval_us != 0) {
        k_timer_start(&data->timer, K_USEC(data->interval_us), K_USEC(data->interval_us));
    }

    return 0;
}

static int adc_ch32_read(const struct device *dev, const struct adc_sequence *sequence) {
    struct adc_ch32_data *data = dev->data;   
    int ret = adc_ch32_read_async(dev, sequence, NULL);
    if (ret == 0) {
        while (!data->done);
        return data->ret;
    }
    return ret;
}

static void adc_ch32_finish(const struct device *dev) {
    struct adc_ch32_data *data = dev->data;
#ifdef CONFIG_POLL
    if (data->async) {
        k_poll_signal_raise(data->async, data->ret);
    }
#endif
    data->done = true;
    k_timer_stop(&data->timer);
}

static void adc_ch32_repeat_scan(const struct device *dev) {
    const struct adc_ch32_config *config = dev->config;
    struct adc_ch32_data *data = dev->data;
    data->scanning = true;
    DMA_Init(config->dma, &data->dma_cfg);
    DMA_Cmd(config->dma, ENABLE);
    ADC_SoftwareStartConvCmd(config->base, ENABLE);
}

static void adc_ch32_timer_callback(struct k_timer *timer) {
    struct adc_ch32_data *data = CONTAINER_OF(timer, struct adc_ch32_data, timer);
    if (data->scanning) {
        data->ret = -EBUSY;
        data->interval_us = 0;
        k_timer_stop(timer);
    } else {
        adc_ch32_repeat_scan(data->dev);
    }
}

static void adc_ch32_isr(const struct device *dev) {
    const struct adc_ch32_config *config = dev->config;
    struct adc_ch32_data *data = dev->data;
    /*
     * NOTE: implementation assumes timer and ADC ISR can't preempt each other
     */

    // process incoming data
    DMA_ClearITPendingBit(config->dma_tc);
    for (int i = 0; i < data->num_rule; i++) {
        *data->rules[i].dst = data->buffer[i];
    }
    data->scanning = false;

    // do next action
    enum adc_action action = ADC_ACTION_CONTINUE;
    if (data->sequence->options && data->sequence->options->callback) {
        action = data->sequence->options->callback(dev, data->sequence, data->sample_idx);
    }
    switch (action) {
        case ADC_ACTION_CONTINUE:
            data->sample_idx++;
            if (data->sample_idx >= data->sample_total) {
                adc_ch32_finish(dev);
                break;
            }
            for (int i = 0; i < data->num_rule; i++) {
                data->rules[i].dst += data->num_chan;
            }
            if (data->interval_us == 0) {
                adc_ch32_repeat_scan(dev);
            }
            break;

        case ADC_ACTION_REPEAT:
            if (data->interval_us == 0) {
                adc_ch32_repeat_scan(dev);
            }
            break;

        case ADC_ACTION_FINISH:
        default:
            adc_ch32_finish(dev);
            break;
    }
}

static int adc_ch32_init(const struct device *dev) {
    const struct adc_ch32_config *config = dev->config;
    struct adc_ch32_data *data = dev->data;

    config->irq_config_func();

    clock_control_on(config->clock_type, config->clock_mask);
    ADC_DeInit(config->base);
    ADC_Cmd(config->base, ENABLE); // turn on
    ADC_DMACmd(config->base, ENABLE);
    ADC_CLKConfig(config->base, config->prescaler);

    DMA_DeInit(config->dma);
    DMA_ITConfig(config->dma, DMA_IT_TC, ENABLE);

    data->done = true;
    data->adc_cfg = (ADC_InitTypeDef) {
        .ADC_Mode               = ADC_Mode_Independent,
        .ADC_ScanConvMode       = ENABLE,
        .ADC_ContinuousConvMode = DISABLE,
        .ADC_ExternalTrigConv   = ADC_ExternalTrigConv_None,
        .ADC_DataAlign          = ADC_DataAlign_Right,
        .ADC_NbrOfChannel       = 0, // set later
        .ADC_OutputBuffer       = 0, // unused
        .ADC_Pga                = 0, // unused
    };
    data->dma_cfg = (DMA_InitTypeDef) {
        .DMA_PeripheralBaseAddr = (uint32_t) &config->base->RDATAR,
        .DMA_MemoryBaseAddr     = (uint32_t) &data->buffer,
        .DMA_DIR                = DMA_DIR_PeripheralSRC,
        .DMA_BufferSize         = 0, // set later
        .DMA_PeripheralInc      = DMA_PeripheralInc_Disable,
        .DMA_MemoryInc          = DMA_MemoryInc_Enable,
        .DMA_PeripheralDataSize = DMA_PeripheralDataSize_HalfWord,
        .DMA_MemoryDataSize     = DMA_MemoryDataSize_HalfWord,
        .DMA_Mode               = DMA_Mode_Normal,
        .DMA_Priority           = DMA_Priority_VeryHigh,
        .DMA_M2M                = DMA_M2M_Disable,
    };

    data->dev = dev;
    k_timer_init(&data->timer, adc_ch32_timer_callback, NULL);

    return 0;
}

static const struct adc_driver_api adc_ch32_driver_api = {
    .channel_setup = adc_ch32_channel_setup,
    .read          = adc_ch32_read,
#ifdef CONFIG_ADC_ASYNC
    .read_async    = adc_ch32_read_async,
#endif
    .ref_internal  = DT_INST_PROP(0, vref_mv),
};

#define ADC_CH32_INIT(n)                                                          \
    static void adc_ch32_##n##_irq_config(void) {                                 \
        IRQ_CONNECT(DT_INST_PROP_BY_IDX(n, irq, 0), 0,                            \
            adc_ch32_isr, DEVICE_DT_INST_GET(n), 0);                              \
        irq_enable(DT_INST_PROP_BY_IDX(n, irq, 0));                               \
    }                                                                             \
                                                                                  \
    static const struct adc_ch32_config adc_ch32_##n##_config = {                 \
        .base            = (ADC_TypeDef*) DT_INST_REG_ADDR(n),                    \
        .clock_type      = DT_INST_PROP_BY_IDX(n, clk, 0),                        \
        .clock_mask      = DT_INST_PROP_BY_IDX(n, clk, 1),                        \
        .prescaler       = DT_INST_PROP(n, prescaler),                            \
        .dma             = (DMA_Channel_TypeDef*) DT_INST_PROP_BY_IDX(n, dma, 0), \
        .dma_tc          = DT_INST_PROP_BY_IDX(n, dma, 1),                        \
        .irq_config_func = adc_ch32_##n##_irq_config,                             \
    };                                                                            \
                                                                                  \
    static struct adc_ch32_data adc_ch32_##n##_data;                              \
                                                                                  \
    DEVICE_DT_INST_DEFINE(n,                                                      \
        &adc_ch32_init,                                                           \
        NULL,                                                                     \
        &adc_ch32_##n##_data,                                                     \
        &adc_ch32_##n##_config,                                                   \
        PRE_KERNEL_1,                                                             \
        CONFIG_ADC_CH32_INIT_PRIORITY,                                            \
        &adc_ch32_driver_api                                                      \
    );

DT_INST_FOREACH_STATUS_OKAY(ADC_CH32_INIT)
