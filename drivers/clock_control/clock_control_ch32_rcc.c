/*
 * Copyright (c) 2025 TiaC Systems
 * Copyright (c) 2024 Michael Hope
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT wch_ch32_rcc

#include <zephyr/drivers/clock_control.h>
#include <zephyr/sys/util.h>
#include <zephyr/arch/cpu.h>
#include <soc.h>

#define CH32_RCC_CLOCK_PCENR_OFFSET(id) (((id) >> 5) & 0xFF)
#define CH32_RCC_CLOCK_PCENR_BIT(id)    ((id) & 0x1F)

struct clock_control_ch32_rcc_config {
	RCC_TypeDef *regs;
	uint16_t ahb_prescaler;
};

static int clock_control_ch32_rcc_on(const struct device *dev,
				     clock_control_subsys_t sub_system)
{
	const struct clock_control_ch32_rcc_config *config = dev->config;
	RCC_TypeDef *regs = config->regs;
	uint8_t id = (uintptr_t)sub_system;
	uint32_t reg;
	uint32_t val;

	ARG_UNUSED(dev);

	if (!IN_RANGE(CH32_RCC_CLOCK_PCENR_OFFSET(id), 0, 2)) {
		/* Attempt to toggle a wrong periph clock bit */
		return -ENOTSUP;
	}

	reg = (uint32_t)(&regs->AHBPCENR + CH32_RCC_CLOCK_PCENR_OFFSET(id));
	val = sys_read32(reg);
	val |= BIT(CH32_RCC_CLOCK_PCENR_BIT(id));
	sys_write32(val, reg);

	return 0;
}

static int clock_control_ch32_rcc_off(const struct device *dev,
				      clock_control_subsys_t sub_system)
{
	const struct clock_control_ch32_rcc_config *config = dev->config;
	RCC_TypeDef *regs = config->regs;
	uint8_t id = (uintptr_t)sub_system;
	uint32_t reg;
	uint32_t val;

	ARG_UNUSED(dev);

	if (!IN_RANGE(CH32_RCC_CLOCK_PCENR_OFFSET(id), 0, 2)) {
		/* Attempt to toggle a wrong periph clock bit */
		return -ENOTSUP;
	}

	reg = (uint32_t)(&regs->AHBPCENR + CH32_RCC_CLOCK_PCENR_OFFSET(id));
	val = sys_read32(reg);
	val &= ~BIT(CH32_RCC_CLOCK_PCENR_BIT(id));
	sys_write32(val, reg);

	return 0;
}

static int clock_control_ch32_rcc_get_rate(const struct device *dev,
					   clock_control_subsys_t sub_system,
					   uint32_t *rate)
{
	const struct clock_control_ch32_rcc_config *config = dev->config;
	RCC_TypeDef *regs = config->regs;
	uint32_t sysclk = CONFIG_SYS_CLOCK_HW_CYCLES_PER_SEC;
	uint32_t ahbclk = sysclk;
	uint32_t reg;
	uint32_t val;

	ARG_UNUSED(dev);

	reg = (uint32_t)(&regs->CFGR0);
	val = sys_read32(reg);

	if ((val & RCC_HPRE_3) != 0) {
		/*
		 * The range 0b1000 divides by a power of 2,
		 * where 0b1000 is /2, 0b1001 is /4, etc.
		 */
		ahbclk /= 2 << ((val & (RCC_HPRE_0 | RCC_HPRE_1 | RCC_HPRE_2)) >> 4);
	} else {
		/*
		 * The range 0b0nnn divides by n + 1,
		 * where 0b0000 is /1, 0b001 is /2, etc.
		 */
		ahbclk /= ((val & (RCC_HPRE_0 | RCC_HPRE_1 | RCC_HPRE_2)) >> 4) + 1;
	}

	/*
	 * The datasheet says that AHB == APB1 == APB2, but the registers imply
	 * that APB1 and APB2 can be divided from the AHB clock. Assume that the
	 * clock tree diagram is correct and always return AHB.
	 */
	*rate = ahbclk;
	return 0;
}

static DEVICE_API(clock_control, clock_control_ch32_rcc_api) = {
	.on = clock_control_ch32_rcc_on,
	.off = clock_control_ch32_rcc_off,
	.get_rate = clock_control_ch32_rcc_get_rate,
};

static int clock_control_ch32_rcc_init(const struct device *dev)
{
	const struct clock_control_ch32_rcc_config *config = dev->config;
	RCC_TypeDef *regs = config->regs;

	if (IS_ENABLED(CONFIG_DT_HAS_WCH_CH32_HSI_CLOCK_ENABLED)) {
		regs->CTLR |= RCC_HSION;
		while ((regs->CTLR & RCC_HSIRDY) == 0) {
		}
	}

	/* TODO: Move to WCH CH32 Flash Controller. This expect SYSCLK=48Mhz */
	FLASH->ACTLR = (FLASH->ACTLR & ~FLASH_ACTLR_LATENCY) | FLASH_ACTLR_LATENCY_2;

	/*
	 * TODO: Adapt to upstream and also support different AHB prescaler
	 * values. For the time beeing set HCLK hard to SYSCLK.
	 */
	regs->CFGR0 = (regs->CFGR0 & ~RCC_HPRE) | RCC_HPRE_DIV1;

// TODO: use clock_control_ch32_rcc_on() with correct clock identifier. */
//	RCC_AHBPeriphClockCmd (RCC_AHBPeriph_DMA1,  ENABLE); // enable DMA

	return 0;
};

/**
 * @brief RCC device, note that priority is intentionally set to 1 so that the
 * device init runs just after SOC init.
 */
#define CLOCK_CONTROL_CH32_RCC_INIT(n)                                                             \
	static const struct clock_control_ch32_rcc_config clock_control_ch32_rcc_##n##_config = {  \
		.regs = (RCC_TypeDef *)DT_INST_REG_ADDR(n),                                        \
		.ahb_prescaler = DT_INST_PROP_OR(n, ahb_prescaler, 3),                             \
	};                                                                                         \
	DEVICE_DT_INST_DEFINE(n, clock_control_ch32_rcc_init, NULL, NULL,                          \
			      &clock_control_ch32_rcc_##n##_config, PRE_KERNEL_1,                  \
			      CONFIG_CLOCK_CONTROL_INIT_PRIORITY, &clock_control_ch32_rcc_api);

/* There is only ever one RCC instance! */
CLOCK_CONTROL_CH32_RCC_INIT(0)
