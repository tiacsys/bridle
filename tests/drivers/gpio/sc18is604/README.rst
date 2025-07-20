.. _tests-drivers-gpio-sc18is604:

Emulator based integration tests of the SC18IS604 GPIO driver
#############################################################

As noted in :external+zephyr:ref:`ci tests` it is a common best practice
to running regression test suites locally before submit. This checking
the buildability and regression of the SC18IS604 GPIO driver with emulated
communication components inside a native simulation:

   .. code-block:: console

      $ west twister \
             --jobs 4 \
             --verbose \
             --inline-logs \
             --integration \
             --testsuite-root bridle/tests/drivers/gpio \
             --tag sc18is604
