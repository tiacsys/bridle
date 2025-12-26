.. _tests-shields-x-grove-testbed-dts-bindings:

Grove Wiring Test Bed DTS Binding
#################################

This integration test verifies the DTS binding of the
:ref:`x_grove_testbed_shield` against all possible
:external+zephyr:term:`boards <board>`
that are supported by this shield:

   .. code-block:: console

      $ west twister \
             --jobs 4 \
             --verbose \
             --inline-logs \
             --integration \
             --quarantine-list bridle/tests/quarantine.yaml \
             --testsuite-root bridle/tests/shields/x_grove_testbed/dts_bindings
