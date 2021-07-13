.. _tiac_magpie_drivers_uart-tests:

UART Loopback (not yet)
#######################

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
             --verbose --jobs 4 --inline-logs \
             --enable-size-report --platform-reports \
             --device-testing --hardware-map map.yaml \
             --extra-args SHIELD=loopback_test_tmph \
             --board-root bridle/boards \
             --testcase-root zephyr/tests/drivers/uart

   .. group-tab:: Results ... t.b.d.

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1/1 tiac_magpie               tests/drivers/uart/uart_async_api/drivers.uart.uart_async_api :byl:`SKIPPED` (filter)

         INFO    - :bgn:`0 of 0` test configurations passed (0.00%), :bbk:`0` failed, :byl:`20` skipped with :bbk:`0` warnings in :bbk:`3.17 seconds`
         INFO    - In total 0 test cases were executed, 82 skipped on 1 out of total 370 platforms (0.27%)
         INFO    - :bgn:`0` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         0 \|
