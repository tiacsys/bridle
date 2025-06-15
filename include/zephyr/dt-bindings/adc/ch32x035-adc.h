#ifndef ZEPHYRBOARDS_INCLUDE_DT_BINDINGS_ADC_CH32X035_ADC_H_
#define ZEPHYRBOARDS_INCLUDE_DT_BINDINGS_ADC_CH32X035_ADC_H_

/*
 * Since 11 cycles may not be enough for higher impedance sources, driver supports using
 * multiple conversions to extend this time. For example, to do 4 conversions w/ an 8 cycle
 * sample time each, use ADC_ACQ_TIME_CH32(4, ADC_SAMPLE_TIME_8).
 */
#define ADC_ACQ_TIME_CH32(num_conv, sample_time) ((((num_conv) & 0xFF) << 4) | ((sample_time) & 0x0F))
#define ADC_ACQ_TIME_NUM_CONV(time)              (((time) >> 4) & 0xFF)
#define ADC_ACQ_TIME_SAMPLE_TIME(time)           ((time) & 0x0F)

// derived from <ch32x035_adc.h> and <ch32x035_dma.h>

#define ADC1_DMA_CHANNEL (0x40020008) // DMA1_Channel1
#define ADC1_DMA_FLAG_TC (0x00000002) // DMA1_IT_TC1

#define ADC_SAMPLE_TIME_4   (0x00)
#define ADC_SAMPLE_TIME_5   (0x01)
#define ADC_SAMPLE_TIME_6   (0x02)
#define ADC_SAMPLE_TIME_7   (0x03)
#define ADC_SAMPLE_TIME_8   (0x04)
#define ADC_SAMPLE_TIME_9   (0x05)
#define ADC_SAMPLE_TIME_10  (0x06)
#define ADC_SAMPLE_TIME_11  (0x07)

#define ADC_CLK_DIV4   (0x00000013)
#define ADC_CLK_DIV5   (0x00000014)
#define ADC_CLK_DIV6   (0x00000025)
#define ADC_CLK_DIV7   (0x00000026)
#define ADC_CLK_DIV8   (0x00000037)
#define ADC_CLK_DIV9   (0x00000038)
#define ADC_CLK_DIV10  (0x00000049)
#define ADC_CLK_DIV11  (0x0000004A)
#define ADC_CLK_DIV12  (0x0000005B)
#define ADC_CLK_DIV13  (0x0000005C)
#define ADC_CLK_DIV14  (0x0000006D)
#define ADC_CLK_DIV15  (0x0000006E)
#define ADC_CLK_DIV16  (0x0000007F)

#endif /* ZEPHYR_INCLUDE_DT_BINDINGS_ADC_CH32X035_ADC_H_ */
