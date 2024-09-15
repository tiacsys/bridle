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

         west twister \
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

         \| Platform      \| ID       \| Serial device   \|
         \|---------------\|----------\|-----------------\|
         \| magpie_f777ni \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1876/1887 magpie_f777ni             tests/subsys/canbus/isotp/implementation/canbus.isotp.implementation :bgn:`PASSED` (device: DT04BNT1, 18.198s)
         INFO    - 1877/1887 magpie_f777ni             tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.txdl_64 :bgn:`PASSED` (device: DT04BNT1, 3.060s)
         INFO    - 1878/1887 magpie_f777ni             tests/drivers/can/api/drivers.can.api.nxp_s32_canxl.non_rx_fifo :byl:`SKIPPED` (runtime filter)
         INFO    - 1879/1887 magpie_f777ni             tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.unused :bgn:`PASSED` (device: DT04BNT1, 13.579s)
         INFO    - 1880/1887 magpie_f777ni             tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.txdl_32 :bgn:`PASSED` (device: DT04BNT1, 4.290s)
         INFO    - 1881/1887 magpie_f777ni             tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance :bgn:`PASSED` (device: DT04BNT1, 13.604s)
         INFO    - 1882/1887 magpie_f777ni             tests/drivers/can/shell/drivers.can.shell          :bgn:`PASSED` (device: DT04BNT1, 5.496s)
         INFO    - 1883/1887 magpie_f777ni             tests/drivers/can/api/drivers.can.api.rtr          :bgn:`PASSED` (device: DT04BNT1, 5.983s)
         INFO    - 1884/1887 magpie_f777ni             tests/drivers/can/api/drivers.can.api              :bgn:`PASSED` (device: DT04BNT1, 6.481s)
         INFO    - 1885/1887 magpie_f777ni             tests/drivers/can/timing/drivers.can.timing.adj    :bgn:`PASSED` (device: DT04BNT1, 3.592s)
         INFO    - 1886/1887 magpie_f777ni             tests/net/socket/can/net.socket.can                :bgn:`PASSED` (device: DT04BNT1, 2.311s)
         INFO    - 1887/1887 magpie_f777ni             tests/drivers/can/timing/drivers.can.timing        :bgn:`PASSED` (device: DT04BNT1, 3.085s)

         INFO    - 2092 test scenarios (1887 test instances) selected, 1876 configurations skipped (1875 by static filter, 1 at runtime).
         INFO    - :bgn:`11 of 1887` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1876` skipped with 0 warnings in :bbk:`214.91 seconds`
         INFO    - In total 190 test cases were executed, 14816 skipped on 1 out of total 1 platforms (100.00%)
         INFO    - :bgn:`11` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board         \| ID       \|   Counter \|
         \|---------------\|----------\|-----------\|
         \| magpie_f777ni \| DT04BNT1 \|        11 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni...
         INFO    - Run completed
