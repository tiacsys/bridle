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

         $ west twister \
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

         \| Platform                  \| ID       \| Serial device   \|
         \|---------------------------\|----------\|-----------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1/7 magpie_f777ni/stm32f777xx tests/drivers/uart/uart_async_api/drivers.uart.async_api.lpuart.rt_nocache :byl:`FILTERED` (runtime filter)
         INFO    - 2/7 magpie_f777ni/stm32f777xx tests/drivers/uart/uart_async_api/drivers.uart.async_api.lpuart :byl:`FILTERED` (runtime filter)
         INFO    - 3/7 magpie_f777ni/stm32f777xx tests/drivers/uart/uart_async_api/drivers.uart.async_api :byl:`FILTERED` (runtime filter)
         INFO    - 4/7 magpie_f777ni/stm32f777xx tests/subsys/logging/log_backend_uart/logging.backend.uart.single :bgn:`PASSED` (device: DT04BNT1, 2.478s <zephyr>)
         INFO    - 5/7 magpie_f777ni/stm32f777xx tests/drivers/uart/uart_async_rx/drivers.uart.async_rx :bgn:`PASSED` (device: DT04BNT1, 12.547s <zephyr>)
         INFO    - 6/7 magpie_f777ni/stm32f777xx tests/subsys/logging/log_backend_uart/logging.backend.uart.multi :bgn:`PASSED` (device: DT04BNT1, 3.146s <zephyr>)
         INFO    - 7/7 magpie_f777ni/stm32f777xx tests/drivers/console/hello_world/drivers.console.uart :bgn:`PASSED` (device: DT04BNT1, 2.475s <zephyr>)

         INFO    - 2537 test scenarios (2325 configurations) selected, :byl:`2321` configurations filtered (2318 by static filter, 3 at runtime).
         INFO    - :bgn:`4 of 4` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`66.71 seconds`.
         INFO    - 7 of 7 executed test cases passed (100.00%) on 1 out of total 947 platforms (0.11%).
         INFO    - :bgn:`4` test configurations executed on platforms, :bbl:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board                     \| ID       \|   Counter \|   Failures \|
         \|---------------------------\|----------\|-----------\|------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \|         4 \|          0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni/stm32f777xx...
         INFO    - Writing JSON report .../twister-out/magpie_f777ni_stm32f777xx.json
         INFO    - Run completed
