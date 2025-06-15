#ifndef SOC_COMMON_H
#define SOC_COMMON_H

#define SOC_MCAUSE_EXP_MASK        0x7FFFFFFF
#define SOC_MCAUSE_ECALL_EXP       11
#define SOC_MCAUSE_USER_ECALL_EXP  8

#define GPIO_GET_PORT(x)  (((x) >> 8) & 0xFF)
#define GPIO_GET_PIN(x)   ((x) & 0xFF)

#ifndef _ASMLANGUAGE

static inline void clock_control_on(uint32_t type, uint32_t mask) {
    // see dt-bindings/clock/${SOC}_clock.h
    switch (type) {
        case 0: RCC_AHBPeriphClockCmd (mask, ENABLE); break;
        case 1: RCC_APB2PeriphClockCmd(mask, ENABLE); break;
        case 2: RCC_APB1PeriphClockCmd(mask, ENABLE); break;
    }
}

static inline void pinctrl_configure_pins(uint32_t pin, GPIOMode_TypeDef mode) {
    GPIO_InitTypeDef cfg = {
        .GPIO_Pin   = (uint32_t) 1 << GPIO_GET_PIN(pin),
        .GPIO_Speed = GPIO_Speed_50MHz,
        .GPIO_Mode  = mode,
    };
    switch (GPIO_GET_PORT(pin)) {
        case 0: GPIO_Init(GPIOA, &cfg); break;
        case 1: GPIO_Init(GPIOB, &cfg); break;
        case 2: GPIO_Init(GPIOC, &cfg); break;
    }
}

static inline void pinctrl_apply_state(uint32_t remap) {
    if (remap) {
        GPIO_PinRemapConfig(remap, ENABLE);
    }
}

#endif

#endif // SOC_COMMON_H
