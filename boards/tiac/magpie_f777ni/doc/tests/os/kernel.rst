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
         INFO    - 1759/1887 magpie_f777ni             tests/kernel/mem_slab/mslab_stats/kernel.memory_slabs.stats :bgn:`PASSED` (device: DT04BNT1, 2.491s)
         INFO    - 1760/1887 magpie_f777ni             tests/kernel/pending/kernel.objects                :bgn:`PASSED` (device: DT04BNT1, 9.042s)
         INFO    - 1761/1887 magpie_f777ni             tests/kernel/mem_slab/mslab/kernel.memory_slabs    :bgn:`PASSED` (device: DT04BNT1, 2.393s)
         INFO    - 1762/1887 magpie_f777ni             tests/kernel/pending/kernel.objects.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 9.056s)
         INFO    - 1763/1887 magpie_f777ni             tests/kernel/mem_slab/mslab_threadsafe/kernel.memory_slabs.threadsafe :bgn:`PASSED` (device: DT04BNT1, 3.284s)
         INFO    - 1764/1887 magpie_f777ni             tests/kernel/ipi_optimize/kernel.ipi_optimize.smp  :byl:`SKIPPED` (runtime filter)
         INFO    - 1765/1887 magpie_f777ni             tests/kernel/mem_slab/mslab_api/kernel.memory_slabs.api :bgn:`PASSED` (device: DT04BNT1, 9.160s)
         INFO    - 1766/1887 magpie_f777ni             tests/kernel/mem_slab/mslab_concept/kernel.memory_slabs.concept :bgn:`PASSED` (device: DT04BNT1, 5.447s)
         INFO    - 1767/1887 magpie_f777ni             tests/kernel/stack/stack/kernel.stack.usage        :bgn:`PASSED` (device: DT04BNT1, 5.374s)
         INFO    - 1768/1887 magpie_f777ni             tests/kernel/semaphore/semaphore/kernel.semaphore  :bgn:`PASSED` (device: DT04BNT1, 15.454s)
         INFO    - 1769/1887 magpie_f777ni             tests/kernel/common/kernel.common.lto              :bgn:`PASSED` (device: DT04BNT1, 6.101s)
         INFO    - 1770/1887 magpie_f777ni             tests/kernel/semaphore/sys_sem/kernel.semaphore.usage :bgn:`PASSED` (device: DT04BNT1, 3.204s)
         INFO    - 1771/1887 magpie_f777ni             tests/kernel/common/kernel.common.picolibc         :bgn:`PASSED` (device: DT04BNT1, 9.321s)
         INFO    - 1772/1887 magpie_f777ni             tests/kernel/common/kernel.common.misra            :byl:`SKIPPED` (runtime filter)
         INFO    - 1773/1887 magpie_f777ni             tests/kernel/common/kernel.common.nano64           :bgn:`PASSED` (device: DT04BNT1, 8.136s)
         INFO    - 1774/1887 magpie_f777ni             tests/kernel/common/kernel.common.nano32           :bgn:`PASSED` (device: DT04BNT1, 9.164s)
         INFO    - 1775/1887 magpie_f777ni             tests/kernel/common/kernel.common.minimallibc      :bgn:`PASSED` (device: DT04BNT1, 9.018s)
         INFO    - 1776/1887 magpie_f777ni             tests/kernel/obj_core/obj_core/kernel.obj_core     :bgn:`PASSED` (device: DT04BNT1, 3.283s)
         INFO    - 1777/1887 magpie_f777ni             tests/kernel/common/kernel.common.tls              :bgn:`PASSED` (device: DT04BNT1, 8.997s)
         INFO    - 1778/1887 magpie_f777ni             tests/kernel/obj_core/obj_core_stats_api/kernel.obj_core.stats.api :bgn:`PASSED` (device: DT04BNT1, 2.408s)
         INFO    - 1779/1887 magpie_f777ni             tests/kernel/common/kernel.common                  :bgn:`PASSED` (device: DT04BNT1, 9.254s)
         INFO    - 1780/1887 magpie_f777ni             tests/kernel/obj_core/obj_core_stats/kernel.obj_core.stats :bgn:`PASSED` (device: DT04BNT1, 3.499s)
         INFO    - 1781/1887 magpie_f777ni             tests/kernel/mbox/mbox_api/kernel.mailbox.api      :bgn:`PASSED` (device: DT04BNT1, 3.669s)
         INFO    - 1782/1887 magpie_f777ni             tests/kernel/usage/thread_runtime_stats/kernel.usage :bgn:`PASSED` (device: DT04BNT1, 3.681s)
         INFO    - 1783/1887 magpie_f777ni             tests/kernel/mbox/mbox_usage/kernel.mailbox.usage  :bgn:`PASSED` (device: DT04BNT1, 2.472s)
         INFO    - 1784/1887 magpie_f777ni             tests/kernel/tickless/tickless_concept/kernel.tickless.concept :bgn:`PASSED` (device: DT04BNT1, 3.338s)
         INFO    - 1785/1887 magpie_f777ni             tests/kernel/smp_abort/kernel.smp_abort            :byl:`SKIPPED` (runtime filter)
         INFO    - 1786/1887 magpie_f777ni             tests/kernel/workq/critical/kernel.workqueue.critical.sam :byl:`SKIPPED` (runtime filter)
         INFO    - 1787/1887 magpie_f777ni             tests/kernel/xip/arch.common.xip.minimallibc       :bgn:`PASSED` (device: DT04BNT1, 3.138s)
         INFO    - 1788/1887 magpie_f777ni             tests/kernel/xip/arch.common.xip                   :bgn:`PASSED` (device: DT04BNT1, 2.359s)
         INFO    - 1789/1887 magpie_f777ni             tests/kernel/workq/work/kernel.workqueue.api       :bgn:`PASSED` (device: DT04BNT1, 6.500s)
         INFO    - 1790/1887 magpie_f777ni             tests/kernel/workq/work_queue/kernel.workqueue     :bgn:`PASSED` (device: DT04BNT1, 7.067s)
         INFO    - 1791/1887 magpie_f777ni             tests/kernel/workq/critical/kernel.workqueue.critical :bgn:`PASSED` (device: DT04BNT1, 3.504s)
         INFO    - 1792/1887 magpie_f777ni             tests/kernel/profiling/profiling_api/kernel.common.profiling :bgn:`PASSED` (device: DT04BNT1, 2.564s)
         INFO    - 1793/1887 magpie_f777ni             tests/kernel/workq/user_work/kernel.workqueue.user :bgn:`PASSED` (device: DT04BNT1, 3.052s)
         INFO    - 1794/1887 magpie_f777ni             tests/kernel/poll/kernel.poll.minimallibc          :bgn:`PASSED` (device: DT04BNT1, 8.039s)
         INFO    - 1795/1887 magpie_f777ni             tests/kernel/poll/kernel.poll                      :bgn:`PASSED` (device: DT04BNT1, 8.766s)
         INFO    - 1796/1887 magpie_f777ni             tests/kernel/sched/preempt/kernel.scheduler.preempt :bgn:`PASSED` (device: DT04BNT1, 3.086s)
         INFO    - 1797/1887 magpie_f777ni             tests/kernel/sched/metairq/kernel.scheduler.metairq :bgn:`PASSED` (device: DT04BNT1, 2.433s)
         INFO    - 1798/1887 magpie_f777ni             tests/kernel/sched/deadline/kernel.scheduler.deadline.scalable :bgn:`PASSED` (device: DT04BNT1, 4.470s)
         INFO    - 1799/1887 magpie_f777ni             tests/kernel/sched/deadline/kernel.scheduler.deadline :bgn:`PASSED` (device: DT04BNT1, 4.850s)
         INFO    - 1800/1887 magpie_f777ni             tests/kernel/sched/schedule_api/kernel.scheduler.dumb_no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 5.366s)
         INFO    - 1801/1887 magpie_f777ni             tests/kernel/sched/schedule_api/kernel.scheduler.dumb_timeslicing :bgn:`PASSED` (device: DT04BNT1, 21.176s)
         INFO    - 1802/1887 magpie_f777ni             tests/kernel/sched/schedule_api/kernel.scheduler.multiq_no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 6.194s)
         INFO    - 1803/1887 magpie_f777ni             tests/kernel/sched/schedule_api/kernel.scheduler.multiq :bgn:`PASSED` (device: DT04BNT1, 21.187s)
         INFO    - 1804/1887 magpie_f777ni             tests/kernel/sched/schedule_api/kernel.scheduler.slice_perthread :bgn:`PASSED` (device: DT04BNT1, 23.232s)
         INFO    - 1805/1887 magpie_f777ni             tests/kernel/sched/schedule_api/kernel.scheduler.no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 6.461s)
         INFO    - 1806/1887 magpie_f777ni             tests/kernel/sched/schedule_api/kernel.scheduler   :bgn:`PASSED` (device: DT04BNT1, 21.201s)
         INFO    - 1807/1887 magpie_f777ni             tests/kernel/interrupt/arch.shared_interrupt.lto   :bgn:`PASSED` (device: DT04BNT1, 3.406s)
         INFO    - 1808/1887 magpie_f777ni             tests/kernel/interrupt/arch.shared_interrupt       :bgn:`PASSED` (device: DT04BNT1, 3.205s)
         INFO    - 1809/1887 magpie_f777ni             tests/kernel/interrupt/arch.interrupt.minimallibc  :bgn:`PASSED` (device: DT04BNT1, 2.421s)
         INFO    - 1810/1887 magpie_f777ni             tests/kernel/smp/kernel.multiprocessing.smp.affinity :byl:`SKIPPED` (runtime filter)
         INFO    - 1811/1887 magpie_f777ni             tests/kernel/smp/kernel.multiprocessing.smp.minimallibc :byl:`SKIPPED` (runtime filter)
         INFO    - 1812/1887 magpie_f777ni             tests/kernel/smp/kernel.multiprocessing.smp        :byl:`SKIPPED` (runtime filter)
         INFO    - 1813/1887 magpie_f777ni             tests/kernel/interrupt/arch.interrupt              :bgn:`PASSED` (device: DT04BNT1, 3.353s)
         INFO    - 1814/1887 magpie_f777ni             tests/kernel/obj_tracking/kernel.objects.tracking  :bgn:`PASSED` (device: DT04BNT1, 3.368s)
         INFO    - 1815/1887 magpie_f777ni             tests/kernel/obj_tracking/kernel.objects.tracking.minimallibc :bgn:`PASSED` (device: DT04BNT1, 3.196s)
         INFO    - 1816/1887 magpie_f777ni             tests/kernel/queue/kernel.queue.minimallibc        :bgn:`PASSED` (device: DT04BNT1, 4.822s)
         INFO    - 1817/1887 magpie_f777ni             tests/kernel/queue/kernel.queue                    :bgn:`PASSED` (device: DT04BNT1, 4.862s)
         INFO    - 1818/1887 magpie_f777ni             tests/kernel/smp_suspend/kernel.smp_suspend        :byl:`SKIPPED` (runtime filter)
         INFO    - 1819/1887 magpie_f777ni             tests/kernel/sleep/kernel.common.timing            :bgn:`PASSED` (device: DT04BNT1, 5.999s)
         INFO    - 1820/1887 magpie_f777ni             tests/kernel/sleep/kernel.common.timing.minimallibc :bgn:`PASSED` (device: DT04BNT1, 5.999s)
         INFO    - 1821/1887 magpie_f777ni             tests/kernel/timer/timer_behavior/kernel.timer.timer :bgn:`PASSED` (device: DT04BNT1, 34.061s)
         INFO    - 1822/1887 magpie_f777ni             tests/kernel/timer/timer_api/kernel.timer          :bgn:`PASSED` (device: DT04BNT1, 6.593s)
         INFO    - 1823/1887 magpie_f777ni             tests/kernel/timer/timer_error_case/kernel.timer.error_case :bgn:`PASSED` (device: DT04BNT1, 3.561s)
         INFO    - 1824/1887 magpie_f777ni             tests/kernel/timer/timepoints/kernel.timer.timepoints :bgn:`PASSED` (device: DT04BNT1, 4.284s)
         INFO    - 1825/1887 magpie_f777ni             tests/kernel/timer/timer_monotonic/kernel.timer.monotonic :bgn:`PASSED` (device: DT04BNT1, 5.339s)
         INFO    - 1826/1887 magpie_f777ni             tests/kernel/mem_heap/k_heap_api/kernel.k_heap_api :bgn:`PASSED` (device: DT04BNT1, 2.653s)
         INFO    - 1827/1887 magpie_f777ni             tests/kernel/cache/kernel.cache.api.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 3.016s)
         INFO    - 1828/1887 magpie_f777ni             tests/kernel/cache/kernel.cache.api                :bgn:`PASSED` (device: DT04BNT1, 4.197s)
         INFO    - 1829/1887 magpie_f777ni             tests/kernel/fpu_sharing/float_disable/kernel.fpu_sharing.float_disable :bgn:`PASSED` (device: DT04BNT1, 4.086s)
         INFO    - 1830/1887 magpie_f777ni             tests/kernel/fifo/fifo_usage/kernel.fifo.usage     :bgn:`PASSED` (device: DT04BNT1, 2.494s)
         INFO    - 1831/1887 magpie_f777ni             tests/kernel/fifo/fifo_api/kernel.fifo             :bgn:`PASSED` (device: DT04BNT1, 3.787s)
         INFO    - 1832/1887 magpie_f777ni             tests/kernel/fifo/fifo_timeout/kernel.fifo.timeout :bgn:`PASSED` (device: DT04BNT1, 3.273s)
         INFO    - 1833/1887 magpie_f777ni             tests/kernel/early_sleep/kernel.common.sleep       :bgn:`PASSED` (device: DT04BNT1, 4.603s)
         INFO    - 1834/1887 magpie_f777ni             tests/kernel/early_sleep/kernel.common.sleep.minimallibc :bgn:`PASSED` (device: DT04BNT1, 3.786s)
         INFO    - 1835/1887 magpie_f777ni             tests/kernel/threads/tls/kernel.threads.tls        :bgn:`PASSED` (device: DT04BNT1, 4.269s)
         INFO    - 1836/1887 magpie_f777ni             tests/kernel/threads/tls/kernel.threads.tls.userspace :bgn:`PASSED` (device: DT04BNT1, 4.434s)
         INFO    - 1837/1887 magpie_f777ni             tests/kernel/threads/thread_apis/kernel.threads.apis :bgn:`PASSED` (device: DT04BNT1, 10.108s)
         INFO    - 1838/1887 magpie_f777ni             tests/kernel/threads/dynamic_thread/kernel.threads.dynamic :bgn:`PASSED` (device: DT04BNT1, 4.043s)
         INFO    - 1839/1887 magpie_f777ni             tests/kernel/ipi_cascade/kernel.ipi_cascade.smp    :byl:`SKIPPED` (runtime filter)
         INFO    - 1840/1887 magpie_f777ni             tests/kernel/threads/thread_init/kernel.threads.init :bgn:`PASSED` (device: DT04BNT1, 7.997s)
         INFO    - 1841/1887 magpie_f777ni             tests/kernel/fatal/exception/kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`SKIPPED` (runtime filter)
         INFO    - 1842/1887 magpie_f777ni             tests/kernel/fatal/message_capture/kernel.logging.message_capture :bgn:`PASSED` (device: DT04BNT1, 3.376s)
         INFO    - 1843/1887 magpie_f777ni             tests/kernel/fatal/exception/kernel.common.stack_sentinel :bgn:`PASSED` (device: DT04BNT1, 2.717s)
         INFO    - 1844/1887 magpie_f777ni             tests/kernel/threads/thread_error_case/kernel.threads.error.case :bgn:`PASSED` (device: DT04BNT1, 3.420s)
         INFO    - 1845/1887 magpie_f777ni             tests/kernel/fatal/exception/kernel.common.stack_protection_no_userspace :bgn:`PASSED` (device: DT04BNT1, 4.611s)
         INFO    - 1846/1887 magpie_f777ni             tests/kernel/fatal/exception/kernel.common.stack_protection_arm_fpu_sharing :bgn:`PASSED` (device: DT04BNT1, 4.034s)
         INFO    - 1847/1887 magpie_f777ni             tests/kernel/device/kernel.device.pm               :bgn:`PASSED` (device: DT04BNT1, 4.934s)
         INFO    - 1848/1887 magpie_f777ni             tests/kernel/fatal/exception/kernel.common.stack_protection :bgn:`PASSED` (device: DT04BNT1, 4.245s)
         INFO    - 1849/1887 magpie_f777ni             tests/kernel/msgq/msgq_usage/kernel.message_queue.usage :bgn:`PASSED` (device: DT04BNT1, 3.461s)
         INFO    - 1850/1887 magpie_f777ni             tests/kernel/device/kernel.device.minimallibc      :bgn:`PASSED` (device: DT04BNT1, 4.077s)
         INFO    - 1851/1887 magpie_f777ni             tests/kernel/device/kernel.device                  :bgn:`PASSED` (device: DT04BNT1, 3.973s)
         INFO    - 1852/1887 magpie_f777ni             tests/kernel/msgq/msgq_api/kernel.message_queue    :bgn:`PASSED` (device: DT04BNT1, 4.906s)
         INFO    - 1853/1887 magpie_f777ni             tests/kernel/condvar/condvar_api/kernel.condvar    :bgn:`PASSED` (device: DT04BNT1, 5.554s)
         INFO    - 1854/1887 magpie_f777ni             tests/kernel/pipe/pipe_api/kernel.pipe.api         :bgn:`PASSED` (device: DT04BNT1, 5.498s)
         INFO    - 1855/1887 magpie_f777ni             tests/kernel/pipe/pipe/kernel.pipe                 :bgn:`PASSED` (device: DT04BNT1, 6.583s)
         INFO    - 1856/1887 magpie_f777ni             tests/kernel/events/event_api/kernel.events        :bgn:`PASSED` (device: DT04BNT1, 2.784s)
         INFO    - 1857/1887 magpie_f777ni             tests/kernel/events/sys_event/kernel.events.usage  :bgn:`PASSED` (device: DT04BNT1, 4.398s)
         INFO    - 1858/1887 magpie_f777ni             tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot_tls :byl:`SKIPPED` (runtime filter)
         INFO    - 1859/1887 magpie_f777ni             tests/kernel/lifo/lifo_usage/kernel.lifo.usage     :bgn:`PASSED` (device: DT04BNT1, 3.608s)
         INFO    - 1860/1887 magpie_f777ni             tests/kernel/lifo/lifo_api/kernel.lifo             :bgn:`PASSED` (device: DT04BNT1, 2.978s)
         INFO    - 1861/1887 magpie_f777ni             tests/kernel/mem_protect/stack_random/kernel.memory_protection.stack_random :bgn:`PASSED` (device: DT04BNT1, 4.036s)
         INFO    - 1862/1887 magpie_f777ni             tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem.nouser :bgn:`PASSED` (device: DT04BNT1, 3.714s)
         INFO    - 1863/1887 magpie_f777ni             tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64 :byl:`SKIPPED` (runtime filter)
         INFO    - 1864/1887 magpie_f777ni             tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot :bgn:`PASSED` (device: DT04BNT1, 4.005s)
         INFO    - 1865/1887 magpie_f777ni             tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map :byl:`SKIPPED` (runtime filter)
         INFO    - 1866/1887 magpie_f777ni             tests/kernel/mem_protect/futex/kernel.futex        :bgn:`PASSED` (device: DT04BNT1, 4.358s)
         INFO    - 1867/1887 magpie_f777ni             tests/kernel/mutex/sys_mutex/kernel.mutex.system.nouser :bgn:`PASSED` (device: DT04BNT1, 9.955s)
         INFO    - 1868/1887 magpie_f777ni             tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem :bgn:`PASSED` (device: DT04BNT1, 5.001s)
         INFO    - 1869/1887 magpie_f777ni             tests/kernel/mutex/mutex_api/kernel.mutex          :bgn:`PASSED` (device: DT04BNT1, 16.103s)
         INFO    - 1870/1887 magpie_f777ni             tests/kernel/mutex/sys_mutex/kernel.mutex.system   :bgn:`PASSED` (device: DT04BNT1, 11.435s)
         INFO    - 1871/1887 magpie_f777ni             tests/kernel/context/kernel.context.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 8.066s)
         INFO    - 1872/1887 magpie_f777ni             tests/kernel/mutex/mutex_error_case/kernel.mutex.error :bgn:`PASSED` (device: DT04BNT1, 6.207s)
         INFO    - 1873/1887 magpie_f777ni             tests/kernel/context/kernel.context                :bgn:`PASSED` (device: DT04BNT1, 9.945s)
         INFO    - 1874/1887 magpie_f777ni             tests/integration/kernel/integration.kernel        :bgn:`PASSED` (device: DT04BNT1, 5.714s)
         INFO    - 1875/1887 magpie_f777ni             tests/lib/p4workq/libraries.p4wq                   :bgn:`PASSED` (device: DT04BNT1, 3.816s)
         INFO    - 1876/1887 magpie_f777ni             tests/benchmarks/latency_measure/benchmark.kernel.latency :byl:`SKIPPED` (runtime filter)
         INFO    - 1877/1887 magpie_f777ni             tests/benchmarks/latency_measure/benchmark.kernel.latency.stm32 :bgn:`PASSED` (device: DT04BNT1, 5.245s)
         INFO    - 1878/1887 magpie_f777ni             tests/benchmarks/sys_kernel/benchmark.kernel.core  :bgn:`PASSED` (device: DT04BNT1, 4.504s)
         INFO    - 1879/1887 magpie_f777ni             tests/benchmarks/data_structure_perf/dlist_perf/benchmark.data_structure_perf.dlist :bgn:`PASSED` (device: DT04BNT1, 2.525s)
         INFO    - 1880/1887 magpie_f777ni             tests/benchmarks/latency_measure/benchmark.kernel.latency.userspace :bgn:`PASSED` (device: DT04BNT1, 7.688s)
         INFO    - 1881/1887 magpie_f777ni             tests/benchmarks/data_structure_perf/rbtree_perf/benchmark.data_structure_perf.rbtree :bgn:`PASSED` (device: DT04BNT1, 2.638s)
         INFO    - 1882/1887 magpie_f777ni             tests/benchmarks/app_kernel/benchmark.kernel.application.timeslicing :bgn:`PASSED` (device: DT04BNT1, 4.282s)
         INFO    - 1883/1887 magpie_f777ni             tests/benchmarks/app_kernel/benchmark.kernel.application.objcore.stats :bgn:`PASSED` (device: DT04BNT1, 4.100s)
         INFO    - 1884/1887 magpie_f777ni             tests/benchmarks/app_kernel/benchmark.kernel.application.user.timeslicing :bgn:`PASSED` (device: DT04BNT1, 8.456s)
         INFO    - 1885/1887 magpie_f777ni             tests/benchmarks/app_kernel/benchmark.kernel.application.user.objcore.stats :bgn:`PASSED` (device: DT04BNT1, 9.750s)
         INFO    - 1886/1887 magpie_f777ni             tests/benchmarks/app_kernel/benchmark.kernel.application.user :bgn:`PASSED` (device: DT04BNT1, 8.132s)
         INFO    - 1887/1887 magpie_f777ni             tests/benchmarks/app_kernel/benchmark.kernel.application :bgn:`PASSED` (device: DT04BNT1, 3.635s)

         INFO    - 2092 test scenarios (1887 test instances) selected, 1772 configurations skipped (1758 by static filter, 14 at runtime).
         INFO    - :bgn:`115 of 1887` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1772` skipped with :bbk:`0` warnings in :bbk:`1885.32 seconds`
         INFO    - In total 1238 test cases were executed, 13735 skipped on 1 out of total 1 platforms (100.00%)
         INFO    - :bgn:`115` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board         \| ID       \|   Counter \|
         \|---------------\|----------\|-----------\|
         \| magpie_f777ni \| DT04BNT1 \|       115 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni...
         INFO    - Run completed
