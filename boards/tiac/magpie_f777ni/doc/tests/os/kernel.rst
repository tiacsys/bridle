.. _magpie_f777ni_kernel-tests:

Zephyr OS Kernel
################

Overview
********

See :zephyr_file:`tests/kernel`
for the original scope of tests, its structure and description.

.. _magpie_f777ni_kernel-tests-requirements:

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
              --alt-config-root bridle/zephyr/alt-config/tests \
              --testsuite-root zephyr/tests --tag kernel --exclude-tag security

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight-console notranslate

         Device testing on:

         \| Platform      \| ID       \| Serial device   \|
         \|---------------\|----------\|-----------------\|
         \| magpie_f777ni \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1653/1780 magpie_f777ni             tests/kernel/pending/kernel.objects                :bgn:`PASSED` (device: DT04BNT1, 8.454s)
         INFO    - 1654/1780 magpie_f777ni             tests/kernel/mem_slab/mslab/kernel.memory_slabs    :bgn:`PASSED` (device: DT04BNT1, 3.288s)
         INFO    - 1655/1780 magpie_f777ni             tests/kernel/pending/kernel.objects.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 8.413s)
         INFO    - 1656/1780 magpie_f777ni             tests/kernel/mem_slab/mslab_stats/kernel.memory_slabs.stats :bgn:`PASSED` (device: DT04BNT1, 3.647s)
         INFO    - 1657/1780 magpie_f777ni             tests/kernel/mem_slab/mslab_threadsafe/kernel.memory_slabs.threadsafe :bgn:`PASSED` (device: DT04BNT1, 3.378s)
         INFO    - 1658/1780 magpie_f777ni             tests/kernel/mem_slab/mslab_api/kernel.memory_slabs.api :bgn:`PASSED` (device: DT04BNT1, 8.543s)
         INFO    - 1659/1780 magpie_f777ni             tests/kernel/mem_slab/mslab_concept/kernel.memory_slabs.concept :bgn:`PASSED` (device: DT04BNT1, 6.660s)
         INFO    - 1660/1780 magpie_f777ni             tests/kernel/stack/stack/kernel.stack.usage        :bgn:`PASSED` (device: DT04BNT1, 5.506s)
         INFO    - 1661/1780 magpie_f777ni             tests/kernel/semaphore/semaphore/kernel.semaphore  :bgn:`PASSED` (device: DT04BNT1, 16.420s)
         INFO    - 1662/1780 magpie_f777ni             tests/kernel/common/kernel.common.lto              :bgn:`PASSED` (device: DT04BNT1, 5.971s)
         INFO    - 1663/1780 magpie_f777ni             tests/kernel/semaphore/sys_sem/kernel.semaphore.usage :bgn:`PASSED` (device: DT04BNT1, 4.730s)
         INFO    - 1664/1780 magpie_f777ni             tests/kernel/common/kernel.common.picolibc         :bgn:`PASSED` (device: DT04BNT1, 10.262s)
         INFO    - 1665/1780 magpie_f777ni             tests/kernel/common/kernel.common.misra            :byl:`SKIPPED` (runtime filter)
         INFO    - 1666/1780 magpie_f777ni             tests/kernel/common/kernel.common.nano64           :bgn:`PASSED` (device: DT04BNT1, 8.273s)
         INFO    - 1667/1780 magpie_f777ni             tests/kernel/common/kernel.common.minimallibc      :bgn:`PASSED` (device: DT04BNT1, 8.177s)
         INFO    - 1668/1780 magpie_f777ni             tests/kernel/common/kernel.common.nano32           :bgn:`PASSED` (device: DT04BNT1, 9.303s)
         INFO    - 1669/1780 magpie_f777ni             tests/kernel/obj_core/obj_core/kernel.obj_core     :bgn:`PASSED` (device: DT04BNT1, 3.591s)
         INFO    - 1670/1780 magpie_f777ni             tests/kernel/obj_core/obj_core_stats_api/kernel.obj_core.stats.api :bgn:`PASSED` (device: DT04BNT1, 2.680s)
         INFO    - 1671/1780 magpie_f777ni             tests/kernel/common/kernel.common.tls              :bgn:`PASSED` (device: DT04BNT1, 8.204s)
         INFO    - 1672/1780 magpie_f777ni             tests/kernel/common/kernel.common                  :bgn:`PASSED` (device: DT04BNT1, 9.554s)
         INFO    - 1673/1780 magpie_f777ni             tests/kernel/obj_core/obj_core_stats/kernel.obj_core.stats :bgn:`PASSED` (device: DT04BNT1, 2.907s)
         INFO    - 1674/1780 magpie_f777ni             tests/kernel/mbox/mbox_api/kernel.mailbox.api      :bgn:`PASSED` (device: DT04BNT1, 3.301s)
         INFO    - 1675/1780 magpie_f777ni             tests/kernel/usage/thread_runtime_stats/kernel.usage :bgn:`PASSED` (device: DT04BNT1, 3.537s)
         INFO    - 1676/1780 magpie_f777ni             tests/kernel/mbox/mbox_usage/kernel.mailbox.usage  :bgn:`PASSED` (device: DT04BNT1, 3.626s)
         INFO    - 1677/1780 magpie_f777ni             tests/kernel/tickless/tickless_concept/kernel.tickless.concept :bgn:`PASSED` (device: DT04BNT1, 3.470s)
         INFO    - 1678/1780 magpie_f777ni             tests/kernel/workq/critical/kernel.workqueue.critical.sam :byl:`SKIPPED` (runtime filter)
         INFO    - 1679/1780 magpie_f777ni             tests/kernel/xip/arch.common.xip.minimallibc       :bgn:`PASSED` (device: DT04BNT1, 2.672s)
         INFO    - 1680/1780 magpie_f777ni             tests/kernel/xip/arch.common.xip                   :bgn:`PASSED` (device: DT04BNT1, 4.082s)
         INFO    - 1681/1780 magpie_f777ni             tests/kernel/workq/work/kernel.workqueue.api       :bgn:`PASSED` (device: DT04BNT1, 5.799s)
         INFO    - 1682/1780 magpie_f777ni             tests/kernel/workq/critical/kernel.workqueue.critical :bgn:`PASSED` (device: DT04BNT1, 3.814s)
         INFO    - 1683/1780 magpie_f777ni             tests/kernel/workq/work_queue/kernel.workqueue     :bgn:`PASSED` (device: DT04BNT1, 7.227s)
         INFO    - 1684/1780 magpie_f777ni             tests/kernel/profiling/profiling_api/kernel.common.profiling :bgn:`PASSED` (device: DT04BNT1, 2.640s)
         INFO    - 1685/1780 magpie_f777ni             tests/kernel/workq/user_work/kernel.workqueue.user :bgn:`PASSED` (device: DT04BNT1, 3.174s)
         INFO    - 1686/1780 magpie_f777ni             tests/kernel/poll/kernel.poll                      :bgn:`PASSED` (device: DT04BNT1, 7.371s)
         INFO    - 1687/1780 magpie_f777ni             tests/kernel/poll/kernel.poll.minimallibc          :bgn:`PASSED` (device: DT04BNT1, 8.543s)
         INFO    - 1688/1780 magpie_f777ni             tests/kernel/sched/preempt/kernel.scheduler.preempt :bgn:`PASSED` (device: DT04BNT1, 3.658s)
         INFO    - 1689/1780 magpie_f777ni             tests/kernel/sched/metairq/kernel.scheduler.metairq :bgn:`PASSED` (device: DT04BNT1, 3.677s)
         INFO    - 1690/1780 magpie_f777ni             tests/kernel/sched/deadline/kernel.scheduler.deadline.scalable :bgn:`PASSED` (device: DT04BNT1, 5.329s)
         INFO    - 1691/1780 magpie_f777ni             tests/kernel/sched/deadline/kernel.scheduler.deadline :bgn:`PASSED` (device: DT04BNT1, 4.430s)
         INFO    - 1692/1780 magpie_f777ni             tests/kernel/sched/schedule_api/kernel.scheduler.dumb_no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 5.553s)
         INFO    - 1693/1780 magpie_f777ni             tests/kernel/sched/schedule_api/kernel.scheduler.dumb_timeslicing :bgn:`PASSED` (device: DT04BNT1, 21.373s)
         INFO    - 1694/1780 magpie_f777ni             tests/kernel/sched/schedule_api/kernel.scheduler.multiq :bgn:`PASSED` (device: DT04BNT1, 22.279s)
         INFO    - 1695/1780 magpie_f777ni             tests/kernel/sched/schedule_api/kernel.scheduler.multiq_no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 6.492s)
         INFO    - 1696/1780 magpie_f777ni             tests/kernel/sched/schedule_api/kernel.scheduler.slice_perthread :bgn:`PASSED` (device: DT04BNT1, 22.093s)
         INFO    - 1697/1780 magpie_f777ni             tests/kernel/sched/schedule_api/kernel.scheduler.no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 7.177s)
         INFO    - 1698/1780 magpie_f777ni             tests/kernel/interrupt/arch.shared_interrupt.lto   :bgn:`PASSED` (device: DT04BNT1, 2.649s)
         INFO    - 1699/1780 magpie_f777ni             tests/kernel/sched/schedule_api/kernel.scheduler   :bgn:`PASSED` (device: DT04BNT1, 23.465s)
         INFO    - 1700/1780 magpie_f777ni             tests/kernel/interrupt/arch.shared_interrupt       :bgn:`PASSED` (device: DT04BNT1, 3.533s)
         INFO    - 1701/1780 magpie_f777ni             tests/kernel/interrupt/arch.interrupt.minimallibc  :bgn:`PASSED` (device: DT04BNT1, 3.446s)
         INFO    - 1702/1780 magpie_f777ni             tests/kernel/interrupt/arch.interrupt              :bgn:`PASSED` (device: DT04BNT1, 2.593s)
         INFO    - 1703/1780 magpie_f777ni             tests/kernel/smp/kernel.multiprocessing.smp.minimallibc :byl:`SKIPPED` (runtime filter)
         INFO    - 1704/1780 magpie_f777ni             tests/kernel/smp/kernel.multiprocessing.smp        :byl:`SKIPPED` (runtime filter)
         INFO    - 1705/1780 magpie_f777ni             tests/kernel/obj_tracking/kernel.objects.tracking  :bgn:`PASSED` (device: DT04BNT1, 4.922s)
         INFO    - 1706/1780 magpie_f777ni             tests/kernel/obj_tracking/kernel.objects.tracking.minimallibc :bgn:`PASSED` (device: DT04BNT1, 3.422s)
         INFO    - 1707/1780 magpie_f777ni             tests/kernel/queue/kernel.queue                    :bgn:`PASSED` (device: DT04BNT1, 5.874s)
         INFO    - 1708/1780 magpie_f777ni             tests/kernel/smp_suspend/kernel.smp_suspend        :byl:`SKIPPED` (runtime filter)
         INFO    - 1709/1780 magpie_f777ni             tests/kernel/queue/kernel.queue.minimallibc        :bgn:`PASSED` (device: DT04BNT1, 5.468s)
         INFO    - 1710/1780 magpie_f777ni             tests/kernel/sleep/kernel.common.timing            :bgn:`PASSED` (device: DT04BNT1, 6.170s)
         INFO    - 1711/1780 magpie_f777ni             tests/kernel/sleep/kernel.common.timing.minimallibc :bgn:`PASSED` (device: DT04BNT1, 8.387s)
         INFO    - 1712/1780 magpie_f777ni             tests/kernel/timer/timer_behavior/kernel.timer.timer :bgn:`PASSED` (device: DT04BNT1, 33.145s)
         INFO    - 1713/1780 magpie_f777ni             tests/kernel/timer/timer_api/kernel.timer          :bgn:`PASSED` (device: DT04BNT1, 6.701s)
         INFO    - 1714/1780 magpie_f777ni             tests/kernel/timer/timepoints/kernel.timer.timepoints :bgn:`PASSED` (device: DT04BNT1, 3.564s)
         INFO    - 1715/1780 magpie_f777ni             tests/kernel/timer/timer_error_case/kernel.timer.error_case :bgn:`PASSED` (device: DT04BNT1, 4.534s)
         INFO    - 1716/1780 magpie_f777ni             tests/kernel/timer/timer_monotonic/kernel.timer.monotonic :bgn:`PASSED` (device: DT04BNT1, 5.599s)
         INFO    - 1717/1780 magpie_f777ni             tests/kernel/mem_heap/k_heap_api/kernel.k_heap_api :bgn:`PASSED` (device: DT04BNT1, 2.754s)
         INFO    - 1718/1780 magpie_f777ni             tests/kernel/cache/kernel.cache.api.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 3.181s)
         INFO    - 1719/1780 magpie_f777ni             tests/kernel/cache/kernel.cache.api                :bgn:`PASSED` (device: DT04BNT1, 4.352s)
         INFO    - 1720/1780 magpie_f777ni             tests/kernel/fpu_sharing/float_disable/kernel.fpu_sharing.float_disable :bgn:`PASSED` (device: DT04BNT1, 4.470s)
         INFO    - 1721/1780 magpie_f777ni             tests/kernel/fifo/fifo_usage/kernel.fifo.usage     :bgn:`PASSED` (device: DT04BNT1, 2.480s)
         INFO    - 1722/1780 magpie_f777ni             tests/kernel/fifo/fifo_api/kernel.fifo             :bgn:`PASSED` (device: DT04BNT1, 3.164s)
         INFO    - 1723/1780 magpie_f777ni             tests/kernel/fifo/fifo_timeout/kernel.fifo.timeout :bgn:`PASSED` (device: DT04BNT1, 3.867s)
         INFO    - 1724/1780 magpie_f777ni             tests/kernel/early_sleep/kernel.common.sleep       :bgn:`PASSED` (device: DT04BNT1, 5.016s)
         INFO    - 1725/1780 magpie_f777ni             tests/kernel/early_sleep/kernel.common.sleep.minimallibc :bgn:`PASSED` (device: DT04BNT1, 3.951s)
         INFO    - 1726/1780 magpie_f777ni             tests/kernel/threads/tls/kernel.threads.tls        :bgn:`PASSED` (device: DT04BNT1, 4.664s)
         INFO    - 1727/1780 magpie_f777ni             tests/kernel/threads/tls/kernel.threads.tls.userspace :bgn:`PASSED` (device: DT04BNT1, 5.286s)
         INFO    - 1728/1780 magpie_f777ni             tests/kernel/threads/thread_apis/kernel.threads.apis :bgn:`PASSED` (device: DT04BNT1, 10.402s)
         INFO    - 1729/1780 magpie_f777ni             tests/kernel/threads/dynamic_thread/kernel.threads.dynamic :bgn:`PASSED` (device: DT04BNT1, 4.150s)
         INFO    - 1730/1780 magpie_f777ni             tests/kernel/threads/thread_init/kernel.threads.init :bgn:`PASSED` (device: DT04BNT1, 8.352s)
         INFO    - 1731/1780 magpie_f777ni             tests/kernel/fatal/exception/kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`SKIPPED` (runtime filter)
         INFO    - 1732/1780 magpie_f777ni             tests/kernel/fatal/message_capture/kernel.logging.message_capture :bgn:`PASSED` (device: DT04BNT1, 3.630s)
         INFO    - 1733/1780 magpie_f777ni             tests/kernel/fatal/exception/kernel.common.stack_sentinel :bgn:`PASSED` (device: DT04BNT1, 2.719s)
         INFO    - 1734/1780 magpie_f777ni             tests/kernel/threads/thread_error_case/kernel.threads.error.case :bgn:`PASSED` (device: DT04BNT1, 3.516s)
         INFO    - 1735/1780 magpie_f777ni             tests/kernel/fatal/exception/kernel.common.stack_protection_no_userspace :bgn:`PASSED` (device: DT04BNT1, 5.333s)
         INFO    - 1736/1780 magpie_f777ni             tests/kernel/fatal/exception/kernel.common.stack_protection_arm_fpu_sharing :bgn:`PASSED` (device: DT04BNT1, 4.167s)
         INFO    - 1737/1780 magpie_f777ni             tests/kernel/fatal/exception/kernel.common.stack_protection :bgn:`PASSED` (device: DT04BNT1, 4.638s)
         INFO    - 1738/1780 magpie_f777ni             tests/kernel/device/kernel.device.pm               :bgn:`PASSED` (device: DT04BNT1, 4.993s)
         INFO    - 1739/1780 magpie_f777ni             tests/kernel/msgq/msgq_usage/kernel.message_queue.usage :bgn:`PASSED` (device: DT04BNT1, 3.561s)
         INFO    - 1740/1780 magpie_f777ni             tests/kernel/device/kernel.device.minimallibc      :bgn:`PASSED` (device: DT04BNT1, 4.057s)
         INFO    - 1741/1780 magpie_f777ni             tests/kernel/device/kernel.device                  :bgn:`PASSED` (device: DT04BNT1, 4.786s)
         INFO    - 1742/1780 magpie_f777ni             tests/kernel/msgq/msgq_api/kernel.message_queue    :bgn:`PASSED` (device: DT04BNT1, 5.137s)
         INFO    - 1743/1780 magpie_f777ni             tests/kernel/condvar/condvar_api/kernel.condvar    :bgn:`PASSED` (device: DT04BNT1, 6.058s)
         INFO    - 1744/1780 magpie_f777ni             tests/kernel/pipe/pipe_api/kernel.pipe.api         :bgn:`PASSED` (device: DT04BNT1, 5.691s)
         INFO    - 1745/1780 magpie_f777ni             tests/kernel/pipe/pipe/kernel.pipe                 :bgn:`PASSED` (device: DT04BNT1, 5.895s)
         INFO    - 1746/1780 magpie_f777ni             tests/kernel/events/event_api/kernel.events        :bgn:`PASSED` (device: DT04BNT1, 2.927s)
         INFO    - 1747/1780 magpie_f777ni             tests/kernel/events/sys_event/kernel.events.usage  :bgn:`PASSED` (device: DT04BNT1, 4.362s)
         INFO    - 1748/1780 magpie_f777ni             tests/kernel/lifo/lifo_usage/kernel.lifo.usage     :bgn:`PASSED` (device: DT04BNT1, 4.080s)
         INFO    - 1749/1780 magpie_f777ni             tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot_tls :byl:`SKIPPED` (runtime filter)
         INFO    - 1750/1780 magpie_f777ni             tests/kernel/lifo/lifo_api/kernel.lifo             :bgn:`PASSED` (device: DT04BNT1, 3.048s)
         INFO    - 1751/1780 magpie_f777ni             tests/kernel/mem_protect/stack_random/kernel.memory_protection.stack_random :bgn:`PASSED` (device: DT04BNT1, 4.187s)
         INFO    - 1752/1780 magpie_f777ni             tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem.nouser :bgn:`PASSED` (device: DT04BNT1, 4.317s)
         INFO    - 1753/1780 magpie_f777ni             tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64 :byl:`SKIPPED` (runtime filter)
         INFO    - 1754/1780 magpie_f777ni             tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot :bgn:`PASSED` (device: DT04BNT1, 4.085s)
         INFO    - 1755/1780 magpie_f777ni             tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map :byl:`SKIPPED` (runtime filter)
         INFO    - 1756/1780 magpie_f777ni             tests/kernel/mem_protect/futex/kernel.futex        :bgn:`PASSED` (device: DT04BNT1, 4.771s)
         INFO    - 1757/1780 magpie_f777ni             tests/kernel/mutex/sys_mutex/kernel.mutex.system.nouser :bgn:`PASSED` (device: DT04BNT1, 10.056s)
         INFO    - 1758/1780 magpie_f777ni             tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem :bgn:`PASSED` (device: DT04BNT1, 5.161s)
         INFO    - 1759/1780 magpie_f777ni             tests/kernel/mutex/mutex_api/kernel.mutex          :bgn:`PASSED` (device: DT04BNT1, 16.163s)
         INFO    - 1760/1780 magpie_f777ni             tests/kernel/mutex/sys_mutex/kernel.mutex.system   :bgn:`PASSED` (device: DT04BNT1, 11.564s)
         INFO    - 1761/1780 magpie_f777ni             tests/kernel/context/kernel.context.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 8.471s)
         INFO    - 1762/1780 magpie_f777ni             tests/kernel/mutex/mutex_error_case/kernel.mutex.error :bgn:`PASSED` (device: DT04BNT1, 3.460s)
         INFO    - 1763/1780 magpie_f777ni             tests/kernel/context/kernel.context                :bgn:`PASSED` (device: DT04BNT1, 9.066s)
         INFO    - 1764/1780 magpie_f777ni             tests/benchmarks/latency_measure/benchmark.kernel.latency.timeslicing :byl:`SKIPPED` (runtime filter)
         INFO    - 1765/1780 magpie_f777ni             tests/lib/p4workq/libraries.p4wq                   :bgn:`PASSED` (device: DT04BNT1, 2.914s)
         INFO    - 1766/1780 magpie_f777ni             tests/benchmarks/latency_measure/benchmark.kernel.latency.stm32 :bgn:`PASSED` (device: DT04BNT1, 3.307s)
         INFO    - 1767/1780 magpie_f777ni             tests/benchmarks/latency_measure/benchmark.kernel.latency.objcore.stats :byl:`SKIPPED` (runtime filter)
         INFO    - 1768/1780 magpie_f777ni             tests/benchmarks/latency_measure/benchmark.kernel.latency.timeslicing.userspace :bgn:`PASSED` (device: DT04BNT1, 7.614s)
         INFO    - 1769/1780 magpie_f777ni             tests/benchmarks/latency_measure/benchmark.kernel.latency :byl:`SKIPPED` (runtime filter)
         INFO    - 1770/1780 magpie_f777ni             tests/benchmarks/latency_measure/benchmark.kernel.latency.userspace.objcore.stats :bgn:`PASSED` (device: DT04BNT1, 8.067s)
         INFO    - 1771/1780 magpie_f777ni             tests/benchmarks/latency_measure/benchmark.kernel.latency.userspace :bgn:`PASSED` (device: DT04BNT1, 8.294s)
         INFO    - 1772/1780 magpie_f777ni             tests/benchmarks/sys_kernel/benchmark.kernel.core  :bgn:`PASSED` (device: DT04BNT1, 5.500s)
         INFO    - 1773/1780 magpie_f777ni             tests/benchmarks/data_structure_perf/dlist_perf/benchmark.data_structure_perf.dlist :bgn:`PASSED` (device: DT04BNT1, 3.997s)
         INFO    - 1774/1780 magpie_f777ni             tests/benchmarks/data_structure_perf/rbtree_perf/benchmark.data_structure_perf.rbtree :bgn:`PASSED` (device: DT04BNT1, 2.627s)
         INFO    - 1775/1780 magpie_f777ni             tests/benchmarks/app_kernel/benchmark.kernel.application.timeslicing :bgn:`PASSED` (device: DT04BNT1, 4.522s)
         INFO    - 1776/1780 magpie_f777ni             tests/benchmarks/app_kernel/benchmark.kernel.application.user.timeslicing :bgn:`PASSED` (device: DT04BNT1, 9.734s)
         INFO    - 1777/1780 magpie_f777ni             tests/benchmarks/app_kernel/benchmark.kernel.application.objcore.stats :bgn:`PASSED` (device: DT04BNT1, 3.866s)
         INFO    - 1778/1780 magpie_f777ni             tests/benchmarks/app_kernel/benchmark.kernel.application.user.objcore.stats :bgn:`PASSED` (device: DT04BNT1, 9.257s)
         INFO    - 1779/1780 magpie_f777ni             tests/benchmarks/app_kernel/benchmark.kernel.application.user :bgn:`PASSED` (device: DT04BNT1, 9.109s)
         INFO    - 1780/1780 magpie_f777ni             tests/benchmarks/app_kernel/benchmark.kernel.application :bgn:`PASSED` (device: DT04BNT1, 3.502s)

         INFO    - 1984 test scenarios (1780 test instances) selected, 1664 configurations skipped (1652 by static filter, 12 at runtime).
         INFO    - :bgn:`116 of 1780` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1664` skipped with :bbk:`0` warnings in :bbk:`1910.00 seconds`
         INFO    - In total 1214 test cases were executed, 12211 skipped on 1 out of total 739 platforms (0.14%)
         INFO    - :bgn:`116` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board         \| ID       \|   Counter \|
         \|---------------\|----------\|-----------\|
         \| magpie_f777ni \| DT04BNT1 \|       116 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni...
         INFO    - Run completed
