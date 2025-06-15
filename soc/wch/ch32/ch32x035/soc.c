#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include "soc.h"

static void clock_init(void) {
    // set to 48MHz clock
    FLASH->ACTLR = (FLASH->ACTLR & ~FLASH_ACTLR_LATENCY) | FLASH_ACTLR_LATENCY_2;
    RCC->CFGR0   = (RCC->CFGR0 & ~RCC_HPRE) | RCC_HPRE_DIV1;

    RCC_AHBPeriphClockCmd (RCC_AHBPeriph_DMA1,  ENABLE); // enable DMA
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE); // enable pin remap and EXTI
}

static int wch_ch32x035_init(void) {
    clock_init();
    return 0;
}

SYS_INIT(wch_ch32x035_init, PRE_KERNEL_1, 0);
