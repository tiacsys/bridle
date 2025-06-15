#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/timer/system_timer.h>
#include <soc.h>

// inspired by drivers/timer/riscv_machine_timer.c

#define CYC_PER_TICK (sys_clock_hw_cycles_per_sec() / CONFIG_SYS_CLOCK_TICKS_PER_SEC)

static struct {
    struct k_spinlock lock;
    uint64_t last_count;
    uint64_t last_ticks;
} data;

static void set_mtimecmp(uint64_t time) {
    volatile uint32_t *r = (uint32_t*) &SysTick->CMP;
    r[1] = 0xffffffff;
    r[0] = (uint32_t) (time);
    r[1] = (uint32_t) (time >> 32);
}

static uint64_t mtime(void) {
    volatile uint32_t *r = (uint32_t*) &SysTick->CNT;
    uint32_t lo, hi;
    do {
        hi = r[1];
        lo = r[0];
    } while (r[1] != hi);
    return (((uint64_t) hi) << 32) | lo;
}

static void timer_isr(const void *arg) {
    ARG_UNUSED(arg);
    SysTick->SR = 0;
    k_spinlock_key_t key = k_spin_lock(&data.lock);
    uint64_t now     = mtime();
    uint64_t dcycles = now - data.last_count;
    uint32_t dticks  = (uint32_t) dcycles / CYC_PER_TICK;
    data.last_count += dticks * CYC_PER_TICK;
    data.last_ticks += dticks;
    if (!IS_ENABLED(CONFIG_TICKLESS_KERNEL)) {
        set_mtimecmp(data.last_count + CYC_PER_TICK);
    }
    k_spin_unlock(&data.lock, key);
    sys_clock_announce(dticks);
}

void sys_clock_set_timeout(int32_t ticks, bool idle) {
    if (!IS_ENABLED(CONFIG_TICKLESS_KERNEL)) {
        return;
    }

    if (ticks == K_TICKS_FOREVER) {
        set_mtimecmp(mtime() - 1);
        return;
    }

    uint32_t elapsed = sys_clock_elapsed();
    if (ticks <= 0) {
        data.last_count += elapsed * CYC_PER_TICK;
        sys_clock_announce(elapsed);
    } else {
        ticks = CLAMP(ticks, 0, UINT32_MAX / 2 / CYC_PER_TICK); // keep native width divisions
        ticks = CLAMP(ticks, 0, INT32_MAX / 2); // space for ISR latency
    
        k_spinlock_key_t key = k_spin_lock(&data.lock);
        uint64_t cyc = (data.last_ticks + elapsed + ticks) * CYC_PER_TICK;
        k_spin_unlock(&data.lock, key);
        set_mtimecmp(cyc);
    }
}

uint32_t sys_clock_elapsed(void) {
    if (!IS_ENABLED(CONFIG_TICKLESS_KERNEL)) {
        return 0;
    }
    k_spinlock_key_t key = k_spin_lock(&data.lock);
    uint64_t now     = mtime();
    uint64_t dcycles = now - data.last_count;
    uint32_t dticks = (uint32_t) dcycles / CYC_PER_TICK;
    k_spin_unlock(&data.lock, key);
    return dticks;
}

uint32_t sys_clock_cycle_get_32(void) {
    return mtime();
}

uint64_t sys_clock_cycle_get_64(void) {
    return mtime();
}

static int sys_clock_driver_init(void) {
    IRQ_CONNECT(SysTicK_IRQn, 0, timer_isr, NULL, 0);
    SysTick->CNT    = 0;
    data.last_count = 0;
    data.last_ticks = 0;
    if (!IS_ENABLED(CONFIG_TICKLESS_KERNEL)) {
        set_mtimecmp(CYC_PER_TICK);
    }
    SysTick->CTLR = 0x00000027; // count up, no reload, enable
    irq_enable(SysTicK_IRQn);
    return 0;
}

SYS_INIT(sys_clock_driver_init, PRE_KERNEL_2, CONFIG_SYSTEM_CLOCK_INIT_PRIORITY);
