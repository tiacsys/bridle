.. _tests-bridle-common:

Bridle Common Testing
#####################

Currently this integration test verifies the auto-generated version number:

   .. code-block:: console

      $ west twister \
             --jobs 4 \
             --verbose \
             --inline-logs \
             --quarantine-list bridle/tests/quarantine.yaml \
             --testsuite-root bridle/tests/bridle/common

Depending on the number of compatible boards, this test suite will take several
minutes or hours to complete (:bbl:`≈4.60h` on :ibl:`≈1300 platforms`).

With the option :code:`--integration` the time for testing can be reduced
significantly by limiting the test runs to the boards currently supported
by this test suite (checks only :bbl:`≈2.78%` of all platforms). But then
the runtime filter will not act as intended and the filtering rules become
ineffective:

   .. code-block:: console

      $ west twister \
             --jobs 4 \
             --verbose \
             --inline-logs \
             --integration \
             --testsuite-root bridle/tests/bridle/common

API Reference
*************

   .. doxygengroup:: bridle_common_tests
      :project: bridle

.. rubric:: Functions

- :c:func:`test_version()`
