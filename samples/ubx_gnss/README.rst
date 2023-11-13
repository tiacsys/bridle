.. _ubx_gnss_sample:

Ubxlib GNSS Sample
##################

Overview
********

A sample application demonstrating how to integrate a u-blox GNSS device into a
zephyr application.

Requirements
************

A u-blox GNSS device must be connected via UART, and a devicetree alias
`ubxlib-uart0` must exist and point towards this UART port. To fulfil this
requirement, you can add a simple devicetree overlay for your board such as

.. code-block:: devicetree

    / {
        aliases {
            ubxlib-uart0 = &usart3;
        };
    };

Building and Running
********************

ST Nucleo L496ZG
================

.. zephyr-app-commands::
   :zephyr-app: bridle/samples/ubx_gnss
   :board: nucleo_l496zg
   :build-dir: nucleo_l496zg-ubx_gnss
   :west-args: -p
   :goals: flash
   :compact:
