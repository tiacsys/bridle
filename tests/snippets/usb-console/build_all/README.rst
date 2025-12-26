.. _tests-snippets-usb-console-build-all:

Buildability over all Bridle USB Console Boards and Snippets (usb-console)
##########################################################################

This integration test verifies the correct application of DTS overlays
and Kconfig configurations from the :ref:`snippet-usb-console`, which is
only included in Bridle, against all approved (snippet-supported)
:zephyr:term:`boards <board>` from :external+zephyr:ref:`Zephyr <boards>`
and :ref:`Bridle <boards>`.

Depending on the number of compatible boards, this test suite will take several
hours to complete (:bbl:`≈2.30h` for :ibl:`≈12 test scenarios` on
:ibl:`≈1130 platforms`) – :brd:`MAY FAIL – NOT EVALUATED`:

   .. code-block:: console

      $ west twister \
             --jobs 4 \
             --verbose \
             --inline-logs \
             --quarantine-list bridle/tests/quarantine.yaml \
             --testsuite-root bridle/tests/snippets/usb-console/build_all

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
             --testsuite-root bridle/tests/snippets/usb-console/build_all

Even more time can be saved with the option :code:`--integration` by limiting
the test runs to the boards currently supported by this shield and that will
be used for maintenance (checks only :bbl:`≈2.01%` of all platforms):

   .. code-block:: console

      $ west twister \
             --jobs 4 \
             --verbose \
             --cmake-only \
             --inline-logs \
             --integration \
             --quarantine-list bridle/tests/quarantine.yaml \
             --testsuite-root bridle/tests/snippets/usb-console/build_all
