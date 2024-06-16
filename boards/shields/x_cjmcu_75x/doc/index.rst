.. _x_cjmcu_75x_shield:

CJMCU-75x Interconnection Shield
################################

Overview
********

This shield is less a plug-on module in the conventional sense than more
a wiring for interconnection of certain signals from a board down to the
:ref:`sc16is75x_bb_shield`.

Requirements
************

This shield requires a board which provides a configuration that allows:

- two GPIO lines, 1st for reset output and 2nd for optional interrupt input
- one SPI interface, COPI for output and CIPO for input
- one I2C interfaces, SDA and SCL for peripheral

Supported variations
********************

The table below suggests shield variation often found on many development
boards:

+--------------------+--------------------------+-----------+
| Connector Standard | Shield Designation       | Variation |
+====================+==========================+===========+
| Without standard   | **needs board adaption** |     1     |
+--------------------+--------------------------+-----------+
| |Arduino UNO R3|   | |arduino_to_cjmcu_if|    |     2     |
+--------------------+--------------------------+-----------+
| |MikroBus|         | (:yl:`not yet, planned`) |     3     |
+--------------------+--------------------------+-----------+

.. |arduino_to_cjmcu_if| replace::
   :bridle_file:`boards/arduino_to_cjmcu_if.dtsi
   <boards/shields/x_cjmcu_75x/boards/arduino_to_cjmcu_if.dtsi>`

Arduino Uno (R3) headers
========================

The connector standard |Arduino UNO R3| can be used with a variety of
development boards that provide it. Any of these boards must be added
separately. For example, the file |nucleo_f746zg_overlay| exists for
the :ref:`zephyr:nucleo_f746zg_board` and simply integrates the
generally valid interface |arduino_to_cjmcu_if|:

.. literalinclude:: ../boards/nucleo_f746zg.overlay
   :caption: nucleo_f746zg.overlay (as an example)
   :language: DTS
   :encoding: ISO-8859-1
   :emphasize-lines: 1
   :linenos:
   :start-at: arduino_to_cjmcu_if.dtsi
   :end-at: arduino_to_cjmcu_if.dtsi

.. |nucleo_f746zg_overlay| replace::
   :bridle_file:`boards/nucleo_f746zg.overlay
   <boards/shields/x_cjmcu_75x/boards/nucleo_f746zg.overlay>`

.. rubric:: Serial Bus and GPIO Mapping

.. list-table::
   :class: longtable
   :align: center
   :widths: 50, 50
   :header-rows: 1

   * - I2C Host Interface
     - SPI Host Interface
   * - .. literalinclude:: ../boards/arduino_to_cjmcu_if.dtsi
          :caption: arduino_to_cjmcu_if.dtsi: I2C serial bus mapping
          :language: DTS
          :encoding: ISO-8859-1
          :emphasize-lines: 1
          :linenos:
          :start-at: cjmcu_i2c
          :end-at: cjmcu_i2c
       .. literalinclude:: ../boards/arduino_to_cjmcu_if.dtsi
          :caption: arduino_to_cjmcu_if.dtsi: I2C host interface GPIO mapping
          :language: DTS
          :encoding: ISO-8859-1
          :emphasize-lines: 2,7,8,10,14
          :linenos:
          :prepend: / {
          :start-at: cjmcu_hif_i2c
          :end-at: };
          :append: };
     - .. literalinclude:: ../boards/arduino_to_cjmcu_if.dtsi
          :caption: arduino_to_cjmcu_if.dtsi: SPI serial bus mapping
          :language: DTS
          :encoding: ISO-8859-1
          :emphasize-lines: 1
          :linenos:
          :start-at: cjmcu_spi
          :end-at: cjmcu_spi
       .. literalinclude:: ../boards/arduino_to_cjmcu_if.dtsi
          :caption: arduino_to_cjmcu_if.dtsi: SPI host interface GPIO mapping
          :language: DTS
          :encoding: ISO-8859-1
          :emphasize-lines: 2,8,10,11,12,13,14
          :linenos:
          :prepend: / {
          :start-at: cjmcu_hif_spi
          :end-at: };
          :append: };

.. rubric:: Interconnection

.. include:: arduino_to_cjmcu_hif_map.rsti

Sample Prototypes
-----------------

.. tabs::

   .. group-tab:: CJMCU-750 (SC16IS750) on I2C bus

      * Fritzing project file: :download:`TCS-750-i2c-ard.fzz`

      .. list-table::
         :align: center
         :width: 100%
         :widths: 55, 45

         * - .. rubric:: Schematic (not for production)
           - .. rubric:: Prototype and Printed Circuit Board

         * - .. image:: img/TCS-750-i2c-ard_schem.png
                :align: center
                :alt: TCS-750-i2c-ard Schematic
           - .. image:: img/TCS-750-i2c-ard_bb.png
                :align: center
                :alt: TCS-750-i2c-ard Prototype
             .. image:: img/TCS-750-i2c-ard_pcb.png
                :align: center
                :alt: TCS-750-i2c-ard PCB

   .. group-tab:: CJMCU-750 (SC16IS750) on SPI bus

      * Fritzing project file: :download:`TCS-750-spi-ard.fzz`

      .. list-table::
         :align: center
         :width: 100%
         :widths: 55, 45

         * - .. rubric:: Schematic (not for production)
           - .. rubric:: Prototype and Printed Circuit Board

         * - .. image:: img/TCS-750-spi-ard_schem.png
                :align: center
                :alt: TCS-750-spi-ard Schematic
           - .. image:: img/TCS-750-spi-ard_bb.png
                :align: center
                :alt: TCS-750-spi-ard Prototype
             .. image:: img/TCS-750-spi-ard_pcb.png
                :align: center
                :alt: TCS-750-spi-ard PCB

Mikro BUS headers
=================

.. note::

   The connector standard |MikroBus| is not yet supported
   and has yet to be defined.
