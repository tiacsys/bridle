#ifndef SYSTEM_CH32X035_H
#define SYSTEM_CH32X035_H

#include <stdint.h>

static inline void Delay_Init(void) {}

static inline void Delay_Us(uint32_t us) {
    // approximately correct at 48MHz w/ 2 wait states
    __asm__ (
        "mv t0, %0       \n"
        "slli t0, t0, 2  \n"
        "beqz t0, 2f     \n"
    "1:"
        "addi t0, t0, -1 \n"
        "bnez t0, 1b     \n"
    "2:"
        : : "r" (us) : "t0"
    );
}

#endif // SYSTEM_CH32X035_H
