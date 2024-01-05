.. _mimxrt1010_evk-extensions:

NXP MIMXRT1010-EVK
##################

Overview
********

This is a set of Bridle's extension to the original Zephyr upstream board
:ref:`zephyr:mimxrt1010_evk` with some adaptions and improvement on
Kconfig and Devicetree level.

List of extensions
******************

.. rubric:: Kconfig

- :bbl:`activate` self powered USB explicitly and set the maximum of
  electrical current consumption to :bbl:`0㎃`:

  - :kconfig:option:`CONFIG_USB_SELF_POWERED`
  - :kconfig:option:`CONFIG_USB_MAX_POWER`

  .. list-table::
     :align: left
     :width: 25%
     :widths: 100

     * - .. rubric:: NXP MIMXRT1010-EVK

     * - .. literalinclude:: ../mimxrt1010_evk.conf
            :caption: mimxrt1010_evk.conf
            :language: cfg
            :encoding: ISO-8859-1
            :start-at: CONFIG_USB_SELF_POWERED
            :end-at: CONFIG_USB_MAX_POWER

.. rubric:: Devicetree

- overwrite the Arduino UNO R3 specific edge connecor binding:

  - :devicetree:`&arduino_header {...};`

- enable ARM Cortex-M Data Cache (DTCM) with Zephyr chosen entry:

  - :devicetree:`/ { chosen { zephyr,dtcm = &dtcm; }; };`

- add a :dtcompatible:`zephyr,flash-disk` node linked to the
  :devicetree:`partition = <&storage_partition>;` with the hard defined
  mass storage disk name :devicetree:`disk-name = "NAND";` – also set
  the mass storage disk name hard on Kconfig level by a new board config
  file with :kconfig:option:`CONFIG_MASS_STORAGE_DISK_NAME`

.. note::

   On :ref:`zephyr:mimxrt1010_evk` pin D4 (GPIO), D5 (GPIO/PWM), and
   D9 (GPIO/PWM) are disconnected in default and can be closed optionally.
   With this GPIO map overwrites the resistors R793, R795 and R800 must be
   fitted for proper use. But keep in mind that the signals are already
   connected to other on-board header for the NXP special motor driver
   add-on bard.
