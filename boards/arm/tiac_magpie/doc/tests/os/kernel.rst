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

         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    -  1/93 tiac_magpie               tests/kernel/lifo/lifo_usage/kernel.lifo.usage     :bgn:`PASSED` (device 3.912s)
         INFO    -  2/93 tiac_magpie               tests/kernel/spinlock/kernel.multiprocessing.spinlock :byl:`SKIPPED` (filter)
         INFO    -  3/93 tiac_magpie               tests/kernel/lifo/lifo_api/kernel.lifo             :bgn:`PASSED` (device 4.427s)
         INFO    -  4/93 tiac_magpie               tests/kernel/semaphore/sys_sem/kernel.semaphore.usage :bgn:`PASSED` (device 5.255s)
         INFO    -  5/93 tiac_magpie               tests/kernel/semaphore/semaphore/kernel.semaphore  :bgn:`PASSED` (device 17.739s)
         INFO    -  6/93 tiac_magpie               tests/kernel/mem_heap/k_heap_api/kernel.k_heap_api :bgn:`PASSED` (device 3.748s)
         INFO    -  7/93 tiac_magpie               tests/kernel/mem_heap/mheap_api_concept/kernel.memory_heap :bgn:`PASSED` (device 3.849s)
         INFO    -  8/93 tiac_magpie               tests/kernel/condvar/condvar_api/kernel.condvar    :bgn:`PASSED` (device 6.965s)
         INFO    -  9/93 tiac_magpie               tests/kernel/mem_slab/mslab_api/kernel.memory_slabs.api :bgn:`PASSED` (device 9.812s)
         INFO    - 10/93 tiac_magpie               tests/kernel/mem_slab/mslab/kernel.memory_slabs.api :bgn:`PASSED` (device 3.788s)
         INFO    - 11/93 tiac_magpie               tests/kernel/mem_slab/mslab_threadsafe/kernel.memory_slabs.threadsafe :bgn:`PASSED` (device 3.664s)
         INFO    - 12/93 tiac_magpie               tests/kernel/mem_slab/mslab_concept/kernel.memory_slabs.concept :bgn:`PASSED` (device 5.783s)
         INFO    - 13/93 tiac_magpie               tests/kernel/profiling/profiling_api/kernel.common.profiling :bgn:`PASSED` (device 3.963s)
         INFO    - 14/93 tiac_magpie               tests/kernel/device/kernel.device.pm               :bgn:`PASSED` (device 5.249s)
         INFO    - 15/93 tiac_magpie               tests/kernel/interrupt/arch.interrupt              :bgn:`PASSED` (device 5.790s)
         INFO    - 16/93 tiac_magpie               tests/kernel/device/kernel.device                  :bgn:`PASSED` (device 5.258s)
         INFO    - 17/93 tiac_magpie               tests/kernel/sched/preempt/kernel.scheduler.preempt :bgn:`PASSED` (device 3.759s)
         INFO    - 18/93 tiac_magpie               tests/kernel/stack/stack/kernel.stack.usage        :bgn:`PASSED` (device 6.291s)
         INFO    - 19/93 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.dumb_no_timeslicing :bgn:`PASSED` (device 7.848s)
         INFO    - 20/93 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq_no_timeslicing :bgn:`PASSED` (device 7.800s)
         INFO    - 21/93 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq :bgn:`PASSED` (device 23.588s)
         INFO    - 22/93 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.no_timeslicing :bgn:`PASSED` (device 7.749s)
         INFO    - 23/93 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler   :bgn:`PASSED` (device 23.439s)
         INFO    - 24/93 tiac_magpie               tests/kernel/sched/metairq/kernel.scheduler.metairq :bgn:`PASSED` (device 3.795s)
         INFO    - 25/93 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`SKIPPED` (filter)
         INFO    - 26/93 tiac_magpie               tests/kernel/fatal/message_capture/kernel.logging.message_capture :bgn:`PASSED` (device 2.511s)
         INFO    - 27/93 tiac_magpie               tests/kernel/sched/deadline/kernel.scheduler.deadline :bgn:`PASSED` (device 4.146s)
         INFO    - 28/93 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_sentinel :bgn:`PASSED` (device 4.053s)
         INFO    - 29/93 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_no_userspace :bgn:`PASSED` (device 4.115s)
         INFO    - 30/93 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_arm_fpu_sharing :bgn:`PASSED` (device 6.372s)
         INFO    - 31/93 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection :bgn:`PASSED` (device 5.546s)
         INFO    - 32/93 tiac_magpie               tests/kernel/fpu_sharing/float_disable/kernel.fpu_sharing.float_disable.arm :bgn:`PASSED` (device 5.066s)
         INFO    - 33/93 tiac_magpie               tests/kernel/poll/kernel.poll                      :bgn:`PASSED` (device 10.335s)
         INFO    - 34/93 tiac_magpie               tests/kernel/mbox/mbox_usage/kernel.mailbox.usage  :bgn:`PASSED` (device 3.750s)
         INFO    - 35/93 tiac_magpie               tests/kernel/mbox/mbox_api/kernel.mailbox.api      :bgn:`PASSED` (device 4.313s)
         INFO    - 36/93 tiac_magpie               tests/kernel/fifo/fifo_usage/kernel.fifo.usage     :bgn:`PASSED` (device 3.729s)
         INFO    - 37/93 tiac_magpie               tests/kernel/fifo/fifo_timeout/kernel.fifo.timeout :bgn:`PASSED` (device 4.002s)
         INFO    - 38/93 tiac_magpie               tests/kernel/fifo/fifo_api/kernel.fifo             :bgn:`PASSED` (device 4.456s)
         INFO    - 39/93 tiac_magpie               tests/kernel/sleep/kernel.common.timing            :bgn:`PASSED` (device 8.185s)
         INFO    - 40/93 tiac_magpie               tests/kernel/mutex/sys_mutex/system.mutex.nouser   :bgn:`PASSED` (device 11.423s)
         INFO    - 41/93 tiac_magpie               tests/kernel/pipe/pipe/kernel.pipe                 :bgn:`PASSED` (device 6.820s)
         INFO    - 42/93 tiac_magpie               tests/kernel/pipe/pipe_api/kernel.pipe.api         :bgn:`PASSED` (device 6.860s)
         INFO    - 43/93 tiac_magpie               tests/kernel/mutex/sys_mutex/system.mutex          :bgn:`PASSED` (device 12.765s)
         INFO    - 44/93 tiac_magpie               tests/kernel/mutex/mutex_api/kernel.mutex          :bgn:`PASSED` (device 17.312s)
         INFO    - 45/93 tiac_magpie               tests/kernel/timer/timer_error_case/kernel.timer   :bgn:`PASSED` (device 5.481s)
         INFO    - 46/93 tiac_magpie               tests/kernel/timer/timer_monotonic/kernel.timer.monotonic :bgn:`PASSED` (device 5.198s)
         INFO    - 47/93 tiac_magpie               tests/kernel/mutex/mutex_error_case/kernel.mutex   :bgn:`PASSED` (device 5.423s)
         INFO    - 48/93 tiac_magpie               tests/kernel/xip/arch.common.xip                   :bgn:`PASSED` (device 3.769s)
         INFO    - 49/93 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer.tickless :bgn:`PASSED` (device 8.705s)
         INFO    - 50/93 tiac_magpie               tests/kernel/common/kernel.common.misra            :byl:`SKIPPED` (filter)
         INFO    - 51/93 tiac_magpie               tests/kernel/common/kernel.common.tls              :byl:`SKIPPED` (filter)
         INFO    - 52/93 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer          :bgn:`PASSED` (device 8.595s)
         INFO    - 53/93 tiac_magpie               tests/kernel/common/kernel.common.nano64           :bgn:`PASSED` (device 7.890s)
         INFO    - 54/93 tiac_magpie               tests/kernel/common/kernel.common.nano32           :bgn:`PASSED` (device 7.830s)
         INFO    - 55/93 tiac_magpie               tests/kernel/mem_protect/stack_random/kernel.memory_protection.stack_random :bgn:`PASSED` (device 3.958s)
         INFO    - 56/93 tiac_magpie               tests/kernel/common/kernel.common                  :bgn:`PASSED` (device 7.768s)
         INFO    - 57/93 tiac_magpie               tests/kernel/queue/kernel.queue                    :bgn:`PASSED` (device 7.259s)
         INFO    - 58/93 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64.coverage.exec :byl:`SKIPPED` (filter)
         INFO    - 59/93 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64.coverage :byl:`SKIPPED` (filter)
         INFO    - 60/93 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64 :byl:`SKIPPED` (filter)
         INFO    - 61/93 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem.nouser :bgn:`PASSED` (device 4.527s)
         INFO    - 62/93 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map :byl:`SKIPPED` (filter)
         INFO    - 63/93 tiac_magpie               tests/kernel/mem_protect/futex/kernel.futex        :bgn:`PASSED` (device 5.634s)
         INFO    - 64/93 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem :bgn:`PASSED` (device 5.970s)
         INFO    - 65/93 tiac_magpie               tests/kernel/mem_protect/protection/kernel.memory_protection.protection :bgn:`PASSED` (device 4.022s)
         INFO    - 66/93 tiac_magpie               tests/kernel/mem_protect/userspace/kernel.memory_protection.userspace :bgn:`PASSED` (device 6.662s)
         INFO    - 67/93 tiac_magpie               tests/kernel/mem_protect/demand_paging/kernel.demand_paging :byl:`SKIPPED` (filter)
         INFO    - 68/93 tiac_magpie               tests/kernel/mem_protect/syscalls/kernel.memory_protection.syscalls :bgn:`PASSED` (device 20.382s)
         INFO    - 69/93 tiac_magpie               tests/kernel/mem_protect/mem_protect/kernel.memory_protection :bgn:`PASSED` (device 9.810s)
         INFO    - 70/93 tiac_magpie               tests/kernel/mem_protect/obj_validation/kernel.memory_protection.obj_validation :bgn:`PASSED` (device 5.180s)
         INFO    - 71/93 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.sam   :byl:`SKIPPED` (filter)
         INFO    - 72/93 tiac_magpie               tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot :bgn:`PASSED` (device 6.487s)
         INFO    - 73/93 tiac_magpie               tests/kernel/workq/work_queue/kernel.workqueue     :bgn:`PASSED` (device 7.974s)
         INFO    - 74/93 tiac_magpie               tests/kernel/workq/work/kernel.work.api            :bgn:`PASSED` (device 5.970s)
         INFO    - 75/93 tiac_magpie               tests/kernel/threads/thread_stack/kernel.threads.armv8m_mpu_stack_guard :byl:`SKIPPED` (filter)
         INFO    - 76/93 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue       :bgn:`PASSED` (device 3.922s)
         INFO    - 77/93 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls.userspace :byl:`SKIPPED` (filter)
         INFO    - 78/93 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls        :byl:`SKIPPED` (filter)
         INFO    - 79/93 tiac_magpie               tests/kernel/early_sleep/kernel.common.sleep       :bgn:`PASSED` (device 5.194s)
         INFO    - 80/93 tiac_magpie               tests/kernel/workq/user_work/kernel.work.user      :bgn:`PASSED` (device 5.182s)
         INFO    - 81/93 tiac_magpie               tests/kernel/threads/thread_stack/kernel.threads.thread_stack :bgn:`PASSED` (device 5.598s)
         INFO    - 82/93 tiac_magpie               tests/kernel/threads/thread_init/kernel.threads.init :bgn:`PASSED` (device 9.169s)
         INFO    - 83/93 tiac_magpie               tests/kernel/threads/thread_error_case/kernel.threads.error.case :bgn:`PASSED` (device 5.408s)
         INFO    - 84/93 tiac_magpie               tests/kernel/threads/thread_apis/kernel.threads.apis :bgn:`PASSED` (device 11.826s)
         INFO    - 85/93 tiac_magpie               tests/kernel/threads/dynamic_thread/kernel.threads.dynamic :bgn:`PASSED` (device 6.303s)
         INFO    - 86/93 tiac_magpie               tests/kernel/mp/kernel.multiprocessing             :byl:`SKIPPED` (filter)
         INFO    - 87/93 tiac_magpie               tests/kernel/msgq/msgq_usage/kernel.message_queue_usage :bgn:`PASSED` (device 5.063s)
         INFO    - 88/93 tiac_magpie               tests/kernel/smp/kernel.multiprocessing.smp        :byl:`SKIPPED` (filter)
         INFO    - 89/93 tiac_magpie               tests/kernel/msgq/msgq_api/kernel.message_queue    :bgn:`PASSED` (device 6.093s)
         INFO    - 90/93 tiac_magpie               tests/kernel/pending/kernel.objects                :bgn:`PASSED` (device 9.885s)
         INFO    - 91/93 tiac_magpie               tests/kernel/gen_isr_table/arch.interrupt.gen_isr_table.arm_mainline :bgn:`PASSED` (device 3.896s)
         INFO    - 92/93 tiac_magpie               tests/kernel/tickless/tickless_concept/kernel.tickless.concept :bgn:`PASSED` (device 4.995s)
         INFO    - 93/93 tiac_magpie               tests/kernel/context/kernel.common                 :bgn:`PASSED` (device 9.755s)

         INFO    - :bgn:`78 of 78` test configurations passed (100.00%), :bbk:`0` failed, :byl:`50` skipped with :bbk:`0` warnings in :bbk:`887.04 seconds`
         INFO    - In total 872 test cases were executed, 473 skipped on 1 out of total 370 platforms (0.27%)
         INFO    - :bgn:`78` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|        78 \|
