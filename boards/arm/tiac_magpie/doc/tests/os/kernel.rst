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

         INFO    - 174 test scenarios (174 configurations) selected, 73 configurations discarded due to filters.
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    -  74/174 tiac_magpie               tests/kernel/mem_slab/mslab_stats/kernel.memory_slab.stats :bgn:`PASSED` (device 3.338s)
         INFO    -  75/174 tiac_magpie               tests/kernel/pending/kernel.objects                :bgn:`PASSED` (device 9.364s)
         INFO    -  76/174 tiac_magpie               tests/kernel/mem_slab/mslab_api/kernel.memory_slabs.api :bgn:`PASSED` (device 9.473s)
         INFO    -  77/174 tiac_magpie               tests/kernel/mem_slab/mslab_threadsafe/kernel.memory_slabs.threadsafe :bgn:`PASSED` (device 3.254s)
         INFO    -  78/174 tiac_magpie               tests/kernel/mem_slab/mslab_concept/kernel.memory_slabs.concept :bgn:`PASSED` (device 5.331s)
         INFO    -  79/174 tiac_magpie               tests/kernel/mem_slab/mslab/kernel.memory_slabs    :bgn:`PASSED` (device 3.501s)
         INFO    -  80/174 tiac_magpie               tests/kernel/stack/stack/kernel.stack.usage        :bgn:`PASSED` (device 6.113s)
         INFO    -  81/174 tiac_magpie               tests/kernel/semaphore/semaphore/kernel.semaphore  :bgn:`PASSED` (device 17.649s)
         INFO    -  82/174 tiac_magpie               tests/kernel/semaphore/sys_sem/kernel.semaphore.usage :bgn:`PASSED` (device 4.650s)
         INFO    -  83/174 tiac_magpie               tests/kernel/common/kernel.common.misra            :byl:`SKIPPED` (runtime filter)
         INFO    -  84/174 tiac_magpie               tests/kernel/common/kernel.common.picolibc         :bgn:`PASSED` (device 11.465s)
         INFO    -  85/174 tiac_magpie               tests/kernel/common/kernel.common.nano64           :bgn:`PASSED` (device 11.444s)
         INFO    -  86/174 tiac_magpie               tests/kernel/common/kernel.common.nano32           :bgn:`PASSED` (device 10.845s)
         INFO    -  87/174 tiac_magpie               tests/kernel/usage/thread_runtime_stats/kernel.usage :bgn:`PASSED` (device 3.388s)
         INFO    -  88/174 tiac_magpie               tests/kernel/spinlock/kernel.multiprocessing.spinlock :byl:`SKIPPED` (runtime filter)
         INFO    -  89/174 tiac_magpie               tests/kernel/common/kernel.common.tls              :bgn:`PASSED` (device 10.898s)
         INFO    -  90/174 tiac_magpie               tests/kernel/mbox/mbox_api/kernel.mailbox.api      :bgn:`PASSED` (device 3.977s)
         INFO    -  91/174 tiac_magpie               tests/kernel/mbox/mbox_usage/kernel.mailbox.usage  :bgn:`PASSED` (device 3.871s)
         INFO    -  92/174 tiac_magpie               tests/kernel/tickless/tickless_concept/kernel.tickless.concept :bgn:`PASSED` (device 4.330s)
         INFO    -  93/174 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.critical.sam :byl:`SKIPPED` (runtime filter)
         INFO    -  94/174 tiac_magpie               tests/kernel/common/kernel.common                  :bgn:`PASSED` (device 10.911s)
         INFO    -  95/174 tiac_magpie               tests/kernel/workq/work/kernel.work.api            :bgn:`PASSED` (device 5.598s)
         INFO    -  96/174 tiac_magpie               tests/kernel/xip/arch.common.xip                   :bgn:`PASSED` (device 3.344s)
         INFO    -  97/174 tiac_magpie               tests/kernel/workq/work_queue/kernel.workqueue     :bgn:`PASSED` (device 8.544s)
         INFO    -  98/174 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.critical :bgn:`PASSED` (device 3.626s)
         INFO    -  99/174 tiac_magpie               tests/kernel/profiling/profiling_api/kernel.common.profiling :bgn:`PASSED` (device 3.514s)
         INFO    - 100/174 tiac_magpie               tests/kernel/workq/user_work/kernel.work.user      :bgn:`PASSED` (device 4.420s)
         INFO    - 101/174 tiac_magpie               tests/kernel/sched/preempt/kernel.scheduler.preempt :bgn:`PASSED` (device 3.757s)
         INFO    - 102/174 tiac_magpie               tests/kernel/poll/kernel.poll                      :bgn:`PASSED` (device 8.229s)
         INFO    - 103/174 tiac_magpie               tests/kernel/sched/deadline/kernel.scheduler.deadline :bgn:`PASSED` (device 3.993s)
         INFO    - 104/174 tiac_magpie               tests/kernel/sched/metairq/kernel.scheduler.metairq :bgn:`PASSED` (device 3.947s)
         INFO    - 105/174 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.dumb_no_timeslicing :bgn:`PASSED` (device 7.065s)
         INFO    - 106/174 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.dumb_timeslicing :bgn:`PASSED` (device 22.999s)
         INFO    - 107/174 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.slice_perthread :bgn:`PASSED` (device 22.920s)
         INFO    - 108/174 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.no_timeslicing :bgn:`PASSED` (device 7.146s)
         INFO    - 109/174 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq :bgn:`PASSED` (device 22.912s)
         INFO    - 110/174 tiac_magpie               tests/kernel/smp/kernel.multiprocessing.smp        :byl:`SKIPPED` (runtime filter)
         INFO    - 111/174 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq_no_timeslicing :bgn:`PASSED` (device 7.076s)
         INFO    - 112/174 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler   :bgn:`PASSED` (device 22.941s)
         INFO    - 113/174 tiac_magpie               tests/kernel/obj_tracking/kernel.objects.tracking  :bgn:`PASSED` (device 3.279s)
         INFO    - 114/174 tiac_magpie               tests/kernel/gen_isr_table/arch.interrupt.gen_isr_table.riscv_no_direct :byl:`SKIPPED` (runtime filter)
         INFO    - 115/174 tiac_magpie               tests/kernel/queue/kernel.queue                    :bgn:`PASSED` (device 5.716s)
         INFO    - 116/174 tiac_magpie               tests/kernel/interrupt/arch.interrupt              :bgn:`PASSED` (device 3.458s)
         INFO    - 117/174 tiac_magpie               tests/kernel/gen_isr_table/arch.interrupt.gen_isr_table.riscv_direct :byl:`SKIPPED` (runtime filter)
         INFO    - 118/174 tiac_magpie               tests/kernel/timer/timer_behavior/kernel.timer.timer :bgn:`PASSED` (device 13.400s)
         INFO    - 119/174 tiac_magpie               tests/kernel/sleep/kernel.common.timing            :bgn:`PASSED` (device 7.398s)
         INFO    - 120/174 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer.tickless :bgn:`PASSED` (device 8.006s)
         INFO    - 121/174 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer          :bgn:`PASSED` (device 7.994s)
         INFO    - 122/174 tiac_magpie               tests/kernel/timer/timer_monotonic/kernel.timer.monotonic :bgn:`PASSED` (device 4.698s)
         INFO    - 123/174 tiac_magpie               tests/kernel/timer/timer_error_case/kernel.timer.error_case :bgn:`PASSED` (device 5.615s)
         INFO    - 124/174 tiac_magpie               tests/kernel/mem_heap/mheap_api_concept/kernel.memory_heap :bgn:`PASSED` (device 3.980s)
         INFO    - 125/174 tiac_magpie               tests/kernel/fpu_sharing/float_disable/kernel.fpu_sharing.float_disable.arm :bgn:`PASSED` (device 4.476s)
         INFO    - 126/174 tiac_magpie               tests/kernel/mem_heap/k_heap_api/kernel.k_heap_api :bgn:`PASSED` (device 3.703s)
         INFO    - 127/174 tiac_magpie               tests/kernel/fifo/fifo_usage/kernel.fifo.usage     :bgn:`PASSED` (device 3.307s)
         INFO    - 128/174 tiac_magpie               tests/kernel/fifo/fifo_api/kernel.fifo             :bgn:`PASSED` (device 4.347s)
         INFO    - 129/174 tiac_magpie               tests/kernel/fifo/fifo_timeout/kernel.fifo.timeout :bgn:`PASSED` (device 3.716s)
         INFO    - 130/174 tiac_magpie               tests/kernel/early_sleep/kernel.common.sleep       :bgn:`PASSED` (device 5.331s)
         INFO    - 131/174 tiac_magpie               tests/kernel/threads/thread_apis/kernel.threads.apis.pinonly :byl:`SKIPPED` (runtime filter)
         INFO    - 132/174 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls        :bgn:`PASSED` (device 4.303s)
         INFO    - 133/174 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls.userspace :bgn:`PASSED` (device 5.470s)
         INFO    - 134/174 tiac_magpie               tests/kernel/threads/dynamic_thread/kernel.threads.dynamic :bgn:`PASSED` (device 5.683s)
         INFO    - 135/174 tiac_magpie               tests/kernel/threads/thread_stack/kernel.threads.armv8m_mpu_stack_guard :byl:`SKIPPED` (runtime filter)
         INFO    - 136/174 tiac_magpie               tests/kernel/threads/thread_apis/kernel.threads.apis :bgn:`PASSED` (device 11.233s)
         INFO    - 137/174 tiac_magpie               tests/kernel/threads/thread_init/kernel.threads.init :bgn:`PASSED` (device 8.543s)
         INFO    - 138/174 tiac_magpie               tests/kernel/fatal/message_capture/kernel.logging.message_capture :bgn:`PASSED` (device 2.346s)
         INFO    - 139/174 tiac_magpie               tests/kernel/threads/thread_error_case/kernel.threads.error.case :bgn:`PASSED` (device 5.000s)
         INFO    - 140/174 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`SKIPPED` (runtime filter)
         INFO    - 141/174 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_sentinel :bgn:`PASSED` (device 3.608s)
         INFO    - 142/174 tiac_magpie               tests/kernel/threads/thread_stack/kernel.threads.thread_stack :bgn:`PASSED` (device 5.089s)
         INFO    - 143/174 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_no_userspace :bgn:`PASSED` (device 3.612s)
         INFO    - 144/174 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_arm_fpu_sharing :bgn:`PASSED` (device 5.613s)
         INFO    - 145/174 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection :bgn:`PASSED` (device 4.932s)
         INFO    - 146/174 tiac_magpie               tests/kernel/device/kernel.device                  :bgn:`PASSED` (device 5.184s)
         INFO    - 147/174 tiac_magpie               tests/kernel/device/kernel.device.pm               :bgn:`PASSED` (device 5.289s)
         INFO    - 148/174 tiac_magpie               tests/kernel/msgq/msgq_usage/kernel.message_queue_usage :bgn:`PASSED` (device 4.836s)
         INFO    - 149/174 tiac_magpie               tests/kernel/msgq/msgq_api/kernel.message_queue    :bgn:`PASSED` (device 5.629s)
         INFO    - 150/174 tiac_magpie               tests/kernel/mp/kernel.multiprocessing             :byl:`SKIPPED` (runtime filter)
         INFO    - 151/174 tiac_magpie               tests/kernel/condvar/condvar_api/kernel.condvar    :bgn:`PASSED` (device 6.245s)
         INFO    - 152/174 tiac_magpie               tests/kernel/pipe/pipe_api/kernel.pipe.api         :bgn:`PASSED` (device 6.978s)
         INFO    - 153/174 tiac_magpie               tests/kernel/pipe/pipe/kernel.pipe                 :bgn:`PASSED` (device 7.104s)
         INFO    - 154/174 tiac_magpie               tests/kernel/events/event_api/kernel.events        :bgn:`PASSED` (device 4.055s)
         INFO    - 155/174 tiac_magpie               tests/kernel/lifo/lifo_usage/kernel.lifo.usage     :bgn:`PASSED` (device 3.995s)
         INFO    - 156/174 tiac_magpie               tests/kernel/events/sys_event/kernel.events.usage  :bgn:`PASSED` (device 4.878s)
         INFO    - 157/174 tiac_magpie               tests/kernel/lifo/lifo_api/kernel.lifo             :bgn:`PASSED` (device 4.048s)
         INFO    - 158/174 tiac_magpie               tests/kernel/mem_protect/protection/kernel.memory_protection.protection :bgn:`PASSED` (device 3.663s)
         INFO    - 159/174 tiac_magpie               tests/kernel/mem_protect/stack_random/kernel.memory_protection.stack_random :bgn:`PASSED` (device 4.025s)
         INFO    - 160/174 tiac_magpie               tests/kernel/mem_protect/obj_validation/kernel.memory_protection.obj_validation :bgn:`PASSED` (device 4.381s)
         INFO    - 161/174 tiac_magpie               tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot :bgn:`PASSED` (device 5.511s)
         INFO    - 162/174 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem.nouser :bgn:`PASSED` (device 4.237s)
         INFO    - 163/174 tiac_magpie               tests/kernel/mem_protect/syscalls/kernel.memory_protection.syscalls :bgn:`PASSED` (device 20.298s)
         INFO    - 164/174 tiac_magpie               tests/kernel/mem_protect/demand_paging/kernel.demand_paging :byl:`SKIPPED` (runtime filter)
         INFO    - 165/174 tiac_magpie               tests/kernel/mem_protect/futex/kernel.futex        :bgn:`PASSED` (device 4.958s)
         INFO    - 166/174 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map :byl:`SKIPPED` (runtime filter)
         INFO    - 167/174 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem :bgn:`PASSED` (device 5.345s)
         INFO    - 168/174 tiac_magpie               tests/kernel/mem_protect/mem_protect/kernel.memory_protection :bgn:`PASSED` (device 9.006s)
         INFO    - 169/174 tiac_magpie               tests/kernel/mutex/sys_mutex/system.mutex.nouser   :bgn:`PASSED` (device 10.894s)
         INFO    - 170/174 tiac_magpie               tests/kernel/mem_protect/userspace/kernel.memory_protection.userspace :bgn:`PASSED` (device 6.403s)
         INFO    - 171/174 tiac_magpie               tests/kernel/mutex/sys_mutex/system.mutex          :bgn:`PASSED` (device 12.271s)
         INFO    - 172/174 tiac_magpie               tests/kernel/mutex/mutex_api/kernel.mutex          :bgn:`PASSED` (device 16.553s)
         INFO    - 173/174 tiac_magpie               tests/kernel/mutex/mutex_error_case/kernel.mutex_error_case :bgn:`PASSED` (device 4.970s)
         INFO    - 174/174 tiac_magpie               tests/kernel/context/kernel.context                :bgn:`PASSED` (device 8.988s)

         INFO    - :bgn:`89 of 174` test configurations passed (100.00%), :bbk:`0` failed, :byl:`85` skipped with :bbk:`0` warnings in :bbk:`802.40 seconds`
         INFO    - In total 871 test cases were executed, 110 skipped on 1 out of total 501 platforms (0.20%)
         INFO    - :bgn:`89` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|        89 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Using 'zephyr' toolchain.
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
