.. _mimxrt1010_evk-extensions:

NXP MIMXRT1010-EVK
##################

Overview
********

This is a set of Bridle's extension to the original Zephyr upstream board
:ref:`zephyr:mimxrt1010_evk` with some adaptions and improvement on
Devicetree level.

List of extensions
******************

- overwrite the Arduino specific edge connecor binding:

  - :code:`&arduino_header {...};`

.. note::

   On :ref:`zephyr:mimxrt1010_evk` pin D4 (GPIO), D5 (GPIO/PWM), and
   D9 (GPIO/PWM) are disconnected in default and can be closed optionally.
   With this GPIO map overwrites the resistors R793, R795 and R800 must be
   fitted for proper use. But keep in mind that the signals are already
   connected to other on-board header for the NXP special motor driver
   add-on bard.