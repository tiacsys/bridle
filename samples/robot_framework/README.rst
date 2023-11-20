.. _robot_framework:

Robot Framework
###############

Overview
********

A sample how you can use the Robot Framework to run tests on a development
board using harness "pytest".

Requirements
************

* Install the Robot Framework using pip:

  .. code-block:: console

    pip install robotframework

* One of the following development boards:

  * :ref:`zephyr:nucleo_f303re_board` (NUCLEO-F303RE)
  * :ref:`zephyr:nucleo_f401re_board` (NUCLEO-F401RE)
  * :ref:`zephyr:mimxrt1060_evk`

Building and Running
********************

* On :ref:`zephyr:nucleo_f303re_board` board run the following command:

  .. code-block:: console

    west twister --verbose --inline-logs --platform nucleo_f303re \
    --testsuite-root bridle/samples/robot_framework \
    --device-testing --device-serial /dev/ttyACM0


* On :ref:`zephyr:nucleo_f401re_board` board run the following command:

  .. code-block:: console

    west twister --verbose --inline-logs --platform nucleo_f401re \
    --testsuite-root bridle/samples/robot_framework \
    --device-testing --device-serial /dev/ttyACM0


* On :ref:`zephyr:mimxrt1060_evkb_board` board run the following command:

  .. code-block:: console

    west twister --verbose --inline-logs --platform mimxrt1060_evkb \
    --testsuite-root bridle/samples/robot_framework \
    --device-testing --device-serial /dev/ttyACM0

Sample Output
=============

The log, report and output files from the Robot Framework can be found
in the 'twister_out' folder, e.g:

.. code-block:: console

  ls twister-out/*2023*
  twister-out/log-20231120-162624.html
  twister-out/output-20231120-162624.xml
  twister-out/report-20231120-162624.html

  .. test-results:: twister-out/output-20231121-135736.xml
