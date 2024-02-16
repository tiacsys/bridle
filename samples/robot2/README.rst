.. _robot_framework:

Robot Framework
###############

Overview
********

A sample how you can use the Robot Framework without Renode to run
tests on a development board.

Requirements
************

* Checkout the branch "snks/robot-twister-int" from the Zephyr
  repository in case it is not merged into main.

https://github.com/tiacsys/zephyr/tree/snks/robot-twister-int
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
    --testsuite-root bridle/samples/robot2 \
    --device-testing --device-serial /dev/ttyACM0


* On :ref:`zephyr:nucleo_f401re_board` board run the following command:

  .. code-block:: console

    west twister --verbose --inline-logs --platform nucleo_f401re \
    --testsuite-root bridle/samples/robot2 \
    --device-testing --device-serial /dev/ttyACM0


* On :ref:`zephyr:mimxrt1060_evk` or MIMXRT1060_EVKB board run the
  following command:

  .. code-block:: console

    west twister --verbose --inline-logs --west-flash --west-runner=pyocd \
    --platform mimxrt1060_evkb --testsuite-root bridle/samples/robot2 \
    --device-testing --device-serial /dev/ttyACM0

Sample output
=============

The log, report and output files from the Robot Framework can be found
in the 'twister_out' folder, e.g:

.. code-block:: console

  ls twister-out/*2023*
  twister-out/log*.html
  twister-out/output*.xml
  twister-out/report*.html
