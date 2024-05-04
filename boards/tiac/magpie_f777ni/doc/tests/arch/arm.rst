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
              --alt-config-root bridle/zephyr/alt-config \
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
         INFO    - 1759/1780 magpie_f777ni             tests/arch/arm/arm_mem_protect/arch.arm.mem_protect.syscalls :byl:`SKIPPED` (runtime filter)
         INFO    - 1760/1780 magpie_f777ni             tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features.secure_fw :byl:`SKIPPED` (runtime filter)
         INFO    - 1761/1780 magpie_f777ni             tests/arch/arm/arm_irq_vector_table/arch.arm.irq_vector_table :bgn:`PASSED` (device: DT04BNT1, 3.218s)
         INFO    - 1762/1780 magpie_f777ni             tests/arch/arm/arm_runtime_nmi/arch.arm.interrupt.nmi :bgn:`PASSED` (device: DT04BNT1, 4.457s)
         INFO    - 1763/1780 magpie_f777ni             tests/arch/common/ramfunc/arch.common.ramfunc      :bgn:`PASSED` (device: DT04BNT1, 3.241s)
         INFO    - 1764/1780 magpie_f777ni             tests/arch/arm/arm_irq_advanced_features/arch.arm.irq_advanced_features :bgn:`PASSED` (device: DT04BNT1, 2.695s)
         INFO    - 1765/1780 magpie_f777ni             tests/arch/arm/arm_thread_swap_tz/arch.arm.swap.tz_off :byl:`SKIPPED` (runtime filter)
         INFO    - 1766/1780 magpie_f777ni             tests/arch/arm/arm_tz_wrap_func/arch.arm.tz_wrap_func :bgn:`PASSED` (device: DT04BNT1, 3.975s)
         INFO    - 1767/1780 magpie_f777ni             tests/arch/arm/arm_thread_swap_tz/arch.arm.swap.tz :byl:`SKIPPED` (runtime filter)
         INFO    - 1768/1780 magpie_f777ni             tests/arch/arm/arm_sw_vector_relay/arch.arm.sw_vector_relay :bgn:`PASSED` (device: DT04BNT1, 2.563s)
         INFO    - 1769/1780 magpie_f777ni             tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing.no_optimizations :bgn:`PASSED` (device: DT04BNT1, 6.198s)
         INFO    - 1770/1780 magpie_f777ni             tests/arch/arm/arm_thread_swap/arch.arm.swap.common.no_optimizations :bgn:`PASSED` (device: DT04BNT1, 6.246s)
         INFO    - 1771/1780 magpie_f777ni             tests/arch/arm/arm_irq_zero_latency_levels/arch.arm.irq_zero_latency_levels.secure_fw :byl:`SKIPPED` (runtime filter)
         INFO    - 1772/1780 magpie_f777ni             tests/arch/arm/arm_thread_swap/arch.arm.swap.common.fpu_sharing :bgn:`PASSED` (device: DT04BNT1, 3.848s)
         INFO    - 1773/1780 magpie_f777ni             tests/arch/arm/arm_thread_swap/arch.arm.swap.common :bgn:`PASSED` (device: DT04BNT1, 3.206s)
         INFO    - 1774/1780 magpie_f777ni             tests/arch/arm/arm_irq_zero_latency_levels/arch.arm.irq_zero_latency_levels :bgn:`PASSED` (device: DT04BNT1, 3.936s)
         INFO    - 1775/1780 magpie_f777ni             tests/arch/arm/arm_interrupt/arch.arm.interrupt.no_optimizations :bgn:`PASSED` (device: DT04BNT1, 6.317s)
         INFO    - 1776/1780 magpie_f777ni             tests/arch/arm/arm_interrupt/arch.arm.interrupt.extra_exception_info :bgn:`PASSED` (device: DT04BNT1, 4.695s)
         INFO    - 1777/1780 magpie_f777ni             tests/arch/arm/arm_interrupt/arch.arm.interrupt    :bgn:`PASSED` (device: DT04BNT1, 3.544s)
         INFO    - 1778/1780 magpie_f777ni             tests/arch/arm64/arm64_psci/arch.arm64.psci        :byl:`SKIPPED` (runtime filter)
         INFO    - 1779/1780 magpie_f777ni             tests/arch/arm/arm_custom_interrupt/arch.arm.custom_interrupt :bgn:`PASSED` (device: DT04BNT1, 2.531s)
         INFO    - 1780/1780 magpie_f777ni             tests/arch/arm/arm_hardfault_validation/arch.arm.interrupt.hardfault_validation :bgn:`PASSED` (device: DT04BNT1, 2.526s)

         INFO    - 1984 test scenarios (1780 test instances) selected, 1764 configurations skipped (1758 by static filter, 6 at runtime).
         INFO    - :bgn:`16 of 1780` test configurations passed (100.00%), :bbk:`0 failed, :bbk:`0` errored, :byl:`1764` skipped with :bbk:`0` warnings in :bbk:`316.02 seconds`
         INFO    - In total 35 test cases were executed, 13413 skipped on 1 out of total 739 platforms (0.14%)
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
