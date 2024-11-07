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
                --testsuite-root zephyr/tests --tag kernel --exclude-tag security

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
         INFO    -   1/135 magpie_f777ni/stm32f777xx tests/kernel/mem_slab/mslab_stats/kernel.memory_slabs.stats :bgn:`PASSED` (device: DT04BNT1, 2.918s)
         INFO    -   2/135 magpie_f777ni/stm32f777xx tests/kernel/pending/kernel.objects                :bgn:`PASSED` (device: DT04BNT1, 8.910s)
         INFO    -   3/135 magpie_f777ni/stm32f777xx tests/kernel/mem_slab/mslab/kernel.memory_slabs    :bgn:`PASSED` (device: DT04BNT1, 2.389s)
         INFO    -   4/135 magpie_f777ni/stm32f777xx tests/kernel/pending/kernel.objects.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 8.498s)
         INFO    -   5/135 magpie_f777ni/stm32f777xx tests/kernel/mem_slab/mslab_threadsafe/kernel.memory_slabs.threadsafe :bgn:`PASSED` (device: DT04BNT1, 3.560s)
         INFO    -   6/135 magpie_f777ni/stm32f777xx tests/kernel/mem_slab/mslab_api/kernel.memory_slabs.api :bgn:`PASSED` (device: DT04BNT1, 9.503s)
         INFO    -   7/135 magpie_f777ni/stm32f777xx tests/kernel/ipi_optimize/kernel.ipi_optimize.smp  :byl:`FILTERED` (runtime filter)
         INFO    -   8/135 magpie_f777ni/stm32f777xx tests/kernel/mem_slab/mslab_concept/kernel.memory_slabs.concept :bgn:`PASSED` (device: DT04BNT1, 5.023s)
         INFO    -   9/135 magpie_f777ni/stm32f777xx tests/kernel/stack/stack/kernel.stack.usage        :bgn:`PASSED` (device: DT04BNT1, 4.987s)
         INFO    -  10/135 magpie_f777ni/stm32f777xx tests/kernel/semaphore/semaphore/kernel.semaphore  :bgn:`PASSED` (device: DT04BNT1, 15.487s)
         INFO    -  11/135 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.lto              :bgn:`PASSED` (device: DT04BNT1, 5.962s)
         INFO    -  12/135 magpie_f777ni/stm32f777xx tests/kernel/semaphore/sys_sem/kernel.semaphore.usage :bgn:`PASSED` (device: DT04BNT1, 3.187s)
         INFO    -  13/135 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.picolibc         :bgn:`PASSED` (device: DT04BNT1, 8.853s)
         INFO    -  14/135 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.misra            :byl:`FILTERED` (runtime filter)
         INFO    -  15/135 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.nano64           :bgn:`PASSED` (device: DT04BNT1, 8.126s)
         INFO    -  16/135 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.nano32           :bgn:`PASSED` (device: DT04BNT1, 9.026s)
         INFO    -  17/135 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.minimallibc      :bgn:`PASSED` (device: DT04BNT1, 8.698s)
         INFO    -  18/135 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common.tls              :bgn:`PASSED` (device: DT04BNT1, 8.263s)
         INFO    -  19/135 magpie_f777ni/stm32f777xx tests/kernel/obj_core/obj_core/kernel.obj_core     :bgn:`PASSED` (device: DT04BNT1, 3.422s)
         INFO    -  20/135 magpie_f777ni/stm32f777xx tests/kernel/obj_core/obj_core_stats_api/kernel.obj_core.stats.api :bgn:`PASSED` (device: DT04BNT1, 2.440s)
         INFO    -  21/135 magpie_f777ni/stm32f777xx tests/kernel/common/kernel.common                  :bgn:`PASSED` (device: DT04BNT1, 8.239s)
         INFO    -  22/135 magpie_f777ni/stm32f777xx tests/kernel/obj_core/obj_core_stats/kernel.obj_core.stats :bgn:`PASSED` (device: DT04BNT1, 3.557s)
         INFO    -  23/135 magpie_f777ni/stm32f777xx tests/kernel/mbox/mbox_api/kernel.mailbox.api      :bgn:`PASSED` (device: DT04BNT1, 4.675s)
         INFO    -  24/135 magpie_f777ni/stm32f777xx tests/kernel/usage/thread_runtime_stats/kernel.usage :bgn:`PASSED` (device: DT04BNT1, 3.122s)
         INFO    -  25/135 magpie_f777ni/stm32f777xx tests/kernel/mbox/mbox_usage/kernel.mailbox.usage  :bgn:`PASSED` (device: DT04BNT1, 3.369s)
         INFO    -  26/135 magpie_f777ni/stm32f777xx tests/kernel/tickless/tickless_concept/kernel.tickless.concept :bgn:`PASSED` (device: DT04BNT1, 3.339s)
         INFO    -  27/135 magpie_f777ni/stm32f777xx tests/kernel/smp_abort/kernel.smp_abort            :byl:`FILTERED` (runtime filter)
         INFO    -  28/135 magpie_f777ni/stm32f777xx tests/kernel/workq/critical/kernel.workqueue.critical.sam :byl:`FILTERED` (runtime filter)
         INFO    -  29/135 magpie_f777ni/stm32f777xx tests/kernel/xip/arch.common.xip.minimallibc       :bgn:`PASSED` (device: DT04BNT1, 3.134s)
         INFO    -  30/135 magpie_f777ni/stm32f777xx tests/kernel/xip/arch.common.xip                   :bgn:`PASSED` (device: DT04BNT1, 2.376s)
         INFO    -  31/135 magpie_f777ni/stm32f777xx tests/kernel/workq/work/kernel.workqueue.api       :bgn:`PASSED` (device: DT04BNT1, 5.211s)
         INFO    -  32/135 magpie_f777ni/stm32f777xx tests/kernel/workq/critical/kernel.workqueue.critical :bgn:`PASSED` (device: DT04BNT1, 3.771s)
         INFO    -  33/135 magpie_f777ni/stm32f777xx tests/kernel/workq/work_queue/kernel.workqueue     :bgn:`PASSED` (device: DT04BNT1, 7.137s)
         INFO    -  34/135 magpie_f777ni/stm32f777xx tests/kernel/profiling/profiling_api/kernel.common.profiling :bgn:`PASSED` (device: DT04BNT1, 2.581s)
         INFO    -  35/135 magpie_f777ni/stm32f777xx tests/kernel/workq/user_work/kernel.workqueue.user :bgn:`PASSED` (device: DT04BNT1, 3.178s)
         INFO    -  36/135 magpie_f777ni/stm32f777xx tests/kernel/poll/kernel.poll                      :bgn:`PASSED` (device: DT04BNT1, 7.212s)
         INFO    -  37/135 magpie_f777ni/stm32f777xx tests/kernel/poll/kernel.poll.minimallibc          :bgn:`PASSED` (device: DT04BNT1, 7.931s)
         INFO    -  38/135 magpie_f777ni/stm32f777xx tests/kernel/sched/preempt/kernel.scheduler.preempt :bgn:`PASSED` (device: DT04BNT1, 3.135s)
         INFO    -  39/135 magpie_f777ni/stm32f777xx tests/kernel/sched/metairq/kernel.scheduler.metairq :bgn:`PASSED` (device: DT04BNT1, 2.569s)
         INFO    -  40/135 magpie_f777ni/stm32f777xx tests/kernel/sched/deadline/kernel.scheduler.deadline.scalable :bgn:`PASSED` (device: DT04BNT1, 3.642s)
         INFO    -  41/135 magpie_f777ni/stm32f777xx tests/kernel/sched/deadline/kernel.scheduler.deadline :bgn:`PASSED` (device: DT04BNT1, 4.750s)
         INFO    -  42/135 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.dumb_no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 6.180s)
         INFO    -  43/135 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.dumb_timeslicing :bgn:`PASSED` (device: DT04BNT1, 21.198s)
         INFO    -  44/135 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.multiq :bgn:`PASSED` (device: DT04BNT1, 21.704s)
         INFO    -  45/135 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.multiq_no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 6.104s)
         INFO    -  46/135 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.slice_perthread :bgn:`PASSED` (device: DT04BNT1, 22.106s)
         INFO    -  47/135 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler.no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 6.857s)
         INFO    -  48/135 magpie_f777ni/stm32f777xx tests/kernel/interrupt/arch.shared_interrupt.lto   :bgn:`PASSED` (device: DT04BNT1, 2.592s)
         INFO    -  49/135 magpie_f777ni/stm32f777xx tests/kernel/sched/schedule_api/kernel.scheduler   :bgn:`PASSED` (device: DT04BNT1, 22.747s)
         INFO    -  50/135 magpie_f777ni/stm32f777xx tests/kernel/interrupt/arch.shared_interrupt       :bgn:`PASSED` (device: DT04BNT1, 2.904s)
         INFO    -  51/135 magpie_f777ni/stm32f777xx tests/kernel/interrupt/arch.interrupt.minimallibc  :bgn:`PASSED` (device: DT04BNT1, 2.626s)
         INFO    -  52/135 magpie_f777ni/stm32f777xx tests/kernel/smp/kernel.multiprocessing.smp.affinity.custom_rom_offset :byl:`FILTERED` (runtime filter)
         INFO    -  53/135 magpie_f777ni/stm32f777xx tests/kernel/smp/kernel.multiprocessing.smp.affinity :byl:`FILTERED` (runtime filter)
         INFO    -  54/135 magpie_f777ni/stm32f777xx tests/kernel/smp/kernel.multiprocessing.smp.minimallibc :byl:`FILTERED` (runtime filter)
         INFO    -  55/135 magpie_f777ni/stm32f777xx tests/kernel/interrupt/arch.interrupt              :bgn:`PASSED` (device: DT04BNT1, 2.440s)
         INFO    -  56/135 magpie_f777ni/stm32f777xx tests/kernel/smp/kernel.multiprocessing.smp        :byl:`FILTERED` (runtime filter)
         INFO    -  57/135 magpie_f777ni/stm32f777xx tests/kernel/obj_tracking/kernel.objects.tracking  :bgn:`PASSED` (device: DT04BNT1, 4.873s)
         INFO    -  58/135 magpie_f777ni/stm32f777xx tests/kernel/obj_tracking/kernel.objects.tracking.minimallibc :bgn:`PASSED` (device: DT04BNT1, 3.521s)
         INFO    -  59/135 magpie_f777ni/stm32f777xx tests/kernel/queue/kernel.queue                    :bgn:`PASSED` (device: DT04BNT1, 6.118s)
         INFO    -  60/135 magpie_f777ni/stm32f777xx tests/kernel/queue/kernel.queue.minimallibc        :bgn:`PASSED` (device: DT04BNT1, 7.207s)
         INFO    -  61/135 magpie_f777ni/stm32f777xx tests/kernel/smp_suspend/kernel.smp_suspend        :byl:`FILTERED` (runtime filter)
         INFO    -  62/135 magpie_f777ni/stm32f777xx tests/kernel/sleep/kernel.common.timing            :bgn:`PASSED` (device: DT04BNT1, 7.245s)
         INFO    -  63/135 magpie_f777ni/stm32f777xx tests/kernel/sleep/kernel.common.timing.minimallibc :bgn:`PASSED` (device: DT04BNT1, 8.196s)
         INFO    -  64/135 magpie_f777ni/stm32f777xx tests/kernel/timer/timer_behavior/kernel.timer.timer :bgn:`PASSED` (device: DT04BNT1, 33.275s)
         INFO    -  65/135 magpie_f777ni/stm32f777xx tests/kernel/timer/timer_api/kernel.timer          :bgn:`PASSED` (device: DT04BNT1, 7.315s)
         INFO    -  66/135 magpie_f777ni/stm32f777xx tests/kernel/timer/timepoints/kernel.timer.timepoints :bgn:`PASSED` (device: DT04BNT1, 3.483s)
         INFO    -  67/135 magpie_f777ni/stm32f777xx tests/kernel/timer/timer_error_case/kernel.timer.error_case :bgn:`PASSED` (device: DT04BNT1, 4.602s)
         INFO    -  68/135 magpie_f777ni/stm32f777xx tests/kernel/timer/timer_monotonic/kernel.timer.monotonic :bgn:`PASSED` (device: DT04BNT1, 5.593s)
         INFO    -  69/135 magpie_f777ni/stm32f777xx tests/kernel/mem_heap/k_heap_api/kernel.k_heap_api :bgn:`PASSED` (device: DT04BNT1, 2.644s)
         INFO    -  70/135 magpie_f777ni/stm32f777xx tests/kernel/cache/kernel.cache.api.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 3.115s)
         INFO    -  71/135 magpie_f777ni/stm32f777xx tests/kernel/cache/kernel.cache.api                :bgn:`PASSED` (device: DT04BNT1, 3.054s)
         INFO    -  72/135 magpie_f777ni/stm32f777xx tests/kernel/fpu_sharing/float_disable/kernel.fpu_sharing.float_disable :bgn:`PASSED` (device: DT04BNT1, 4.659s)
         INFO    -  73/135 magpie_f777ni/stm32f777xx tests/kernel/fifo/fifo_usage/kernel.fifo.usage     :bgn:`PASSED` (device: DT04BNT1, 3.782s)
         INFO    -  74/135 magpie_f777ni/stm32f777xx tests/kernel/fifo/fifo_api/kernel.fifo             :bgn:`PASSED` (device: DT04BNT1, 4.100s)
         INFO    -  75/135 magpie_f777ni/stm32f777xx tests/kernel/fifo/fifo_timeout/kernel.fifo.timeout :bgn:`PASSED` (device: DT04BNT1, 2.623s)
         INFO    -  76/135 magpie_f777ni/stm32f777xx tests/kernel/early_sleep/kernel.common.sleep       :bgn:`PASSED` (device: DT04BNT1, 3.910s)
         INFO    -  77/135 magpie_f777ni/stm32f777xx tests/kernel/early_sleep/kernel.common.sleep.minimallibc :bgn:`PASSED` (device: DT04BNT1, 3.838s)
         INFO    -  78/135 magpie_f777ni/stm32f777xx tests/kernel/threads/tls/kernel.threads.tls        :bgn:`PASSED` (device: DT04BNT1, 4.386s)
         INFO    -  79/135 magpie_f777ni/stm32f777xx tests/kernel/threads/tls/kernel.threads.tls.userspace :bgn:`PASSED` (device: DT04BNT1, 4.106s)
         INFO    -  80/135 magpie_f777ni/stm32f777xx tests/kernel/threads/thread_apis/kernel.threads.apis :bgn:`PASSED` (device: DT04BNT1, 9.542s)
         INFO    -  81/135 magpie_f777ni/stm32f777xx tests/kernel/threads/dynamic_thread/kernel.threads.dynamic :bgn:`PASSED` (device: DT04BNT1, 5.019s)
         INFO    -  82/135 magpie_f777ni/stm32f777xx tests/kernel/threads/thread_init/kernel.threads.init :bgn:`PASSED` (device: DT04BNT1, 7.880s)
         INFO    -  83/135 magpie_f777ni/stm32f777xx tests/kernel/ipi_cascade/kernel.ipi_cascade.smp    :byl:`FILTERED` (runtime filter)
         INFO    -  84/135 magpie_f777ni/stm32f777xx tests/kernel/fatal/exception/kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`FILTERED` (runtime filter)
         INFO    -  85/135 magpie_f777ni/stm32f777xx tests/kernel/threads/thread_error_case/kernel.threads.error.case :bgn:`PASSED` (device: DT04BNT1, 4.145s)
         INFO    -  86/135 magpie_f777ni/stm32f777xx tests/kernel/fatal/message_capture/kernel.logging.message_capture :bgn:`PASSED` (device: DT04BNT1, 3.272s)
         INFO    -  87/135 magpie_f777ni/stm32f777xx tests/kernel/fatal/exception/kernel.common.stack_sentinel :bgn:`PASSED` (device: DT04BNT1, 2.679s)
         INFO    -  88/135 magpie_f777ni/stm32f777xx tests/kernel/fatal/exception/kernel.common.stack_protection_no_userspace :bgn:`PASSED` (device: DT04BNT1, 3.792s)
         INFO    -  89/135 magpie_f777ni/stm32f777xx tests/kernel/fatal/exception/kernel.common.stack_protection_arm_fpu_sharing :bgn:`PASSED` (device: DT04BNT1, 4.152s)
         INFO    -  90/135 magpie_f777ni/stm32f777xx tests/kernel/device/kernel.device.pm               :bgn:`PASSED` (device: DT04BNT1, 3.901s)
         INFO    -  91/135 magpie_f777ni/stm32f777xx tests/kernel/fatal/exception/kernel.common.stack_protection :bgn:`PASSED` (device: DT04BNT1, 4.949s)
         INFO    -  92/135 magpie_f777ni/stm32f777xx tests/kernel/msgq/msgq_usage/kernel.message_queue.usage :bgn:`PASSED` (device: DT04BNT1, 3.740s)
         INFO    -  93/135 magpie_f777ni/stm32f777xx tests/kernel/device/kernel.device.minimallibc      :bgn:`PASSED` (device: DT04BNT1, 4.154s)
         INFO    -  94/135 magpie_f777ni/stm32f777xx tests/kernel/device/kernel.device                  :bgn:`PASSED` (device: DT04BNT1, 4.018s)
         INFO    -  95/135 magpie_f777ni/stm32f777xx tests/kernel/msgq/msgq_api/kernel.message_queue    :bgn:`PASSED` (device: DT04BNT1, 4.313s)
         INFO    -  96/135 magpie_f777ni/stm32f777xx tests/kernel/condvar/condvar_api/kernel.condvar    :bgn:`PASSED` (device: DT04BNT1, 6.284s)
         INFO    -  97/135 magpie_f777ni/stm32f777xx tests/kernel/pipe/pipe_api/kernel.pipe.api         :bgn:`PASSED` (device: DT04BNT1, 6.391s)
         INFO    -  98/135 magpie_f777ni/stm32f777xx tests/kernel/pipe/pipe/kernel.pipe                 :bgn:`PASSED` (device: DT04BNT1, 6.010s)
         INFO    -  99/135 magpie_f777ni/stm32f777xx tests/kernel/events/sys_event/kernel.events.usage  :bgn:`PASSED` (device: DT04BNT1, 3.447s)
         INFO    - 100/135 magpie_f777ni/stm32f777xx tests/kernel/events/event_api/kernel.events        :bgn:`PASSED` (device: DT04BNT1, 3.852s)
         INFO    - 101/135 magpie_f777ni/stm32f777xx tests/kernel/lifo/lifo_usage/kernel.lifo.usage     :bgn:`PASSED` (device: DT04BNT1, 4.584s)
         INFO    - 102/135 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot_tls :byl:`FILTERED` (runtime filter)
         INFO    - 103/135 magpie_f777ni/stm32f777xx tests/kernel/lifo/lifo_api/kernel.lifo             :bgn:`PASSED` (device: DT04BNT1, 2.936s)
         INFO    - 104/135 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/stack_random/kernel.memory_protection.stack_random :bgn:`PASSED` (device: DT04BNT1, 3.777s)
         INFO    - 105/135 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem.nouser :bgn:`PASSED` (device: DT04BNT1, 4.153s)
         INFO    - 106/135 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot :bgn:`PASSED` (device: DT04BNT1, 4.502s)
         INFO    - 107/135 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64 :byl:`FILTERED` (runtime filter)
         INFO    - 108/135 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map :byl:`FILTERED` (runtime filter)
         INFO    - 109/135 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/futex/kernel.futex        :bgn:`PASSED` (device: DT04BNT1, 5.296s)
         INFO    - 110/135 magpie_f777ni/stm32f777xx tests/kernel/mutex/sys_mutex/kernel.mutex.system.nouser :bgn:`PASSED` (device: DT04BNT1, 10.108s)
         INFO    - 111/135 magpie_f777ni/stm32f777xx tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem :bgn:`PASSED` (device: DT04BNT1, 4.867s)
         INFO    - 112/135 magpie_f777ni/stm32f777xx tests/kernel/mutex/mutex_api/kernel.mutex          :bgn:`PASSED` (device: DT04BNT1, 16.428s)
         INFO    - 113/135 magpie_f777ni/stm32f777xx tests/kernel/mutex/sys_mutex/kernel.mutex.system   :bgn:`PASSED` (device: DT04BNT1, 12.043s)
         INFO    - 114/135 magpie_f777ni/stm32f777xx tests/kernel/context/kernel.context.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 8.133s)
         INFO    - 115/135 magpie_f777ni/stm32f777xx tests/kernel/mutex/mutex_error_case/kernel.mutex.error :bgn:`PASSED` (device: DT04BNT1, 5.002s)
         INFO    - 116/135 magpie_f777ni/stm32f777xx tests/kernel/context/kernel.context                :bgn:`PASSED` (device: DT04BNT1, 9.489s)
         INFO    - 117/135 magpie_f777ni/stm32f777xx tests/integration/kernel/integration.kernel        :bgn:`PASSED` (device: DT04BNT1, 3.649s)
         INFO    - 118/135 magpie_f777ni/stm32f777xx tests/lib/p4workq/libraries.p4wq                   :bgn:`PASSED` (device: DT04BNT1, 2.800s)
         INFO    - 119/135 magpie_f777ni/stm32f777xx tests/benchmarks/latency_measure/benchmark.kernel.latency :byl:`FILTERED` (runtime filter)
         INFO    - 120/135 magpie_f777ni/stm32f777xx tests/benchmarks/latency_measure/benchmark.kernel.latency.stm32 :bgn:`PASSED` (device: DT04BNT1, 4.500s)
         INFO    - 121/135 magpie_f777ni/stm32f777xx tests/benchmarks/data_structure_perf/dlist_perf/benchmark.data_structure_perf.dlist :bgn:`PASSED` (device: DT04BNT1, 2.481s)
         INFO    - 122/135 magpie_f777ni/stm32f777xx tests/benchmarks/sys_kernel/benchmark.kernel.core  :bgn:`PASSED` (device: DT04BNT1, 4.446s)
         INFO    - 123/135 magpie_f777ni/stm32f777xx tests/benchmarks/latency_measure/benchmark.kernel.latency.userspace :bgn:`PASSED` (device: DT04BNT1, 7.096s)
         INFO    - 124/135 magpie_f777ni/stm32f777xx tests/benchmarks/data_structure_perf/rbtree_perf/benchmark.data_structure_perf.rbtree :bgn:`PASSED` (device: DT04BNT1, 3.542s)
         INFO    - 125/135 magpie_f777ni/stm32f777xx tests/benchmarks/app_kernel/benchmark.kernel.application.timeslicing :bgn:`PASSED` (device: DT04BNT1, 5.150s)
         INFO    - 126/135 magpie_f777ni/stm32f777xx tests/benchmarks/app_kernel/benchmark.kernel.application.user.timeslicing :bgn:`PASSED` (device: DT04BNT1, 10.241s)
         INFO    - 127/135 magpie_f777ni/stm32f777xx tests/benchmarks/app_kernel/benchmark.kernel.application.objcore.stats :bgn:`PASSED` (device: DT04BNT1, 3.576s)
         INFO    - 128/135 magpie_f777ni/stm32f777xx tests/benchmarks/app_kernel/benchmark.kernel.application.user.objcore.stats :bgn:`PASSED` (device: DT04BNT1, 10.321s)
         INFO    - 129/135 magpie_f777ni/stm32f777xx tests/benchmarks/app_kernel/benchmark.kernel.application.user :bgn:`PASSED` (device: DT04BNT1, 9.233s)
         INFO    - 130/135 magpie_f777ni/stm32f777xx tests/benchmarks/app_kernel/benchmark.kernel.application :bgn:`PASSED` (device: DT04BNT1, 4.782s)
         INFO    - 131/135 magpie_f777ni/stm32f777xx tests/benchmarks/wait_queues/benchmark.wait_queues.scalable :bgn:`PASSED` (device: DT04BNT1, 9.871s)
         INFO    - 132/135 magpie_f777ni/stm32f777xx tests/benchmarks/wait_queues/benchmark.wait_queues.dumb :bgn:`PASSED` (device: DT04BNT1, 8.689s)
         INFO    - 133/135 magpie_f777ni/stm32f777xx tests/benchmarks/sched_queues/benchmark.sched_queues.multiq :bgn:`PASSED` (device: DT04BNT1, 8.271s)
         INFO    - 134/135 magpie_f777ni/stm32f777xx tests/benchmarks/sched_queues/benchmark.sched_queues.scalable :bgn:`PASSED` (device: DT04BNT1, 10.743s)
         INFO    - 135/135 magpie_f777ni/stm32f777xx tests/benchmarks/sched_queues/benchmark.sched_queues.dumb :bgn:`PASSED` (device: DT04BNT1, 7.651s)

         INFO    - 2294 test scenarios (2077 test instances) selected, :byl:`1957` configurations filtered (1942 by static filter, 15 at runtime).
         INFO    - :bgn:`120 of 120` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`2185.91 seconds`.
         INFO    - 1243 of 1194 executed test cases passed (104.10%) on 1 out of total 876 platforms (0.11%).
         INFO    - 14864 selected test cases not executed: 258 skipped, 14606 filtered.
         INFO    - :bgn:`120` test configurations executed on platforms, :bbl:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board                     \| ID       \|   Counter \|   Failures \|
         \|---------------------------\|----------\|-----------\|------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \|       120 \|          0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni/stm32f777xx...
         INFO    - Writing JSON report .../twister-out/magpie_f777ni_stm32f777xx.json
         INFO    - Run completed
