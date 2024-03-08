.. _tiac_magpie_drivers_i2c-tests:

I2C Loopback (:brd:`FAILED`)
############################

Overview
********

See :zephyr_file:`tests/drivers/i2c`
for the original scope of tests, its structure and description.

.. _tiac_magpie_drivers_i2c-tests-requirements:

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

         west twister \
              --verbose --jobs 4 --inline-logs \
              --enable-size-report --platform-reports \
              --device-testing --hardware-map map.yaml \
              --extra-args SHIELD="loopback_test_tmph" \
              --alt-config-root bridle/zephyr/alt-config \
              --testsuite-root zephyr/tests --tag i2c

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight-console notranslate

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1708/1709 tiac_magpie               tests/drivers/i2c/i2c_api/drivers.i2c.api          :byl:`SKIPPED` (runtime filter)
         INFO    - 1709/1709 tiac_magpie               tests/drivers/i2c/i2c_target_api/drivers.i2c.target_api.dual_role  :brd:`ERROR` Build failure (device)
         INFO    - :byl:`.../twister-out/tiac_magpie/tests/drivers/i2c/i2c_target_api/drivers.i2c.target_api.dual_role/build.log`

         INFO    - 1922 test scenarios (1709 test instances) selected, 1708 configurations skipped (1707 by static filter, 1 at runtime).
         INFO    - :bgn:`0 of 1709` test configurations passed (0.00%), :bbk:`0` failed, :brd:`1` errored, :byl:`1708` skipped with :bbk:`0` warnings in :bbk:`18.87 seconds`
         INFO    - In total 1 test cases were executed, 12683 skipped on 1 out of total 699 platforms (0.14%)
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
         INFO    - 1) tests/drivers/i2c/i2c_target_api/drivers.i2c.target_api.dual_role on tiac_magpie error (Build failure)
         INFO    - 
         INFO    - To rerun the tests, call twister using the following commandline:
         INFO    - west twister -p <PLATFORM> -s <TEST ID>, for example:
         INFO    - 
         INFO    - west twister -p tiac_magpie -s tests/drivers/i2c/i2c_target_api/drivers.i2c.target_api.dual_role
         INFO    - or with west:
         INFO    - west build -p -b tiac_magpie tests/drivers/i2c/i2c_target_api -T drivers.i2c.target_api.dual_role
         INFO    - -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
         INFO    - Run completed

Open Issues
***********

Dual role with one I2C controller and one I2C device
====================================================

.. parsed-literal::
   :class: highlight-console notranslate

   ... ... ...
   .../zephyr/drivers/i2c/target/eeprom_target.c:229:12: :brd:`error:` 'i2c_eeprom_target_init' defined but not used
   .../zephyr/drivers/i2c/target/eeprom_target.c:212:43: :brd:`error:` 'api_funcs' defined but not used
   ... ... ...
   ... ... ...
   ... ... ...
