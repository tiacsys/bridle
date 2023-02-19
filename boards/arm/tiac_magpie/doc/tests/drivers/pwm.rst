.. _tiac_magpie_drivers_pwm-tests:

PWM Loopback (:brd:`FAILED`)
############################

Overview
********

See :zephyr_file:`tests/drivers/pwm`
for the original scope of tests, its structure and description.

.. _tiac_magpie_drivers_pwm-tests-requirements:

Requirements
************

You will need an ST-LINK/V2 debug tool adapter already connected to the
TiaC Magpie board, which has an already configured UART console connection.

On the TiaC MAGPIE pin headers the following PWM pins must be connected.

.. image:: loopback_test_PWM.svg
   :alt: TiaC MAGPIE Pin Header PWM Loopback Wiring
   :align: center

Building and Running
********************

.. tabs::

   .. group-tab:: Running

      Build and run the tests on target as follows:

      .. code-block:: console

         $ ./zephyr/scripts/twister \
             --verbose --jobs 4 --inline-logs \
             --enable-size-report --platform-reports \
             --device-testing --hardware-map map.yaml \
             --extra-args SHIELD=loopback_test_tmph \
             --board-root bridle/boards \
             --testcase-root zephyr/tests/drivers/pwm

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - 2 test scenarios (2 configurations) selected, 0 configurations discarded due to filters.
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1/2 tiac_magpie               tests/drivers/pwm/pwm_api/drivers.pwm              :brd:`FAILED` Failed (device 7.745s)
         ERROR   - see: :byl:`.../twister-out/tiac_magpie/tests/drivers/pwm/pwm_api/drivers.pwm/handler.log`
         INFO    - 2/2 tiac_magpie               tests/drivers/pwm/pwm_loopback/drivers.pwm.loopback :brd:`FAILED` Failed (device 6.017s)
         ERROR   - see: :byl:`.../twister-out/tiac_magpie/tests/drivers/pwm/pwm_loopback/drivers.pwm.loopback/handler.log`

         INFO    - :bgn:`0 of 2` test configurations passed (0.00%), :bbk:`2` failed, :byl:`0` skipped with :bbk:`0` warnings in :bbk:`54.91 seconds`
         INFO    - In total 11 test cases were executed, 0 skipped on 1 out of total 428 platforms (0.23%)
         INFO    - :bgn:`2` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         2 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Using 'zephyr' toolchain.
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed

Open Issues
***********

PWM API
=======

Verify PWM can work well when configure through nsec, or cycle.

.. parsed-literal::
   :class: highlight

   Running TESTSUITE pwm_basic_test
   ===================================================================
   START - test_pwm_usec
   [PWM]: 1, [period]: 2000, [pulse]: 1000
   :bbk:`Fail to set the period and pulse width`
   :brd:`Assertion failed` at WEST_TOPDIR/zephyr/tests/drivers/pwm/pwm_api/src/test_pwm.c:144: :byl:`test_pwm_usec: test_task(DEFAULT_PWM_PORT, DEFAULT_PERIOD_USEC, DEFAULT_PULSE_USEC, UNIT_USECS) == TC_PASS is false`
   :brd:`FAIL` - test_pwm_usec in 0.26 seconds
   ===================================================================
   START - test_pwm_nsec
   [PWM]: 1, [period]: 2000000, [pulse]: 1000000
   :bbk:`Fail to set the period and pulse width`
   :brd:`Assertion failed` at WEST_TOPDIR/zephyr/tests/drivers/pwm/pwm_api/src/test_pwm.c:162: :byl:`test_pwm_nsec: test_task(DEFAULT_PWM_PORT, DEFAULT_PERIOD_NSEC, DEFAULT_PULSE_NSEC, UNIT_NSECS) == TC_PASS is false`
   :brd:`FAIL` - test_pwm_nsec in 0.26 seconds
   ===================================================================
   START - test_pwm_cycle
   [PWM]: 1, [period]: 64000, [pulse]: 32000
   [PWM]: 1, [period]: 64000, [pulse]: 64000
   [PWM]: 1, [period]: 64000, [pulse]: 0
   :bgn:`PASS` - test_pwm_cycle in 2.11 seconds
   ===================================================================
   TESTSUITE pwm_basic_test failed.
   ===================================================================
   :brd:`PROJECT EXECUTION FAILED`

PWM Loopback
============

Verify PWM can capture pulse, period, or pulse and period. It needs
the ``test-pwm-loopback`` DTS binding with two PWM channels, first
index must be a 32-Bit timer.

.. parsed-literal::
   :class: highlight

   Running TESTSUITE pwm_loopback_test
   ===================================================================
   START - test_pulse_capture
   Testing PWM capture @ 15000000/100000000 nsec
   :brd:`Assertion failed` at WEST_TOPDIR/zephyr/tests/drivers/pwm/pwm_loopback/src/test_pwm_loopback.c:71: :byl:`test_capture: (err not equal to 0)`
   :bbk:`failed to set pwm output (err -134)`
   :brd:`FAIL` - test_pulse_capture in 0.20 seconds
   ===================================================================
   START - test_pulse_capture_inverted
   Testing PWM capture @ 15000000/100000000 nsec
   :brd:`Assertion failed` at WEST_TOPDIR/zephyr/tests/drivers/pwm/pwm_loopback/src/test_pwm_loopback.c:71: :byl:`test_capture: (err not equal to 0)`
   :bbk:`failed to set pwm output (err -134)`
   :brd:`FAIL` - test_pulse_capture_inverted in 0.20 seconds
   ===================================================================
   START - test_period_capture
   Testing PWM capture @ 15000000/100000000 nsec
   :brd:`Assertion failed` at WEST_TOPDIR/zephyr/tests/drivers/pwm/pwm_loopback/src/test_pwm_loopback.c:71: :byl:`test_capture: (err not equal to 0)`
   :bbk:`failed to set pwm output (err -134)`
   :brd:`FAIL` - test_period_capture in 0.20 seconds
   ===================================================================
   START - test_period_capture_inverted
   Testing PWM capture @ 15000000/100000000 nsec
   :brd:`Assertion failed` at WEST_TOPDIR/zephyr/tests/drivers/pwm/pwm_loopback/src/test_pwm_loopback.c:71: :byl:`test_capture: (err not equal to 0)`
   :bbk:`failed to set pwm output (err -134)`
   :brd:`FAIL` - test_period_capture_inverted in 0.20 seconds
   ===================================================================
   START - test_pulse_and_period_capture
   Testing PWM capture @ 15000000/100000000 nsec
   :brd:`Assertion failed` at WEST_TOPDIR/zephyr/tests/drivers/pwm/pwm_loopback/src/test_pwm_loopback.c:71: :byl:`test_capture: (err not equal to 0)`
   :bbk:`failed to set pwm output (err -134)`
   :brd:`FAIL` - test_pulse_and_period_capture in 0.20 seconds
   ===================================================================
   START - test_capture_timeout
   :bbk:`E: PWM capture only supported on first two channels`
   E: failed to configure pwm capture
   Pulse capture not supported, trying period capture
   :bbk:`E: PWM capture only supported on first two channels`
   E: failed to configure pwm capture
   :brd:`Assertion failed` at WEST_TOPDIR/zephyr/tests/drivers/pwm/pwm_loopback/src/test_pwm_loopback.c:183: :byl:`test_capture_timeout: (err not equal to -EAGAIN)`
   pwm capture did not timeout (err -134)
   :brd:`FAIL` - test_capture_timeout in 0.37 seconds
   ===================================================================
   START - test_continuous_capture
   :brd:`Assertion failed` at WEST_TOPDIR/zephyr/tests/drivers/pwm/pwm_loopback/src/test_pwm_loopback.c:243: :byl:`test_continuous_capture: (err not equal to 0)`
   :bbk:`failed to set pwm output (err -134)`
   :brd:`FAIL` - test_continuous_capture in 0.17 seconds
   ===================================================================
   START - test_capture_busy
   :bbk:`E: PWM capture only supported on first two channels`
   Pulse capture not supported, trying period capture
   :bbk:`E: PWM capture only supported on first two channels`
   :brd:`Assertion failed` at WEST_TOPDIR/zephyr/tests/drivers/pwm/pwm_loopback/src/test_pwm_loopback.c:324: :byl:`test_capture_busy: (err not equal to 0)`
   failed to configure pwm input (err -134)
   :brd:`FAIL` - test_capture_busy in 0.31 seconds
   ===================================================================
   TESTSUITE pwm_loopback_test failed.
   ===================================================================
   :brd:`PROJECT EXECUTION FAILED`
