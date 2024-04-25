.. _tiac_magpie_drivers_can-tests:

CAN Loopback (internal)
#######################

Overview
********

See :zephyr_file:`tests/drivers/can`
for the original scope of tests, its structure and description.

.. _tiac_magpie_drivers_can-tests-requirements:

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
              --testsuite-root zephyr/tests --tag can

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
         INFO    - 1699/1709 tiac_magpie               tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.txdl_32 :bgn:`PASSED` (device: DT04BNT1, 3.382s)
         INFO    - 1700/1709 tiac_magpie               tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.txdl_64 :bgn:`PASSED` (device: DT04BNT1, 3.290s)
         INFO    - 1701/1709 tiac_magpie               tests/drivers/can/api/drivers.can.api.nxp_s32_canxl.non_rx_fifo :byl:`SKIPPED` (runtime filter)
         INFO    - 1702/1709 tiac_magpie               tests/subsys/canbus/isotp/implementation/canbus.isotp.implementation :bgn:`PASSED` (device: DT04BNT1, 18.374s)
         INFO    - 1703/1709 tiac_magpie               tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.unused :bgn:`PASSED` (device: DT04BNT1, 13.786s)
         INFO    - 1704/1709 tiac_magpie               tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance :bgn:`PASSED` (device: DT04BNT1, 15.124s)
         INFO    - 1705/1709 tiac_magpie               tests/drivers/can/shell/drivers.can.shell          :bgn:`PASSED` (device: DT04BNT1, 4.554s)
         INFO    - 1706/1709 tiac_magpie               tests/drivers/can/api/drivers.can.api.rtr          :bgn:`PASSED` (device: DT04BNT1, 6.303s)
         INFO    - 1707/1709 tiac_magpie               tests/drivers/can/api/drivers.can.api              :bgn:`PASSED` (device: DT04BNT1, 5.910s)
         INFO    - 1708/1709 tiac_magpie               tests/net/socket/can/net.socket.can                :bgn:`PASSED` (device: DT04BNT1, 2.479s)
         INFO    - 1709/1709 tiac_magpie               tests/drivers/can/timing/drivers.can.timing        :bgn:`PASSED` (device: DT04BNT1, 3.320s)

         INFO    - 1922 test scenarios (1709 test instances) selected, 1699 configurations skipped (1698 by static filter, 1 at runtime).
         INFO    - :bgn:`10 of 1709` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1699` skipped with 0 warnings in :bbk:`177.67 seconds`
         INFO    - In total 169 test cases were executed, 12515 skipped on 1 out of total 699 platforms (0.14%)
         INFO    - :bgn:`10` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|        10 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
