.. _snippet-wdt-timing-adj:

Watchdog timing adjustments (wdt-timing-adj)
############################################

Overview
********

With this snippet, the user can create Zephyr standard watchdog drivers and API
test suites and also run them successfully. Since boards are very often designed
for high performance and thus a high CPU clock, lower watchdog speeds or higher
timeout values can no longer be set by the Zephyr API without acceptable errors.
This is also not an issue for normal operation. The test suites, however, want
to prove that this is also possible in principle. However, this requires an
individual board-specific reduction of the CPU clock.

How to add support of a new board
*********************************

* add board dts overlay to this snippet which overwrites CPU clock setup nodes;
* add correct CPU clock setup ready for the Zephyr standard watchdog test suites

Programming
***********

Correct snippet designation must be entered when you invoke ``west build``.
For example:

.. code-block:: console

   west build -b magpie_f777ni \
              -d build/magpie_f777ni \
              -p always \
              -S wdt-timing-adj \
              zephyr/tests/drivers/watchdog/wdt_basic_api \
              -- -DDTC_OVERLAY_FILE="boards/stm32_wwdg.overlay"
   west flash -d build/magpie_f777ni

Testing
*******

Correct snippet designation must be entered when you invoke ``west twister``,
either directly on the command line or as an alternative test specification.
For example:

.. code-block:: console

   west twister --device-testing \
                --hardware-map map_magpie_f777ni.yaml \
                --alt-config-root bridle/zephyr/alt-config/tests/drivers/watchdog/wdt_basic_api \
                --testsuite-root zephyr/tests/drivers/watchdog/wdt_basic_api
