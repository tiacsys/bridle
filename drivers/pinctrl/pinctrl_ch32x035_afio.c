/*
 * Copyright (c) 2025 TiaC Systems
 * Copyright (c) 2024 Michael Hope
 * SPDX-License-Identifier: Apache-2.0
 */

#define DT_DRV_COMPAT wch_ch32x035_afio

#include <zephyr/dt-bindings/pinctrl/ch32x035-pinctrl.h>
#include <zephyr/drivers/clock_control.h>
#include <zephyr/drivers/pinctrl.h>
#include <soc.h>

static GPIO_TypeDef *const wch_ch32x035_afio_pinctrl_regs[] = {
	[CH32X035_PINMUX_PORT_PA] = (GPIO_TypeDef *)DT_REG_ADDR(DT_NODELABEL(gpioa)),
	[CH32X035_PINMUX_PORT_PB] = (GPIO_TypeDef *)DT_REG_ADDR(DT_NODELABEL(gpiob)),
	[CH32X035_PINMUX_PORT_PC] = (GPIO_TypeDef *)DT_REG_ADDR(DT_NODELABEL(gpioc)),
};

int pinctrl_configure_pins(const pinctrl_soc_pin_t *pins, uint8_t pin_cnt, uintptr_t reg)
{
	int i;

	for (i = 0; i < pin_cnt; i++, pins++) {
		uint8_t port = FIELD_GET(CH32X035_PINCTRL_PORT_MASK, pins->config);
		uint8_t pin = FIELD_GET(CH32X035_PINCTRL_PIN_MASK, pins->config);
		uint8_t bit0 = FIELD_GET(CH32X035_PINCTRL_RM_BASE_MASK, pins->config);
		uint8_t remap = FIELD_GET(CH32X035_PINCTRL_RM_MASK, pins->config);
		GPIO_TypeDef *regs = wch_ch32x035_afio_pinctrl_regs[port];
		uint8_t cnf_mode = 0;

		if (pins->output_high || pins->output_low) {
			cnf_mode |= (pins->slew_rate + 1);
			cnf_mode |= BIT(3);	/* Select the alternate function */
		} else {
			if (pins->bias_pull_up || pins->bias_pull_down) {
				cnf_mode |= BIT(3);
			}
		}


		if (pin < 8) {
			regs->CFGLR = (regs->CFGLR & ~(0x0F << (4 * pin))) |
				      (cnf_mode << (4 * pin));
		} else if (pin < 16) {
			regs->CFGHR = (regs->CFGHR & ~(0x0F << (4 * (pin - 8)))) |
				      (cnf_mode << (4 * (pin - 8)));
		} else {
			regs->CFGXR = (regs->CFGXR & ~(0x0F << (4 * (pin - 16)))) |
				      (cnf_mode << (4 * (pin - 16)));
		}

		if (pins->output_high) {
			/*
			 * TODO: OUTDR isn't a kind of a OUTput Direction Register! It is
			 *       the so named OUTput Data Register and doesn't change the
			 *       the direction - check OUTDR vs. BSHR/BSXR.
			 */
			regs->OUTDR |= BIT(pin);
			if (pin < 16) { /* Set the pin. */
				regs->BSHR |= BIT(pin);
			} else {
				regs->BSXR |= BIT(pin);
			}
		} else if (pins->output_low) {
			/*
			 * TODO: OUTDR isn't a kind of a OUTput Direction Register! It is
			 *       the so named OUTput Data Register and doesn't change the
			 *       the direction - check OUTDR vs. BSHR/BSXR.
			 */
			regs->OUTDR |= BIT(pin);
			if (pin < 16) { /* Reset the pin. */
				regs->BSHR |= BIT(pin + 16);
			} else {
				regs->BSXR |= BIT(pin + 16);
			}
		} else {
			/*
			 * TODO: OUTDR isn't a kind of a OUTput Direction Register! It is
			 *       the so named OUTput Data Register and doesn't change the
			 *       the direction - check OUTDR vs. BSHR/BSXR.
			 */
			regs->OUTDR &= ~BIT(pin);
			if (pins->bias_pull_up) {
				regs->BSHR = BIT(pin);
				if (pin < 16) {
					regs->BSHR |= BIT(pin);
				} else {
					regs->BSXR |= BIT(pin);
				}
			}
			if (pins->bias_pull_down) {
				regs->BCR = BIT(pin);
			}
		}

		if (remap != 0) {
			RCC->APB2PCENR |= RCC_AFIOEN;
			AFIO->PCFR1 |= (uint32_t)remap << bit0;
		}
	}

	return 0;
}

static int pinctrl_clock_init(void)
{
	const struct device *clock_dev = DEVICE_DT_GET(DT_INST_CLOCKS_CTLR(0));
	uint8_t clock_id = DT_INST_CLOCKS_CELL(0, id);

	return clock_control_on(clock_dev, (clock_control_subsys_t *)(uintptr_t)clock_id);
}

SYS_INIT(pinctrl_clock_init, PRE_KERNEL_1, 0);
