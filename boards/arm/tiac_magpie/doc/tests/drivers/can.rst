.. _tiac_magpie_drivers_can-tests:

CAN Loopback (internal)
#######################

Overview
********

See :zephyr_file:`tests/drivers/can`
for the original scope of tests, its structure and description.

.. _tiac_magpie_drivers_can-tests-requirements:

Requirements
************

You will need an ST-LINK/V2 debug tool adapter already connected to the
TiaC Magpie board, which has an already configured UART console connection.

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
             --board-root bridle/boards \
             --testcase-root zephyr/tests/drivers/can

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
         INFO    - 1/3 tiac_magpie               tests/drivers/can/stm32/drivers.can.stm32          :bgn:`PASSED` (device 4.158s)
         INFO    - 2/3 tiac_magpie               tests/drivers/can/api/drivers.can                  :bgn:`PASSED` (device 4.450s)
         INFO    - 3/3 tiac_magpie               tests/drivers/can/timing/drivers.can.timing        :bgn:`PASSED` (device 4.249s)

         INFO    - :bgn:`3 of 3` test configurations passed (100.00%), :bbk:`0` failed, :byl:`2` skipped with :bbk:`0` warnings in :bbk:`39.21 seconds`
         INFO    - In total 14 test cases were executed, 5 skipped on 1 out of total 370 platforms (0.27%)
         INFO    - :bgn:`3` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         3 \|
