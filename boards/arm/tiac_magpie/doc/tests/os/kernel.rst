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
             --testcase-root zephyr/tests/kernel

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - 167 test scenarios (167 configurations) selected, 71 configurations discarded due to filters.
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    -  1/96 tiac_magpie               tests/kernel/pending/kernel.objects                :bgn:`PASSED` (device 10.088s)
         INFO    -  2/96 tiac_magpie               tests/kernel/mem_slab/mslab/kernel.memory_slabs.api :bgn:`PASSED` (device 4.050s)
         INFO    -  3/96 tiac_magpie               tests/kernel/mem_slab/mslab_api/kernel.memory_slabs.api :bgn:`PASSED` (device 9.853s)
         INFO    -  4/96 tiac_magpie               tests/kernel/mem_slab/mslab_threadsafe/kernel.memory_slabs.threadsafe :bgn:`PASSED` (device 3.684s)
         INFO    -  5/96 tiac_magpie               tests/kernel/mem_slab/mslab_concept/kernel.memory_slabs.concept :bgn:`PASSED` (device 5.803s)
         INFO    -  6/96 tiac_magpie               tests/kernel/stack/stack/kernel.stack.usage        :bgn:`PASSED` (device 6.501s)
         INFO    -  7/96 tiac_magpie               tests/kernel/semaphore/semaphore/kernel.semaphore  :bgn:`PASSED` (device 17.921s)
         INFO    -  8/96 tiac_magpie               tests/kernel/common/kernel.common.misra            :byl:`SKIPPED` (filter)
         INFO    -  9/96 tiac_magpie               tests/kernel/semaphore/sys_sem/kernel.semaphore.usage :bgn:`PASSED` (device 5.450s)
         INFO    - 10/96 tiac_magpie               tests/kernel/common/kernel.common.tls              :byl:`SKIPPED` (filter)
         INFO    - 11/96 tiac_magpie               tests/kernel/spinlock/kernel.multiprocessing.spinlock :byl:`SKIPPED` (filter)
         INFO    - 12/96 tiac_magpie               tests/kernel/common/kernel.common.nano64           :bgn:`PASSED` (device 8.231s)
         INFO    - 13/96 tiac_magpie               tests/kernel/common/kernel.common.nano32           :bgn:`PASSED` (device 7.934s)
         INFO    - 14/96 tiac_magpie               tests/kernel/mbox/mbox_api/kernel.mailbox.api      :bgn:`PASSED` (device 4.375s)
         INFO    - 15/96 tiac_magpie               tests/kernel/mbox/mbox_usage/kernel.mailbox.usage  :bgn:`PASSED` (device 3.849s)
         INFO    - 16/96 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.sam   :byl:`SKIPPED` (filter)
         INFO    - 17/96 tiac_magpie               tests/kernel/common/kernel.common                  :bgn:`PASSED` (device 8.021s)
         INFO    - 18/96 tiac_magpie               tests/kernel/tickless/tickless_concept/kernel.tickless.concept :bgn:`PASSED` (device 4.871s)
         INFO    - 19/96 tiac_magpie               tests/kernel/xip/arch.common.xip                   :bgn:`PASSED` (device 3.719s)
         INFO    - 20/96 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue       :bgn:`PASSED` (device 4.063s)
         INFO    - 21/96 tiac_magpie               tests/kernel/workq/work/kernel.work.api            :bgn:`PASSED` (device 6.388s)
         INFO    - 22/96 tiac_magpie               tests/kernel/workq/work_queue/kernel.workqueue     :bgn:`PASSED` (device 7.961s)
         INFO    - 23/96 tiac_magpie               tests/kernel/workq/user_work/kernel.work.user      :bgn:`PASSED` (device 5.282s)
         INFO    - 24/96 tiac_magpie               tests/kernel/profiling/profiling_api/kernel.common.profiling :bgn:`PASSED` (device 4.047s)
         INFO    - 25/96 tiac_magpie               tests/kernel/poll/kernel.poll                      :bgn:`PASSED` (device 9.933s)
         INFO    - 26/96 tiac_magpie               tests/kernel/sched/preempt/kernel.scheduler.preempt :bgn:`PASSED` (device 3.802s)
         INFO    - 27/96 tiac_magpie               tests/kernel/sched/metairq/kernel.scheduler.metairq :bgn:`PASSED` (device 3.786s)
         INFO    - 28/96 tiac_magpie               tests/kernel/sched/deadline/kernel.scheduler.deadline :bgn:`PASSED` (device 4.111s)
         INFO    - 29/96 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.dumb_no_timeslicing :bgn:`PASSED` (device 8.061s)
         INFO    - 30/96 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq_no_timeslicing :bgn:`PASSED` (device 8.259s)
         INFO    - 31/96 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq :bgn:`PASSED` (device 23.847s)
         INFO    - 32/96 tiac_magpie               tests/kernel/smp/kernel.multiprocessing.smp        :byl:`SKIPPED` (filter)
         INFO    - 33/96 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.no_timeslicing :bgn:`PASSED` (device 8.335s)
         INFO    - 34/96 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler   :bgn:`PASSED` (device 23.710s)
         INFO    - 35/96 tiac_magpie               tests/kernel/obj_tracking/kernel.objects.tracking  :bgn:`PASSED` (device 3.775s)
         INFO    - 36/96 tiac_magpie               tests/kernel/interrupt/arch.interrupt              :bgn:`PASSED` (device 4.052s)
         INFO    - 37/96 tiac_magpie               tests/kernel/queue/kernel.queue                    :bgn:`PASSED` (device 7.241s)
         INFO    - 38/96 tiac_magpie               tests/kernel/sleep/kernel.common.timing            :bgn:`PASSED` (device 8.236s)
         INFO    - 39/96 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer.tickless :bgn:`PASSED` (device 8.937s)
         INFO    - 40/96 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer          :bgn:`PASSED` (device 8.820s)
         INFO    - 41/96 tiac_magpie               tests/kernel/timer/timer_error_case/kernel.timer.error_case :bgn:`PASSED` (device 5.607s)
         INFO    - 42/96 tiac_magpie               tests/kernel/timer/timer_monotonic/kernel.timer.monotonic :bgn:`PASSED` (device 5.080s)
         INFO    - 43/96 tiac_magpie               tests/kernel/mem_heap/mheap_api_concept/kernel.memory_heap :bgn:`PASSED` (device 3.789s)
         INFO    - 44/96 tiac_magpie               tests/kernel/mem_heap/k_heap_api/kernel.k_heap_api :bgn:`PASSED` (device 4.033s)
         INFO    - 45/96 tiac_magpie               tests/kernel/fpu_sharing/float_disable/kernel.fpu_sharing.float_disable.arm :bgn:`PASSED` (device 5.236s)
         INFO    - 46/96 tiac_magpie               tests/kernel/fifo/fifo_usage/kernel.fifo.usage     :bgn:`PASSED` (device 3.818s)
         INFO    - 47/96 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls.userspace :byl:`SKIPPED` (filter)
         INFO    - 48/96 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls        :byl:`SKIPPED` (filter)
         INFO    - 49/96 tiac_magpie               tests/kernel/threads/thread_apis/kernel.threads.apis.pinonly :byl:`SKIPPED` (filter)
         INFO    - 50/96 tiac_magpie               tests/kernel/fifo/fifo_api/kernel.fifo             :bgn:`PASSED` (device 4.482s)
         INFO    - 51/96 tiac_magpie               tests/kernel/fifo/fifo_timeout/kernel.fifo.timeout :bgn:`PASSED` (device 4.051s)
         INFO    - 52/96 tiac_magpie               tests/kernel/early_sleep/kernel.common.sleep       :bgn:`PASSED` (device 5.237s)
         INFO    - 53/96 tiac_magpie               tests/kernel/threads/dynamic_thread/kernel.threads.dynamic :bgn:`PASSED` (device 6.421s)
         INFO    - 54/96 tiac_magpie               tests/kernel/threads/thread_stack/kernel.threads.armv8m_mpu_stack_guard :byl:`SKIPPED` (filter)
         INFO    - 55/96 tiac_magpie               tests/kernel/threads/thread_init/kernel.threads.init :bgn:`PASSED` (device 9.401s)
         INFO    - 56/96 tiac_magpie               tests/kernel/threads/thread_apis/kernel.threads.apis :bgn:`PASSED` (device 12.110s)
         INFO    - 57/96 tiac_magpie               tests/kernel/threads/thread_error_case/kernel.threads.error.case :bgn:`PASSED` (device 5.515s)
         INFO    - 58/96 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`SKIPPED` (filter)
         INFO    - 59/96 tiac_magpie               tests/kernel/fatal/message_capture/kernel.logging.message_capture :bgn:`PASSED` (device 2.545s)
         INFO    - 60/96 tiac_magpie               tests/kernel/threads/thread_stack/kernel.threads.thread_stack :bgn:`PASSED` (device 5.644s)
         INFO    - 61/96 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_sentinel :bgn:`PASSED` (device 4.097s)
         INFO    - 62/96 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_no_userspace :bgn:`PASSED` (device 4.010s)
         INFO    - 63/96 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_arm_fpu_sharing :bgn:`PASSED` (device 6.307s)
         INFO    - 64/96 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection :bgn:`PASSED` (device 5.655s)
         INFO    - 65/96 tiac_magpie               tests/kernel/device/kernel.device.pm               :bgn:`PASSED` (device 5.395s)
         INFO    - 66/96 tiac_magpie               tests/kernel/device/kernel.device                  :bgn:`PASSED` (device 5.368s)
         INFO    - 67/96 tiac_magpie               tests/kernel/msgq/msgq_api/kernel.message_queue    :bgn:`PASSED` (device 6.084s)
         INFO    - 68/96 tiac_magpie               tests/kernel/msgq/msgq_usage/kernel.message_queue_usage :bgn:`PASSED` (device 5.169s)
         INFO    - 69/96 tiac_magpie               tests/kernel/mp/kernel.multiprocessing             :byl:`SKIPPED` (filter)
         INFO    - 70/96 tiac_magpie               tests/kernel/condvar/condvar_api/kernel.condvar    :bgn:`PASSED` (device 8.026s)
         INFO    - 71/96 tiac_magpie               tests/kernel/pipe/pipe_api/kernel.pipe.api         :bgn:`PASSED` (device 7.022s)
         INFO    - 72/96 tiac_magpie               tests/kernel/pipe/pipe/kernel.pipe                 :bgn:`PASSED` (device 7.310s)
         INFO    - 73/96 tiac_magpie               tests/kernel/events/event_api/kernel.events        :bgn:`PASSED` (device 4.258s)
         INFO    - 74/96 tiac_magpie               tests/kernel/events/sys_event/kernel.events.usage  :bgn:`PASSED` (device 5.743s)
         INFO    - 75/96 tiac_magpie               tests/kernel/lifo/lifo_usage/kernel.lifo.usage     :bgn:`PASSED` (device 4.340s)
         INFO    - 76/96 tiac_magpie               tests/kernel/lifo/lifo_api/kernel.lifo             :bgn:`PASSED` (device 4.274s)
         INFO    - 77/96 tiac_magpie               tests/kernel/mem_protect/protection/kernel.memory_protection.protection :bgn:`PASSED` (device 3.992s)
         INFO    - 78/96 tiac_magpie               tests/kernel/mem_protect/obj_validation/kernel.memory_protection.obj_validation :bgn:`PASSED` (device 5.052s)
         INFO    - 79/96 tiac_magpie               tests/kernel/mem_protect/stack_random/kernel.memory_protection.stack_random :bgn:`PASSED` (device 3.763s)
         INFO    - 80/96 tiac_magpie               tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot :bgn:`PASSED` (device 6.644s)
         INFO    - 81/96 tiac_magpie               tests/kernel/mem_protect/syscalls/kernel.memory_protection.syscalls :bgn:`PASSED` (device 20.298s)
         INFO    - 82/96 tiac_magpie               tests/kernel/mem_protect/futex/kernel.futex        :bgn:`PASSED` (device 5.851s)
         INFO    - 83/96 tiac_magpie               tests/kernel/mem_protect/demand_paging/kernel.demand_paging :byl:`SKIPPED` (filter)
         INFO    - 84/96 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem.nouser :bgn:`PASSED` (device 4.497s)
         INFO    - 85/96 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64.coverage.exec :byl:`SKIPPED` (filter)
         INFO    - 86/96 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem :bgn:`PASSED` (device 6.043s)
         INFO    - 87/96 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64.coverage :byl:`SKIPPED` (filter)
         INFO    - 88/96 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64 :byl:`SKIPPED` (filter)
         INFO    - 89/96 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map :byl:`SKIPPED` (filter)
         INFO    - 90/96 tiac_magpie               tests/kernel/mem_protect/mem_protect/kernel.memory_protection :bgn:`PASSED` (device 9.358s)
         INFO    - 91/96 tiac_magpie               tests/kernel/mem_protect/userspace/kernel.memory_protection.userspace :bgn:`PASSED` (device 7.002s)
         INFO    - 92/96 tiac_magpie               tests/kernel/mutex/sys_mutex/system.mutex.nouser   :bgn:`PASSED` (device 11.407s)
         INFO    - 93/96 tiac_magpie               tests/kernel/mutex/sys_mutex/system.mutex          :bgn:`PASSED` (device 12.733s)
         INFO    - 94/96 tiac_magpie               tests/kernel/mutex/mutex_api/kernel.mutex          :bgn:`PASSED` (device 17.165s)
         INFO    - 95/96 tiac_magpie               tests/kernel/context/kernel.common                 :bgn:`PASSED` (device 9.563s)
         INFO    - 96/96 tiac_magpie               tests/kernel/mutex/mutex_error_case/kernel.mutex_error_case :bgn:`PASSED` (device 5.837s)

         INFO    - :bgn:`80 of 80` test configurations passed (100.00%), :bbk:`0` failed, :byl:`87` skipped with :bbk:`0` warnings in :bbk:`972.04 seconds`
         INFO    - In total 891 test cases were executed, 742 skipped on 1 out of total 428 platforms (0.23%)
         INFO    - :bgn:`80` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|        80 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Using 'zephyr' toolchain.
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
