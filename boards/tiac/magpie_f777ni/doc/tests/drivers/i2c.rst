.. _magpie_f777ni_drivers_i2c-tests:

I2C Loopback (:brd:`FAILED`)
############################

Overview
********

See :zephyr_file:`tests/drivers/i2c`
for the original scope of tests, its structure and description.

.. _magpie_f777ni_drivers_i2c-tests-requirements:

Requirements
************

You will need an ST-LINK/V2 debug tool adapter already connected to the
TiaC Magpie board, which has an already configured UART console connection.

On the TiaC MAGPIE pin headers the following I2C pins must be connected.

.. image:: loopback_test_I2C.svg
   :alt: TiaC MAGPIE Pin Header I2C Loopback Wiring
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
                --testsuite-root zephyr/tests --tag i2c

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
         INFO    - 1/3 magpie_f777ni/stm32f777xx tests/drivers/i2c/i2c_api/drivers.i2c.api          :byl:`FILTERED` (runtime filter)
         INFO    - 2/3 magpie_f777ni/stm32f777xx tests/drivers/i2c/i2c_bme688/drivers.i2c.bme688    :byl:`FILTERED` (runtime filter)
         INFO    - 3/3 magpie_f777ni/stm32f777xx tests/drivers/i2c/i2c_target_api/drivers.i2c.target_api.dual_role :brd:`ERROR` Build failure (device <zephyr>)
         INFO    - :byl:`.../twister-out/magpie_f777ni_stm32f777xx/tests/drivers/i2c/i2c_target_api/drivers.i2c.target_api.dual_role/build.log`

         INFO    - 2763 test scenarios (2539 configurations) selected, :byl:`2538` configurations filtered (2536 by static filter, 2 at runtime).
         INFO    - :bgn:`0 of 1` executed test configurations passed (0.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`1` errored, with no warnings in :bbk:`28.30 seconds`.
         INFO    - 0 of 2 executed test cases passed (0.00%), 2 blocked on 1 out of total 1133 platforms (0.09%).
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
         INFO    - 1) tests/drivers/i2c/i2c_target_api/drivers.i2c.target_api.dual_role on magpie_f777ni/stm32f777xx error (Build failure - error: 'i2c_eeprom_target_init' defined but not used [-Werror=unused-function])
         INFO    -
         INFO    - To rerun the tests, call twister using the following commandline:
         INFO    - west twister -p <PLATFORM> -s <TEST ID>, for example:
         INFO    -
         INFO    - west twister -p magpie_f777ni/stm32f777xx -s tests/drivers/i2c/i2c_target_api/drivers.i2c.target_api.dual_role
         INFO    - or with west:
         INFO    - west build -p -b magpie_f777ni/stm32f777xx zephyr/tests/drivers/i2c/i2c_target_api -T drivers.i2c.target_api.dual_role
         INFO    - -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
         INFO    - Run completed

Open Issues
***********

Dual role with one I2C controller and one I2C device
====================================================

.. parsed-literal::
   :class: highlight-console notranslate

   ... ... ...
   .../zephyr/drivers/i2c/target/eeprom_target.c:244:12: :brd:`error:` 'i2c_eeprom_target_init' defined but not used
   .../zephyr/drivers/i2c/target/eeprom_target.c:227:43: :brd:`error:` 'api_funcs' defined but not used
   ... ... ...
   ... ... ...
   ... ... ...
