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

         $ west twister \
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

         \| Platform                  \| ID       \| Serial device   \|
         \|---------------------------\|----------\|-----------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1/1 magpie_f777ni/stm32f777xx tests/drivers/hwinfo/api/drivers.hwinfo.api        :bgn:`PASSED` (device: DT04BNT1, 2.473s <zephyr>)

         INFO    - 2537 test scenarios (2325 configurations) selected, :byl:`2324` configurations filtered (2324 by static filter, 0 at runtime).
         INFO    - :bgn:`1 of 1` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`25.84 seconds`.
         INFO    - 4 of 4 executed test cases passed (100.00%) on 1 out of total 947 platforms (0.11%).
         INFO    - :bgn:`1` test configurations executed on platforms, :bbl:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board                     \| ID       \|   Counter \|   Failures \|
         \|---------------------------\|----------\|-----------\|------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \|         1 \|          0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../workspace/twister-out/twister.json
         INFO    - Writing xunit report .../workspace/twister-out/twister.xml...
         INFO    - Writing xunit report .../workspace/twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni/stm32f777xx...
         INFO    - Writing JSON report .../workspace/twister-out/magpie_f777ni_stm32f777xx.json
         INFO    - Run completed
