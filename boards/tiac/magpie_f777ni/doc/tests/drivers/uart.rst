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
         INFO    - 1775/1780 magpie_f777ni             tests/drivers/uart/uart_async_api/drivers.uart.async_api.lpuart :byl:`SKIPPED` (runtime filter)
         INFO    - 1776/1780 magpie_f777ni             tests/drivers/uart/uart_async_api/drivers.uart.async_api :byl:`SKIPPED` (runtime filter)
         INFO    - 1777/1780 magpie_f777ni             tests/subsys/logging/log_backend_uart/logging.backend.uart.multi :bgn:`PASSED` (device: DT04BNT1, 2.620s)
         INFO    - 1778/1780 magpie_f777ni             tests/drivers/uart/uart_async_rx/drivers.uart.async_rx :bgn:`PASSED` (device: DT04BNT1, 12.561s)
         INFO    - 1779/1780 magpie_f777ni             tests/subsys/logging/log_backend_uart/logging.backend.uart.single :bgn:`PASSED` (device: DT04BNT1, 3.426s)
         INFO    - 1780/1780 magpie_f777ni             tests/drivers/console/hello_world/drivers.console.uart :bgn:`PASSED` (device: DT04BNT1, 2.513s)

         INFO    - 1984 test scenarios (1780 test instances) selected, 1776 configurations skipped (1774 by static filter, 2 at runtime).
         INFO    - :bgn:`4 of 1780` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1776` skipped with :bbk:`0` warnings in :bbk:`86.23 seconds`
         INFO    - In total 7 test cases were executed, 13441 skipped on 1 out of total 739 platforms (0.14%)
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
