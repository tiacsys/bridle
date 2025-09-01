.. _mimxrt1060_evk-extensions:

NXP MIMXRT1060-EVK
##################

Overview
********

This is a set of Bridle's extension to the original Zephyr upstream board
|zephyr:board:mimxrt1060_evk| with some adaptions and improvement on
Kconfig and Devicetree level.

List of extensions
******************

.. rubric:: Kconfig

- :bbl:`activate` self powered USB explicitly and set the maximum of
  electrical current consumption to :bbl:`0㎃`:

  - |CONFIG_CDC_ACM_SERIAL_SELF_POWERED|
  - |CONFIG_CDC_ACM_SERIAL_MAX_POWER|

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: NXP MIMXRT1060-EVK, MIMXRT1060-EVKB and MIMXRT1060-EVKC

     * - .. literalinclude:: ../Kconfig.defconfig
            :caption: Kconfig.defconfig
            :language: Kconfig
            :encoding: ISO-8859-1
            :emphasize-lines: 1-2,5-7
            :start-at: config CDC_ACM_SERIAL_SELF_POWERED
            :end-before: Logger cannot use itself to log

- :brd:`change` log level only in case of use the native USB device port
  :dtcompatible:`nxp,ehci` with CDC-ACM UART
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

     * - .. rubric:: NXP MIMXRT1060-EVK, MIMXRT1060-EVKB and MIMXRT1060-EVKC

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

     * - .. rubric:: NXP MIMXRT1060-EVK, MIMXRT1060-EVKB and MIMXRT1060-EVKC

     * - .. literalinclude:: ../mimxrt1060_evk.dtsi
            :caption: mimxrt1060_evk.dtsi
            :language: DTS
            :encoding: ISO-8859-1
            :prepend: / {
            :start-at: model
            :end-at: compatible
            :append: };

- FlexPWM not routed to the green user LED ``LED1`` on the EVK **B**
  and **C** revision, thus why board DTS disables :dts:`&flexpwm2_pwm3`
  but neither related :dts:`&pwmleds` node nor alias:

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: NXP MIMXRT1060-EVKB and MIMXRT1060-EVKC

     * - .. literalinclude:: ../mimxrt1060_evk_mimxrt1062_qspi_B.overlay
            :caption: mimxrt1060_evk_mimxrt1062_qspi_B.overlay
            :language: DTS
            :encoding: ISO-8859-1
            :emphasize-lines: 3,6
            :prepend: / {
            :start-at: aliases {
            :end-at: /delete-node/ pwmleds;
            :append: };

         .. literalinclude:: ../mimxrt1060_evk_mimxrt1062_qspi_C.overlay
            :caption: mimxrt1060_evk_mimxrt1062_qspi_C.overlay
            :language: DTS
            :encoding: ISO-8859-1
            :emphasize-lines: 3,6
            :prepend: / {
            :start-at: aliases {
            :end-at: /delete-node/ pwmleds;
            :append: };

- add a :dtcompatible:`zephyr,flash-disk` node linked to the
  :dts:`partition = <&storage_partition>;` with the hard defined
  mass storage disk name :dts:`disk-name = "NAND";`:

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: NXP MIMXRT1060-EVK, MIMXRT1060-EVKB and MIMXRT1060-EVKC

     * - .. literalinclude:: ../mimxrt1060_evk.dtsi
            :caption: mimxrt1060_evk.dtsi
            :language: DTS
            :encoding: ISO-8859-1
            :emphasize-lines: 5
            :prepend: / {
            :start-at: msc_disk0 {
            :end-at: };
            :append: };
