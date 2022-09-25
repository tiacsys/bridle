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

         $ ./zephyr/scripts/twister \
             --verbose --jobs 4 --inline-logs \
             --enable-size-report --platform-reports \
             --device-testing --hardware-map map.yaml \
             --board-root bridle/boards \
             --testsuite-root zephyr/tests/drivers/entropy

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - 2 test scenarios (2 configurations) selected, 1 configurations discarded due to filters.
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 2/2 tiac_magpie               tests/drivers/entropy/api/drivers.entropy          :bgn:`PASSED` (device 3.871s)

         INFO    - :bgn:`1 of 2` test configurations passed (100.00%), :bbk:`0` failed, :byl:`1` skipped with :bbk:`0` warnings in :bbk:`21.76 seconds`
         INFO    - In total 2 test cases were executed, 0 skipped on 1 out of total 457 platforms (0.22%)
         INFO    - :bgn:`1` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         1 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Using 'zephyr' toolchain.
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

         $ ./zephyr/scripts/twister \
             --verbose --jobs 4 --inline-logs \
             --enable-size-report --platform-reports \
             --device-testing --hardware-map map.yaml \
             --board-root bridle/boards \
             --testsuite-root zephyr/tests/crypto/rand32

   .. group-tab:: Results

      You should see the following messages on host console:

      .. parsed-literal::
         :class: highlight

         Device testing on:

         \| Platform    \| ID       \| Serial device   \|
         \|-------------\|----------\|-----------------\|
         \| tiac_magpie \| DT04BNT1 \| /dev/ttyUSB0    \|

         INFO    - 4 test scenarios (4 configurations) selected, 0 configurations discarded due to filters.
         INFO    - Adding tasks to the queue...
         INFO    - Added initial list of jobs to queue
         INFO    - 1/4 tiac_magpie               tests/crypto/rand32/crypto.rand32                  :bgn:`PASSED` (device 3.885s)
         INFO    - 2/4 tiac_magpie               tests/crypto/rand32/crypto.rand32.random_sw_systimer :bgn:`PASSED` (device 4.006s)
         INFO    - 3/4 tiac_magpie               tests/crypto/rand32/crypto.rand32.random_hw_xoshiro :bgn:`PASSED` (device 3.898s)
         INFO    - 4/4 tiac_magpie               tests/crypto/rand32/crypto.rand32.random_ctr_drbg  :bgn:`PASSED` (device 3.798s)

         INFO    - :bgn:`4 of 4` test configurations passed (100.00%), :bbk:`0` failed, :byl:`0` skipped with :bbk:`0` warnings in :bbk:`36.11 seconds`
         INFO    - In total 4 test cases were executed, 0 skipped on 1 out of total 457 platforms (0.22%)
         INFO    - :bgn:`4` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         4 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Using 'zephyr' toolchain.
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for tiac_magpie...
         INFO    - Run completed
