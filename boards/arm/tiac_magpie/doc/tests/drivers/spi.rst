.. _tiac_magpie_drivers_spi-tests:

SPI Loopback
############

Overview
********

See :zephyr_file:`tests/drivers/spi`
for the original scope of tests, its structure and description.

.. _tiac_magpie_drivers_spi-tests-requirements:

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
             --alt-config-root bridle/zephyr/alt-config \
             --testsuite-root zephyr/tests --tag spi

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1565/1570 tiac_magpie               tests/drivers/spi/spi_loopback/drivers.spi.loopback.lpspi.async.unset :byl:`SKIPPED` (runtime filter)
         INFO    - 1566/1570 tiac_magpie               tests/drivers/spi/spi_loopback/drivers.spi.loopback.internal :byl:`SKIPPED` (runtime filter)
         INFO    - 1567/1570 tiac_magpie               tests/drivers/spi/spi_loopback/drivers.spi.loopback.lpspi.dma :byl:`SKIPPED` (runtime filter)
         INFO    - 1568/1570 tiac_magpie               tests/drivers/spi/spi_loopback/drivers.spi.loopback.lpspi.dma.async.unset :byl:`SKIPPED` (runtime filter)
         INFO    - 1569/1570 tiac_magpie               tests/drivers/spi/dt_spec/drivers.spi.dt_spec      :bgn:`PASSED` (device: DT04BNT1, 3.171s)
         INFO    - 1570/1570 tiac_magpie               tests/drivers/spi/spi_loopback/drivers.spi.loopback :bgn:`PASSED` (device: DT04BNT1, 2.428s)

         INFO    - 1782 test scenarios (1570 test instances) selected, 1568 configurations skipped (1564 by static filter, 4 at runtime).
         INFO    - :bgn:`2 of 1570` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1568` skipped with :bbk:`0` warnings in :bbk:`36.99 seconds`
         INFO    - In total 2 test cases were executed, 10955 skipped on 1 out of total 638 platforms (0.16%)
         INFO    - :bgn:`2` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         2 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
