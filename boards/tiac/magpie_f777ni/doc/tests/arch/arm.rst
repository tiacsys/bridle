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

         west twister \
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

         \| Platform      \| ID       \| Serial device   \|
         \|---------------\|----------\|-----------------\|
         \| magpie_f777ni \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1866/1887 magpie_f777ni             tests/arch/arm/arm_mem_protect/arch.arm.mem_protect.syscalls :byl:`SKIPPED` (runtime filter)
         INFO    - 1867/1887 magpie_f777ni             tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features.secure_fw :byl:`SKIPPED` (runtime filter)
         INFO    - 1868/1887 magpie_f777ni             tests/arch/arm/arm_irq_vector_table/arch.arm.irq_vector_table :bgn:`PASSED` (device: DT04BNT1, 3.082s)
         INFO    - 1869/1887 magpie_f777ni             tests/arch/arm/arm_runtime_nmi/arch.arm.interrupt.nmi :bgn:`PASSED` (device: DT04BNT1, 4.288s)
         INFO    - 1870/1887 magpie_f777ni             tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features :bgn:`PASSED` (device: DT04BNT1, 2.381s)
         INFO    - 1871/1887 magpie_f777ni             tests/arch/common/ramfunc/arch.common.ramfunc      :bgn:`PASSED` (device: DT04BNT1, 3.080s)
         INFO    - 1872/1887 magpie_f777ni             tests/arch/arm/arm_thread_swap_tz/arch.arm.swap.tz_off :byl:`SKIPPED` (runtime filter)
         INFO    - 1873/1887 magpie_f777ni             tests/arch/arm/arm_tz_wrap_func/arch.arm.tz_wrap_func :bgn:`PASSED` (device: DT04BNT1, 3.427s)
         INFO    - 1874/1887 magpie_f777ni             tests/arch/arm/arm_thread_swap_tz/arch.arm.swap.tz :byl:`SKIPPED` (runtime filter)
         INFO    - 1875/1887 magpie_f777ni             tests/arch/arm/arm_sw_vector_relay/arch.arm.sw_vector_relay :bgn:`PASSED` (device: DT04BNT1, 2.359s)
         INFO    - 1876/1887 magpie_f777ni             tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing.no_optimizations :bgn:`PASSED` (device: DT04BNT1, 5.992s)
         INFO    - 1877/1887 magpie_f777ni             tests/arch/arm/arm_thread_swap/arch.arm.swap.common.no_optimizations :bgn:`PASSED` (device: DT04BNT1, 6.009s)
         INFO    - 1878/1887 magpie_f777ni             tests/arch/arm/arm_irq_zero_latency_levels/arch.arm.irq_zero_latency_levels.secure_fw :byl:`SKIPPED` (runtime filter)
         INFO    - 1879/1887 magpie_f777ni             tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing :bgn:`PASSED` (device: DT04BNT1, 3.693s)
         INFO    - 1880/1887 magpie_f777ni             tests/arch/arm/arm_thread_swap/arch.arm.swap.common :bgn:`PASSED` (device: DT04BNT1, 3.070s)
         INFO    - 1881/1887 magpie_f777ni             tests/arch/arm/arm_irq_zero_latency_levels/arch.arm.irq_zero_latency_levels :bgn:`PASSED` (device: DT04BNT1, 3.552s)
         INFO    - 1882/1887 magpie_f777ni             tests/arch/arm/arm_interrupt/arch.arm.interrupt.no_optimizations :bgn:`PASSED` (device: DT04BNT1, 6.251s)
         INFO    - 1883/1887 magpie_f777ni             tests/arch/arm/arm_interrupt/arch.arm.interrupt.extra_exception_info :bgn:`PASSED` (device: DT04BNT1, 4.103s)
         INFO    - 1884/1887 magpie_f777ni             tests/arch/arm/arm_interrupt/arch.arm.interrupt    :bgn:`PASSED` (device: DT04BNT1, 3.188s)
         INFO    - 1885/1887 magpie_f777ni             tests/arch/arm64/arm64_psci/arch.arm64.psci        :byl:`SKIPPED` (runtime filter)
         INFO    - 1886/1887 magpie_f777ni             tests/arch/arm/arm_custom_interrupt/arch.arm.custom_interrupt :bgn:`PASSED` (device: DT04BNT1, 2.377s)
         INFO    - 1887/1887 magpie_f777ni             tests/arch/arm/arm_hardfault_validation/arch.arm.interrupt.hardfault_validation :bgn:`PASSED` (device: DT04BNT1, 2.345s)

         INFO    - 2092 test scenarios (1887 test instances) selected, 1871 configurations skipped (1865 by static filter, 6 at runtime).
         INFO    - :bgn:`16 of 1887` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1871` skipped with :bbk:`0` warnings in :bbk:`278.97 seconds`
         INFO    - In total 35 test cases were executed, 14967 skipped on 1 out of total 1 platforms (100.00%)
         INFO    - :bgn:`16` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board         \| ID       \|   Counter \|
         \|---------------\|----------\|-----------\|
         \| magpie_f777ni \| DT04BNT1 \|        16 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni...
         INFO    - Run completed
