.. _snippet-can-timing-adj:

CAN timing adjustments (can-timing-adj)
#######################################

Overview
********

With this snippet, the user can create Zephyr standard CAN drivers and API test
suites and also run them successfully. Since boards are very often designed for
high performance and thus a high CPU clock, lower CAN speeds can no longer be
set by the Zephyr API without acceptable errors. This is also not an issue for
normal operation. The test suites, however, want to prove that this is also
possible in principle. However, this requires an individual board-specific
reduction of the CPU clock.

How to add support of a new board
*********************************

* add board dts overlay to this snippet which overwrites CPU clock setup nodes;
* add correct CPU clock setup ready for the Zephyr standard CAN test suites

Programming
***********

Correct snippet designation must be entered when you invoke ``west build``.
For example:

   .. zephyr-app-commands::
      :app: zephyr/tests/drivers/can/timing
      :build-dir: magpie_f777ni
      :board: magpie_f777ni
      :snippets: "can-timing-adj"
      :west-args: -p always
      :goals: flash
      :compact:

Testing
*******

Correct snippet designation must be entered when you invoke ``west twister``.
For example:

   .. code-block:: console

      west twister --device-testing \
                   --hardware-map map_magpie_f777ni.yaml \
                   --extra-args SNIPPET="can-timing-adj" \
                   --testsuite-root zephyr/tests/drivers/can/timing
