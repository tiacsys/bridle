.. _magpie_f777ni_drivers_can-tests:

CAN Loopback (internal)
#######################

Overview
********

See :zephyr_file:`tests/drivers/can`
for the original scope of tests, its structure and description.

.. _magpie_f777ni_drivers_can-tests-requirements:

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
                --testsuite-root zephyr/tests --tag can

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
         INFO    -  1/12 magpie_f777ni/stm32f777xx tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.unused :bgn:`PASSED` (device: DT04BNT1, 13.627s <zephyr>)
         INFO    -  2/12 magpie_f777ni/stm32f777xx tests/subsys/canbus/isotp/implementation/canbus.isotp.implementation :bgn:`PASSED` (device: DT04BNT1, 18.297s <zephyr>)
         INFO    -  3/12 magpie_f777ni/stm32f777xx tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.txdl_64 :bgn:`PASSED` (device: DT04BNT1, 3.202s <zephyr>)
         INFO    -  4/12 magpie_f777ni/stm32f777xx tests/drivers/can/api/drivers.can.api.nxp_s32_canxl.non_rx_fifo :byl:`FILTERED` (runtime filter)
         INFO    -  5/12 magpie_f777ni/stm32f777xx tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.txdl_32 :bgn:`PASSED` (device: DT04BNT1, 3.134s <zephyr>)
         INFO    -  6/12 magpie_f777ni/stm32f777xx tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance :bgn:`PASSED` (device: DT04BNT1, 13.637s <zephyr>)
         INFO    -  7/12 magpie_f777ni/stm32f777xx tests/drivers/can/shell/drivers.can.shell          :bgn:`PASSED` (device: DT04BNT1, 4.573s <zephyr>)
         INFO    -  8/12 magpie_f777ni/stm32f777xx tests/drivers/can/api/drivers.can.api.rtr          :bgn:`PASSED` (device: DT04BNT1, 6.211s <zephyr>)
         INFO    -  9/12 magpie_f777ni/stm32f777xx tests/drivers/can/api/drivers.can.api              :bgn:`PASSED` (device: DT04BNT1, 6.254s <zephyr>)
         INFO    - 10/12 magpie_f777ni/stm32f777xx tests/drivers/can/timing/drivers.can.timing.adj    :bgn:`PASSED` (device: DT04BNT1, 3.331s <zephyr>)
         INFO    - 11/12 magpie_f777ni/stm32f777xx tests/net/socket/can/net.socket.can                :bgn:`PASSED` (device: DT04BNT1, 2.368s <zephyr>)
         INFO    - 12/12 magpie_f777ni/stm32f777xx tests/drivers/can/timing/drivers.can.timing        :bgn:`PASSED` (device: DT04BNT1, 3.137s <zephyr>)

         INFO    - 2537 test scenarios (2325 configurations) selected, :byl:`2314` configurations filtered (2313 by static filter, 1 at runtime).
         INFO    - :bgn:`11 of 11` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`164.91 seconds`.
         INFO    - 196 of 262 executed test cases passed (74.81%), 66 blocked on 1 out of total 947 platforms (0.11%).
         INFO    - 12 selected test cases not executed: 12 skipped.
         INFO    - :bgn:`11` test configurations executed on platforms, :bbl:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board                     \| ID       \|   Counter \|   Failures \|
         \|---------------------------\|----------\|-----------\|------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \|        11 \|          0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni/stm32f777xx...
         INFO    - Writing JSON report .../twister-out/magpie_f777ni_stm32f777xx.json
         INFO    - Run completed
