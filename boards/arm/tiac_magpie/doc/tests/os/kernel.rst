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

         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1431/1543 tiac_magpie               tests/kernel/mem_slab/mslab_stats/kernel.memory_slabs.stats :bgn:`PASSED` (device: DT04BNT1, 2.418s)
         INFO    - 1432/1543 tiac_magpie               tests/kernel/mem_slab/mslab/kernel.memory_slabs    :bgn:`PASSED` (device: DT04BNT1, 3.075s)
         INFO    - 1433/1543 tiac_magpie               tests/kernel/pending/kernel.objects                :bgn:`PASSED` (device: DT04BNT1, 8.381s)
         INFO    - 1434/1543 tiac_magpie               tests/kernel/pending/kernel.objects.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 8.900s)
         INFO    - 1435/1543 tiac_magpie               tests/kernel/mem_slab/mslab_threadsafe/kernel.memory_slabs.threadsafe :bgn:`PASSED` (device: DT04BNT1, 2.391s)
         INFO    - 1436/1543 tiac_magpie               tests/kernel/mem_slab/mslab_api/kernel.memory_slabs.api :bgn:`PASSED` (device: DT04BNT1, 8.454s)
         INFO    - 1437/1543 tiac_magpie               tests/kernel/mem_slab/mslab_concept/kernel.memory_slabs.concept :bgn:`PASSED` (device: DT04BNT1, 5.110s)
         INFO    - 1438/1543 tiac_magpie               tests/kernel/stack/stack/kernel.stack.usage        :bgn:`PASSED` (device: DT04BNT1, 5.112s)
         INFO    - 1439/1543 tiac_magpie               tests/kernel/semaphore/semaphore/kernel.semaphore  :bgn:`PASSED` (device: DT04BNT1, 16.140s)
         INFO    - 1440/1543 tiac_magpie               tests/kernel/semaphore/sys_sem/kernel.semaphore.usage :bgn:`PASSED` (device: DT04BNT1, 3.242s)
         INFO    - 1441/1543 tiac_magpie               tests/kernel/common/kernel.common.picolibc         :bgn:`PASSED` (device: DT04BNT1, 7.822s)
         INFO    - 1442/1543 tiac_magpie               tests/kernel/common/kernel.common.misra            :byl:`SKIPPED` (runtime filter)
         INFO    - 1443/1543 tiac_magpie               tests/kernel/common/kernel.common.nano64           :bgn:`PASSED` (device: DT04BNT1, 8.526s)
         INFO    - 1444/1543 tiac_magpie               tests/kernel/common/kernel.common.nano32           :bgn:`PASSED` (device: DT04BNT1, 9.613s)
         INFO    - 1445/1543 tiac_magpie               tests/kernel/common/kernel.common.minimallibc      :bgn:`PASSED` (device: DT04BNT1, 7.819s)
         INFO    - 1446/1543 tiac_magpie               tests/kernel/common/kernel.common.tls              :bgn:`PASSED` (device: DT04BNT1, 8.064s)
         INFO    - 1447/1543 tiac_magpie               tests/kernel/common/kernel.common                  :bgn:`PASSED` (device: DT04BNT1, 7.771s)
         INFO    - 1448/1543 tiac_magpie               tests/kernel/usage/thread_runtime_stats/kernel.usage :bgn:`PASSED` (device: DT04BNT1, 2.341s)
         INFO    - 1449/1543 tiac_magpie               tests/kernel/mbox/mbox_usage/kernel.mailbox.usage  :bgn:`PASSED` (device: DT04BNT1, 2.348s)
         INFO    - 1450/1543 tiac_magpie               tests/kernel/mbox/mbox_api/kernel.mailbox.api      :bgn:`PASSED` (device: DT04BNT1, 3.505s)
         INFO    - 1451/1543 tiac_magpie               tests/kernel/tickless/tickless_concept/kernel.tickless.concept :bgn:`PASSED` (device: DT04BNT1, 3.355s)
         INFO    - 1452/1543 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.critical.sam :byl:`SKIPPED` (runtime filter)
         INFO    - 1453/1543 tiac_magpie               tests/kernel/xip/arch.common.xip.minimallibc       :bgn:`PASSED` (device: DT04BNT1, 2.587s)
         INFO    - 1454/1543 tiac_magpie               tests/kernel/xip/arch.common.xip                   :bgn:`PASSED` (device: DT04BNT1, 2.973s)
         INFO    - 1455/1543 tiac_magpie               tests/kernel/workq/work/kernel.workqueue.api       :bgn:`PASSED` (device: DT04BNT1, 4.594s)
         INFO    - 1456/1543 tiac_magpie               tests/kernel/workq/critical/kernel.workqueue.critical :bgn:`PASSED` (device: DT04BNT1, 2.501s)
         INFO    - 1457/1543 tiac_magpie               tests/kernel/workq/work_queue/kernel.workqueue     :bgn:`PASSED` (device: DT04BNT1, 7.511s)
         INFO    - 1458/1543 tiac_magpie               tests/kernel/profiling/profiling_api/kernel.common.profiling :bgn:`PASSED` (device: DT04BNT1, 2.529s)
         INFO    - 1459/1543 tiac_magpie               tests/kernel/workq/user_work/kernel.workqueue.user :bgn:`PASSED` (device: DT04BNT1, 3.059s)
         INFO    - 1460/1543 tiac_magpie               tests/kernel/poll/kernel.poll                      :bgn:`PASSED` (device: DT04BNT1, 7.219s)
         INFO    - 1461/1543 tiac_magpie               tests/kernel/sched/preempt/kernel.scheduler.preempt :bgn:`PASSED` (device: DT04BNT1, 2.990s)
         INFO    - 1462/1543 tiac_magpie               tests/kernel/poll/kernel.poll.minimallibc          :bgn:`PASSED` (device: DT04BNT1, 7.226s)
         INFO    - 1463/1543 tiac_magpie               tests/kernel/sched/metairq/kernel.scheduler.metairq :bgn:`PASSED` (device: DT04BNT1, 3.009s)
         INFO    - 1464/1543 tiac_magpie               tests/kernel/sched/deadline/kernel.scheduler.deadline :bgn:`PASSED` (device: DT04BNT1, 2.935s)
         INFO    - 1465/1543 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.dumb_no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 5.454s)
         INFO    - 1466/1543 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.dumb_timeslicing :bgn:`PASSED` (device: DT04BNT1, 21.173s)
         INFO    - 1467/1543 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq :bgn:`PASSED` (device: DT04BNT1, 21.176s)
         INFO    - 1468/1543 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.slice_perthread :bgn:`PASSED` (device: DT04BNT1, 21.144s)
         INFO    - 1469/1543 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.multiq_no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 5.339s)
         INFO    - 1470/1543 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler.no_timeslicing :bgn:`PASSED` (device: DT04BNT1, 5.348s)
         INFO    - 1471/1543 tiac_magpie               tests/kernel/sched/schedule_api/kernel.scheduler   :bgn:`PASSED` (device: DT04BNT1, 21.840s)
         INFO    - 1472/1543 tiac_magpie               tests/kernel/interrupt/arch.interrupt              :bgn:`PASSED` (device: DT04BNT1, 2.434s)
         INFO    - 1473/1543 tiac_magpie               tests/kernel/smp/kernel.multiprocessing.smp.minimallibc :byl:`SKIPPED` (runtime filter)
         INFO    - 1474/1543 tiac_magpie               tests/kernel/interrupt/arch.shared_interrupt       :bgn:`PASSED` (device: DT04BNT1, 2.538s)
         INFO    - 1475/1543 tiac_magpie               tests/kernel/smp/kernel.multiprocessing.smp        :byl:`SKIPPED` (runtime filter)
         INFO    - 1476/1543 tiac_magpie               tests/kernel/interrupt/arch.interrupt.minimallibc  :bgn:`PASSED` (device: DT04BNT1, 2.521s)
         INFO    - 1477/1543 tiac_magpie               tests/kernel/obj_tracking/kernel.objects.tracking  :bgn:`PASSED` (device: DT04BNT1, 3.016s)
         INFO    - 1478/1543 tiac_magpie               tests/kernel/obj_tracking/kernel.objects.tracking.minimallibc :bgn:`PASSED` (device: DT04BNT1, 2.639s)
         INFO    - 1479/1543 tiac_magpie               tests/kernel/queue/kernel.queue                    :bgn:`PASSED` (device: DT04BNT1, 4.803s)
         INFO    - 1480/1543 tiac_magpie               tests/kernel/queue/kernel.queue.minimallibc        :bgn:`PASSED` (device: DT04BNT1, 4.790s)
         INFO    - 1481/1543 tiac_magpie               tests/kernel/sleep/kernel.common.timing            :bgn:`PASSED` (device: DT04BNT1, 6.559s)
         INFO    - 1482/1543 tiac_magpie               tests/kernel/sleep/kernel.common.timing.minimallibc :bgn:`PASSED` (device: DT04BNT1, 6.804s)
         INFO    - 1483/1543 tiac_magpie               tests/kernel/timer/timer_behavior/kernel.timer.timer :bgn:`PASSED` (device: DT04BNT1, 32.908s)
         INFO    - 1484/1543 tiac_magpie               tests/kernel/timer/timer_error_case/kernel.timer.error_case :bgn:`PASSED` (device: DT04BNT1, 3.476s)
         INFO    - 1485/1543 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer.tickless :bgn:`PASSED` (device: DT04BNT1, 6.548s)
         INFO    - 1486/1543 tiac_magpie               tests/kernel/cache/kernel.cache.api.minimallibc    :byl:`SKIPPED` (runtime filter)
         INFO    - 1487/1543 tiac_magpie               tests/kernel/timer/timer_api/kernel.timer          :bgn:`PASSED` (device: DT04BNT1, 6.959s)
         INFO    - 1488/1543 tiac_magpie               tests/kernel/cache/kernel.cache.api                :byl:`SKIPPED` (runtime filter)
         INFO    - 1489/1543 tiac_magpie               tests/kernel/timer/timepoints/kernel.timer.timepoints :bgn:`PASSED` (device: DT04BNT1, 3.419s)
         INFO    - 1490/1543 tiac_magpie               tests/kernel/timer/timer_monotonic/kernel.timer.monotonic :bgn:`PASSED` (device: DT04BNT1, 3.723s)
         INFO    - 1491/1543 tiac_magpie               tests/kernel/mem_heap/mheap_api_concept/kernel.memory_heap :bgn:`PASSED` (device: DT04BNT1, 3.221s)
         INFO    - 1492/1543 tiac_magpie               tests/kernel/mem_heap/k_heap_api/kernel.k_heap_api :bgn:`PASSED` (device: DT04BNT1, 3.338s)
         INFO    - 1493/1543 tiac_magpie               tests/kernel/fifo/fifo_usage/kernel.fifo.usage     :bgn:`PASSED` (device: DT04BNT1, 2.421s)
         INFO    - 1494/1543 tiac_magpie               tests/kernel/fifo/fifo_api/kernel.fifo             :bgn:`PASSED` (device: DT04BNT1, 3.644s)
         INFO    - 1495/1543 tiac_magpie               tests/kernel/fpu_sharing/float_disable/kernel.fpu_sharing.float_disable :bgn:`PASSED` (device: DT04BNT1, 3.051s)
         INFO    - 1496/1543 tiac_magpie               tests/kernel/fifo/fifo_timeout/kernel.fifo.timeout :bgn:`PASSED` (device: DT04BNT1, 3.427s)
         INFO    - 1497/1543 tiac_magpie               tests/kernel/early_sleep/kernel.common.sleep.minimallibc :bgn:`PASSED` (device: DT04BNT1, 4.697s)
         INFO    - 1498/1543 tiac_magpie               tests/kernel/early_sleep/kernel.common.sleep       :bgn:`PASSED` (device: DT04BNT1, 3.862s)
         INFO    - 1499/1543 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls        :bgn:`PASSED` (device: DT04BNT1, 3.426s)
         INFO    - 1500/1543 tiac_magpie               tests/kernel/threads/tls/kernel.threads.tls.userspace :bgn:`PASSED` (device: DT04BNT1, 3.994s)
         INFO    - 1501/1543 tiac_magpie               tests/kernel/threads/thread_apis/kernel.threads.apis :bgn:`PASSED` (device: DT04BNT1, 9.494s)
         INFO    - 1502/1543 tiac_magpie               tests/kernel/threads/dynamic_thread/kernel.threads.dynamic :bgn:`PASSED` (device: DT04BNT1, 4.925s)
         INFO    - 1503/1543 tiac_magpie               tests/kernel/threads/thread_init/kernel.threads.init :bgn:`PASSED` (device: DT04BNT1, 7.067s)
         INFO    - 1504/1543 tiac_magpie               tests/kernel/fatal/message_capture/kernel.logging.message_capture :bgn:`PASSED` (device: DT04BNT1, 2.893s)
         INFO    - 1505/1543 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`SKIPPED` (runtime filter)
         INFO    - 1506/1543 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_sentinel :bgn:`PASSED` (device: DT04BNT1, 2.663s)
         INFO    - 1507/1543 tiac_magpie               tests/kernel/threads/thread_error_case/kernel.threads.error.case :bgn:`PASSED` (device: DT04BNT1, 3.492s)
         INFO    - 1508/1543 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_no_userspace :bgn:`PASSED` (device: DT04BNT1, 2.645s)
         INFO    - 1509/1543 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection_arm_fpu_sharing :bgn:`PASSED` (device: DT04BNT1, 4.218s)
         INFO    - 1510/1543 tiac_magpie               tests/kernel/device/kernel.device.pm               :bgn:`PASSED` (device: DT04BNT1, 4.461s)
         INFO    - 1511/1543 tiac_magpie               tests/kernel/fatal/exception/kernel.common.stack_protection :bgn:`PASSED` (device: DT04BNT1, 3.468s)
         INFO    - 1512/1543 tiac_magpie               tests/kernel/msgq/msgq_usage/kernel.message_queue.usage :bgn:`PASSED` (device: DT04BNT1, 3.452s)
         INFO    - 1513/1543 tiac_magpie               tests/kernel/device/kernel.device.minimallibc      :bgn:`PASSED` (device: DT04BNT1, 3.281s)
         INFO    - 1514/1543 tiac_magpie               tests/kernel/device/kernel.device                  :bgn:`PASSED` (device: DT04BNT1, 3.912s)
         INFO    - 1515/1543 tiac_magpie               tests/kernel/msgq/msgq_api/kernel.message_queue    :bgn:`PASSED` (device: DT04BNT1, 4.669s)
         INFO    - 1516/1543 tiac_magpie               tests/kernel/condvar/condvar_api/kernel.condvar    :bgn:`PASSED` (device: DT04BNT1, 5.407s)
         INFO    - 1517/1543 tiac_magpie               tests/kernel/pipe/pipe_api/kernel.pipe.api         :bgn:`PASSED` (device: DT04BNT1, 5.511s)
         INFO    - 1518/1543 tiac_magpie               tests/kernel/pipe/pipe/kernel.pipe                 :bgn:`PASSED` (device: DT04BNT1, 6.406s)
         INFO    - 1519/1543 tiac_magpie               tests/kernel/events/sys_event/kernel.events.usage  :bgn:`PASSED` (device: DT04BNT1, 4.018s)
         INFO    - 1520/1543 tiac_magpie               tests/kernel/lifo/lifo_usage/kernel.lifo.usage     :bgn:`PASSED` (device: DT04BNT1, 2.944s)
         INFO    - 1521/1543 tiac_magpie               tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot_tls :byl:`SKIPPED` (runtime filter)
         INFO    - 1522/1543 tiac_magpie               tests/kernel/events/event_api/kernel.events        :bgn:`PASSED` (device: DT04BNT1, 3.564s)
         INFO    - 1523/1543 tiac_magpie               tests/kernel/lifo/lifo_api/kernel.lifo             :bgn:`PASSED` (device: DT04BNT1, 2.918s)
         INFO    - 1524/1543 tiac_magpie               tests/kernel/mem_protect/stack_random/kernel.memory_protection.stack_random :bgn:`PASSED` (device: DT04BNT1, 2.930s)
         INFO    - 1525/1543 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem.nouser :bgn:`PASSED` (device: DT04BNT1, 3.880s)
         INFO    - 1526/1543 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map.x86_64 :byl:`SKIPPED` (runtime filter)
         INFO    - 1527/1543 tiac_magpie               tests/kernel/mem_protect/stackprot/kernel.memory_protection.stackprot :bgn:`PASSED` (device: DT04BNT1, 3.903s)
         INFO    - 1528/1543 tiac_magpie               tests/kernel/mem_protect/mem_map/kernel.memory_protection.mem_map :byl:`SKIPPED` (runtime filter)
         INFO    - 1529/1543 tiac_magpie               tests/kernel/mem_protect/futex/kernel.futex        :bgn:`PASSED` (device: DT04BNT1, 3.525s)
         INFO    - 1530/1543 tiac_magpie               tests/kernel/mutex/sys_mutex/kernel.mutex.system.nouser :bgn:`PASSED` (device: DT04BNT1, 9.947s)
         INFO    - 1531/1543 tiac_magpie               tests/kernel/mem_protect/sys_sem/kernel.memory_protection.sys_sem :bgn:`PASSED` (device: DT04BNT1, 4.078s)
         INFO    - 1532/1543 tiac_magpie               tests/kernel/mutex/sys_mutex/kernel.mutex.system   :bgn:`PASSED` (device: DT04BNT1, 10.678s)
         INFO    - 1533/1543 tiac_magpie               tests/kernel/context/kernel.context.minimallibc    :bgn:`PASSED` (device: DT04BNT1, 7.949s)
         INFO    - 1534/1543 tiac_magpie               tests/kernel/mutex/mutex_error_case/kernel.mutex.error :bgn:`PASSED` (device: DT04BNT1, 3.320s)
         INFO    - 1535/1543 tiac_magpie               tests/kernel/mutex/mutex_api/kernel.mutex          :bgn:`PASSED` (device: DT04BNT1, 15.215s)
         INFO    - 1536/1543 tiac_magpie               tests/lib/p4workq/libraries.p4wq                   :bgn:`PASSED` (device: DT04BNT1, 2.600s)
         INFO    - 1537/1543 tiac_magpie               tests/benchmarks/latency_measure/benchmark.kernel.latency :byl:`SKIPPED` (runtime filter)
         INFO    - 1538/1543 tiac_magpie               tests/benchmarks/latency_measure/benchmark.kernel.latency.stm32 :bgn:`PASSED` (device: DT04BNT1, 3.055s)
         INFO    - 1539/1543 tiac_magpie               tests/kernel/context/kernel.context                :bgn:`PASSED` (device: DT04BNT1, 7.937s)
         INFO    - 1540/1543 tiac_magpie               tests/benchmarks/sys_kernel/benchmark.kernel.core  :bgn:`PASSED` (device: DT04BNT1, 4.759s)
         INFO    - 1541/1543 tiac_magpie               tests/benchmarks/data_structure_perf/rbtree_perf/benchmark.data_structure_perf.rbtree :bgn:`PASSED` (device: DT04BNT1, 2.344s)
         INFO    - 1542/1543 tiac_magpie               tests/benchmarks/data_structure_perf/dlist_perf/benchmark.data_structure_perf.dlist :bgn:`PASSED` (device: DT04BNT1, 2.903s)
         INFO    - 1543/1543 tiac_magpie               tests/benchmarks/app_kernel/benchmark.kernel.application :bgn:`PASSED` (device: DT04BNT1, 9.464s)

         INFO    - 1755 test scenarios (1543 test instances) selected, 1441 configurations skipped (1430 by static filter, 11 at runtime).
         INFO    - :bgn:`102 of 1543` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1441` skipped with :bbk:`0` warnings in :bbk:`895.49 seconds`
         INFO    - In total 1075 test cases were executed, 9721 skipped on 1 out of total 634 platforms (0.16%)
         INFO    - :bgn:`102` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|       102 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
