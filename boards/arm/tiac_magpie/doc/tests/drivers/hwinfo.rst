.. _tiac_magpie_drivers_hwinfo-tests:

Hardware Info-API
#################

Overview
********

See :zephyr_file:`tests/drivers/hwinfo`
for the original scope of tests, its structure and description.

.. _tiac_magpie_drivers_hwinfo-tests-requirements:

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
             --board-root bridle/boards \
             --testsuite-root zephyr/tests/drivers/hwinfo

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - 1 test scenarios (1 configurations) selected, 0 configurations discarded due to filters.
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1/1 tiac_magpie               tests/drivers/hwinfo/api/drivers.hwinfo.api        :bgn:`PASSED` (device 3.807s)

         INFO    - :bgn:`1 of 1` test configurations passed (100.00%), :bbk:`0` failed, :byl:`0` skipped with :bbk:`0` warnings in :bbk:`20.97 seconds`
         INFO    - In total 4 test cases were executed, 0 skipped on 1 out of total 457 platforms (0.22%)
         INFO    - :bgn:`1` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         1 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Using 'zephyr' toolchain.
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
