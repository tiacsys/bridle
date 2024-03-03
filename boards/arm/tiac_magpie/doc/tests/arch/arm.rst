.. _tiac_magpie_arch_arm-tests:

ARM Architecture
################

Overview
********

See :zephyr_file:`tests/arch/arm`
for the original scope of tests, its structure and description.

.. _tiac_magpie_arch_arm-tests-requirements:

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
              --testsuite-root zephyr/tests --tag arm --tag vector_relay

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
         INFO    - 1550/1570 tiac_magpie               tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features.secure_fw :byl:`SKIPPED` (runtime filter)
         INFO    - 1551/1570 tiac_magpie               tests/arch/arm/arm_mem_protect/arch.arm.mem_protect.syscalls :byl:`SKIPPED` (runtime filter)
         INFO    - 1552/1570 tiac_magpie               tests/arch/arm/arm_irq_vector_table/arch.arm.irq_vector_table :bgn:`PASSED` (device: DT04BNT1, 5.098s)
         INFO    - 1553/1570 tiac_magpie               tests/arch/arm/arm_runtime_nmi/arch.interrupt.arm.nmi :bgn:`PASSED` (device: DT04BNT1, 6.820s)
         INFO    - 1554/1570 tiac_magpie               tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features :bgn:`PASSED` (device: DT04BNT1, 2.615s)
         INFO    - 1555/1570 tiac_magpie               tests/arch/arm/arm_thread_swap_tz/arch.arm.swap.tz_off :byl:`SKIPPED` (runtime filter)
         INFO    - 1556/1570 tiac_magpie               tests/arch/arm/arm_tz_wrap_func/arch.arm.tz_wrap_func :bgn:`PASSED` (device: DT04BNT1, 2.521s)
         INFO    - 1557/1570 tiac_magpie               tests/arch/arm/arm_thread_swap_tz/arch.arm.swap.tz :byl:`SKIPPED` (runtime filter)
         INFO    - 1558/1570 tiac_magpie               tests/arch/arm/arm_sw_vector_relay/arch.arm.sw_vector_relay :bgn:`PASSED` (device: DT04BNT1, 2.760s)
         INFO    - 1559/1570 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing.no_optimizations :bgn:`PASSED` (device: DT04BNT1, 8.432s)
         INFO    - 1560/1570 tiac_magpie               tests/arch/arm/arm_irq_zero_latency_levels/arch.arm.irq_zero_latency_levels.secure_fw :byl:`SKIPPED` (runtime filter)
         INFO    - 1561/1570 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.no_optimizations :bgn:`PASSED` (device: DT04BNT1, 6.293s)
         INFO    - 1562/1570 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing :bgn:`PASSED` (device: DT04BNT1, 3.203s)
         INFO    - 1563/1570 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common :bgn:`PASSED` (device: DT04BNT1, 4.062s)
         INFO    - 1564/1570 tiac_magpie               tests/arch/arm/arm_irq_zero_latency_levels/arch.arm.irq_zero_latency_levels :bgn:`PASSED` (device: DT04BNT1, 3.670s)
         INFO    - 1565/1570 tiac_magpie               tests/arch/arm/arm_interrupt/arch.interrupt.no_optimizations :bgn:`PASSED` (device: DT04BNT1, 8.092s)
         INFO    - 1566/1570 tiac_magpie               tests/arch/arm/arm_interrupt/arch.interrupt.extra_exception_info :bgn:`PASSED` (device: DT04BNT1, 3.838s)
         INFO    - 1567/1570 tiac_magpie               tests/arch/arm64/arm64_psci/arch.arm64.psci        :byl:`SKIPPED` (runtime filter)
         INFO    - 1568/1570 tiac_magpie               tests/arch/arm/arm_interrupt/arch.interrupt.arm    :bgn:`PASSED` (device: DT04BNT1, 3.306s)
         INFO    - 1569/1570 tiac_magpie               tests/arch/arm/arm_ramfunc/arch.arm.ramfunc        :bgn:`PASSED` (device: DT04BNT1, 3.827s)
         INFO    - 1570/1570 tiac_magpie               tests/arch/arm/arm_hardfault_validation/arch.interrupt.arm.hardfault_validation :bgn:`PASSED` (device: DT04BNT1, 2.539s)

         INFO    - 1782 test scenarios (1570 test instances) selected, 1555 configurations skipped (1549 by static filter, 6 at runtime).
         INFO    - :bgn:`15 of 1570` test configurations passed (100.00%), :bbk:`0 failed, :bbk:`0` errored, :byl:`1555` skipped with :bbk:`0` warnings in :bbk:`249.23 seconds`
         INFO    - In total 34 test cases were executed, 10963 skipped on 1 out of total 640 platforms (0.16%)
         INFO    - :bgn:`15` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|        15 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
