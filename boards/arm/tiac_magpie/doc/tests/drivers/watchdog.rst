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
             --testcase-root zephyr/tests/drivers/watchdog

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
         INFO    - 1/2 tiac_magpie               tests/drivers/watchdog/wdt_basic_api/drivers.watchdog.stm32wwdg :byl:`SKIPPED` (filter)
         INFO    - 2/2 tiac_magpie               tests/drivers/watchdog/wdt_basic_api/drivers.watchdog :bgn:`PASSED` (device 5.192s)

         INFO    - :bgn:`1 of 1` test configurations passed (100.00%), :bbk:`0` failed, :byl:`2` skipped with :bbk:`0` warnings in :bbk:`33.01 seconds`
         INFO    - In total 1 test cases were executed, 2 skipped on 1 out of total 330 platforms (0.30%)
         INFO    - :bgn:`1` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         1 \|
