.. _magpie_f777ni_drivers_adc-tests:

ADC Loopback (:brd:`FAILED`)
############################

Overview
********

See :zephyr_file:`tests/drivers/adc`
for the original scope of tests, its structure and description.

.. _magpie_f777ni_drivers_adc-tests-requirements:

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

         $ west twister \
                --verbose --jobs 4 --inline-logs \
                --enable-size-report --platform-reports \
                --device-testing --hardware-map map.yaml \
                --extra-args SHIELD="loopback_test_tmph" \
                --alt-config-root bridle/zephyr/alt-config/tests \
                --testsuite-root zephyr/tests --tag adc

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
         INFO    - 1/1 magpie_f777ni/stm32f777xx tests/drivers/adc/adc_api/drivers.adc              :brd:`ERROR` Build failure (device <zephyr>)
         INFO    - :byl:`.../twister-out/magpie_f777ni_stm32f777xx/tests/drivers/adc/adc_api/drivers.adc/build.log`

         INFO    - 2763 test scenarios (2539 configurations) selected, :byl:`2538` configurations filtered (2538 by static filter, 0 at runtime).
         INFO    - :bgn:`0 of 1` test configurations passed (0.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`1` errored, with no warnings in :bbk:`20.00 seconds`.
         INFO    - 0 of 6 executed test cases passed (0.00%), 6 blocked on 1 out of total 1133 platforms (0.09%).
         INFO    - :bgn:`0` test configurations executed on platforms, :bbl:`1` test configurations were only built.

         Hardware distribution summary:

         \| Board                     \| ID       \|   Counter \|   Failures \|
         \|---------------------------\|----------\|-----------\|------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \|         0 \|          0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni/stm32f777xx...
         INFO    - Writing JSON report .../twister-out/magpie_f777ni_stm32f777xx.json
         INFO    - -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
         INFO    - The following issues were found (showing the top 10 items):
         INFO    - 1) tests/drivers/adc/adc_api/drivers.adc on magpie_f777ni/stm32f777xx error (Build failure - error: #error "Unsupported board.")
         INFO    -
         INFO    - To rerun the tests, call twister using the following commandline:
         INFO    - west twister -p <PLATFORM> -s <TEST ID>, for example:
         INFO    -
         INFO    - west twister -p magpie_f777ni/stm32f777xx -s tests/drivers/adc/adc_api/drivers.adc
         INFO    - or with west:
         INFO    - west build -p -b magpie_f777ni/stm32f777xx tests/drivers/adc/adc_api -T drivers.adc
         INFO    - -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
         INFO    - Run completed

Open Issues
***********

.. parsed-literal::
   :class: highlight-console notranslate

   ... ... ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:52:2: :brd:`error:` #error "Unsupported board."
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:57:31: :brd:`error:` :bbk:`'adc_channels'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:89:39: :brd:`error:` :bbk:`'adc_channels'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:91:25: :brd:`error:` :bbk:`'adc_channels_count'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:142:37: :brd:`error:` :bbk:`'adc_channels'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:169:37: :brd:`error:` :bbk:`'adc_channels'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:171:29: :brd:`error:` :bbk:`'adc_channels_count'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:188:13: :brd:`error:` :bbk:`'adc_channels_count'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:220:37: :brd:`error:` :bbk:`'adc_channels'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:279:37: :brd:`error:` :bbk:`'adc_channels'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:312:35: :brd:`error:` :bbk:`'adc_channels_count'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:355:37: :brd:`error:` :bbk:`'adc_channels'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:357:13: :brd:`error:` :bbk:`'adc_channels_count'` undeclared here ...
   .../zephyr/tests/drivers/adc/adc_api/src/test_adc.c:382:36: :brd:`error:` :bbk:`'adc_channels'` undeclared here ...
   ... ... ...
   ... ... ...
   ... ... ...
