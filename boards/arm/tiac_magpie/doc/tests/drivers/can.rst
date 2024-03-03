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
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1562/1570 tiac_magpie               tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.txdl_32 :bgn:`PASSED` (device: DT04BNT1, 3.284s)
         INFO    - 1563/1570 tiac_magpie               tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.unused :bgn:`PASSED` (device: DT04BNT1, 13.639s)
         INFO    - 1564/1570 tiac_magpie               tests/subsys/canbus/isotp/implementation/canbus.isotp.implementation :bgn:`PASSED` (device: DT04BNT1, 19.361s)
         INFO    - 1565/1570 tiac_magpie               tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance :bgn:`PASSED` (device: DT04BNT1, 14.912s)
         INFO    - 1566/1570 tiac_magpie               tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.txdl_64 :bgn:`PASSED` (device: DT04BNT1, 4.323s)
         INFO    - 1567/1570 tiac_magpie               tests/drivers/can/shell/drivers.can.shell          :bgn:`PASSED` (device: DT04BNT1, 4.471s)
         INFO    - 1568/1570 tiac_magpie               tests/drivers/can/api/drivers.can.api              :bgn:`PASSED` (device: DT04BNT1, 6.311s)
         INFO    - 1569/1570 tiac_magpie               tests/net/socket/can/net.socket.can                :bgn:`PASSED` (device: DT04BNT1, 3.240s)
         INFO    - 1570/1570 tiac_magpie               tests/drivers/can/timing/drivers.can.timing        :bgn:`PASSED` (device: DT04BNT1, 3.285s)

         INFO    - 1782 test scenarios (1570 test instances) selected, 1561 configurations skipped (1561 by static filter, 0 at runtime).
         INFO    - :bgn:`9 of 1570` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1561` skipped with 0 warnings in :bbk:`158.46 seconds`
         INFO    - In total 171 test cases were executed, 10827 skipped on 1 out of total 640 platforms (0.16%)
         INFO    - :bgn:`9` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         9 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
