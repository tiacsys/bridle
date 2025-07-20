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
         INFO    - 1/3 magpie_f777ni/stm32f777xx tests/drivers/entropy/api/drivers.entropy.virtio   :byl:`FILTERED` (runtime filter)
         INFO    - 2/3 magpie_f777ni/stm32f777xx tests/drivers/entropy/api/drivers.entropy.psa_crypto :byl:`FILTERED` (runtime filter)
         INFO    - 3/3 magpie_f777ni/stm32f777xx tests/drivers/entropy/api/drivers.entropy          :bgn:`PASSED` (device: DT04BNT1, 2.407s <zephyr>)

         INFO    - 2763 test scenarios (2539 configurations) selected, :byl:`2538` configurations filtered (2536 by static filter, 2 at runtime).
         INFO    - :bgn:`1 of 1` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`40.60 seconds`.
         INFO    - 1 of 1 executed test cases passed (100.00%) on 1 out of total 1133 platforms (0.09%).
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
         INFO    - 2/5 magpie_f777ni/stm32f777xx tests/subsys/random/rng/crypto.rng.random_sw_systimer :bgn:`PASSED` (device: DT04BNT1, 6.095s <zephyr>)
         INFO    - 3/5 magpie_f777ni/stm32f777xx tests/subsys/random/rng/crypto.rng.random_ctr_drbg :bgn:`PASSED` (device: DT04BNT1, 2.396s <zephyr>)
         INFO    - 4/5 magpie_f777ni/stm32f777xx tests/subsys/random/rng/crypto.rng                 :bgn:`PASSED` (device: DT04BNT1, 2.408s <zephyr>)
         INFO    - 5/5 magpie_f777ni/stm32f777xx tests/subsys/random/rng/crypto.rng.random_hw_xoshiro :bgn:`PASSED` (device: DT04BNT1, 2.430s <zephyr>)

         INFO    - 2763 test scenarios (2539 configurations) selected, :byl:`2535` configurations filtered (2534 by static filter, 1 at runtime).
         INFO    - :bgn:`4 of 4` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`82.03 seconds`.
         INFO    - 4 of 4 executed test cases passed (100.00%) on 1 out of total 1133 platforms (0.09%).
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
