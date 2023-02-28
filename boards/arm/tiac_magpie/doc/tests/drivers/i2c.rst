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

         $ ./zephyr/scripts/twister \
             --verbose --jobs 4 --inline-logs \
             --enable-size-report --platform-reports \
             --device-testing --hardware-map map.yaml \
             --extra-args SHIELD=loopback_test_tmph \
             --board-root bridle/boards \
             --testsuite-root zephyr/tests/drivers/i2c \
             --testsuite-root bridle/tests/drivers/i2c

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
         INFO    - 3/5 tiac_magpie               tests/drivers/i2c/i2c_api/drivers.i2c.api          :byl:`SKIPPED` (runtime filter)
         INFO    - 4/5 tiac_magpie               i2c_target_api/drivers.i2c.target_api.tiac_magpie  :brd:`FAILED` Failed (device 2.637s)
         ERROR   - see: :byl:`.../twister-out/tiac_magpie/i2c_slave_api/drivers.i2c.target_api.tiac_magpie/handler.log`
         INFO    - 5/5 tiac_magpie               i2c_target_api/drivers.i2c.target_api.dual_role.tiac_magpie :brd:`FAILED` Failed (device 2.637s)
         ERROR   - see: :byl:`.../twister-out/tiac_magpie/i2c_slave_api/drivers.i2c.target_api.dual_role.tiac_magpie/handler.log`

         INFO    - 5 test scenarios (5 test instances) selected, 3 configurations skipped (2 by static filter, 1 at runtime).
         INFO    - :brd:`0 of 5` test configurations passed (0.00%), :bbk:`2` failed, :byl:`3` skipped with :bbk:`0` warnings in :bbk:`30.32 seconds`
         INFO    - In total 2 test cases were executed, 4 skipped on 1 out of total 541 platforms (0.18%)
         INFO    - :bgn:`2` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         2 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
         INFO    - The following issues were found (showing the top 10 items):
         INFO    - 1) i2c_target_api/drivers.i2c.target_api.tiac_magpie on tiac_magpie failed (Failed)
         INFO    - 2) i2c_target_api/drivers.i2c.target_api.dual_role.tiac_magpie on tiac_magpie failed (Failed)
         INFO    -
         INFO    - To rerun the tests, call twister using the following commandline:
         INFO    - west twister -p <PLATFORM> -s <TEST ID>, for example:
         INFO    -
         INFO    - west twister -p tiac_magpie -s i2c_target_api/drivers.i2c.target_api.dual_role.tiac_magpie
         INFO    - or with west:
         INFO    - west build -p -b tiac_magpie -T i2c_target_api/drivers.i2c.target_api.dual_role.tiac_magpie
         INFO    - -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
         INFO    - Run completed

Open Issues
***********

Single role with two I2C controller
===================================

.. parsed-literal::
   :class: highlight

   Running TESTSUITE i2c_eeprom_target
   ===================================================================
   START - test_eeprom_target
   Found EEPROM 0 on I2C bus device i2c@40005c00 at addr 54
   Found EEPROM 1 on I2C bus device i2c@40006000 at addr 56
   :bbk:`Testing single-role`
   Testing full read: Master: i2c@40006000, address: 0x54
   :brd:`Assertion failed` at WEST_TOPDIR/zephyr/tests/drivers/i2c/i2c_target_api/src/main.c:55: :byl:`run_full_read: (ret not equal to 0)`
   Failed to read EEPROM
   :brd:`FAIL` - test_eeprom_target in 0.031 seconds
   ===================================================================
   TESTSUITE i2c_eeprom_target failed.
   ------ TESTSUITE SUMMARY START ------
   SUITE FAIL -   0.00% [i2c_eeprom_target]: pass = 0, fail = 1, skip = 0, total = 1 duration = 0.031 seconds
   - :brd:`FAIL` - [i2c_eeprom_target.test_eeprom_target] duration = 0.031 seconds
   ------ TESTSUITE SUMMARY END ------
   ===================================================================
   RunID: 55c0aabe41d4d446bfaf27e3808917d0
   :brd:`PROJECT EXECUTION FAILED`

Dual role with one I2C controller and one I2C device
====================================================

.. parsed-literal::
   :class: highlight

   Running TESTSUITE i2c_eeprom_target
   ===================================================================
   START - test_eeprom_target
   Found EEPROM 0 on I2C bus device i2c@40005c00 at addr 54
   Found EEPROM 1 on I2C bus device i2c@40006000 at addr 56
   :bbk:`Testing dual-role`
   Testing full read: Master: i2c@40006000, address: 0x54
   :brd:`Assertion failed` at WEST_TOPDIR/zephyr/tests/drivers/i2c/i2c_target_api/src/main.c:55: :byl:`run_full_read: (ret not equal to 0)`
   Failed to read EEPROM
   :brd:`FAIL` - test_eeprom_target in 0.030 seconds
   ===================================================================
   TESTSUITE i2c_eeprom_target failed.
   ------ TESTSUITE SUMMARY START ------
   SUITE FAIL -   0.00% [i2c_eeprom_target]: pass = 0, fail = 1, skip = 0, total = 1 duration = 0.030 seconds
   - :brd:`FAIL` - [i2c_eeprom_target.test_eeprom_target] duration = 0.030 seconds
   ------ TESTSUITE SUMMARY END ------
   ===================================================================
   RunID: 3beabba9b33b1dc4a1e19ec0ddfbd881
   :brd:`PROJECT EXECUTION FAILED`
