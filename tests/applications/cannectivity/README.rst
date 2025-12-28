.. _tests-apps-cannectivity:

CANnectivity USB-to-CAN adapter firmware
########################################

This integration test verifies the buildability of
:external+cannectivity:doc:`CANnectivity <index>` against all possible
:external+zephyr:term:`boards <board>` that are supported by this application:

   .. code-block:: console

      $ west twister \
             --jobs 4 \
             --verbose \
             --inline-logs \
             --integration \
             --alt-config-root bridle/zephyr/alt-config/cannectivity \
             --testsuite-root cannectivity \
             --tag bridle
