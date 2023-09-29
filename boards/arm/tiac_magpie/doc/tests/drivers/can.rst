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

         $ west twister \
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

         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1535/1543 tiac_magpie               tests/subsys/canbus/isotp/implementation/canbus.isotp.implementation PASSED (device: DT04BNT1, 17.651s)
         INFO    - 1536/1543 tiac_magpie               tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.txdl_64 PASSED (device: DT04BNT1, 3.085s)
         INFO    - 1537/1543 tiac_magpie               tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.txdl_32 PASSED (device: DT04BNT1, 3.136s)
         INFO    - 1538/1543 tiac_magpie               tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.unused PASSED (device: DT04BNT1, 13.632s)
         INFO    - 1539/1543 tiac_magpie               tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance PASSED (device: DT04BNT1, 13.850s)
         INFO    - 1540/1543 tiac_magpie               tests/drivers/can/shell/drivers.can.shell          PASSED (device: DT04BNT1, 4.353s)
         INFO    - 1541/1543 tiac_magpie               tests/drivers/can/api/drivers.can.api              PASSED (device: DT04BNT1, 5.113s)
         INFO    - 1542/1543 tiac_magpie               tests/net/socket/can/net.socket.can                PASSED (device: DT04BNT1, 2.382s)
         INFO    - 1543/1543 tiac_magpie               tests/drivers/can/timing/drivers.can.timing.tiac_magpie PASSED (device: DT04BNT1, 3.233s)

         INFO    - 1755 test scenarios (1543 test instances) selected, 1534 configurations skipped (1534 by static filter, 0 at runtime).
         INFO    - :bgn:`9 of 1543` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1534` skipped with :bbk:`0` warnings in :bbk:`100.98 seconds`
         INFO    - In total 171 test cases were executed, 10639 skipped on 1 out of total 634 platforms (0.16%)
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
