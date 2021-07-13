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

         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    -  1/16 tiac_magpie               tests/arch/arm/arm_irq_vector_table/arch.arm.irq_vector_table :bgn:`PASSED` (device 2.662s)
         INFO    -  2/16 tiac_magpie               tests/arch/arm/arm_runtime_nmi/arch.interrupt.arm.nmi :bgn:`PASSED` (device 13.769s)
         INFO    -  3/16 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing.no_optimizations :bgn:`PASSED` (device 10.762s)
         INFO    -  4/16 tiac_magpie               tests/arch/arm/arm_ramfunc/arch.arm.ramfunc        :bgn:`PASSED` (device 5.130s)
         INFO    -  5/16 tiac_magpie               tests/arch/arm/arm_thread_swap_tz/arch.arm.swap.tz_off :byl:`SKIPPED` (filter)
         INFO    -  6/16 tiac_magpie               tests/arch/arm/arm_thread_swap_tz/arch.arm.swap.tz :byl:`SKIPPED` (filter)
         INFO    -  7/16 tiac_magpie               tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features.secure_fw :byl:`SKIPPED` (filter)
         INFO    -  8/16 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing :bgn:`PASSED` (device 5.127s)
         INFO    -  9/16 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.no_optimizations :bgn:`PASSED` (device 10.938s)
         INFO    - 10/16 tiac_magpie               tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features :bgn:`PASSED` (device 3.751s)
         INFO    - 11/16 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common :bgn:`PASSED` (device 5.172s)
         INFO    - 12/16 tiac_magpie               tests/arch/arm/arm_tz_wrap_func/arch.arm.tz_wrap_func :bgn:`PASSED` (device 3.733s)
         INFO    - 13/16 tiac_magpie               tests/arch/arm/arm_sw_vector_relay/arch.arm.sw_vector_relay :bgn:`PASSED` (device 3.672s)
         INFO    - 14/16 tiac_magpie               tests/arch/arm/arm_interrupt/arch.interrupt.no_optimizations :bgn:`PASSED` (device 11.555s)
         INFO    - 15/16 tiac_magpie               tests/arch/arm/arm_interrupt/arch.interrupt.extra_exception_info :bgn:`PASSED` (device 5.999s)
         INFO    - 16/16 tiac_magpie               tests/arch/arm/arm_interrupt/arch.interrupt.arm    :bgn:`PASSED` (device 5.747s)

         INFO    - :bgn:`13 of 13` test configurations passed (100.00%), :bbk:`0` failed, :byl:`4` skipped with :bbk:`0` warnings in :bbk:`158.84 seconds`
         INFO    - In total 32 test cases were executed, 6 skipped on 1 out of total 370 platforms (0.27%)
         INFO    - :bgn:`13` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|        13 \|
