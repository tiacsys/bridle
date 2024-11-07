.. _tests-drivers-build-all:

Buildability over all Bridle drivers
####################################

As noted in :zephyr:ref:`ci tests` it is a common best practice to running
regression test suites locally before submit. Checking the buildability of
all drivers maintained by Bridle is not a single test suite but rather the
reuse of Zephyr's :zephyr_file:`tests/drivers/build_all` test strategy with
significant adaptations to Bridle's needs. The following :command:`west`
commands can be used to check individual driver sets or really all drivers
(checks only :bbl:`≈12.00%` of all platforms, :ibl:`≈150 test scenarios`).

.. tabs::

   .. group-tab:: ALL

      .. rubric:: Check all drivers:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --alt-config-root bridle/zephyr/alt-config/tests/drivers/build_all \
                --testsuite-root zephyr/tests/drivers/build_all \
                --tag bridle \
                --tag zephyr

   .. group-tab:: ABC

   .. group-tab:: DEF

      .. rubric:: Check all :zephyr:ref:`display_api` drivers:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --alt-config-root bridle/zephyr/alt-config/tests/drivers/build_all/display \
                --testsuite-root zephyr/tests/drivers/build_all/display \
                --tag bridle \
                --tag zephyr

   .. group-tab:: GHI

      .. rubric:: Check all :zephyr:ref:`gpio_api` drivers:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --alt-config-root bridle/zephyr/alt-config/tests/drivers/build_all/gpio \
                --testsuite-root zephyr/tests/drivers/build_all/gpio \
                --tag bridle \
                --tag zephyr

      .. rubric:: Check all :zephyr:ref:`i2c_api` drivers:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --alt-config-root bridle/zephyr/alt-config/tests/drivers/build_all/i2c \
                --testsuite-root zephyr/tests/drivers/build_all/i2c \
                --tag bridle \
                --tag zephyr

   .. group-tab:: JKL

   .. group-tab:: MNO

      .. rubric:: Check all *Multi Function Device (MFD)* drivers:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --alt-config-root bridle/zephyr/alt-config/tests/drivers/build_all/mfd \
                --testsuite-root zephyr/tests/drivers/build_all/mfd \
                --tag bridle \
                --tag zephyr

   .. group-tab:: PQRS

      .. rubric:: Check all :zephyr:ref:`rtc_api` drivers:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --alt-config-root bridle/zephyr/alt-config/tests/drivers/build_all/rtc \
                --testsuite-root zephyr/tests/drivers/build_all/rtc \
                --tag bridle \
                --tag zephyr

      .. rubric:: Check all :zephyr:ref:`sensor` drivers:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --alt-config-root bridle/zephyr/alt-config/tests/drivers/build_all/sensor \
                --testsuite-root zephyr/tests/drivers/build_all/sensor \
                --tag bridle \
                --tag zephyr

   .. group-tab:: TUV

      .. rubric:: Check all :zephyr:ref:`uart_api` drivers:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --alt-config-root bridle/zephyr/alt-config/tests/drivers/build_all/uart \
                --testsuite-root zephyr/tests/drivers/build_all/uart \
                --tag bridle \
                --tag zephyr

   .. group-tab:: WXYZ
