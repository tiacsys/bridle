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

         $ ./zephyr/scripts/twister \
             --verbose --jobs 4 --inline-logs \
             --enable-size-report --platform-reports \
             --device-testing --hardware-map map.yaml \
             --board-root bridle/boards \
             --testsuite-root zephyr/tests/arch/arm

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - 21 test scenarios (21 configurations) selected, 1 configurations discarded due to filters.
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    -  2/21 tiac_magpie               tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features.secure_fw :byl:`SKIPPED` (runtime filter)
         INFO    -  3/21 tiac_magpie               tests/arch/arm/arm_mem_protect/arch.arm.mem_protect.syscalls :byl:`SKIPPED` (runtime filter)
         INFO    -  4/21 tiac_magpie               tests/arch/arm/arm_irq_vector_table/arch.arm.irq_vector_table :bgn:`PASSED` (device 5.202s)
         INFO    -  5/21 tiac_magpie               tests/arch/arm/arm_runtime_nmi/arch.interrupt.arm.nmi :bgn:`PASSED` (device 15.271s)
         INFO    -  6/21 tiac_magpie               tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features :bgn:`PASSED` (device 3.957s)
         INFO    -  7/21 tiac_magpie               tests/arch/arm/arm_thread_swap_tz/arch.arm.swap.tz_off :byl:`SKIPPED` (runtime filter)
         INFO    -  8/21 tiac_magpie               tests/arch/arm/arm_tz_wrap_func/arch.arm.tz_wrap_func :bgn:`PASSED` (device 3.355s)
         INFO    -  9/21 tiac_magpie               tests/arch/arm/arm_thread_swap_tz/arch.arm.swap.tz :byl:`SKIPPED` (runtime filter)
         INFO    - 10/21 tiac_magpie               tests/arch/arm/arm_sw_vector_relay/arch.arm.sw_vector_relay :bgn:`PASSED` (device 3.331s)
         INFO    - 11/21 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing.no_optimizations :bgn:`PASSED` (device 9.218s)
         INFO    - 12/21 tiac_magpie               tests/arch/arm/arm_irq_zero_latency_levels/arch.arm.irq_zero_latency_levels.secure_fw :byl:`SKIPPED` (runtime filter)
         INFO    - 13/21 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.no_optimizations :bgn:`PASSED` (device 9.239s)
         INFO    - 14/21 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing :bgn:`PASSED` (device 5.189s)
         INFO    - 15/21 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common :bgn:`PASSED` (device 4.812s)
         INFO    - 16/21 tiac_magpie               tests/arch/arm/arm_irq_zero_latency_levels/arch.arm.irq_zero_latency_levels :bgn:`PASSED` (device 4.093s)
         INFO    - 17/21 tiac_magpie               tests/arch/arm/arm_interrupt/arch.interrupt.no_optimizations :bgn:`PASSED` (device 9.314s)
         INFO    - 18/21 tiac_magpie               tests/arch/arm/arm_interrupt/arch.interrupt.extra_exception_info :bgn:`PASSED` (device 4.827s)
         INFO    - 19/21 tiac_magpie               tests/arch/arm/arm_ramfunc/arch.arm.ramfunc        :bgn:`PASSED` (device 5.151s)
         INFO    - 20/21 tiac_magpie               tests/arch/arm/arm_interrupt/arch.interrupt.arm    :bgn:`PASSED` (device 5.266s)
         INFO    - 21/21 tiac_magpie               tests/arch/arm/arm_hardfault_validation/arch.interrupt.arm.hardfault_validation :bgn:`PASSED` (device 3.432s)

         INFO    - :bgn:`15 of 21` test configurations passed (100.00%), :bbk:`0` failed, :byl:`6` skipped with :bbk:`0` warnings in :bbk:`194.56 seconds`
         INFO    - In total 16 test cases were executed, 5 skipped on 1 out of total 501 platforms (0.20%)
         INFO    - :bgn:`15` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|        15 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Using 'zephyr' toolchain.
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
