.. _mimxrt1060_evk-extensions:

NXP MIMXRT1060-EVK
##################

Overview
********

This is a set of Bridle's extension to the original Zephyr upstream board
:ref:`zephyr:mimxrt1060_evk` with some adaptions and improvement on
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
     :width: 75%
     :widths: 33, 33, 33

     * - .. rubric:: NXP MIMXRT1060-EVK
       - .. rubric:: NXP MIMXRT1060-EVKB
       - .. rubric:: NXP MIMXRT1060-EVK Hyper Flash

     * - .. literalinclude:: ../mimxrt1060_evk.conf
            :caption: mimxrt1060_evk.conf
            :language: cfg
            :encoding: ISO-8859-1
            :start-at: CONFIG_USB_SELF_POWERED
            :end-at: CONFIG_USB_MAX_POWER
       - .. literalinclude:: ../mimxrt1060_evkb.conf
            :caption: mimxrt1060_evkb.conf
            :language: cfg
            :encoding: ISO-8859-1
            :start-at: CONFIG_USB_SELF_POWERED
            :end-at: CONFIG_USB_MAX_POWER
       - .. literalinclude:: ../mimxrt1060_evk_hyperflash.conf
            :caption: mimxrt1060_evk_hyperflash.conf
            :language: cfg
            :encoding: ISO-8859-1
            :start-at: CONFIG_USB_SELF_POWERED
            :end-at: CONFIG_USB_MAX_POWER

.. rubric:: Devicetree

- add a :dtcompatible:`zephyr,flash-disk` node linked to the
  :devicetree:`partition = <&storage_partition>;` with the hard defined
  mass storage disk name :devicetree:`disk-name = "NAND";` – also set
  the mass storage disk name hard on Kconfig level by a new board config
  file with :kconfig:option:`CONFIG_MASS_STORAGE_DISK_NAME`
