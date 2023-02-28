.. _tiac_magpie_kernel-tests:

Zephyr OS Kernel
################

Overview
********

See :zephyr_file:`tests/kernel`
for the original scope of tests, its structure and description.

.. _tiac_magpie_kernel-tests-requirements:

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

         $ ./zephyr/scripts/twister \
             --verbose --jobs 4 --inline-logs \
             --enable-size-report --platform-reports \
             --device-testing --hardware-map map.yaml \
             --board-root bridle/boards \
             --testsuite-root zephyr/tests/kernel

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    -  69/171 tiac_magpie               tests/kernel/mem_slab/mslab/kernel.memory_slabs    :bgn:`PASSED` (device 2.655s)
         INFO    -  70/171 tiac_magpie               tests/kernel/mem_slab/mslab_stats/kernel.memory_slab.stats :bgn:`PASSED` (device 2.576s)
         INFO    -  71/171 tiac_magpie               tests/kernel/mem_slab/mslab_threadsafe/kernel.memory_slabs.threadsafe :bgn:`PASSED` (device 3.203s)
         INFO    -  72/171 tiac_magpie               tests/kernel/pending/kernel.objects                :bgn:`PASSED` (device 9.647s)
         INFO    -  73/171 tiac_magpie               tests/kernel/mem_slab/mslab_api/kernel.memory_slabs.api :bgn:`PASSED` (device 10.293s)
         INFO    -  74/171 tiac_magpie               tests/kernel/mem_slab/mslab_concept/kernel.memory_slabs.concept :bgn:`PASSED` (device 5.664s)
         INFO    -  75/171 tiac_magpie               tests/kernel/stack/stack/kernel.stack.usage        :bgn:`PASSED` (device 4.774s)
         INFO    -  76/171 tiac_magpie               tests/kernel/semaphore/semaphore/kernel.semaphore  :bgn:`PASSED` (device 15.805s)
         INFO    -  77/171 tiac_magpie               tests/kernel/semaphore/sys_sem/kernel.semaphore.usage :bgn:`PASSED` (device 3.462s)
         INFO    -  78/171 tiac_magpie               tests/kernel/common/kernel.common.misra            :byl:`SKIPPED` (runtime filter)
         INFO    -  79/171 tiac_magpie               tests/kernel/common/kernel.common.picolibc         :bgn:`PASSED` (device 8.732s)
         INFO    -  80/171 tiac_magpie               tests/kernel/common/kernel.common.nano64           :bgn:`PASSED` (device 8.714s)
         INFO    -  81/171 tiac_magpie               tests/kernel/common/kernel.common.nano32           :bgn:`PASSED` (device 8.087s)
         INFO    -  82/171 tiac_magpie               tests/kernel/usage/thread_runtime_stats/kernel.usage :bgn:`PASSED` (device 2.640s)
         INFO    -  83/171 tiac_magpie               tests/kernel/spinlock/kernel.multiprocessing.spinlock :byl:`SKIPPED` (runtime filter)
         INFO    -  84/171 tiac_magpie               tests/kernel/common/kernel.common.tls              :bgn:`PASSED` (device 8.127s)
         INFO    -  85/171 tiac_magpie               tests/kernel/common/kernel.common                  :bgn:`PASSED` (device 10.068s)
         INFO    -  86/171 tiac_magpie               tests/kernel/mbox/mbox_api/kernel.mailbox.api      :bgn:`PASSED` (device 3.767s)
         INFO    -  87/171 tiac_magpie               tests/kernel/mbox/mbox_usage/kernel.mailbox.usage  :bgn:`PASSED` (device 3.797s)
         INFO    -  88/171 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.critical.sam :byl:`SKIPPED` (runtime filter)
         INFO    -  89/171 tiac_magpie               tests/kernel/tickless/tickless_concept/kernel.tickless.concept :bgn:`PASSED` (device 4.232s)
         INFO    -  90/171 tiac_magpie               tests/kernel/xip/arch.common.xip                   :bgn:`PASSED` (device 3.467s)
         INFO    -  91/171 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.critical :bgn:`PASSED` (device 4.021s)
         INFO    -  92/171 tiac_magpie               tests/kernel/workq/work/kernel.work.api            :bgn:`PASSED` (device 6.606s)
         INFO    -  93/171 tiac_magpie               tests/kernel/workq/work_queue/kernel.workqueue     :bgn:`PASSED` (device 8.339s)
         INFO    -  94/171 tiac_magpie               tests/kernel/profiling/profiling_api/kernel.common.profiling :bgn:`PASSED` (device 3.690s)
         INFO    -  95/171 tiac_magpie               tests/kernel/sched/preempt/kernel.scheduler.preempt :bgn:`PASSED` (device 2.755s)
         INFO    -  96/171 tiac_magpie               tests/kernel/workq/user_work/kernel.work.user      :bgn:`PASSED` (device 4.012s)
         INFO    -  97/171 tiac_magpie               tests/kernel/poll/kernel.poll                      :bgn:`PASSED` (device 7.582s)
         INFO    -  98/171 tiac_magpie               tests/kernel/sched/metairq/kernel.scheduler.metairq :bgn:`PASSED` (device 4.157s)
         INFO    -  99/171 tiac_magpie               tests/kernel/sched/deadline/kernel.scheduler.deadline :bgn:`PASSED` (device 3.704s)
         INFO    - 100/171 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.dumb_no_timeslicing :bgn:`PASSED` (device 5.686s)
         INFO    - 101/171 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq_no_timeslicing :bgn:`PASSED` (device 5.588s)
         INFO    - 102/171 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq :bgn:`PASSED` (device 22.032s)
         INFO    - 103/171 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.dumb_timeslicing :bgn:`PASSED` (device 21.361s)
         INFO    - 104/171 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.slice_perthread :bgn:`PASSED` (device 21.362s)
         INFO    - 105/171 tiac_magpie               tests/kernel/interrupt/arch.interrupt              :bgn:`PASSED` (device 2.652s)
         INFO    - 106/171 tiac_magpie               tests/kernel/smp/kernel.multiprocessing.smp        :byl:`SKIPPED` (runtime filter)
         INFO    - 107/171 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler   :bgn:`PASSED` (device 21.343s)
         INFO    - 108/171 tiac_magpie               tests/kernel/obj_tracking/kernel.objects.tracking  :bgn:`PASSED` (device 2.569s)
         INFO    - 109/171 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.no_timeslicing :bgn:`PASSED` (device 6.483s)
         INFO    - 110/171 tiac_magpie               tests/kernel/gen_isr_table/arch.interrupt.gen_isr_table.riscv_no_direct :byl:`SKIPPED` (runtime filter)
         INFO    - 111/171 tiac_magpie               tests/kernel/gen_isr_table/arch.interrupt.gen_isr_table.riscv_direct :byl:`SKIPPED` (runtime filter)
         INFO    - 112/171 tiac_magpie               tests/kernel/queue/kernel.queue                    :bgn:`PASSED` (device 5.864s)
         INFO    - 113/171 tiac_magpie               tests/kernel/sleep/kernel.common.timing            :bgn:`PASSED` (device 7.271s)
         INFO    - 114/171 tiac_magpie               tests/kernel/timer/timer_behavior/kernel.timer.timer :bgn:`PASSED` (device 23.006s)
         INFO    - 115/171 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer.tickless :bgn:`PASSED` (device 6.790s)
         INFO    - 116/171 tiac_magpie               tests/kernel/cache/kernel.cache.api                :byl:`SKIPPED` (runtime filter)
         INFO    - 117/171 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer          :bgn:`PASSED` (device 7.620s)
         INFO    - 118/171 tiac_magpie               tests/kernel/timer/timer_error_case/kernel.timer.error_case :bgn:`PASSED` (device 3.865s)
         INFO    - 119/171 tiac_magpie               tests/kernel/timer/timer_monotonic/kernel.timer.monotonic :bgn:`PASSED` (device 4.785s)
         INFO    - 120/171 tiac_magpie               tests/kernel/mem_heap/mheap_api_concept/kernel.memory_heap :bgn:`PASSED` (device 4.315s)
         INFO    - 121/171 tiac_magpie               tests/kernel/mem_heap/k_heap_api/kernel.k_heap_api :bgn:`PASSED` (device 2.867s)
         INFO    - 122/171 tiac_magpie               tests/kernel/fifo/fifo_usage/kernel.fifo.usage     :bgn:`PASSED` (device 3.274s)
         INFO    - 123/171 tiac_magpie               tests/kernel/fpu_sharing/float_disable/kernel.fpu_sharing.float_disable :bgn:`PASSED` (device 3.962s)
         INFO    - 124/171 tiac_magpie               tests/kernel/fifo/fifo_api/kernel.fifo             :bgn:`PASSED` (device 5.519s)
         INFO    - 125/171 tiac_magpie               tests/kernel/fifo/fifo_timeout/kernel.fifo.timeout :bgn:`PASSED` (device 2.856s)
         INFO    - 126/171 tiac_magpie               tests/kernel/early_sleep/kernel.common.sleep       :bgn:`PASSED` (device 4.722s)
         INFO    - 127/171 tiac_magpie               tests/kernel/threads/thread_apis/kernel.threads.apis.pinonly :byl:`SKIPPED` (runtime filter)
         INFO    - 128/171 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls        :bgn:`PASSED` (device 4.206s)
         INFO    - 129/171 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls.userspace :bgn:`PASSED` (device 3.740s)
         INFO    - 130/171 tiac_magpie               tests/kernel/threads/thread_apis/kernel.threads.apis :bgn:`PASSED` (device 10.360s)
         INFO    - 131/171 tiac_magpie               tests/kernel/threads/thread_stack/kernel.threads.armv8m_mpu_stack_guard :byl:`SKIPPED` (runtime filter)
         INFO    - 132/171 tiac_magpie               tests/kernel/threads/thread_init/kernel.threads.init :bgn:`PASSED` (device 7.278s)
         INFO    - 133/171 tiac_magpie               tests/kernel/threads/dynamic_thread/kernel.threads.dynamic :bgn:`PASSED` (device 5.028s)
         INFO    - 134/171 tiac_magpie               tests/kernel/threads/thread_error_case/kernel.threads.error.case :bgn:`PASSED` (device 3.935s)
         INFO    - 135/171 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`SKIPPED` (runtime filter)
         INFO    - 136/171 tiac_magpie               tests/kernel/fatal/message_capture/kernel.logging.message_capture :bgn:`PASSED` (device 2.368s)
         INFO    - 137/171 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_sentinel :bgn:`PASSED` (device 2.867s)
         INFO    - 138/171 tiac_magpie               tests/kernel/threads/thread_stack/kernel.threads.thread_stack :bgn:`PASSED` (device 5.431s)
         INFO    - 139/171 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_no_userspace :bgn:`PASSED` (device 3.580s)
         INFO    - 140/171 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_arm_fpu_sharing :bgn:`PASSED` (device 4.408s)
         INFO    - 141/171 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection :bgn:`PASSED` (device 3.682s)
         INFO    - 142/171 tiac_magpie               tests/kernel/device/kernel.device.pm               :bgn:`PASSED` (device 4.426s)
         INFO    - 143/171 tiac_magpie               tests/kernel/device/kernel.device                  :bgn:`PASSED` (device 4.329s)
         INFO    - 144/171 tiac_magpie               tests/kernel/msgq/msgq_usage/kernel.message_queue_usage :bgn:`PASSED` (device 4.553s)
         INFO    - 145/171 tiac_magpie               tests/kernel/msgq/msgq_api/kernel.message_queue    :bgn:`PASSED` (device 5.113s)
         INFO    - 146/171 tiac_magpie               tests/kernel/mp/kernel.multiprocessing             :byl:`SKIPPED` (runtime filter)
         INFO    - 147/171 tiac_magpie               tests/kernel/condvar/condvar_api/kernel.condvar    :bgn:`PASSED` (device 5.091s)
         INFO    - 148/171 tiac_magpie               tests/kernel/pipe/pipe_api/kernel.pipe.api         :bgn:`PASSED` (device 6.233s)
         INFO    - 149/171 tiac_magpie               tests/kernel/pipe/pipe/kernel.pipe                 :bgn:`PASSED` (device 6.211s)
         INFO    - 150/171 tiac_magpie               tests/kernel/events/event_api/kernel.events        :bgn:`PASSED` (device 3.811s)
         INFO    - 151/171 tiac_magpie               tests/kernel/lifo/lifo_usage/kernel.lifo.usage     :bgn:`PASSED` (device 3.938s)
         INFO    - 152/171 tiac_magpie               tests/kernel/events/sys_event/kernel.events.usage  :bgn:`PASSED` (device 4.206s)
         INFO    - 153/171 tiac_magpie               tests/kernel/lifo/lifo_api/kernel.lifo             :bgn:`PASSED` (device 4.486s)
         INFO    - 154/171 tiac_magpie               tests/kernel/mem_protect/protection/kernel.memory_protection.protection :bgn:`PASSED` (device 4.108s)
         INFO    - 155/171 tiac_magpie               tests/kernel/mem_protect/stack_random/kernel.memory_protection.stack_random :bgn:`PASSED` (device 4.072s)
         INFO    - 156/171 tiac_magpie               tests/kernel/mem_protect/obj_validation/kernel.memory_protection.obj_validation :bgn:`PASSED` (device 4.135s)
         INFO    - 157/171 tiac_magpie               tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot :bgn:`PASSED` (device 4.938s)
         INFO    - 158/171 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem.nouser :bgn:`PASSED` (device 3.412s)
         INFO    - 159/171 tiac_magpie               tests/kernel/mem_protect/syscalls/kernel.memory_protection.syscalls :bgn:`PASSED` (device 19.254s)
         INFO    - 160/171 tiac_magpie               tests/kernel/mem_protect/demand_paging/kernel.demand_paging :byl:`SKIPPED` (runtime filter)
         INFO    - 161/171 tiac_magpie               tests/kernel/mem_protect/futex/kernel.futex        :bgn:`PASSED` (device 3.738s)
         INFO    - 162/171 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64 :byl:`SKIPPED` (runtime filter)
         INFO    - 163/171 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem :bgn:`PASSED` (device 4.165s)
         INFO    - 164/171 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map :byl:`SKIPPED` (runtime filter)
         INFO    - 165/171 tiac_magpie               tests/kernel/mem_protect/mem_protect/kernel.memory_protection :bgn:`PASSED` (device 8.116s)
         INFO    - 166/171 tiac_magpie               tests/kernel/mutex/sys_mutex/system.mutex.nouser   :bgn:`PASSED` (device 10.821s)
         INFO    - 167/171 tiac_magpie               tests/kernel/mem_protect/userspace/kernel.memory_protection.userspace :bgn:`PASSED` (device 5.338s)
         INFO    - 168/171 tiac_magpie               tests/kernel/mutex/sys_mutex/system.mutex          :bgn:`PASSED` (device 11.663s)
         INFO    - 169/171 tiac_magpie               tests/kernel/context/kernel.context                :bgn:`PASSED` (device 8.163s)
         INFO    - 170/171 tiac_magpie               tests/kernel/mutex/mutex_error_case/kernel.mutex_error_case :bgn:`PASSED` (device 3.643s)
         INFO    - 171/171 tiac_magpie               tests/kernel/mutex/mutex_api/kernel.mutex          :bgn:`PASSED` (device 15.520s)

         INFO    - 171 test scenarios (171 test instances) selected, 82 configurations skipped (68 by static filter, 14 at runtime).
         INFO    - :bgn:`89 of 171` test configurations passed (100.00%), :bbk:`0` failed, :byl:`82` skipped with :bbk:`0` warnings in :bbk:`1196.47 seconds`
         INFO    - In total 1033 test cases were executed, 533 skipped on 1 out of total 541 platforms (0.18%)
         INFO    - :bgn:`89` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|        89 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
