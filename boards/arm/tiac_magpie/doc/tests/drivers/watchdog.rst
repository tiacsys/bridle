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
             --board-root bridle/boards \
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

         INFO    - 8 test scenarios (8 configurations) selected, 5 configurations discarded due to filters.
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 6/8 tiac_magpie               tests/drivers/watchdog/wdt_basic_api/drivers.watchdog :byl:`SKIPPED` (runtime filter)
         INFO    - 7/8 tiac_magpie               wdt_basic_api/drivers.watchdog.stm32iwdg.tiac_magpie :bgn:`PASSED` (device 5.986s)
         INFO    - 8/8 tiac_magpie               wdt_basic_api/drivers.watchdog.stm32wwdg.tiac_magpie :bgn:`PASSED` (device 3.830s)

         INFO    - :bgn:`2 of 8` test configurations passed (100.00%), :bbk:`0` failed, :byl:`6` skipped with :bbk:`0` warnings in :bbk:`29.34 seconds`
         INFO    - In total 7 test cases were executed, 1 skipped on 1 out of total 457 platforms (0.22%)
         INFO    - :bgn:`2` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         2 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Using 'zephyr' toolchain.
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
