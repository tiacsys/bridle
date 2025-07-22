.. _magpie_f777ni_drivers_spi-tests:

SPI Loopback
############

Overview
********

See :zephyr_file:`tests/drivers/spi`
for the original scope of tests, its structure and description.

.. _magpie_f777ni_drivers_spi-tests-requirements:

Requirements
************

You will need an ST-LINK/V2 debug tool adapter already connected to the
TiaC Magpie board, which has an already configured UART console connection.

On the TiaC MAGPIE pin headers the following SPI pins must be connected.

.. image:: loopback_test_SPI.svg
   :alt: TiaC MAGPIE Pin Header SPI Loopback Wiring
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
                --testsuite-root zephyr/tests --tag spi

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
         INFO    - 1/8 magpie_f777ni/stm32f777xx tests/drivers/spi/spi_loopback/drivers.spi.max32_dma.loopback :byl:`FILTERED` (runtime filter)
         INFO    - 2/8 magpie_f777ni/stm32f777xx tests/drivers/spi/spi_loopback/drivers.spi.nrf_pm_runtime :byl:`FILTERED` (runtime filter)
         INFO    - 3/8 magpie_f777ni/stm32f777xx tests/drivers/spi/spi_loopback/drivers.spi.loopback.lpspi.async.unset :byl:`FILTERED` (runtime filter)
         INFO    - 4/8 magpie_f777ni/stm32f777xx tests/drivers/spi/spi_loopback/drivers.spi.loopback.lpspi.dma.async.unset :byl:`FILTERED` (runtime filter)
         INFO    - 5/8 magpie_f777ni/stm32f777xx tests/drivers/spi/spi_loopback/drivers.spi.loopback.internal :byl:`FILTERED` (runtime filter)
         INFO    - 6/8 magpie_f777ni/stm32f777xx tests/drivers/spi/spi_loopback/drivers.spi.loopback.lpspi.dma :byl:`FILTERED` (runtime filter)
         INFO    - 7/8 magpie_f777ni/stm32f777xx tests/drivers/spi/dt_spec/drivers.spi.dt_spec      :bgn:`PASSED` (device: DT04BNT1, 3.251s <zephyr>)
         INFO    - 8/8 magpie_f777ni/stm32f777xx tests/drivers/spi/spi_loopback/drivers.spi.loopback.stm32f777xx :bgn:`PASSED` (device: DT04BNT1, 3.829s <zephyr>)

         INFO    - 2763 test scenarios (2539 configurations) selected, :byl:`2537` configurations filtered (2531 by static filter, 6 at runtime).
         INFO    - :bgn:`2 of 2` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`59.08 seconds`.
         INFO    - 2 of 2 executed test cases passed (100.00%) on 1 out of total 1133 platforms (0.09%).
         INFO    - 5 selected test cases not executed: 5 skipped.
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
