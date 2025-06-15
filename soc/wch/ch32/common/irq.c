#include <zephyr/kernel.h>
#include <soc.h>

void arch_irq_enable(unsigned int irq) {
    NVIC_EnableIRQ(irq);
}

void arch_irq_disable(unsigned int irq) {
    NVIC_DisableIRQ(irq);
}

void __soc_handle_irq(unsigned long mcause) {
    (void) mcause; // do nothing
}

/*
 * For normal RISC-V, interrupts are disabled (MIE=0) upon entering an ISR and get re-enabled on
 * return (mret sets MIE=MPIE). While in the ISR, it's possible to manually re-enable interrupts,
 * after clearing the IRQ of course, and simply jump elsewhere. Zephyr uses this to implement context
 * switches from within _isr_wrapper.
 * 
 * In order to support interrupt nesting, CH32 doesn't follow these assumptions. Interrupts remain
 * enabled (MIE=1) and an mret is required to exit the interrupt level. Since Zephyr's context switch
 * simply jumps without mret, the next thread will effectively have same or lower priority interrupts
 * disabled. It should be noted that FreeRTOS does context switches using mret so it lacks this issue,
 * but it also doesn't currently support nesting.
 * 
 * The workaround consists of three parts. First, we need to mret before a context switch in _isr_wrapper.
 * We can't do it in __soc_handle_irq since our installed handlers which clear the IRQ get called after.
 * The cleanest way is instead hooking into sys_trace_isr_exit, which does mean we can't use the trace
 * subsystem. Since interrupts must remain disabled after this added mret, we clear MPIE, do the ret, then
 * set MPIE again. The double mret would definitely mess with CH32 interrupt nesting, so we completely disable
 * that in INTSYSCR.
 * 
 * Second, we need to make a wrapper around _isr_wrapper, which we call _isr_wrapper_wrapper, that clears
 * MIE before jumping to _isr_wrapper. Since _isr_wrapper saves and restores mstatus, having MIE=1 and our
 * added mret can unintentionally re-enable interrupts before _isr_wrapper returns.
 * 
 * Third, we need to disable wfi inside the idle thread. Unforunately, it looks like the double mret can
 * cause the next IRQ to be missed. This does mean we can't use sleep states effectively.
 */
__attribute__((naked))
void sys_trace_isr_exit_user(void) {
    __asm__ (
        "li a0, 0x1800    \n" // disable MPIE so MIE disabled after mret
        "csrw mstatus, a0 \n"
        "la a0, 1f        \n"
        "csrw mepc, a0    \n"
        "mret             \n"
    "1:"
        "li a0, 0x1880    \n" // enable MPIE so MIE restored correctly
        "csrw mstatus, a0 \n"
        "ret              \n"
    );
}

#if !(defined(CONFIG_TRACING) && defined(CONFIG_TRACING_USER) && defined(CONFIG_TRACING_ISR))
#error "please don't use tracing subsytem"
#endif
