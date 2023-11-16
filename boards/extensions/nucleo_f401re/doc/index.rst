.. _nucleo_f401re_board-extensions:

ST Nucleo F401RE
################

Overview
********

This is a set of Bridle's extension to the original Zephyr upstream board
:ref:`zephyr:nucleo_f401re_board` with some adaptions and improvement on
Devicetree level.

List of extensions
******************

- add the missing Arduino specific interface labels:

  - :code:`arduino_serial: &usart2 {};`

.. note::

   On :ref:`zephyr:nucleo_f401re_board` pin D0 (RX) and D1 (TX) should be
   disconnected from the on-board STLinx/V2; open the solder bridges SB13 (RX)
   and SB14 (TX). For more details, see schematic MB1136-C05 on sheet 4 and
   manual UM1724 section 6.8 on page 25 and table 10 on page 27.
