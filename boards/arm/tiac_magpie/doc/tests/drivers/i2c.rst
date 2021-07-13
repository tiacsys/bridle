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
             --testcase-root zephyr/tests/drivers/i2c

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
         INFO    - 1/1 tiac_magpie               tests/drivers/i2c/i2c_slave_api/drivers.i2c_slave  :brd:`FAILED` Failed (device 4.155s)

         INFO    - :brd:`0 of 1` test configurations passed (0.00%), :bbk:`1` failed, :byl:`2` skipped with :bbk:`0` warnings in :bbk:`21.22 seconds`
         INFO    - In total 1 test cases were executed, 3 skipped on 1 out of total 370 platforms (0.27%)
         INFO    - :bgn:`1` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         1 \|

Open Issues
***********

.. parsed-literal::
   :class: highlight

   Running test suite test_eeprom_slave
   ===================================================================
   START - test_eeprom_slave
   Found EP0 EEPROM_0 on I2C Master device I2C_3 at addr 54
   Found EP1 EEPROM_1 on I2C Master device I2C_4 at addr 56
   Testing single-role
   Testing full read: Master: I2C_4, address: 0x54

       :brd:`Assertion failed` at WEST_TOPDIR/zephyr/tests/drivers/i2c/i2c_slave_api/src/main.c:55: :byl:`run_full_read: (ret not equal to 0)`
   Failed to read EEPROM
    :brd:`FAIL` - test_eeprom_slave
   ===================================================================
   Test suite test_eeprom_slave failed.
   ===================================================================
   :brd:`PROJECT EXECUTION FAILED`
