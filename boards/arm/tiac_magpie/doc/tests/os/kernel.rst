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

         INFO    - 169 test scenarios (169 configurations) selected, 71 configurations discarded due to filters.
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    -  72/169 tiac_magpie               tests/kernel/lifo/lifo_usage/kernel.lifo.usage     :bgn:`PASSED` (device 4.189s)
         INFO    -  73/169 tiac_magpie               tests/kernel/spinlock/kernel.multiprocessing.spinlock :byl:`SKIPPED` (runtime filter)
         INFO    -  74/169 tiac_magpie               tests/kernel/lifo/lifo_api/kernel.lifo             :bgn:`PASSED` (device 4.368s)
         INFO    -  75/169 tiac_magpie               tests/kernel/semaphore/semaphore/kernel.semaphore  :bgn:`PASSED` (device 17.661s)
         INFO    -  76/169 tiac_magpie               tests/kernel/semaphore/sys_sem/kernel.semaphore.usage :bgn:`PASSED` (device 5.346s)
         INFO    -  77/169 tiac_magpie               tests/kernel/mem_heap/k_heap_api/kernel.k_heap_api :bgn:`PASSED` (device 3.884s)
         INFO    -  78/169 tiac_magpie               tests/kernel/mem_heap/mheap_api_concept/kernel.memory_heap :bgn:`PASSED` (device 3.795s)
         INFO    -  79/169 tiac_magpie               tests/kernel/events/event_api/kernel.events        :bgn:`PASSED` (device 4.134s)
         INFO    -  80/169 tiac_magpie               tests/kernel/mem_slab/mslab_api/kernel.memory_slabs.api :bgn:`PASSED` (device 9.752s)
         INFO    -  81/169 tiac_magpie               tests/kernel/events/sys_event/kernel.events.usage  :bgn:`PASSED` (device 5.486s)
         INFO    -  82/169 tiac_magpie               tests/kernel/condvar/condvar_api/kernel.condvar    :bgn:`PASSED` (device 6.783s)
         INFO    -  83/169 tiac_magpie               tests/kernel/mem_slab/mslab/kernel.memory_slabs    :bgn:`PASSED` (device 4.562s)
         INFO    -  84/169 tiac_magpie               tests/kernel/mem_slab/mslab_threadsafe/kernel.memory_slabs.threadsafe :bgn:`PASSED` (device 3.627s)
         INFO    -  85/169 tiac_magpie               tests/kernel/mem_slab/mslab_concept/kernel.memory_slabs.concept :bgn:`PASSED` (device 5.615s)
         INFO    -  86/169 tiac_magpie               tests/kernel/profiling/profiling_api/kernel.common.profiling :bgn:`PASSED` (device 3.935s)
         INFO    -  87/169 tiac_magpie               tests/kernel/interrupt/arch.interrupt              :bgn:`PASSED` (device 3.704s)
         INFO    -  88/169 tiac_magpie               tests/kernel/device/kernel.device                  :bgn:`PASSED` (device 5.103s)
         INFO    -  89/169 tiac_magpie               tests/kernel/device/kernel.device.pm               :bgn:`PASSED` (device 5.117s)
         INFO    -  90/169 tiac_magpie               tests/kernel/sched/preempt/kernel.scheduler.preempt :bgn:`PASSED` (device 3.680s)
         INFO    -  91/169 tiac_magpie               tests/kernel/stack/stack/kernel.stack.usage        :bgn:`PASSED` (device 6.232s)
         INFO    -  92/169 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.dumb_no_timeslicing :bgn:`PASSED` (device 7.898s)
         INFO    -  93/169 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq_no_timeslicing :bgn:`PASSED` (device 7.738s)
         INFO    -  94/169 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq :bgn:`PASSED` (device 23.519s)
         INFO    -  95/169 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.no_timeslicing :bgn:`PASSED` (device 7.934s)
         INFO    -  96/169 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.slice_perthread :bgn:`PASSED` (device 24.012s)
         INFO    -  97/169 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler   :bgn:`PASSED` (device 23.756s)
         INFO    -  98/169 tiac_magpie               tests/kernel/sched/deadline/kernel.scheduler.deadline :bgn:`PASSED` (device 4.161s)
         INFO    -  99/169 tiac_magpie               tests/kernel/sched/metairq/kernel.scheduler.metairq :bgn:`PASSED` (device 3.636s)
         INFO    - 100/169 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`SKIPPED` (runtime filter)
         INFO    - 101/169 tiac_magpie               tests/kernel/fatal/message_capture/kernel.logging.message_capture :bgn:`PASSED` (device 2.598s)
         INFO    - 102/169 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_sentinel :bgn:`PASSED` (device 3.910s)
         INFO    - 103/169 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_no_userspace :bgn:`PASSED` (device 3.921s)
         INFO    - 104/169 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_arm_fpu_sharing :bgn:`PASSED` (device 6.195s)
         INFO    - 105/169 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection :bgn:`PASSED` (device 5.572s)
         INFO    - 106/169 tiac_magpie               tests/kernel/fpu_sharing/float_disable/kernel.fpu_sharing.float_disable.arm :bgn:`PASSED` (device 5.001s)
         INFO    - 107/169 tiac_magpie               tests/kernel/mbox/mbox_usage/kernel.mailbox.usage  :bgn:`PASSED` (device 3.636s)
         INFO    - 108/169 tiac_magpie               tests/kernel/poll/kernel.poll                      :bgn:`PASSED` (device 9.636s)
         INFO    - 109/169 tiac_magpie               tests/kernel/fifo/fifo_usage/kernel.fifo.usage     :bgn:`PASSED` (device 3.862s)
         INFO    - 110/169 tiac_magpie               tests/kernel/mbox/mbox_api/kernel.mailbox.api      :bgn:`PASSED` (device 4.250s)
         INFO    - 111/169 tiac_magpie               tests/kernel/fifo/fifo_timeout/kernel.fifo.timeout :bgn:`PASSED` (device 3.890s)
         INFO    - 112/169 tiac_magpie               tests/kernel/fifo/fifo_api/kernel.fifo             :bgn:`PASSED` (device 4.315s)
         INFO    - 113/169 tiac_magpie               tests/kernel/sleep/kernel.common.timing            :bgn:`PASSED` (device 8.088s)
         INFO    - 114/169 tiac_magpie               tests/kernel/mutex/sys_mutex/system.mutex.nouser   :bgn:`PASSED` (device 11.433s)
         INFO    - 115/169 tiac_magpie               tests/kernel/pipe/pipe_api/kernel.pipe.api         :bgn:`PASSED` (device 6.822s)
         INFO    - 116/169 tiac_magpie               tests/kernel/pipe/pipe/kernel.pipe                 :bgn:`PASSED` (device 7.081s)
         INFO    - 117/169 tiac_magpie               tests/kernel/mutex/sys_mutex/system.mutex          :bgn:`PASSED` (device 12.543s)
         INFO    - 118/169 tiac_magpie               tests/kernel/mutex/mutex_api/kernel.mutex          :bgn:`PASSED` (device 17.393s)
         INFO    - 119/169 tiac_magpie               tests/kernel/timer/timer_error_case/kernel.timer.error_case :bgn:`PASSED` (device 5.507s)
         INFO    - 120/169 tiac_magpie               tests/kernel/mutex/mutex_error_case/kernel.mutex_error_case :bgn:`PASSED` (device 5.280s)
         INFO    - 121/169 tiac_magpie               tests/kernel/timer/timer_monotonic/kernel.timer.monotonic :bgn:`PASSED` (device 5.069s)
         INFO    - 122/169 tiac_magpie               tests/kernel/xip/arch.common.xip                   :bgn:`PASSED` (device 3.687s)
         INFO    - 123/169 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer.tickless :bgn:`PASSED` (device 8.698s)
         INFO    - 124/169 tiac_magpie               tests/kernel/common/kernel.common.misra            :byl:`SKIPPED` (runtime filter)
         INFO    - 125/169 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer          :bgn:`PASSED` (device 8.714s)
         INFO    - 126/169 tiac_magpie               tests/kernel/common/kernel.common.nano64           :bgn:`PASSED` (device 11.946s)
         INFO    - 127/169 tiac_magpie               tests/kernel/common/kernel.common.nano32           :bgn:`PASSED` (device 12.160s)
         INFO    - 128/169 tiac_magpie               tests/kernel/common/kernel.common.tls              :bgn:`PASSED` (device 11.956s)
         INFO    - 129/169 tiac_magpie               tests/kernel/common/kernel.common                  :bgn:`PASSED` (device 11.799s)
         INFO    - 130/169 tiac_magpie               tests/kernel/queue/kernel.queue                    :bgn:`PASSED` (device 7.041s)
         INFO    - 131/169 tiac_magpie               tests/kernel/obj_tracking/kernel.objects.tracking  :bgn:`PASSED` (device 3.647s)
         INFO    - 132/169 tiac_magpie               tests/kernel/mem_protect/stack_random/kernel.memory_protection.stack_random :bgn:`PASSED` (device 3.602s)
         INFO    - 133/169 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64.coverage.exec :byl:`SKIPPED` (runtime filter)
         INFO    - 134/169 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64.coverage :byl:`SKIPPED` (runtime filter)
         INFO    - 135/169 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64 :byl:`SKIPPED` (runtime filter)
         INFO    - 136/169 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem.nouser :bgn:`PASSED` (device 4.559s)
         INFO    - 137/169 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map :byl:`SKIPPED` (runtime filter)
         INFO    - 138/169 tiac_magpie               tests/kernel/mem_protect/futex/kernel.futex        :bgn:`PASSED` (device 5.500s)
         INFO    - 139/169 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem :bgn:`PASSED` (device 5.877s)
         INFO    - 140/169 tiac_magpie               tests/kernel/mem_protect/protection/kernel.memory_protection.protection :bgn:`PASSED` (device 3.925s)
         INFO    - 141/169 tiac_magpie               tests/kernel/mem_protect/userspace/kernel.memory_protection.userspace :bgn:`PASSED` (device 6.546s)
         INFO    - 142/169 tiac_magpie               tests/kernel/mem_protect/demand_paging/kernel.demand_paging :byl:`SKIPPED` (runtime filter)
         INFO    - 143/169 tiac_magpie               tests/kernel/mem_protect/syscalls/kernel.memory_protection.syscalls :bgn:`PASSED` (device 20.196s)
         INFO    - 144/169 tiac_magpie               tests/kernel/mem_protect/mem_protect/kernel.memory_protection :bgn:`PASSED` (device 9.225s)
         INFO    - 145/169 tiac_magpie               tests/kernel/mem_protect/obj_validation/kernel.memory_protection.obj_validation :bgn:`PASSED` (device 5.056s)
         INFO    - 146/169 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.critical.sam :byl:`SKIPPED` (runtime filter)
         INFO    - 147/169 tiac_magpie               tests/kernel/workq/work_queue/kernel.workqueue     :bgn:`PASSED` (device 7.853s)
         INFO    - 148/169 tiac_magpie               tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot :bgn:`PASSED` (device 6.179s)
         INFO    - 149/169 tiac_magpie               tests/kernel/workq/work/kernel.work.api            :bgn:`PASSED` (device 6.065s)
         INFO    - 150/169 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.critical :bgn:`:bgn:`PASSED`` (device 3.954s)
         INFO    - 151/169 tiac_magpie               tests/kernel/threads/thread_stack/kernel.threads.armv8m_mpu_stack_guard :byl:`SKIPPED` (runtime filter)
         INFO    - 152/169 tiac_magpie               tests/kernel/early_sleep/kernel.common.sleep       :bgn:`:bgn:`PASSED`` (device 5.220s)
         INFO    - 153/169 tiac_magpie               tests/kernel/workq/user_work/kernel.work.user      :bgn:`:bgn:`PASSED`` (device 5.076s)
         INFO    - 154/169 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls        :bgn:`:bgn:`PASSED`` (device 4.170s)
         INFO    - 155/169 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls.userspace :bgn:`:bgn:`PASSED`` (device 5.621s)
         INFO    - 156/169 tiac_magpie               tests/kernel/threads/thread_apis/kernel.threads.apis.pinonly :byl:`SKIPPED` (runtime filter)
         INFO    - 157/169 tiac_magpie               tests/kernel/threads/thread_stack/kernel.threads.thread_stack :bgn:`:bgn:`PASSED`` (device 5.655s)
         INFO    - 158/169 tiac_magpie               tests/kernel/threads/thread_init/kernel.threads.init :bgn:`:bgn:`PASSED`` (device 8.878s)
         INFO    - 159/169 tiac_magpie               tests/kernel/threads/thread_error_case/kernel.threads.error.case :bgn:`:bgn:`PASSED`` (device 5.418s)
         INFO    - 160/169 tiac_magpie               tests/kernel/threads/dynamic_thread/kernel.threads.dynamic :bgn:`:bgn:`PASSED`` (device 5.949s)
         INFO    - 161/169 tiac_magpie               tests/kernel/threads/thread_apis/kernel.threads.apis :bgn:`:bgn:`PASSED`` (device 11.824s)
         INFO    - 162/169 tiac_magpie               tests/kernel/msgq/msgq_api/kernel.message_queue    :bgn:`:bgn:`PASSED`` (device 5.912s)
         INFO    - 163/169 tiac_magpie               tests/kernel/mp/kernel.multiprocessing             :byl:`SKIPPED` (runtime filter)
         INFO    - 164/169 tiac_magpie               tests/kernel/msgq/msgq_usage/kernel.message_queue_usage :bgn:`:bgn:`PASSED`` (device 4.729s)
         INFO    - 165/169 tiac_magpie               tests/kernel/smp/kernel.multiprocessing.smp        :byl:`SKIPPED` (runtime filter)
         INFO    - 166/169 tiac_magpie               tests/kernel/pending/kernel.objects                :bgn:`:bgn:`PASSED`` (device 9.742s)
         INFO    - 167/169 tiac_magpie               tests/kernel/usage/thread_runtime_stats/kernel.usage :bgn:`:bgn:`PASSED`` (device 3.639s)
         INFO    - 168/169 tiac_magpie               tests/kernel/tickless/tickless_concept/kernel.tickless.concept :bgn:`:bgn:`PASSED`` (device 5.052s)
         INFO    - 169/169 tiac_magpie               tests/kernel/context/kernel.context                :bgn:`:bgn:`PASSED`` (device 9.768s)

         INFO    - :bgn:`85 of 169` test configurations passed (100.00%), :bbk:`0` failed, :byl:`84` skipped with :bbk:`0` warnings in :bbk:`925.77 seconds`
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
