#ifndef ZEPHYR_INCLUDE_DT_BINDINGS_CLOCK_CH32X035_CLOCK_H_
#define ZEPHYR_INCLUDE_DT_BINDINGS_CLOCK_CH32X035_CLOCK_H_

// derived from <ch32x035_rcc.h>

#define RCC_Type_AHB   (0)
#define RCC_Type_APB2  (1)
#define RCC_Type_APB1  (2)

#define RCC_AHBPeriph_DMA1     (0x00000001)
#define RCC_AHBPeriph_SRAM     (0x00000004)
#define RCC_AHBPeriph_USBFS    (0x00001000)
#define RCC_AHBPeriph_IO2W     (0x00002000)
#define RCC_AHBPeriph_USBPD    (0x00020000)

#define RCC_APB2Periph_AFIO    (0x00000001)
#define RCC_APB2Periph_GPIOA   (0x00000004)
#define RCC_APB2Periph_GPIOB   (0x00000008)
#define RCC_APB2Periph_GPIOC   (0x00000010)
#define RCC_APB2Periph_ADC1    (0x00000200)
#define RCC_APB2Periph_TIM1    (0x00000800)
#define RCC_APB2Periph_SPI1    (0x00001000)
#define RCC_APB2Periph_USART1  (0x00004000)

#define RCC_APB1Periph_TIM2    (0x00000001)
#define RCC_APB1Periph_TIM3    (0x00000002)
#define RCC_APB1Periph_WWDG    (0x00000800)
#define RCC_APB1Periph_USART2  (0x00020000)
#define RCC_APB1Periph_USART3  (0x00040000)
#define RCC_APB1Periph_USART4  (0x00080000)
#define RCC_APB1Periph_I2C1    (0x00200000)
#define RCC_APB1Periph_PWR     (0x10000000)

#endif /* ZEPHYR_INCLUDE_DT_BINDINGS_CLOCK_CH32X035_CLOCK_H_ */
