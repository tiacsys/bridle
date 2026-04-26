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
         INFO    -  1/26 magpie_f777ni/stm32f777xx arch.arm.mem_protect.syscalls                      :byl:`FILTERED` (runtime filter)
         INFO    -  2/26 magpie_f777ni/stm32f777xx arch.arm.irq_advanced_features.secure_fw           :byl:`FILTERED` (runtime filter)
         INFO    -  3/26 magpie_f777ni/stm32f777xx arch.arm.irq_vector_table                          :bgn:`PASSED` (device: DT04BNT1, 3.592s <zephyr/gnu>)
         INFO    -  4/26 magpie_f777ni/stm32f777xx arch.common.ramfunc                                :bgn:`PASSED` (device: DT04BNT1, 4.752s <zephyr/gnu>)
         INFO    -  5/26 magpie_f777ni/stm32f777xx arch.arm.irq_advanced_features                     :bgn:`PASSED` (device: DT04BNT1, 2.668s <zephyr/gnu>)
         INFO    -  6/26 magpie_f777ni/stm32f777xx arch.arm.tz_wrap_func                              :bgn:`PASSED` (device: DT04BNT1, 4.174s <zephyr/gnu>)
         INFO    -  7/26 magpie_f777ni/stm32f777xx arch.arm.user.stack.float                          :bgn:`PASSED` (device: DT04BNT1, 4.412s <zephyr/gnu>)
         INFO    -  8/26 magpie_f777ni/stm32f777xx arch.arm.sw_vector_relay.sram_vector_table         :bgn:`PASSED` (device: DT04BNT1, 2.718s <zephyr/gnu>)
         INFO    -  9/26 magpie_f777ni/stm32f777xx arch.arm.user.stack                                :bgn:`PASSED` (device: DT04BNT1, 4.792s <zephyr/gnu>)
         INFO    - 10/26 magpie_f777ni/stm32f777xx arch.arm.swap.tz_off                               :byl:`FILTERED` (runtime filter)
         INFO    - 11/26 magpie_f777ni/stm32f777xx arch.arm.sw_vector_relay                           :bgn:`PASSED` (device: DT04BNT1, 2.629s <zephyr/gnu>)
         INFO    - 12/26 magpie_f777ni/stm32f777xx arch.arm.swap.tz                                   :byl:`FILTERED` (runtime filter)
         INFO    - 13/26 magpie_f777ni/stm32f777xx arch.arm.swap.common.fpu_sharing.no_optimizations  :bgn:`PASSED` (device: DT04BNT1, 7.546s <zephyr/gnu>)
         INFO    - 14/26 magpie_f777ni/stm32f777xx arch.arm.swap.common.fpu_sharing                   :bgn:`PASSED` (device: DT04BNT1, 3.931s <zephyr/gnu>)
         INFO    - 15/26 magpie_f777ni/stm32f777xx arch.arm.irq_zero_latency_levels.secure_fw         :byl:`FILTERED` (runtime filter)
         INFO    - 16/26 magpie_f777ni/stm32f777xx arch.arm.swap.common                               :bgn:`PASSED` (device: DT04BNT1, 3.226s <zephyr/gnu>)
         INFO    - 17/26 magpie_f777ni/stm32f777xx arch.arm.interrupt.extra_exception_info            :byl:`FILTERED` (runtime filter)
         INFO    - 18/26 magpie_f777ni/stm32f777xx arch.arm.mpu.write_through                         :byl:`FILTERED` (runtime filter)
         INFO    - 19/26 magpie_f777ni/stm32f777xx arch.arm.irq_zero_latency_levels                   :bgn:`PASSED` (device: DT04BNT1, 5.014s <zephyr/gnu>)
         INFO    - 20/26 magpie_f777ni/stm32f777xx arch.arm.interrupt.no_optimizations                :bgn:`PASSED` (device: DT04BNT1, 6.435s <zephyr/gnu>)
         INFO    - 21/26 magpie_f777ni/stm32f777xx arch.arm.interrupt                                 :bgn:`PASSED` (device: DT04BNT1, 4.913s <zephyr/gnu>)
         INFO    - 22/26 magpie_f777ni/stm32f777xx arch.arm.interrupt.nmi                             :bgn:`PASSED` (device: DT04BNT1, 5.695s <zephyr/gnu>)
         INFO    - 23/26 magpie_f777ni/stm32f777xx arch.arm64.psci                                    :byl:`FILTERED` (runtime filter)
         INFO    - 24/26 magpie_f777ni/stm32f777xx arch.arm.swap.common.no_optimizations              :bgn:`PASSED` (device: DT04BNT1, 7.434s <zephyr/gnu>)
         INFO    - 25/26 magpie_f777ni/stm32f777xx arch.arm.custom_interrupt                          :bgn:`PASSED` (device: DT04BNT1, 3.661s <zephyr/gnu>)
         INFO    - 26/26 magpie_f777ni/stm32f777xx arch.arm.interrupt.hardfault_validation            :bgn:`PASSED` (device: DT04BNT1, 2.531s <zephyr/gnu>)

         INFO    - 2090 test scenarios (2888 configurations) selected, :byl:`2870` configurations filtered (:byl:`2862` by static filter, :byl:`8` at runtime).
         INFO    - :bgn:`18 of 18` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`461.09 seconds`.
         INFO    - 32 of 32 executed test cases passed (100.00%) on 1 out of total 1511 platforms (0.07%).
         INFO    - 2 selected test cases not executed: 2 skipped.
         INFO    - :bgn:`18` test configurations executed on platforms, :bbl:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board                     \| ID       \|   Counter \|   Failures \|
         \|---------------------------\|----------\|-----------\|------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \|        18 \|          0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni/stm32f777xx...
         INFO    - Writing JSON report .../twister-out/magpie_f777ni_stm32f777xx.json
         INFO    - Run completed
