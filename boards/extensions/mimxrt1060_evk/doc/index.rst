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
     :width: 50%
     :widths: 100

     * - .. rubric:: NXP MIMXRT1060-EVK and MIMXRT1060-EVKB

     * - .. literalinclude:: ../Kconfig.defconfig
            :caption: Kconfig.defconfig
            :language: Kconfig
            :encoding: ISO-8859-1
            :emphasize-lines: 1-2,5-7
            :start-at: config USB_SELF_POWERED
            :end-before: Workaround for not being able to have commas in macro arguments

- :brd:`change` log level and startup delay only in case of use the
  native USB device port :dtcompatible:`nxp,ehci` with CDC-ACM UART
  :dtcompatible:`zephyr,cdc-acm-uart` as Zephyr console:

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

     * - .. rubric:: NXP MIMXRT1060-EVK and MIMXRT1060-EVKB

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

     * - .. rubric:: NXP MIMXRT1060-EVK and MIMXRT1060-EVKB

     * - .. literalinclude:: ../mimxrt1060_evk.dtsi
            :caption: mimxrt1060_evk.dtsi
            :language: DTS
            :encoding: ISO-8859-1
            :prepend: / {
            :start-at: model
            :end-at: compatible
            :append: };

- FlexPWM not routed to the green user LED ``LED1`` on the EVK **B**
  revision, thus why board DTS disables :devicetree:`&flexpwm2_pwm3`
  but neither related :devicetree:`&pwmleds` node nor alias:

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: NXP MIMXRT1060-EVKB

     * - .. literalinclude:: ../mimxrt1060_evkb.overlay
            :caption: mimxrt1060_evkb.overlay
            :language: DTS
            :encoding: ISO-8859-1
            :emphasize-lines: 3,6
            :prepend: / {
            :start-at: aliases {
            :end-at: /delete-node/ pwmleds;
            :append: };

- add a :dtcompatible:`zephyr,flash-disk` node linked to the
  :devicetree:`partition = <&storage_partition>;` with the hard defined
  mass storage disk name :devicetree:`disk-name = "NAND";` – also set
  the mass storage disk name hard on Kconfig level by a new board config
  file with :kconfig:option:`CONFIG_MASS_STORAGE_DISK_NAME`:

  .. list-table::
     :align: left
     :width: 50%
     :widths: 100

     * - .. rubric:: NXP MIMXRT1060-EVK and MIMXRT1060-EVKB

     * - .. literalinclude:: ../mimxrt1060_evk.dtsi
            :caption: mimxrt1060_evk.dtsi
            :language: DTS
            :encoding: ISO-8859-1
            :emphasize-lines: 5
            :prepend: / {
            :start-at: msc_disk0 {
            :end-at: };
            :append: };

         .. literalinclude:: ../Kconfig.defconfig
            :caption: Kconfig.defconfig
            :language: Kconfig
            :encoding: ISO-8859-1
            :prepend: #
            :emphasize-lines: 21-22
            :start-at: NOTES for the disk name (CONFIG_MASS_STORAGE_DISK_NAME)
            :end-at: depends on USB_DEVICE_STACK && USB_MASS_STORAGE
