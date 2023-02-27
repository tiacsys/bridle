.. _tiac_magpie_drivers_counter-tests:

Counter (Real-Time Clock)
#########################

Overview
********

See :zephyr_file:`tests/drivers/counter`
for the original scope of tests, its structure and description.

.. _tiac_magpie_drivers_counter-tests-requirements:

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
             --testsuite-root zephyr/tests/drivers/counter

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - 6 test scenarios (6 configurations) selected, 5 configurations discarded due to filters.
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 6/6 tiac_magpie               tests/drivers/counter/counter_basic_api/drivers.counter.basic_api :bgn:`PASSED` (device 326.290s)

         INFO    - :bgn:`1 of 6` test configurations passed (100.00%), :bbk:`0` failed, :byl:`5` skipped with :bbk:`0` warnings in :bbk:`353.38 seconds`
         INFO    - In total 33 test cases were executed, 0 skipped on 1 out of total 501 platforms (0.20%)
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
