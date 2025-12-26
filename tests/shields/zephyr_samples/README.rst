.. _tests-shields-zephyr-samples:

Buildability over all Zephyr samples
####################################

The Zephyr examples can also be instantiated with the help of the Zephyr
:external+zephyr:ref:`twister_script` and thus their buildability can be
checked for their originally intended integration platforms (checks only
:bbl:`≈1.25%` of all platforms, :ibl:`≈1100 test scenarios`).

.. tabs::

   .. group-tab:: ALL

      .. rubric:: Check all Zephyr samples:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --alt-config-root bridle/zephyr/alt-config/samples \
                --testsuite-root zephyr/samples \
                --tag zephyr

   .. zephyr-keep-sorted-start re(^\s{3}\.\. group-tab:: \w)

   .. group-tab:: ABC

   .. group-tab:: DEF

      .. rubric:: Check :external+zephyr:zephyr:code-sample:`display` sample:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --alt-config-root bridle/zephyr/alt-config/samples/drivers/display \
                --testsuite-root zephyr/samples/drivers/display

   .. group-tab:: GHI

      .. rubric:: Check :external+zephyr:zephyr:code-sample:`input-dump` sample:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --alt-config-root bridle/zephyr/alt-config/samples/subsys/input/input_dump \
                --testsuite-root zephyr/samples/subsys/input/input_dump

   .. group-tab:: JKL

      .. rubric:: Check :external+zephyr:zephyr:code-sample:`led-strip` sample:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --alt-config-root bridle/zephyr/alt-config/samples/drivers/led/led_strip \
                --testsuite-root zephyr/samples/drivers/led/led_strip

      .. rubric:: Check :external+zephyr:zephyr:code-sample:`rgb-led` sample:

      .. code-block:: console

         $ west twister \
                --jobs 4 \
                --verbose \
                --inline-logs \
                --integration \
                --alt-config-root bridle/zephyr/alt-config/samples/basic/rgb_led \
                --testsuite-root zephyr/samples/basic/rgb_led

   .. group-tab:: MNO

   .. group-tab:: PQRS

   .. group-tab:: TUV

   .. group-tab:: WXYZ

   .. zephyr-keep-sorted-stop
