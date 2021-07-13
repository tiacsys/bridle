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
             --testcase-root zephyr/tests/drivers/spi

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
         INFO    - 1/2 tiac_magpie               tests/drivers/spi/spi_loopback/driver.spi.loopback.internal :byl:`SKIPPED` (filter)
         INFO    - 2/2 tiac_magpie               tests/drivers/spi/spi_loopback/drivers.spi.loopback :bgn:`PASSED` (device 4.115s)

         INFO    - :bgn:`1 of 1` test configurations passed (100.00%), :bbk:`0` failed, :byl:`1` skipped with :bbk:`0` warnings in :bbk:`21.61 seconds`
         INFO    - In total 1 test cases were executed, 1 skipped on 1 out of total 370 platforms (0.27%)
         INFO    - :bgn:`1` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         1 \|
