.. _magpie_f777ni_drivers_counter-tests:

Counter (Real-Time Clock)
#########################

Overview
********

See :zephyr_file:`tests/drivers/counter`
for the original scope of tests, its structure and description.

.. _magpie_f777ni_drivers_counter-tests-requirements:

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
                --testsuite-root zephyr/tests --tag counter

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
         INFO    - 1/1 magpie_f777ni/stm32f777xx tests/drivers/counter/counter_basic_api/drivers.counter.basic_api :bgn:`PASSED` (device: DT04BNT1, 326.017s)

         INFO    - 2294 test scenarios (2077 test instances) selected, :byl:`2076` configurations filtered (2076 by static filter, 0 at runtime).
         INFO    - :bgn:`1 of 1` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`362.75 seconds`.
         INFO    - 4 of -3 executed test cases passed (-133.33%) on 1 out of total 876 platforms (0.11%).
         INFO    - 16095 selected test cases not executed: 14 skipped, 16081 filtered.
         INFO    - :bgn:`1` test configurations executed on platforms, :bbl:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board                     \| ID       \|   Counter \|   Failures \|
         \|---------------------------\|----------\|-----------\|------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \|         1 \|          0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni/stm32f777xx...
         INFO    - Writing JSON report .../twister-out/magpie_f777ni_stm32f777xx.json
         INFO    - Run completed
