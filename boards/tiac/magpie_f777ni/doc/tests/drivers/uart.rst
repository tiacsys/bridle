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

         west twister \
              --verbose --jobs 4 --inline-logs \
              --enable-size-report --platform-reports \
              --device-testing --hardware-map map.yaml \
              --extra-args SHIELD="loopback_test_tmph" \
              --alt-config-root bridle/zephyr/alt-config \
              --testsuite-root zephyr/tests --tag uart

   .. group-tab:: Results ... t.b.d.

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight-console notranslate

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1704/1709 tiac_magpie               tests/drivers/uart/uart_async_api/drivers.uart.async_api.lpuart :byl:`SKIPPED` (runtime filter)
         INFO    - 1705/1709 tiac_magpie               tests/drivers/uart/uart_async_api/drivers.uart.async_api :byl:`SKIPPED` (runtime filter)
         INFO    - 1706/1709 tiac_magpie               tests/subsys/logging/log_backend_uart/logging.backend.uart.multi :bgn:`PASSED` (device: DT04BNT1, 2.476s)
         INFO    - 1707/1709 tiac_magpie               tests/subsys/logging/log_backend_uart/logging.backend.uart.single :bgn:`PASSED` (device: DT04BNT1, 2.579s)
         INFO    - 1708/1709 tiac_magpie               tests/drivers/uart/uart_async_rx/drivers.uart.async_rx :bgn:`PASSED` (device: DT04BNT1, 13.207s)
         INFO    - 1709/1709 tiac_magpie               tests/drivers/console/hello_world/drivers.console.uart :bgn:`PASSED` (device: DT04BNT1, 2.539s)

         INFO    - 1922 test scenarios (1709 test instances) selected, 1705 configurations skipped (1703 by static filter, 2 at runtime).
         INFO    - :bgn:`4 of 1709` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1705` skipped with :bbk:`0` warnings in :bbk:`69.39 seconds`
         INFO    - In total 7 test cases were executed, 12677 skipped on 1 out of total 699 platforms (0.14%)
         INFO    - :bgn:`4` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         4 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
