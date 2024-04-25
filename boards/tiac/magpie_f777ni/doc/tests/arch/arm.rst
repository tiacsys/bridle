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
         :class: highlight-console notranslate

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1688/1709 tiac_magpie               tests/arch/arm/arm_mem_protect/arch.arm.mem_protect.syscalls :byl:`SKIPPED` (runtime filter)
         INFO    - 1689/1709 tiac_magpie               tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features.secure_fw :byl:`SKIPPED` (runtime filter)
         INFO    - 1690/1709 tiac_magpie               tests/arch/arm/arm_irq_vector_table/arch.arm.irq_vector_table :bgn:`PASSED` (device: DT04BNT1, 2.590s)
         INFO    - 1691/1709 tiac_magpie               tests/arch/arm/arm_runtime_nmi/arch.arm.interrupt.nmi :bgn:`PASSED` (device: DT04BNT1, 4.449s)
         INFO    - 1692/1709 tiac_magpie               tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features :bgn:`PASSED` (device: DT04BNT1, 2.506s)
         INFO    - 1693/1709 tiac_magpie               tests/arch/common/ramfunc/arch.common.ramfunc      :bgn:`PASSED` (device: DT04BNT1, 3.730s)
         INFO    - 1694/1709 tiac_magpie               tests/arch/arm/arm_tz_wrap_func/arch.arm.tz_wrap_func :bgn:`PASSED` (device: DT04BNT1, 2.656s)
         INFO    - 1695/1709 tiac_magpie               tests/arch/arm/arm_thread_swap_tz/arch.arm.swap.tz_off :byl:`SKIPPED` (runtime filter)
         INFO    - 1696/1709 tiac_magpie               tests/arch/arm/arm_thread_swap_tz/arch.arm.swap.tz :byl:`SKIPPED` (runtime filter)
         INFO    - 1697/1709 tiac_magpie               tests/arch/arm/arm_sw_vector_relay/arch.arm.sw_vector_relay :bgn:`PASSED` (device: DT04BNT1, 2.504s)
         INFO    - 1698/1709 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing.no_optimizations :bgn:`PASSED` (device: DT04BNT1, 6.067s)
         INFO    - 1699/1709 tiac_magpie               tests/arch/arm/arm_irq_zero_latency_levels/arch.arm.irq_zero_latency_levels.secure_fw :byl:`SKIPPED` (runtime filter)
         INFO    - 1700/1709 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.no_optimizations :bgn:`PASSED` (device: DT04BNT1, 6.086s)
         INFO    - 1701/1709 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing :bgn:`PASSED` (device: DT04BNT1, 3.804s)
         INFO    - 1702/1709 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common :bgn:`PASSED` (device: DT04BNT1, 3.185s)
         INFO    - 1703/1709 tiac_magpie               tests/arch/arm/arm_irq_zero_latency_levels/arch.arm.irq_zero_latency_levels :bgn:`PASSED` (device: DT04BNT1, 3.325s)
         INFO    - 1704/1709 tiac_magpie               tests/arch/arm/arm_interrupt/arch.arm.interrupt.no_optimizations :bgn:`PASSED` (device: DT04BNT1, 6.412s)
         INFO    - 1705/1709 tiac_magpie               tests/arch/arm/arm_interrupt/arch.arm.interrupt.extra_exception_info :bgn:`PASSED` (device: DT04BNT1, 3.633s)
         INFO    - 1706/1709 tiac_magpie               tests/arch/arm/arm_custom_interrupt/arch.arm.custom_interrupt :bgn:`PASSED` (device: DT04BNT1, 2.583s)
         INFO    - 1707/1709 tiac_magpie               tests/arch/arm64/arm64_psci/arch.arm64.psci        :byl:`SKIPPED` (runtime filter)
         INFO    - 1708/1709 tiac_magpie               tests/arch/arm/arm_interrupt/arch.arm.interrupt    :bgn:`PASSED` (device: DT04BNT1, 3.441s)
         INFO    - 1709/1709 tiac_magpie               tests/arch/arm/arm_hardfault_validation/arch.arm.interrupt.hardfault_validation :bgn:`PASSED` (device: DT04BNT1, 2.547s)

         INFO    - 1922 test scenarios (1709 test instances) selected, 1693 configurations skipped (1687 by static filter, 6 at runtime).
         INFO    - :bgn:`16 of 1709` test configurations passed (100.00%), :bbk:`0 failed, :bbk:`0` errored, :byl:`1693` skipped with :bbk:`0` warnings in :bbk:`166.19 seconds`
         INFO    - In total 35 test cases were executed, 12649 skipped on 1 out of total 699 platforms (0.14%)
         INFO    - :bgn:`16` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|        16 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
