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

  - |CONFIG_CDC_ACM_SERIAL_SELF_POWERED|
  - |CONFIG_CDC_ACM_SERIAL_MAX_POWER|

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
            :start-at: config CDC_ACM_SERIAL_SELF_POWERED
            :end-before: Logger cannot use itself to log

- :brd:`change` log level only in case of use the native USB device port
  :dtcompatible:`atmel,sam0-usb` with CDC-ACM UART
  :dtcompatible:`zephyr,cdc-acm-uart` as Zephyr console:

  - |CONFIG_USBD_CDC_ACM_LOG_LEVEL_CHOICE| :=
    |CONFIG_USBD_CDC_ACM_LOG_LEVEL_OFF|
  - |CONFIG_USBD_LOG_LEVEL_CHOICE| :=
    |CONFIG_USBD_LOG_LEVEL_ERR|
  - |CONFIG_UDC_DRIVER_LOG_LEVEL_CHOICE| :=
    |CONFIG_UDC_DRIVER_LOG_LEVEL_ERR|

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: Seeeduino XIAO

     * - .. literalinclude:: ../Kconfig.defconfig
            :caption: Kconfig.defconfig
            :language: Kconfig
            :encoding: ISO-8859-1
            :lines: -14,23-
            :emphasize-lines: 3-4,16-17,22-23,28-29
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
