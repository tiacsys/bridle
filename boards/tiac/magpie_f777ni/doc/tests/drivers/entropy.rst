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
              --alt-config-root bridle/zephyr/alt-config \
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
         INFO    - 1779/1780 magpie_f777ni             tests/drivers/entropy/api/drivers.entropy.psa_crypto :byl:`SKIPPED` (runtime filter)
         INFO    - 1780/1780 magpie_f777ni             tests/drivers/entropy/api/drivers.entropy          :bgn:`PASSED` (device: DT04BNT1, 2.490s)

         INFO    - 1984 test scenarios (1780 test instances) selected, 1779 configurations skipped (1778 by static filter, 1 at runtime).
         INFO    - :bgn:`1 of 1780` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1779` skipped with :bbk:`0` warnings in :bbk:`39.11 seconds`
         INFO    - In total 1 test cases were executed, 13447 skipped on 1 out of total 739 platforms (0.14%)
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
              --alt-config-root bridle/zephyr/alt-config \
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
         INFO    - 1776/1780 magpie_f777ni             tests/crypto/rand32/drivers.rand32.random_psa_crypto :byl:`SKIPPED` (runtime filter)
         INFO    - 1777/1780 magpie_f777ni             tests/crypto/rand32/crypto.rand32.random_sw_systimer :bgn:`PASSED` (device: DT04BNT1, 2.939s)
         INFO    - 1778/1780 magpie_f777ni             tests/crypto/rand32/crypto.rand32.random_hw_xoshiro :bgn:`PASSED` (device: DT04BNT1, 2.617s)
         INFO    - 1779/1780 magpie_f777ni             tests/crypto/rand32/crypto.rand32.random_ctr_drbg  :bgn:`PASSED` (device: DT04BNT1, 2.557s)
         INFO    - 1780/1780 magpie_f777ni             tests/crypto/rand32/crypto.rand32                  :bgn:`PASSED` (device: DT04BNT1, 2.654s)

         INFO    - 1984 test scenarios (1780 test instances) selected, 1776 configurations skipped (1775 by static filter, 1 at runtime).
         INFO    - :bgn:`4 of 1780` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1776` skipped with :bbk:`0` warnings in :bbk:`77.34 seconds`
         INFO    - In total 4 test cases were executed, 13444 skipped on 1 out of total 739 platforms (0.14%)
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
