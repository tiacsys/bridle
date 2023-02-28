.. _tiac_magpie_drivers_adc-tests:

ADC Loopback (:brd:`FAILED`)
############################

Overview
********

See :zephyr_file:`tests/drivers/adc`
for the original scope of tests, its structure and description.

.. _tiac_magpie_drivers_adc-tests-requirements:

Requirements
************

You will need an ST-LINK/V2 debug tool adapter already connected to the
TiaC Magpie board, which has an already configured UART console connection.

On the TiaC MAGPIE pin headers the following ADC pins must be connected.

.. image:: loopback_test_ADC.svg
   :alt: TiaC MAGPIE Pin Header ADC Loopback Wiring
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
             --testsuite-root zephyr/tests/drivers/adc

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
         INFO    - 3/3 tiac_magpie               tests/drivers/adc/adc_api/drivers.adc              :brd:`FAILED` Build failure (device)
         ERROR   - see: :byl:`.../twister-out/tiac_magpie/tests/drivers/adc/adc_api/drivers.adc/build.log`

         INFO    - 3 test scenarios (3 test instances) selected, 2 configurations skipped (2 by static filter, 0 at runtime).
         INFO    - :bgn:`0 of 3` test configurations passed (0.00%), :bbk:`1` failed, :byl:`2` skipped with :bbk:`0` warnings in :bbk:`8.85 seconds`
         INFO    - In total 1 test cases were executed, 10 skipped on 1 out of total 541 platforms (0.18%)
         INFO    - :bgn:`0` test configurations executed on platforms, :brd:`1` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
         INFO    - The following issues were found (showing the top 10 items):
         INFO    - 1) tests/drivers/adc/adc_api/drivers.adc on tiac_magpie error (Build failure)
         INFO    -
         INFO    - To rerun the tests, call twister using the following commandline:
         INFO    - west twister -p <PLATFORM> -s <TEST ID>, for example:
         INFO    -
         INFO    - west twister -p tiac_magpie -s tests/drivers/adc/adc_api/drivers.adc
         INFO    - or with west:
         INFO    - west build -p -b tiac_magpie -T tests/drivers/adc/adc_api/drivers.adc
         INFO    - -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
         INFO    - Run completed

Open Issues
***********

.. parsed-literal::
   :class: highlight

   ... ... ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:422:2: :brd:`error:` #error "Unsupported board."
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:437:22: :brd:`error:` :bbk:`'ADC_GAIN'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:438:22: :brd:`error:` :bbk:`'ADC_REFERENCE'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:439:22: :brd:`error:` :bbk:`'ADC_ACQUISITION_TIME'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:440:22: :brd:`error:` :bbk:`'ADC_1ST_CHANNEL_ID'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:459:28: :brd:`error:` :bbk:`'__device_dts_ord_ADC_DEVICE_NODE_ORD'` undeclared ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:472:52: :brd:`error:` :bbk:`'__device_dts_ord_ADC_DEVICE_NODE_ORD'` undeclared ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:523:18: :brd:`error:` :bbk:`'ADC_RESOLUTION'` undeclared ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:603:18: :brd:`error:` :bbk:`'ADC_RESOLUTION'` undeclared ...
   ... ... ...
   ... ... ...
   ... ... ...
