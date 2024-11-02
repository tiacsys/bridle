.. _seeeduino_xiao-extensions:

Seeeduino XIAO
##############

Overview
********

This is a set of Bridle's extension to the original Zephyr upstream board
|zephyr:board:seeeduino_xiao| with some adaptions and improvement on Kconfig
and Devicetree level.

List of extensions
******************

.. rubric:: Kconfig

- :brd:`deactivate` self powered USB explicitly and set the maximum of
  electrical current consumption to :brd:`500㎃`:

  - |CONFIG_USB_SELF_POWERED|
  - |CONFIG_USB_MAX_POWER|

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: Seeeduino XIAO

     * - .. literalinclude:: ../Kconfig.defconfig
            :caption: Kconfig.defconfig
            :language: Kconfig
            :encoding: ISO-8859-1
            :emphasize-lines: 1-2,5-6
            :start-at: config USB_SELF_POWERED
            :end-before: Workaround for not being able to have commas in macro arguments

- :brd:`change` log level and startup delay only in case of use the
  native USB device port :dtcompatible:`atmel,sam0-usb` with CDC-ACM
  UART :dtcompatible:`zephyr,cdc-acm-uart` as Zephyr console:

  - |CONFIG_USB_CDC_ACM_LOG_LEVEL_CHOICE| :=
    |CONFIG_USB_CDC_ACM_LOG_LEVEL_OFF|
  - |CONFIG_USB_DEVICE_LOG_LEVEL_CHOICE| :=
    |CONFIG_USB_DEVICE_LOG_LEVEL_ERR|
  - |CONFIG_LOG_PROCESS_THREAD_STARTUP_DELAY_MS|
  - |CONFIG_BOOT_DELAY|

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: Seeeduino XIAO

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

     * - .. rubric:: Seeeduino XIAO

     * - .. literalinclude:: ../seeeduino_xiao.overlay
            :caption: seeeduino_xiao.overlay
            :language: DTS
            :encoding: ISO-8859-1
            :prepend: / {
            :start-at: model
            :end-at: "atmel,samd21";
            :append: };
