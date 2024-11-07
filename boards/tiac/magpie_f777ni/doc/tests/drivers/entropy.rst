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

         $ west twister \
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

         \| Platform                  \| ID       \| Serial device   \|
         \|---------------------------\|----------\|-----------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1/2 magpie_f777ni/stm32f777xx tests/drivers/entropy/api/drivers.entropy.psa_crypto :byl:`FILTERED` (runtime filter)
         INFO    - 2/2 magpie_f777ni/stm32f777xx tests/drivers/entropy/api/drivers.entropy          :bgn:`PASSED` (device: DT04BNT1, 2.347s)

         INFO    - 2294 test scenarios (2077 test instances) selected, :byl:`2076` configurations filtered (2075 by static filter, 1 at runtime).
         INFO    - :bgn:`1 of 1` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`33.18 seconds`.
         INFO    - 1 of 1 executed test cases passed (100.00%) on 1 out of total 876 platforms (0.11%).
         INFO    - 16091 selected test cases not executed: 1 skipped, 16090 filtered.
         INFO    - :bgn:`1` test configurations executed on platforms, :bbl:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board                     \| ID       \|   Counter \|   Failures \|
         \|---------------------------\|----------\|-----------\|------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \|         1 \|          0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni/stm32f777xx...
         INFO    - Writing JSON report .../twister-out/magpie_f777ni_stm32f777xx.json
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
                --alt-config-root bridle/zephyr/alt-config/tests \
                --testsuite-root zephyr/tests --tag random

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight-console notranslate

         Device testing on:

         \| Platform                  \| ID       \| Serial device   \|
         \|---------------------------\|----------\|-----------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - JOBS: 4
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1/5 magpie_f777ni/stm32f777xx tests/subsys/random/rng/drivers.rng.random_psa_crypto :byl:`FILTERED` (runtime filter)
         INFO    - 2/5 magpie_f777ni/stm32f777xx tests/subsys/random/rng/crypto.rng.random_sw_systimer :bgn:`PASSED` (device: DT04BNT1, 5.552s)
         INFO    - 3/5 magpie_f777ni/stm32f777xx tests/subsys/random/rng/crypto.rng.random_hw_xoshiro :bgn:`PASSED` (device: DT04BNT1, 2.369s)
         INFO    - 4/5 magpie_f777ni/stm32f777xx tests/subsys/random/rng/crypto.rng                 :bgn:`PASSED` (device: DT04BNT1, 2.381s)
         INFO    - 5/5 magpie_f777ni/stm32f777xx tests/subsys/random/rng/crypto.rng.random_ctr_drbg :bgn:`PASSED` (device: DT04BNT1, 2.419s)

         INFO    - 2294 test scenarios (2077 test instances) selected, :byl:`2073` configurations filtered (2072 by static filter, 1 at runtime).
         INFO    - :bgn:`4 of 4` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`67.10 seconds`.
         INFO    - 4 of 4 executed test cases passed (100.00%) on 1 out of total 876 platforms (0.11%).
         INFO    - 16088 selected test cases not executed: 1 skipped, 16087 filtered.
         INFO    - :bgn:`4` test configurations executed on platforms, :bbl:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board                     \| ID       \|   Counter \|   Failures \|
         \|---------------------------\|----------\|-----------\|------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \|         4 \|          0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni/stm32f777xx...
         INFO    - Writing JSON report .../twister-out/magpie_f777ni_stm32f777xx.json
         INFO    - Run completed
