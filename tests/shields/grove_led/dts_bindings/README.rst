.. _tests-shields-grove-led-dts-bindings:

Grove LED Shields DTS Binding
#############################

This integration test verifies the DTS binding of the :ref:`grove_led_shield`
against all possible :external+zephyr:term:`boards <board>`
and shields that are supported by :external+zephyr:ref:`Zephyr <boards>`
and :ref:`Bridle <boards>`.

Depending on the number of compatible boards, this test suite will take several
hours to complete (:bbl:`≈41.10h` for :ibl:`≈195 test scenarios` on
:ibl:`≈1500 platforms`) – :brd:`MAY FAIL – NOT EVALUATED`:

   .. code-block:: console

      $ west twister \
             --jobs 4 \
             --verbose \
             --inline-logs \
             --quarantine-list bridle/tests/quarantine.yaml \
             --testsuite-root bridle/tests/shields/grove_led/dts_bindings

With the option :code:`--cmake-only` the time for testing can be reduced
significantly, but then the runtime filter will not act as expected and
the filtering rules become ineffective – :brd:`MAY FAIL – NOT EVALUATED`:

   .. code-block:: console

      $ west twister \
             --jobs 4 \
             --verbose \
             --cmake-only \
             --inline-logs \
             --quarantine-list bridle/tests/quarantine.yaml \
             --testsuite-root bridle/tests/shields/grove_led/dts_bindings

Even more time can be saved with the option :code:`--integration` by limiting
the test runs to the boards currently supported by this shield and that will
be used for maintenance (checks only :bbl:`≈3.16%` of all platforms in about
:bbl:`≈5.10h`):

   .. code-block:: console

      $ west twister \
             --jobs 4 \
             --verbose \
             --cmake-only \
             --inline-logs \
             --integration \
             --quarantine-list bridle/tests/quarantine.yaml \
             --testsuite-root bridle/tests/shields/grove_led/dts_bindings
