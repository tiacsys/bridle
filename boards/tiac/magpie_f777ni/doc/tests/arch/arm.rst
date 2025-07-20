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
         INFO    -  1/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_mem_protect/arch.arm.mem_protect.syscalls :byl:`FILTERED` (runtime filter)
         INFO    -  2/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features.secure_fw :byl:`FILTERED` (runtime filter)
         INFO    -  3/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_irq_vector_table/arch.arm.irq_vector_table :bgn:`PASSED` (device: DT04BNT1, 3.181s <zephyr>)
         INFO    -  4/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_runtime_nmi/arch.arm.interrupt.nmi :bgn:`PASSED` (device: DT04BNT1, 4.480s <zephyr>)
         INFO    -  5/22 magpie_f777ni/stm32f777xx tests/arch/common/ramfunc/arch.common.ramfunc      :bgn:`PASSED` (device: DT04BNT1, 3.821s <zephyr>)
         INFO    -  6/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features :bgn:`PASSED` (device: DT04BNT1, 2.683s <zephyr>)
         INFO    -  7/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_thread_swap_tz/arch.arm.swap.tz_off :byl:`FILTERED` (runtime filter)
         INFO    -  8/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_tz_wrap_func/arch.arm.tz_wrap_func :bgn:`PASSED` (device: DT04BNT1, 3.817s <zephyr>)
         INFO    -  9/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_thread_swap_tz/arch.arm.swap.tz :byl:`FILTERED` (runtime filter)
         INFO    - 10/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_sw_vector_relay/arch.arm.sw_vector_relay :bgn:`PASSED` (device: DT04BNT1, 2.391s <zephyr>)
         INFO    - 11/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing.no_optimizations :bgn:`PASSED` (device: DT04BNT1, 7.111s <zephyr>)
         INFO    - 12/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_irq_zero_latency_levels/arch.arm.irq_zero_latency_levels.secure_fw :byl:`FILTERED` (runtime filter)
         INFO    - 13/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_thread_swap/arch.arm.swap.common.no_optimizations :bgn:`PASSED` (device: DT04BNT1, 6.043s <zephyr>)
         INFO    - 14/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing :bgn:`PASSED` (device: DT04BNT1, 3.754s <zephyr>)
         INFO    - 15/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_thread_swap/arch.arm.swap.common :bgn:`PASSED` (device: DT04BNT1, 3.121s <zephyr>)
         INFO    - 16/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_irq_zero_latency_levels/arch.arm.irq_zero_latency_levels :bgn:`PASSED` (device: DT04BNT1, 4.573s <zephyr>)
         INFO    - 17/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_interrupt/arch.arm.interrupt.no_optimizations :bgn:`PASSED` (device: DT04BNT1, 6.180s <zephyr>)
         INFO    - 18/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_interrupt/arch.arm.interrupt.extra_exception_info :bgn:`PASSED` (device: DT04BNT1, 3.636s <zephyr>)
         INFO    - 19/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_interrupt/arch.arm.interrupt    :bgn:`PASSED` (device: DT04BNT1, 4.241s <zephyr>)
         INFO    - 20/22 magpie_f777ni/stm32f777xx tests/arch/arm64/arm64_psci/arch.arm64.psci        :byl:`FILTERED` (runtime filter)
         INFO    - 21/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_custom_interrupt/arch.arm.custom_interrupt :bgn:`PASSED` (device: DT04BNT1, 2.360s <zephyr>)
         INFO    - 22/22 magpie_f777ni/stm32f777xx tests/arch/arm/arm_hardfault_validation/arch.arm.interrupt.hardfault_validation :bgn:`PASSED` (device: DT04BNT1, 2.389s <zephyr>)

         INFO    - 2763 test scenarios (2539 configurations) selected, :byl:`2523` configurations filtered (2517 by static filter, 6 at runtime).
         INFO    - :bgn:`16 of 16` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`330.03 seconds`.
         INFO    - 32 of 32 executed test cases passed (100.00%) on 1 out of total 1133 platforms (0.09%).
         INFO    - 3 selected test cases not executed: 3 skipped.
         INFO    - :bgn:`16` test configurations executed on platforms, :bbl:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board                     \| ID       \|   Counter \|   Failures \|
         \|---------------------------\|----------\|-----------\|------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \|        16 \|          0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni/stm32f777xx...
         INFO    - Writing JSON report .../twister-out/magpie_f777ni_stm32f777xx.json
         INFO    - Run completed
