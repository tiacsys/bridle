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
         INFO    -  48/147 tiac_magpie               tests/kernel/mem_slab/mslab_stats/kernel.memory_slab.stats :bgn:`PASSED` (device 2.361s)
         INFO    -  49/147 tiac_magpie               tests/kernel/pending/kernel.objects                :bgn:`PASSED` (device 8.306s)
         INFO    -  50/147 tiac_magpie               tests/kernel/mem_slab/mslab/kernel.memory_slabs    :bgn:`PASSED` (device 3.094s)
         INFO    -  51/147 tiac_magpie               tests/kernel/mem_slab/mslab_threadsafe/kernel.memory_slabs.threadsafe :bgn:`PASSED` (device 2.347s)
         INFO    -  52/147 tiac_magpie               tests/kernel/mem_slab/mslab_api/kernel.memory_slabs.api :bgn:`PASSED` (device 8.388s)
         INFO    -  53/147 tiac_magpie               tests/kernel/mem_slab/mslab_concept/kernel.memory_slabs.concept :bgn:`PASSED` (device 6.043s)
         INFO    -  54/147 tiac_magpie               tests/kernel/stack/stack/kernel.stack.usage        :bgn:`PASSED` (device 4.694s)
         INFO    -  55/147 tiac_magpie               tests/kernel/semaphore/semaphore/kernel.semaphore  :bgn:`PASSED` (device 15.413s)
         INFO    -  56/147 tiac_magpie               tests/kernel/semaphore/sys_sem/kernel.semaphore.usage :bgn:`PASSED` (device 4.026s)
         INFO    -  57/147 tiac_magpie               tests/kernel/common/kernel.common.picolibc         :bgn:`PASSED` (device 7.653s)
         INFO    -  58/147 tiac_magpie               tests/kernel/common/kernel.common.misra            :byl:`SKIPPED` (runtime filter)
         INFO    -  59/147 tiac_magpie               tests/kernel/common/kernel.common.nano64           :bgn:`PASSED` (device 7.716s)
         INFO    -  60/147 tiac_magpie               tests/kernel/common/kernel.common.nano32           :bgn:`PASSED` (device 8.510s)
         INFO    -  61/147 tiac_magpie               tests/kernel/common/kernel.common.minimallibc      :bgn:`PASSED` (device 7.802s)
         INFO    -  62/147 tiac_magpie               tests/kernel/spinlock/kernel.multiprocessing.spinlock :byl:`SKIPPED` (runtime filter)
         INFO    -  63/147 tiac_magpie               tests/kernel/common/kernel.common.tls              :bgn:`PASSED` (device 8.450s)
         INFO    -  64/147 tiac_magpie               tests/kernel/usage/thread_runtime_stats/kernel.usage :bgn:`PASSED` (device 2.392s)
         INFO    -  65/147 tiac_magpie               tests/kernel/common/kernel.common                  :bgn:`PASSED` (device 8.440s)
         INFO    -  66/147 tiac_magpie               tests/kernel/mbox/mbox_api/kernel.mailbox.api      :bgn:`PASSED` (device 3.964s)
         INFO    -  67/147 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.critical.sam :byl:`SKIPPED` (runtime filter)
         INFO    -  68/147 tiac_magpie               tests/kernel/mbox/mbox_usage/kernel.mailbox.usage  :bgn:`PASSED` (device 2.554s)
         INFO    -  69/147 tiac_magpie               tests/kernel/tickless/tickless_concept/kernel.tickless.concept :bgn:`PASSED` (device 3.286s)
         INFO    -  70/147 tiac_magpie               tests/kernel/xip/arch.common.xip                   :bgn:`PASSED` (device 3.191s)
         INFO    -  71/147 tiac_magpie               tests/kernel/workq/work/kernel.work.api            :bgn:`PASSED` (device 6.074s)
         INFO    -  72/147 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.critical :bgn:`PASSED` (device 2.483s)
         INFO    -  73/147 tiac_magpie               tests/kernel/workq/work_queue/kernel.workqueue     :bgn:`PASSED` (device 7.461s)
         INFO    -  74/147 tiac_magpie               tests/kernel/profiling/profiling_api/kernel.common.profiling :bgn:`PASSED` (device 3.491s)
         INFO    -  75/147 tiac_magpie               tests/kernel/sched/preempt/kernel.scheduler.preempt :bgn:`PASSED` (device 2.343s)
         INFO    -  76/147 tiac_magpie               tests/kernel/workq/user_work/kernel.work.user      :bgn:`PASSED` (device 3.113s)
         INFO    -  77/147 tiac_magpie               tests/kernel/sched/metairq/kernel.scheduler.metairq :bgn:`PASSED` (device 2.981s)
         INFO    -  78/147 tiac_magpie               tests/kernel/poll/kernel.poll                      :bgn:`PASSED` (device 7.785s)
         INFO    -  79/147 tiac_magpie               tests/kernel/sched/deadline/kernel.scheduler.deadline :bgn:`PASSED` (device 4.943s)
         INFO    -  80/147 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.dumb_no_timeslicing :bgn:`PASSED` (device 5.292s)
         INFO    -  81/147 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.dumb_timeslicing :bgn:`PASSED` (device 21.162s)
         INFO    -  82/147 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq_no_timeslicing :bgn:`PASSED` (device 5.297s)
         INFO    -  83/147 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq :bgn:`PASSED` (device 21.072s)
         INFO    -  84/147 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.slice_perthread :bgn:`PASSED` (device 21.848s)
         INFO    -  85/147 tiac_magpie               tests/kernel/smp/kernel.multiprocessing.smp        :byl:`SKIPPED` (runtime filter)
         INFO    -  86/147 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.no_timeslicing :bgn:`PASSED` (device 5.242s)
         INFO    -  87/147 tiac_magpie               tests/kernel/interrupt/arch.interrupt              :bgn:`PASSED` (device 2.414s)
         INFO    -  88/147 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler   :bgn:`PASSED` (device 21.145s)
         INFO    -  89/147 tiac_magpie               tests/kernel/obj_tracking/kernel.objects.tracking  :bgn:`PASSED` (device 3.299s)
         INFO    -  90/147 tiac_magpie               tests/kernel/queue/kernel.queue                    :bgn:`PASSED` (device 4.688s)
         INFO    -  91/147 tiac_magpie               tests/kernel/sleep/kernel.common.timing            :bgn:`PASSED` (device 5.934s)
         INFO    -  92/147 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer.tickless :bgn:`PASSED` (device 7.325s)
         INFO    -  93/147 tiac_magpie               tests/kernel/timer/timer_behavior/kernel.timer.timer :bgn:`PASSED` (device 33.383s)
         INFO    -  94/147 tiac_magpie               tests/kernel/timer/timer_error_case/kernel.timer.error_case :bgn:`PASSED` (device 3.459s)
         INFO    -  95/147 tiac_magpie               tests/kernel/cache/kernel.cache.api                :byl:`SKIPPED` (runtime filter)
         INFO    -  96/147 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer          :bgn:`PASSED` (device 6.616s)
         INFO    -  97/147 tiac_magpie               tests/kernel/timer/timer_monotonic/kernel.timer.monotonic :bgn:`PASSED` (device 4.286s)
         INFO    -  98/147 tiac_magpie               tests/kernel/mem_heap/mheap_api_concept/kernel.memory_heap :bgn:`PASSED` (device 3.103s)
         INFO    -  99/147 tiac_magpie               tests/kernel/mem_heap/k_heap_api/kernel.k_heap_api :bgn:`PASSED` (device 3.171s)
         INFO    - 100/147 tiac_magpie               tests/kernel/fifo/fifo_usage/kernel.fifo.usage     :bgn:`PASSED` (device 3.500s)
         INFO    - 101/147 tiac_magpie               tests/kernel/fifo/fifo_api/kernel.fifo             :bgn:`PASSED` (device 2.966s)
         INFO    - 102/147 tiac_magpie               tests/kernel/fpu_sharing/float_disable/kernel.fpu_sharing.float_disable :bgn:`PASSED` (device 3.761s)
         INFO    - 103/147 tiac_magpie               tests/kernel/fifo/fifo_timeout/kernel.fifo.timeout :bgn:`PASSED` (device 2.648s)
         INFO    - 104/147 tiac_magpie               tests/kernel/early_sleep/kernel.common.sleep       :bgn:`PASSED` (device 3.906s)
         INFO    - 105/147 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls        :bgn:`PASSED` (device 3.768s)
         INFO    - 106/147 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls.userspace :bgn:`PASSED` (device 4.177s)
         INFO    - 107/147 tiac_magpie               tests/kernel/threads/thread_apis/kernel.threads.apis :bgn:`PASSED` (device 9.400s)
         INFO    - 108/147 tiac_magpie               tests/kernel/threads/dynamic_thread/kernel.threads.dynamic :bgn:`PASSED` (device 4.763s)
         INFO    - 109/147 tiac_magpie               tests/kernel/threads/thread_stack/kernel.threads.armv8m_mpu_stack_guard :byl:`SKIPPED` (runtime filter)
         INFO    - 110/147 tiac_magpie               tests/kernel/threads/thread_init/kernel.threads.init :bgn:`PASSED` (device 6.969s)
         INFO    - 111/147 tiac_magpie               tests/kernel/fatal/message_capture/kernel.logging.message_capture :bgn:`PASSED` (device 2.460s)
         INFO    - 112/147 tiac_magpie               tests/kernel/threads/thread_error_case/kernel.threads.error.case :bgn:`PASSED` (device 4.110s)
         INFO    - 113/147 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`SKIPPED` (runtime filter)
         INFO    - 114/147 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_sentinel :bgn:`PASSED` (device 2.625s)
         INFO    - 115/147 tiac_magpie               tests/kernel/threads/thread_stack/kernel.threads.thread_stack :bgn:`PASSED` (device 3.409s)
         INFO    - 116/147 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_no_userspace :bgn:`PASSED` (device 3.588s)
         INFO    - 117/147 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_arm_fpu_sharing :bgn:`PASSED` (device 4.135s)
         INFO    - 118/147 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection :bgn:`PASSED` (device 3.473s)
         INFO    - 119/147 tiac_magpie               tests/kernel/device/kernel.device.pm               :bgn:`PASSED` (device 3.233s)
         INFO    - 120/147 tiac_magpie               tests/kernel/device/kernel.device                  :bgn:`PASSED` (device 3.743s)
         INFO    - 121/147 tiac_magpie               tests/kernel/msgq/msgq_usage/kernel.message_queue_usage :bgn:`PASSED` (device 4.282s)
         INFO    - 122/147 tiac_magpie               tests/kernel/msgq/msgq_api/kernel.message_queue    :bgn:`PASSED` (device 4.454s)
         INFO    - 123/147 tiac_magpie               tests/kernel/mp/kernel.multiprocessing             :byl:`SKIPPED` (runtime filter)
         INFO    - 124/147 tiac_magpie               tests/kernel/condvar/condvar_api/kernel.condvar    :bgn:`PASSED` (device 4.716s)
         INFO    - 125/147 tiac_magpie               tests/kernel/pipe/pipe_api/kernel.pipe.api         :bgn:`PASSED` (device 5.586s)
         INFO    - 126/147 tiac_magpie               tests/kernel/pipe/pipe/kernel.pipe                 :bgn:`PASSED` (device 5.788s)
         INFO    - 127/147 tiac_magpie               tests/kernel/events/event_api/kernel.events        :bgn:`PASSED` (device 3.730s)
         INFO    - 128/147 tiac_magpie               tests/kernel/lifo/lifo_usage/kernel.lifo.usage     :bgn:`PASSED` (device 3.380s)
         INFO    - 129/147 tiac_magpie               tests/kernel/lifo/lifo_api/kernel.lifo             :bgn:`PASSED` (device 3.046s)
         INFO    - 130/147 tiac_magpie               tests/kernel/events/sys_event/kernel.events.usage  :bgn:`PASSED` (device 4.203s)
         INFO    - 131/147 tiac_magpie               tests/kernel/mem_protect/protection/kernel.memory_protection.protection :bgn:`PASSED` (device 2.830s)
         INFO    - 132/147 tiac_magpie               tests/kernel/mem_protect/stack_random/kernel.memory_protection.stack_random :bgn:`PASSED` (device 2.921s)
         INFO    - 133/147 tiac_magpie               tests/kernel/mem_protect/obj_validation/kernel.memory_protection.obj_validation :bgn:`PASSED` (device 3.048s)
         INFO    - 134/147 tiac_magpie               tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot :bgn:`PASSED` (device 4.569s)
         INFO    - 135/147 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem.nouser :bgn:`PASSED` (device 3.270s)
         INFO    - 136/147 tiac_magpie               tests/kernel/mem_protect/syscalls/kernel.memory_protection.syscalls :bgn:`PASSED` (device 18.117s)
         INFO    - 137/147 tiac_magpie               tests/kernel/mem_protect/futex/kernel.futex        :bgn:`PASSED` (device 3.463s)
         INFO    - 138/147 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64 :byl:`SKIPPED` (runtime filter)
         INFO    - 139/147 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem :bgn:`PASSED` (device 3.894s)
         INFO    - 140/147 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map :byl:`SKIPPED` (runtime filter)
         INFO    - 141/147 tiac_magpie               tests/kernel/mem_protect/mem_protect/kernel.memory_protection :bgn:`PASSED` (device 7.617s)
         INFO    - 142/147 tiac_magpie               tests/kernel/mutex/sys_mutex/system.mutex.nouser   :bgn:`PASSED` (device 9.950s)
         INFO    - 143/147 tiac_magpie               tests/kernel/mem_protect/userspace/kernel.memory_protection.userspace :bgn:`PASSED` (device 5.383s)
         INFO    - 144/147 tiac_magpie               tests/kernel/mutex/sys_mutex/system.mutex          :bgn:`PASSED` (device 11.270s)
         INFO    - 145/147 tiac_magpie               tests/kernel/mutex/mutex_api/kernel.mutex          :bgn:`PASSED` (device 15.075s)
         INFO    - 146/147 tiac_magpie               tests/kernel/context/kernel.context                :bgn:`PASSED` (device 7.912s)
         INFO    - 147/147 tiac_magpie               tests/kernel/mutex/mutex_error_case/kernel.mutex_error_case :bgn:`PASSED` (device 3.347s)

         INFO    - 147 test scenarios (147 test instances) selected, 57 configurations skipped (68 by static filter, 10 at runtime).
         INFO    - :bgn:`90 of 147` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`57` skipped with :bbk:`0` warnings in :bbk:`1186.80 seconds`
         INFO    - In total 1077 test cases were executed, 513 skipped on 1 out of total 580 platforms (0.17%)
         INFO    - :bgn:`90` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|        90 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
