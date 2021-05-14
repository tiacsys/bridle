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

         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1/2 tiac_magpie               tests/drivers/pwm/pwm_api/drivers.pwm              :bgn:`PASSED` (device 11.436s)
         INFO    - 2/2 tiac_magpie               tests/drivers/pwm/pwm_loopback/drivers.pwm.loopback :brd:`FAILED` Timeout (device 63.270s)

         INFO    - :bgn:`1 of 2` test configurations passed (100.00%), :bbk:`1` failed, :byl:`0` skipped with :bbk:`0` warnings in :bbk:`105.09 seconds`
         INFO    - In total 11 test cases were executed, 5 skipped on 1 out of total 330 platforms (0.30%)
         INFO    - :bgn:`2` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         2 \|

Open Issues
***********

.. parsed-literal::
   :class: highlight

   Running test suite pwm_loopback_test
   ===================================================================
   START - test_pulse_capture
   Testing PWM capture @ 15000000/100000000 nsec
   E: :brd:`syscall z_vrfy_pwm_pin_capture_cycles failed check:` :byl:`Operation` :brd:`pin_configure_capture not defined` :byl:`for driver instance 0x8010514`
   E: r0/a1:  0x00000000  r1/a2:  0x00000000  r2/a3:  0x00000000
   E: r3/a4:  0x00000000 r12/ip:  0x00000000 r14/lr:  0x00000000
   E:  xpsr:  0x00000000
   E: Faulting instruction address (r15/pc): 0x00000000
   E: >>> :brd:`ZEPHYR FATAL ERROR 3:` :byl:`Kernel oops on CPU 0`
   E: Current thread: 0x20020100 (unknown)
   E: :brd:`Halting system`
