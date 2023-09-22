.. _tiac_magpie_bridle-tests:

Bridle for Zephyr
#################

Overview
********

See :bridle_file:`tests/bridle`
for the original scope of tests, its structure and description.

.. _tiac_magpie_bridle-tests-requirements:

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
             --testsuite-root bridle/tests/bridle

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
         INFO    - 1/1 tiac_magpie               common/bridle.common                               :bgn:`PASSED` (device 3.444s)

         INFO    - 1 test scenarios (1 test instances) selected, 0 configurations skipped (0 by static filter, 0 at runtime).
         INFO    - :bgn:`1 of 1` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`0` skipped with :bbk:`0` warnings in :bbk:`33.16 seconds`
         INFO    - In total 1 test cases were executed, 0 skipped on 1 out of total 580 platforms (0.17%)
         INFO    - :bgn:`1` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         1 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
