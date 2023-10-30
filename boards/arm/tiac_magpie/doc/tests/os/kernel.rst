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

         $ west twister \
             --verbose --jobs 4 --inline-logs \
             --enable-size-report --platform-reports \
             --device-testing --hardware-map map.yaml \
             --alt-config-root bridle/zephyr/alt-config \
             --testsuite-root zephyr/tests --tag kernel --exclude-tag security

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1455/1570 tiac_magpie               tests/kernel/mem_slab/mslab/kernel.memory_slabs    :bgn:`PASSED` (device: DT04BNT1, 3.151s)
         INFO    - 1456/1570 tiac_magpie               tests/kernel/pending/kernel.objects                :bgn:`PASSED` (device: DT04BNT1, 9.578s)
         INFO    - 1457/1570 tiac_magpie               tests/kernel/pending/kernel.objects.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 9.226s)
         INFO    - 1458/1570 tiac_magpie               tests/kernel/mem_slab/mslab_stats/kernel.memory_slabs.stats :bgn:`PASSED` (device: DT04BNT1, 2.608s)
         INFO    - 1459/1570 tiac_magpie               tests/kernel/mem_slab/mslab_threadsafe/kernel.memory_slabs.threadsafe :bgn:`PASSED` (device: DT04BNT1, 3.452s)
         INFO    - 1460/1570 tiac_magpie               tests/kernel/mem_slab/mslab_api/kernel.memory_slabs.api :bgn:`PASSED` (device: DT04BNT1, 9.316s)
         INFO    - 1461/1570 tiac_magpie               tests/kernel/mem_slab/mslab_concept/kernel.memory_slabs.concept :bgn:`PASSED` (device: DT04BNT1, 6.793s)
         INFO    - 1462/1570 tiac_magpie               tests/kernel/stack/stack/kernel.stack.usage        :bgn:`PASSED` (device: DT04BNT1, 5.509s)
         INFO    - 1463/1570 tiac_magpie               tests/kernel/semaphore/semaphore/kernel.semaphore  :bgn:`PASSED` (device: DT04BNT1, 15.577s)
         INFO    - 1464/1570 tiac_magpie               tests/kernel/semaphore/sys_sem/kernel.semaphore.usage :bgn:`PASSED` (device: DT04BNT1, 4.242s)
         INFO    - 1465/1570 tiac_magpie               tests/kernel/common/kernel.common.picolibc         :bgn:`PASSED` (device: DT04BNT1, 8.222s)
         INFO    - 1466/1570 tiac_magpie               tests/kernel/common/kernel.common.misra            :byl:`SKIPPED` (runtime filter)
         INFO    - 1467/1570 tiac_magpie               tests/kernel/common/kernel.common.nano64           :bgn:`PASSED` (device: DT04BNT1, 8.115s)
         INFO    - 1468/1570 tiac_magpie               tests/kernel/common/kernel.common.nano32           :bgn:`PASSED` (device: DT04BNT1, 8.657s)
         INFO    - 1469/1570 tiac_magpie               tests/kernel/common/kernel.common.minimallibc      :bgn:`PASSED` (device: DT04BNT1, 9.097s)
         INFO    - 1470/1570 tiac_magpie               tests/kernel/common/kernel.common.tls              :bgn:`PASSED` (device: DT04BNT1, 8.075s)
         INFO    - 1471/1570 tiac_magpie               tests/kernel/obj_core/obj_core/kernel.obj_core     :bgn:`PASSED` (device: DT04BNT1, 3.974s)
         INFO    - 1472/1570 tiac_magpie               tests/kernel/common/kernel.common                  :bgn:`PASSED` (device: DT04BNT1, 8.002s)
         INFO    - 1473/1570 tiac_magpie               tests/kernel/obj_core/obj_core_stats_api/kernel.obj_core.stats.api :bgn:`PASSED` (device: DT04BNT1, 3.484s)
         INFO    - 1474/1570 tiac_magpie               tests/kernel/obj_core/obj_core_stats/kernel.obj_core.stats :bgn:`PASSED` (device: DT04BNT1, 2.838s)
         INFO    - 1475/1570 tiac_magpie               tests/kernel/usage/thread_runtime_stats/kernel.usage :bgn:`PASSED` (device: DT04BNT1, 3.306s)
         INFO    - 1476/1570 tiac_magpie               tests/kernel/mbox/mbox_api/kernel.mailbox.api      :bgn:`PASSED` (device: DT04BNT1, 3.692s)
         INFO    - 1477/1570 tiac_magpie               tests/kernel/mbox/mbox_usage/kernel.mailbox.usage  :bgn:`PASSED` (device: DT04BNT1, 3.720s)
         INFO    - 1478/1570 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.critical.sam :byl:`SKIPPED` (runtime filter)
         INFO    - 1479/1570 tiac_magpie               tests/kernel/tickless/tickless_concept/kernel.tickless.concept :bgn:`PASSED` (device: DT04BNT1, 3.472s)
         INFO    - 1480/1570 tiac_magpie               tests/kernel/xip/arch.common.xip.minimallibc       :bgn:`PASSED` (device: DT04BNT1, 3.742s)
         INFO    - 1481/1570 tiac_magpie               tests/kernel/xip/arch.common.xip                   :bgn:`PASSED` (device: DT04BNT1, 3.749s)
         INFO    - 1482/1570 tiac_magpie               tests/kernel/workq/work/kernel.workqueue.api       :bgn:`PASSED` (device: DT04BNT1, 5.489s)
         INFO    - 1483/1570 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.critical :bgn:`PASSED` (device: DT04BNT1, 3.738s)
         INFO    - 1484/1570 tiac_magpie               tests/kernel/workq/work_queue/kernel.workqueue     :bgn:`PASSED` (device: DT04BNT1, 7.668s)
         INFO    - 1485/1570 tiac_magpie               tests/kernel/profiling/profiling_api/kernel.common.profiling :bgn:`PASSED` (device: DT04BNT1, 2.586s)
         INFO    - 1486/1570 tiac_magpie               tests/kernel/workq/user_work/kernel.workqueue.user :bgn:`PASSED` (device: DT04BNT1, 3.140s)
         INFO    - 1487/1570 tiac_magpie               tests/kernel/poll/kernel.poll                      :bgn:`PASSED` (device: DT04BNT1, 8.182s)
         INFO    - 1488/1570 tiac_magpie               tests/kernel/poll/kernel.poll.minimallibc          :bgn:`PASSED` (device: DT04BNT1, 6.850s)
         INFO    - 1489/1570 tiac_magpie               tests/kernel/sched/preempt/kernel.scheduler.preempt :bgn:`PASSED` (device: DT04BNT1, 3.465s)
         INFO    - 1490/1570 tiac_magpie               tests/kernel/sched/metairq/kernel.scheduler.metairq :bgn:`PASSED` (device: DT04BNT1, 3.524s)
         INFO    - 1491/1570 tiac_magpie               tests/kernel/sched/deadline/kernel.scheduler.deadline :bgn:`PASSED` (device: DT04BNT1, 4.972s)
         INFO    - 1492/1570 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.dumb_no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 5.515s)
         INFO    - 1493/1570 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq_no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 5.429s)
         INFO    - 1494/1570 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.dumb_timeslicing :bgn:`PASSED` (device: DT04BNT1, 21.229s)
         INFO    - 1495/1570 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq :bgn:`PASSED` (device: DT04BNT1, 22.604s)
         INFO    - 1496/1570 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.slice_perthread :bgn:`PASSED` (device: DT04BNT1, 22.048s)
         INFO    - 1497/1570 tiac_magpie               tests/kernel/interrupt/arch.shared_interrupt       :bgn:`PASSED` (device: DT04BNT1, 2.605s)
         INFO    - 1498/1570 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 5.419s)
         INFO    - 1499/1570 tiac_magpie               tests/kernel/smp/kernel.multiprocessing.smp.minimallibc :byl:`SKIPPED` (runtime filter)
         INFO    - 1500/1570 tiac_magpie               tests/kernel/smp/kernel.multiprocessing.smp        :byl:`SKIPPED` (runtime filter)
         INFO    - 1501/1570 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler   :bgn:`PASSED` (device: DT04BNT1, 21.960s)
         INFO    - 1502/1570 tiac_magpie               tests/kernel/interrupt/arch.interrupt.minimallibc  :bgn:`PASSED` (device: DT04BNT1, 2.486s)
         INFO    - 1503/1570 tiac_magpie               tests/kernel/interrupt/arch.interrupt              :bgn:`PASSED` (device: DT04BNT1, 2.621s)
         INFO    - 1504/1570 tiac_magpie               tests/kernel/obj_tracking/kernel.objects.tracking  :bgn:`PASSED` (device: DT04BNT1, 4.010s)
         INFO    - 1505/1570 tiac_magpie               tests/kernel/obj_tracking/kernel.objects.tracking.minimallibc :bgn:`PASSED` (device: DT04BNT1, 4.750s)
         INFO    - 1506/1570 tiac_magpie               tests/kernel/queue/kernel.queue                    :bgn:`PASSED` (device: DT04BNT1, 4.892s)
         INFO    - 1507/1570 tiac_magpie               tests/kernel/queue/kernel.queue.minimallibc        :bgn:`PASSED` (device: DT04BNT1, 4.942s)
         INFO    - 1508/1570 tiac_magpie               tests/kernel/sleep/kernel.common.timing.minimallibc :bgn:`PASSED` (device: DT04BNT1, 7.113s)
         INFO    - 1509/1570 tiac_magpie               tests/kernel/sleep/kernel.common.timing            :bgn:`PASSED` (device: DT04BNT1, 7.418s)
         INFO    - 1510/1570 tiac_magpie               tests/kernel/timer/timer_behavior/kernel.timer.timer :bgn:`PASSED` (device: DT04BNT1, 34.176s)
         INFO    - 1511/1570 tiac_magpie               tests/kernel/timer/timer_error_case/kernel.timer.error_case :bgn:`PASSED` (device: DT04BNT1, 3.526s)
         INFO    - 1512/1570 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer          :bgn:`PASSED` (device: DT04BNT1, 6.670s)
         INFO    - 1513/1570 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer.tickless :bgn:`PASSED` (device: DT04BNT1, 7.671s)
         INFO    - 1514/1570 tiac_magpie               tests/kernel/cache/kernel.cache.api.minimallibc    :byl:`SKIPPED` (runtime filter)
         INFO    - 1515/1570 tiac_magpie               tests/kernel/timer/timepoints/kernel.timer.timepoints :bgn:`PASSED` (device: DT04BNT1, 4.565s)
         INFO    - 1516/1570 tiac_magpie               tests/kernel/cache/kernel.cache.api                :byl:`SKIPPED` (runtime filter)
         INFO    - 1517/1570 tiac_magpie               tests/kernel/timer/timer_monotonic/kernel.timer.monotonic :bgn:`PASSED` (device: DT04BNT1, 3.826s)
         INFO    - 1518/1570 tiac_magpie               tests/kernel/mem_heap/mheap_api_concept/kernel.memory_heap :bgn:`PASSED` (device: DT04BNT1, 6.037s)
         INFO    - 1519/1570 tiac_magpie               tests/kernel/mem_heap/k_heap_api/kernel.k_heap_api :bgn:`PASSED` (device: DT04BNT1, 4.023s)
         INFO    - 1520/1570 tiac_magpie               tests/kernel/fifo/fifo_usage/kernel.fifo.usage     :bgn:`PASSED` (device: DT04BNT1, 2.810s)
         INFO    - 1521/1570 tiac_magpie               tests/kernel/fifo/fifo_api/kernel.fifo             :bgn:`PASSED` (device: DT04BNT1, 4.296s)
         INFO    - 1522/1570 tiac_magpie               tests/kernel/fpu_sharing/float_disable/kernel.fpu_sharing.float_disable :bgn:`PASSED` (device: DT04BNT1, 3.256s)
         INFO    - 1523/1570 tiac_magpie               tests/kernel/fifo/fifo_timeout/kernel.fifo.timeout :bgn:`PASSED` (device: DT04BNT1, 3.780s)
         INFO    - 1524/1570 tiac_magpie               tests/kernel/early_sleep/kernel.common.sleep.minimallibc :bgn:`PASSED` (device: DT04BNT1, 4.793s)
         INFO    - 1525/1570 tiac_magpie               tests/kernel/early_sleep/kernel.common.sleep       :bgn:`PASSED` (device: DT04BNT1, 3.934s)
         INFO    - 1526/1570 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls        :bgn:`PASSED` (device: DT04BNT1, 4.093s)
         INFO    - 1527/1570 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls.userspace :bgn:`PASSED` (device: DT04BNT1, 4.559s)
         INFO    - 1528/1570 tiac_magpie               tests/kernel/threads/thread_apis/kernel.threads.apis :bgn:`PASSED` (device: DT04BNT1, 9.566s)
         INFO    - 1529/1570 tiac_magpie               tests/kernel/threads/dynamic_thread/kernel.threads.dynamic :bgn:`PASSED` (device: DT04BNT1, 4.992s)
         INFO    - 1530/1570 tiac_magpie               tests/kernel/threads/thread_init/kernel.threads.init :bgn:`PASSED` (device: DT04BNT1, 8.252s)
         INFO    - 1531/1570 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`SKIPPED` (runtime filter)
         INFO    - 1532/1570 tiac_magpie               tests/kernel/fatal/message_capture/kernel.logging.message_capture :bgn:`PASSED` (device: DT04BNT1, 3.415s)
         INFO    - 1533/1570 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_sentinel :bgn:`PASSED` (device: DT04BNT1, 2.670s)
         INFO    - 1534/1570 tiac_magpie               tests/kernel/threads/thread_error_case/kernel.threads.error.case :bgn:`PASSED` (device: DT04BNT1, 3.525s)
         INFO    - 1535/1570 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_no_userspace :bgn:`PASSED` (device: DT04BNT1, 4.710s)
         INFO    - 1536/1570 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_arm_fpu_sharing :bgn:`PASSED` (device: DT04BNT1, 5.212s)
         INFO    - 1537/1570 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection :bgn:`PASSED` (device: DT04BNT1, 3.765s)
         INFO    - 1538/1570 tiac_magpie               tests/kernel/device/kernel.device.pm               :bgn:`PASSED` (device: DT04BNT1, 4.322s)
         INFO    - 1539/1570 tiac_magpie               tests/kernel/device/kernel.device.minimallibc      :bgn:`PASSED` (device: DT04BNT1, 5.609s)
         INFO    - 1540/1570 tiac_magpie               tests/kernel/msgq/msgq_usage/kernel.message_queue.usage :bgn:`PASSED` (device: DT04BNT1, 3.490s)
         INFO    - 1541/1570 tiac_magpie               tests/kernel/device/kernel.device                  :bgn:`PASSED` (device: DT04BNT1, 4.609s)
         INFO    - 1542/1570 tiac_magpie               tests/kernel/msgq/msgq_api/kernel.message_queue    :bgn:`PASSED` (device: DT04BNT1, 5.094s)
         INFO    - 1543/1570 tiac_magpie               tests/kernel/condvar/condvar_api/kernel.condvar    :bgn:`PASSED` (device: DT04BNT1, 5.080s)
         INFO    - 1544/1570 tiac_magpie               tests/kernel/pipe/pipe_api/kernel.pipe.api         :bgn:`PASSED` (device: DT04BNT1, 5.568s)
         INFO    - 1545/1570 tiac_magpie               tests/kernel/pipe/pipe/kernel.pipe                 :bgn:`PASSED` (device: DT04BNT1, 6.106s)
         INFO    - 1546/1570 tiac_magpie               tests/kernel/events/event_api/kernel.events        :bgn:`PASSED` (device: DT04BNT1, 2.850s)
         INFO    - 1547/1570 tiac_magpie               tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot_tls :byl:`SKIPPED` (runtime filter)
         INFO    - 1548/1570 tiac_magpie               tests/kernel/events/sys_event/kernel.events.usage  :bgn:`PASSED` (device: DT04BNT1, 4.167s)
         INFO    - 1549/1570 tiac_magpie               tests/kernel/lifo/lifo_usage/kernel.lifo.usage     :bgn:`PASSED` (device: DT04BNT1, 3.832s)
         INFO    - 1550/1570 tiac_magpie               tests/kernel/lifo/lifo_api/kernel.lifo             :bgn:`PASSED` (device: DT04BNT1, 2.993s)
         INFO    - 1551/1570 tiac_magpie               tests/kernel/mem_protect/stack_random/kernel.memory_protection.stack_random :bgn:`PASSED` (device: DT04BNT1, 3.084s)
         INFO    - 1552/1570 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem.nouser :bgn:`PASSED` (device: DT04BNT1, 3.210s)
         INFO    - 1553/1570 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64 :byl:`SKIPPED` (runtime filter)
         INFO    - 1554/1570 tiac_magpie               tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot :bgn:`PASSED` (device: DT04BNT1, 4.930s)
         INFO    - 1555/1570 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map :byl:`SKIPPED` (runtime filter)
         INFO    - 1556/1570 tiac_magpie               tests/kernel/mem_protect/futex/kernel.futex        :bgn:`PASSED` (device: DT04BNT1, 3.630s)
         INFO    - 1557/1570 tiac_magpie               tests/kernel/mutex/sys_mutex/kernel.mutex.system.nouser :bgn:`PASSED` (device: DT04BNT1, 9.981s)
         INFO    - 1558/1570 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem :bgn:`PASSED` (device: DT04BNT1, 6.262s)
         INFO    - 1559/1570 tiac_magpie               tests/kernel/mutex/mutex_api/kernel.mutex          :bgn:`PASSED` (device: DT04BNT1, 15.332s)
         INFO    - 1560/1570 tiac_magpie               tests/kernel/mutex/sys_mutex/kernel.mutex.system   :bgn:`PASSED` (device: DT04BNT1, 10.590s)
         INFO    - 1561/1570 tiac_magpie               tests/kernel/context/kernel.context.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 8.711s)
         INFO    - 1562/1570 tiac_magpie               tests/kernel/mutex/mutex_error_case/kernel.mutex.error :bgn:`PASSED` (device: DT04BNT1, 4.278s)
         INFO    - 1563/1570 tiac_magpie               tests/benchmarks/latency_measure/benchmark.kernel.latency :byl:`SKIPPED` (runtime filter)
         INFO    - 1564/1570 tiac_magpie               tests/kernel/context/kernel.context                :bgn:`PASSED` (device: DT04BNT1, 9.009s)
         INFO    - 1565/1570 tiac_magpie               tests/lib/p4workq/libraries.p4wq                   :bgn:`PASSED` (device: DT04BNT1, 3.415s)
         INFO    - 1566/1570 tiac_magpie               tests/benchmarks/latency_measure/benchmark.kernel.latency.stm32 :bgn:`PASSED` (device: DT04BNT1, 4.219s)
         INFO    - 1567/1570 tiac_magpie               tests/benchmarks/sys_kernel/benchmark.kernel.core  :bgn:`PASSED` (device: DT04BNT1, 5.653s)
         INFO    - 1568/1570 tiac_magpie               tests/benchmarks/data_structure_perf/dlist_perf/benchmark.data_structure_perf.dlist :bgn:`PASSED` (device: DT04BNT1, 2.494s)
         INFO    - 1569/1570 tiac_magpie               tests/benchmarks/data_structure_perf/rbtree_perf/benchmark.data_structure_perf.rbtree :bgn:`PASSED` (device: DT04BNT1, 3.121s)
         INFO    - 1570/1570 tiac_magpie               tests/benchmarks/app_kernel/benchmark.kernel.application :bgn:`PASSED` (device: DT04BNT1, 9.530s)

         INFO    - 1782 test scenarios (1570 test instances) selected, 1465 configurations skipped (1454 by static filter, 11 at runtime).
         INFO    - :bgn:`105 of 1570` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1465` skipped with :bbk:`0` warnings in :bbk:`1486.94 seconds`
         INFO    - In total 1127 test cases were executed, 9818 skipped on 1 out of total 638 platforms (0.16%)
         INFO    - :bgn:`105` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|       105 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
