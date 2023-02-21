.. _tiac_magpie_drivers_uart-tests:

UART Loopback :byl:`(not yet)`
##############################

Overview
********

See :zephyr_file:`tests/drivers/uart`
for the original scope of tests, its structure and description.

.. _tiac_magpie_drivers_uart-tests-requirements:

Requirements
************

You will need an ST-LINK/V2 debug tool adapter already connected to the
TiaC Magpie board, which has an already configured UART console connection.

On the TiaC MAGPIE pin headers the following UART pins must be connected.

.. image:: loopback_test_UART.svg
   :alt: TiaC MAGPIE Pin Header UART Loopback Wiring
   :align: center

Building and Running
********************

.. tabs::

   .. group-tab:: Running ... t.b.d.

      Build and run the tests on target as follows:

      .. code-block:: console

         $ ./zephyr/scripts/twister \
             --verbose --jobs 1 --inline-logs \
             --enable-size-report --platform-reports \
             --device-testing --hardware-map map.yaml \
             --extra-args SHIELD=loopback_test_tmph \
             --board-root bridle/boards \
             --testsuite-root zephyr/tests/drivers/uart

   .. group-tab:: Results ... t.b.d.

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - 24 test scenarios (24 configurations) selected, 22 configurations discarded due to filters.
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 23/24 tiac_magpie               tests/drivers/uart/uart_async_api/drivers.uart.async_api :byl:`SKIPPED` (runtime filter)
         INFO    - 24/24 tiac_magpie               tests/drivers/uart/uart_async_api/drivers.uart.async_api.lpuart :byl:`SKIPPED` (runtime filter)

         INFO    - :bgn:`0 of 24` test configurations passed (0.00%), :bbk:`0` failed, :byl:`24` skipped with :bbk:`0` warnings in :bbk:`7.78 seconds`
         INFO    - In total 94 test cases were executed, 36 skipped on 1 out of total 457 platforms (0.22%)
         INFO    - :bgn:`0` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Using 'zephyr' toolchain.
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
