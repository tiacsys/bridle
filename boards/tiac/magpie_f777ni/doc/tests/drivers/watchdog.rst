.. _magpie_f777ni_drivers_watchdog-tests:

Watchdog
########

Overview
********

See :zephyr_file:`tests/drivers/watchdog`
for the original scope of tests, its structure and description.

.. _magpie_f777ni_drivers_watchdog-tests-requirements:

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
                --alt-config-root bridle/zephyr/alt-config/tests \
                --testsuite-root zephyr/tests --tag watchdog

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight-console notranslate

         Device testing on:

         \| Platform                  \| ID       \| Serial device   \|
         \|---------------------------\|----------\|-----------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1/3 magpie_f777ni/stm32f777xx tests/drivers/watchdog/wdt_basic_api/drivers.watchdog :byl:`FILTERED` (runtime filter)
         WARNING - TS_START: already STARTED 'wdt_basic_test_suite':{'count': 1, 'repeat': 0}
         WARNING - TC_START: already STARTED case 'drivers.watchdog.stm32wwdg.timing.adj.wdt_basic_test_suite.wdt':{'count': 1}
         INFO    - 2/3 magpie_f777ni/stm32f777xx tests/drivers/watchdog/wdt_basic_api/drivers.watchdog.stm32wwdg.timing.adj :bgn:`PASSED` (device: DT04BNT1, 2.626s <zephyr>)
         WARNING - TS_START: already STARTED 'wdt_basic_test_suite':{'count': 1, 'repeat': 0}
         WARNING - TC_START: already STARTED case 'drivers.watchdog.stm32iwdg.boot.off.wdt_basic_test_suite.wdt':{'count': 1}
         INFO    - 3/3 magpie_f777ni/stm32f777xx tests/drivers/watchdog/wdt_basic_api/drivers.watchdog.stm32iwdg.boot.off :bgn:`PASSED` (device: DT04BNT1, 4.477s <zephyr>)

         INFO    - 2537 test scenarios (2325 configurations) selected, :byl:`2323` configurations filtered (2322 by static filter, 1 at runtime).
         INFO    - :bgn:`2 of 2` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`40.39 seconds`.
         INFO    - 2 of 2 executed test cases passed (100.00%) on 1 out of total 947 platforms (0.11%).
         INFO    - :bgn:`2` test configurations executed on platforms, :bbl:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board                     \| ID       \|   Counter \|   Failures \|
         \|---------------------------\|----------\|-----------\|------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \|         2 \|          0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni/stm32f777xx...
         INFO    - Writing JSON report .../twister-out/magpie_f777ni_stm32f777xx.json
         INFO    - Run completed
