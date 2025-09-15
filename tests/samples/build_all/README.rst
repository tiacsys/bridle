.. _tests-samples-build-all:

Buildability over all Bridle samples
####################################

The Bridle examples can also be instantiated with the help of the Zephyr
:external+zephyr:ref:`twister_script` and thus their buildability can be
checked for their originally intended integration platforms (checks only
:bbl:`≈2.65%` of all platforms, :ibl:`≈12 test scenarios`).

.. tabs::

   .. group-tab:: ALL

      .. rubric:: Check all Bridle samples:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --testsuite-root bridle/samples

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: ABC

      .. rubric:: Check :ref:`button-sample` sample:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --testsuite-root bridle/samples/button

      .. rubric:: Check :ref:`buzzer-sample` sample:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --testsuite-root bridle/samples/buzzer

   .. group-tab:: DEF

   .. group-tab:: GHI

      .. rubric:: Check :ref:`helloshell-sample` sample:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --testsuite-root bridle/samples/helloshell

   .. group-tab:: JKL

   .. group-tab:: MNO

   .. group-tab:: PQRS

      .. rubric:: Check :ref:`stk8ba58_3_axis_accelerometer-sample` sample:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --testsuite-root bridle/samples/stk8ba58

   .. group-tab:: TUV

      .. rubric:: Check :ref:`ubx_gnss-sample` sample:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --testsuite-root bridle/samples/ubx_gnss

   .. group-tab:: WXYZ

      .. rubric:: Check :ref:`waveshare_pico_10dof_imu_sensor-sample` sample:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --testsuite-root bridle/samples/waveshare_pico_10dof_imu_sensor

      .. rubric:: Check :ref:`waveshare_pico_environment_sensor-sample` sample:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --testsuite-root bridle/samples/waveshare_pico_environment_sensor

   .. zephyr-keep-sorted-stop
