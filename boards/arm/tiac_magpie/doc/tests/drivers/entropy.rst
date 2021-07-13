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
             --testcase-root zephyr/tests/drivers/entropy

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
         INFO    - 1/1 tiac_magpie               tests/drivers/entropy/api/drivers.entropy          :bgn:`PASSED` (device 4.012s)

         INFO    - :bgn:`1 of 1` test configurations passed (100.00%), :bbk:`0` failed, :byl:`0` skipped with :bbk:`0` warnings in :bbk:`27.33 seconds`
         INFO    - In total 1 test cases were executed, 0 skipped on 1 out of total 370 platforms (0.27%)
         INFO    - :bgn:`1` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         1 \|

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
             --testcase-root zephyr/tests/crypto/rand32

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
         INFO    - 1/4 tiac_magpie               tests/crypto/rand32/crypto.rand32                  :bgn:`PASSED` (device 4.360s)
         INFO    - 2/4 tiac_magpie               tests/crypto/rand32/crypto.rand32.random_hw_xoroshiro :bgn:`PASSED` (device 4.356s)
         INFO    - 3/4 tiac_magpie               tests/crypto/rand32/crypto.rand32.random_ctr_drbg  :bgn:`PASSED` (device 4.239s)
         INFO    - 4/4 tiac_magpie               tests/crypto/rand32/crypto.rand32.random_sw_systimer :bgn:`PASSED` (device 4.341s)

         INFO    - :bgn:`4 of 4` test configurations passed (100.00%), :bbk:`0` failed, :byl:`0` skipped with :bbk:`0` warnings in :bbk:`49.35 seconds`
         INFO    - In total 4 test cases were executed, 0 skipped on 1 out of total 370 platforms (0.27%)
         INFO    - :bgn:`4` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board       \| ID       \|   Counter \|
         \|-------------\|----------\|-----------\|
         \| tiac_magpie \| DT04BNT1 \|         4 \|
