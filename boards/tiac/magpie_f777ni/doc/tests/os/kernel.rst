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
         INFO    -   1/127 magpie_f777ni/stm32f777xx kernel.memory_slabs.stats                          :bgn:`PASSED` (device: DT04BNT1, 2.616s <zephyr/gnu>)
         INFO    -   2/127 magpie_f777ni/stm32f777xx kernel.pending.minimallibc                         :bgn:`PASSED` (device: DT04BNT1, 8.535s <zephyr/gnu>)
         INFO    -   3/127 magpie_f777ni/stm32f777xx kernel.memory_slabs.threadsafe                     :bgn:`PASSED` (device: DT04BNT1, 2.612s <zephyr/gnu>)
         INFO    -   4/127 magpie_f777ni/stm32f777xx kernel.ipi_optimize.smp                            :byl:`FILTERED` (runtime filter)
         INFO    -   5/127 magpie_f777ni/stm32f777xx kernel.stack.usage                                 :bgn:`PASSED` (device: DT04BNT1, 6.508s <zephyr/gnu>)
         INFO    -   6/127 magpie_f777ni/stm32f777xx kernel.semaphore                                   :bgn:`PASSED` (device: DT04BNT1, 16.923s <zephyr/gnu>)
         INFO    -   7/127 magpie_f777ni/stm32f777xx kernel.semaphore.usage                             :bgn:`PASSED` (device: DT04BNT1, 3.626s <zephyr/gnu>)
         INFO    -   8/127 magpie_f777ni/stm32f777xx kernel.common.lto.singlethreaded                   :bgn:`PASSED` (device: DT04BNT1, 6.884s <zephyr/gnu>)
         INFO    -   9/127 magpie_f777ni/stm32f777xx kernel.common.lto                                  :bgn:`PASSED` (device: DT04BNT1, 7.036s <zephyr/gnu>)
         INFO    -  10/127 magpie_f777ni/stm32f777xx kernel.common.picolibc                             :bgn:`PASSED` (device: DT04BNT1, 8.540s <zephyr/gnu>)
         INFO    -  11/127 magpie_f777ni/stm32f777xx kernel.common.misra                                :byl:`FILTERED` (runtime filter)
         INFO    -  12/127 magpie_f777ni/stm32f777xx kernel.common.nano32                               :bgn:`PASSED` (device: DT04BNT1, 9.894s <zephyr/gnu>)
         INFO    -  13/127 magpie_f777ni/stm32f777xx kernel.ipi_work                                    :byl:`FILTERED` (runtime filter)
         INFO    -  14/127 magpie_f777ni/stm32f777xx kernel.common.minimallibc                          :bgn:`PASSED` (device: DT04BNT1, 8.838s <zephyr/gnu>)
         INFO    -  15/127 magpie_f777ni/stm32f777xx kernel.obj_core                                    :bgn:`PASSED` (device: DT04BNT1, 2.733s <zephyr/gnu>)
         INFO    -  16/127 magpie_f777ni/stm32f777xx kernel.obj_core.stats                              :bgn:`PASSED` (device: DT04BNT1, 2.968s <zephyr/gnu>)
         INFO    -  17/127 magpie_f777ni/stm32f777xx kernel.usage                                       :bgn:`PASSED` (device: DT04BNT1, 2.904s <zephyr/gnu>)
         INFO    -  18/127 magpie_f777ni/stm32f777xx kernel.smp_abort                                   :byl:`FILTERED` (runtime filter)
         INFO    -  19/127 magpie_f777ni/stm32f777xx kernel.tickless.concept                            :bgn:`PASSED` (device: DT04BNT1, 4.514s <zephyr/gnu>)
         INFO    -  20/127 magpie_f777ni/stm32f777xx kernel.workqueue.work_timeout                      :bgn:`PASSED` (device: DT04BNT1, 11.179s <zephyr/gnu>)
         INFO    -  21/127 magpie_f777ni/stm32f777xx kernel.workqueue                                   :bgn:`PASSED` (device: DT04BNT1, 11.183s <zephyr/gnu>)
         INFO    -  22/127 magpie_f777ni/stm32f777xx kernel.workqueue.user                              :bgn:`PASSED` (device: DT04BNT1, 4.788s <zephyr/gnu>)
         INFO    -  23/127 magpie_f777ni/stm32f777xx kernel.common.profiling                            :bgn:`PASSED` (device: DT04BNT1, 2.917s <zephyr/gnu>)
         INFO    -  24/127 magpie_f777ni/stm32f777xx kernel.poll.minimallibc                            :bgn:`PASSED` (device: DT04BNT1, 7.595s <zephyr/gnu>)
         INFO    -  25/127 magpie_f777ni/stm32f777xx kernel.scheduler.preempt                           :bgn:`PASSED` (device: DT04BNT1, 4.618s <zephyr/gnu>)
         INFO    -  26/127 magpie_f777ni/stm32f777xx kernel.scheduler.metairq                           :bgn:`PASSED` (device: DT04BNT1, 2.663s <zephyr/gnu>)
         INFO    -  27/127 magpie_f777ni/stm32f777xx kernel.scheduler.deadline.scalable                 :bgn:`PASSED` (device: DT04BNT1, 3.747s <zephyr/gnu>)
         INFO    -  28/127 magpie_f777ni/stm32f777xx kernel.scheduler.deadline                          :bgn:`PASSED` (device: DT04BNT1, 5.295s <zephyr/gnu>)
         INFO    -  29/127 magpie_f777ni/stm32f777xx kernel.scheduler.simple_no_timeslicing             :bgn:`PASSED` (device: DT04BNT1, 6.791s <zephyr/gnu>)
         INFO    -  30/127 magpie_f777ni/stm32f777xx kernel.scheduler.multiq_no_timeslicing             :bgn:`PASSED` (device: DT04BNT1, 5.615s <zephyr/gnu>)
         INFO    -  31/127 magpie_f777ni/stm32f777xx kernel.scheduler.multiq                            :bgn:`PASSED` (device: DT04BNT1, 21.318s <zephyr/gnu>)
         INFO    -  32/127 magpie_f777ni/stm32f777xx kernel.multiprocessing.smp.affinity.custom_rom_offset :byl:`FILTERED` (runtime filter)
         INFO    -  33/127 magpie_f777ni/stm32f777xx kernel.multiprocessing.smp.affinity                :byl:`FILTERED` (runtime filter)
         INFO    -  34/127 magpie_f777ni/stm32f777xx kernel.multiprocessing.smp.minimallibc             :byl:`FILTERED` (runtime filter)
         INFO    -  35/127 magpie_f777ni/stm32f777xx kernel.scheduler.slice_perthread                   :bgn:`PASSED` (device: DT04BNT1, 22.822s <zephyr/gnu>)
         INFO    -  36/127 magpie_f777ni/stm32f777xx kernel.multiprocessing.smp                         :byl:`FILTERED` (runtime filter)
         INFO    -  37/127 magpie_f777ni/stm32f777xx kernel.objects.tracking                            :bgn:`PASSED` (device: DT04BNT1, 4.008s <zephyr/gnu>)
         INFO    -  38/127 magpie_f777ni/stm32f777xx kernel.objects.tracking.minimallibc                :bgn:`PASSED` (device: DT04BNT1, 3.749s <zephyr/gnu>)
         INFO    -  39/127 magpie_f777ni/stm32f777xx kernel.queue                                       :bgn:`PASSED` (device: DT04BNT1, 4.979s <zephyr/gnu>)
         INFO    -  40/127 magpie_f777ni/stm32f777xx kernel.queue.minimallibc                           :bgn:`PASSED` (device: DT04BNT1, 5.213s <zephyr/gnu>)
         INFO    -  41/127 magpie_f777ni/stm32f777xx kernel.smp_suspend                                 :byl:`FILTERED` (runtime filter)
         INFO    -  42/127 magpie_f777ni/stm32f777xx kernel.common.timing                               :bgn:`PASSED` (device: DT04BNT1, 8.519s <zephyr/gnu>)
         INFO    -  43/127 magpie_f777ni/stm32f777xx kernel.timer.timer                                 :bgn:`PASSED` (device: DT04BNT1, 33.367s <zephyr/gnu>)
         INFO    -  44/127 magpie_f777ni/stm32f777xx kernel.timer.timer_observer                        :bgn:`PASSED` (device: DT04BNT1, 3.659s <zephyr/gnu>)
         INFO    -  45/127 magpie_f777ni/stm32f777xx kernel.timer.error_case                            :bgn:`PASSED` (device: DT04BNT1, 5.734s <zephyr/gnu>)
         INFO    -  46/127 magpie_f777ni/stm32f777xx kernel.timer.timepoints                            :bgn:`PASSED` (device: DT04BNT1, 6.256s <zephyr/gnu>)
         INFO    -  47/127 magpie_f777ni/stm32f777xx kernel.timer.monotonic                             :bgn:`PASSED` (device: DT04BNT1, 6.499s <zephyr/gnu>)
         INFO    -  48/127 magpie_f777ni/stm32f777xx kernel.k_heap_api                                  :bgn:`PASSED` (device: DT04BNT1, 6.616s <zephyr/gnu>)
         INFO    -  49/127 magpie_f777ni/stm32f777xx kernel.cache.api.minimallibc                       :bgn:`PASSED` (device: DT04BNT1, 4.069s <zephyr/gnu>)
         INFO    -  50/127 magpie_f777ni/stm32f777xx kernel.fpu_sharing.float_disable                   :bgn:`PASSED` (device: DT04BNT1, 4.482s <zephyr/gnu>)
         INFO    -  51/127 magpie_f777ni/stm32f777xx kernel.fifo.usage                                  :bgn:`PASSED` (device: DT04BNT1, 2.551s <zephyr/gnu>)
         INFO    -  52/127 magpie_f777ni/stm32f777xx kernel.fifo.timeout                                :bgn:`PASSED` (device: DT04BNT1, 2.782s <zephyr/gnu>)
         INFO    -  53/127 magpie_f777ni/stm32f777xx kernel.common.sleep                                :bgn:`PASSED` (device: DT04BNT1, 5.053s <zephyr/gnu>)
         INFO    -  54/127 magpie_f777ni/stm32f777xx kernel.common.sleep.minimallibc                    :bgn:`PASSED` (device: DT04BNT1, 4.189s <zephyr/gnu>)
         INFO    -  55/127 magpie_f777ni/stm32f777xx kernel.threads.tls                                 :bgn:`PASSED` (device: DT04BNT1, 4.689s <zephyr/gnu>)
         INFO    -  56/127 magpie_f777ni/stm32f777xx kernel.threads.tls.userspace                       :bgn:`PASSED` (device: DT04BNT1, 4.807s <zephyr/gnu>)
         INFO    -  57/127 magpie_f777ni/stm32f777xx kernel.threads.apis                                :bgn:`PASSED` (device: DT04BNT1, 12.220s <zephyr/gnu>)
         INFO    -  58/127 magpie_f777ni/stm32f777xx kernel.ipi_cascade.smp                             :byl:`FILTERED` (runtime filter)
         INFO    -  59/127 magpie_f777ni/stm32f777xx kernel.threads.dynamic                             :bgn:`PASSED` (device: DT04BNT1, 4.322s <zephyr/gnu>)
         INFO    -  60/127 magpie_f777ni/stm32f777xx kernel.threads.init                                :bgn:`PASSED` (device: DT04BNT1, 8.614s <zephyr/gnu>)
         INFO    -  61/127 magpie_f777ni/stm32f777xx kernel.common.stack_protection_armv8m_mpu_stack_guard :byl:`FILTERED` (runtime filter)
         INFO    -  62/127 magpie_f777ni/stm32f777xx kernel.logging.message_capture                     :bgn:`PASSED` (device: DT04BNT1, 3.980s <zephyr/gnu>)
         INFO    -  63/127 magpie_f777ni/stm32f777xx kernel.common.stack_sentinel                       :bgn:`PASSED` (device: DT04BNT1, 2.796s <zephyr/gnu>)
         INFO    -  64/127 magpie_f777ni/stm32f777xx kernel.common.stack_protection_no_userspace        :bgn:`PASSED` (device: DT04BNT1, 3.926s <zephyr/gnu>)
         INFO    -  65/127 magpie_f777ni/stm32f777xx kernel.common.stack_protection_arm_fpu_sharing     :bgn:`PASSED` (device: DT04BNT1, 4.241s <zephyr/gnu>)
         INFO    -  66/127 magpie_f777ni/stm32f777xx kernel.common.stack_protection                     :bgn:`PASSED` (device: DT04BNT1, 3.620s <zephyr/gnu>)
         INFO    -  67/127 magpie_f777ni/stm32f777xx kernel.message_queue.put_front                     :bgn:`PASSED` (device: DT04BNT1, 5.012s <zephyr/gnu>)
         INFO    -  68/127 magpie_f777ni/stm32f777xx kernel.message_queue                               :bgn:`PASSED` (device: DT04BNT1, 5.013s <zephyr/gnu>)
         INFO    -  69/127 magpie_f777ni/stm32f777xx kernel.smp_metairq                                 :byl:`FILTERED` (runtime filter)
         INFO    -  70/127 magpie_f777ni/stm32f777xx kernel.message_queue.usage                         :bgn:`PASSED` (device: DT04BNT1, 4.692s <zephyr/gnu>)
         INFO    -  71/127 magpie_f777ni/stm32f777xx kernel.pipe.api                                    :bgn:`PASSED` (device: DT04BNT1, 6.804s <zephyr/gnu>)
         INFO    -  72/127 magpie_f777ni/stm32f777xx kernel.events                                      :bgn:`PASSED` (device: DT04BNT1, 3.129s <zephyr/gnu>)
         INFO    -  73/127 magpie_f777ni/stm32f777xx kernel.memory_protection.stackprot_tls             :byl:`FILTERED` (runtime filter)
         INFO    -  74/127 magpie_f777ni/stm32f777xx kernel.events.usage                                :bgn:`PASSED` (device: DT04BNT1, 4.917s <zephyr/gnu>)
         INFO    -  75/127 magpie_f777ni/stm32f777xx kernel.memory_protection.sys_sem.nouser            :bgn:`PASSED` (device: DT04BNT1, 3.308s <zephyr/gnu>)
         INFO    -  76/127 magpie_f777ni/stm32f777xx kernel.memory_protection.mem_map                   :byl:`FILTERED` (runtime filter)
         INFO    -  77/127 magpie_f777ni/stm32f777xx kernel.memory_protection.stackprot                 :bgn:`PASSED` (device: DT04BNT1, 4.336s <zephyr/gnu>)
         INFO    -  78/127 magpie_f777ni/stm32f777xx kernel.futex                                       :bgn:`PASSED` (device: DT04BNT1, 3.892s <zephyr/gnu>)
         INFO    -  79/127 magpie_f777ni/stm32f777xx kernel.mutex.system.nouser                         :bgn:`PASSED` (device: DT04BNT1, 10.205s <zephyr/gnu>)
         INFO    -  80/127 magpie_f777ni/stm32f777xx kernel.memory_protection.sys_sem                   :bgn:`PASSED` (device: DT04BNT1, 5.894s <zephyr/gnu>)
         INFO    -  81/127 magpie_f777ni/stm32f777xx kernel.mutex.system                                :bgn:`PASSED` (device: DT04BNT1, 11.727s <zephyr/gnu>)
         INFO    -  82/127 magpie_f777ni/stm32f777xx kernel.mutex                                       :bgn:`PASSED` (device: DT04BNT1, 17.498s <zephyr/gnu>)
         INFO    -  83/127 magpie_f777ni/stm32f777xx kernel.context                                     :bgn:`PASSED` (device: DT04BNT1, 8.973s <zephyr/gnu>)
         INFO    -  84/127 magpie_f777ni/stm32f777xx kernel.mutex.error                                 :bgn:`PASSED` (device: DT04BNT1, 4.273s <zephyr/gnu>)
         INFO    -  85/127 magpie_f777ni/stm32f777xx kernel.context.minimallibc                         :bgn:`PASSED` (device: DT04BNT1, 9.217s <zephyr/gnu>)
         INFO    -  86/127 magpie_f777ni/stm32f777xx integration.kernel                                 :bgn:`PASSED` (device: DT04BNT1, 2.813s <zephyr/gnu>)
         INFO    -  87/127 magpie_f777ni/stm32f777xx arch.interrupt.multilevel_l3                       :byl:`FILTERED` (runtime filter)
         INFO    -  88/127 magpie_f777ni/stm32f777xx libraries.p4wq                                     :bgn:`PASSED` (device: DT04BNT1, 3.019s <zephyr/gnu>)
         INFO    -  89/127 magpie_f777ni/stm32f777xx arch.interrupt.multilevel                          :byl:`FILTERED` (runtime filter)
         INFO    -  90/127 magpie_f777ni/stm32f777xx arch.common.xip.minimallibc                        :bgn:`PASSED` (device: DT04BNT1, 3.619s <zephyr/gnu>)
         INFO    -  91/127 magpie_f777ni/stm32f777xx arch.common.xip                                    :bgn:`PASSED` (device: DT04BNT1, 2.592s <zephyr/gnu>)
         INFO    -  92/127 magpie_f777ni/stm32f777xx arch.shared_interrupt.lto.speed                    :bgn:`PASSED` (device: DT04BNT1, 4.184s <zephyr/gnu>)
         INFO    -  93/127 magpie_f777ni/stm32f777xx arch.shared_interrupt                              :bgn:`PASSED` (device: DT04BNT1, 3.718s <zephyr/gnu>)
         INFO    -  94/127 magpie_f777ni/stm32f777xx kernel.memory_slabs.api                            :bgn:`PASSED` (device: DT04BNT1, 9.602s <zephyr/gnu>)
         INFO    -  95/127 magpie_f777ni/stm32f777xx kernel.timer                                       :bgn:`PASSED` (device: DT04BNT1, 7.388s <zephyr/gnu>)
         INFO    -  96/127 magpie_f777ni/stm32f777xx kernel.memory_slabs.concept                        :bgn:`PASSED` (device: DT04BNT1, 4.456s <zephyr/gnu>)
         INFO    -  97/127 magpie_f777ni/stm32f777xx kernel.poll                                        :bgn:`PASSED` (device: DT04BNT1, 8.340s <zephyr/gnu>)
         INFO    -  98/127 magpie_f777ni/stm32f777xx kernel.mutex.scalable                              :bgn:`PASSED` (device: DT04BNT1, 17.366s <zephyr/gnu>)
         INFO    -  99/127 magpie_f777ni/stm32f777xx kernel.timer.timeout                               :bgn:`PASSED` (device: DT04BNT1, 2.552s <zephyr/gnu>)
         INFO    - 100/127 magpie_f777ni/stm32f777xx kernel.lifo.usage                                  :bgn:`PASSED` (device: DT04BNT1, 3.077s <zephyr/gnu>)
         INFO    - 101/127 magpie_f777ni/stm32f777xx arch.interrupt.minimallibc                         :bgn:`PASSED` (device: DT04BNT1, 2.595s <zephyr/gnu>)
         INFO    - 102/127 magpie_f777ni/stm32f777xx kernel.common.timing.minimallibc                   :bgn:`PASSED` (device: DT04BNT1, 6.144s <zephyr/gnu>)
         INFO    - 103/127 magpie_f777ni/stm32f777xx kernel.workqueue.critical                          :bgn:`PASSED` (device: DT04BNT1, 2.660s <zephyr/gnu>)
         INFO    - 104/127 magpie_f777ni/stm32f777xx kernel.device.pm                                   :bgn:`PASSED` (device: DT04BNT1, 4.158s <zephyr/gnu>)
         INFO    - 105/127 magpie_f777ni/stm32f777xx kernel.mailbox.usage                               :bgn:`PASSED` (device: DT04BNT1, 2.570s <zephyr/gnu>)
         INFO    - 106/127 magpie_f777ni/stm32f777xx kernel.cache.api                                   :bgn:`PASSED` (device: DT04BNT1, 3.815s <zephyr/gnu>)
         INFO    - 107/127 magpie_f777ni/stm32f777xx kernel.common                                      :bgn:`PASSED` (device: DT04BNT1, 8.447s <zephyr/gnu>)
         INFO    - 108/127 magpie_f777ni/stm32f777xx arch.interrupt                                     :bgn:`PASSED` (device: DT04BNT1, 2.580s <zephyr/gnu>)
         INFO    - 109/127 magpie_f777ni/stm32f777xx kernel.lifo                                        :bgn:`PASSED` (device: DT04BNT1, 3.077s <zephyr/gnu>)
         INFO    - 110/127 magpie_f777ni/stm32f777xx kernel.scheduler.wraparound                        :bgn:`PASSED` (device: DT04BNT1, 2.492s <zephyr/gnu>)
         INFO    - 111/127 magpie_f777ni/stm32f777xx arch.shared_interrupt.lto                          :bgn:`PASSED` (device: DT04BNT1, 2.687s <zephyr/gnu>)
         INFO    - 112/127 magpie_f777ni/stm32f777xx kernel.scheduler.simple_timeslicing                :bgn:`PASSED` (device: DT04BNT1, 21.382s <zephyr/gnu>)
         INFO    - 113/127 magpie_f777ni/stm32f777xx kernel.device.minimallibc                          :bgn:`PASSED` (device: DT04BNT1, 4.144s <zephyr/gnu>)
         INFO    - 114/127 magpie_f777ni/stm32f777xx kernel.threads.error.case                          :bgn:`PASSED` (device: DT04BNT1, 3.569s <zephyr/gnu>)
         INFO    - 115/127 magpie_f777ni/stm32f777xx kernel.scheduler.no_timeslicing                    :bgn:`PASSED` (device: DT04BNT1, 5.519s <zephyr/gnu>)
         INFO    - 116/127 magpie_f777ni/stm32f777xx kernel.memory_slabs                                :bgn:`PASSED` (device: DT04BNT1, 2.586s <zephyr/gnu>)
         INFO    - 117/127 magpie_f777ni/stm32f777xx kernel.device                                      :bgn:`PASSED` (device: DT04BNT1, 4.136s <zephyr/gnu>)
         INFO    - 118/127 magpie_f777ni/stm32f777xx kernel.common.nano64                               :bgn:`PASSED` (device: DT04BNT1, 8.461s <zephyr/gnu>)
         INFO    - 119/127 magpie_f777ni/stm32f777xx kernel.condvar                                     :bgn:`PASSED` (device: DT04BNT1, 4.945s <zephyr/gnu>)
         INFO    - 120/127 magpie_f777ni/stm32f777xx kernel.fifo                                        :bgn:`PASSED` (device: DT04BNT1, 3.173s <zephyr/gnu>)
         INFO    - 121/127 magpie_f777ni/stm32f777xx kernel.obj_core.stats.api                          :bgn:`PASSED` (device: DT04BNT1, 2.586s <zephyr/gnu>)
         INFO    - 122/127 magpie_f777ni/stm32f777xx kernel.scheduler                                   :bgn:`PASSED` (device: DT04BNT1, 21.345s <zephyr/gnu>)
         INFO    - 123/127 magpie_f777ni/stm32f777xx kernel.mailbox.api                                 :bgn:`PASSED` (device: DT04BNT1, 3.105s <zephyr/gnu>)
         INFO    - 124/127 magpie_f777ni/stm32f777xx kernel.memory_protection.stack_random              :bgn:`PASSED` (device: DT04BNT1, 3.115s <zephyr/gnu>)
         INFO    - 125/127 magpie_f777ni/stm32f777xx kernel.common.tls                                  :bgn:`PASSED` (device: DT04BNT1, 8.459s <zephyr/gnu>)
         INFO    - 126/127 magpie_f777ni/stm32f777xx kernel.workqueue.api                               :bgn:`PASSED` (device: DT04BNT1, 4.694s <zephyr/gnu>)
         INFO    - 127/127 magpie_f777ni/stm32f777xx kernel.pending                                     :bgn:`PASSED` (device: DT04BNT1, 8.473s <zephyr/gnu>)

         INFO    - 3090 test scenarios (2888 configurations) selected, :byl:`2777` configurations filtered (:byl:`2761` by static filter, :byl:`16` at runtime).
         INFO    - :bgn:`111 of 111` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`2770.69 seconds`.
         INFO    - 1411 of 1411 executed test cases passed (100.00%) on 1 out of total 1511 platforms (0.07%).
         INFO    - 52 selected test cases not executed: 52 skipped.
         INFO    - :bgn:`111` test configurations executed on platforms, :bbl:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board                     \| ID       \|   Counter \|   Failures \|
         \|---------------------------\|----------\|-----------\|------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \|       111 \|          0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni/stm32f777xx...
         INFO    - Writing JSON report .../twister-out/magpie_f777ni_stm32f777xx.json
         INFO    - Run completed
