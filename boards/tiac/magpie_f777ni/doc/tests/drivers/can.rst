.. _magpie_f777ni_drivers_can-tests:

CAN Loopback (internal)
#######################

Overview
********

See :zephyr_file:`tests/drivers/can`
for the original scope of tests, its structure and description.

.. _magpie_f777ni_drivers_can-tests-requirements:

Requirements
************

You will need an ST-LINK/V2 debug tool adapter already connected to the
TiaC Magpie board, which has an already configured UART console connection.

Building and Running
********************

.. tabs::

   .. group-tab:: Running

      Build and run the tests on target as follows:

      .. code-block:: console

         $ west twister \
                --verbose --jobs 4 --inline-logs \
                --enable-size-report --platform-reports \
                --device-testing --hardware-map map.yaml \
                --alt-config-root bridle/zephyr/alt-config/tests \
                --testsuite-root zephyr/tests --tag can

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
         INFO    -  1/11 magpie_f777ni/stm32f777xx canbus.isotp.conformance.fd.txdl_32                :bgn:`PASSED` (device: DT04BNT1, 3.355s <zephyr/gnu>)
         INFO    -  2/11 magpie_f777ni/stm32f777xx drivers.can.shell                                  :bgn:`PASSED` (device: DT04BNT1, 8.209s <zephyr/gnu>)
         INFO    -  3/11 magpie_f777ni/stm32f777xx canbus.isotp.conformance                           :bgn:`PASSED` (device: DT04BNT1, 15.367s <zephyr/gnu>)
         INFO    -  4/11 magpie_f777ni/stm32f777xx drivers.can.api.rtr                                :bgn:`PASSED` (device: DT04BNT1, 7.710s <zephyr/gnu>)
         INFO    -  5/11 magpie_f777ni/stm32f777xx canbus.isotp.implementation                        :bgn:`PASSED` (device: DT04BNT1, 19.562s <zephyr/gnu>)
         INFO    -  6/11 magpie_f777ni/stm32f777xx canbus.isotp.conformance.fd.txdl_64                :bgn:`PASSED` (device: DT04BNT1, 3.642s <zephyr/gnu>)
         INFO    -  7/11 magpie_f777ni/stm32f777xx canbus.isotp.conformance.fd.unused                 :bgn:`PASSED` (device: DT04BNT1, 14.751s <zephyr/gnu>)
         INFO    -  8/11 magpie_f777ni/stm32f777xx drivers.can.api                                    :bgn:`PASSED` (device: DT04BNT1, 9.928s <zephyr/gnu>)
         INFO    -  9/11 magpie_f777ni/stm32f777xx net.socket.can                                     :bgn:`PASSED` (device: DT04BNT1, 3.445s <zephyr/gnu>)
         INFO    - 10/11 magpie_f777ni/stm32f777xx drivers.can.timing.adj                             :bgn:`PASSED` (device: DT04BNT1, 4.721s <zephyr/gnu>)
         INFO    - 11/11 magpie_f777ni/stm32f777xx drivers.can.timing                                 :bgn:`PASSED` (device: DT04BNT1, 3.858s <zephyr/gnu>)

         INFO    - 3090 test scenarios (2888 configurations) selected, :byl:`2877` configurations filtered (:byl:`2877` by static filter, :byl:`0` at runtime).
         INFO    - :bgn:`11 of 11` executed test configurations passed (100.00%), :bbk:`0` built (not run), :brd:`0` failed, :bbk:`0` errored, with no warnings in :bbk:`293.33 seconds`.
         INFO    - 196 of 196 executed test cases passed (100.00%) on 1 out of total 1511 platforms (0.07%).
         INFO    - 84 selected test cases not executed: 84 skipped.
         INFO    - :bgn:`11` test configurations executed on platforms, :bbl:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board                     \| ID       \|   Counter \|   Failures \|
         \|---------------------------\|----------\|-----------\|------------\|
         \| magpie_f777ni/stm32f777xx \| DT04BNT1 \|        11 \|          0 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni/stm32f777xx...
         INFO    - Writing JSON report .../twister-out/magpie_f777ni_stm32f777xx.json
         INFO    - Run completed
