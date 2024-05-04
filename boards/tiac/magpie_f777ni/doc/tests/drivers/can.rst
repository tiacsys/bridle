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

         west twister \
              --verbose --jobs 4 --inline-logs \
              --enable-size-report --platform-reports \
              --device-testing --hardware-map map.yaml \
              --alt-config-root bridle/zephyr/alt-config \
              --testsuite-root zephyr/tests --tag can

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
         INFO    - 1770/1780 magpie_f777ni             tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.unused :bgn:`PASSED` (device: DT04BNT1, 13.711s)
         INFO    - 1771/1780 magpie_f777ni             tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.txdl_32 :bgn:`PASSED` (device: DT04BNT1, 3.238s)
         INFO    - 1772/1780 magpie_f777ni             tests/drivers/can/api/drivers.can.api.nxp_s32_canxl.non_rx_fifo :byl:`SKIPPED` (runtime filter)
         INFO    - 1773/1780 magpie_f777ni             tests/subsys/canbus/isotp/implementation/canbus.isotp.implementation :bgn:`PASSED` (device: DT04BNT1, 18.372s)
         INFO    - 1774/1780 magpie_f777ni             tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance.fd.txdl_64 :bgn:`PASSED` (device: DT04BNT1, 4.665s)
         INFO    - 1775/1780 magpie_f777ni             tests/subsys/canbus/isotp/conformance/canbus.isotp.conformance :bgn:`PASSED` (device: DT04BNT1, 13.756s)
         INFO    - 1776/1780 magpie_f777ni             tests/drivers/can/shell/drivers.can.shell          :bgn:`PASSED` (device: DT04BNT1, 5.906s)
         INFO    - 1777/1780 magpie_f777ni             tests/drivers/can/api/drivers.can.api.rtr          :bgn:`PASSED` (device: DT04BNT1, 6.219s)
         INFO    - 1778/1780 magpie_f777ni             tests/drivers/can/api/drivers.can.api              :bgn:`PASSED` (device: DT04BNT1, 5.321s)
         INFO    - 1779/1780 magpie_f777ni             tests/net/socket/can/net.socket.can                :bgn:`PASSED` (device: DT04BNT1, 2.635s)
         INFO    - 1780/1780 magpie_f777ni             tests/drivers/can/timing/drivers.can.timing        :bgn:`PASSED` (device: DT04BNT1, 3.244s)

         INFO    - 1984 test scenarios (1780 test instances) selected, 1770 configurations skipped (1769 by static filter, 1 at runtime).
         INFO    - :bgn:`10 of 1780` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1770` skipped with 0 warnings in :bbk:`213.01 seconds`
         INFO    - In total 187 test cases were executed, 13265 skipped on 1 out of total 739 platforms (0.14%)
         INFO    - :bgn:`10` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board         \| ID       \|   Counter \|
         \|---------------\|----------\|-----------\|
         \| magpie_f777ni \| DT04BNT1 \|        10 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni...
         INFO    - Run completed
