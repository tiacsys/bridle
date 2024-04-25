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

         west twister \
              --verbose --jobs 4 --inline-logs \
              --enable-size-report --platform-reports \
              --device-testing --hardware-map map.yaml \
              --alt-config-root bridle/zephyr/alt-config \
              --testsuite-root zephyr/tests --tag kernel --exclude-tag security

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight-console notranslate

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1582/1709 tiac_magpie               tests/kernel/pending/kernel.objects                :bgn:`PASSED` (device: DT04BNT1, 8.439s)
         INFO    - 1583/1709 tiac_magpie               tests/kernel/pending/kernel.objects.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 8.439s)
         INFO    - 1584/1709 tiac_magpie               tests/kernel/mem_slab/mslab/kernel.memory_slabs    :bgn:`PASSED` (device: DT04BNT1, 3.083s)
         INFO    - 1585/1709 tiac_magpie               tests/kernel/mem_slab/mslab_stats/kernel.memory_slabs.stats :bgn:`PASSED` (device: DT04BNT1, 2.447s)
         INFO    - 1586/1709 tiac_magpie               tests/kernel/mem_slab/mslab_threadsafe/kernel.memory_slabs.threadsafe :bgn:`PASSED` (device: DT04BNT1, 2.672s)
         INFO    - 1587/1709 tiac_magpie               tests/kernel/mem_slab/mslab_api/kernel.memory_slabs.api :bgn:`PASSED` (device: DT04BNT1, 9.268s)
         INFO    - 1588/1709 tiac_magpie               tests/kernel/mem_slab/mslab_concept/kernel.memory_slabs.concept :bgn:`PASSED` (device: DT04BNT1, 5.392s)
         INFO    - 1589/1709 tiac_magpie               tests/kernel/stack/stack/kernel.stack.usage        :bgn:`PASSED` (device: DT04BNT1, 5.188s)
         INFO    - 1590/1709 tiac_magpie               tests/kernel/semaphore/semaphore/kernel.semaphore  :bgn:`PASSED` (device: DT04BNT1, 15.576s)
         INFO    - 1591/1709 tiac_magpie               tests/kernel/semaphore/sys_sem/kernel.semaphore.usage :bgn:`PASSED` (device: DT04BNT1, 3.291s)
         INFO    - 1592/1709 tiac_magpie               tests/kernel/common/kernel.common.lto              :bgn:`PASSED` (device: DT04BNT1, 5.216s)
         INFO    - 1593/1709 tiac_magpie               tests/kernel/common/kernel.common.picolibc         :bgn:`PASSED` (device: DT04BNT1, 8.177s)
         INFO    - 1594/1709 tiac_magpie               tests/kernel/common/kernel.common.misra            :byl:`SKIPPED` (runtime filter)
         INFO    - 1595/1709 tiac_magpie               tests/kernel/common/kernel.common.nano64           :bgn:`PASSED` (device: DT04BNT1, 8.121s)
         INFO    - 1596/1709 tiac_magpie               tests/kernel/common/kernel.common.nano32           :bgn:`PASSED` (device: DT04BNT1, 9.101s)
         INFO    - 1597/1709 tiac_magpie               tests/kernel/common/kernel.common.minimallibc      :bgn:`PASSED` (device: DT04BNT1, 9.259s)
         INFO    - 1598/1709 tiac_magpie               tests/kernel/obj_core/obj_core/kernel.obj_core     :bgn:`PASSED` (device: DT04BNT1, 2.771s)
         INFO    - 1599/1709 tiac_magpie               tests/kernel/common/kernel.common.tls              :bgn:`PASSED` (device: DT04BNT1, 8.745s)
         INFO    - 1600/1709 tiac_magpie               tests/kernel/common/kernel.common                  :bgn:`PASSED` (device: DT04BNT1, 8.941s)
         INFO    - 1601/1709 tiac_magpie               tests/kernel/obj_core/obj_core_stats/kernel.obj_core.stats :bgn:`PASSED` (device: DT04BNT1, 2.846s)
         INFO    - 1602/1709 tiac_magpie               tests/kernel/obj_core/obj_core_stats_api/kernel.obj_core.stats.api :bgn:`PASSED` (device: DT04BNT1, 3.305s)
         INFO    - 1603/1709 tiac_magpie               tests/kernel/usage/thread_runtime_stats/kernel.usage :bgn:`PASSED` (device: DT04BNT1, 3.190s)
         INFO    - 1604/1709 tiac_magpie               tests/kernel/mbox/mbox_api/kernel.mailbox.api      :bgn:`PASSED` (device: DT04BNT1, 3.561s)
         INFO    - 1605/1709 tiac_magpie               tests/kernel/mbox/mbox_usage/kernel.mailbox.usage  :bgn:`PASSED` (device: DT04BNT1, 3.169s)
         INFO    - 1606/1709 tiac_magpie               tests/kernel/tickless/tickless_concept/kernel.tickless.concept :bgn:`PASSED` (device: DT04BNT1, 3.487s)
         INFO    - 1607/1709 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.critical.sam :byl:`SKIPPED` (runtime filter)
         INFO    - 1608/1709 tiac_magpie               tests/kernel/xip/arch.common.xip.minimallibc       :bgn:`PASSED` (device: DT04BNT1, 2.587s)
         INFO    - 1609/1709 tiac_magpie               tests/kernel/xip/arch.common.xip                   :bgn:`PASSED` (device: DT04BNT1, 2.617s)
         INFO    - 1610/1709 tiac_magpie               tests/kernel/workq/work/kernel.workqueue.api       :bgn:`PASSED` (device: DT04BNT1, 4.810s)
         INFO    - 1611/1709 tiac_magpie               tests/kernel/workq/work_queue/kernel.workqueue     :bgn:`PASSED` (device: DT04BNT1, 7.215s)
         INFO    - 1612/1709 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.critical :bgn:`PASSED` (device: DT04BNT1, 3.227s)
         INFO    - 1613/1709 tiac_magpie               tests/kernel/profiling/profiling_api/kernel.common.profiling :bgn:`PASSED` (device: DT04BNT1, 2.695s)
         INFO    - 1614/1709 tiac_magpie               tests/kernel/workq/user_work/kernel.workqueue.user :bgn:`PASSED` (device: DT04BNT1, 3.211s)
         INFO    - 1615/1709 tiac_magpie               tests/kernel/poll/kernel.poll.minimallibc          :bgn:`PASSED` (device: DT04BNT1, 7.418s)
         INFO    - 1616/1709 tiac_magpie               tests/kernel/poll/kernel.poll                      :bgn:`PASSED` (device: DT04BNT1, 8.087s)
         INFO    - 1617/1709 tiac_magpie               tests/kernel/sched/preempt/kernel.scheduler.preempt :bgn:`PASSED` (device: DT04BNT1, 3.335s)
         INFO    - 1618/1709 tiac_magpie               tests/kernel/sched/metairq/kernel.scheduler.metairq :bgn:`PASSED` (device: DT04BNT1, 2.662s)
         INFO    - 1619/1709 tiac_magpie               tests/kernel/sched/deadline/kernel.scheduler.deadline :bgn:`PASSED` (device: DT04BNT1, 2.966s)
         INFO    - 1620/1709 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.dumb_no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 5.509s)
         INFO    - 1621/1709 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq_no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 5.557s)
         INFO    - 1622/1709 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.dumb_timeslicing :bgn:`PASSED` (device: DT04BNT1, 21.264s)
         INFO    - 1623/1709 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq :bgn:`PASSED` (device: DT04BNT1, 21.344s)
         INFO    - 1624/1709 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.slice_perthread :bgn:`PASSED` (device: DT04BNT1, 21.283s)
         INFO    - 1625/1709 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 5.489s)
         INFO    - 1626/1709 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler   :bgn:`PASSED` (device: DT04BNT1, 21.299s)
         INFO    - 1627/1709 tiac_magpie               tests/kernel/interrupt/arch.shared_interrupt.lto   :bgn:`PASSED` (device: DT04BNT1, 2.614s)
         INFO    - 1628/1709 tiac_magpie               tests/kernel/interrupt/arch.interrupt.minimallibc  :bgn:`PASSED` (device: DT04BNT1, 2.516s)
         INFO    - 1629/1709 tiac_magpie               tests/kernel/smp/kernel.multiprocessing.smp.minimallibc :byl:`SKIPPED` (runtime filter)
         INFO    - 1630/1709 tiac_magpie               tests/kernel/interrupt/arch.shared_interrupt       :bgn:`PASSED` (device: DT04BNT1, 2.661s)
         INFO    - 1631/1709 tiac_magpie               tests/kernel/smp/kernel.multiprocessing.smp        :byl:`SKIPPED` (runtime filter)
         INFO    - 1632/1709 tiac_magpie               tests/kernel/interrupt/arch.interrupt              :bgn:`PASSED` (device: DT04BNT1, 2.646s)
         INFO    - 1633/1709 tiac_magpie               tests/kernel/obj_tracking/kernel.objects.tracking  :bgn:`PASSED` (device: DT04BNT1, 2.840s)
         INFO    - 1634/1709 tiac_magpie               tests/kernel/obj_tracking/kernel.objects.tracking.minimallibc :bgn:`PASSED` (device: DT04BNT1, 3.629s)
         INFO    - 1635/1709 tiac_magpie               tests/kernel/queue/kernel.queue                    :bgn:`PASSED` (device: DT04BNT1, 4.955s)
         INFO    - 1636/1709 tiac_magpie               tests/kernel/smp_suspend/kernel.smp_suspend        :byl:`SKIPPED` (runtime filter)
         INFO    - 1637/1709 tiac_magpie               tests/kernel/queue/kernel.queue.minimallibc        :bgn:`PASSED` (device: DT04BNT1, 4.981s)
         INFO    - 1638/1709 tiac_magpie               tests/kernel/sleep/kernel.common.timing.minimallibc :bgn:`PASSED` (device: DT04BNT1, 6.102s)
         INFO    - 1639/1709 tiac_magpie               tests/kernel/sleep/kernel.common.timing            :bgn:`PASSED` (device: DT04BNT1, 7.711s)
         INFO    - 1640/1709 tiac_magpie               tests/kernel/timer/timer_behavior/kernel.timer.timer :bgn:`PASSED` (device: DT04BNT1, 33.734s)
         INFO    - 1641/1709 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer.tickless :bgn:`PASSED` (device: DT04BNT1, 6.675s)
         INFO    - 1642/1709 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer          :bgn:`PASSED` (device: DT04BNT1, 7.513s)
         INFO    - 1643/1709 tiac_magpie               tests/kernel/timer/timer_error_case/kernel.timer.error_case :bgn:`PASSED` (device: DT04BNT1, 4.477s)
         INFO    - 1644/1709 tiac_magpie               tests/kernel/timer/timepoints/kernel.timer.timepoints :bgn:`PASSED` (device: DT04BNT1, 3.541s)
         INFO    - 1645/1709 tiac_magpie               tests/kernel/timer/timer_monotonic/kernel.timer.monotonic :bgn:`PASSED` (device: DT04BNT1, 5.121s)
         INFO    - 1646/1709 tiac_magpie               tests/kernel/mem_heap/k_heap_api/kernel.k_heap_api :bgn:`PASSED` (device: DT04BNT1, 2.787s)
         INFO    - 1647/1709 tiac_magpie               tests/kernel/cache/kernel.cache.api.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 3.138s)
         INFO    - 1648/1709 tiac_magpie               tests/kernel/cache/kernel.cache.api                :bgn:`PASSED` (device: DT04BNT1, 3.282s)
         INFO    - 1649/1709 tiac_magpie               tests/kernel/fifo/fifo_usage/kernel.fifo.usage     :bgn:`PASSED` (device: DT04BNT1, 2.603s)
         INFO    - 1650/1709 tiac_magpie               tests/kernel/fpu_sharing/float_disable/kernel.fpu_sharing.float_disable :bgn:`PASSED` (device: DT04BNT1, 3.950s)
         INFO    - 1651/1709 tiac_magpie               tests/kernel/fifo/fifo_api/kernel.fifo             :bgn:`PASSED` (device: DT04BNT1, 4.230s)
         INFO    - 1652/1709 tiac_magpie               tests/kernel/fifo/fifo_timeout/kernel.fifo.timeout :bgn:`PASSED` (device: DT04BNT1, 2.671s)
         INFO    - 1653/1709 tiac_magpie               tests/kernel/early_sleep/kernel.common.sleep       :bgn:`PASSED` (device: DT04BNT1, 4.595s)
         INFO    - 1654/1709 tiac_magpie               tests/kernel/early_sleep/kernel.common.sleep.minimallibc :bgn:`PASSED` (device: DT04BNT1, 3.994s)
         INFO    - 1655/1709 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls        :bgn:`PASSED` (device: DT04BNT1, 4.425s)
         INFO    - 1656/1709 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls.userspace :bgn:`PASSED` (device: DT04BNT1, 3.628s)
         INFO    - 1657/1709 tiac_magpie               tests/kernel/threads/thread_apis/kernel.threads.apis :bgn:`PASSED` (device: DT04BNT1, 9.444s)
         INFO    - 1658/1709 tiac_magpie               tests/kernel/threads/dynamic_thread/kernel.threads.dynamic :bgn:`PASSED` (device: DT04BNT1, 5.307s)
         INFO    - 1659/1709 tiac_magpie               tests/kernel/threads/thread_init/kernel.threads.init :bgn:`PASSED` (device: DT04BNT1, 7.167s)
         INFO    - 1660/1709 tiac_magpie               tests/kernel/fatal/message_capture/kernel.logging.message_capture :bgn:`PASSED` (device: DT04BNT1, 3.478s)
         INFO    - 1661/1709 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`SKIPPED` (runtime filter)
         INFO    - 1662/1709 tiac_magpie               tests/kernel/threads/thread_error_case/kernel.threads.error.case :bgn:`PASSED` (device: DT04BNT1, 4.120s)
         INFO    - 1663/1709 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_sentinel :bgn:`PASSED` (device: DT04BNT1, 2.751s)
         INFO    - 1664/1709 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_no_userspace :bgn:`PASSED` (device: DT04BNT1, 4.983s)
         INFO    - 1665/1709 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_arm_fpu_sharing :bgn:`PASSED` (device: DT04BNT1, 4.947s)
         INFO    - 1666/1709 tiac_magpie               tests/kernel/device/kernel.device.pm               :bgn:`PASSED` (device: DT04BNT1, 5.040s)
         INFO    - 1667/1709 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection :bgn:`PASSED` (device: DT04BNT1, 4.591s)
         INFO    - 1668/1709 tiac_magpie               tests/kernel/device/kernel.device.minimallibc      :bgn:`PASSED` (device: DT04BNT1, 4.732s)
         INFO    - 1669/1709 tiac_magpie               tests/kernel/msgq/msgq_usage/kernel.message_queue.usage :bgn:`PASSED` (device: DT04BNT1, 3.540s)
         INFO    - 1670/1709 tiac_magpie               tests/kernel/device/kernel.device                  :bgn:`PASSED` (device: DT04BNT1, 5.165s)
         INFO    - 1671/1709 tiac_magpie               tests/kernel/msgq/msgq_api/kernel.message_queue    :bgn:`PASSED` (device: DT04BNT1, 5.104s)
         INFO    - 1672/1709 tiac_magpie               tests/kernel/condvar/condvar_api/kernel.condvar    :bgn:`PASSED` (device: DT04BNT1, 5.979s)
         INFO    - 1673/1709 tiac_magpie               tests/kernel/pipe/pipe_api/kernel.pipe.api         :bgn:`PASSED` (device: DT04BNT1, 6.834s)
         INFO    - 1674/1709 tiac_magpie               tests/kernel/pipe/pipe/kernel.pipe                 :bgn:`PASSED` (device: DT04BNT1, 6.262s)
         INFO    - 1675/1709 tiac_magpie               tests/kernel/events/event_api/kernel.events        :bgn:`PASSED` (device: DT04BNT1, 3.008s)
         INFO    - 1676/1709 tiac_magpie               tests/kernel/events/sys_event/kernel.events.usage  :bgn:`PASSED` (device: DT04BNT1, 5.890s)
         INFO    - 1677/1709 tiac_magpie               tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot_tls :byl:`SKIPPED` (runtime filter)
         INFO    - 1678/1709 tiac_magpie               tests/kernel/lifo/lifo_usage/kernel.lifo.usage     :bgn:`PASSED` (device: DT04BNT1, 4.078s)
         INFO    - 1679/1709 tiac_magpie               tests/kernel/lifo/lifo_api/kernel.lifo             :bgn:`PASSED` (device: DT04BNT1, 3.013s)
         INFO    - 1680/1709 tiac_magpie               tests/kernel/mem_protect/stack_random/kernel.memory_protection.stack_random :bgn:`PASSED` (device: DT04BNT1, 3.128s)
         INFO    - 1681/1709 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem.nouser :bgn:`PASSED` (device: DT04BNT1, 4.451s)
         INFO    - 1682/1709 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64 :byl:`SKIPPED` (runtime filter)
         INFO    - 1683/1709 tiac_magpie               tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot :bgn:`PASSED` (device: DT04BNT1, 5.017s)
         INFO    - 1684/1709 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map :byl:`SKIPPED` (runtime filter)
         INFO    - 1685/1709 tiac_magpie               tests/kernel/mem_protect/futex/kernel.futex        :bgn:`PASSED` (device: DT04BNT1, 3.679s)
         INFO    - 1686/1709 tiac_magpie               tests/kernel/mutex/sys_mutex/kernel.mutex.system.nouser :bgn:`PASSED` (device: DT04BNT1, 10.054s)
         INFO    - 1687/1709 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem :bgn:`PASSED` (device: DT04BNT1, 6.393s)
         INFO    - 1688/1709 tiac_magpie               tests/kernel/mutex/mutex_api/kernel.mutex          :bgn:`PASSED` (device: DT04BNT1, 16.930s)
         INFO    - 1689/1709 tiac_magpie               tests/kernel/mutex/mutex_error_case/kernel.mutex.error :bgn:`PASSED` (device: DT04BNT1, 3.389s)
         INFO    - 1690/1709 tiac_magpie               tests/kernel/context/kernel.context.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 8.018s)
         INFO    - 1691/1709 tiac_magpie               tests/kernel/mutex/sys_mutex/kernel.mutex.system   :bgn:`PASSED` (device: DT04BNT1, 11.679s)
         INFO    - 1692/1709 tiac_magpie               tests/benchmarks/latency_measure/benchmark.kernel.latency.timeslicing :byl:`SKIPPED` (runtime filter)
         INFO    - 1693/1709 tiac_magpie               tests/kernel/context/kernel.context                :bgn:`PASSED` (device: DT04BNT1, 8.205s)
         INFO    - 1694/1709 tiac_magpie               tests/lib/p4workq/libraries.p4wq                   :bgn:`PASSED` (device: DT04BNT1, 3.795s)
         INFO    - 1695/1709 tiac_magpie               tests/benchmarks/latency_measure/benchmark.kernel.latency.timeslicing.userspace :bgn:`PASSED` (device: DT04BNT1, 6.794s)
         INFO    - 1696/1709 tiac_magpie               tests/benchmarks/latency_measure/benchmark.kernel.latency.stm32 :bgn:`PASSED` (device: DT04BNT1, 3.184s)
         INFO    - 1697/1709 tiac_magpie               tests/benchmarks/latency_measure/benchmark.kernel.latency.objcore.stats :byl:`SKIPPED` (runtime filter)
         INFO    - 1698/1709 tiac_magpie               tests/benchmarks/latency_measure/benchmark.kernel.latency :byl:`SKIPPED` (runtime filter)
         INFO    - 1699/1709 tiac_magpie               tests/benchmarks/latency_measure/benchmark.kernel.latency.userspace.objcore.stats :bgn:`PASSED` (device: DT04BNT1, 7.396s)
         INFO    - 1700/1709 tiac_magpie               tests/benchmarks/latency_measure/benchmark.kernel.latency.userspace :bgn:`PASSED` (device: DT04BNT1, 7.416s)
         INFO    - 1701/1709 tiac_magpie               tests/benchmarks/sys_kernel/benchmark.kernel.core  :bgn:`PASSED` (device: DT04BNT1, 5.316s)
         INFO    - 1702/1709 tiac_magpie               tests/benchmarks/data_structure_perf/dlist_perf/benchmark.data_structure_perf.dlist :bgn:`PASSED` (device: DT04BNT1, 3.482s)
         INFO    - 1703/1709 tiac_magpie               tests/benchmarks/data_structure_perf/rbtree_perf/benchmark.data_structure_perf.rbtree :bgn:`PASSED` (device: DT04BNT1, 2.755s)
         INFO    - 1704/1709 tiac_magpie               tests/benchmarks/app_kernel/benchmark.kernel.application.timeslicing :bgn:`PASSED` (device: DT04BNT1, 4.350s)
         INFO    - 1705/1709 tiac_magpie               tests/benchmarks/app_kernel/benchmark.kernel.application.user.timeslicing :bgn:`PASSED` (device: DT04BNT1, 8.643s)
         INFO    - 1706/1709 tiac_magpie               tests/benchmarks/app_kernel/benchmark.kernel.application.objcore.stats :bgn:`PASSED` (device: DT04BNT1, 3.593s)
         INFO    - 1707/1709 tiac_magpie               tests/benchmarks/app_kernel/benchmark.kernel.application.user :bgn:`PASSED` (device: DT04BNT1, 8.215s)
         INFO    - 1708/1709 tiac_magpie               tests/benchmarks/app_kernel/benchmark.kernel.application.user.objcore.stats :bgn:`PASSED` (device: DT04BNT1, 11.182s)
         INFO    - 1709/1709 tiac_magpie               tests/benchmarks/app_kernel/benchmark.kernel.application :bgn:`PASSED` (device: DT04BNT1, 3.760s)

         INFO    - 1922 test scenarios (1709 test instances) selected, 1593 configurations skipped (1581 by static filter, 12 at runtime).
         INFO    - :bgn:`116 of 1709` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1593` skipped with :bbk:`0` warnings in :bbk:`1376.20 seconds`
         INFO    - In total 1192 test cases were executed, 11469 skipped on 1 out of total 699 platforms (0.14%)
         INFO    - :bgn:`116` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|       116 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
