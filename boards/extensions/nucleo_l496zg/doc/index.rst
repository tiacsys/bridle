.. _nucleo_l496zg_board-extensions:

ST Nucleo L496ZG
################

Overview
********

This is a set of Bridle's extension to the original Zephyr upstream board
|zephyr:board:nucleo_l496zg| with some adaptions and improvement on
Devicetree level.

List of extensions
******************

- fix the wrong Arduino UNO R3 specific interface labels:

  - :dts:`arduino_serial: &usart3 {};`

.. note::

   On |zephyr:board:nucleo_l496zg| pin D0 (RX) and D1 (TX) are
   connected to **USART3** and not to *LPUART1* as set in the origin
   upstream Devicetree. For more details, see schematic MB1312-A03 on
   sheet 5 and manual UM2179 table 11 on page 40.
