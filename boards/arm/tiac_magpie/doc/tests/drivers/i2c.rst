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

         INFO    - 5 test scenarios (5 configurations) selected, 3 configurations discarded due to filters.
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 4/5 tiac_magpie               i2c_slave_api/drivers.i2c.slave_api.tiac_magpie    :brd:`FAILED` Failed (device 4.491s)
         ERROR   - see: :byl:`.../twister-out/tiac_magpie/i2c_slave_api/drivers.i2c.slave_api.tiac_magpie/handler.log`
         INFO    - 5/5 tiac_magpie               i2c_slave_api/drivers.i2c.slave_api.dual_role.tiac_magpie :brd:`FAILED` Failed (device 4.757s)
         ERROR   - see: :byl:`.../twister-out/tiac_magpie/i2c_slave_api/drivers.i2c.slave_api.dual_role.tiac_magpie/handler.log`

         INFO    - :brd:`0 of 5` test configurations passed (0.00%), :bbk:`2` failed, :byl:`3` skipped with :bbk:`0` warnings in :bbk:`27.96 seconds`
         INFO    - In total 6 test cases were executed, 0 skipped on 1 out of total 457 platforms (0.22%)
         INFO    - :bgn:`2` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         2 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Using 'zephyr' toolchain.
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed

Open Issues
***********

Single role with two I2C controller
===================================

.. parsed-literal::
   :class: highlight

   Running TESTSUITE test_eeprom_slave
   ===================================================================
   START - test_eeprom_slave
   Found EP0 EEPROM_0 on I2C Master device I2C_3 at addr 54
   Found EP1 EEPROM_1 on I2C Master device I2C_4 at addr 56
   :bbk:`Testing single-role`
   Testing full read: Master: I2C_4, address: 0x54
   :brd:`Assertion failed` at WEST_TOPDIR/zephyr/tests/drivers/i2c/i2c_slave_api/src/main.c:55: :byl:`run_full_read: (ret not equal to 0)`
   Failed to read EEPROM
   :brd:`FAIL` - test_eeprom_slave in 0.33 seconds
   ===================================================================
   TESTSUITE test_eeprom_slave failed.
   ===================================================================
   RunID: a742ed391022d2d25746793fb51d07be
   :brd:`PROJECT EXECUTION FAILED`

Dual role with one I2C controller and one I2C device
====================================================

.. parsed-literal::
   :class: highlight

   Running TESTSUITE test_eeprom_slave
   ===================================================================
   START - test_eeprom_slave
   Found EP0 EEPROM_0 on I2C Master device I2C_3 at addr 54
   Found EP1 EEPROM_1 on I2C Master device I2C_4 at addr 56
   :bbk:`Testing dual-role`
   Testing full read: Master: I2C_4, address: 0x54
   :brd:`Assertion failed` at WEST_TOPDIR/zephyr/tests/drivers/i2c/i2c_slave_api/src/main.c:55: :byl:`run_full_read: (ret not equal to 0)`
   Failed to read EEPROM
   :brd:`FAIL` - test_eeprom_slave in 0.530 seconds
   ===================================================================
   TESTSUITE test_eeprom_slave failed.
   ===================================================================
   RunID: 676b8933f8a718e671517aa01104bf1b
   :brd:`PROJECT EXECUTION FAILED`
