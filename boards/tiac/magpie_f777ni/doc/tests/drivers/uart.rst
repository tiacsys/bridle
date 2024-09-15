.. _magpie_f777ni_drivers_uart-tests:

UART Loopback :byl:`(not yet)`
##############################

Overview
********

See :zephyr_file:`tests/drivers/uart`
for the original scope of tests, its structure and description.

.. _magpie_f777ni_drivers_uart-tests-requirements:

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

   .. group-tab:: Running

      Build and run the tests on target as follows:

      .. code-block:: console

         west twister \
              --verbose --jobs 4 --inline-logs \
              --enable-size-report --platform-reports \
              --device-testing --hardware-map map.yaml \
              --extra-args SHIELD="loopback_test_tmph" \
              --alt-config-root bridle/zephyr/alt-config/tests \
              --testsuite-root zephyr/tests --tag uart

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight-console notranslate

         Device testing on:

         \| Platform      \| ID       \| Serial device   \|
         \|---------------\|----------\|-----------------\|
         \| magpie_f777ni \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1882/1887 magpie_f777ni             tests/drivers/uart/uart_async_api/drivers.uart.async_api.lpuart :byl:`SKIPPED` (runtime filter)
         INFO    - 1883/1887 magpie_f777ni             tests/drivers/uart/uart_async_api/drivers.uart.async_api :byl:`SKIPPED` (runtime filter)
         INFO    - 1884/1887 magpie_f777ni             tests/subsys/logging/log_backend_uart/logging.backend.uart.single :bgn:`PASSED` (device: DT04BNT1, 2.378s)
         INFO    - 1885/1887 magpie_f777ni             tests/drivers/uart/uart_async_rx/drivers.uart.async_rx :bgn:`PASSED` (device: DT04BNT1, 12.408s)
         INFO    - 1886/1887 magpie_f777ni             tests/subsys/logging/log_backend_uart/logging.backend.uart.multi :bgn:`PASSED` (device: DT04BNT1, 2.419s)
         INFO    - 1887/1887 magpie_f777ni             tests/drivers/console/hello_world/drivers.console.uart :bgn:`PASSED` (device: DT04BNT1, 2.410s)

         INFO    - 2092 test scenarios (1887 test instances) selected, 1883 configurations skipped (1881 by static filter, 2 at runtime).
         INFO    - :bgn:`4 of 1887` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1883` skipped with :bbk:`0` warnings in :bbk:`72.33 seconds`
         INFO    - In total 7 test cases were executed, 14995 skipped on 1 out of total 1 platforms (100.00%)
         INFO    - :bgn:`4` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board         \| ID       \|   Counter \|
         \|---------------\|----------\|-----------\|
         \| magpie_f777ni \| DT04BNT1 \|         4 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni...
         INFO    - Run completed
