.. _tiac_magpie_drivers_watchdog-tests:

Watchdog
########

Overview
********

See :zephyr_file:`tests/drivers/watchdog`
for the original scope of tests, its structure and description.

.. _tiac_magpie_drivers_watchdog-tests-requirements:

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
             --testsuite-root zephyr/tests/drivers/watchdog \
             --testsuite-root bridle/tests/drivers/watchdog

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
         INFO    - 12/14 tiac_magpie               tests/drivers/watchdog/wdt_basic_api/drivers.watchdog :byl:`SKIPPED` (runtime filter)
         INFO    - 13/14 tiac_magpie               wdt_basic_api/drivers.watchdog.stm32iwdg.tiac_magpie :bgn:`PASSED` (device 4.404s)
         INFO    - 14/14 tiac_magpie               wdt_basic_api/drivers.watchdog.stm32wwdg.tiac_magpie :bgn:`PASSED` (device 2.414s)

         INFO    - 14 test scenarios (14 test instances) selected, 12 configurations skipped ((0 by static filter, 1 at runtime).
         INFO    - :bgn:`2 of 14` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`12` skipped with :bbk:`0` warnings in :bbk:`31.40 seconds`
         INFO    - In total 2 test cases were executed, 13 skipped on 1 out of total 580 platforms (0.17%)
         INFO    - :bgn:`2` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         2 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
