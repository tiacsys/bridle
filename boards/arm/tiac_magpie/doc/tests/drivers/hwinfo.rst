.. _tiac_magpie_drivers_hwinfo-tests:

Hardware Info-API
#################

Overview
********

See :zephyr_file:`tests/drivers/hwinfo`
for the original scope of tests, its structure and description.

.. _tiac_magpie_drivers_hwinfo-tests-requirements:

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
             --board-root bridle/boards \
             --platform tiac_magpie \
             --device-testing --device-serial /dev/ttyUSBx \
             --testcase-root zephyr/tests/drivers/hwinfo

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1/1 tiac_magpie               tests/drivers/hwinfo/api/drivers.device_id         :bgn:`PASSED` (device 2.941s)

         INFO    - :bgn:`1 of 1` test configurations passed (100.00%), :bbk:`0` failed, :byl:`0` skipped with :bbk:`0` warnings in :bbk:`30.53 seconds`
         INFO    - In total 2 test cases were executed, 0 skipped on 1 out of total 330 platforms (0.30%)
         INFO    - :bgn:`1` test configurations executed on platforms, :brd:`0` test configurations were only built.
