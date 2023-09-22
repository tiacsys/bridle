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
             --extra-args SHIELD=can_timing_adj \
             --testsuite-root zephyr/tests/drivers/can

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
         INFO    - 2/4 tiac_magpie               tests/drivers/can/shell/drivers.can.shell          :bgn:`PASSED` (device 5.781s)
         INFO    - 3/4 tiac_magpie               tests/drivers/can/timing/drivers.can.timing        :bgn:`PASSED` (device 3.224s)
         INFO    - 4/4 tiac_magpie               tests/drivers/can/api/drivers.can.api              :bgn:`PASSED` (device 5.158s)

         INFO    - 4 test scenarios (4 test instances) selected, 1 configurations skipped (1 by static filter, 0 at runtime).
         INFO    - :bgn:`3 of 4` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1` skipped with :bbk:`0` warnings in :bbk:`43.26 seconds`
         INFO    - In total 86 test cases were executed, 46 skipped on 1 out of total 580 platforms (0.17%)
         INFO    - :bgn:`3` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         3 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
