.. _nucleo_f401re_board-extensions:

Nucleo F401RE (BBE)
###################

Overview
********

This is a set of Bridle's board extensions (BBE) to the original Zephyr
upstream board |zephyr:board:nucleo_f401re| with some adaptions and
improvement on Twister and Devicetree level.

List of extensions
******************

.. rubric:: Board YAML

- add the missing features that this board supports and
  that Twister tests might depends on:

  - :code:`arduino_serial`

.. rubric:: Devicetree

- set default entries for ``model`` and ``compatible`` of the boards:

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: ST Nucleo F401RE

     * - .. literalinclude:: ../nucleo_f401re_bbe.dts
            :caption: nucleo_f401re_bbe.dts
            :language: DTS
            :encoding: ISO-8859-1
            :prepend: / {
            :start-at: model
            :end-at: compatible
            :append: };

- add the missing Arduino UNO R3 specific interface labels:

  - :dts:`arduino_serial: &usart2 {};`

.. note::

   On |zephyr:board:nucleo_f401re| pin D0 (RX) and D1 (TX) should be
   disconnected from the on-board STLinx/V2; open the solder bridges SB13 (RX)
   and SB14 (TX). For more details, see schematic MB1136-C05 on sheet 4 and
   manual UM1724 section 6.8 on page 25 and table 10 on page 27.
