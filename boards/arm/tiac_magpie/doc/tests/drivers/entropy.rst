.. _tiac_magpie_drivers_entropy-tests:

Entropy (Random-Number Generator)
#################################

Overview
********

See :zephyr_file:`tests/drivers/entropy`
and :zephyr_file:`tests/crypto/rand32`
for the original scope of tests, its structure and description.

.. _tiac_magpie_drivers_entropy-tests-requirements:

Requirements
************

You will need an ST-LINK/V2 debug tool adapter already connected to the
TiaC Magpie board, which has an already configured UART console connection.

Building and Running
********************

Drivers
=======

.. tabs::

   .. group-tab:: Running

      Build and run the tests on target as follows:

      .. code-block:: console

         $ west twister \
             --verbose --jobs 4 --inline-logs \
             --enable-size-report --platform-reports \
             --device-testing --hardware-map map.yaml \
             --testsuite-root zephyr/tests/drivers/entropy

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
         INFO    - 2/3 tiac_magpie               tests/drivers/entropy/api/drivers.entropy.psa_crypto :byl:`SKIPPED` (runtime filter)
         INFO    - 3/3 tiac_magpie               tests/drivers/entropy/api/drivers.entropy          :bgn:`PASSED` (device 2.357s)

         INFO    - 3 test scenarios (3 test instances) selected, 2 configurations skipped (1 by static filter, 1 at runtime).
         INFO    - :bgn:`1 of 3` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`2` skipped with :bbk:`0` warnings in :bbk:`20.45 seconds`
         INFO    - In total 1 test cases were executed, 2 skipped on 1 out of total 580 platforms (0.17%)
         INFO    - :bgn:`1` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         1 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed

Cryptography
============

.. tabs::

   .. group-tab:: Running

      Build and run the tests on target as follows:

      .. code-block:: console

         $ west twister \
             --verbose --jobs 4 --inline-logs \
             --enable-size-report --platform-reports \
             --device-testing --hardware-map map.yaml \
             --testsuite-root zephyr/tests/crypto/rand32

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
         INFO    - 1/5 tiac_magpie               tests/crypto/rand32/drivers.rand32.random_psa_crypto :byl:`SKIPPED` (runtime filter)
         INFO    - 2/5 tiac_magpie               tests/crypto/rand32/crypto.rand32.random_sw_systimer :bgn:`PASSED` (device 5.536s)
         INFO    - 3/5 tiac_magpie               tests/crypto/rand32/crypto.rand32.random_hw_xoshiro :bgn:`PASSED` (device 2.313s)
         INFO    - 4/5 tiac_magpie               tests/crypto/rand32/crypto.rand32.random_ctr_drbg  :bgn:`PASSED` (device 2.383s)
         INFO    - 5/5 tiac_magpie               tests/crypto/rand32/crypto.rand32                  :bgn:`PASSED` (device 2.417s)

         INFO    - 5 test scenarios (5 test instances) selected, 1 configurations skipped (0 by static filter, 1 at runtime).
         INFO    - :bgn:`4 of 5` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1` skipped with :bbk:`0` warnings in :bbk:`44.94 seconds`
         INFO    - In total 4 test cases were executed, 1 skipped on 1 out of total 580 platforms (0.17%)
         INFO    - :bgn:`4` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         4 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
