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
             --verbose --jobs 1 --inline-logs \
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

         INFO    - 169 test scenarios (169 configurations) selected, 71 configurations discarded due to filters.
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    -  72/169 tiac_magpie               tests/kernel/pending/kernel.objects                :bgn:`PASSED` (device 10.186s)
         INFO    -  73/169 tiac_magpie               tests/kernel/mem_slab/mslab/kernel.memory_slabs    :bgn:`PASSED` (device 3.972s)
         INFO    -  74/169 tiac_magpie               tests/kernel/mem_slab/mslab_threadsafe/kernel.memory_slabs.threadsafe :bgn:`PASSED` (device 4.034s)
         INFO    -  75/169 tiac_magpie               tests/kernel/mem_slab/mslab_api/kernel.memory_slabs.api :bgn:`PASSED` (device 10.244s)
         INFO    -  76/169 tiac_magpie               tests/kernel/mem_slab/mslab_concept/kernel.memory_slabs.concept :bgn:`PASSED` (device 6.070s)
         INFO    -  77/169 tiac_magpie               tests/kernel/stack/stack/kernel.stack.usage        :bgn:`PASSED` (device 6.957s)
         INFO    -  78/169 tiac_magpie               tests/kernel/semaphore/semaphore/kernel.semaphore  :bgn:`PASSED` (device 18.611s)
         INFO    -  79/169 tiac_magpie               tests/kernel/semaphore/sys_sem/kernel.semaphore.usage :bgn:`PASSED` (device 5.615s)
         INFO    -  80/169 tiac_magpie               tests/kernel/common/kernel.common.nano64           :bgn:`PASSED` (device 13.724s)
         INFO    -  81/169 tiac_magpie               tests/kernel/common/kernel.common.nano32           :bgn:`PASSED` (device 13.921s)
         INFO    -  82/169 tiac_magpie               tests/kernel/common/kernel.common.misra            :byl:`SKIPPED` (runtime filter)
         INFO    -  83/169 tiac_magpie               tests/kernel/common/kernel.common.tls              :bgn:`PASSED` (device 13.843s)
         INFO    -  84/169 tiac_magpie               tests/kernel/common/kernel.common                  :bgn:`PASSED` (device 13.661s)
         INFO    -  85/169 tiac_magpie               tests/kernel/usage/thread_runtime_stats/kernel.usage :bgn:`PASSED` (device 4.303s)
         INFO    -  86/169 tiac_magpie               tests/kernel/spinlock/kernel.multiprocessing.spinlock :byl:`SKIPPED` (runtime filter)
         INFO    -  87/169 tiac_magpie               tests/kernel/mbox/mbox_api/kernel.mailbox.api      :bgn:`PASSED` (device 4.758s)
         INFO    -  88/169 tiac_magpie               tests/kernel/mbox/mbox_usage/kernel.mailbox.usage  :bgn:`PASSED` (device 4.113s)
         INFO    -  89/169 tiac_magpie               tests/kernel/tickless/tickless_concept/kernel.tickless.concept :bgn:`PASSED` (device 5.168s)
         INFO    -  90/169 tiac_magpie               tests/kernel/xip/arch.common.xip                   :bgn:`PASSED` (device 4.035s)
         INFO    -  91/169 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.critical.sam :byl:`SKIPPED` (runtime filter)
         INFO    -  92/169 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.critical :bgn:`PASSED` (device 4.234s)
         INFO    -  93/169 tiac_magpie               tests/kernel/workq/work/kernel.work.api            :bgn:`PASSED` (device 6.530s)
         INFO    -  94/169 tiac_magpie               tests/kernel/workq/work_queue/kernel.workqueue     :bgn:`PASSED` (device 8.313s)
         INFO    -  95/169 tiac_magpie               tests/kernel/workq/user_work/kernel.work.user      :bgn:`PASSED` (device 5.623s)
         INFO    -  96/169 tiac_magpie               tests/kernel/poll/kernel.poll                      :bgn:`PASSED` (device 10.237s)
         INFO    -  97/169 tiac_magpie               tests/kernel/profiling/profiling_api/kernel.common.profiling :bgn:`PASSED` (device 4.398s)
         INFO    -  98/169 tiac_magpie               tests/kernel/sched/preempt/kernel.scheduler.preempt :bgn:`PASSED` (device 3.977s)
         INFO    -  99/169 tiac_magpie               tests/kernel/sched/metairq/kernel.scheduler.metairq :bgn:`PASSED` (device 4.087s)
         INFO    - 100/169 tiac_magpie               tests/kernel/sched/deadline/kernel.scheduler.deadline :bgn:`PASSED` (device 4.390s)
         INFO    - 101/169 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.dumb_no_timeslicing :bgn:`PASSED` (device 8.358s)
         INFO    - 102/169 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq_no_timeslicing :bgn:`PASSED` (device 8.519s)
         INFO    - 103/169 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq :bgn:`PASSED` (device 24.815s)
         INFO    - 104/169 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.slice_perthread :bgn:`PASSED` (device 24.332s)
         INFO    - 105/169 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.no_timeslicing :bgn:`PASSED` (device 8.796s)
         INFO    - 106/169 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler   :bgn:`PASSED` (device 24.127s)
         INFO    - 107/169 tiac_magpie               tests/kernel/interrupt/arch.interrupt              :bgn:`PASSED` (device 4.157s)
         INFO    - 108/169 tiac_magpie               tests/kernel/smp/kernel.multiprocessing.smp        :byl:`SKIPPED` (runtime filter)
         INFO    - 109/169 tiac_magpie               tests/kernel/obj_tracking/kernel.objects.tracking  :bgn:`PASSED` (device 4.304s)
         INFO    - 110/169 tiac_magpie               tests/kernel/queue/kernel.queue                    :bgn:`PASSED` (device 7.830s)
         INFO    - 111/169 tiac_magpie               tests/kernel/sleep/kernel.common.timing            :bgn:`PASSED` (device 8.558s)
         INFO    - 112/169 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer.tickless :bgn:`PASSED` (device 8.989s)
         INFO    - 113/169 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer          :bgn:`PASSED` (device 9.065s)
         INFO    - 114/169 tiac_magpie               tests/kernel/timer/timer_error_case/kernel.timer.error_case :bgn:`PASSED` (device 6.194s)
         INFO    - 115/169 tiac_magpie               tests/kernel/timer/timer_monotonic/kernel.timer.monotonic :bgn:`PASSED` (device 5.393s)
         INFO    - 116/169 tiac_magpie               tests/kernel/fpu_sharing/float_disable/kernel.fpu_sharing.float_disable.arm :bgn:`PASSED` (device 5.685s)
         INFO    - 117/169 tiac_magpie               tests/kernel/mem_heap/mheap_api_concept/kernel.memory_heap :bgn:`PASSED` (device 4.237s)
         INFO    - 118/169 tiac_magpie               tests/kernel/mem_heap/k_heap_api/kernel.k_heap_api :bgn:`PASSED` (device 4.207s)
         INFO    - 119/169 tiac_magpie               tests/kernel/fifo/fifo_usage/kernel.fifo.usage     :bgn:`PASSED` (device 4.042s)
         INFO    - 120/169 tiac_magpie               tests/kernel/fifo/fifo_api/kernel.fifo             :bgn:`PASSED` (device 4.668s)
         INFO    - 121/169 tiac_magpie               tests/kernel/fifo/fifo_timeout/kernel.fifo.timeout :bgn:`PASSED` (device 4.305s)
         INFO    - 122/169 tiac_magpie               tests/kernel/early_sleep/kernel.common.sleep       :bgn:`PASSED` (device 5.584s)
         INFO    - 123/169 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls.userspace :bgn:`PASSED` (device 6.166s)
         INFO    - 124/169 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls        :bgn:`PASSED` (device 4.455s)
         INFO    - 125/169 tiac_magpie               tests/kernel/threads/thread_apis/kernel.threads.apis.pinonly :byl:`SKIPPED` (runtime filter)
         INFO    - 126/169 tiac_magpie               tests/kernel/threads/thread_apis/kernel.threads.apis :bgn:`PASSED` (device 12.609s)
         INFO    - 127/169 tiac_magpie               tests/kernel/threads/dynamic_thread/kernel.threads.dynamic :bgn:`PASSED` (device 6.553s)
         INFO    - 128/169 tiac_magpie               tests/kernel/threads/thread_init/kernel.threads.init :bgn:`PASSED` (device 9.464s)
         INFO    - 129/169 tiac_magpie               tests/kernel/threads/thread_error_case/kernel.threads.error.case :bgn:`PASSED` (device 6.060s)
         INFO    - 130/169 tiac_magpie               tests/kernel/threads/thread_stack/kernel.threads.armv8m_mpu_stack_guard :byl:`SKIPPED` (runtime filter)
         INFO    - 131/169 tiac_magpie               tests/kernel/threads/thread_stack/kernel.threads.thread_stack :bgn:`PASSED` (device 6.012s)
         INFO    - 132/169 tiac_magpie               tests/kernel/fatal/message_capture/kernel.logging.message_capture :bgn:`PASSED` (device 2.671s)
         INFO    - 133/169 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_sentinel :bgn:`PASSED` (device 4.415s)
         INFO    - 134/169 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`SKIPPED` (runtime filter)
         INFO    - 135/169 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_arm_fpu_sharing :bgn:`PASSED` (device 6.885s)
         INFO    - 136/169 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_no_userspace :bgn:`PASSED` (device 4.406s)
         INFO    - 137/169 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection :bgn:`PASSED` (device 5.962s)
         INFO    - 138/169 tiac_magpie               tests/kernel/device/kernel.device.pm               :bgn:`PASSED` (device 5.766s)
         INFO    - 139/169 tiac_magpie               tests/kernel/device/kernel.device                  :bgn:`PASSED` (device 5.774s)
         INFO    - 140/169 tiac_magpie               tests/kernel/msgq/msgq_api/kernel.message_queue    :bgn:`PASSED` (device 6.421s)
         INFO    - 141/169 tiac_magpie               tests/kernel/msgq/msgq_usage/kernel.message_queue_usage :bgn:`PASSED` (device 5.323s)
         INFO    - 142/169 tiac_magpie               tests/kernel/condvar/condvar_api/kernel.condvar    :bgn:`PASSED` (device 7.697s)
         INFO    - 143/169 tiac_magpie               tests/kernel/pipe/pipe_api/kernel.pipe.api         :bgn:`PASSED` (device 7.219s)
         INFO    - 144/169 tiac_magpie               tests/kernel/pipe/pipe/kernel.pipe                 :bgn:`PASSED` (device 7.830s)
         INFO    - 145/169 tiac_magpie               tests/kernel/mp/kernel.multiprocessing             :byl:`SKIPPED` (runtime filter)
         INFO    - 146/169 tiac_magpie               tests/kernel/events/sys_event/kernel.events.usage  :bgn:`PASSED` (device 5.577s)
         INFO    - 147/169 tiac_magpie               tests/kernel/events/event_api/kernel.events        :bgn:`PASSED` (device 4.498s)
         INFO    - 148/169 tiac_magpie               tests/kernel/lifo/lifo_usage/kernel.lifo.usage     :bgn:`PASSED` (device 4.666s)
         INFO    - 149/169 tiac_magpie               tests/kernel/lifo/lifo_api/kernel.lifo             :bgn:`PASSED` (device 4.908s)
         INFO    - 150/169 tiac_magpie               tests/kernel/mem_protect/obj_validation/kernel.memory_protection.obj_validation :bgn:`PASSED` (device 5.431s)
         INFO    - 151/169 tiac_magpie               tests/kernel/mem_protect/protection/kernel.memory_protection.protection :bgn:`PASSED` (device 4.433s)
         INFO    - 152/169 tiac_magpie               tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot :bgn:`PASSED` (device 7.179s)
         INFO    - 153/169 tiac_magpie               tests/kernel/mem_protect/stack_random/kernel.memory_protection.stack_random :bgn:`PASSED` (device 3.937s)
         INFO    - 154/169 tiac_magpie               tests/kernel/mem_protect/syscalls/kernel.memory_protection.syscalls :bgn:`PASSED` (device 20.978s)
         INFO    - 155/169 tiac_magpie               tests/kernel/mem_protect/futex/kernel.futex        :bgn:`PASSED` (device 6.018s)
         INFO    - 156/169 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem.nouser :bgn:`PASSED` (device 4.920s)
         INFO    - 157/169 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem :bgn:`PASSED` (device 6.411s)
         INFO    - 158/169 tiac_magpie               tests/kernel/mem_protect/mem_protect/kernel.memory_protection :bgn:`PASSED` (device 9.823s)
         INFO    - 159/169 tiac_magpie               tests/kernel/mem_protect/demand_paging/kernel.demand_paging :byl:`SKIPPED` (runtime filter)
         INFO    - 160/169 tiac_magpie               tests/kernel/mem_protect/userspace/kernel.memory_protection.userspace :bgn:`PASSED` (device 7.120s)
         INFO    - 161/169 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64.coverage.exec :byl:`SKIPPED` (runtime filter)
         INFO    - 162/169 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64.coverage :byl:`SKIPPED` (runtime filter)
         INFO    - 163/169 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64 :byl:`SKIPPED` (runtime filter)
         INFO    - 164/169 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map :byl:`SKIPPED` (runtime filter)
         INFO    - 165/169 tiac_magpie               tests/kernel/mutex/sys_mutex/system.mutex.nouser   :bgn:`PASSED` (device 11.827s)
         INFO    - 166/169 tiac_magpie               tests/kernel/mutex/sys_mutex/system.mutex          :bgn:`PASSED` (device 13.038s)
         INFO    - 167/169 tiac_magpie               tests/kernel/mutex/mutex_api/kernel.mutex          :bgn:`PASSED` (device 17.460s)
         INFO    - 168/169 tiac_magpie               tests/kernel/mutex/mutex_error_case/kernel.mutex_error_case :bgn:`PASSED` (device 5.931s)
         INFO    - 169/169 tiac_magpie               tests/kernel/context/kernel.context                :bgn:`PASSED` (device 9.684s)

         INFO    - :bgn:`85 of 169` test configurations passed (100.00%), :bbk:`0` failed, :byl:`84` skipped with :bbk:`0` warnings in :bbk:`4902.98 seconds`
         INFO    - In total 1476 test cases were executed, 201 skipped on 1 out of total 457 platforms (0.22%)
         INFO    - :bgn:`85` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|        85 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Using 'zephyr' toolchain.
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
