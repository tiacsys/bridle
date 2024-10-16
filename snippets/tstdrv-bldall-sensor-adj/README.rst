.. _snippet-tstdrv-bldall-sensor-adj:

Build all Sensor drivers test adjustments (tstdrv-bldall-sensor-adj)
####################################################################

Overview
********

With this snippet, the user can create the Zephyr build all Sensor drivers
standard test suites and also run them successfully.

Programming
***********

Correct snippet designation must be entered when you invoke ``west build``.
For example:

.. code-block:: console

   west build -b native_sim \
              -d build/native_sim \
              -p always \
              -S tstdrv-bldall-sensor-adj \
              zephyr/tests/drivers/build_all/sensor
   ./build/native_sim/zephyr/zephyr.exe -stop_at=2

.. note::

   Be aware, error messages for runs on target are normal and expected for
   mocked hardware components such as test UART, test SPI, or test I2C.

Testing
*******

Correct snippet designation must be entered when you invoke ``west twister``,
either directly on the command line or as an alternative test specification.
For example:

.. code-block:: console

   west twister --alt-config-root bridle/zephyr/alt-config/tests/drivers/build_all/sensor \
                --testsuite-root zephyr/tests/drivers/build_all/sensor
