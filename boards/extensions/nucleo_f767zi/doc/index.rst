.. _nucleo_f767zi-extensions:

ST Nucleo F767ZI
################

Overview
********

This is a set of Bridle's extension to the original Zephyr upstream board
:ref:`zephyr:nucleo_f767zi_board` with some adaptions and improvement on
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
     :width: 50%
     :widths: 100

     * - .. rubric:: ST Nucleo F767ZI

     * - .. literalinclude:: ../Kconfig.defconfig
            :caption: Kconfig.defconfig
            :language: Kconfig
            :encoding: ISO-8859-1
            :emphasize-lines: 1-2,5-6
            :start-at: config USB_SELF_POWERED
            :end-before: Workaround for not being able to have commas in macro arguments

- :brd:`change` log level and startup delay only in case of use the
  native USB device port :dtcompatible:`st,stm32-otgfs` with CDC-ACM
  UART :dtcompatible:`zephyr,cdc-acm-uart` as Zephyr console:

  - :kconfig:option:`CONFIG_USB_CDC_ACM_LOG_LEVEL_CHOICE` :=
    :kconfig:option:`CONFIG_USB_CDC_ACM_LOG_LEVEL_OFF`
  - :kconfig:option:`CONFIG_USB_DEVICE_LOG_LEVEL_CHOICE` :=
    :kconfig:option:`CONFIG_USB_DEVICE_LOG_LEVEL_ERR`
  - :kconfig:option:`CONFIG_LOG_PROCESS_THREAD_STARTUP_DELAY_MS`
  - :kconfig:option:`CONFIG_BOOT_DELAY`

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: ST Nucleo F767ZI

     * - .. literalinclude:: ../Kconfig.defconfig
            :caption: Kconfig.defconfig
            :language: Kconfig
            :encoding: ISO-8859-1
            :emphasize-lines: 3-4,16-17,22-23,28-29,33-34
            :start-at: Workaround for not being able to have commas in macro arguments
            :end-at: endif # zephyr,cdc-acm-uart

.. rubric:: Devicetree

- set default entries for ``model`` and ``compatible`` of the boards:

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: ST Nucleo F767ZI

     * - .. literalinclude:: ../nucleo_f767zi.overlay
            :caption: nucleo_f767zi.overlay
            :language: DTS
            :encoding: ISO-8859-1
            :prepend: / {
            :start-at: model
            :end-at: compatible
            :append: };
