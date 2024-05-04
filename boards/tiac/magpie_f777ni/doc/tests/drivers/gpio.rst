.. _magpie_f777ni_drivers_gpio-tests:

GPIO Loopback
#############

Overview
********

See :zephyr_file:`tests/drivers/gpio`
for the original scope of tests, its structure and description.

.. _magpie_f777ni_drivers_gpio-tests-requirements:

Requirements
************

You will need an ST-LINK/V2 debug tool adapter already connected to the
TiaC Magpie board, which has an already configured UART console connection.

On the TiaC MAGPIE pin headers the following GPIO pins must be connected.

.. image:: loopback_test_GPIO.svg
   :alt: TiaC MAGPIE Pin Header GPIO Loopback Wiring
   :align: center

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
              --extra-args SHIELD="loopback_test_tmph" \
              --alt-config-root bridle/zephyr/alt-config \
              --testsuite-root zephyr/tests --tag gpio

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
         INFO    - 1777/1780 magpie_f777ni             tests/drivers/gpio/gpio_nrf/drivers.gpio.gpio_nrf  :byl:`SKIPPED` (runtime filter)
         INFO    - 1778/1780 magpie_f777ni             tests/drivers/gpio/gpio_get_direction/drivers.gpio.get_direction :bgn:`PASSED` (device: DT04BNT1, 2.547s)
         INFO    - 1779/1780 magpie_f777ni             tests/drivers/gpio/gpio_api_1pin/drivers.gpio.1pin :bgn:`PASSED` (device: DT04BNT1, 9.506s)
         INFO    - 1780/1780 magpie_f777ni             tests/drivers/gpio/gpio_basic_api/drivers.gpio.2pin :bgn:`PASSED` (device: DT04BNT1, 18.049s)

         INFO    - 1984 test scenarios (1780 test instances) selected, 1777 configurations skipped (1777 by static filter, 0 at runtime).
         INFO    - :bgn:`3 of 1780` test configurations passed (100.00%), :bbk:`0` failed, :bbk:`0` errored, :byl:`1777` skipped with :bbk:`0` warnings in :bbk:`89.82 seconds`
         INFO    - In total 28 test cases were executed, 13420 skipped on 1 out of total 739 platforms (0.14%)
         INFO    - :bgn:`3` test configurations executed on platforms, :brd:`0` test configurations were only built.

         Hardware distribution summary:

         \| Board         \| ID       \|   Counter \|
         \|---------------\|----------\|-----------\|
         \| magpie_f777ni \| DT04BNT1 \|         3 \|

         INFO    - Saving reports...
         INFO    - Writing JSON report .../twister-out/twister.json
         INFO    - Writing xunit report .../twister-out/twister.xml...
         INFO    - Writing xunit report .../twister-out/twister_report.xml...
         INFO    - Writing target report for magpie_f777ni...
         INFO    - Run completed
