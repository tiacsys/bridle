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

         west twister \
              --verbose --jobs 4 --inline-logs \
              --enable-size-report --platform-reports \
              --device-testing --hardware-map map.yaml \
              --extra-args SHIELD="loopback_test_tmph" \
              --alt-config-root bridle/zephyr/alt-config \
              --testsuite-root zephyr/tests --tag adc

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
         INFO    - 1570/1570 tiac_magpie               tests/drivers/adc/adc_api/drivers.adc               :brd:`ERROR` Build failure (device)
         INFO    - :byl:`.../twister-out/tiac_magpie/tests/drivers/adc/adc_api/drivers.adc/build.log`

         INFO    - 1782 test scenarios (1570 test instances) selected, 1569 configurations skipped (1569 by static filter, 0 at runtime).
         INFO    - :bgn:`0 of 1570` test configurations passed (0.00%), :bbk:`0` failed, :brd:`1` errored, :byl:`1569` skipped with :bbk:`0` warnings in :bbk:`13.96 seconds`
         INFO    - In total 6 test cases were executed, 10952 skipped on 1 out of total 638 platforms (0.16%)
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
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:33:2: :brd:`error:` #error "Unsupported board."
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:38:31: :brd:`error:` :bbk:`'adc_channels'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:50:39: :brd:`error:` :bbk:`'adc_channels'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:52:25: :brd:`error:` :bbk:`'adc_channels_count'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:94:37: :brd:`error:` :bbk:`'adc_channels'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:121:37: :brd:`error:` :bbk:`'adc_channels'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:123:29: :brd:`error:` :bbk:`'adc_channels_count'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:140:13: :brd:`error:` :bbk:`'adc_channels_count'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:172:37: :brd:`error:` :bbk:`'adc_channels'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:231:37: :brd:`error:` :bbk:`'adc_channels'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:264:35: :brd:`error:` :bbk:`'adc_channels_count'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:307:37: :brd:`error:` :bbk:`'adc_channels'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:309:13: :brd:`error:` :bbk:`'adc_channels_count'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:334:36: :brd:`error:` :bbk:`'adc_channels'` undeclared here ...
   ... ... ...
   ... ... ...
   ... ... ...
