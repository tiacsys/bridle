.. _magpie_f777ni_arch_arm-tests:

ARM Architecture
################

Overview
********

See :zephyr_file:`tests/arch/arm`
for the original scope of tests, its structure and description.

.. _magpie_f777ni_arch_arm-tests-requirements:

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
                --testsuite-root zephyr/tests --tag arm --tag vector_relay

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
         INFO    -  1/25 magpie_f777ni/stm32f777xx arch.arm.mem_protect.syscalls                      :byl:`FILTERED` (runtime filter)
         INFO    -  2/25 magpie_f777ni/stm32f777xx arch.arm.irq_advanced_features.secure_fw           :byl:`FILTERED` (runtime filter)
         INFO    -  3/25 magpie_f777ni/stm32f777xx arch.arm.irq_vector_table                          :bgn:`PASSED` (device: DT04BNT1, 3.248s <zephyr>)
         INFO    -  4/25 magpie_f777ni/stm32f777xx arch.arm.interrupt.nmi                             :bgn:`PASSED` (device: DT04BNT1, 4.363s <zephyr>)
         INFO    -  5/25 magpie_f777ni/stm32f777xx arch.common.ramfunc                                :bgn:`PASSED` (device: DT04BNT1, 4.649s <zephyr>)
         INFO    -  6/25 magpie_f777ni/stm32f777xx arch.arm.irq_advanced_features                     :bgn:`PASSED` (device: DT04BNT1, 2.471s <zephyr>)
         INFO    -  7/25 magpie_f777ni/stm32f777xx arch.arm.tz_wrap_func                              :bgn:`PASSED` (device: DT04BNT1, 3.401s <zephyr>)
         INFO    -  8/25 magpie_f777ni/stm32f777xx arch.arm.user.stack.float                          :bgn:`PASSED` (device: DT04BNT1, 4.397s <zephyr>)
         INFO    -  9/25 magpie_f777ni/stm32f777xx arch.arm.sw_vector_relay.sram_vector_table         :bgn:`PASSED` (device: DT04BNT1, 2.562s <zephyr>)
         INFO    - 10/25 magpie_f777ni/stm32f777xx arch.arm.user.stack                                :bgn:`PASSED` (device: DT04BNT1, 4.143s <zephyr>)
         INFO    - 11/25 magpie_f777ni/stm32f777xx arch.arm.swap.tz_off                               :byl:`FILTERED` (runtime filter)
         INFO    - 12/25 magpie_f777ni/stm32f777xx arch.arm.sw_vector_relay                           :bgn:`PASSED` (device: DT04BNT1, 2.450s <zephyr>)
         INFO    - 13/25 magpie_f777ni/stm32f777xx arch.arm.swap.tz                                   :byl:`FILTERED` (runtime filter)
         INFO    - 14/25 magpie_f777ni/stm32f777xx arch.arm.swap.common.fpu_sharing.no_optimizations  :bgn:`PASSED` (device: DT04BNT1, 6.055s <zephyr>)
         INFO    - 15/25 magpie_f777ni/stm32f777xx arch.arm.swap.common.no_optimizations              :bgn:`PASSED` (device: DT04BNT1, 6.139s <zephyr>)
         INFO    - 16/25 magpie_f777ni/stm32f777xx arch.arm.irq_zero_latency_levels.secure_fw         :byl:`FILTERED` (runtime filter)
         INFO    - 17/25 magpie_f777ni/stm32f777xx arch.arm.swap.common                               :bgn:`PASSED` (device: DT04BNT1, 3.169s <zephyr>)
         INFO    - 18/25 magpie_f777ni/stm32f777xx arch.arm.swap.common.fpu_sharing                   :bgn:`PASSED` (device: DT04BNT1, 3.702s <zephyr>)
         INFO    - 19/25 magpie_f777ni/stm32f777xx arch.arm.irq_zero_latency_levels                   :bgn:`PASSED` (device: DT04BNT1, 5.751s <zephyr>)
         INFO    - 20/25 magpie_f777ni/stm32f777xx arch.arm.interrupt.no_optimizations                :bgn:`PASSED` (device: DT04BNT1, 6.289s <zephyr>)
         INFO    - 21/25 magpie_f777ni/stm32f777xx arch.arm.interrupt.extra_exception_info            :bgn:`PASSED` (device: DT04BNT1, 3.423s <zephyr>)
         INFO    - 22/25 magpie_f777ni/stm32f777xx arch.arm.interrupt                                 :bgn:`PASSED` (device: DT04BNT1, 3.371s <zephyr>)
         INFO    - 23/25 magpie_f777ni/stm32f777xx arch.arm64.psci                                    :byl:`FILTERED` (runtime filter)
         INFO    - 24/25 magpie_f777ni/stm32f777xx arch.arm.custom_interrupt                          :bgn:`PASSED` (device: DT04BNT1, 2.360s <zephyr>)
         INFO    - 25/25 magpie_f777ni/stm32f777xx arch.arm.interrupt.hardfault_validation            :bgn:`PASSED` (device: DT04BNT1, 2.374s <zephyr>)

         INFO    - 2867 test scenarios (2655 configurations) selected, :byl:`2636` configurations filtered (:byl:`2630` by static filter, :byl:`6` at runtime).
         INFO    - :bgn:`19 of 19` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`451.20 seconds`.
         INFO    - 35 of 35 executed test cases passed (100.00%) on 1 out of total 1293 platforms (0.08%).
         INFO    - 3 selected test cases not executed: 3 skipped.
         INFO    - :bgn:`19` test configurations executed on platforms, :bbl:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board                     \| ID       \|   Counter \|   Failures \|
         \|---------------------------\|----------\|-----------\|------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \|        19 \|          0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni/stm32f777xx...
         INFO    - Writing JSON report .../twister-out/magpie_f777ni_stm32f777xx.json
         INFO    - Run completed
