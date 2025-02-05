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
         INFO    -   1/118 magpie_f777ni/stm32f777xx tests/kernel/pending/kernel.objects                :bgn:`PASSED` (device: DT04BNT1, 8.490s <zephyr>)
         INFO    -   2/118 magpie_f777ni/stm32f777xx tests/kernel/mem_slab/mslab_stats/kernel.memory_slabs.stats :bgn:`PASSED` (device: DT04BNT1, 2.494s <zephyr>)
         INFO    -   3/118 magpie_f777ni/stm32f777xx tests/kernel/mem_slab/mslab/kernel.memory_slabs    :bgn:`PASSED` (device: DT04BNT1, 2.563s <zephyr>)
         INFO    -   4/118 magpie_f777ni/stm32f777xx tests/kernel/pending/kernel.objects.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 8.645s <zephyr>)
         INFO    -   5/118 magpie_f777ni/stm32f777xx tests/kernel/mem_slab/mslab_threadsafe/kernel.memory_slabs.threadsafe :bgn:`PASSED` (device: DT04BNT1, 3.712s <zephyr>)
         INFO    -   6/118 magpie_f777ni/stm32f777xx tests/kernel/mem_slab/mslab_api/kernel.memory_slabs.api :bgn:`PASSED` (device: DT04BNT1, 9.512s <zephyr>)
         INFO    -   7/118 magpie_f777ni/stm32f777xx tests/kernel/ipi_optimize/kernel.ipi_optimize.smp  :byl:`FILTERED` (runtime filter)
         INFO    -   8/118 magpie_f777ni/stm32f777xx tests/kernel/mem_slab/mslab_concept/kernel.memory_slabs.concept :bgn:`PASSED` (device: DT04BNT1, 5.536s <zephyr>)
         INFO    -   9/118 magpie_f777ni/stm32f777xx tests/kernel/stack/stack/kernel.stack.usage        :bgn:`PASSED` (device: DT04BNT1, 4.933s <zephyr>)
         INFO    -  10/118 magpie_f777ni/stm32f777xx tests/kernel/semaphore/semaphore/kernel.semaphore  :bgn:`PASSED` (device: DT04BNT1, 15.804s <zephyr>)
         INFO    -  11/118 magpie_f777ni/stm32f777xx tests/kernel/semaphore/sys_sem/kernel.semaphore.usage :bgn:`PASSED` (device: DT04BNT1, 4.540s <zephyr>)
         INFO    -  12/118 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.lto              :bgn:`PASSED` (device: DT04BNT1, 5.554s <zephyr>)
         INFO    -  13/118 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.picolibc         :bgn:`PASSED` (device: DT04BNT1, 8.486s <zephyr>)
         INFO    -  14/118 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.misra            :byl:`FILTERED` (runtime filter)
         INFO    -  15/118 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.nano64           :bgn:`PASSED` (device: DT04BNT1, 8.442s <zephyr>)
         INFO    -  16/118 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.nano32           :bgn:`PASSED` (device: DT04BNT1, 9.129s <zephyr>)
         INFO    -  17/118 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.minimallibc      :bgn:`PASSED` (device: DT04BNT1, 8.478s <zephyr>)
         INFO    -  18/118 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.tls              :bgn:`PASSED` (device: DT04BNT1, 9.340s <zephyr>)
         INFO    -  19/118 magpie_f777ni/stm32f777xx tests/kernel/obj_core/obj_core/kernel.obj_core     :bgn:`PASSED` (device: DT04BNT1, 3.437s <zephyr>)
         INFO    -  20/118 magpie_f777ni/stm32f777xx tests/kernel/obj_core/obj_core_stats_api/kernel.obj_core.stats.api :bgn:`PASSED` (device: DT04BNT1, 2.655s <zephyr>)
         INFO    -  21/118 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common                  :bgn:`PASSED` (device: DT04BNT1, 8.514s <zephyr>)
         INFO    -  22/118 magpie_f777ni/stm32f777xx tests/kernel/obj_core/obj_core_stats/kernel.obj_core.stats :bgn:`PASSED` (device: DT04BNT1, 2.917s <zephyr>)
         INFO    -  23/118 magpie_f777ni/stm32f777xx tests/kernel/mbox/mbox_api/kernel.mailbox.api      :bgn:`PASSED` (device: DT04BNT1, 4.223s <zephyr>)
         INFO    -  24/118 magpie_f777ni/stm32f777xx tests/kernel/usage/thread_runtime_stats/kernel.usage :bgn:`PASSED` (device: DT04BNT1, 3.379s <zephyr>)
         INFO    -  25/118 magpie_f777ni/stm32f777xx tests/kernel/mbox/mbox_usage/kernel.mailbox.usage  :bgn:`PASSED` (device: DT04BNT1, 3.603s <zephyr>)
         INFO    -  26/118 magpie_f777ni/stm32f777xx tests/kernel/tickless/tickless_concept/kernel.tickless.concept :bgn:`PASSED` (device: DT04BNT1, 3.413s <zephyr>)
         INFO    -  27/118 magpie_f777ni/stm32f777xx tests/kernel/smp_abort/kernel.smp_abort            :byl:`FILTERED` (runtime filter)
         INFO    -  28/118 magpie_f777ni/stm32f777xx tests/kernel/xip/arch.common.xip.minimallibc       :bgn:`PASSED` (device: DT04BNT1, 3.560s <zephyr>)
         INFO    -  29/118 magpie_f777ni/stm32f777xx tests/kernel/xip/arch.common.xip                   :bgn:`PASSED` (device: DT04BNT1, 3.299s <zephyr>)
         INFO    -  30/118 magpie_f777ni/stm32f777xx tests/kernel/workq/critical/kernel.workqueue.critical :bgn:`PASSED` (device: DT04BNT1, 2.907s <zephyr>)
         INFO    -  31/118 magpie_f777ni/stm32f777xx tests/kernel/workq/work/kernel.workqueue.api       :bgn:`PASSED` (device: DT04BNT1, 4.812s <zephyr>)
         INFO    -  32/118 magpie_f777ni/stm32f777xx tests/kernel/workq/work_queue/kernel.workqueue     :bgn:`PASSED` (device: DT04BNT1, 8.304s <zephyr>)
         INFO    -  33/118 magpie_f777ni/stm32f777xx tests/kernel/profiling/profiling_api/kernel.common.profiling :bgn:`PASSED` (device: DT04BNT1, 2.666s <zephyr>)
         INFO    -  34/118 magpie_f777ni/stm32f777xx tests/kernel/poll/kernel.poll                      :bgn:`PASSED` (device: DT04BNT1, 7.439s <zephyr>)
         INFO    -  35/118 magpie_f777ni/stm32f777xx tests/kernel/poll/kernel.poll.minimallibc          :bgn:`PASSED` (device: DT04BNT1, 7.404s <zephyr>)
         INFO    -  36/118 magpie_f777ni/stm32f777xx tests/kernel/workq/user_work/kernel.workqueue.user :bgn:`PASSED` (device: DT04BNT1, 3.293s <zephyr>)
         INFO    -  37/118 magpie_f777ni/stm32f777xx tests/kernel/sched/preempt/kernel.scheduler.preempt :bgn:`PASSED` (device: DT04BNT1, 2.545s <zephyr>)
         INFO    -  38/118 magpie_f777ni/stm32f777xx tests/kernel/sched/metairq/kernel.scheduler.metairq :bgn:`PASSED` (device: DT04BNT1, 3.251s <zephyr>)
         INFO    -  39/118 magpie_f777ni/stm32f777xx tests/kernel/sched/wraparound/kernel.scheduler.wraparound :bgn:`PASSED` (device: DT04BNT1, 3.771s <zephyr>)
         INFO    -  40/118 magpie_f777ni/stm32f777xx tests/kernel/sched/deadline/kernel.scheduler.deadline.scalable :bgn:`PASSED` (device: DT04BNT1, 3.437s <zephyr>)
         INFO    -  41/118 magpie_f777ni/stm32f777xx tests/kernel/sched/deadline/kernel.scheduler.deadline :bgn:`PASSED` (device: DT04BNT1, 2.791s <zephyr>)
         INFO    -  42/118 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.dumb_no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 5.480s <zephyr>)
         INFO    -  43/118 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.dumb_timeslicing :bgn:`PASSED` (device: DT04BNT1, 21.263s <zephyr>)
         INFO    -  44/118 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.multiq :bgn:`PASSED` (device: DT04BNT1, 21.331s <zephyr>)
         INFO    -  45/118 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.multiq_no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 5.714s <zephyr>)
         INFO    -  46/118 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.slice_perthread :bgn:`PASSED` (device: DT04BNT1, 21.459s <zephyr>)
         INFO    -  47/118 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 6.488s <zephyr>)
         INFO    -  48/118 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler   :bgn:`PASSED` (device: DT04BNT1, 21.277s <zephyr>)
         INFO    -  49/118 magpie_f777ni/stm32f777xx tests/kernel/interrupt/arch.interrupt.minimallibc  :bgn:`PASSED` (device: DT04BNT1, 2.523s <zephyr>)
         INFO    -  50/118 magpie_f777ni/stm32f777xx tests/kernel/interrupt/arch.shared_interrupt       :bgn:`PASSED` (device: DT04BNT1, 2.666s <zephyr>)
         INFO    -  51/118 magpie_f777ni/stm32f777xx tests/kernel/interrupt/arch.shared_interrupt.lto   :bgn:`PASSED` (device: DT04BNT1, 2.701s <zephyr>)
         INFO    -  52/118 magpie_f777ni/stm32f777xx tests/kernel/smp/kernel.multiprocessing.smp.affinity.custom_rom_offset :byl:`FILTERED` (runtime filter)
         INFO    -  53/118 magpie_f777ni/stm32f777xx tests/kernel/smp/kernel.multiprocessing.smp.affinity :byl:`FILTERED` (runtime filter)
         INFO    -  54/118 magpie_f777ni/stm32f777xx tests/kernel/smp/kernel.multiprocessing.smp.minimallibc :byl:`FILTERED` (runtime filter)
         INFO    -  55/118 magpie_f777ni/stm32f777xx tests/kernel/smp/kernel.multiprocessing.smp        :byl:`FILTERED` (runtime filter)
         INFO    -  56/118 magpie_f777ni/stm32f777xx tests/kernel/interrupt/arch.interrupt              :bgn:`PASSED` (device: DT04BNT1, 2.656s <zephyr>)
         INFO    -  57/118 magpie_f777ni/stm32f777xx tests/kernel/obj_tracking/kernel.objects.tracking  :bgn:`PASSED` (device: DT04BNT1, 3.739s <zephyr>)
         INFO    -  58/118 magpie_f777ni/stm32f777xx tests/kernel/obj_tracking/kernel.objects.tracking.minimallibc :bgn:`PASSED` (device: DT04BNT1, 3.332s <zephyr>)
         INFO    -  59/118 magpie_f777ni/stm32f777xx tests/kernel/queue/kernel.queue                    :bgn:`PASSED` (device: DT04BNT1, 5.796s <zephyr>)
         INFO    -  60/118 magpie_f777ni/stm32f777xx tests/kernel/queue/kernel.queue.minimallibc        :bgn:`PASSED` (device: DT04BNT1, 5.008s <zephyr>)
         INFO    -  61/118 magpie_f777ni/stm32f777xx tests/kernel/smp_suspend/kernel.smp_suspend        :byl:`FILTERED` (runtime filter)
         INFO    -  62/118 magpie_f777ni/stm32f777xx tests/kernel/sleep/kernel.common.timing            :bgn:`PASSED` (device: DT04BNT1, 6.061s <zephyr>)
         INFO    -  63/118 magpie_f777ni/stm32f777xx tests/kernel/sleep/kernel.common.timing.minimallibc :bgn:`PASSED` (device: DT04BNT1, 7.195s <zephyr>)
         INFO    -  64/118 magpie_f777ni/stm32f777xx tests/kernel/timer/timer_behavior/kernel.timer.timer :bgn:`PASSED` (device: DT04BNT1, 33.325s <zephyr>)
         INFO    -  65/118 magpie_f777ni/stm32f777xx tests/kernel/timer/timer_api/kernel.timer          :bgn:`PASSED` (device: DT04BNT1, 7.344s <zephyr>)
         INFO    -  66/118 magpie_f777ni/stm32f777xx tests/kernel/timer/timer_error_case/kernel.timer.error_case :bgn:`PASSED` (device: DT04BNT1, 3.603s <zephyr>)
         INFO    -  67/118 magpie_f777ni/stm32f777xx tests/kernel/timer/timepoints/kernel.timer.timepoints :bgn:`PASSED` (device: DT04BNT1, 4.349s <zephyr>)
         INFO    -  68/118 magpie_f777ni/stm32f777xx tests/kernel/timer/timer_monotonic/kernel.timer.monotonic :bgn:`PASSED` (device: DT04BNT1, 5.554s <zephyr>)
         INFO    -  69/118 magpie_f777ni/stm32f777xx tests/kernel/mem_heap/k_heap_api/kernel.k_heap_api :bgn:`PASSED` (device: DT04BNT1, 2.715s <zephyr>)
         INFO    -  70/118 magpie_f777ni/stm32f777xx tests/kernel/cache/kernel.cache.api.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 3.158s <zephyr>)
         INFO    -  71/118 magpie_f777ni/stm32f777xx tests/kernel/cache/kernel.cache.api                :bgn:`PASSED` (device: DT04BNT1, 3.383s <zephyr>)
         INFO    -  72/118 magpie_f777ni/stm32f777xx tests/kernel/fpu_sharing/float_disable/kernel.fpu_sharing.float_disable :bgn:`PASSED` (device: DT04BNT1, 3.992s <zephyr>)
         INFO    -  73/118 magpie_f777ni/stm32f777xx tests/kernel/fifo/fifo_usage/kernel.fifo.usage     :bgn:`PASSED` (device: DT04BNT1, 2.759s <zephyr>)
         INFO    -  74/118 magpie_f777ni/stm32f777xx tests/kernel/fifo/fifo_api/kernel.fifo             :bgn:`PASSED` (device: DT04BNT1, 3.758s <zephyr>)
         INFO    -  75/118 magpie_f777ni/stm32f777xx tests/kernel/fifo/fifo_timeout/kernel.fifo.timeout :bgn:`PASSED` (device: DT04BNT1, 2.715s <zephyr>)
         INFO    -  76/118 magpie_f777ni/stm32f777xx tests/kernel/early_sleep/kernel.common.sleep       :bgn:`PASSED` (device: DT04BNT1, 4.644s <zephyr>)
         INFO    -  77/118 magpie_f777ni/stm32f777xx tests/kernel/early_sleep/kernel.common.sleep.minimallibc :bgn:`PASSED` (device: DT04BNT1, 3.834s <zephyr>)
         INFO    -  78/118 magpie_f777ni/stm32f777xx tests/kernel/threads/tls/kernel.threads.tls        :bgn:`PASSED` (device: DT04BNT1, 3.475s <zephyr>)
         INFO    -  79/118 magpie_f777ni/stm32f777xx tests/kernel/threads/tls/kernel.threads.tls.userspace :bgn:`PASSED` (device: DT04BNT1, 4.953s <zephyr>)
         INFO    -  80/118 magpie_f777ni/stm32f777xx tests/kernel/threads/thread_apis/kernel.threads.apis :bgn:`PASSED` (device: DT04BNT1, 10.185s <zephyr>)
         INFO    -  81/118 magpie_f777ni/stm32f777xx tests/kernel/threads/dynamic_thread/kernel.threads.dynamic :bgn:`PASSED` (device: DT04BNT1, 4.148s <zephyr>)
         INFO    -  82/118 magpie_f777ni/stm32f777xx tests/kernel/ipi_cascade/kernel.ipi_cascade.smp    :byl:`FILTERED` (runtime filter)
         INFO    -  83/118 magpie_f777ni/stm32f777xx tests/kernel/threads/thread_init/kernel.threads.init :bgn:`PASSED` (device: DT04BNT1, 8.218s <zephyr>)
         INFO    -  84/118 magpie_f777ni/stm32f777xx tests/kernel/fatal/message_capture/kernel.logging.message_capture :bgn:`PASSED` (device: DT04BNT1, 3.116s <zephyr>)
         INFO    -  85/118 magpie_f777ni/stm32f777xx tests/kernel/fatal/exception/kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`FILTERED` (runtime filter)
         INFO    -  86/118 magpie_f777ni/stm32f777xx tests/kernel/threads/thread_error_case/kernel.threads.error.case :bgn:`PASSED` (device: DT04BNT1, 3.544s <zephyr>)
         INFO    -  87/118 magpie_f777ni/stm32f777xx tests/kernel/fatal/exception/kernel.common.stack_sentinel :bgn:`PASSED` (device: DT04BNT1, 2.717s <zephyr>)
         INFO    -  88/118 magpie_f777ni/stm32f777xx tests/kernel/fatal/exception/kernel.common.stack_protection_no_userspace :bgn:`PASSED` (device: DT04BNT1, 3.538s <zephyr>)
         INFO    -  89/118 magpie_f777ni/stm32f777xx tests/kernel/fatal/exception/kernel.common.stack_protection_arm_fpu_sharing :bgn:`PASSED` (device: DT04BNT1, 4.233s <zephyr>)
         INFO    -  90/118 magpie_f777ni/stm32f777xx tests/kernel/device/kernel.device.pm               :bgn:`PASSED` (device: DT04BNT1, 4.191s <zephyr>)
         INFO    -  91/118 magpie_f777ni/stm32f777xx tests/kernel/fatal/exception/kernel.common.stack_protection :bgn:`PASSED` (device: DT04BNT1, 4.756s <zephyr>)
         INFO    -  92/118 magpie_f777ni/stm32f777xx tests/kernel/device/kernel.device.minimallibc      :bgn:`PASSED` (device: DT04BNT1, 4.091s <zephyr>)
         INFO    -  93/118 magpie_f777ni/stm32f777xx tests/kernel/msgq/msgq_usage/kernel.message_queue.usage :bgn:`PASSED` (device: DT04BNT1, 3.778s <zephyr>)
         INFO    -  94/118 magpie_f777ni/stm32f777xx tests/kernel/device/kernel.device                  :bgn:`PASSED` (device: DT04BNT1, 4.260s <zephyr>)
         INFO    -  95/118 magpie_f777ni/stm32f777xx tests/kernel/msgq/msgq_api/kernel.message_queue    :bgn:`PASSED` (device: DT04BNT1, 4.263s <zephyr>)
         INFO    -  96/118 magpie_f777ni/stm32f777xx tests/kernel/pipe/pipe_api/kernel.pipe.api         :bgn:`PASSED` (device: DT04BNT1, 7.950s <zephyr>)
         INFO    -  97/118 magpie_f777ni/stm32f777xx tests/kernel/condvar/condvar_api/kernel.condvar    :bgn:`PASSED` (device: DT04BNT1, 5.900s <zephyr>)
         INFO    -  98/118 magpie_f777ni/stm32f777xx tests/kernel/pipe/deprecated/pipe_api/kernel.deprecated.pipe.api :bgn:`PASSED` (device: DT04BNT1, 5.939s <zephyr>)
         INFO    -  99/118 magpie_f777ni/stm32f777xx tests/kernel/pipe/deprecated/pipe/kernel.deprecated.pipe :bgn:`PASSED` (device: DT04BNT1, 6.579s <zephyr>)
         INFO    - 100/118 magpie_f777ni/stm32f777xx tests/kernel/events/event_api/kernel.events        :bgn:`PASSED` (device: DT04BNT1, 3.187s <zephyr>)
         INFO    - 101/118 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot_tls :byl:`FILTERED` (runtime filter)
         INFO    - 102/118 magpie_f777ni/stm32f777xx tests/kernel/lifo/lifo_usage/kernel.lifo.usage     :bgn:`PASSED` (device: DT04BNT1, 3.372s <zephyr>)
         INFO    - 103/118 magpie_f777ni/stm32f777xx tests/kernel/events/sys_event/kernel.events.usage  :bgn:`PASSED` (device: DT04BNT1, 3.469s <zephyr>)
         INFO    - 104/118 magpie_f777ni/stm32f777xx tests/kernel/lifo/lifo_api/kernel.lifo             :bgn:`PASSED` (device: DT04BNT1, 3.078s <zephyr>)
         INFO    - 105/118 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/stack_random/kernel.memory_protection.stack_random :bgn:`PASSED` (device: DT04BNT1, 3.024s <zephyr>)
         INFO    - 106/118 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem.nouser :bgn:`PASSED` (device: DT04BNT1, 3.346s <zephyr>)
         INFO    - 107/118 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot :bgn:`PASSED` (device: DT04BNT1, 4.344s <zephyr>)
         INFO    - 108/118 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map :byl:`FILTERED` (runtime filter)
         INFO    - 109/118 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/futex/kernel.futex        :bgn:`PASSED` (device: DT04BNT1, 5.346s <zephyr>)
         INFO    - 110/118 magpie_f777ni/stm32f777xx tests/kernel/mutex/sys_mutex/kernel.mutex.system.nouser :bgn:`PASSED` (device: DT04BNT1, 10.026s <zephyr>)
         INFO    - 111/118 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem :bgn:`PASSED` (device: DT04BNT1, 6.139s <zephyr>)
         INFO    - 112/118 magpie_f777ni/stm32f777xx tests/kernel/mutex/sys_mutex/kernel.mutex.system   :bgn:`PASSED` (device: DT04BNT1, 10.658s <zephyr>)
         INFO    - 113/118 magpie_f777ni/stm32f777xx tests/kernel/mutex/mutex_api/kernel.mutex          :bgn:`PASSED` (device: DT04BNT1, 17.294s <zephyr>)
         INFO    - 114/118 magpie_f777ni/stm32f777xx tests/kernel/context/kernel.context.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 8.711s <zephyr>)
         INFO    - 115/118 magpie_f777ni/stm32f777xx tests/kernel/mutex/mutex_error_case/kernel.mutex.error :bgn:`PASSED` (device: DT04BNT1, 3.516s <zephyr>)
         INFO    - 116/118 magpie_f777ni/stm32f777xx tests/kernel/context/kernel.context                :bgn:`PASSED` (device: DT04BNT1, 8.729s <zephyr>)
         INFO    - 117/118 magpie_f777ni/stm32f777xx tests/integration/kernel/integration.kernel        :bgn:`PASSED` (device: DT04BNT1, 3.300s <zephyr>)
         INFO    - 118/118 magpie_f777ni/stm32f777xx tests/lib/p4workq/libraries.p4wq                   :bgn:`PASSED` (device: DT04BNT1, 2.713s <zephyr>)

         INFO    - 2537 test scenarios (2325 configurations) selected, :byl:`2219` configurations filtered (2207 by static filter, 12 at runtime).
         INFO    - :bgn:`106 of 106` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`1290.28 seconds`.
         INFO    - 1306 of 1306 executed test cases passed (100.00%) on 1 out of total 947 platforms (0.11%).
         INFO    - 49 selected test cases not executed: 49 skipped.
         INFO    - :bgn:`106` test configurations executed on platforms, :bbl:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board                     \| ID       \|   Counter \|   Failures \|
         \|---------------------------\|----------\|-----------\|------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \|       106 \|          0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni/stm32f777xx...
         INFO    - Writing JSON report .../twister-out/magpie_f777ni_stm32f777xx.json
         INFO    - Run completed
