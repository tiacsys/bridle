#include <zephyr/kernel.h>

extern void __reset(void);

__attribute__((naked))
static void _isr_wrapper_wrapper(void) {
    __asm__ (
        "csrci mstatus, 0x8 \n" // clear MIE, matching RISC-V spec
        "j _isr_wrapper     \n"
    );
}

__attribute__((naked, section(".vectors.reset")))
void __start(void) {
    __asm__ (
        ".option push             \n"
        ".option norelax          \n"
        "la gp, __global_pointer$ \n" // set gp
        ".option pop              \n"
        : : : "gp"
    );

#if IS_ENABLED(CONFIG_SOC_CH32X035)
    __asm__ (
        "li t0, 0x1f       \n"
        "csrw 0xbc0, t0    \n" // from startup, exact effect unknown
        "li t0, 0x0        \n"
        "csrw 0x804, t0    \n" // disable interrupt nesting and hardware stacking (INTSYSCR)
        : : : "t0"
    );
#else
    #error "define cpu specific settings for soc!"
#endif

    static __aligned(4) void (*isr_handler)(void) = _isr_wrapper_wrapper;
    __asm__ (
        "mv t0, %0         \n"
        "li t1, 0xfffffffc \n"
        "and t0, t0, t1    \n"
        "ori t0, t0, 0x2   \n"
        "csrw mtvec, t0    \n"
        : : "r" (&isr_handler) : "t0", "t1"
    );

    __reset();
    while (1);
}
