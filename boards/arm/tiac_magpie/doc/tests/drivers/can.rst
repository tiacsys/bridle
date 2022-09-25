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

         $ ./zephyr/scripts/twister \
             --verbose --jobs 4 --inline-logs \
             --enable-size-report --platform-reports \
             --device-testing --hardware-map map.yaml \
             --extra-args SHIELD=can_timing_adj \
             --board-root bridle/boards \
             --testsuite-root zephyr/tests/drivers/can

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - 6 test scenarios (6 configurations) selected, 2 configurations discarded due to filters.
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 3/6 tiac_magpie               tests/drivers/can/utilities/drivers.can.utilities  :bgn:`PASSED` (device 3.690s)
         INFO    - 4/6 tiac_magpie               tests/drivers/can/stm32/drivers.can.stm32          :bgn:`PASSED` (device 3.999s)
         INFO    - 5/6 tiac_magpie               tests/drivers/can/timing/drivers.can.timing        :bgn:`PASSED` (device 5.437s)
         INFO    - 6/6 tiac_magpie               tests/drivers/can/api/drivers.can.api              :bgn:`PASSED` (device 6.299s)

         INFO    - :bgn:`4 of 6` test configurations passed (100.00%), :bbk:`0` failed, :byl:`2` skipped with :bbk:`0` warnings in :bbk:`51.79 seconds`
         INFO    - In total 60 test cases were executed, 3 skipped on 1 out of total 457 platforms (0.22%)
         INFO    - :bgn:`4` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         4 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Using 'zephyr' toolchain.
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
