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

         $ west twister \
                --verbose --jobs 4 --inline-logs \
                --enable-size-report --platform-reports \
                --device-testing --hardware-map map.yaml \
                --alt-config-root bridle/zephyr/alt-config/tests \
                --testsuite-root zephyr/tests --tag kernel \
                --exclude-tag security --exclude-tag benchmark

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight-console notranslate

         Device testing on:

         \| Platform                  \| ID       \| Serial device   \|
         \|---------------------------\|----------\|-----------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    -   1/121 magpie_f777ni/stm32f777xx kernel.pending                                     :bgn:`PASSED` (device: DT04BNT1, 8.462s <zephyr>)
         INFO    -   2/121 magpie_f777ni/stm32f777xx kernel.memory_slabs                                :bgn:`PASSED` (device: DT04BNT1, 3.352s <zephyr>)
         INFO    -   3/121 magpie_f777ni/stm32f777xx kernel.memory_slabs.stats                          :bgn:`PASSED` (device: DT04BNT1, 3.221s <zephyr>)
         INFO    -   4/121 magpie_f777ni/stm32f777xx kernel.pending.minimallibc                         :bgn:`PASSED` (device: DT04BNT1, 8.504s <zephyr>)
         INFO    -   5/121 magpie_f777ni/stm32f777xx kernel.memory_slabs.threadsafe                     :bgn:`PASSED` (device: DT04BNT1, 2.832s <zephyr>)
         INFO    -   6/121 magpie_f777ni/stm32f777xx kernel.memory_slabs.api                            :bgn:`PASSED` (device: DT04BNT1, 8.606s <zephyr>)
         INFO    -   7/121 magpie_f777ni/stm32f777xx kernel.memory_slabs.concept                        :bgn:`PASSED` (device: DT04BNT1, 5.309s <zephyr>)
         INFO    -   8/121 magpie_f777ni/stm32f777xx kernel.ipi_optimize.smp                            :byl:`FILTERED` (runtime filter)
         INFO    -   9/121 magpie_f777ni/stm32f777xx kernel.stack.usage                                 :bgn:`PASSED` (device: DT04BNT1, 5.205s <zephyr>)
         INFO    -  10/121 magpie_f777ni/stm32f777xx kernel.semaphore                                   :bgn:`PASSED` (device: DT04BNT1, 16.856s <zephyr>)
         INFO    -  11/121 magpie_f777ni/stm32f777xx kernel.semaphore.usage                             :bgn:`PASSED` (device: DT04BNT1, 4.161s <zephyr>)
         INFO    -  12/121 magpie_f777ni/stm32f777xx kernel.common.lto                                  :bgn:`PASSED` (device: DT04BNT1, 6.477s <zephyr>)
         INFO    -  13/121 magpie_f777ni/stm32f777xx kernel.common.picolibc                             :bgn:`PASSED` (device: DT04BNT1, 8.440s <zephyr>)
         INFO    -  14/121 magpie_f777ni/stm32f777xx kernel.common.misra                                :byl:`FILTERED` (runtime filter)
         INFO    -  15/121 magpie_f777ni/stm32f777xx kernel.common.nano64                               :bgn:`PASSED` (device: DT04BNT1, 8.440s <zephyr>)
         INFO    -  16/121 magpie_f777ni/stm32f777xx kernel.common.minimallibc                          :bgn:`PASSED` (device: DT04BNT1, 8.444s <zephyr>)
         INFO    -  17/121 magpie_f777ni/stm32f777xx kernel.common.nano32                               :bgn:`PASSED` (device: DT04BNT1, 9.150s <zephyr>)
         INFO    -  18/121 magpie_f777ni/stm32f777xx kernel.ipi_work                                    :byl:`FILTERED` (runtime filter)
         INFO    -  19/121 magpie_f777ni/stm32f777xx kernel.common.tls                                  :bgn:`PASSED` (device: DT04BNT1, 9.299s <zephyr>)
         INFO    -  20/121 magpie_f777ni/stm32f777xx kernel.obj_core                                    :bgn:`PASSED` (device: DT04BNT1, 3.459s <zephyr>)
         INFO    -  21/121 magpie_f777ni/stm32f777xx kernel.common                                      :bgn:`PASSED` (device: DT04BNT1, 8.352s <zephyr>)
         INFO    -  22/121 magpie_f777ni/stm32f777xx kernel.obj_core.stats.api                          :bgn:`PASSED` (device: DT04BNT1, 3.511s <zephyr>)
         INFO    -  23/121 magpie_f777ni/stm32f777xx kernel.obj_core.stats                              :bgn:`PASSED` (device: DT04BNT1, 2.874s <zephyr>)
         INFO    -  24/121 magpie_f777ni/stm32f777xx kernel.usage                                       :bgn:`PASSED` (device: DT04BNT1, 3.366s <zephyr>)
         INFO    -  25/121 magpie_f777ni/stm32f777xx kernel.mailbox.api                                 :bgn:`PASSED` (device: DT04BNT1, 3.055s <zephyr>)
         INFO    -  26/121 magpie_f777ni/stm32f777xx kernel.mailbox.usage                               :bgn:`PASSED` (device: DT04BNT1, 3.446s <zephyr>)
         INFO    -  27/121 magpie_f777ni/stm32f777xx kernel.smp_abort                                   :byl:`FILTERED` (runtime filter)
         INFO    -  28/121 magpie_f777ni/stm32f777xx kernel.tickless.concept                            :bgn:`PASSED` (device: DT04BNT1, 3.426s <zephyr>)
         INFO    -  29/121 magpie_f777ni/stm32f777xx kernel.workqueue.critical                          :bgn:`PASSED` (device: DT04BNT1, 3.499s <zephyr>)
         INFO    -  30/121 magpie_f777ni/stm32f777xx kernel.workqueue.api                               :bgn:`PASSED` (device: DT04BNT1, 6.242s <zephyr>)
         INFO    -  31/121 magpie_f777ni/stm32f777xx kernel.workqueue.work_timeout                      :bgn:`PASSED` (device: DT04BNT1, 12.258s <zephyr>)
         INFO    -  32/121 magpie_f777ni/stm32f777xx kernel.workqueue                                   :bgn:`PASSED` (device: DT04BNT1, 11.163s <zephyr>)
         INFO    -  33/121 magpie_f777ni/stm32f777xx kernel.workqueue.user                              :bgn:`PASSED` (device: DT04BNT1, 4.359s <zephyr>)
         INFO    -  34/121 magpie_f777ni/stm32f777xx kernel.common.profiling                            :bgn:`PASSED` (device: DT04BNT1, 2.580s <zephyr>)
         INFO    -  35/121 magpie_f777ni/stm32f777xx kernel.poll.minimallibc                            :bgn:`PASSED` (device: DT04BNT1, 7.339s <zephyr>)
         INFO    -  36/121 magpie_f777ni/stm32f777xx kernel.poll                                        :bgn:`PASSED` (device: DT04BNT1, 7.396s <zephyr>)
         INFO    -  37/121 magpie_f777ni/stm32f777xx kernel.scheduler.preempt                           :bgn:`PASSED` (device: DT04BNT1, 2.998s <zephyr>)
         INFO    -  38/121 magpie_f777ni/stm32f777xx kernel.scheduler.metairq                           :bgn:`PASSED` (device: DT04BNT1, 3.625s <zephyr>)
         INFO    -  39/121 magpie_f777ni/stm32f777xx kernel.scheduler.wraparound                        :bgn:`PASSED` (device: DT04BNT1, 3.670s <zephyr>)
         INFO    -  40/121 magpie_f777ni/stm32f777xx kernel.scheduler.deadline.scalable                 :bgn:`PASSED` (device: DT04BNT1, 3.998s <zephyr>)
         INFO    -  41/121 magpie_f777ni/stm32f777xx kernel.scheduler.deadline                          :bgn:`PASSED` (device: DT04BNT1, 3.916s <zephyr>)
         INFO    -  42/121 magpie_f777ni/stm32f777xx kernel.scheduler.simple_no_timeslicing             :bgn:`PASSED` (device: DT04BNT1, 6.251s <zephyr>)
         INFO    -  43/121 magpie_f777ni/stm32f777xx kernel.scheduler.simple_timeslicing                :bgn:`PASSED` (device: DT04BNT1, 21.238s <zephyr>)
         INFO    -  44/121 magpie_f777ni/stm32f777xx kernel.scheduler.multiq_no_timeslicing             :bgn:`PASSED` (device: DT04BNT1, 6.490s <zephyr>)
         INFO    -  45/121 magpie_f777ni/stm32f777xx kernel.scheduler.multiq                            :bgn:`PASSED` (device: DT04BNT1, 22.442s <zephyr>)
         INFO    -  46/121 magpie_f777ni/stm32f777xx kernel.scheduler.slice_perthread                   :bgn:`PASSED` (device: DT04BNT1, 21.957s <zephyr>)
         INFO    -  47/121 magpie_f777ni/stm32f777xx kernel.multiprocessing.smp.affinity.custom_rom_offset :byl:`FILTERED` (runtime filter)
         INFO    -  48/121 magpie_f777ni/stm32f777xx kernel.multiprocessing.smp.affinity                :byl:`FILTERED` (runtime filter)
         INFO    -  49/121 magpie_f777ni/stm32f777xx kernel.multiprocessing.smp.minimallibc             :byl:`FILTERED` (runtime filter)
         INFO    -  50/121 magpie_f777ni/stm32f777xx kernel.scheduler.no_timeslicing                    :bgn:`PASSED` (device: DT04BNT1, 5.675s <zephyr>)
         INFO    -  51/121 magpie_f777ni/stm32f777xx kernel.multiprocessing.smp                         :byl:`FILTERED` (runtime filter)
         INFO    -  52/121 magpie_f777ni/stm32f777xx kernel.scheduler                                   :bgn:`PASSED` (device: DT04BNT1, 21.355s <zephyr>)
         INFO    -  53/121 magpie_f777ni/stm32f777xx kernel.objects.tracking                            :bgn:`PASSED` (device: DT04BNT1, 3.460s <zephyr>)
         INFO    -  54/121 magpie_f777ni/stm32f777xx kernel.objects.tracking.minimallibc                :bgn:`PASSED` (device: DT04BNT1, 3.689s <zephyr>)
         INFO    -  55/121 magpie_f777ni/stm32f777xx kernel.queue.minimallibc                           :bgn:`PASSED` (device: DT04BNT1, 7.162s <zephyr>)
         INFO    -  56/121 magpie_f777ni/stm32f777xx kernel.queue                                       :bgn:`PASSED` (device: DT04BNT1, 5.664s <zephyr>)
         INFO    -  57/121 magpie_f777ni/stm32f777xx kernel.smp_suspend                                 :byl:`FILTERED` (runtime filter)
         INFO    -  58/121 magpie_f777ni/stm32f777xx kernel.common.timing                               :bgn:`PASSED` (device: DT04BNT1, 6.137s <zephyr>)
         INFO    -  59/121 magpie_f777ni/stm32f777xx kernel.common.timing.minimallibc                   :bgn:`PASSED` (device: DT04BNT1, 7.156s <zephyr>)
         INFO    -  60/121 magpie_f777ni/stm32f777xx kernel.timer.timer                                 :bgn:`PASSED` (device: DT04BNT1, 34.367s <zephyr>)
         INFO    -  61/121 magpie_f777ni/stm32f777xx kernel.timer                                       :bgn:`PASSED` (device: DT04BNT1, 7.443s <zephyr>)
         INFO    -  62/121 magpie_f777ni/stm32f777xx kernel.timer.timepoints                            :bgn:`PASSED` (device: DT04BNT1, 3.480s <zephyr>)
         INFO    -  63/121 magpie_f777ni/stm32f777xx kernel.timer.error_case                            :bgn:`PASSED` (device: DT04BNT1, 3.624s <zephyr>)
         INFO    -  64/121 magpie_f777ni/stm32f777xx kernel.timer.monotonic                             :bgn:`PASSED` (device: DT04BNT1, 5.494s <zephyr>)
         INFO    -  65/121 magpie_f777ni/stm32f777xx kernel.k_heap_api                                  :bgn:`PASSED` (device: DT04BNT1, 3.153s <zephyr>)
         INFO    -  66/121 magpie_f777ni/stm32f777xx kernel.cache.api.minimallibc                       :bgn:`PASSED` (device: DT04BNT1, 3.336s <zephyr>)
         INFO    -  67/121 magpie_f777ni/stm32f777xx kernel.cache.api                                   :bgn:`PASSED` (device: DT04BNT1, 3.264s <zephyr>)
         INFO    -  68/121 magpie_f777ni/stm32f777xx kernel.fpu_sharing.float_disable                   :bgn:`PASSED` (device: DT04BNT1, 3.150s <zephyr>)
         INFO    -  69/121 magpie_f777ni/stm32f777xx kernel.fifo.usage                                  :bgn:`PASSED` (device: DT04BNT1, 4.597s <zephyr>)
         INFO    -  70/121 magpie_f777ni/stm32f777xx kernel.fifo                                        :bgn:`PASSED` (device: DT04BNT1, 3.820s <zephyr>)
         INFO    -  71/121 magpie_f777ni/stm32f777xx kernel.fifo.timeout                                :bgn:`PASSED` (device: DT04BNT1, 2.681s <zephyr>)
         INFO    -  72/121 magpie_f777ni/stm32f777xx kernel.common.sleep.minimallibc                    :bgn:`PASSED` (device: DT04BNT1, 4.188s <zephyr>)
         INFO    -  73/121 magpie_f777ni/stm32f777xx kernel.common.sleep                                :bgn:`PASSED` (device: DT04BNT1, 4.004s <zephyr>)
         INFO    -  74/121 magpie_f777ni/stm32f777xx kernel.threads.tls                                 :bgn:`PASSED` (device: DT04BNT1, 4.628s <zephyr>)
         INFO    -  75/121 magpie_f777ni/stm32f777xx kernel.threads.tls.userspace                       :bgn:`PASSED` (device: DT04BNT1, 4.291s <zephyr>)
         INFO    -  76/121 magpie_f777ni/stm32f777xx kernel.threads.apis                                :bgn:`PASSED` (device: DT04BNT1, 10.771s <zephyr>)
         INFO    -  77/121 magpie_f777ni/stm32f777xx kernel.threads.dynamic                             :bgn:`PASSED` (device: DT04BNT1, 4.101s <zephyr>)
         INFO    -  78/121 magpie_f777ni/stm32f777xx kernel.ipi_cascade.smp                             :byl:`FILTERED` (runtime filter)
         INFO    -  79/121 magpie_f777ni/stm32f777xx kernel.threads.init                                :bgn:`PASSED` (device: DT04BNT1, 7.819s <zephyr>)
         INFO    -  80/121 magpie_f777ni/stm32f777xx kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`FILTERED` (runtime filter)
         INFO    -  81/121 magpie_f777ni/stm32f777xx kernel.common.stack_sentinel                       :bgn:`PASSED` (device: DT04BNT1, 2.652s <zephyr>)
         INFO    -  82/121 magpie_f777ni/stm32f777xx kernel.logging.message_capture                     :bgn:`PASSED` (device: DT04BNT1, 2.394s <zephyr>)
         INFO    -  83/121 magpie_f777ni/stm32f777xx kernel.threads.error.case                          :bgn:`PASSED` (device: DT04BNT1, 3.665s <zephyr>)
         INFO    -  84/121 magpie_f777ni/stm32f777xx kernel.common.stack_protection_no_userspace        :bgn:`PASSED` (device: DT04BNT1, 3.604s <zephyr>)
         INFO    -  85/121 magpie_f777ni/stm32f777xx kernel.common.stack_protection_arm_fpu_sharing     :bgn:`PASSED` (device: DT04BNT1, 4.076s <zephyr>)
         INFO    -  86/121 magpie_f777ni/stm32f777xx kernel.device.pm                                   :bgn:`PASSED` (device: DT04BNT1, 4.251s <zephyr>)
         INFO    -  87/121 magpie_f777ni/stm32f777xx kernel.common.stack_protection                     :bgn:`PASSED` (device: DT04BNT1, 3.591s <zephyr>)
         INFO    -  88/121 magpie_f777ni/stm32f777xx kernel.device                                      :bgn:`PASSED` (device: DT04BNT1, 4.013s <zephyr>)
         INFO    -  89/121 magpie_f777ni/stm32f777xx kernel.device.minimallibc                          :bgn:`PASSED` (device: DT04BNT1, 4.180s <zephyr>)
         INFO    -  90/121 magpie_f777ni/stm32f777xx kernel.message_queue.put_front                     :bgn:`PASSED` (device: DT04BNT1, 4.224s <zephyr>)
         INFO    -  91/121 magpie_f777ni/stm32f777xx kernel.message_queue                               :bgn:`PASSED` (device: DT04BNT1, 4.339s <zephyr>)
         INFO    -  92/121 magpie_f777ni/stm32f777xx kernel.message_queue.usage                         :bgn:`PASSED` (device: DT04BNT1, 4.726s <zephyr>)
         INFO    -  93/121 magpie_f777ni/stm32f777xx kernel.pipe.api                                    :bgn:`PASSED` (device: DT04BNT1, 6.678s <zephyr>)
         INFO    -  94/121 magpie_f777ni/stm32f777xx kernel.condvar                                     :bgn:`PASSED` (device: DT04BNT1, 6.893s <zephyr>)
         INFO    -  95/121 magpie_f777ni/stm32f777xx kernel.events                                      :bgn:`PASSED` (device: DT04BNT1, 2.932s <zephyr>)
         INFO    -  96/121 magpie_f777ni/stm32f777xx kernel.memory_protection.stackprot_tls             :byl:`FILTERED` (runtime filter)
         INFO    -  97/121 magpie_f777ni/stm32f777xx kernel.events.usage                                :bgn:`PASSED` (device: DT04BNT1, 4.660s <zephyr>)
         INFO    -  98/121 magpie_f777ni/stm32f777xx kernel.lifo.usage                                  :bgn:`PASSED` (device: DT04BNT1, 3.813s <zephyr>)
         INFO    -  99/121 magpie_f777ni/stm32f777xx kernel.lifo                                        :bgn:`PASSED` (device: DT04BNT1, 2.979s <zephyr>)
         INFO    - 100/121 magpie_f777ni/stm32f777xx kernel.memory_protection.stack_random              :bgn:`PASSED` (device: DT04BNT1, 4.332s <zephyr>)
         INFO    - 101/121 magpie_f777ni/stm32f777xx kernel.memory_protection.sys_sem.nouser            :bgn:`PASSED` (device: DT04BNT1, 4.585s <zephyr>)
         INFO    - 102/121 magpie_f777ni/stm32f777xx kernel.memory_protection.stackprot                 :bgn:`PASSED` (device: DT04BNT1, 3.555s <zephyr>)
         INFO    - 103/121 magpie_f777ni/stm32f777xx kernel.memory_protection.mem_map                   :byl:`FILTERED` (runtime filter)
         INFO    - 104/121 magpie_f777ni/stm32f777xx kernel.futex                                       :bgn:`PASSED` (device: DT04BNT1, 3.778s <zephyr>)
         INFO    - 105/121 magpie_f777ni/stm32f777xx kernel.mutex.system.nouser                         :bgn:`PASSED` (device: DT04BNT1, 9.996s <zephyr>)
         INFO    - 106/121 magpie_f777ni/stm32f777xx kernel.memory_protection.sys_sem                   :bgn:`PASSED` (device: DT04BNT1, 6.098s <zephyr>)
         INFO    - 107/121 magpie_f777ni/stm32f777xx kernel.mutex.system                                :bgn:`PASSED` (device: DT04BNT1, 11.558s <zephyr>)
         INFO    - 108/121 magpie_f777ni/stm32f777xx kernel.mutex.scalable                              :bgn:`PASSED` (device: DT04BNT1, 17.353s <zephyr>)
         INFO    - 109/121 magpie_f777ni/stm32f777xx kernel.mutex                                       :bgn:`PASSED` (device: DT04BNT1, 16.269s <zephyr>)
         INFO    - 110/121 magpie_f777ni/stm32f777xx kernel.mutex.error                                 :bgn:`PASSED` (device: DT04BNT1, 5.079s <zephyr>)
         INFO    - 111/121 magpie_f777ni/stm32f777xx kernel.context                                     :bgn:`PASSED` (device: DT04BNT1, 8.006s <zephyr>)
         INFO    - 112/121 magpie_f777ni/stm32f777xx kernel.context.minimallibc                         :bgn:`PASSED` (device: DT04BNT1, 9.821s <zephyr>)
         INFO    - 113/121 magpie_f777ni/stm32f777xx integration.kernel                                 :bgn:`PASSED` (device: DT04BNT1, 2.563s <zephyr>)
         INFO    - 114/121 magpie_f777ni/stm32f777xx libraries.p4wq                                     :bgn:`PASSED` (device: DT04BNT1, 2.622s <zephyr>)
         INFO    - 115/121 magpie_f777ni/stm32f777xx arch.common.xip.minimallibc                        :bgn:`PASSED` (device: DT04BNT1, 3.749s <zephyr>)
         INFO    - 116/121 magpie_f777ni/stm32f777xx arch.common.xip                                    :bgn:`PASSED` (device: DT04BNT1, 3.532s <zephyr>)
         INFO    - 117/121 magpie_f777ni/stm32f777xx arch.shared_interrupt.lto.speed                    :bgn:`PASSED` (device: DT04BNT1, 2.712s <zephyr>)
         INFO    - 118/121 magpie_f777ni/stm32f777xx arch.shared_interrupt.lto                          :bgn:`PASSED` (device: DT04BNT1, 2.776s <zephyr>)
         INFO    - 119/121 magpie_f777ni/stm32f777xx arch.shared_interrupt                              :bgn:`PASSED` (device: DT04BNT1, 2.572s <zephyr>)
         INFO    - 120/121 magpie_f777ni/stm32f777xx arch.interrupt.minimallibc                         :bgn:`PASSED` (device: DT04BNT1, 2.502s <zephyr>)
         INFO    - 121/121 magpie_f777ni/stm32f777xx arch.interrupt                                     :bgn:`PASSED` (device: DT04BNT1, 2.495s <zephyr>)

         INFO    - 2867 test scenarios (2655 configurations) selected, :byl:`2547` configurations filtered (:byl:`2534` by static filter, :byl:`13` at runtime).
         INFO    - :bgn:`108 of 108` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`2363.24 seconds`.
         INFO    - 1344 of 1344 executed test cases passed (100.00%) on 1 out of total 1293 platforms (0.08%).
         INFO    - 51 selected test cases not executed: 51 skipped.
         INFO    - :bgn:`108` test configurations executed on platforms, :bbl:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board                     \| ID       \|   Counter \|   Failures \|
         \|---------------------------\|----------\|-----------\|------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \|       108 \|          0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni/stm32f777xx...
         INFO    - Writing JSON report .../twister-out/magpie_f777ni_stm32f777xx.json
         INFO    - Run completed
