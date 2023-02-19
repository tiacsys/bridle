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
             --testcase-root zephyr/tests/arch/arm

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - 19 test scenarios (19 configurations) selected, 1 configurations discarded due to filters.
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    -  1/18 tiac_magpie               tests/arch/arm/arm_mem_protect/arch.arm.mem_protect.syscalls :byl:`SKIPPED` (filter)
         INFO    -  2/18 tiac_magpie               tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features.secure_fw :byl:`SKIPPED` (filter)
         INFO    -  3/18 tiac_magpie               tests/arch/arm/arm_irq_vector_table/arch.arm.irq_vector_table :bgn:`PASSED` (device 2.593s)
         INFO    -  4/18 tiac_magpie               tests/arch/arm/arm_runtime_nmi/arch.interrupt.arm.nmi :bgn:`PASSED` (device 13.859s)
         INFO    -  5/18 tiac_magpie               tests/arch/arm/arm_thread_swap_tz/arch.arm.swap.tz_off :byl:`SKIPPED` (filter)
         INFO    -  6/18 tiac_magpie               tests/arch/arm/arm_tz_wrap_func/arch.arm.tz_wrap_func :bgn:`PASSED` (device 3.840s)
         INFO    -  7/18 tiac_magpie               tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features :bgn:`PASSED` (device 3.985s)
         INFO    -  8/18 tiac_magpie               tests/arch/arm/arm_thread_swap_tz/arch.arm.swap.tz :byl:`SKIPPED` (filter)
         INFO    -  9/18 tiac_magpie               tests/arch/arm/arm_sw_vector_relay/arch.arm.sw_vector_relay :bgn:`PASSED` (device 3.842s)
         INFO    - 10/18 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing.no_optimizations :bgn:`PASSED` (device 11.635s)
         INFO    - 11/18 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.no_optimizations :bgn:`PASSED` (device 11.378s)
         INFO    - 12/18 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing :bgn:`PASSED` (device 5.399s)
         INFO    - 13/18 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common :bgn:`PASSED` (device 5.335s)
         INFO    - 14/18 tiac_magpie               tests/arch/arm/arm_interrupt/arch.interrupt.extra_exception_info :bgn:`PASSED` (device 5.397s)
         INFO    - 15/18 tiac_magpie               tests/arch/arm/arm_interrupt/arch.interrupt.no_optimizations :bgn:`PASSED` (device 11.519s)
         INFO    - 16/18 tiac_magpie               tests/arch/arm/arm_interrupt/arch.interrupt.arm    :bgn:`PASSED` (device 5.461s)
         INFO    - 17/18 tiac_magpie               tests/arch/arm/arm_ramfunc/arch.arm.ramfunc        :bgn:`PASSED` (device 5.156s)
         INFO    - 18/18 tiac_magpie               tests/arch/arm/arm_hardfault_validation/arch.interrupt.arm.hardfault_validation :bgn:`PASSED` (device 4.204s)

         INFO    - :bgn:`14 of 14` test configurations passed (100.00%), :bbk:`0` failed, :byl:`5` skipped with :bbk:`0` warnings in :bbk:`297.63 seconds`
         INFO    - In total 33 test cases were executed, 7 skipped on 1 out of total 428 platforms (0.23%)
         INFO    - :bgn:`14` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|        14 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Using 'zephyr' toolchain.
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
