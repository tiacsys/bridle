.. _magpie_f777ni_kernel-tests:

Zephyr OS Kernel
################

Overview
********

See :zephyr_file:`tests/kernel`
for the original scope of tests, its structure and description.

.. _magpie_f777ni_kernel-tests-requirements:

Requirements
************

You will need an ST-LINK/V2 debug tool adapter already connected to the
TiaC Magpie board, which has an already configured UART console connection.

Building and Running
********************

.. tabs::

   .. group-tab:: Running

      Build and run the tests on target as follows:

      .. code-block:: console

         $ west twister \
                --verbose --jobs 4 --inline-logs \
                --enable-size-report --platform-reports \
                --device-testing --hardware-map map.yaml \
                --alt-config-root bridle/zephyr/alt-config/tests \
                --testsuite-root zephyr/tests --tag kernel \
                --exclude-tag security --exclude-tag benchmark

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight-console notranslate

         Device testing on:

         \| Platform                  \| ID       \| Serial device   \|
         \|---------------------------\|----------\|-----------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    -   1/121 magpie_f777ni/stm32f777xx tests/kernel/pending/kernel.pending                :bgn:`PASSED` (device: DT04BNT1, 8.438s <zephyr>)
         INFO    -   2/121 magpie_f777ni/stm32f777xx tests/kernel/mem_slab/mslab_stats/kernel.memory_slabs.stats :bgn:`PASSED` (device: DT04BNT1, 3.280s <zephyr>)
         INFO    -   3/121 magpie_f777ni/stm32f777xx tests/kernel/mem_slab/mslab/kernel.memory_slabs    :bgn:`PASSED` (device: DT04BNT1, 3.170s <zephyr>)
         INFO    -   4/121 magpie_f777ni/stm32f777xx tests/kernel/pending/kernel.pending.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 8.437s <zephyr>)
         INFO    -   5/121 magpie_f777ni/stm32f777xx tests/kernel/mem_slab/mslab_threadsafe/kernel.memory_slabs.threadsafe :bgn:`PASSED` (device: DT04BNT1, 4.133s <zephyr>)
         INFO    -   6/121 magpie_f777ni/stm32f777xx tests/kernel/mem_slab/mslab_api/kernel.memory_slabs.api :bgn:`PASSED` (device: DT04BNT1, 9.637s <zephyr>)
         INFO    -   7/121 magpie_f777ni/stm32f777xx tests/kernel/mem_slab/mslab_concept/kernel.memory_slabs.concept :bgn:`PASSED` (device: DT04BNT1, 5.177s <zephyr>)
         INFO    -   8/121 magpie_f777ni/stm32f777xx tests/kernel/ipi_optimize/kernel.ipi_optimize.smp  :byl:`FILTERED` (runtime filter)
         INFO    -   9/121 magpie_f777ni/stm32f777xx tests/kernel/stack/stack/kernel.stack.usage        :bgn:`PASSED` (device: DT04BNT1, 5.697s <zephyr>)
         INFO    -  10/121 magpie_f777ni/stm32f777xx tests/kernel/semaphore/semaphore/kernel.semaphore  :bgn:`PASSED` (device: DT04BNT1, 15.556s <zephyr>)
         INFO    -  11/121 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.lto              :bgn:`PASSED` (device: DT04BNT1, 6.566s <zephyr>)
         INFO    -  12/121 magpie_f777ni/stm32f777xx tests/kernel/semaphore/sys_sem/kernel.semaphore.usage :bgn:`PASSED` (device: DT04BNT1, 4.151s <zephyr>)
         INFO    -  13/121 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.picolibc         :bgn:`PASSED` (device: DT04BNT1, 8.889s <zephyr>)
         INFO    -  14/121 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.misra            :byl:`FILTERED` (runtime filter)
         INFO    -  15/121 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.nano64           :bgn:`PASSED` (device: DT04BNT1, 8.354s <zephyr>)
         INFO    -  16/121 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.nano32           :bgn:`PASSED` (device: DT04BNT1, 9.214s <zephyr>)
         INFO    -  17/121 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.minimallibc      :bgn:`PASSED` (device: DT04BNT1, 9.484s <zephyr>)
         INFO    -  18/121 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.tls              :bgn:`PASSED` (device: DT04BNT1, 9.338s <zephyr>)
         INFO    -  19/121 magpie_f777ni/stm32f777xx tests/kernel/obj_core/obj_core/kernel.obj_core     :bgn:`PASSED` (device: DT04BNT1, 3.395s <zephyr>)
         INFO    -  20/121 magpie_f777ni/stm32f777xx tests/kernel/obj_core/obj_core_stats_api/kernel.obj_core.stats.api :bgn:`PASSED` (device: DT04BNT1, 2.443s <zephyr>)
         INFO    -  21/121 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common                  :bgn:`PASSED` (device: DT04BNT1, 8.364s <zephyr>)
         INFO    -  22/121 magpie_f777ni/stm32f777xx tests/kernel/obj_core/obj_core_stats/kernel.obj_core.stats :bgn:`PASSED` (device: DT04BNT1, 3.820s <zephyr>)
         INFO    -  23/121 magpie_f777ni/stm32f777xx tests/kernel/mbox/mbox_api/kernel.mailbox.api      :bgn:`PASSED` (device: DT04BNT1, 5.146s <zephyr>)
         INFO    -  24/121 magpie_f777ni/stm32f777xx tests/kernel/usage/thread_runtime_stats/kernel.usage :bgn:`PASSED` (device: DT04BNT1, 2.545s <zephyr>)
         INFO    -  25/121 magpie_f777ni/stm32f777xx tests/kernel/mbox/mbox_usage/kernel.mailbox.usage  :bgn:`PASSED` (device: DT04BNT1, 3.667s <zephyr>)
         INFO    -  26/121 magpie_f777ni/stm32f777xx tests/kernel/smp_abort/kernel.smp_abort            :byl:`FILTERED` (runtime filter)
         INFO    -  27/121 magpie_f777ni/stm32f777xx tests/kernel/tickless/tickless_concept/kernel.tickless.concept :bgn:`PASSED` (device: DT04BNT1, 3.468s <zephyr>)
         INFO    -  28/121 magpie_f777ni/stm32f777xx tests/kernel/xip/arch.common.xip.minimallibc       :bgn:`PASSED` (device: DT04BNT1, 3.576s <zephyr>)
         INFO    -  29/121 magpie_f777ni/stm32f777xx tests/kernel/xip/arch.common.xip                   :bgn:`PASSED` (device: DT04BNT1, 4.769s <zephyr>)
         INFO    -  30/121 magpie_f777ni/stm32f777xx tests/kernel/workq/work/kernel.workqueue.api       :bgn:`PASSED` (device: DT04BNT1, 5.267s <zephyr>)
         INFO    -  31/121 magpie_f777ni/stm32f777xx tests/kernel/workq/critical/kernel.workqueue.critical :bgn:`PASSED` (device: DT04BNT1, 3.518s <zephyr>)
         INFO    -  32/121 magpie_f777ni/stm32f777xx tests/kernel/workq/work_queue/kernel.workqueue.work_timeout :bgn:`PASSED` (device: DT04BNT1, 11.875s <zephyr>)
         INFO    -  33/121 magpie_f777ni/stm32f777xx tests/kernel/workq/work_queue/kernel.workqueue     :bgn:`PASSED` (device: DT04BNT1, 11.068s <zephyr>)
         INFO    -  34/121 magpie_f777ni/stm32f777xx tests/kernel/workq/user_work/kernel.workqueue.user :bgn:`PASSED` (device: DT04BNT1, 3.320s <zephyr>)
         INFO    -  35/121 magpie_f777ni/stm32f777xx tests/kernel/poll/kernel.poll.minimallibc          :bgn:`PASSED` (device: DT04BNT1, 7.305s <zephyr>)
         INFO    -  36/121 magpie_f777ni/stm32f777xx tests/kernel/poll/kernel.poll                      :bgn:`PASSED` (device: DT04BNT1, 7.274s <zephyr>)
         INFO    -  37/121 magpie_f777ni/stm32f777xx tests/kernel/profiling/profiling_api/kernel.common.profiling :bgn:`PASSED` (device: DT04BNT1, 3.295s <zephyr>)
         INFO    -  38/121 magpie_f777ni/stm32f777xx tests/kernel/sched/preempt/kernel.scheduler.preempt :bgn:`PASSED` (device: DT04BNT1, 2.805s <zephyr>)
         INFO    -  39/121 magpie_f777ni/stm32f777xx tests/kernel/sched/metairq/kernel.scheduler.metairq :bgn:`PASSED` (device: DT04BNT1, 5.007s <zephyr>)
         INFO    -  40/121 magpie_f777ni/stm32f777xx tests/kernel/sched/wraparound/kernel.scheduler.wraparound :bgn:`PASSED` (device: DT04BNT1, 3.773s <zephyr>)
         INFO    -  41/121 magpie_f777ni/stm32f777xx tests/kernel/sched/deadline/kernel.scheduler.deadline.scalable :bgn:`PASSED` (device: DT04BNT1, 3.512s <zephyr>)
         INFO    -  42/121 magpie_f777ni/stm32f777xx tests/kernel/sched/deadline/kernel.scheduler.deadline :bgn:`PASSED` (device: DT04BNT1, 2.880s <zephyr>)
         INFO    -  43/121 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.simple_no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 5.555s <zephyr>)
         INFO    -  44/121 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.simple_timeslicing :bgn:`PASSED` (device: DT04BNT1, 21.174s <zephyr>)
         INFO    -  45/121 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.multiq_no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 6.184s <zephyr>)
         INFO    -  46/121 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.multiq :bgn:`PASSED` (device: DT04BNT1, 22.294s <zephyr>)
         INFO    -  47/121 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.slice_perthread :bgn:`PASSED` (device: DT04BNT1, 22.846s <zephyr>)
         INFO    -  48/121 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 5.451s <zephyr>)
         INFO    -  49/121 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler   :bgn:`PASSED` (device: DT04BNT1, 22.066s <zephyr>)
         INFO    -  50/121 magpie_f777ni/stm32f777xx tests/kernel/interrupt/arch.shared_interrupt.lto.speed :bgn:`PASSED` (device: DT04BNT1, 2.625s <zephyr>)
         INFO    -  51/121 magpie_f777ni/stm32f777xx tests/kernel/interrupt/arch.shared_interrupt.lto   :bgn:`PASSED` (device: DT04BNT1, 2.584s <zephyr>)
         INFO    -  52/121 magpie_f777ni/stm32f777xx tests/kernel/interrupt/arch.shared_interrupt       :bgn:`PASSED` (device: DT04BNT1, 2.604s <zephyr>)
         INFO    -  53/121 magpie_f777ni/stm32f777xx tests/kernel/smp/kernel.multiprocessing.smp.affinity.custom_rom_offset :byl:`FILTERED` (runtime filter)
         INFO    -  54/121 magpie_f777ni/stm32f777xx tests/kernel/smp/kernel.multiprocessing.smp.affinity :byl:`FILTERED` (runtime filter)
         INFO    -  55/121 magpie_f777ni/stm32f777xx tests/kernel/interrupt/arch.interrupt.minimallibc  :bgn:`PASSED` (device: DT04BNT1, 3.508s <zephyr>)
         INFO    -  56/121 magpie_f777ni/stm32f777xx tests/kernel/smp/kernel.multiprocessing.smp.minimallibc :byl:`FILTERED` (runtime filter)
         INFO    -  57/121 magpie_f777ni/stm32f777xx tests/kernel/interrupt/arch.interrupt              :bgn:`PASSED` (device: DT04BNT1, 2.448s <zephyr>)
         INFO    -  58/121 magpie_f777ni/stm32f777xx tests/kernel/smp/kernel.multiprocessing.smp        :byl:`FILTERED` (runtime filter)
         INFO    -  59/121 magpie_f777ni/stm32f777xx tests/kernel/obj_tracking/kernel.objects.tracking  :bgn:`PASSED` (device: DT04BNT1, 3.614s <zephyr>)
         INFO    -  60/121 magpie_f777ni/stm32f777xx tests/kernel/obj_tracking/kernel.objects.tracking.minimallibc :bgn:`PASSED` (device: DT04BNT1, 4.832s <zephyr>)
         INFO    -  61/121 magpie_f777ni/stm32f777xx tests/kernel/queue/kernel.queue                    :bgn:`PASSED` (device: DT04BNT1, 6.857s <zephyr>)
         INFO    -  62/121 magpie_f777ni/stm32f777xx tests/kernel/queue/kernel.queue.minimallibc        :bgn:`PASSED` (device: DT04BNT1, 5.008s <zephyr>)
         INFO    -  63/121 magpie_f777ni/stm32f777xx tests/kernel/smp_suspend/kernel.smp_suspend        :byl:`FILTERED` (runtime filter)
         INFO    -  64/121 magpie_f777ni/stm32f777xx tests/kernel/sleep/kernel.common.timing            :bgn:`PASSED` (device: DT04BNT1, 6.258s <zephyr>)
         INFO    -  65/121 magpie_f777ni/stm32f777xx tests/kernel/sleep/kernel.common.timing.minimallibc :bgn:`PASSED` (device: DT04BNT1, 8.285s <zephyr>)
         INFO    -  66/121 magpie_f777ni/stm32f777xx tests/kernel/timer/timer_behavior/kernel.timer.timer :bgn:`PASSED` (device: DT04BNT1, 33.446s <zephyr>)
         INFO    -  67/121 magpie_f777ni/stm32f777xx tests/kernel/timer/timepoints/kernel.timer.timepoints :bgn:`PASSED` (device: DT04BNT1, 3.431s <zephyr>)
         INFO    -  68/121 magpie_f777ni/stm32f777xx tests/kernel/timer/timer_api/kernel.timer          :bgn:`PASSED` (device: DT04BNT1, 7.422s <zephyr>)
         INFO    -  69/121 magpie_f777ni/stm32f777xx tests/kernel/timer/timer_error_case/kernel.timer.error_case :bgn:`PASSED` (device: DT04BNT1, 4.526s <zephyr>)
         INFO    -  70/121 magpie_f777ni/stm32f777xx tests/kernel/timer/timer_monotonic/kernel.timer.monotonic :bgn:`PASSED` (device: DT04BNT1, 5.447s <zephyr>)
         INFO    -  71/121 magpie_f777ni/stm32f777xx tests/kernel/mem_heap/k_heap_api/kernel.k_heap_api :bgn:`PASSED` (device: DT04BNT1, 2.744s <zephyr>)
         INFO    -  72/121 magpie_f777ni/stm32f777xx tests/kernel/cache/kernel.cache.api.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 3.267s <zephyr>)
         INFO    -  73/121 magpie_f777ni/stm32f777xx tests/kernel/cache/kernel.cache.api                :bgn:`PASSED` (device: DT04BNT1, 3.092s <zephyr>)
         INFO    -  74/121 magpie_f777ni/stm32f777xx tests/kernel/fpu_sharing/float_disable/kernel.fpu_sharing.float_disable :bgn:`PASSED` (device: DT04BNT1, 3.160s <zephyr>)
         INFO    -  75/121 magpie_f777ni/stm32f777xx tests/kernel/fifo/fifo_usage/kernel.fifo.usage     :bgn:`PASSED` (device: DT04BNT1, 3.520s <zephyr>)
         INFO    -  76/121 magpie_f777ni/stm32f777xx tests/kernel/fifo/fifo_api/kernel.fifo             :bgn:`PASSED` (device: DT04BNT1, 3.926s <zephyr>)
         INFO    -  77/121 magpie_f777ni/stm32f777xx tests/kernel/fifo/fifo_timeout/kernel.fifo.timeout :bgn:`PASSED` (device: DT04BNT1, 2.765s <zephyr>)
         INFO    -  78/121 magpie_f777ni/stm32f777xx tests/kernel/early_sleep/kernel.common.sleep.minimallibc :bgn:`PASSED` (device: DT04BNT1, 3.821s <zephyr>)
         INFO    -  79/121 magpie_f777ni/stm32f777xx tests/kernel/early_sleep/kernel.common.sleep       :bgn:`PASSED` (device: DT04BNT1, 4.040s <zephyr>)
         INFO    -  80/121 magpie_f777ni/stm32f777xx tests/kernel/threads/tls/kernel.threads.tls        :bgn:`PASSED` (device: DT04BNT1, 4.155s <zephyr>)
         INFO    -  81/121 magpie_f777ni/stm32f777xx tests/kernel/threads/tls/kernel.threads.tls.userspace :bgn:`PASSED` (device: DT04BNT1, 4.241s <zephyr>)
         INFO    -  82/121 magpie_f777ni/stm32f777xx tests/kernel/threads/thread_apis/kernel.threads.apis :bgn:`PASSED` (device: DT04BNT1, 10.638s <zephyr>)
         INFO    -  83/121 magpie_f777ni/stm32f777xx tests/kernel/threads/dynamic_thread/kernel.threads.dynamic :bgn:`PASSED` (device: DT04BNT1, 4.174s <zephyr>)
         INFO    -  84/121 magpie_f777ni/stm32f777xx tests/kernel/ipi_cascade/kernel.ipi_cascade.smp    :byl:`FILTERED` (runtime filter)
         INFO    -  85/121 magpie_f777ni/stm32f777xx tests/kernel/threads/thread_init/kernel.threads.init :bgn:`PASSED` (device: DT04BNT1, 8.190s <zephyr>)
         INFO    -  86/121 magpie_f777ni/stm32f777xx tests/kernel/fatal/exception/kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`FILTERED` (runtime filter)
         INFO    -  87/121 magpie_f777ni/stm32f777xx tests/kernel/fatal/message_capture/kernel.logging.message_capture :bgn:`PASSED` (device: DT04BNT1, 3.367s <zephyr>)
         INFO    -  88/121 magpie_f777ni/stm32f777xx tests/kernel/threads/thread_error_case/kernel.threads.error.case :bgn:`PASSED` (device: DT04BNT1, 4.336s <zephyr>)
         INFO    -  89/121 magpie_f777ni/stm32f777xx tests/kernel/fatal/exception/kernel.common.stack_sentinel :bgn:`PASSED` (device: DT04BNT1, 2.685s <zephyr>)
         INFO    -  90/121 magpie_f777ni/stm32f777xx tests/kernel/fatal/exception/kernel.common.stack_protection_no_userspace :bgn:`PASSED` (device: DT04BNT1, 3.767s <zephyr>)
         INFO    -  91/121 magpie_f777ni/stm32f777xx tests/kernel/fatal/exception/kernel.common.stack_protection_arm_fpu_sharing :bgn:`PASSED` (device: DT04BNT1, 4.110s <zephyr>)
         INFO    -  92/121 magpie_f777ni/stm32f777xx tests/kernel/device/kernel.device.pm               :bgn:`PASSED` (device: DT04BNT1, 4.152s <zephyr>)
         INFO    -  93/121 magpie_f777ni/stm32f777xx tests/kernel/fatal/exception/kernel.common.stack_protection :bgn:`PASSED` (device: DT04BNT1, 3.639s <zephyr>)
         INFO    -  94/121 magpie_f777ni/stm32f777xx tests/kernel/msgq/msgq_usage/kernel.message_queue.usage :bgn:`PASSED` (device: DT04BNT1, 3.430s <zephyr>)
         INFO    -  95/121 magpie_f777ni/stm32f777xx tests/kernel/device/kernel.device.minimallibc      :bgn:`PASSED` (device: DT04BNT1, 3.992s <zephyr>)
         INFO    -  96/121 magpie_f777ni/stm32f777xx tests/kernel/msgq/msgq_api/kernel.message_queue    :bgn:`PASSED` (device: DT04BNT1, 4.075s <zephyr>)
         INFO    -  97/121 magpie_f777ni/stm32f777xx tests/kernel/device/kernel.device                  :bgn:`PASSED` (device: DT04BNT1, 4.109s <zephyr>)
         INFO    -  98/121 magpie_f777ni/stm32f777xx tests/kernel/pipe/pipe_api/kernel.pipe.api         :bgn:`PASSED` (device: DT04BNT1, 8.356s <zephyr>)
         INFO    -  99/121 magpie_f777ni/stm32f777xx tests/kernel/condvar/condvar_api/kernel.condvar    :bgn:`PASSED` (device: DT04BNT1, 4.782s <zephyr>)
         INFO    - 100/121 magpie_f777ni/stm32f777xx tests/kernel/pipe/deprecated/pipe_api/kernel.deprecated.pipe.api :bgn:`PASSED` (device: DT04BNT1, 5.715s <zephyr>)
         INFO    - 101/121 magpie_f777ni/stm32f777xx tests/kernel/pipe/deprecated/pipe/kernel.deprecated.pipe :bgn:`PASSED` (device: DT04BNT1, 6.755s <zephyr>)
         INFO    - 102/121 magpie_f777ni/stm32f777xx tests/kernel/events/event_api/kernel.events        :bgn:`PASSED` (device: DT04BNT1, 2.848s <zephyr>)
         INFO    - 103/121 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot_tls :byl:`FILTERED` (runtime filter)
         INFO    - 104/121 magpie_f777ni/stm32f777xx tests/kernel/lifo/lifo_usage/kernel.lifo.usage     :bgn:`PASSED` (device: DT04BNT1, 3.633s <zephyr>)
         INFO    - 105/121 magpie_f777ni/stm32f777xx tests/kernel/lifo/lifo_api/kernel.lifo             :bgn:`PASSED` (device: DT04BNT1, 2.943s <zephyr>)
         INFO    - 106/121 magpie_f777ni/stm32f777xx tests/kernel/events/sys_event/kernel.events.usage  :bgn:`PASSED` (device: DT04BNT1, 3.471s <zephyr>)
         INFO    - 107/121 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/stack_random/kernel.memory_protection.stack_random :bgn:`PASSED` (device: DT04BNT1, 3.969s <zephyr>)
         INFO    - 108/121 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem.nouser :bgn:`PASSED` (device: DT04BNT1, 4.146s <zephyr>)
         INFO    - 109/121 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot :bgn:`PASSED` (device: DT04BNT1, 3.518s <zephyr>)
         INFO    - 110/121 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map :byl:`FILTERED` (runtime filter)
         INFO    - 111/121 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/futex/kernel.futex        :bgn:`PASSED` (device: DT04BNT1, 4.794s <zephyr>)
         INFO    - 112/121 magpie_f777ni/stm32f777xx tests/kernel/mutex/sys_mutex/kernel.mutex.system.nouser :bgn:`PASSED` (device: DT04BNT1, 10.227s <zephyr>)
         INFO    - 113/121 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem :bgn:`PASSED` (device: DT04BNT1, 6.057s <zephyr>)
         INFO    - 114/121 magpie_f777ni/stm32f777xx tests/kernel/mutex/sys_mutex/kernel.mutex.system   :bgn:`PASSED` (device: DT04BNT1, 11.226s <zephyr>)
         INFO    - 115/121 magpie_f777ni/stm32f777xx tests/kernel/mutex/mutex_api/kernel.mutex.scalable :bgn:`PASSED` (device: DT04BNT1, 16.467s <zephyr>)
         INFO    - 116/121 magpie_f777ni/stm32f777xx tests/kernel/mutex/mutex_api/kernel.mutex          :bgn:`PASSED` (device: DT04BNT1, 15.387s <zephyr>)
         INFO    - 117/121 magpie_f777ni/stm32f777xx tests/kernel/mutex/mutex_error_case/kernel.mutex.error :bgn:`PASSED` (device: DT04BNT1, 5.202s <zephyr>)
         INFO    - 118/121 magpie_f777ni/stm32f777xx tests/kernel/context/kernel.context.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 8.241s <zephyr>)
         INFO    - 119/121 magpie_f777ni/stm32f777xx tests/kernel/context/kernel.context                :bgn:`PASSED` (device: DT04BNT1, 9.919s <zephyr>)
         INFO    - 120/121 magpie_f777ni/stm32f777xx tests/integration/kernel/integration.kernel        :bgn:`PASSED` (device: DT04BNT1, 2.497s <zephyr>)
         INFO    - 121/121 magpie_f777ni/stm32f777xx tests/lib/p4workq/libraries.p4wq                   :bgn:`PASSED` (device: DT04BNT1, 2.577s <zephyr>)

         INFO    - 2763 test scenarios (2539 configurations) selected, :byl:`2430` configurations filtered (2418 by static filter, 12 at runtime).
         INFO    - :bgn:`109 of 109` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`2063.46 seconds`.
         INFO    - 1354 of 1354 executed test cases passed (100.00%) on 1 out of total 1133 platforms (0.09%).
         INFO    - 51 selected test cases not executed: 51 skipped.
         INFO    - :bgn:`109` test configurations executed on platforms, :bbl:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board                     \| ID       \|   Counter \|   Failures \|
         \|---------------------------\|----------\|-----------\|------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \|       109 \|          0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni/stm32f777xx...
         INFO    - Writing JSON report .../twister-out/magpie_f777ni_stm32f777xx.json
         INFO    - Run completed
