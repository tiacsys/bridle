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

         INFO    - 9 test scenarios (9 configurations) selected, 6 configurations discarded due to filters.
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 7/9 tiac_magpie               tests/drivers/watchdog/wdt_basic_api/drivers.watchdog :byl:`SKIPPED` (runtime filter)
         INFO    - 8/9 tiac_magpie               wdt_basic_api/drivers.watchdog.stm32wwdg.tiac_magpie :bgn:`PASSED` (device 3.251s)
         INFO    - 9/9 tiac_magpie               wdt_basic_api/drivers.watchdog.stm32iwdg.tiac_magpie :bgn:`PASSED` (device 5.607s)

         INFO    - :bgn:`2 of 9` test configurations passed (100.00%), :bbk:`0` failed, :byl:`7` skipped with :bbk:`0` warnings in :bbk:`31.04 seconds`
         INFO    - In total 8 test cases were executed, 1 skipped on 1 out of total 501 platforms (0.20%)
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
