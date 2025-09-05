.. _snippet-tstdrv-bldall-i2c-adj:

Build all I2C drivers test adjustments (tstdrv-bldall-i2c-adj)
##############################################################

Overview
********

With this snippet, the user can create the Zephyr build all I2C drivers
standard test suites and also run them successfully.

Programming
***********

Correct snippet designation must be entered when you invoke ``west build``.
For example:

   .. zephyr-app-commands::
      :app: zephyr/tests/drivers/build_all/i2c
      :build-dir: native_sim
      :board: native_sim
      :snippets: "tstdrv-bldall-i2c-adj"
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

      west twister --alt-config-root bridle/zephyr/alt-config/tests/drivers/build_all/i2c \
                   --testsuite-root zephyr/tests/drivers/build_all/i2c
