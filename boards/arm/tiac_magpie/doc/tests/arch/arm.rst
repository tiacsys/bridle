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
             --board-root bridle/boards \
             --platform tiac_magpie \
             --device-testing --device-serial /dev/ttyUSBx \
             --testcase-root zephyr/tests/arch/arm

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    -  1/16 tiac_magpie               tests/arch/arm/arm_psci/arch.arm64.psci            :byl:`SKIPPED` (filter)
         INFO    -  2/16 tiac_magpie               tests/arch/arm/arm_irq_vector_table/arch.interrupt.arm.irq_vector_table :bgn:`PASSED` (device 2.802s)
         INFO    -  3/16 tiac_magpie               tests/arch/arm/arm_runtime_nmi/arch.interrupt.arm.nmi :bgn:`PASSED` (device 2.833s)
         INFO    -  4/16 tiac_magpie               tests/arch/arm/arm_no_multithreading/arch.arm.no_multithreading :bgn:`PASSED` (device 2.916s)
         INFO    -  5/16 tiac_magpie               tests/arch/arm/arm_ramfunc/arch.arm.ramfunc        :bgn:`PASSED` (device 3.969s)
         INFO    -  6/16 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing.no_optimizations :bgn:`PASSED` (device 7.790s)
         INFO    -  7/16 tiac_magpie               tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features.secure_fw :byl:`SKIPPED` (filter)
         INFO    -  8/16 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing :bgn:`PASSED` (device 4.112s)
         INFO    -  9/16 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common.no_optimizations :bgn:`PASSED` (device 7.688s)
         INFO    - 10/16 tiac_magpie               tests/arch/arm/arm_thread_swap/arch.arm.swap.common :bgn:`PASSED` (device 4.096s)
         INFO    - 11/16 tiac_magpie               tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features :bgn:`PASSED` (device 3.033s)
         INFO    - 12/16 tiac_magpie               tests/arch/arm/arm_tz_wrap_func/arch.arm.tz_wrap_func :bgn:`PASSED` (device 2.994s)
         INFO    - 13/16 tiac_magpie               tests/arch/arm/arm_sw_vector_relay/arch.arm.sw_vector_relay :bgn:`PASSED` (device 3.005s)
         INFO    - 14/16 tiac_magpie               tests/arch/arm/arm_interrupt/arch.interrupt.extra_exception_info :bgn:`PASSED` (device 4.211s)
         INFO    - 15/16 tiac_magpie               tests/arch/arm/arm_interrupt/arch.interrupt.no_optimizations :bgn:`PASSED` (device 7.905s)
         INFO    - 16/16 tiac_magpie               tests/arch/arm/arm_interrupt/arch.interrupt.arm    :bgn:`PASSED` (device 4.247s)

         INFO    - :bgn:`14 of 14` test configurations passed (100.00%), :bbk:`0` failed, :byl:`2` skipped with :bbk:`0` warnings in :bbk:`102.43 seconds`
         INFO    - In total 22 test cases were executed, 4 skipped on 1 out of total 330 platforms (0.30%)
         INFO    - :bgn:`14` test configurations executed on platforms, :brd:`0` test configurations were only built.
