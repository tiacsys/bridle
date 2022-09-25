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

         $ ./zephyr/scripts/twister \
             --verbose --jobs 4 --inline-logs \
             --enable-size-report --platform-reports \
             --device-testing --hardware-map map.yaml \
             --extra-args SHIELD=loopback_test_tmph \
             --board-root bridle/boards \
             --testsuite-root zephyr/tests/drivers/spi

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - 6 test scenarios (6 configurations) selected, 2 configurations discarded due to filters.
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 3/6 tiac_magpie               tests/drivers/spi/spi_loopback/drivers.spi.loopback.internal :byl:`SKIPPED` (runtime filter)
         INFO    - 4/6 tiac_magpie               tests/drivers/spi/spi_loopback/drivers.spi.loopback :byl:`SKIPPED` (runtime filter)
         INFO    - 5/6 tiac_magpie               tests/drivers/spi/dt_spec/drivers.spi.dt_spec      :bgn:`PASSED` (device 3.873s)
         INFO    - 6/6 tiac_magpie               tests/drivers/spi/spi_loopback/drivers.stm32_spi.loopback :bgn:`PASSED` (device 3.944s)

         INFO    - :bgn:`2 of 6` test configurations passed (100.00%), :bbk:`0` failed, :byl:`4` skipped with :bbk:`0` warnings in :bbk:`29.63 seconds`
         INFO    - In total 4 test cases were executed, 2 skipped on 1 out of total 457 platforms (0.22%)
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
