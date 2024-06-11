.. _nxp_sc18is604_evb_shield:

NXP SC18IS604-EVB
#################

.. toctree::

.. image:: ./img/SC18IS604-EVB-Top.jpg
   :align: center

An evaluation kit for the NXP SC18IS604 SPI to I2C/GPIO bridge. Apart from the
SC18IS604 it features five LEDs connected to the GPIO pins, a PCA9533 PWM
controller connected to the outgoing I2C bus which controls 4 additional LEDs,
and a 24LC02B EEPROM, also on the outgoing I2C bus.

Connecting the shield
*********************

Since the shield does not use a standard 'plug-on' design, it must be manually
wired to the correct signals on the host board. This wiring is represented by an
additional 'shield', depending on the signal routing.

Arduino Uno (R3) Connector
==========================

If the host board has an |Arduino UNO R3| connector available, its signals can
be used to connect the shield. The :ref:`x_nxp_sc18is604_evb_via_arduino_shield`
contains the required signal definitions for this configuration. To use this (or
another) connector shield, include it in the shield list for your build:

.. zephyr-app-commands::
   :zephyr-app: <your-application>
   :board: <your_board>
   :shield: "x_nxp_sc18is604_evb_via_arduino; nxp_sc18is604_evb"
   :goals: build
   :compact:
