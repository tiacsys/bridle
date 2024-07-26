.. _magpie_f777ni_drivers_hwinfo-tests:

Hardware Info-API
#################

Overview
********

See :zephyr_file:`tests/drivers/hwinfo`
for the original scope of tests, its structure and description.

.. _magpie_f777ni_drivers_hwinfo-tests-requirements:

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

         west twister \
              --verbose --jobs 4 --inline-logs \
              --enable-size-report --platform-reports \
              --device-testing --hardware-map map.yaml \
              --alt-config-root bridle/zephyr/alt-config/tests \
              --testsuite-root zephyr/tests --tag hwinfo

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
         INFO    - 1780/1780 magpie_f777ni             tests/drivers/hwinfo/api/drivers.hwinfo.api        :bgn:`PASSED` (device: DT04BNT1, 2.510s)

         INFO    - 1984 test scenarios (1780 test instances) selected, 1779 configurations skipped (1779 by static filter, 0 at runtime).
         INFO    - :bgn:`1 of 1780` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1779` skipped with :bbk:`0` warnings in :bbk:`29.52 seconds`
         INFO    - In total 4 test cases were executed, 13444 skipped on 1 out of total 739 platforms (0.14%)
         INFO    - :bgn:`1` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board         \| ID       \|   Counter \|
         \|---------------\|----------\|-----------\|
         \| magpie_f777ni \| DT04BNT1 \|         1 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni...
         INFO    - Run completed
