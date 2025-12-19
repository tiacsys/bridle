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

   .. zephyr-app-commands::
      :app: zephyr/tests/drivers/build_all/sensor
      :build-dir: native_sim
      :board: native_sim
      :snippets: "tstdrv-bldall-sensor-adj"
      :gen-args: -DCONFIG_NATIVE_EXTRA_CMDLINE_ARGS=\"-stop_at=2\"
      :west-args: -p always
      :goals: run
      :compact:

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

Findings
********

.. rubric:: on native_sim/native/64

- disable ADXL362 at SPI, because of compilation errors:
  ``cast to pointer from integer of different size``
- disable ADXL367 at SPI and I2C, because of compilation errors:
  ``cast to pointer from integer of different size``
- disable ADXL372 at SPI and I2C, because of compilation errors:
  ``cast to pointer from integer of different size``
- disable BMA4XX at I2C, because of test assertion failed:
  ``expected_shifted not within actual_shifted +/- epsilon_shifted``
