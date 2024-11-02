Grove LED Shields DTS Binding
#############################

This integration test verifies the DTS binding of the :ref:`grove_led_shield`
against all possible :zephyr:term:`boards <board>` and shields that are supported
by :external+zephyr:ref:`Zephyr <boards>` and :ref:`Bridle <boards>`.

Depending on the number of compatible boards, this test suite will take several
hours to complete::

    west twister \
         --jobs 4 \
         --verbose \
         --inline-logs \
         --quarantine-list bridle/tests/quarantine.yaml \
         --testsuite-root bridle/tests/shields/grove_led/dts_bindings

With the option ``--cmake-only`` the test time can be reduced significantly,
but then the runtime filter will not act as expected and the filtering rules
become ineffective::

    west twister \
         --jobs 4 \
         --verbose \
         --cmake-only \
         --inline-logs \
         --quarantine-list bridle/tests/quarantine.yaml \
         --testsuite-root bridle/tests/shields/grove_led/dts_bindings

Even more time can be saved with the option ``--integration`` by limiting
the test runs to the boards currently supported by this shield and that will
be used for maintenance::

    west twister \
         --jobs 4 \
         --verbose \
         --inline-logs \
         --integration \
         --quarantine-list bridle/tests/quarantine.yaml \
         --testsuite-root bridle/tests/shields/grove_led/dts_bindings
