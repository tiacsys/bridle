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
minutes or hours to complete (:bbl:`≈3.00h` on :ibl:`≈880 platforms`).

With the option :code:`--integration` the time for testing can be reduced
significantly by limiting the test runs to the boards currently supported
by this test suite (checks only :bbl:`≈4.50%` of all platforms). But then
the runtime filter will not act as intended and the filtering rules become
ineffective:

   .. code-block:: console

      $ west twister \
             --jobs 4 \
             --verbose \
             --inline-logs \
             --integration \
             --testsuite-root bridle/tests/bridle/common
