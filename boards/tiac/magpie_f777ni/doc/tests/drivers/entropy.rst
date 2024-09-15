.. _magpie_f777ni_drivers_entropy-tests:

Entropy (Random-Number Generator)
#################################

Overview
********

See :zephyr_file:`tests/drivers/entropy`
and :zephyr_file:`tests/crypto/rand32`
for the original scope of tests, its structure and description.

.. _magpie_f777ni_drivers_entropy-tests-requirements:

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
              --alt-config-root bridle/zephyr/alt-config/tests \
              --testsuite-root zephyr/tests --tag entropy

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight-console notranslate

         Device testing on:

         \| Platform      \| ID       \| Serial device   \|
         \|---------------\|----------\|-----------------\|
         \| magpie_f777ni \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1886/1887 magpie_f777ni             tests/drivers/entropy/api/drivers.entropy.psa_crypto :byl:`SKIPPED` (runtime filter)
         INFO    - 1887/1887 magpie_f777ni             tests/drivers/entropy/api/drivers.entropy          :bgn:`PASSED` (device: DT04BNT1, 2.373s)

         INFO    - 2092 test scenarios (1887 test instances) selected, 1886 configurations skipped (1885 by static filter, 1 at runtime).
         INFO    - :bgn:`1 of 1887` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1886` skipped with :bbk:`0` warnings in :bbk:`31.69 seconds`
         INFO    - In total 1 test cases were executed, 15001 skipped on 1 out of total 1 platforms (100.00%)
         INFO    - :bgn:`1` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board         \| ID       \|   Counter \|
         \|---------------\|----------\|-----------\|
         \| magpie_f777ni \| DT04BNT1 \|         1 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni...
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
              --alt-config-root bridle/zephyr/alt-config/tests \
              --testsuite-root zephyr/tests --tag random

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight-console notranslate

         Device testing on:

         \| Platform      \| ID       \| Serial device   \|
         \|---------------\|----------\|-----------------\|
         \| magpie_f777ni \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1883/1887 magpie_f777ni             tests/subsys/random/rng/drivers.rng.random_psa_crypto :byl:`SKIPPED` (runtime filter)
         INFO    - 1884/1887 magpie_f777ni             tests/subsys/random/rng/crypto.rng.random_sw_systimer :bgn:`PASSED` (device: DT04BNT1, 5.713s)
         INFO    - 1885/1887 magpie_f777ni             tests/subsys/random/rng/crypto.rng.random_ctr_drbg :bgn:`PASSED` (device: DT04BNT1, 2.411s)
         INFO    - 1886/1887 magpie_f777ni             tests/subsys/random/rng/crypto.rng                 :bgn:`PASSED` (device: DT04BNT1, 2.402s)
         INFO    - 1887/1887 magpie_f777ni             tests/subsys/random/rng/crypto.rng.random_hw_xoshiro :bgn:`PASSED` (device: DT04BNT1, 2.403s)

         INFO    - 2092 test scenarios (1887 test instances) selected, 1883 configurations skipped (1882 by static filter, 1 at runtime).
         INFO    - :bgn:`4 of 1887` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1883` skipped with :bbk:`0` warnings in :bbk:`64.87 seconds`
         INFO    - In total 4 test cases were executed, 14998 skipped on 1 out of total 1 platforms (100.00%)
         INFO    - :bgn:`4` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board         \| ID       \|   Counter \|
         \|---------------\|----------\|-----------\|
         \| magpie_f777ni \| DT04BNT1 \|         4 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni...
         INFO    - Run completed
