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
             --board-root bridle/boards \
             --platform tiac_magpie \
             --device-testing --device-serial /dev/ttyUSBx \
             --testcase-root zephyr/tests/kernel

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    -  1/93 tiac_magpie               tests/kernel/spinlock/kernel.multiprocessing.spinlock :byl:`SKIPPED` (filter)
         INFO    -  2/93 tiac_magpie               tests/kernel/lifo/lifo_usage/kernel.lifo.usage     :bgn:`PASSED` (device 3.115s)
         INFO    -  3/93 tiac_magpie               tests/kernel/lifo/lifo_api/kernel.lifo             :bgn:`PASSED` (device 3.478s)
         INFO    -  4/93 tiac_magpie               tests/kernel/mem_heap/mheap_api_concept/kernel.memory_heap :bgn:`PASSED` (device 2.986s)
         INFO    -  5/93 tiac_magpie               tests/kernel/semaphore/semaphore/kernel.semaphore  :bgn:`PASSED` (device 20.119s)
         INFO    -  6/93 tiac_magpie               tests/kernel/mem_heap/k_heap_api/kernel.k_heap_api :bgn:`PASSED` (device 3.005s)
         INFO    -  7/93 tiac_magpie               tests/kernel/mem_slab/mslab_api/kernel.memory_slabs.api :bgn:`PASSED` (device 9.047s)
         INFO    -  8/93 tiac_magpie               tests/kernel/condvar/condvar_api/kernel.condvar    :bgn:`PASSED` (device 8.825s)
         INFO    -  9/93 tiac_magpie               tests/kernel/mem_slab/mslab/kernel.memory_slabs.api :bgn:`PASSED` (device 3.065s)
         INFO    - 10/93 tiac_magpie               tests/kernel/mem_slab/mslab_concept/kernel.memory_slabs.concept :bgn:`PASSED` (device 4.980s)
         INFO    - 11/93 tiac_magpie               tests/kernel/mem_slab/mslab_threadsafe/kernel.memory_slabs.threadsafe :bgn:`PASSED` (device 3.063s)
         INFO    - 12/93 tiac_magpie               tests/kernel/device/kernel.device.pm               :bgn:`PASSED` (device 4.161s)
         INFO    - 13/93 tiac_magpie               tests/kernel/profiling/profiling_api/kernel.common.profiling :bgn:`PASSED` (device 3.171s)
         INFO    - 14/93 tiac_magpie               tests/kernel/device/kernel.device                  :bgn:`PASSED` (device 4.108s)
         INFO    - 15/93 tiac_magpie               tests/kernel/interrupt/arch.interrupt              :bgn:`PASSED` (device 5.031s)
         INFO    - 16/93 tiac_magpie               tests/kernel/sched/preempt/kernel.scheduler.preempt :bgn:`PASSED` (device 3.045s)
         INFO    - 17/93 tiac_magpie               tests/kernel/stack/stack/kernel.stack.usage        :bgn:`PASSED` (device 5.137s)
         INFO    - 18/93 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.dumb_no_timeslicing :bgn:`PASSED` (device 5.820s)
         INFO    - 19/93 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq_no_timeslicing :bgn:`PASSED` (device 5.746s)
         INFO    - 20/93 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq :bgn:`PASSED` (device 21.637s)
         INFO    - 21/93 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.no_timeslicing :bgn:`PASSED` (device 5.636s)
         INFO    - 22/93 tiac_magpie               tests/kernel/sched/metairq/kernel.scheduler.metairq :bgn:`PASSED` (device 3.007s)
         INFO    - 23/93 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler   :bgn:`PASSED` (device 21.567s)
         INFO    - 24/93 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`SKIPPED` (filter)
         INFO    - 25/93 tiac_magpie               tests/kernel/sched/deadline/kernel.scheduler.deadline :bgn:`PASSED` (device 3.188s)
         INFO    - 26/93 tiac_magpie               tests/kernel/fatal/message_capture/kernel.logging.message_capture :bgn:`PASSED` (device 2.204s)
         INFO    - 27/93 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_sentinel :bgn:`PASSED` (device 3.281s)
         INFO    - 28/93 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_no_userspace :bgn:`PASSED` (device 3.278s)
         INFO    - 29/93 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_arm_fpu_sharing :bgn:`PASSED` (device 5.069s)
         INFO    - 30/93 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection :bgn:`PASSED` (device 4.429s)
         INFO    - 31/93 tiac_magpie               tests/kernel/fpu_sharing/float_disable/kernel.fpu_sharing.float_disable.arm :bgn:`PASSED` (device 4.087s)
         INFO    - 32/93 tiac_magpie               tests/kernel/poll/kernel.poll                      :bgn:`PASSED` (device 6.869s)
         INFO    - 33/93 tiac_magpie               tests/kernel/mbox/mbox_api/kernel.mailbox.api      :bgn:`PASSED` (device 3.490s)
         INFO    - 34/93 tiac_magpie               tests/kernel/mbox/mbox_usage/kernel.mailbox.usage  :bgn:`PASSED` (device 2.991s)
         INFO    - 35/93 tiac_magpie               tests/kernel/fifo/fifo_usage/kernel.fifo.usage     :bgn:`PASSED` (device 3.056s)
         INFO    - 36/93 tiac_magpie               tests/kernel/fifo/fifo_timeout/kernel.fifo.timeout :bgn:`PASSED` (device 3.358s)
         INFO    - 37/93 tiac_magpie               tests/kernel/fifo/fifo_api/kernel.fifo             :bgn:`PASSED` (device 3.678s)
         INFO    - 38/93 tiac_magpie               tests/kernel/sleep/kernel.common.timing            :bgn:`PASSED` (device 7.057s)
         INFO    - 39/93 tiac_magpie               tests/kernel/pipe/pipe/kernel.pipe                 :bgn:`PASSED` (device 5.782s)
         INFO    - 40/93 tiac_magpie               tests/kernel/pipe/pipe_api/kernel.pipe.api         :bgn:`PASSED` (device 4.374s)
         INFO    - 41/93 tiac_magpie               tests/kernel/mutex/sys_mutex/system.mutex.nouser   :bgn:`PASSED` (device 10.533s)
         INFO    - 42/93 tiac_magpie               tests/kernel/mutex/sys_mutex/system.mutex          :bgn:`PASSED` (device 11.612s)
         INFO    - 43/93 tiac_magpie               tests/kernel/mutex/mutex_error_case/kernel.mutex   :bgn:`PASSED` (device 4.277s)
         INFO    - 44/93 tiac_magpie               tests/kernel/mutex/mutex_api/kernel.mutex          :bgn:`PASSED` (device 16.134s)
         INFO    - 45/93 tiac_magpie               tests/kernel/timer/timer_monotonic/kernel.timer.monotonic :bgn:`PASSED` (device 4.510s)
         INFO    - 46/93 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer.tickless :bgn:`PASSED` (device 7.156s)
         INFO    - 47/93 tiac_magpie               tests/kernel/timer/timer_error_case/kernel.timer   :bgn:`PASSED` (device 4.497s)
         INFO    - 48/93 tiac_magpie               tests/kernel/xip/arch.common.xip                   :bgn:`PASSED` (device 2.981s)
         INFO    - 49/93 tiac_magpie               tests/kernel/common/kernel.common.misra            :byl:`SKIPPED` (filter)
         INFO    - 50/93 tiac_magpie               tests/kernel/common/kernel.common.tls              :byl:`SKIPPED` (filter)
         INFO    - 51/93 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer          :bgn:`PASSED` (device 7.216s)
         INFO    - 52/93 tiac_magpie               tests/kernel/common/kernel.common.nano64           :bgn:`PASSED` (device 6.041s)
         INFO    - 53/93 tiac_magpie               tests/kernel/common/kernel.common.nano32           :bgn:`PASSED` (device 6.039s)
         INFO    - 54/93 tiac_magpie               tests/kernel/common/kernel.common                  :bgn:`PASSED` (device 6.059s)
         INFO    - 55/93 tiac_magpie               tests/kernel/mem_protect/stack_random/kernel.memory_protection.stack_random :bgn:`PASSED` (device 3.030s)
         INFO    - 56/93 tiac_magpie               tests/kernel/queue/kernel.queue                    :bgn:`PASSED` (device 6.092s)
         INFO    - 57/93 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64.coverage.exec :byl:`SKIPPED` (filter)
         INFO    - 58/93 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64.coverage :byl:`SKIPPED` (filter)
         INFO    - 59/93 tiac_magpie               tests/kernel/mem_protect/futex/kernel.futex        :bgn:`PASSED` (device 4.495s)
         INFO    - 60/93 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64 :byl:`SKIPPED` (filter)
         INFO    - 61/93 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map :byl:`SKIPPED` (filter)
         INFO    - 62/93 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem.nouser :bgn:`PASSED` (device 3.719s)
         INFO    - 63/93 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem :bgn:`PASSED` (device 4.885s)
         INFO    - 64/93 tiac_magpie               tests/kernel/mem_protect/protection/kernel.memory_protection.protection :bgn:`PASSED` (device 3.231s)
         INFO    - 65/93 tiac_magpie               tests/kernel/mem_protect/userspace/kernel.memory_protection.userspace :bgn:`PASSED` (device 5.496s)
         INFO    - 66/93 tiac_magpie               tests/kernel/mem_protect/demand_paging/kernel.memory_protection.demand_paging :byl:`SKIPPED` (filter)
         INFO    - 67/93 tiac_magpie               tests/kernel/mem_protect/syscalls/kernel.memory_protection.syscalls :bgn:`PASSED` (device 19.172s)
         INFO    - 68/93 tiac_magpie               tests/kernel/mem_protect/obj_validation/kernel.memory_protection.obj_validation :bgn:`PASSED` (device 3.926s)
         INFO    - 69/93 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.sam   :byl:`SKIPPED` (filter)
         INFO    - 70/93 tiac_magpie               tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot :bgn:`PASSED` (device 4.885s)
         INFO    - 71/93 tiac_magpie               tests/kernel/mem_protect/mem_protect/kernel.memory_protection :bgn:`PASSED` (device 5.939s)
         INFO    - 72/93 tiac_magpie               tests/kernel/workq/work_queue/kernel.workqueue     :bgn:`PASSED` (device 8.027s)
         INFO    - 73/93 tiac_magpie               tests/kernel/threads/thread_stack/kernel.threads.armv8m_mpu_stack_guard :byl:`SKIPPED` (filter)
         INFO    - 74/93 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue       :bgn:`PASSED` (device 3.209s)
         INFO    - 75/93 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls.userspace :byl:`SKIPPED` (filter)
         INFO    - 76/93 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls        :byl:`SKIPPED` (filter)
         INFO    - 77/93 tiac_magpie               tests/kernel/early_sleep/kernel.common.sleep       :bgn:`PASSED` (device 4.555s)
         INFO    - 78/93 tiac_magpie               tests/kernel/workq/work_queue_api/kernel.workqueue.api :bgn:`PASSED` (device 7.876s)
         INFO    - 79/93 tiac_magpie               tests/kernel/threads/thread_stack/kernel.threads.thread_stack :bgn:`PASSED` (device 4.522s)
         INFO    - 80/93 tiac_magpie               tests/kernel/threads/no-multithreading/kernel.threads.no-multithreading :bgn:`PASSED` (device 2.302s)
         INFO    - 81/93 tiac_magpie               tests/kernel/threads/thread_init/kernel.threads.init :bgn:`PASSED` (device 8.027s)
         INFO    - 82/93 tiac_magpie               tests/kernel/threads/thread_error_case/kernel.threads.error.case :bgn:`PASSED` (device 4.393s)
         INFO    - 83/93 tiac_magpie               tests/kernel/threads/thread_apis/kernel.threads.apis :bgn:`PASSED` (device 9.757s)
         INFO    - 84/93 tiac_magpie               tests/kernel/pending/kernel.objects                :bgn:`PASSED` (device 9.040s)
         INFO    - 85/93 tiac_magpie               tests/kernel/mp/kernel.multiprocessing             :byl:`SKIPPED` (filter)
         INFO    - 86/93 tiac_magpie               tests/kernel/msgq/msgq_api/kernel.message_queue    :bgn:`PASSED` (device 4.929s)
         INFO    - 87/93 tiac_magpie               tests/kernel/smp/kernel.multiprocessing.smp        :byl:`SKIPPED` (filter)
         INFO    - 88/93 tiac_magpie               tests/kernel/threads/dynamic_thread/kernel.threads.dynamic :bgn:`PASSED` (device 5.008s)
         INFO    - 89/93 tiac_magpie               tests/kernel/tickless/tickless/kernel.tickless     :byl:`SKIPPED` (filter)
         INFO    - 90/93 tiac_magpie               tests/kernel/obj_tracing/kernel.objects.tracing    :bgn:`PASSED` (device 3.280s)
         INFO    - 91/93 tiac_magpie               tests/kernel/gen_isr_table/arch.interrupt.gen_isr_table.arm_mainline :bgn:`PASSED` (device 3.107s)
         INFO    - 92/93 tiac_magpie               tests/kernel/tickless/tickless_concept/kernel.tickless.concept :bgn:`PASSED` (device 4.305s)
         INFO    - 93/93 tiac_magpie               tests/kernel/context/kernel.common                 :bgn:`PASSED` (device 8.499s)

         INFO    - :bgn:`77 of 77` test configurations passed (100.00%), :bbk:`0` failed, :byl:`35` skipped with :bbk:`0` warnings in :bbk:`581.06 seconds`
         INFO    - In total 733 test cases were executed, 335 skipped on 1 out of total 330 platforms (0.30%)
         INFO    - :bgn:`77` test configurations executed on platforms, :brd:`0` test configurations were only built.
