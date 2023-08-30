Grove Wiring Test Bed DTS Binding
#################################

This integration test verifies the DTS binding of the
:ref:`x_grove_testbed_shield` against all possible :term:`boards <zephyr:board>`
that are supported by this shield::

    west twister \
         --jobs 4 \
         --verbose \
         --inline-logs \
         --testsuite-root bridle/tests/shields/x_grove_testbed/dts_bindings
