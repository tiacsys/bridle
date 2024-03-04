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

         west twister \
              --verbose --jobs 4 --inline-logs \
              --enable-size-report --platform-reports \
              --device-testing --hardware-map map.yaml \
              --alt-config-root bridle/zephyr/alt-config \
              --testsuite-root zephyr/tests --tag entropy

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1569/1570 tiac_magpie               tests/drivers/entropy/api/drivers.entropy.psa_crypto :byl:`SKIPPED` (runtime filter)
         INFO    - 1570/1570 tiac_magpie               tests/drivers/entropy/api/drivers.entropy          :bgn:`PASSED` (device: DT04BNT1, 2.463s)

         INFO    - 1782 test scenarios (1570 test instances) selected, 1569 configurations skipped (1568 by static filter, 1 at runtime).
         INFO    - :bgn:`1 of 1570` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1569` skipped with :bbk:`0` warnings in :bbk:`27.10 seconds`
         INFO    - In total 1 test cases were executed, 10957 skipped on 1 out of total 638 platforms (0.16%)
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

         west twister \
              --verbose --jobs 4 --inline-logs \
              --enable-size-report --platform-reports \
              --device-testing --hardware-map map.yaml \
              --alt-config-root bridle/zephyr/alt-config \
              --testsuite-root zephyr/tests --tag random

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1566/1570 tiac_magpie               tests/crypto/rand32/drivers.rand32.random_psa_crypto :byl:`SKIPPED` (runtime filter)
         INFO    - 1567/1570 tiac_magpie               tests/crypto/rand32/crypto.rand32.random_sw_systimer :bgn:`PASSED` (device: DT04BNT1, 7.116s)
         INFO    - 1568/1570 tiac_magpie               tests/crypto/rand32/crypto.rand32                  :bgn:`PASSED` (device: DT04BNT1, 2.497s)
         INFO    - 1569/1570 tiac_magpie               tests/crypto/rand32/crypto.rand32.random_ctr_drbg  :bgn:`PASSED` (device: DT04BNT1, 2.509s)
         INFO    - 1570/1570 tiac_magpie               tests/crypto/rand32/crypto.rand32.random_hw_xoshiro :bgn:`PASSED` (device: DT04BNT1, 2.489s)

         INFO    - 1782 test scenarios (1570 test instances) selected, 1566 configurations skipped (1565 by static filter, 1 at runtime).
         INFO    - :bgn:`4 of 1570` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1566` skipped with :bbk:`0` warnings in :bbk:`58.48 seconds`
         INFO    - In total 4 test cases were executed, 10954 skipped on 1 out of total 638 platforms (0.16%)
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
