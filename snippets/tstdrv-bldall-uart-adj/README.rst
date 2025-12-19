.. _snippet-tstdrv-bldall-uart-adj:

Build all UART drivers test adjustments (tstdrv-bldall-uart-adj)
################################################################

Overview
********

With this snippet, the user can create the Zephyr build all UART drivers
standard test suites and also run them successfully.

Programming
***********

Correct snippet designation must be entered when you invoke ``west build``.
For example:

   .. zephyr-app-commands::
      :app: zephyr/tests/drivers/build_all/uart
      :build-dir: native_sim
      :board: native_sim
      :snippets: "tstdrv-bldall-uart-adj"
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

      west twister --alt-config-root bridle/zephyr/alt-config/tests/drivers/build_all/uart \
                   --testsuite-root zephyr/tests/drivers/build_all/uart
